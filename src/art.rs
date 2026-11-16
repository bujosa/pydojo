//! Lesson artwork is decoded off-thread and cached by stable lesson identity.
use egui::{ColorImage, TextureHandle};
use std::{
    collections::{HashMap, VecDeque},
    sync::mpsc,
};
const IMAGES: &[(&str, &str, &[u8])] = &[
    (
        "names-and-values",
        "Names refer to values",
        include_bytes!("../assets/art/names-and-values-v1.png"),
    ),
    (
        "numbers-and-operators",
        "Combine quantities deliberately",
        include_bytes!("../assets/art/numbers-and-operators-v1.png"),
    ),
    (
        "strings-and-text",
        "Normalize, then compose text",
        include_bytes!("../assets/art/strings-and-text-v1.png"),
    ),
    (
        "booleans-and-comparisons",
        "Two outcomes, one clear condition",
        include_bytes!("../assets/art/booleans-and-comparisons-v1.png"),
    ),
    (
        "lists-and-indexes",
        "Order gives each item a position",
        include_bytes!("../assets/art/lists-and-indexes-v1.png"),
    ),
    (
        "dictionaries-and-keys",
        "Keys lead directly to values",
        include_bytes!("../assets/art/dictionaries-and-keys-v1.png"),
    ),
    (
        "functions-and-return",
        "Inputs become returned results",
        include_bytes!("../assets/art/functions-and-return-v1.png"),
    ),
    (
        "branches-and-boundaries",
        "One decision chooses a path",
        include_bytes!("../assets/art/branches-and-boundaries-v1.png"),
    ),
    (
        "loops-and-accumulators",
        "Repeat a step; build a result",
        include_bytes!("../assets/art/loops-and-accumulators-v1.png"),
    ),
    (
        "comprehensions",
        "Filter first, then transform",
        include_bytes!("../assets/art/comprehensions-v1.png"),
    ),
    (
        "sets-and-membership",
        "Keep only unique members",
        include_bytes!("../assets/art/sets-and-membership-v1.png"),
    ),
    (
        "unpacking-and-enumerate",
        "Give each position a clear meaning",
        include_bytes!("../assets/art/unpacking-and-enumerate-v1.png"),
    ),
    (
        "defaults-without-aliasing",
        "New calls, independent containers",
        include_bytes!("../assets/art/defaults-without-aliasing-v1.png"),
    ),
    (
        "keyword-only-apis",
        "Name the options at the call site",
        include_bytes!("../assets/art/keyword-only-apis-v1.png"),
    ),
    (
        "missing-is-not-falsy",
        "Missing is different from empty",
        include_bytes!("../assets/art/missing-is-not-falsy-v1.png"),
    ),
    (
        "grouping-records",
        "Related records share a bucket",
        include_bytes!("../assets/art/grouping-records-v1.png"),
    ),
    (
        "sorting-with-keys",
        "Order by the fields that matter",
        include_bytes!("../assets/art/sorting-with-keys-v1.png"),
    ),
    (
        "generators-and-laziness",
        "One value, only when requested",
        include_bytes!("../assets/art/generators-and-laziness-v1.png"),
    ),
    (
        "exceptions-and-validation",
        "Reject invalid work explicitly",
        include_bytes!("../assets/art/exceptions-and-validation-v1.png"),
    ),
    (
        "parsing-with-fallbacks",
        "Convert first; handle failure",
        include_bytes!("../assets/art/parsing-with-fallbacks-v1.png"),
    ),
    (
        "json-at-the-boundary",
        "Decoded data still needs validation",
        include_bytes!("../assets/art/json-at-the-boundary-v1.png"),
    ),
    (
        "csv-with-a-parser",
        "Quoted fields stay together",
        include_bytes!("../assets/art/csv-with-a-parser-v1.png"),
    ),
    (
        "files-and-contexts",
        "Acquire, use, always close",
        include_bytes!("../assets/art/files-and-contexts-v1.png"),
    ),
    (
        "decimal-money",
        "Exact units, explicit rounding",
        include_bytes!("../assets/art/decimal-money-v1.png"),
    ),
    (
        "dates-with-timezones",
        "Different offsets, the same instant",
        include_bytes!("../assets/art/dates-with-timezones-v1.png"),
    ),
    (
        "classes-and-state",
        "One blueprint, independent state",
        include_bytes!("../assets/art/classes-and-state-v1.png"),
    ),
    (
        "dataclasses-and-values",
        "Equal fields, equal values",
        include_bytes!("../assets/art/dataclasses-and-values-v1.png"),
    ),
    (
        "explicit-state-transitions",
        "Only valid transitions move forward",
        include_bytes!("../assets/art/explicit-state-transitions-v1.png"),
    ),
    (
        "properties-and-invariants",
        "Guard each change to state",
        include_bytes!("../assets/art/properties-and-invariants-v1.png"),
    ),
    (
        "inject-dependencies",
        "Keep policy separate from delivery",
        include_bytes!("../assets/art/inject-dependencies-v1.png"),
    ),
    (
        "copying-nested-data",
        "Copy the structure you own",
        include_bytes!("../assets/art/copying-nested-data-v1.png"),
    ),
    (
        "closures-and-state",
        "A function can retain its environment",
        include_bytes!("../assets/art/closures-and-state-v1.png"),
    ),
    (
        "decorators-and-metadata",
        "Wrap behavior; preserve metadata",
        include_bytes!("../assets/art/decorators-and-metadata-v1.png"),
    ),
    (
        "custom-context-managers",
        "Cleanup runs on every exit",
        include_bytes!("../assets/art/custom-context-managers-v1.png"),
    ),
    (
        "iterator-protocol",
        "Advance until there are no more values",
        include_bytes!("../assets/art/iterator-protocol-v1.png"),
    ),
    (
        "async-and-await",
        "Concurrent work, ordered results",
        include_bytes!("../assets/art/async-and-await-v1.png"),
    ),
    (
        "type-hints-and-contracts",
        "Describe intent; validate actual input",
        include_bytes!("../assets/art/type-hints-and-contracts-v1.png"),
    ),
    (
        "project-log-report",
        "Many events become a useful report",
        include_bytes!("../assets/art/project-log-report-v1.png"),
    ),
    (
        "project-stock-reservation",
        "A batch succeeds as a whole",
        include_bytes!("../assets/art/project-stock-reservation-v1.png"),
    ),
    (
        "project-cart-pricing",
        "Precise totals in integer cents",
        include_bytes!("../assets/art/project-cart-pricing-v1.png"),
    ),
    (
        "project-idempotent-handler",
        "Repeated request, one recorded result",
        include_bytes!("../assets/art/project-idempotent-handler-v1.png"),
    ),
    (
        "project-retry-policy",
        "Try again within a clear limit",
        include_bytes!("../assets/art/project-retry-policy-v1.png"),
    ),
    (
        "project-import-pipeline",
        "Parse, validate, group, reconcile",
        include_bytes!("../assets/art/project-import-pipeline-v1.png"),
    ),
];
pub fn caption(id: &str) -> &'static str {
    IMAGES
        .iter()
        .find(|(key, _, _)| *key == id)
        .map(|(_, caption, _)| *caption)
        .unwrap_or("Lesson illustration")
}
#[derive(Default)]
pub struct Illustrations {
    cache: VecDeque<(String, TextureHandle)>,
    pending: HashMap<String, mpsc::Receiver<Result<ColorImage, String>>>,
    errors: HashMap<String, String>,
}
impl Illustrations {
    pub fn get(&mut self, ctx: &egui::Context, id: &str) -> Option<TextureHandle> {
        // Drop stale results after navigation; a previous lesson can never replace this image.
        self.pending.retain(|key, _| key == id);
        if let Some(index) = self.cache.iter().position(|(key, _)| key == id)
            && let Some(entry) = self.cache.remove(index)
        {
            let texture = entry.1.clone();
            self.cache.push_front(entry);
            return Some(texture);
        }
        if let Some(receiver) = self.pending.get(id) {
            match receiver.try_recv() {
                Ok(Ok(image)) => {
                    self.pending.remove(id);
                    let texture = ctx.load_texture(
                        format!("lesson-art-{id}"),
                        image,
                        egui::TextureOptions::LINEAR,
                    );
                    self.cache.push_front((id.into(), texture.clone()));
                    self.cache.truncate(4);
                    return Some(texture);
                }
                Ok(Err(error)) => {
                    self.pending.remove(id);
                    self.errors.insert(id.into(), error);
                }
                Err(mpsc::TryRecvError::Disconnected) => {
                    self.pending.remove(id);
                    self.errors
                        .insert(id.into(), "Illustration could not load".into());
                }
                Err(mpsc::TryRecvError::Empty) => {}
            }
        } else if !self.errors.contains_key(id) {
            if let Some((_, _, bytes)) = IMAGES.iter().find(|(key, _, _)| *key == id) {
                let (tx, rx) = mpsc::channel();
                self.pending.insert(id.into(), rx);
                let bytes = *bytes;
                let ctx = ctx.clone();
                std::thread::spawn(move || {
                    let image = image::load_from_memory(bytes)
                        .map_err(|e| e.to_string())
                        .map(|image| {
                            // Contain rather than crop: every educational object stays visible.
                            let rgba = image.thumbnail(1000, 480).to_rgba8();
                            ColorImage::from_rgba_unmultiplied(
                                [rgba.width() as usize, rgba.height() as usize],
                                rgba.as_raw(),
                            )
                        });
                    let _ = tx.send(image);
                    ctx.request_repaint();
                });
            } else {
                self.errors
                    .insert(id.into(), "No artwork for this lesson".into());
            }
        }
        if self.pending.contains_key(id) {
            ctx.request_repaint_after(std::time::Duration::from_millis(30));
        }
        None
    }
    pub fn failed(&self, id: &str) -> bool {
        self.errors.contains_key(id)
    }
}

/// Validate shipped image delivery and identity coverage, independent of UI presentation.
pub fn verify(lessons: &[crate::course::Lesson]) -> Result<(), String> {
    let ids: std::collections::HashSet<_> = IMAGES.iter().map(|(id, _, _)| *id).collect();
    if ids.len() != IMAGES.len() || IMAGES.len() != lessons.len() {
        return Err("Every lesson needs one uniquely keyed illustration".into());
    }
    for lesson in lessons {
        let (_, _, bytes) = IMAGES
            .iter()
            .find(|(id, _, _)| *id == lesson.id)
            .ok_or_else(|| format!("Missing illustration for {}", lesson.id))?;
        let image = image::load_from_memory(bytes)
            .map_err(|e| format!("{}: {e}", lesson.id))?
            .to_rgba8();
        if image.width() < 900
            || image.height() < 400
            || !image.pixels().any(|p| p.0[3] == 0)
            || !image.pixels().any(|p| p.0[3] > 0)
        {
            return Err(format!(
                "{}: expected a visible high-resolution illustration with transparency",
                lesson.id
            ));
        }
    }
    println!(
        "Verified {} uniquely keyed, decodable transparent lesson illustrations.",
        IMAGES.len()
    );
    Ok(())
}
