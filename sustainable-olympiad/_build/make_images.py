"""Generate the lightweight SVG illustrations used in the gallery, partner
logos and favicon. Output: ../assets/img/"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")

SKIN = ["#8d5524", "#f1c27d", "#c68642", "#e0ac69", "#5c3a1e", "#ffdbac"]
SHIRT = ["#0a6b3d", "#0b5394", "#f2b705", "#d9480f", "#5f3dc4", "#1098ad"]
HAIR = ["#2b1a10", "#4a2c17", "#111111", "#7a4a1d", "#1d1d1d", "#a0522d"]


def svg(body, w=800, h=500):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">{body}</svg>\n')


def person(x, y, i=0, s=1.0, arms="down"):
    """Simple flat figure standing with feet at (x, y)."""
    skin, shirt, hair = SKIN[i % 6], SHIRT[i % 6], HAIR[i % 6]
    g = [f'<g transform="translate({x} {y}) scale({s})">',
         '<rect x="-15" y="-55" width="12" height="55" rx="5" fill="#26323a"/>',
         '<rect x="3" y="-55" width="12" height="55" rx="5" fill="#26323a"/>',
         f'<rect x="-22" y="-118" width="44" height="70" rx="16" fill="{shirt}"/>']
    if arms == "up":
        g.append(f'<rect x="18" y="-165" width="11" height="55" rx="5" fill="{shirt}" transform="rotate(20 23 -112)"/>')
        g.append(f'<rect x="-29" y="-112" width="11" height="50" rx="5" fill="{shirt}"/>')
    elif arms == "forward":
        g.append(f'<rect x="10" y="-112" width="50" height="11" rx="5" fill="{shirt}"/>')
        g.append(f'<rect x="-29" y="-112" width="11" height="50" rx="5" fill="{shirt}"/>')
    else:
        g.append(f'<rect x="18" y="-112" width="11" height="50" rx="5" fill="{shirt}"/>')
        g.append(f'<rect x="-29" y="-112" width="11" height="50" rx="5" fill="{shirt}"/>')
    g += [f'<circle cx="0" cy="-138" r="20" fill="{skin}"/>',
          f'<path d="M-20 -140a20 20 0 0 1 40 0c-8-8-26-8-40 0z" fill="{hair}"/>',
          '</g>']
    return "".join(g)


def sky(top="#bfe3ff", bottom="#e9f6ff", ground="#7cc242", ground_y=380):
    return (f'<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
            f'<rect width="800" height="500" fill="url(#s)"/>'
            f'<rect y="{ground_y}" width="800" height="{500-ground_y}" fill="{ground}"/>')


def sun(x=680, y=90, r=42):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffd34d"/>'


def cloud(x, y):
    return (f'<g fill="#fff" opacity=".9"><circle cx="{x}" cy="{y}" r="22"/><circle cx="{x+26}" cy="{y-10}" r="28"/>'
            f'<circle cx="{x+56}" cy="{y}" r="22"/><rect x="{x}" y="{y}" width="56" height="22"/></g>')


def solar_panel(x, y, w=150, h=80):
    cells = "".join(
        f'<rect x="{x + 6 + c * (w - 12) / 4}" y="{y + 6 + r * (h - 12) / 2}" width="{(w - 12) / 4 - 4}" '
        f'height="{(h - 12) / 2 - 4}" fill="#1c4f8c"/>' for c in range(4) for r in range(2))
    return (f'<g transform="skewX(-12)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#0b2e59"/>{cells}</g>'
            f'<rect x="{x + w / 2 - 30}" y="{y + h}" width="8" height="40" fill="#6b7a86"/>')


def turbine(x, y, h=220):
    return (f'<rect x="{x - 4}" y="{y - h}" width="8" height="{h}" fill="#f4f7f9" stroke="#9fb3c0"/>'
            f'<g transform="translate({x} {y - h})" fill="#ffffff" stroke="#9fb3c0">'
            '<path d="M0 0 L-6 -90 L6 -90Z"/><path d="M0 0 L-6 -90 L6 -90Z" transform="rotate(120)"/>'
            '<path d="M0 0 L-6 -90 L6 -90Z" transform="rotate(240)"/><circle r="8"/></g>')


def tree(x, y, s=1.0, c="#2f9e44"):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-6" y="-50" width="12" height="50" fill="#7a4a1d"/>'
            f'<circle cy="-80" r="40" fill="{c}"/><circle cx="-24" cy="-60" r="26" fill="{c}"/>'
            f'<circle cx="24" cy="-60" r="26" fill="{c}"/></g>')


SCENES = {}

SCENES["solar"] = svg(
    sky() + sun() + cloud(120, 90) +
    '<polygon points="80,380 400,180 720,380" fill="#d9480f" opacity=".2"/>'
    '<rect x="160" y="300" width="480" height="90" fill="#e9ecef"/><rect x="160" y="290" width="480" height="14" fill="#adb5bd"/>' +
    solar_panel(250, 200) + solar_panel(430, 200) +
    person(200, 440, 0) + person(560, 445, 1, arms="up") + person(640, 450, 2))

SCENES["wind"] = svg(
    sky("#9fd3ff", "#e7f5ff", "#69b34c", 360) + cloud(500, 80) + cloud(150, 120) +
    '<path d="M0 360 Q200 250 400 330 T800 300 V500 H0Z" fill="#4c9a3a"/>' +
    turbine(560, 320, 230) + turbine(700, 300, 180) +
    '<rect x="160" y="350" width="10" height="70" fill="#495057"/>'
    '<g transform="translate(165 350)" fill="#f2b705"><path d="M0 0 L-4 -46 L4 -46Z"/>'
    '<path d="M0 0 L-4 -46 L4 -46Z" transform="rotate(120)"/><path d="M0 0 L-4 -46 L4 -46Z" transform="rotate(240)"/></g>' +
    person(110, 460, 3) + person(240, 465, 4, arms="forward"))

SCENES["recycling"] = svg(
    sky("#e6f4ea", "#f4fbf6", "#ced4da", 400) +
    "".join(f'<rect x="{x}" y="250" width="110" height="150" rx="10" fill="{c}"/>'
            f'<rect x="{x - 6}" y="238" width="122" height="18" rx="6" fill="{c}"/>'
            f'<path d="M{x + 40} 330 l15 -26 l15 26z" fill="none" stroke="#fff" stroke-width="5"/>'
            for x, c in [(150, "#0b5394"), (300, "#f2b705"), (450, "#0a6b3d"), (600, "#868e96")]) +
    '<rect x="70" y="370" width="40" height="30" fill="#c0eb75"/><circle cx="740" cy="385" r="15" fill="#74c0fc"/>' +
    person(100, 470, 5, arms="forward") + person(720, 470, 1))

SCENES["trees"] = svg(
    sky() + sun(120, 90) +
    '<rect y="300" width="800" height="12" fill="#adb5bd"/>' +
    "".join(f'<rect x="{x}" y="250" width="6" height="62" fill="#adb5bd"/>' for x in range(20, 800, 60)) +
    tree(480, 400, .6) + tree(600, 400, .5) + tree(700, 400, .7, "#40c057") +
    '<path d="M300 420 q20 -40 40 0z" fill="#7a4a1d"/><path d="M320 400 q-10 -30 10 -50 q10 30 -10 50z" fill="#2f9e44"/>' +
    person(240, 470, 2, arms="forward") + person(390, 470, 4))

SCENES["ocean"] = svg(
    '<rect width="800" height="500" fill="#a5d8ff"/>' + sun(650, 80) + cloud(180, 80) +
    '<path d="M0 260 Q50 240 100 260 T200 260 T300 260 T400 260 T500 260 T600 260 T700 260 T800 260 V500 H0Z" fill="#1c7ed6"/>'
    '<path d="M0 320 Q50 300 100 320 T200 320 T300 320 T400 320 T500 320 T600 320 T700 320 T800 320 V500 H0Z" fill="#1864ab"/>'
    '<path d="M220 250 h340 l-40 60 h-260z" fill="#f8f9fa"/><rect x="380" y="140" width="8" height="110" fill="#495057"/>'
    '<path d="M388 145 l90 90 h-90z" fill="#ffd34d"/>'
    '<path d="M560 260 q60 40 100 120" stroke="#495057" stroke-width="3" fill="none"/>'
    '<path d="M620 360 q40 -10 80 20 q-40 40 -80 -20z" fill="none" stroke="#f8f9fa" stroke-width="3" stroke-dasharray="6 4"/>'
    '<rect x="640" y="370" width="16" height="10" fill="#e64980"/><circle cx="672" cy="380" r="6" fill="#fab005"/>' +
    person(300, 255, 0, s=.7) + person(470, 255, 3, s=.7, arms="forward"))

SCENES["lab"] = svg(
    '<rect width="800" height="500" fill="#edf6f9"/><rect x="60" y="50" width="250" height="160" fill="#c5f6fa" stroke="#99a" />'
    '<line x1="185" y1="50" x2="185" y2="210" stroke="#99a"/>'
    '<rect y="330" width="800" height="20" fill="#adb5bd"/><rect x="40" y="350" width="20" height="150" fill="#868e96"/>'
    '<rect x="740" y="350" width="20" height="150" fill="#868e96"/>'
    '<rect x="420" y="240" width="160" height="90" rx="6" fill="#343a40"/><rect x="430" y="250" width="140" height="70" fill="#4dabf7"/>'
    '<polyline points="440,305 470,290 500,298 530,272 560,280" fill="none" stroke="#fff" stroke-width="4"/>'
    '<rect x="400" y="326" width="200" height="8" rx="3" fill="#495057"/>' +
    "".join(f'<rect x="{x}" y="270" width="18" height="60" rx="8" fill="#e7f5ff" stroke="#74c0fc"/>'
            f'<rect x="{x + 2}" y="300" width="14" height="28" rx="6" fill="{c}"/>'
            for x, c in [(250, "#69db7c"), (280, "#ffd43b"), (310, "#74c0fc")]) +
    person(170, 470, 1, arms="forward") + person(680, 470, 4))

SCENES["garden"] = svg(
    sky("#d0ebff", "#f1f8ff", "#adb5bd", 470) + sun(90, 80) +
    '<rect x="140" y="230" width="520" height="240" fill="#dee2e6"/>' +
    "".join(f'<rect x="{x}" y="{y}" width="50" height="40" fill="#74c0fc" opacity=".7"/>'
            for x in range(180, 640, 90) for y in (290, 380)) +
    '<rect x="130" y="220" width="540" height="14" fill="#868e96"/>' +
    "".join(f'<rect x="{x}" y="190" width="90" height="30" fill="#8d5524"/>'
            f'<circle cx="{x + 20}" cy="185" r="14" fill="#40c057"/><circle cx="{x + 48}" cy="180" r="16" fill="#2f9e44"/>'
            f'<circle cx="{x + 74}" cy="186" r="12" fill="#69db7c"/>' for x in (160, 280)) +
    solar_panel(420, 150, 110, 50) +
    '<rect x="600" y="170" width="40" height="50" rx="6" fill="#1971c2"/>' +
    cloud(560, 70))

SCENES["awards"] = svg(
    '<rect width="800" height="500" fill="#0b3d2e"/>' +
    "".join(f'<rect x="{x}" y="{y}" width="10" height="16" fill="{c}" transform="rotate({r} {x} {y})"/>'
            for x, y, c, r in [(90, 60, "#ffd34d", 20), (200, 120, "#74c0fc", -30), (320, 50, "#69db7c", 45),
                               (480, 90, "#ff8787", 10), (600, 40, "#ffd34d", -15), (700, 140, "#74c0fc", 30),
                               (150, 200, "#69db7c", 60), (650, 220, "#ff8787", -40), (400, 30, "#fff", 15)]) +
    '<rect x="300" y="330" width="200" height="170" fill="#f8f9fa"/><rect x="100" y="380" width="200" height="120" fill="#dee2e6"/>'
    '<rect x="500" y="410" width="200" height="90" fill="#ced4da"/>'
    '<text x="400" y="430" font-family="Arial, sans-serif" font-size="64" font-weight="700" fill="#0a6b3d" text-anchor="middle">1</text>'
    '<text x="200" y="460" font-family="Arial, sans-serif" font-size="48" font-weight="700" fill="#0b5394" text-anchor="middle">2</text>'
    '<text x="600" y="475" font-family="Arial, sans-serif" font-size="40" font-weight="700" fill="#5c3a1e" text-anchor="middle">3</text>' +
    person(370, 330, 0, .9, "up") + person(430, 330, 2, .9) +
    person(180, 380, 3, .85) + person(225, 380, 5, .85) +
    person(580, 410, 1, .8) + person(625, 410, 4, .8) +
    '<g transform="translate(442 168)"><path d="M-18 0h36v20a18 18 0 0 1-36 0z" fill="#ffd34d"/>'
    '<rect x="-4" y="36" width="8" height="12" fill="#ffd34d"/><rect x="-12" y="46" width="24" height="6" fill="#ffd34d"/></g>')


LOGO_ICON = {
    "openplanet": '<circle cx="28" cy="28" r="20" fill="none" stroke="#0b5394" stroke-width="5"/><path d="M14 30c8-10 20-10 28 0" stroke="#0a6b3d" stroke-width="5" fill="none"/>',
    "verdalis": '<path d="M28 8 L46 44 H10Z" fill="#0a6b3d"/><circle cx="28" cy="32" r="7" fill="#ffd34d"/>',
    "bluetide": '<path d="M6 34q11-14 22 0t22 0" stroke="#0b5394" stroke-width="6" fill="none"/><path d="M6 46q11-14 22 0t22 0" stroke="#1098ad" stroke-width="6" fill="none"/>',
    "circulo": '<circle cx="28" cy="28" r="18" fill="none" stroke="#0a6b3d" stroke-width="6" stroke-dasharray="26 8"/>',
    "heliora": '<circle cx="28" cy="28" r="10" fill="#e8590c"/><circle cx="28" cy="28" r="19" fill="none" stroke="#e8590c" stroke-width="3" stroke-dasharray="4 5"/>',
    "greenleaf": '<path d="M10 46C10 20 30 8 48 8c0 22-14 38-38 38z" fill="#2b8a3e"/><path d="M10 46L36 20" stroke="#fff" stroke-width="3"/>',
    "ycn": '<circle cx="20" cy="22" r="8" fill="#0b5394"/><circle cx="38" cy="22" r="8" fill="#0a6b3d"/><path d="M6 46a14 14 0 0 1 28 0zM24 46a14 14 0 0 1 28 0z" fill="#495057"/>',
    "mwb": '<rect x="10" y="10" width="36" height="36" rx="6" fill="none" stroke="#5f3dc4" stroke-width="5"/><path d="M18 36V20l10 10 10-10v16" stroke="#5f3dc4" stroke-width="4" fill="none"/>',
    "eduaccess": '<circle cx="28" cy="12" r="5" fill="#0b5394"/><path d="M12 22l16 4 16-4M28 26v10l-8 12M28 36l8 12" stroke="#0b5394" stroke-width="4" fill="none" stroke-linecap="round"/>',
}


def logo(key, name):
    w = 64 + len(name) * 13
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 56" width="{w}" height="56">'
            f'{LOGO_ICON[key]}<text x="60" y="36" font-family="Segoe UI, Arial, sans-serif" font-size="22" '
            f'font-weight="700" fill="#1d2b24">{name}</text></svg>\n')


LOGO_SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand", "logo-source.png")


def content_box(im, y0, y1, threshold=235):
    """Bounding box of non-white pixels between rows y0 and y1."""
    px, w = im.load(), im.width
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(w):
            if min(px[x, y]) < threshold:
                xs.append(x)
                ys.append(y)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def square(im, box, pad):
    """Crop box to a centred square with padding, on white."""
    x0, y0, x1, y1 = box
    side = max(x1 - x0, y1 - y0) + 2 * pad
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    canvas = Image.new("RGB", (side, side), "white")
    left, top = round(cx - side / 2), round(cy - side / 2)
    canvas.paste(im.crop((max(left, 0), max(top, 0), min(left + side, im.width), min(top + side, im.height))),
                 (max(-left, 0), max(-top, 0)))
    return canvas


def make_logos():
    """Emblem (header, footer, favicons) and full logo (social preview, PDFs) from the source artwork."""
    src = Image.open(LOGO_SOURCE).convert("RGB")
    text_top = 505                                   # the wordmark starts below this row
    emblem = square(src, content_box(src, 0, text_top), pad=10)
    full_box = content_box(src, 0, src.height)
    x0, y0, x1, y1 = full_box
    full = src.crop((x0 - 24, y0 - 24, x1 + 24, y1 + 24))
    out = lambda name: os.path.join(IMG, name)
    def png(img, name):                              # 128-colour palette keeps PNGs small
        img.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(out(name), optimize=True)

    mark = emblem.resize((192, 192), Image.LANCZOS)
    mark.save(out("logo-mark.webp"), quality=88, method=6)
    png(mark, "logo-mark.png")
    png(emblem.resize((64, 64), Image.LANCZOS), "favicon-64.png")
    png(emblem.resize((180, 180), Image.LANCZOS), "apple-touch-icon.png")
    big = full.resize((640, round(640 * full.height / full.width)), Image.LANCZOS)
    png(big, "logo.png")
    big.save(out("logo.webp"), quality=88, method=6)


def main():
    from content import SPONSORS
    os.makedirs(os.path.join(IMG, "gallery"), exist_ok=True)
    os.makedirs(os.path.join(IMG, "partners"), exist_ok=True)
    for key, data in SCENES.items():
        with open(os.path.join(IMG, "gallery", f"{key}.svg"), "w") as f:
            f.write(data)
    for tier in SPONSORS.values():
        for name, key, _ in tier:
            with open(os.path.join(IMG, "partners", f"{key}.svg"), "w") as f:
                f.write(logo(key, name))
    make_logos()


if __name__ == "__main__":
    main()
