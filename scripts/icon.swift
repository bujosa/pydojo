import AppKit
// Original PyDojo bracket seal. The same geometry is painted by src/design.rs.
let image = NSImage(size: NSSize(width: 1024, height: 1024))
image.lockFocus()
NSColor(calibratedRed: 0.051, green: 0.082, blue: 0.122, alpha: 1).setFill()
NSBezierPath(roundedRect: NSRect(x: 48, y: 48, width: 928, height: 928), xRadius: 210, yRadius: 210).fill()
NSColor(calibratedRed: 0.114, green: 0.357, blue: 0.310, alpha: 1).setFill()
NSBezierPath(roundedRect: NSRect(x: 154, y: 154, width: 716, height: 716), xRadius: 152, yRadius: 152).fill()
NSColor(calibratedRed: 0.949, green: 0.929, blue: 0.882, alpha: 1).setStroke()
func line(_ points: [(CGFloat, CGFloat)]) {
    let path = NSBezierPath()
    if let first = points.first { path.move(to: NSPoint(x: first.0, y: first.1)) }
    for point in points.dropFirst() { path.line(to: NSPoint(x: point.0, y: point.1)) }
    path.lineWidth = 42
    path.lineCapStyle = .square
    path.lineJoinStyle = .miter
    path.stroke()
}
let label = NSAttributedString(string: "Py", attributes: [.font: NSFont.systemFont(ofSize: 350, weight: .bold), .foregroundColor: NSColor(calibratedRed: 0.91, green: 0.89, blue: 0.83, alpha: 1)])
label.draw(at: NSPoint(x: 270, y: 320))
NSColor(calibratedRed: 0.91, green: 0.75, blue: 0.44, alpha: 1).setStroke()
line([(300, 290), (720, 290)])
image.unlockFocus()
if let tiff = image.tiffRepresentation, let bitmap = NSBitmapImageRep(data: tiff), let png = bitmap.representation(using: .png, properties: [:]) {
    try png.write(to: URL(fileURLWithPath: CommandLine.arguments[1]))
} else {
    throw NSError(domain: "PyDojo icon", code: 1)
}
