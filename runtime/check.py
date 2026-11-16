"""Behavioral grading, separate from interactive Run/Debug."""

import contextlib
import io
import json
import sys
import traceback
import types
from pathlib import Path
from guard import install
import contracts


class CappedOutput(io.TextIOBase):
    def __init__(self):
        self.count = 0

    def write(self, text):
        self.count += len(text)
        if self.count > 65536:
            raise RuntimeError("Output exceeded 64 KiB. Remove noisy prints and retry.")
        return len(text)


def main():
    source = Path("answer.py").read_text()
    checks = Path("checks.py").read_text()
    result = Path("result.json")
    install()
    module = types.ModuleType("answer")
    module.__file__ = str(Path("answer.py").resolve())
    sys.modules["answer"] = module
    try:
        with (
            contextlib.redirect_stdout(CappedOutput()),
            contextlib.redirect_stderr(CappedOutput()),
        ):
            exec(compile(source, module.__file__, "exec"), module.__dict__)
            exec(
                compile(checks, "checks.py", "exec"),
                {
                    "s": module,
                    **{
                        name: value
                        for name, value in vars(contracts).items()
                        if not name.startswith("_")
                    },
                },
            )
    except BaseException as error:
        trace = traceback.TracebackException.from_exception(error, limit=8)
        trace.stack = traceback.StackSummary.from_list(
            entry
            for entry in trace.stack
            if Path(entry.filename).name in {"answer.py", "checks.py"}
        )
        report = {
            "passed": False,
            "text": "Not yet. Read the failed assertion or Python traceback below.\n\n"
            + "".join(trace.format())[-12000:].replace(str(Path.cwd()) + "/", ""),
        }
    else:
        report = {
            "passed": True,
            "text": "Behavior checks passed for this exact answer. Try your own inputs in the playground, too.",
        }
    result.write_text(json.dumps(report))


if __name__ == "__main__":
    main()
