"""Required local gates. Never touches installed apps or learner data."""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMANDS = [
    ["cargo", "fmt", "--check"],
    ["cargo", "clippy", "--all-targets", "--", "-D", "warnings"],
    ["cargo", "test", "--locked"],
    ["cargo", "run", "--locked", "--", "--verify-art"],
    ["cargo", "run", "--locked", "--", "--verify-content"],
    ["cargo", "run", "--locked", "--", "--verify-learning"],
    [
        "target/toolchain/python/bin/python3.13",
        "-I",
        "-B",
        "-m",
        "unittest",
        "discover",
        "-s",
        "runtime",
        "-p",
        "test_*.py",
    ],
    ["python3", "tools/format_content.py"],
    [
        "target/toolchain/ruff/ruff",
        "format",
        "--check",
        "--isolated",
        "runtime",
        "scripts",
        "tools",
    ],
]
for command in COMMANDS:
    print("Running:", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)
print("All local gates passed.")
