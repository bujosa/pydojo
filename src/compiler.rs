//! Real Python behavioral checks. Only this adapter may credit lab completion.
use crate::{
    course::Lesson,
    tooling::{self, Work},
};
use std::{
    fs,
    process::Stdio,
    time::{Duration, Instant},
};
#[derive(serde::Deserialize)]
pub struct Report {
    pub passed: bool,
    pub text: String,
}
pub fn check(lesson: &Lesson, source: &str) -> Result<Report, String> {
    if source.len() > 128 * 1024 {
        return Err("Answers are limited to 128 KiB.".into());
    }
    let work = Work::new("check")?;
    work.guard()?;
    work.write("contracts.py", include_str!("../runtime/contracts.py"))?;
    work.write("answer.py", source)?;
    work.write(
        "checks.py",
        format!("{}\n{}", lesson.checks, lesson.runtime),
    )?;
    work.write("check.py", include_str!("../runtime/check.py"))?;
    let log = fs::File::create(work.0.join("error.log")).map_err(|e| e.to_string())?;
    let mut child = tooling::python(&work, "check.py")?
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(log)
        .spawn()
        .map_err(|e| format!("Python could not start: {e}"))?;
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
            return Ok(Report {
                passed: false,
                text: "Check exceeded 5 seconds. Look for an infinite loop or blocking call."
                    .into(),
            });
        }
        std::thread::sleep(Duration::from_millis(10));
    };
    let result = work.0.join("result.json");
    if !status.success() || !result.is_file() {
        return Ok(Report {
            passed: false,
            text: format!(
                "Python ended before checks completed ({status}). Do not terminate the process from an answer.\n{}",
                fs::read_to_string(work.0.join("error.log"))
                    .unwrap_or_default()
                    .chars()
                    .take(4096)
                    .collect::<String>()
            ),
        });
    }
    if fs::metadata(&result).map_err(|e| e.to_string())?.len() > 32 * 1024 {
        return Err("Check report exceeded 32 KiB.".into());
    }
    serde_json::from_slice(&fs::read(result).map_err(|e| e.to_string())?).map_err(|e| e.to_string())
}
pub fn verify(lessons: &[Lesson]) -> Result<(), String> {
    let mut count = 0;
    for lesson in lessons {
        for (name, source, expected) in [
            ("starter", lesson.starter.as_str(), false),
            ("solution", &lesson.solution, true),
            ("alternative", &lesson.alternative, true),
            ("empty", "", false),
            ("unrelated", "unrelated = 1\n", false),
            ("negative", &lesson.negative, false),
        ] {
            let report = check(lesson, source)?;
            if report.passed != expected {
                return Err(format!(
                    "{} / {name}: unexpected result\n{}",
                    lesson.id, report.text
                ));
            }
            count += 1;
        }
        println!("{}: six behavioral contract cases passed", lesson.id);
    }
    println!("Verified {count} cases.");
    Ok(())
}
#[cfg(test)]
mod tests {
    #[test]
    fn checks_reject_syntax_errors_exceptions_and_process_exit() {
        let lesson = crate::course::load().unwrap().remove(0);
        for source in [
            "def broken(:",
            "raise ValueError('broken')",
            "raise SystemExit(0)",
            "import os; os._exit(0)",
        ] {
            assert!(!super::check(&lesson, source).unwrap().passed);
        }
    }
    #[test]
    fn guard_blocks_external_files_network_processes_and_output_floods() {
        let mut lesson = crate::course::load().unwrap().remove(0);
        lesson.checks = "assert True".into();
        lesson.runtime.clear();
        for source in [
            "open('/etc/passwd').read()",
            "import socket; socket.socket()",
            "import subprocess; subprocess.run(['/usr/bin/true'])",
            "print('x' * 70000)",
        ] {
            assert!(!super::check(&lesson, source).unwrap().passed, "{source}");
        }
    }
}
