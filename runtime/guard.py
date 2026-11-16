"""Limits for trusted educational code. This is not a hostile-code sandbox."""

import os
import resource
import sys
from pathlib import Path

ROOT = Path.cwd().resolve()
STDLIB = Path(os.__file__).resolve().parent


def inside(path, root):
    try:
        Path(path).resolve().relative_to(root)
        return True
    except (ValueError, TypeError, OSError):
        return False


def audit(event, args):
    if event == "open":
        path, mode, flags = args
        if isinstance(path, int):
            return
        writing = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if not inside(path, ROOT) and (writing or not inside(path, STDLIB)):
            raise PermissionError(
                "Labs can access only their scratch directory and Python's library."
            )
    if event == "socket.__new__" and args[1] == 1:
        return  # asyncio uses a local socketpair for wakeups; connect/bind remain prohibited.
    if event.startswith(("socket.", "subprocess.", "ctypes.")) or event in {
        "os.system",
        "os.fork",
        "os.forkpty",
        "os.posix_spawn",
        "os.exec",
        "os.kill",
        "os.killpg",
        "os.symlink",
        "os.link",
        "os.putenv",
        "os.unsetenv",
    }:
        raise PermissionError(f"{event} is unavailable in the learning workspace.")
    if event in {
        "os.remove",
        "os.rmdir",
        "os.mkdir",
        "os.chmod",
        "os.chdir",
        "os.listdir",
        "os.scandir",
    }:
        if args and args[0] is not None and not isinstance(args[0], int):
            if not inside(args[0], ROOT) and not (
                event in {"os.listdir", "os.scandir"} and inside(args[0], STDLIB)
            ):
                raise PermissionError("This path is outside the learning workspace.")
    if event == "os.rename" and not all(inside(p, ROOT) for p in args[:2]):
        raise PermissionError("Renames must stay inside the learning workspace.")


def install():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))
    resource.setrlimit(resource.RLIMIT_CPU, (8, 8))
    sys.addaudithook(audit)
