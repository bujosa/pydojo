# Authoring a lesson

The source of the curriculum is tools/author_course.py. Run it to rebuild content/course.json and content/learning.json deterministically. Keep the source and generated JSON in the same change.

A lesson has a stable lowercase hyphenated ID, chapter, title, concept, task, starter, reference solution, independent alternative, plausible wrong solution, behavioral checks, runtime checks and a hint. IDs are storage keys: renaming one does not migrate existing drafts. Do not reuse an ID for a different task.

Every lesson needs a guide with an outcome, earlier-only prerequisite IDs, vocabulary, a runnable explained example, at least two substantive explanation paragraphs, an explained three-choice prediction, transfer questions and a separately graded smaller practice. A guided solution must not simply give away the independent answer.

Write English that teaches each new symbol before requiring it. Show input, output, state ownership and failure policy. Distinguish runtime behavior from static type hints. State when a production concern is outside a local exercise.

Checks receive the learner module as s. Assert behavior, not source substrings or one implementation style. Include ordinary values, empty inputs, boundaries and failure cases. Runtime contracts may use helpers in runtime/contracts.py (exception assertions, in-memory retry/idempotency collaborators and real asyncio tests). Every source is executed in a fresh scratch directory; do not depend on another lesson's files or external services. Use only the standard library.

Reference and alternative solutions must pass. The starter, empty answer, unrelated answer and plausible negative must fail. Verify both course and guided contracts through scripts/validate.py; explained examples must run, and each guided playground must run with its solution. Add a meaningful engine test when the runtime contract changes. Do not add presentation tests.

Examples containing CSV or newlines need properly escaped string literals in checks. The authoring helper normalizes newlines inside single-expression cases; multiline raw checks must be valid Python statements. Use the bundled Ruff version to format code examples; preserve deliberately incomplete starters only when formatting remains meaningful.

## Lesson artwork

Every lesson ID has one original transparent PNG in assets/art, with a specific conceptual scene, caption and production prompt in prompts-v1.json. Add the corresponding stable-ID entry in src/art.rs when adding a lesson. Preserve source transparency and compose an illustration that remains legible at about 300 by 140 points. Keep code, exact numeric assertions and instructional text in the native reader, not baked into the bitmap. The app contains the complete scene rather than cropping it, and decodes images off the UI thread. Run cargo run --locked -- --verify-art to validate shipped coverage and PNG delivery.
