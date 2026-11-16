# Contributing

PyDojo is a native Rust/egui app with original English learning content. Keep contributions focused on a concrete learning or runtime behavior. Read AGENTS.md and docs/architecture.md first.

Use a fork and a pull request for publication. Maintainer branches use bujosa/ plus a short kebab-case purpose; commits use Conventional Commits. Preserve unrelated changes and never place credentials or real learner data in examples, screenshots, logs or issues. Include only original or appropriately licensed assets.

Install the pinned toolchain with `python3 scripts/toolchain.py`, then run `cargo run --locked`. Code and content gates are `python3 scripts/validate.py`. These run real local Python processes; no Docker or service account is required. Do not weaken failed contracts just to make a gate green.

For native review, export PYDOJO_HOME to a new private directory before launching. Never test against another dojo's progress. Exercise Learn -> guided -> independent, wrong and correct answers, edit-after-pass, Run, Debug, Format/Undo and reopen. Review a wide and compact window. Do not generate automated presentation tests; runtime and storage behavior still need meaningful tests.

The UI is in main.rs, reader.rs, ide.rs and editor.rs. Pure curriculum models are course.rs and learning.rs; the JSON is authored by tools/author_course.py. Grading is compiler.rs plus runtime/check.py; the interactive bridge is engine.rs plus runtime/bridge.py; storage is store.rs. Bundled tools have pinned checksums in runtime/toolchain.json and runtime/completion-tools.json. completion.rs and runtime/complete.py own static language queries; suggest.rs owns debouncing and presentation. A toolchain update needs licenses, signatures and actual relocated-bundle validation.

In a PR, describe the learner-visible change, exact base/head, checks run and their results, manual review and known limitations. Maintainers publish verified bundles separately. Never publish an installable Keiko entry before a signed release with matching SHA256SUMS exists.
