"""Private JSON-lines protocol. Debugging uses real CPython line events, no TCP port."""

import ast
import builtins
import io
import itertools
import json
import queue
import sys
import threading
import traceback
import types
from pathlib import Path

from guard import install

WIRE = sys.stdout
INPUT = sys.stdin
COMMANDS = queue.Queue(maxsize=128)
FRAMES = {}
TOTAL_OUTPUT = 0
FILES = {str(Path(name).resolve()): name for name in ("answer.py", "playground.py")}


def emit(kind, **payload):
    WIRE.write(json.dumps({"type": kind, **payload}, ensure_ascii=True) + "\n")
    WIRE.flush()


class Output(io.TextIOBase):
    def __init__(self, level):
        self.level = level
        self.pending = ""

    def write(self, text):
        global TOTAL_OUTPUT
        TOTAL_OUTPUT += len(text)
        if TOTAL_OUTPUT > 65536:
            raise RuntimeError("Console output exceeded 64 KiB. Print fewer values.")
        self.pending += text
        while "\n" in self.pending or len(self.pending) > 2048:
            line, separator, rest = self.pending.partition("\n")
            if not separator:
                line, rest = self.pending[:2048], self.pending[2048:]
            emit("log", level=self.level, text=line[:4096])
            self.pending = rest
        return len(text)

    def flush(self):
        if self.pending:
            emit("log", level=self.level, text=self.pending[:4096])
            self.pending = ""


def safe_value(value, depth=0):
    # Never invoke learner-defined repr/properties/iterators while inspecting a pause.
    kind = type(value)
    if kind in (str, int, float, bool, type(None)):
        if kind is int and value.bit_length() > 1024:
            return "<large int>"
        return repr(value[:160] if kind is str else value)[:240]
    if depth < 2 and kind in (list, tuple):
        items = [safe_value(v, depth + 1) for v in value[:8]]
        return (
            ("[" if kind is list else "(")
            + ", ".join(items)
            + (", …" if len(value) > 8 else "")
            + ("]" if kind is list else ")")
        )
    if depth < 2 and kind is dict:
        return (
            "{"
            + ", ".join(
                safe_value(k, depth + 1) + ": " + safe_value(v, depth + 1)
                for k, v in itertools.islice(value.items(), 8)
            )
            + (", …" if len(value) > 8 else "")
            + "}"
        )
    return "<" + kind.__name__[:80] + ">"


def read_commands():
    for line in INPUT:
        try:
            if len(line) > 8192:
                continue
            COMMANDS.put(json.loads(line))
        except (ValueError, TypeError):
            continue
    COMMANDS.put({"action": "stop"})


def learner_frames(frame):
    global FRAMES
    FRAMES = {}
    frames = []
    while frame and len(frames) < 16:
        if frame.f_code.co_filename in FILES:
            identity = str(id(frame))
            FRAMES[identity] = frame
            variables = []
            for scope, values in (
                ("local", frame.f_locals),
                ("global", frame.f_globals),
            ):
                for name, value in list(values.items())[:64]:
                    if not name.startswith("__") and not any(
                        v["name"] == name for v in variables
                    ):
                        variables.append(
                            {"name": name, "value": safe_value(value), "scope": scope}
                        )
            frames.append(
                {
                    "id": identity,
                    "name": frame.f_code.co_name,
                    "file": FILES[frame.f_code.co_filename],
                    "line": frame.f_lineno,
                    "column": 1,
                    "variables": variables[:64],
                }
            )
        frame = frame.f_back
    return frames


def inspect(command):
    frame = FRAMES.get(command.get("frame"))
    expression = command.get("expression", "")
    try:
        if not frame or len(expression) > 256:
            raise ValueError("Select a live frame and a name or literal value.")
        node = ast.parse(expression, mode="eval").body
        if isinstance(node, ast.Name):
            if node.id in frame.f_locals:
                value = frame.f_locals[node.id]
            elif node.id in frame.f_globals and not node.id.startswith("__"):
                value = frame.f_globals[node.id]
            else:
                raise ValueError("This name is not available in the selected frame.")
        elif isinstance(node, ast.Constant):
            value = node.value
        else:
            raise ValueError(
                "Read-only inspection accepts a variable name or literal; calls and attributes are disabled."
            )
        emit("evaluation", text=safe_value(value))
    except (ValueError, SyntaxError) as error:
        emit("commandError", text=str(error))


def depth(frame):
    count = 0
    while frame:
        count += frame.f_code.co_filename in FILES
        frame = frame.f_back
    return count


class Debugger:
    def __init__(self, request):
        self.mode = "into" if request["debug"] else "continue"
        self.level = 0
        self.breakpoints = request["breakpoints"]

    def trace(self, frame, event, arg):
        if event != "line" or frame.f_code.co_filename not in FILES:
            return self.trace
        while not COMMANDS.empty():
            command = COMMANDS.get_nowait()
            if command["action"] == "stop":
                raise SystemExit("Session stopped")
            if command["action"] == "pause":
                self.mode = "into"
        file = FILES[frame.f_code.co_filename]
        stop = frame.f_lineno in self.breakpoints.get(file, [])
        stop = (
            stop
            or self.mode == "into"
            or (self.mode == "over" and depth(frame) <= self.level)
            or (self.mode == "out" and depth(frame) < self.level)
        )
        if stop:
            emit(
                "paused",
                reason="breakpoint"
                if frame.f_lineno in self.breakpoints.get(file, [])
                else "step",
                frames=learner_frames(frame),
            )
            while True:
                command = COMMANDS.get()
                action = command.get("action")
                if action == "evaluate":
                    inspect(command)
                elif action == "stop":
                    raise SystemExit("Session stopped")
                elif action in ("continue", "over", "into", "out"):
                    self.mode = action
                    self.level = depth(frame)
                    emit("running")
                    break
        return self.trace


def no_input(*args, **kwargs):
    raise RuntimeError(
        "Use explicit function arguments in labs; interactive input() is unavailable."
    )


def main():
    request = json.loads(Path("session.json").read_text())
    codes = {}
    try:
        for file, name in FILES.items():
            codes[name] = compile(Path(file).read_text(), file, "exec")
    except SyntaxError as error:
        emit("problems", text="".join(traceback.format_exception_only(error)))
        emit("finished", success=False)
        return

    def executable_lines(code):
        lines = {line for _, _, line in code.co_lines() if line and line > 0}
        for constant in code.co_consts:
            if isinstance(constant, types.CodeType):
                lines.update(executable_lines(constant))
        return lines

    bound = {}
    for name, requested in request["breakpoints"].items():
        if name not in codes:
            continue
        available = sorted(executable_lines(codes[name]))
        bound[name] = []
        for line in requested:
            actual = next(
                (candidate for candidate in available if candidate >= line), None
            )
            if actual is None:
                emit(
                    "commandError", text=f"No executable line at or after {name}:{line}"
                )
            else:
                bound[name].append(actual)
                emit("breakpoint", file=name, requested=line, line=actual)
    request["breakpoints"] = bound
    threading.Thread(target=read_commands, daemon=True).start()
    sys.stdout = Output("log")
    sys.stderr = Output("error")
    builtins.input = no_input
    install()
    debugger = Debugger(request)
    emit("running")
    module = types.ModuleType("answer")
    module.__file__ = str(Path("answer.py").resolve())
    sys.modules["answer"] = module
    try:
        sys.settrace(debugger.trace)
        exec(codes["answer.py"], module.__dict__)
        exec(
            codes["playground.py"],
            {"__name__": "__main__", "__file__": str(Path("playground.py").resolve())},
        )
    except BaseException as error:
        sys.settrace(None)
        trace = traceback.TracebackException.from_exception(error, limit=10)
        trace.stack = traceback.StackSummary.from_list(
            entry
            for entry in trace.stack
            if Path(entry.filename).name not in {"bridge.py", "<string>"}
        )
        emit(
            "log",
            level="error",
            text="".join(trace.format())[-8000:].replace(str(Path.cwd()) + "/", ""),
        )
        emit("finished", success=False)
    else:
        sys.settrace(None)
        sys.stdout.flush()
        sys.stderr.flush()
        emit("finished", success=True)


if __name__ == "__main__":
    main()
