//! Pinned Ruff formats data, never executes learner code. The UI guards replacement snapshots.
use crate::tooling::{self, Work};
use std::{
    fs,
    process::Stdio,
    time::{Duration, Instant},
};
pub const VERSION: &str = "0.12.5";
pub struct Formatted {
    pub source: String,
    pub breakpoints: std::collections::BTreeSet<usize>,
}
pub fn format(
    source: &str,
    breakpoints: &std::collections::BTreeSet<usize>,
) -> Result<Formatted, String> {
    if source.len() > 128 * 1024 {
        return Err("Format supports files up to 128 KiB.".into());
    }
    let work = Work::new("format")?;
    work.write("input.py", source)?;
    let log = fs::File::create(work.0.join("error.log")).map_err(|e| e.to_string())?;
    let mut child = tooling::ruff(&work)?
        .args([
            "format",
            "--isolated",
            "--no-cache",
            "--target-version",
            "py313",
            "--quiet",
            "input.py",
        ])
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(log)
        .spawn()
        .map_err(|e| format!("Ruff could not start: {e}. Your code was preserved."))?;
    let start = Instant::now();
    let status = loop {
        match child.try_wait() {
            Ok(Some(s)) => break s,
            Ok(None) => {}
            Err(e) => {
                let _ = child.kill();
                let _ = child.wait();
                return Err(e.to_string());
            }
        }
        if start.elapsed() > Duration::from_secs(5) {
            let _ = child.kill();
            let _ = child.wait();
            return Err("Formatting timed out. Your code was preserved.".into());
        }
        std::thread::sleep(Duration::from_millis(10));
    };
    if !status.success() {
        return Err(format!(
            "Ruff could not format this code. Fix its syntax and retry.\n{}",
            fs::read_to_string(work.0.join("error.log"))
                .unwrap_or_default()
                .chars()
                .take(4096)
                .collect::<String>()
        ));
    }
    let path = work.0.join("input.py");
    if fs::metadata(&path).map_err(|e| e.to_string())?.len() > 256 * 1024 {
        return Err("Formatted output exceeded 256 KiB.".into());
    }
    let formatted = fs::read_to_string(path).map_err(|e| e.to_string())?;
    let points = if formatted == source {
        breakpoints.clone()
    } else {
        Default::default()
    };
    Ok(Formatted {
        source: formatted,
        breakpoints: points,
    })
}
#[cfg(test)]
mod tests {
    #[test]
    fn real_ruff_is_idempotent_and_rejects_invalid_syntax() {
        let raw = "def greet(name:str):\n return {'hello':name,'ok':True}\n";
        let out = super::format(raw, &[2].into()).unwrap();
        assert!(out.source.contains("def greet(name: str):"));
        assert!(out.breakpoints.is_empty());
        assert_eq!(
            out.source,
            super::format(&out.source, &Default::default())
                .unwrap()
                .source
        );
        assert!(super::format("def broken(:", &Default::default()).is_err());
        let points = [2].into();
        assert_eq!(
            super::format(&out.source, &points).unwrap().breakpoints,
            points
        );
    }
}
