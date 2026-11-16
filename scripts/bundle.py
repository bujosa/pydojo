#!/usr/bin/env python3
"""Build a Keiko-compatible signed macOS release. Never touches installed applications."""

import hashlib
import os
import platform
import plistlib
import shutil
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)


def run(*args, **kwargs):
    subprocess.run(args, check=True, **kwargs)


run("python3", "scripts/toolchain.py")
version = tomllib.loads(Path("Cargo.toml").read_text())["package"]["version"]
env = os.environ.copy()
env["RUSTFLAGS"] = env.get("RUSTFLAGS", "") + f" --remap-path-prefix={Path.home()}=~"
run("cargo", "build", "--release", "--locked", env=env)
binary = Path("target/release/pydojo")
if str(Path.home()).encode() in binary.read_bytes():
    raise SystemExit("Release rejected: builder home path found in binary")
base = Path("target/bundle")
app = base / "PyDojo.app"
if app.exists():
    shutil.rmtree(app)  # exclusively generated output inside this repository
macos = app / "Contents/MacOS"
resources = app / "Contents/Resources"
macos.mkdir(parents=True)
resources.mkdir()
licenses = resources / "Licenses"
licenses.mkdir()
for license_file in list(Path("assets/fonts").glob("OFL-*.txt")) + list(
    Path("assets/licenses").glob("*")
):
    shutil.copy2(license_file, licenses / license_file.name)
shutil.copy2("ATTRIBUTION.md", resources / "ATTRIBUTION.md")
shutil.copytree("target/toolchain/python", resources / "python", symlinks=True)
shutil.copytree("target/toolchain/ruff", resources / "ruff", symlinks=True)
shutil.copytree("target/toolchain/completion", resources / "completion")
shutil.copy2("runtime/completion-tools.json", resources / "completion-tools.json")
shutil.copy2("runtime/toolchain.json", resources / "toolchain.json")
shutil.copy2(binary, macos / "pydojo")
info = dict(
    CFBundleName="PyDojo",
    CFBundleDisplayName="PyDojo",
    CFBundleIdentifier="dev.bujosa.pydojo",
    CFBundleVersion=version,
    CFBundleShortVersionString=version,
    CFBundleExecutable="pydojo",
    CFBundleIconFile="PyDojo",
    CFBundlePackageType="APPL",
    LSApplicationCategoryType="public.app-category.education",
    LSMinimumSystemVersion="12.0",
    NSHighResolutionCapable=True,
)
(app / "Contents/Info.plist").write_bytes(plistlib.dumps(info))
run("swift", "scripts/icon.swift", str(base / "icon.png"))
iconset = base / "PyDojo.iconset"
iconset.mkdir(exist_ok=True)
for size in (16, 32, 128, 256, 512):
    for scale in (1, 2):
        suffix = "@2x" if scale == 2 else ""
        run(
            "sips",
            "-z",
            str(size * scale),
            str(size * scale),
            str(base / "icon.png"),
            "--out",
            str(iconset / f"icon_{size}x{size}{suffix}.png"),
            stdout=subprocess.DEVNULL,
        )
run("iconutil", "-c", "icns", str(iconset), "-o", str(resources / "PyDojo.icns"))
# Sign every embedded Mach-O first, preserving relative interpreter links.
magic = {
    b"\xcf\xfa\xed\xfe",
    b"\xce\xfa\xed\xfe",
    b"\xca\xfe\xba\xbe",
    b"\xfe\xed\xfa\xcf",
}
for path in sorted(resources.rglob("*"), key=lambda p: len(p.parts), reverse=True):
    if path.is_file() and not path.is_symlink():
        with path.open("rb") as stream:
            if stream.read(4) in magic:
                run(
                    "codesign",
                    "--force",
                    "--sign",
                    "-",
                    str(path),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
run("codesign", "--force", "--sign", "-", str(app))
run("codesign", "--verify", "--deep", "--strict", str(app))
out = Path("target/release-assets")
out.mkdir(exist_ok=True)
arch = {"aarch64": "arm64"}.get(platform.machine(), platform.machine())
archive = out / f"PyDojo-v{version}-macos-{arch}.zip"
run("ditto", "-c", "-k", "--keepParent", str(app), str(archive))
checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
(out / "SHA256SUMS.txt").write_text(f"{checksum}  {archive.name}\n")
print(f"Prepared {archive} and SHA256SUMS.txt (ad-hoc signed, not notarized).")
