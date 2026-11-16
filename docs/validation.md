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

This initial course teaches fundamentals through advanced language features and focused engineering projects. Larger professional projects and service integration remain on ROADMAP.md. The initial local-only scope above is historical. Publication status is recorded below; Developer ID notarization remains separate work.

## Visual refinement · 0.1.1

The follow-up design pass consolidates charcoal surfaces, mint selection, shared editor/console colors and consistent hover/active states. Reading allocates less width to definitions and more to code/reasoning. Compact reading folds the glossary; examples have an explicit filename and copy control. The outcome area provides a direct practice action. Stage tabs pair selected state with an underline, and Check is the emphasized workbench action. The guided task title avoids repeating its stage label.

Native review covered 1280x860 and 820x700: reading, glossary expansion/collapse, code copy control, wrong/correct explained predictions, direct entry to practice, focus mode, failed starter feedback, Format and a passed guided exercise. A final pass checks the active tab's accessibility state and the installed app. The required local gates are rerun; no automated presentation tests are added. Curriculum, execution and progress contracts are unchanged by this visual pass.

## Lesson illustrations · 0.1.2

The generic contour decoration is replaced by a collection of 43 original transparent lesson-specific dioramas. Every stable lesson ID maps to a different PNG and an authored conceptual caption. The complete prompts are saved in assets/art/prompts-v1.json; generation uses the built-in image_gen tool. Images are packaged locally, so lessons require no image service or network connection.

The masthead contains the full image with a separate text region in both wide and compact layouts. Native image alt text uses the educational caption. Decode/thumbnail preparation happens off the UI thread, completed work is associated with its exact lesson ID, stale navigation results are dropped, and the GPU cache retains at most four textures. The --verify-art gate checks complete unique lesson coverage, actual PNG decoding, sufficient dimensions and real transparency; source-file SHA-256 hashes are recorded with the prompts. This checks asset delivery rather than generating presentation tests.

Native artwork review covered 1280x860 and 820x700. Observed artwork changes for values, arithmetic, text, booleans, dictionaries, CSV, async and the final import project. The review also revisited the first lesson after more than four different images to exercise cache eviction and confirmed matching accessible image captions. A layout correction keeps the complete image and caption inside the masthead without moving the following reader section upward. The full content/runtime gate and final Clippy/build pass are recorded under target/art-review/validation. The existing learner profile is preserved during the local update.

## Public distribution · 0.1.2

The public repository is https://github.com/bujosa/pydojo. PR #1 was merged after the required local gates and the secret scan passed. Release v0.1.2 is built from merged main and contains the signed ZIP and SHA256SUMS.txt. Keiko's anonymous live integration verifies the public download checksum, signature and bundle identity, repeated replacement, rejected invalid asset, uninstall, restore and retained test data in isolated folders. The four-test suite includes PyDojo, TypeDojo, PodDojo and launcher self-update; all four passed during the catalog rollout. No ordinary learner data was used.

These checks do not add notarization, Intel support or an adversarial execution sandbox. Manual native review and automated behavioral checks retain the scopes documented above.
