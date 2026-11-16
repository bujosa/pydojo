//! Process and scratch-directory boundary shared by the Python adapters.
use std::{
    fs,
    path::{Path, PathBuf},
    process::Command,
    sync::atomic::{AtomicU64, Ordering},
    time::{SystemTime, UNIX_EPOCH},
};
pub struct Work(pub PathBuf);
impl Work {
    pub fn new(purpose: &str) -> Result<Self, String> {
        static NEXT: AtomicU64 = AtomicU64::new(0);
        let tick = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_err(|e| e.to_string())?
            .as_nanos();
        let root = std::env::temp_dir().join(format!(
            "pydojo-{purpose}-{}-{tick}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        fs::create_dir(&root).map_err(|e| e.to_string())?;
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            fs::set_permissions(&root, fs::Permissions::from_mode(0o700))
                .map_err(|e| e.to_string())?;
        }
        Ok(Self(root))
    }
    pub fn write(&self, name: &str, bytes: impl AsRef<[u8]>) -> Result<(), String> {
        fs::write(self.0.join(name), bytes).map_err(|e| e.to_string())
    }
    pub fn guard(&self) -> Result<(), String> {
        self.write("guard.py", include_str!("../runtime/guard.py"))
    }
}
impl Drop for Work {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn executable(variable: &str, relative: &str) -> Result<PathBuf, String> {
    if let Some(path) = std::env::var_os(variable) {
        return Ok(path.into());
    }
    let executable = std::env::current_exe().map_err(|e| e.to_string())?;
    let bundle = executable
        .parent()
        .and_then(Path::parent)
        .map(|p| p.join("Resources").join(relative));
    if let Some(path) = bundle.filter(|p| p.is_file()) {
        return Ok(path);
    }
    #[cfg(debug_assertions)]
    {
        let dev = Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("target/toolchain")
            .join(relative);
        if dev.is_file() {
            return Ok(dev);
        }
    }
    Err(format!(
        "Bundled toolchain missing. Developers: run python3 scripts/toolchain.py or set {variable} to an absolute executable path."
    ))
}
pub fn python(work: &Work, script: &str) -> Result<Command, String> {
    let mut command = Command::new(executable("PYDOJO_PYTHON", "python/bin/python3.13")?);
    command.args(["-I","-u","-B","-c","import runpy,sys; sys.path.insert(0, '.'); runpy.run_path(sys.argv[1], run_name='__main__')",script]);
    isolate(&mut command, work);
    Ok(command)
}
pub fn ruff(work: &Work) -> Result<Command, String> {
    let mut command = Command::new(executable("PYDOJO_RUFF", "ruff/ruff")?);
    isolate(&mut command, work);
    Ok(command)
}
fn isolate(command: &mut Command, work: &Work) {
    command
        .current_dir(&work.0)
        .env_clear()
        .env("HOME", &work.0)
        .env("TMPDIR", &work.0)
        .env("PATH", "/usr/bin:/bin")
        .env("LANG", "en_US.UTF-8");
}
