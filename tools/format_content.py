"""Format embedded Python snippets with the pinned Ruff, without executing them."""

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    ruff = ROOT / "target/toolchain/ruff/ruff"
    changed = 0
    fields = 0
    for filename in ("course.json", "learning.json"):
        path = ROOT / "content" / filename
        data = json.loads(path.read_text())
        snippets = []
        for item in data:
            exercise = item.get("practice", item)
            for field in (
                "starter",
                "solution",
                "alternative",
                "negative",
                "checks",
                "runtime",
            ):
                if exercise[field].strip():
                    snippets.append((exercise, field))
            if "practice" in item:
                snippets.append((item, "example"))
        for owner, field in snippets:
            process = subprocess.run(
                [
                    str(ruff),
                    "format",
                    "--isolated",
                    "--no-cache",
                    "--target-version",
                    "py313",
                    "--stdin-filename",
                    "example.py",
                    "-",
                ],
                input=owner[field],
                text=True,
                capture_output=True,
                check=True,
            )
            fields += 1
            if process.stdout != owner[field]:
                changed += 1
                owner[field] = process.stdout
        if args.write:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(
        f"Ruff: {fields} snippets, {changed} {'formatted' if args.write else 'requiring formatting'}."
    )
    if changed and not args.write:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
