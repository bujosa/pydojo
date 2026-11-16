#!/usr/bin/env python3
"""Fetch pinned upstream archives into generated target/toolchain. Never modifies system Python."""

import hashlib
import json
import platform
import shutil
import subprocess
import tarfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def completion_tools():
    base = ROOT / "target/toolchain"
    dest = base / "completion"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir()
    for name, spec in json.loads(
        (ROOT / "runtime/completion-tools.json").read_text()
    ).items():
        archive = base / (name + ".whl")
        if (
            not archive.exists()
            or hashlib.sha256(archive.read_bytes()).hexdigest() != spec["sha256"]
        ):
            with urllib.request.urlopen(spec["url"], timeout=60) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != spec["sha256"]:
                raise SystemExit("Completion tool checksum mismatch: " + name)
            archive.write_bytes(data)
        with zipfile.ZipFile(archive) as wheel:
            for item in wheel.infolist():
                path = Path(item.filename)
                if path.is_absolute() or ".." in path.parts:
                    raise SystemExit("Invalid wheel path")
                wheel.extract(item, dest)


def main():
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        raise SystemExit("The initial bundled toolchain targets Apple Silicon macOS.")
    manifest = json.loads((ROOT / "runtime/toolchain.json").read_text())
    base = ROOT / "target/toolchain"
    base.mkdir(parents=True, exist_ok=True)
    for name, item in manifest.items():
        archive = base / (name + ".tar.gz")
        if (
            not archive.exists()
            or hashlib.sha256(archive.read_bytes()).hexdigest() != item["sha256"]
        ):
            pending = archive.with_suffix(".pending")
            with (
                urllib.request.urlopen(item["url"], timeout=60) as response,
                pending.open("wb") as out,
            ):
                shutil.copyfileobj(response, out)
            if hashlib.sha256(pending.read_bytes()).hexdigest() != item["sha256"]:
                pending.unlink()
                raise SystemExit(f"Checksum mismatch: {name}")
            pending.replace(archive)
        dest = base / name
        if not dest.exists():
            staging = base / (name + "-unpack")
            staging.mkdir(exist_ok=True)
            with tarfile.open(archive) as tar:
                # Upstream Python includes safe relative interpreter links; data filter checks escapes.
                tar.extractall(staging, filter="data")
            unpacked = next(staging.iterdir())
            unpacked.rename(dest)
            staging.rmdir()
        executable = dest / ("bin/python3.13" if name == "python" else "ruff")
        subprocess.run([str(executable), "--version"], check=True)
    completion_tools()
    print("Verified local toolchain ready in target/toolchain.")


if __name__ == "__main__":
    main()
