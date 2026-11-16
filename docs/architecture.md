# Architecture and learning contract

PyDojo is a local native practice app. The learner reads an explained example, predicts its behavior, solves a smaller guided exercise, then transfers the idea to an independent lab. Each stage owns separate drafts and evidence. Only Check on the exact current answer credits that stage. Run is experimentation; Debug reveals actual Python frames, never a simulated execution.

The Rust UI owns navigation, editing and snapshot identity. Pure course and guide models load embedded original English material. The store owns only PyDojo's directory, uses an exclusive session lock and atomic writes, preserves unreadable files and invalidates completion after edits. PYDOJO_HOME isolates review data.

The runtime adapter owns short-lived processes and private temporary directories. A bundled, checksum-pinned CPython interpreter executes code; Ruff formats source as data. There are no Node, npm, webview, network-service or Python-package installation dependencies. The release includes upstream notices and a portable interpreter. Development may explicitly select PYDOJO_PYTHON or PYDOJO_RUFF.

Checks compile Python syntax and execute authored behavioral assertions in a separate namespace. Missing implementations, wrong results, raised exceptions and timeouts fail. No type-checking or production certification is implied. Reference answers, independent alternatives, broken starters, unrelated answers, empty answers and wrong solutions are verified for every exercise.

Run/Debug use a JSON-lines bridge over stdin/stdout, not a listening TCP port. Python's trace hooks implement entry/breakpoints/step into/over/out; snapshots contain only learner frames. Expression inspection accepts plain names and literal values only: no calls, operators, attributes or arbitrary evaluation. Stop kills and reaps the process; running time, total debug lifetime, source size and output are bounded. Formatting discards stale results, keeps Undo/Redo, and clears line breakpoints with a notice rather than silently moving them incorrectly.

Code is trusted local learning code, not an adversarial sandbox. A Python audit hook blocks network/process creation, native library loading, and file access outside the scratch directory and interpreter's standard library. Environment variables are cleared; resource limits and process timeouts bound ordinary mistakes. Audit hooks do not make CPython a security boundary. Never run downloaded untrusted code. File, JSON and CSV labs use the private scratch directory or in-memory strings, never the learner's documents.

The first release targets Apple Silicon macOS. A verified signed bundle precedes any Keiko catalog entry. Public rollout and catalog integration are separate from local implementation; ad-hoc signing is reported honestly and is not notarization.
