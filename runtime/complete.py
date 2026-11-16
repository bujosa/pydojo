"""Static Jedi Script completion in the two-file educational workspace."""

import json
import pathlib
import sys

sys.path.insert(0, sys.argv[-1])
import jedi
from jedi.api.environment import InterpreterEnvironment

request = json.loads(pathlib.Path("request.json").read_text())
source = request["source"]
file = request["file"]
sibling = "playground.py" if file == "answer.py" else "answer.py"
pathlib.Path(file).write_text(source)
pathlib.Path(sibling).write_text(request["sibling"])
before = source[: request["cursor"]]
line = before.count("\n") + 1
column = len(before.rsplit("\n", 1)[-1])
# Script analyzes text. InterpreterEnvironment keeps trusted stdlib inference in-process.
# Never use jedi.Interpreter on learner objects or import the learner module.
project = jedi.Project(
    path=".",
    sys_path=[str(pathlib.Path.cwd()), *sys.path],
    smart_sys_path=False,
    load_unsafe_extensions=False,
)
# Restrict inference reads to this workspace, the bundled stdlib and completion tools.
# These are educational guards; they are not a hostile-code sandbox.
import os
import resource

roots = [
    pathlib.Path.cwd().resolve(),
    pathlib.Path(sys.prefix).resolve(),
    pathlib.Path(sys.argv[-1]).resolve(),
]


def allowed(value, write=False):
    if isinstance(value, int):
        return True
    path = pathlib.Path(value).resolve()
    return (
        any(path.is_relative_to(root) for root in roots[:1] if write)
        if write
        else any(path.is_relative_to(root) for root in roots)
    )


def audit(event, args):
    if event == "open":
        writing = bool(args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if not allowed(args[0], writing):
            raise PermissionError("Completion access outside its workspace")
    if event.startswith(("socket.", "subprocess.", "ctypes.")) or event in {
        "os.system",
        "os.fork",
        "os.posix_spawn",
        "os.exec",
        "os.symlink",
        "os.link",
    }:
        raise PermissionError("Completion cannot start processes or network operations")
    if (
        event
        in {
            "os.listdir",
            "os.scandir",
            "os.mkdir",
            "os.remove",
            "os.rmdir",
            "os.chdir",
            "os.chmod",
        }
        and args
        and args[0] is not None
    ):
        if not allowed(args[0], event not in {"os.listdir", "os.scandir"}):
            raise PermissionError("Completion path is outside its workspace")


resource.setrlimit(resource.RLIMIT_CPU, (4, 4))
resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
sys.addaudithook(audit)
script = jedi.Script(
    code=source, path=file, project=project, environment=InterpreterEnvironment()
)
entries = []
for entry in [e for e in script.complete(line, column) if e.complete][:32]:
    prefix = entry.name[: len(entry.name) - len(entry.complete)]
    start = request["cursor"] - len(prefix)
    end = request["cursor"]
    while end < len(source) and (source[end].isalnum() or source[end] == "_"):
        end += 1
    entries.append(
        dict(
            label=entry.name,
            kind=entry.type,
            detail=entry.description[:350],
            insert=entry.name,
            start=start,
            end=end,
        )
    )
pathlib.Path("result.json").write_text(json.dumps(entries))
