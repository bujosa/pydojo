# Local validation · 15 November 2026

Scope: PyDojo 0.1.0 for macOS Apple Silicon. Local application and signed distributable; no GitHub publication or Keiko catalog rollout has been performed for this new app.

## Automated behavior and content

`python3 scripts/validate.py` is the required gate. Evidence logs are kept under target/qa/validation. It checks Rust formatting, Clippy with warnings denied, 12 Rust tests (real Python execution, syntax/runtime failures, debugger stepping and breakpoints, Stop, timeout/output limits, external-file/network/process guards, formatting and isolated storage), and three Python inspection tests.

The curriculum gate checks 258 cases for 43 independent labs and 258 for 43 distinct guided practices. Each rejects a starter, empty answer, unrelated answer and plausible negative, and accepts a reference solution plus a different valid alternative. It also executes 43 explained examples and both sets of 43 playgrounds with their corresponding solutions. These 645 executions are behavioral/content verification, not 645 UI end-to-end tests. Ruff checks 473 embedded Python snippets and the Python tooling.

The same content and learning verification are run directly from the extracted signed release app, with PATH restricted to /usr/bin:/bin and no PYDOJO_PYTHON/PYDOJO_RUFF override. This proves the bundled interpreter is usable after relocation. Bundle signatures and SHA256SUMS are checked independently.

## Native review

Manual native interaction used separate PYDOJO_HOME profiles, never the normal learner directory. Wide 1280x860 and compact 820x700 windows were reviewed. Observed flows: reading and explained prediction, rejected guided starter, actual guided solution, Format -> Undo -> Redo, Check success, transition to independent lab, separate completion, actual Run output, Debug entry/step over/variable display/name inspection, Stop, edit-after-pass invalidation, re-check and close/reopen persistence. The final build was also checked for Python tab labels, four-space Tab insertion, autoindent after a colon and actual execution of the edited playground.

No automated presentation tests were added. Functional engine tests cover breakpoints and failure/timeout handling; manual review does not imply every lesson was clicked end-to-end in the UI.

## Distribution and limits

The app is ad-hoc signed, not notarized. Initial platform: Apple Silicon macOS. It includes pinned CPython 3.13.18 and Ruff 0.12.5 with upstream notices. The app and course use trusted local code with educational guards; CPython audit hooks are not an adversarial security sandbox. No terminal, external package installation, LSP autocomplete, static type checker or multi-file project workspace is shipped.

This initial course teaches fundamentals through advanced language features and focused engineering projects. Larger professional projects and service integration remain on ROADMAP.md. Public release/catalog integration and Developer ID notarization are separate work.
