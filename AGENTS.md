# PyDojo
Native Rust/egui Python learning app in Keiko. English UI and original English lessons.

- `src/art.rs` owns lesson-keyed embedded illustrations: background decode, four-texture cache, contain-fit, and no cross-lesson stale results. Update assets/art/prompts-v1.json and run --verify-art when adding a lesson.
- Pure course/learning models, embedded JSON; every lesson has its own guide and separately graded practice.
- `compiler.rs` owns lab grading; Run and Debug never credit completion.
- `runtime/` owns the Python runner, debugger protocol and educational safety guards. Trusted local learning code only; never claim a hostile-code sandbox.
- Python commands run off the UI thread, in private temporary directories, with isolated environment, bounded output and time limits. No shell expansion or package installation from learner code.
- `store.rs` isolates all learner data with PYDOJO_HOME, atomic writes, single-writer lock; preserve unreadable data.
- `formatter.rs` uses pinned Ruff, never executes source; stale results must preserve edits and breakpoints. Formatting clears breakpoints explicitly because lines can move.
- Never read or alter TypeDojo/PodDojo learner data. Use PYDOJO_HOME for QA.
- No shipped unwrap, panic, unsafe, webview or async runtime. UI visual review is manual native interaction; don't generate UI tests.
- Required gates: cargo fmt --check; cargo clippy --all-targets -- -D warnings; cargo test; cargo run --locked -- --verify-art; cargo run --locked -- --verify-content; cargo run --locked -- --verify-learning; Python runtime unit tests; pinned Ruff formatting checks.
- Bundle only verified, checksum-pinned runtime assets with licenses. No catalog installation entry before a verified signed release exists.
- bujosa/ branches, Conventional Commits; no hosted CI. Preserve unrelated work.
