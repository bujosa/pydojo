# PyDojo

A native Python learning workspace in the Keiko family. Read an explained example, predict the result, practice with guidance, and solve a separate lab with real Python checks.

- **43 lessons, 43 guided practices, seven chapters:** first values, control flow, collection patterns, reliable data, domain modeling, advanced Python, and six engineering projects.
- Original lesson-specific illustrations, with a different conceptual scene for each of the 43 lessons and an accessible native caption.
- Syntax-colored editor, line numbers, find, Undo/Redo, command palette and a focused workbench.
- Real CPython Run and Debug: console logs, breakpoints, step into/over/out, call stacks and read-only variable inspection.
- **Format** with pinned Ruff. Background formatting preserves newer edits; line breakpoints are cleared explicitly after formatting.
- Exact-answer completion, independently saved guided/lab drafts, atomic persistence and a single-writer lock.
- A portable Python interpreter and formatter included in the macOS app. No terminal setup or package download needed to solve a lesson.

The initial course goes from first syntax to advanced language features and bounded engineering exercises. It is a foundation for professional practice, not a complete professional qualification. See [the curriculum](docs/curriculum.md) and [roadmap](ROADMAP.md).

## Install

Download **PyDojo-v0.1.3-macos-arm64.zip** from the [latest release](https://github.com/bujosa/pydojo/releases/latest), extract it and move PyDojo.app to `~/Applications`. The verified Keiko catalog integration is being released with Keiko 0.3.7.

Python 3.13.18 and Ruff 0.12.5 are included. No terminal setup or account is needed. Initial platform: macOS Apple Silicon; the app is ad-hoc signed and not notarized. macOS may require first-launch approval in System Settings → Privacy & Security.

## Build and run

Initial supported bundle: macOS Apple Silicon. Development needs Rust (pinned in rust-toolchain.toml), Python 3.11+ for scripts, and Xcode command-line tools for macOS packaging.

```sh
python3 scripts/toolchain.py
cargo run --locked
```

The setup script verifies upstream SHA-256 checksums and places CPython 3.13.18 and Ruff 0.12.5 inside `target/toolchain`. It never changes the system interpreter. Explicit developer overrides: `PYDOJO_PYTHON`, `PYDOJO_RUFF`.

```sh
python3 scripts/validate.py
python3 scripts/bundle.py
```

The bundle script generates an ad-hoc signed app, ZIP and SHA256SUMS in target. It does not install, publish or notarize them. Initial release status is recorded in [validation](docs/validation.md).

## Use

Start with **Learn**, choose **Guided practice**, then **Independent lab**. Check validates the current answer; Run is experimentation and does not credit completion. `answer.py` contains your implementation; `playground.py` calls it. Debug pauses on actual Python lines. Inspection accepts a plain variable name or literal, with no calls or attributes.

Shortcuts: Cmd+Enter Check, Cmd+R Run, F5 Debug/Continue, F10 Step over, F11 Step into, Shift+F11 Step out, Cmd+Shift+I Format, Cmd+F Find, Cmd+Shift+P commands. Function keys may require Fn on macOS.

Drafts live in `~/Library/Application Support/PyDojo`. `PYDOJO_HOME` selects a separate directory for review. If unreadable data is found, it is preserved; do not delete the file to hide the problem. A stale session.lock may be removed only after confirming every PyDojo process is closed.

Each execution uses a disposable scratch directory with time/output limits and educational guards against network, process and external-file access. Run trusted local code only: CPython audit hooks are not a security sandbox. There is no interactive terminal, package manager, LSP autocomplete, project import or static type checker in this version. Files created by labs are temporary.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md), [content authoring](docs/content-authoring.md), and [architecture](docs/architecture.md). Original application/course code is MIT OR Apache-2.0. Fonts and bundled tools retain their upstream licenses; see [ATTRIBUTION.md](ATTRIBUTION.md).
