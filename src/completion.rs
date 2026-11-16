//! Snapshot-based language assistance. It cannot execute a lesson or credit progress.
use serde::{Deserialize, Serialize};
use std::{
    fs,
    io::Read,
    path::PathBuf,
    process::Stdio,
    time::{Duration, Instant, SystemTime, UNIX_EPOCH},
};
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct Request {
    pub id: String,
    pub file: String,
    pub source: String,
    pub sibling: String,
    pub cursor: usize,
}
#[derive(Clone, Debug, Deserialize)]
pub struct Entry {
    pub label: String,
    pub kind: String,
    pub detail: String,
    pub insert: String,
    pub start: usize,
    pub end: usize,
}
impl Entry {
    pub fn apply(&self, request: &Request) -> Result<(String, usize), String> {
        let n = request.source.chars().count();
        if self.start > request.cursor
            || self.end < request.cursor
            || self.end > n
            || self.insert.len() > 256
            || self.insert.contains(['\n', '\r'])
        {
            return Err("Invalid suggestion range".into());
        }
        let before: String = request.source.chars().take(self.start).collect();
        let after: String = request.source.chars().skip(self.end).collect();
        Ok((
            format!("{before}{}{after}", self.insert),
            self.start + self.insert.chars().count(),
        ))
    }
}
struct Work(PathBuf);
impl Drop for Work {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
pub fn query(request: &Request) -> Result<Vec<Entry>, String> {
    if !FILES.contains(&request.file.as_str())
        || request.source.len() > 128 * 1024
        || request.sibling.len() > 128 * 1024
        || request.cursor > request.source.chars().count()
    {
        return Err("Suggestions support workspace files up to 128 KiB.".into());
    }
    static NEXT: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
    let seq = NEXT.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
    let tick = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_err(|e| e.to_string())?
        .as_nanos();
    let work = Work(
        std::env::temp_dir().join(format!("dojo-complete-{}-{tick}-{seq}", std::process::id())),
    );
    fs::create_dir(&work.0).map_err(|e| e.to_string())?;
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        fs::set_permissions(&work.0, fs::Permissions::from_mode(0o700))
            .map_err(|e| e.to_string())?;
    }
    fs::write(
        work.0.join("request.json"),
        serde_json::to_vec(request).map_err(|e| e.to_string())?,
    )
    .map_err(|e| e.to_string())?;
    fs::write(
        work.0.join("complete.py"),
        include_str!("../runtime/complete.py"),
    )
    .map_err(|e| e.to_string())?;
    let tools = crate::tooling::resource("PYDOJO_COMPLETION_TOOLS", "completion")?;
    let mut command = crate::tooling::python_at(&work.0, "complete.py")?;
    command.arg(tools);
    let log = fs::File::create(work.0.join("error.log")).map_err(|e| e.to_string())?;
    let mut child = command
        .current_dir(&work.0)
        .env_clear()
        .env("HOME", &work.0)
        .env("TMPDIR", &work.0)
        .env("PATH", "/usr/bin:/bin")
        .env("LANG", "en_US.UTF-8")
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(log)
        .spawn()
        .map_err(|e| format!("Suggestions unavailable: {e}"))?;
    let start = Instant::now();
    let result = (|| {
        loop {
            if let Some(status) = child.try_wait().map_err(|e| e.to_string())? {
                if status.success() {
                    break;
                } else {
                    return Err("Suggestions unavailable. Retry with Suggest.".into());
                }
            }
            if start.elapsed() > Duration::from_secs(5)
                || fs::metadata(work.0.join("error.log")).is_ok_and(|m| m.len() > 65536)
            {
                return Err("Suggestions timed out. Keep typing or retry.".into());
            }
            std::thread::sleep(Duration::from_millis(15));
        }
        let mut bytes = Vec::new();
        fs::File::open(work.0.join("result.json"))
            .map_err(|e| e.to_string())?
            .take(128 * 1024 + 1)
            .read_to_end(&mut bytes)
            .map_err(|e| e.to_string())?;
        if bytes.len() > 128 * 1024 {
            return Err("Suggestion response exceeded its limit.".into());
        }
        let entries: Vec<Entry> = serde_json::from_slice(&bytes).map_err(|e| e.to_string())?;
        Ok(entries
            .into_iter()
            .filter(|e| {
                e.label.len() <= 160
                    && e.kind.len() <= 80
                    && e.detail.len() <= 1500
                    && e.apply(request).is_ok()
            })
            .take(32)
            .collect())
    })();
    let _ = child.kill();
    let _ = child.wait();
    result
}

const FILES: &[&str] = &["answer.py", "playground.py"];

pub fn verify() -> Result<(), String> {
    let source = "name = 'Ada'\nname.upp".to_owned();
    let request = Request {
        id: "verify-completion".into(),
        file: "answer.py".into(),
        cursor: source.chars().count(),
        source,
        sibling: String::new(),
    };
    if !query(&request)?.iter().any(|e| e.label == "upper") {
        return Err("Bundled Python completion did not return upper.".into());
    }
    println!("Bundled semantic completion verified.");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    fn request(source: &str, sibling: &str) -> Request {
        let cursor = source.chars().position(|c| c == '|').unwrap();
        Request {
            id: "isolated-test".into(),
            file: "answer.py".into(),
            source: source.replace('|', ""),
            sibling: sibling.into(),
            cursor,
        }
    }
    #[test]
    fn rejects_invalid_files_and_cursor_without_starting_tools() {
        let mut r = request("he|", "");
        r.file = "../outside".into();
        assert!(query(&r).is_err());
        r.file = "answer.py".into();
        r.cursor = 99;
        assert!(query(&r).is_err());
    }
    #[test]
    fn completes_inferred_members_with_unicode_and_replaces_the_whole_identifier()
    -> Result<(), String> {
        let r = request("emoji = '🧪'\nname = 'Ada'\nname.upp|er", "");
        let entries = query(&r)?;
        let e = entries
            .iter()
            .find(|e| e.label == "upper")
            .ok_or("missing inferred string member")?;
        let (after, cursor) = e.apply(&r)?;
        assert!(after.ends_with("name.upper"));
        assert_eq!(after.chars().count(), cursor);
        assert!(after.contains("🧪"));
        Ok(())
    }
    #[test]
    fn completes_cross_file_exports_without_running_side_effects() -> Result<(), String> {
        let marker = std::env::temp_dir().join(format!(
            "pydojo-no-completion-execution-{}",
            std::process::id()
        ));
        assert!(!marker.exists());
        let sibling = format!(
            "from pathlib import Path\nPath({:?}).write_text('executed')\ndef greet(name: str) -> str:\n    return name\n",
            marker.to_string_lossy()
        );
        let mut r = request("import answer\nanswer.gre|", &sibling);
        r.file = "playground.py".into();
        assert!(query(&r)?.iter().any(|e| e.label == "greet"));
        assert!(!marker.exists());
        Ok(())
    }
}
