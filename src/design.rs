//! PyDojo's original visual language: forest ink, warm paper, and an original loop monogram.
use egui::{Color32, FontId, RichText, Stroke, Vec2};
pub const BG: Color32 = Color32::from_rgb(12, 23, 25);
pub const PANEL: Color32 = Color32::from_rgb(17, 34, 36);
pub const BORDER: Color32 = Color32::from_rgb(44, 65, 67);
pub const PAPER: Color32 = Color32::from_rgb(232, 226, 212);
pub const INK: Color32 = Color32::from_rgb(36, 45, 60);
pub const BLUE_INK: Color32 = Color32::from_rgb(29, 91, 79);
pub const ACCENT: Color32 = Color32::from_rgb(142, 219, 184);
pub const MUTED: Color32 = Color32::from_rgb(163, 180, 199);
pub const TEXT: Color32 = Color32::from_rgb(233, 237, 241);

pub fn display(size: f32) -> FontId {
    FontId::new(size, egui::FontFamily::Name("display".into()))
}
pub fn eyebrow(ui: &mut egui::Ui, text: &str, color: Color32) {
    ui.label(RichText::new(text).monospace().size(11.5).color(color));
}
pub fn seal(ui: &mut egui::Ui, size: f32) {
    let (rect, _) = ui.allocate_exact_size(Vec2::splat(size), egui::Sense::hover());
    let p = ui.painter();
    p.rect_filled(rect, 8.0, BLUE_INK);
    p.text(
        rect.center(),
        egui::Align2::CENTER_CENTER,
        "Py",
        display(size * 0.48),
        PAPER,
    );
    p.line_segment(
        [
            rect.left_bottom() + egui::vec2(size * 0.2, -size * 0.15),
            rect.right_bottom() + egui::vec2(-size * 0.2, -size * 0.15),
        ],
        Stroke::new(2.0, Color32::from_rgb(231, 192, 112)),
    );
}

/// Six original chapter crests drawn on the same grid as the bracket seal.
pub fn chapter(ui: &mut egui::Ui, index: u8) {
    let (rect, _) = ui.allocate_exact_size(egui::vec2(20.0, 20.0), egui::Sense::hover());
    let p = ui.painter();
    let c = rect.center();
    let stroke = Stroke::new(1.4, ACCENT);
    match index {
        b'1' => {
            p.circle_stroke(c, 6.5, stroke);
            p.circle_filled(c, 2.0, ACCENT);
        }
        b'2' => {
            p.line_segment(
                [c + egui::vec2(-3.0, -6.0), c + egui::vec2(-7.0, -6.0)],
                stroke,
            );
            p.line_segment(
                [c + egui::vec2(-7.0, -6.0), c + egui::vec2(-7.0, 6.0)],
                stroke,
            );
            p.line_segment(
                [c + egui::vec2(-7.0, 6.0), c + egui::vec2(-3.0, 6.0)],
                stroke,
            );
            p.line_segment(
                [c + egui::vec2(3.0, -6.0), c + egui::vec2(7.0, -6.0)],
                stroke,
            );
            p.line_segment(
                [c + egui::vec2(7.0, -6.0), c + egui::vec2(7.0, 6.0)],
                stroke,
            );
            p.line_segment([c + egui::vec2(7.0, 6.0), c + egui::vec2(3.0, 6.0)], stroke);
        }
        b'3' => {
            for offset in [-3.0, 3.0] {
                p.rect_stroke(
                    egui::Rect::from_center_size(
                        c + egui::vec2(offset, offset),
                        egui::vec2(9.0, 9.0),
                    ),
                    1.0,
                    stroke,
                    egui::StrokeKind::Inside,
                );
            }
        }
        b'4' => {
            for dy in [-5.0, 5.0] {
                p.line_segment([c + egui::vec2(-6.0, 0.0), c + egui::vec2(5.0, dy)], stroke);
                p.circle_filled(c + egui::vec2(6.0, dy), 1.5, ACCENT);
            }
        }
        b'5' => {
            p.circle_stroke(c + egui::vec2(-3.0, 0.0), 5.0, stroke);
            p.circle_stroke(c + egui::vec2(3.0, 0.0), 5.0, stroke);
        }
        _ => {
            p.rect_stroke(
                egui::Rect::from_center_size(c, egui::vec2(14.0, 14.0)),
                1.0,
                stroke,
                egui::StrokeKind::Inside,
            );
            p.line_segment(
                [c + egui::vec2(-4.0, 1.0), c + egui::vec2(-1.0, 4.0)],
                stroke,
            );
            p.line_segment(
                [c + egui::vec2(-1.0, 4.0), c + egui::vec2(5.0, -4.0)],
                stroke,
            );
        }
    }
}

/// A compact editorial masthead that protects the working area on small screens.
pub fn masthead(
    ui: &mut egui::Ui,
    section: &str,
    title: &str,
    index: usize,
    compact: bool,
    practice: bool,
) {
    let width = ui.available_width();
    let short = compact && practice;
    let height = if short { 82.0 } else { 108.0 };
    let (banner, _) = ui.allocate_exact_size(egui::vec2(width, height), egui::Sense::hover());
    ui.painter().rect_filled(banner, 10.0, PANEL);
    // Original contour drawing: code-native artwork stays sharp at every window scale.
    let painter = ui.painter().with_clip_rect(banner.shrink(4.0));
    let origin = egui::pos2(banner.right() - width.min(300.0) * 0.5, banner.center().y);
    if width > 480.0 {
        for ring in 0..9 {
            let radius = 18.0 + ring as f32 * 8.0;
            let points = (0..81)
                .map(|step| {
                    let angle = step as f32 * std::f32::consts::TAU / 80.0;
                    origin + egui::vec2(angle.cos() * radius * 1.6, angle.sin() * radius * 0.62)
                })
                .collect();
            painter.add(egui::Shape::line(
                points,
                Stroke::new(1.0, Color32::from_rgba_unmultiplied(142, 219, 184, 70)),
            ));
        }
        painter.circle_filled(origin, 10.0, Color32::from_rgb(231, 192, 112));
        painter.line_segment(
            [
                origin + egui::vec2(-30.0, 0.0),
                origin + egui::vec2(30.0, 0.0),
            ],
            Stroke::new(1.0, PANEL),
        );
    }
    let text_rect = egui::Rect::from_min_size(
        banner.min + egui::vec2(20.0, 12.0),
        egui::vec2(width * 0.60 - 26.0, height - 20.0),
    );
    ui.scope_builder(egui::UiBuilder::new().max_rect(text_rect), |ui| {
        eyebrow(ui, &section.to_uppercase(), ACCENT);
        ui.add_space(5.0);
        ui.label(RichText::new(title).font(display(if compact { 20.0 } else { 26.0 })));
        if !short {
            ui.add_space(5.0);
            ui.label(
                RichText::new(format!("LAB {:02}  /  Learn by building", index + 1))
                    .monospace()
                    .size(11.5)
                    .color(MUTED),
            );
        }
    });
}
