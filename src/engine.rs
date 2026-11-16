//! Local process owner for the IDE. No completion authority: only compiler::check credits labs.
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::{
    collections::{BTreeMap, BTreeSet},
    fs,
    io::{BufRead, BufReader, Read, Write},
    process::{Child, Stdio},
    sync::mpsc::{self, Receiver, Sender, SyncSender},
    time::{Duration, Instant},
};

pub const PLAYGROUND: &str = "import answer\n\n# Call your functions here and inspect values with print().\nprint({name: value for name, value in vars(answer).items() if not name.startswith('_')})\n";
pub type Breakpoints = BTreeMap<String, BTreeSet<usize>>;
#[derive(Clone, Debug, Deserialize)]
pub struct Variable {
    pub name: String,
    pub value: String,
    pub scope: String,
}
#[derive(Clone, Debug, Deserialize)]
pub struct Frame {
    pub id: String,
    pub name: String,
    pub file: String,
    pub line: usize,
    pub column: usize,
    pub variables: Vec<Variable>,
}
#[derive(Debug, Deserialize)]
#[serde(tag = "type")]
pub enum Event {
    #[serde(rename = "running")]
    Running,
    #[serde(rename = "pausing")]
    Pausing,
    #[serde(rename = "paused")]
    Paused { reason: String, frames: Vec<Frame> },
    #[serde(rename = "log")]
    Log { level: String, text: String },
    #[serde(rename = "evaluation")]
    Evaluation { text: String },
    #[serde(rename = "commandError")]
    CommandError { text: String },
    #[serde(rename = "breakpoint")]
    Breakpoint {
        file: String,
        requested: usize,
        line: usize,
    },
    #[serde(rename = "finished")]
    Finished { success: bool },
    #[serde(rename = "failure")]
    Failure { text: String },
    #[serde(rename = "problems")]
    Problems { text: String },
    #[serde(rename = "stopped")]
    Stopped,
}
#[derive(Serialize)]
pub struct Request {
    pub debug: bool,
    pub breakpoints: Breakpoints,
    #[serde(skip)]
    pub answer: String,
    #[serde(skip)]
    pub playground: String,
}
pub struct Session {
    pub events: Receiver<Event>,
    commands: Sender<Value>,
}
impl Session {
    pub fn start(request: Request) -> Self {
        let (commands, input) = mpsc::channel();
        let (output, events) = mpsc::sync_channel(128);
        std::thread::spawn(move || {
            if let Err(text) = run(request, &input, &output) {
                let _ = output.send(Event::Failure { text });
            }
        });
        Self { events, commands }
    }
    pub fn command(&self, action: &str) {
        let _ = self.commands.send(json!({"action":action}));
    }
    pub fn evaluate(&self, frame: &str, expression: &str) {
        let _ = self
            .commands
            .send(json!({"action":"evaluate", "frame":frame, "expression":expression}));
    }
}
impl Drop for Session {
    fn drop(&mut self) {
        self.command("stop");
    }
}
struct Process(Child);
impl Drop for Process {
    fn drop(&mut self) {
        let _ = self.0.kill();
        let _ = self.0.wait();
    }
}
fn send(output: &SyncSender<Event>, event: Event) -> Result<(), String> {
    output.send(event).map_err(|_| "Workspace closed".into())
}
fn run(
    request: Request,
    input: &Receiver<Value>,
    output: &SyncSender<Event>,
) -> Result<(), String> {
    if request.answer.len() > 128 * 1024
        || request.playground.len() > 128 * 1024
        || request.answer.lines().count() > 4000
        || request.playground.lines().count() > 4000
    {
        return Err("Each workspace file is limited to 128 KiB and 4,000 lines.".into());
    }
    let work = crate::tooling::Work::new("ide")?;
    work.guard()?;
    for (name, content) in [
        ("answer.py", request.answer.as_str()),
        ("playground.py", request.playground.as_str()),
        ("bridge.py", include_str!("../runtime/bridge.py")),
    ] {
        work.write(name, content)?;
    }
    work.write(
        "session.json",
        serde_json::to_vec(&request).map_err(|e| e.to_string())?,
    )?;
    let stderr = fs::File::create(work.0.join("python.log")).map_err(|e| e.to_string())?;
    let mut child = Process(
        crate::tooling::python(&work, "bridge.py")?
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(stderr)
            .spawn()
            .map_err(|e| format!("Python could not start: {e}"))?,
    );
    let stdout = child.0.stdout.take().ok_or("Runtime output unavailable")?;
    let mut stdin = child.0.stdin.take().ok_or("Runtime input unavailable")?;
    let (lines_tx, lines_rx) = mpsc::sync_channel(64);
    std::thread::spawn(move || {
        let mut reader = BufReader::new(stdout);
        loop {
            let mut bytes = Vec::new();
            let read = (&mut reader).take(64 * 1024).read_until(b'\n', &mut bytes);
            match read {
                Ok(0) | Err(_) => break,
                Ok(_) => {
                    if bytes.last() != Some(&b'\n') {
                        let _ = lines_tx.send(Err("Runtime message exceeded 64 KiB".to_string()));
                        break;
                    }
                    if lines_tx
                        .send(
                            serde_json::from_slice::<Event>(&bytes)
                                .map_err(|e| format!("Runtime protocol error: {e}")),
                        )
                        .is_err()
                    {
                        break;
                    }
                }
            }
        }
    });
    let started = Instant::now();
    let mut active = Duration::ZERO;
    let mut last = Instant::now();
    let mut paused = false;
    loop {
        let now = Instant::now();
        if !paused {
            active += now.duration_since(last);
        }
        last = now;
        while let Ok(command) = input.try_recv() {
            if command["action"] == "stop" {
                let _ = child.0.kill();
                let _ = child.0.wait();
                return send(output, Event::Stopped);
            }
            writeln!(stdin, "{command}").map_err(|e| e.to_string())?;
            stdin.flush().map_err(|e| e.to_string())?;
        }
        while let Ok(event) = lines_rx.try_recv() {
            let event = event?;
            match &event {
                Event::Paused { .. } | Event::Pausing => paused = true,
                Event::Running => paused = false,
                Event::Finished { .. } | Event::Failure { .. } => {
                    // Reap before declaring completion so no process or temp files outlive a result.
                    let _ = child.0.kill();
                    let _ = child.0.wait();
                    return send(output, event);
                }
                _ => {}
            }
            send(output, event)?;
        }
        if active > Duration::from_secs(5) {
            return Err("Execution exceeded 5 seconds of running time. Check for an infinite loop, or use Stop.".into());
        }
        if started.elapsed() > Duration::from_secs(600) {
            return Err(
                "Debug session reached its 10-minute limit. Start another session to continue."
                    .into(),
            );
        }
        if let Some(status) = child.0.try_wait().map_err(|e| e.to_string())? {
            // The reader may still be draining stdout after process exit.
            match lines_rx.recv_timeout(Duration::from_millis(100)) {
                Ok(Ok(event)) => {
                    let terminal = matches!(event, Event::Finished { .. } | Event::Failure { .. });
                    send(output, event)?;
                    if terminal {
                        return Ok(());
                    }
                }
                Ok(Err(e)) => return Err(e),
                Err(_) => {
                    let mut bytes = Vec::new();
                    fs::File::open(work.0.join("python.log"))
                        .map_err(|e| e.to_string())?
                        .take(4096)
                        .read_to_end(&mut bytes)
                        .map_err(|e| e.to_string())?;
                    return Err(format!(
                        "Runtime exited unexpectedly ({status}). {}",
                        String::from_utf8_lossy(&bytes)
                    ));
                }
            }
        }
        std::thread::sleep(Duration::from_millis(15));
    }
}

#[cfg(test)]
#[allow(clippy::panic)]
mod tests {
    use super::*;
    fn request(answer: &str, playground: &str, debug: bool) -> Request {
        Request {
            answer: answer.into(),
            playground: playground.into(),
            debug,
            breakpoints: Default::default(),
        }
    }
    fn next(session: &Session) -> Event {
        session
            .events
            .recv_timeout(Duration::from_secs(15))
            .unwrap()
    }
    #[test]
    fn real_python_streams_logs_and_reports_syntax_and_runtime_failures() {
        let session = Session::start(request(
            "value = 42",
            "import answer\nprint('answer', answer.value)",
            false,
        ));
        let mut log = false;
        loop {
            match next(&session) {
                Event::Log { text, .. } => log |= text.contains("answer 42"),
                Event::Finished { success } => {
                    assert!(success);
                    break;
                }
                Event::Failure { text } => panic!("{text}"),
                _ => {}
            }
        }
        assert!(log);
        for (answer, syntax) in [
            ("def broken(:", true),
            ("raise ValueError('broken')", false),
        ] {
            let session = Session::start(request(answer, "", false));
            let mut problem = false;
            loop {
                match next(&session) {
                    Event::Problems { text } => {
                        problem = true;
                        assert!(text.contains("SyntaxError"));
                    }
                    Event::Finished { success } => {
                        assert!(!success);
                        break;
                    }
                    Event::Failure { text } => panic!("{text}"),
                    _ => {}
                }
            }
            assert_eq!(problem, syntax);
        }
    }
    #[test]
    fn real_debugger_steps_evaluates_binds_breakpoints_and_stops() {
        let mut request = request(
            "def double(value):\n    result = value * 2\n    return result\n",
            "import answer\nvalue = answer.double(3)\nprint(value)",
            true,
        );
        request.breakpoints.insert("answer.py".into(), [3].into());
        let session = Session::start(request);
        let mut pauses = 0;
        let mut inspected = false;
        loop {
            match next(&session) {
                Event::Paused { frames, .. } => {
                    pauses += 1;
                    let frame = &frames[0];
                    if frame.file == "answer.py" && frame.line == 3 {
                        session.evaluate(&frame.id, "result");
                        inspected = true;
                    } else if pauses == 1 {
                        session.command("into");
                    } else {
                        session.command("continue");
                    }
                }
                Event::Evaluation { text } => {
                    assert_eq!(text, "6");
                    session.evaluate("invalid", "result");
                }
                Event::CommandError { text } => {
                    assert!(text.contains("live frame"));
                    session.command("stop");
                }
                Event::Stopped => break,
                Event::Failure { text } => panic!("{text}"),
                Event::Finished { .. } => panic!("debugger missed breakpoint"),
                _ => {}
            }
        }
        assert!(inspected && pauses >= 2);
    }
    #[test]
    fn loop_timeout_output_limit_and_cancel_are_terminal() {
        for (source, needle) in [
            ("while True: pass", "5 seconds"),
            ("print('x' * 70000)", "output exceeded"),
        ] {
            let session = Session::start(request(source, "", false));
            let mut evidence = false;
            loop {
                match next(&session) {
                    Event::Log { text, .. } => evidence |= text.contains(needle),
                    Event::Failure { text } => {
                        assert!(text.contains(needle), "{text}");
                        evidence = true;
                        break;
                    }
                    Event::Finished { success } => {
                        assert!(!success);
                        break;
                    }
                    _ => {}
                }
            }
            assert!(evidence);
        }
        let session = Session::start(request("while True: pass", "", false));
        session.command("stop");
        loop {
            match next(&session) {
                Event::Stopped => break,
                Event::Failure { text } => panic!("{text}"),
                _ => {}
            }
        }
    }
}
