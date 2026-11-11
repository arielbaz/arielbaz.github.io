#!/usr/bin/env python3
"""Génère les illustrations explicatives des articles (SVG, 1200x900).

Sortie : assets/img/articles/<slug>.svg
Usage  : python3 tools/make-article-illustrations.py
"""
import html
import os

OUT = os.environ.get("ARTICLE_ILL_OUT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img", "articles"))
os.makedirs(OUT, exist_ok=True)

PALETTE = {
    "Productivité": ("#e8f1ff", "#b9d4ff", "#0b64c7"),
    "Sécurité": ("#ecebff", "#c3c0ff", "#4a47c4"),
    "Filtrage": ("#e6f9ec", "#aee8c4", "#14854a"),
    "Alternatives": ("#fff2e2", "#ffd0a1", "#b8560a"),
    "Mobile": ("#f8e9ff", "#e2c1fb", "#8c35c0"),
    "Religion": ("#fcf5e0", "#ecd48e", "#8a6a1f"),
}
INK = "#18181c"
SOFT = "#5f5f6b"
FAINT = "#8a8a94"
RED = "#c93b4b"
GREEN = "#1a9e4b"


def esc(s):
    return html.escape(str(s), quote=True)


def text(x, y, s, size=28, weight=400, fill=INK, anchor="start", spacing=0, opacity=1):
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
        f'letter-spacing="{spacing}" opacity="{opacity}">{esc(s)}</text>'
    )


def panel(x, y, w, h, r=24, fill="#fff", stroke="none", extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'


def circle(cx, cy, r, fill, stroke="none", sw=1, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def line(x1, y1, x2, y2, color, width=3, dash=None, marker=False, opacity=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#arrow)"' if marker else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}{m} opacity="{opacity}"/>'


def path(d, color, width=3, fill="none", dash=None, marker=False, opacity=1):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#arrow)"' if marker else ""
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{da}{m} opacity="{opacity}"/>'


def phone(x, y, w, h, accent, screen="#fff", fill="#fff", stroke="#d9d9e4"):
    r = w * 0.18
    sw = max(2, w * 0.022)
    notch_w = w * 0.36
    return (
        f'<g>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        f'<rect x="{x+w*0.055}" y="{y+h*0.06}" width="{w*0.89}" height="{h*0.88}" rx="{r*0.7}" fill="{screen}"/>'
        f'<rect x="{x+(w-notch_w)/2}" y="{y+h*0.025}" width="{notch_w}" height="{h*0.018}" rx="{h*0.009}" fill="{accent}" opacity=".35"/>'
        f'</g>'
    )


def laptop(x, y, w, h, accent):
    r = w * 0.035
    return (
        f'<g>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" stroke="#d9d9e4" stroke-width="3"/>'
        f'<rect x="{x+w*0.045}" y="{y+h*0.05}" width="{w*0.91}" height="{h*0.84}" rx="{r*0.6}" fill="{accent}" opacity=".08"/>'
        f'<path d="M{x-w*0.09} {y+h+4} L{x+w*1.09} {y+h+4} L{x+w*1.02} {y+h+18} L{x-w*0.02} {y+h+18} Z" fill="#fff" stroke="#d9d9e4" stroke-width="3"/>'
        f'</g>'
    )


def browser(x, y, w, h, accent, url="aribaz.com"):
    r = 20
    return (
        f'<g>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" stroke="#d9d9e4" stroke-width="3"/>'
        f'<path d="M{x} {y+58} H{x+w}" stroke="#ececf2" stroke-width="3"/>'
        f'<circle cx="{x+28}" cy="{y+29}" r="6" fill="#ff6b6b"/>'
        f'<circle cx="{x+48}" cy="{y+29}" r="6" fill="#ffd166"/>'
        f'<circle cx="{x+68}" cy="{y+29}" r="6" fill="#52d273"/>'
        f'<rect x="{x+96}" y="{y+18}" width="{w*0.44}" height="22" rx="11" fill="#f3f3f7"/>'
        f'{text(x+108, y+35, url, 15, 400, FAINT)}'
        f'</g>'
    )


def lock(x, y, s, color, fill="none"):
    return (
        f'<g transform="translate({x} {y}) scale({s/24})" fill="{fill}" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
        f'<rect x="4.8" y="10.5" width="14.4" height="10" rx="2.6"/>'
        f'<path d="M8.4 10.5V8a3.6 3.6 0 0 1 7.2 0v2.5"/>'
        f'<circle cx="12" cy="15.5" r="1.3"/>'
        f'</g>'
    )


def shield(x, y, s, color, fill="none"):
    return (
        f'<g transform="translate({x} {y}) scale({s/24})" fill="{fill}" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M12 3 4.5 6v6c0 4.6 3.2 7.8 7.5 9 4.3-1.2 7.5-4.4 7.5-9V6L12 3Z"/>'
        f'</g>'
    )


def wifi(x, y, s, color, width=1.8):
    return (
        f'<g transform="translate({x} {y}) scale({s/24})" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round">'
        f'<path d="M2.5 9.2a14 14 0 0 1 19 0M5.8 12.6a9.4 9.4 0 0 1 12.4 0M9 16a4.7 4.7 0 0 1 6 0"/>'
        f'<circle cx="12" cy="19.2" r="1.2" fill="{color}" stroke="none"/>'
        f'</g>'
    )


def cloud(x, y, s, color, fill="#fff"):
    return (
        f'<g transform="translate({x} {y}) scale({s/100})" fill="{fill}" stroke="{color}" stroke-width="4" stroke-linejoin="round">'
        f'<path d="M26 70 C8 70 4 48 18 41 C18 21 42 10 56 24 C70 6 98 14 98 38 C116 40 120 70 100 70 Z"/>'
        f'</g>'
    )


def cross_badge(x, y, r, color=RED):
    return (
        f'<g>{circle(x, y, r, "#fff", color, 3)}'
        f'<path d="M{x-r*0.35} {y-r*0.35} L{x+r*0.35} {y+r*0.35} M{x+r*0.35} {y-r*0.35} L{x-r*0.35} {y+r*0.35}" stroke="{color}" stroke-width="4" stroke-linecap="round"/></g>'
    )


def check_badge(x, y, r, color=GREEN):
    return (
        f'<g>{circle(x, y, r, color)}'
        f'<path d="M{x-r*0.4} {y} L{x-r*0.08} {y+r*0.32} L{x+r*0.44} {y-r*0.32}" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>'
    )


def tag(x, y, label, fill, color="#fff", size=22, padx=18, h=40, r=20):
    w = len(label) * size * 0.58 + padx * 2
    return f'<g>{panel(x, y, w, h, r, fill)}{text(x+w/2, y+h*0.69, label, size, 700, color, "middle")}</g>'


def document(x, y, w, h, label, color, rotate=0):
    fold = 34
    body = (
        f'<g transform="rotate({rotate} {x+w/2} {y+h/2})">'
        f'<path d="M{x} {y+12} Q{x} {y} {x+12} {y} H{x+w-fold} L{x+w} {y+fold} V{y+h-12} Q{x+w} {y+h} {x+w-12} {y+h} H{x+12} Q{x} {y+h} {x} {y+h-12} Z" fill="#fff" stroke="#d9d9e4" stroke-width="3"/>'
        f'<path d="M{x+w-fold} {y} V{y+fold} H{x+w}" fill="none" stroke="#d9d9e4" stroke-width="3"/>'
        f'<rect x="{x+22}" y="{y+24}" width="{w-44}" height="{h*0.46}" rx="10" fill="{color}" opacity=".10"/>'
        f'{text(x+w/2, y+h*0.40, label, 30, 700, color, "middle")}'
        f'</g>'
    )
    return body


def keycap(x, y, w, h, label, accent=".12"):
    return (
        f'<g>{panel(x, y, w, h, 14, "#fff", "#d9d9e4")}'
        f'{panel(x, y+h-8, w, 8, 4, "#f0f0f5")}'
        f'{text(x+w/2, y+h*0.64, label, 24, 700, "#4c4c58", "middle")}</g>'
    )


def image_tile(x, y, w, h, accent, blur=False, icon="mountain"):
    inner = (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{accent}" opacity=".13"/>'
        f'<path d="M{x+w*0.12} {y+h*0.74} L{x+w*0.38} {y+h*0.42} L{x+w*0.56} {y+h*0.62} L{x+w*0.7} {y+h*0.48} L{x+w*0.9} {y+h*0.74} Z" fill="{accent}" opacity=".55"/>'
        f'<circle cx="{x+w*0.7}" cy="{y+h*0.3}" r="{min(w,h)*0.075}" fill="{accent}" opacity=".55"/>'
    )
    if blur:
        mosaic = []
        step = 14
        for yy in range(int(y), int(y+h), step):
            for xx in range(int(x), int(x+w), step):
                if (xx // step + yy // step) % 3 == 0:
                    mosaic.append(f'<rect x="{xx}" y="{yy}" width="{step}" height="{step}" fill="#fff" opacity=".35"/>')
        inner = f'<g opacity=".85">{inner}</g>' + "".join(mosaic)
    return f'<g clip-path="url(#clip-{x}-{y})"><defs><clipPath id="clip-{x}-{y}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16"/></clipPath></defs>{inner}</g>'


def qr(x, y, size, color):
    cell = size / 21
    out = [panel(x, y, size, size, 14, "#fff", "#d9d9e4")]
    pattern = [
        "111111101010101111111",
        "100000101110101000001",
        "101110101010101011101",
        "101110100101101011101",
        "101110101110101011101",
        "100000100010101000001",
        "111111101010101111111",
        "000000001101000000000",
        "110101110011011010110",
        "001011001100101100100",
        "111010110101110010111",
        "010101001110001101000",
        "101110111011101011011",
        "000000001010001100010",
        "111111101101111010101",
        "100000101001001010010",
        "101110101111101110111",
        "101110100010001010100",
        "101110101101111011011",
        "100000101001000110010",
        "111111101011101010111",
    ]
    for r, row in enumerate(pattern):
        for c, v in enumerate(row):
            if v == "1":
                out.append(f'<rect x="{x+cell*c+cell*0.08}" y="{y+cell*r+cell*0.08}" width="{cell*0.84}" height="{cell*0.84}" fill="{color}"/>')
    return "".join(out)


def tower(x, y, w, h, color):
    cx = x + w / 2
    return (
        f'<g stroke="{color}" stroke-width="5" stroke-linecap="round" fill="none">'
        f'<path d="M{cx-w*0.22} {y+h} L{cx-w*0.06} {y+h*0.35} L{cx+w*0.06} {y+h*0.35} L{cx+w*0.22} {y+h}"/>'
        f'<path d="M{cx-w*0.2} {y+h*0.28} Q{cx} {y+h*0.1} {cx+w*0.2} {y+h*0.28}"/>'
        f'<path d="M{cx-w*0.32} {y+h*0.18} Q{cx} {y-h*0.02} {cx+w*0.32} {y+h*0.18}"/>'
        f'<circle cx="{cx}" cy="{y+h*0.35}" r="7" fill="{color}" stroke="none"/>'
        f'</g>'
    )


def house(x, y, w, h, accent):
    return (
        f'<g fill="none" stroke="{accent}" stroke-width="5" stroke-linejoin="round">'
        f'<path d="M{x} {y+h*0.42} L{x+w/2} {y} L{x+w} {y+h*0.42}"/>'
        f'<path d="M{x+w*0.08} {y+h*0.38} V{y+h} H{x+w*0.92} V{y+h*0.38}"/>'
        f'<rect x="{x+w*0.42}" y="{y+h*0.62}" width="{w*0.16}" height="{h*0.38}" rx="4"/>'
        f'</g>'
    )


def usb_drive(x, y, w, h, accent):
    return (
        f'<g>{panel(x, y, w, h, 14, "#fff", "#d9d9e4")}'
        f'{panel(x+w*0.08, y+h*0.12, w*0.55, h*0.76, 8, accent, "none", "opacity=\".14\"")}'
        f'<rect x="{x+w*0.68}" y="{y+h*0.42}" width="{w*0.18}" height="{h*0.16}" rx="4" fill="#c9c9d4"/>'
        f'<rect x="{x+w*0.84}" y="{y+h*0.44}" width="{w*0.12}" height="{h*0.12}" rx="3" fill="{accent}" opacity=".45"/></g>'
    )


def frame(cat, headline, scene, accent):
    c1, c2, _ = PALETTE[cat]
    head = "".join(text(72, 185 + i * 68, line, 60, 700, INK) for i, line in enumerate(headline))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="12" stdDeviation="18" flood-color="#1e1e37" flood-opacity="0.14"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{accent}"/>
    </marker>
    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.4" fill="#22223a" opacity=".07"/>
    </pattern>
  </defs>
  <rect width="1200" height="900" fill="url(#bg)"/>
  <circle cx="1080" cy="60" r="260" fill="#fff" opacity=".22"/>
  <circle cx="110" cy="850" r="300" fill="#fff" opacity=".18"/>
  <rect x="36" y="36" width="1128" height="828" rx="44" fill="#fff" fill-opacity=".94" filter="url(#shadow)"/>
  <rect x="36" y="36" width="1128" height="828" rx="44" fill="url(#dots)" opacity=".35"/>
  <circle cx="76" cy="86" r="7" fill="{accent}"/>
  {text(96, 94, cat.upper(), 20, 700, accent, spacing=1.2)}
  {text(1128, 94, "ARIBAZ · ILLUSTRATION", 16, 700, FAINT, "end", spacing=1.2)}
  {head}
  {scene}
  {text(1128, 824, "ARIBAZ", 22, 700, INK, "end", opacity=.55)}
</svg>'''


def caption(y, s, size=23):
    return text(600, y, s, size, 400, SOFT, "middle")


def scene_bitchat(a):
    out = []
    pts = [(145, 470, "Toi"), (385, 400, "Relais"), (600, 500, "Relais"), (815, 400, "Relais"), (1030, 470, "Reçu")]
    out.append(f'<g opacity=".7">{cloud(525, 300, 110, "#9a9aac", "#fff")}</g>')
    out.append(cross_badge(630, 315, 19, RED))
    for i, (x, y, label) in enumerate(pts):
        if i < 4:
            nx, ny = pts[i + 1][0], pts[i + 1][1]
            out.append(path(f"M{x+44} {y} C{x+110} {y-50} {nx-110} {ny-50} {nx-44} {ny}", a, 4, dash="10 9", marker=True))
    for i, (x, y, label) in enumerate(pts):
        w, h = 88, 166
        fill = a if i in (0, 4) else "#fff"
        screen = "#f0efff" if i in (0, 4) else "#fff"
        out.append(phone(x - w / 2, y - h / 2, w, h, a, screen=screen, fill=fill))
        if i == 0:
            out.append(panel(x - 30, y - 14, 60, 34, 10, "#fff"))
            out.append(lock(x - 9, y - 8, 18, a))
        if i == 4:
            out.append(check_badge(x, y + 48, 17, a))
        out.append(text(x, y + h / 2 + 27, label, 21, 700, "#4c4c58", "middle"))
    out.append(caption(720, "Le message saute de téléphone en téléphone, sans internet."))
    return "".join(out)


def scene_ublock(a):
    out = [browser(170, 320, 860, 420, a, "site-actu.fr")]
    out.append(panel(210, 405, 250, 16, 8, "#e8e8f0"))
    out.append(panel(210, 438, 470, 11, 5, "#eeeef5"))
    out.append(panel(210, 462, 420, 11, 5, "#eeeef5"))
    out.append(panel(210, 500, 780, 150, 14, "#f4f4f8"))
    out.append(text(240, 540, "ARTICLE", 19, 700, "#a0a0ac"))
    out.append(f'<g filter="url(#shadow)">{shield(558, 485, 190, a, "#fff")}</g>')
    out.append(text(653, 580, "uBlock", 28, 700, a, "middle"))
    out.append(text(653, 700, "listes de blocage", 19, 400, SOFT, "middle"))
    for x, y, rot in [(78, 382, -7), (58, 508, 4), (92, 634, 8)]:
        out.append(f'<g transform="rotate({rot} {x+80} {y+40})">')
        out.append(panel(x, y, 160, 80, 14, "#fff", "#e5c3c8"))
        out.append(text(x + 80, y + 37, "PUB", 21, 700, RED, "middle"))
        out.append(panel(x + 20, y + 52, 120, 9, 4, "#f3d9dd"))
        out.append('</g>')
        out.append(cross_badge(x + 150, y + 5, 13, RED))
    out.append(path("M250 430 C340 440 410 485 520 520", RED, 4, dash="8 8", marker=True))
    out.append(path("M240 560 C340 560 420 560 545 560", RED, 4, dash="8 8", marker=True))
    out.append(caption(790, "Les requêtes publicitaires sont arrêtées avant la page."))
    return "".join(out)


def scene_signal(a):
    out = [phone(120, 380, 130, 250, a), phone(950, 380, 130, 250, a)]
    for x in (120, 950):
        out.append(panel(x + 22, 455, 86, 42, 12, a, "none", 'opacity=".12"'))
        out.append(panel(x + 32, 468, 48, 7, 3, a, "none", 'opacity=".3"'))
    out.append(text(185, 680, "Toi", 22, 700, "#4c4c58", "middle"))
    out.append(text(1015, 680, "Contact", 22, 700, "#4c4c58", "middle"))
    out.append(panel(470, 365, 260, 300, 24, "#2b2b3a", "#1d1d2b"))
    for i in range(3):
        y = 390 + i * 80
        out.append(panel(492, y, 216, 58, 10, "#3a3a4d"))
        out.append(circle(512, y + 29, 5, "#5be08a"))
        out.append(panel(530, y + 22, 140, 8, 4, "#55556b"))
    out.append(text(600, 345, "serveur", 21, 700, SOFT, "middle"))
    out.append(text(600, 373, "?????", 24, 700, RED, "middle"))
    out.append(panel(535, 590, 130, 58, 10, "#fff", "#d8d8e4"))
    out.append(path("M535 595 L600 632 L665 595", a, 3))
    out.append(lock(582, 598, 34, a))
    out.append(path("M260 480 C330 470 390 470 460 480", a, 4, dash="10 8", marker=True))
    out.append(path("M740 480 C810 470 870 470 940 480", a, 4, dash="10 8", marker=True))
    out.append(lock(343, 443, 30, a))
    out.append(lock(843, 443, 30, a))
    out.append(caption(780, "Le serveur transporte le message, mais ne peut pas le lire."))
    return "".join(out)


def scene_localsend(a):
    out = []
    out.append(f'<g opacity=".7">{cloud(660, 305, 100, "#9a9aac", "#fff")}</g>')
    out.append(cross_badge(750, 318, 19, RED))
    out.append(text(600, 385, "pas de cloud", 20, 700, FAINT, "middle"))
    out.append(laptop(150, 440, 310, 200, a))
    out.append(phone(930, 425, 120, 220, a))
    out.append(text(305, 690, "Ordinateur", 21, 700, "#4c4c58", "middle"))
    out.append(text(990, 690, "Téléphone", 21, 700, "#4c4c58", "middle"))
    out.append(path("M480 520 C600 470 720 470 900 520", a, 5, dash="12 10", marker=True))
    out.append(panel(590, 470, 120, 80, 16, "#fff", "#d9d9e4"))
    out.append(path("M612 492 H672 L692 512 V536 H612 Z", a, 3, fill="none"))
    out.append(path("M672 492 V512 H692", a, 3))
    out.append(wifi(575, 290, 60, a))
    out.append(text(600, 620, "même Wi-Fi", 23, 700, a, "middle"))
    out.append(caption(760, "Le fichier passe directement d’un appareil à l’autre."))
    return "".join(out)


def scene_sharex(a):
    out = [browser(100, 320, 760, 410, a, "page-à-capturer.fr")]
    out.append(panel(140, 400, 280, 16, 8, "#e8e8f0"))
    out.append(panel(140, 432, 460, 11, 5, "#eeeef5"))
    out.append(panel(140, 456, 410, 11, 5, "#eeeef5"))
    out.append(panel(140, 495, 680, 150, 14, "#f4f4f8"))
    out.append(f'<rect x="160" y="405" width="380" height="180" rx="10" fill="none" stroke="{a}" stroke-width="4" stroke-dasharray="10 8"/>')
    out.append(text(160, 620, "zone sélectionnée", 18, 700, a))
    out.append(panel(890, 320, 220, 410, 20, "#fff", "#d9d9e4"))
    out.append(text(1000, 356, "Outils", 20, 700, INK, "middle"))
    tools = [("↗", "Flèche"), ("T", "Texte"), ("◌", "Flou"), ("▦", "Recadrer")]
    for i, (glyph, label) in enumerate(tools):
        y = 385 + i * 78
        out.append(panel(915, y, 170, 58, 12, "#f6f6fa"))
        out.append(text(943, y + 38, glyph, 26, 700, a))
        out.append(text(980, y + 36, label, 20, 400, "#4c4c58"))
    out.append(caption(800, "Capture, annotation et export dans le même outil."))
    return "".join(out)


def scene_onlyoffice(a):
    out = []
    docs = [(110, 380, 220, 300, "DOCX", "#0b64c7", -3), (370, 345, 240, 330, "XLSX", "#14854a", 0), (640, 380, 220, 300, "PPTX", "#b8560a", 3)]
    for x, y, w, h, label, color, rot in docs:
        out.append(document(x, y, w, h, label, color, rot))
        out.append(check_badge(x + w - 8, y + 8, 22, GREEN))
    out.append(panel(900, 380, 220, 100, 18, a))
    out.append(text(1010, 450, "0 €", 46, 700, "#fff", "middle"))
    out.append(text(1010, 522, "sans abonnement", 21, 700, a, "middle"))
    out.append(f'<g opacity=".55">{panel(920, 570, 190, 90, 14, "#fff", "#d9d9e4")}'
               f'{text(1015, 606, "9,99 € / mois", 21, 700, SOFT, "middle")}'
               f'{panel(950, 625, 130, 10, 5, "#e8e8f0")}</g>')
    out.append(cross_badge(1100, 580, 24, RED))
    out.append(caption(790, "Tes fichiers Word, Excel et PowerPoint restent compatibles."))
    return "".join(out)


def scene_handy(a):
    out = []
    out.append(f'<g opacity=".7">{cloud(695, 300, 100, "#9a9aac", "#fff")}</g>')
    out.append(cross_badge(785, 313, 19, RED))
    out.append(text(600, 380, "aucun envoi", 20, 700, FAINT, "middle"))
    # micro
    out.append(panel(125, 405, 120, 150, 60, "#fff", "#d9d9e4"))
    out.append(panel(160, 430, 50, 100, 25, a, "none", 'opacity=".18"'))
    out.append(path("M185 555 V595 M155 595 H215", a, 5))
    out.append(text(185, 645, "Micro", 21, 700, "#4c4c58", "middle"))
    # waveform
    pts = []
    for i in range(18):
        x = 260 + i * 14
        amp = 12 + 22 * abs((i * 7) % 9 - 4) / 4
        pts.append(f"{x},{470 - amp} {x},{470 + amp}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{a}" stroke-width="4" stroke-linecap="round" opacity=".7"/>')
    # laptop
    out.append(laptop(460, 380, 350, 240, a))
    out.append(panel(545, 445, 180, 95, 14, "#fff", a))
    out.append(text(635, 482, "Whisper", 23, 700, a, "middle"))
    out.append(text(635, 511, "en local", 19, 400, SOFT, "middle"))
    out.append(text(635, 665, "IA locale", 21, 700, "#4c4c58", "middle"))
    # document
    out.append(panel(885, 400, 220, 250, 18, "#fff", "#d9d9e4"))
    for i in range(6):
        out.append(panel(915, 450 + i * 26, 150 - (i % 2) * 30, 8, 4, "#e8e8f0"))
    out.append(text(995, 690, "Texte", 21, 700, "#4c4c58", "middle"))
    out.append(path("M330 470 C380 470 420 470 450 470", a, 4, dash="9 8", marker=True))
    out.append(path("M820 470 C845 470 860 470 880 470", a, 4, dash="9 8", marker=True))
    out.append(caption(770, "La dictée est transcrite sur l’ordinateur, pas sur un serveur."))
    return "".join(out)


def scene_notebooklm(a):
    out = []
    for i in range(3):
        x, y = 105 + i * 17, 360 + i * 17
        out.append(panel(x, y, 280, 340, 18, "#fff", "#d9d9e4"))
        out.append(text(x + 24, y + 46, "PDF", 24, 700, a))
        for j in range(8):
            out.append(panel(x + 24, y + 80 + j * 25, 220 - (j % 3) * 25, 8, 4, "#e8e8f0"))
    out.append(text(245, 730, "40 pages", 22, 700, "#4c4c58", "middle"))
    out.append(path("M430 520 C520 520 580 520 670 520", a, 5, dash="12 10", marker=True))
    out.append(text(550, 490, "résumé + voix", 22, 700, a, "middle"))
    out.append(phone(880, 350, 190, 340, a))
    out.append(panel(900, 390, 150, 230, 16, "#f6f6fb"))
    out.append(circle(975, 455, 38, a))
    out.append(path("M963 438 L998 455 L963 472 Z", "#fff", 1, fill="#fff"))
    out.append(text(975, 520, "2 voix", 21, 700, a, "middle"))
    for i in range(7):
        h = 10 + (i * 13) % 26
        out.append(panel(925 + i * 17, 565 - h / 2, 9, h, 4, a, "none", 'opacity=".55"'))
    out.append(text(975, 730, "Podcast", 22, 700, "#4c4c58", "middle"))
    out.append(caption(790, "Tes documents deviennent une conversation audio à écouter ailleurs."))
    return "".join(out)


def scene_owc(a):
    out = []
    out.append(phone(130, 340, 190, 350, a))
    colors = ["#ffd6a5", "#bde0fe", "#cdb4db", "#a2d2ff", "#ffc8dd", "#b9fbc0", "#fde4cf", "#caffbf", "#ffd670"]
    for i, col in enumerate(colors):
        x = 150 + (i % 3) * 52
        y = 380 + (i // 3) * 62
        out.append(panel(x, y, 42, 48, 8, col))
    out.append(text(225, 730, "Galerie iPhone", 22, 700, "#4c4c58", "middle"))
    out.append(path("M330 515 C450 620 620 620 880 535", a, 5))
    out.append(usb_drive(890, 490, 210, 100, a))
    out.append(text(995, 630, "Disque USB", 22, 700, "#4c4c58", "middle"))
    out.append(f'<g opacity=".65">{cloud(900, 300, 100, "#9a9aac", "#fff")}</g>')
    out.append(cross_badge(1000, 315, 20, RED))
    out.append(text(875, 380, "iCloud", 20, 700, FAINT, "middle"))
    out.append(tag(930, 650, "0 € de plus", a, "#fff", 20))
    out.append(caption(790, "Le câble copie les photos vers un disque, sans passer par iCloud."))
    return "".join(out)


def scene_familylink(a):
    out = []
    out.append(phone(130, 350, 170, 320, a))
    out.append(phone(900, 350, 170, 320, a))
    out.append(text(215, 700, "Parent", 22, 700, "#4c4c58", "middle"))
    out.append(text(985, 700, "Enfant", 22, 700, "#4c4c58", "middle"))
    # parent dashboard rows
    rows = [("Temps d’écran", "1 h 30"), ("Applications", "validées"), ("Position", "activée")]
    for i, (label, value) in enumerate(rows):
        y = 404 + i * 78
        out.append(panel(148, y, 134, 62, 10, "#f6f6fa"))
        out.append(text(163, y + 26, label, 19, 700, SOFT))
        out.append(text(163, y + 51, value, 21, 700, a))
    # child app grid
    for i in range(6):
        x = 922 + (i % 3) * 42
        y = 410 + (i // 3) * 48
        out.append(panel(x, y, 30, 30, 9, a, "none", 'opacity=".16"'))
    out.append(check_badge(1045, 395, 16, GREEN))
    # center shield and dotted line
    out.append(shield(535, 410, 130, a, "#fff"))
    out.append(text(600, 575, "Family Link", 22, 700, a, "middle"))
    out.append(path("M305 520 C380 520 450 520 520 520", a, 4, dash="9 8", marker=True))
    out.append(path("M680 520 C760 520 820 520 890 520", a, 4, dash="9 8", marker=True))
    out.append(caption(790, "Temps d’écran, applications validées, localisation : le cadre est posé."))
    return "".join(out)


def scene_dns(a):
    out = []
    out.append(house(390, 350, 420, 340, a))
    # router inside
    out.append(panel(545, 515, 120, 70, 12, "#fff", a))
    out.append(text(605, 548, "BOX", 18, 700, a, "middle"))
    out.append(line(575, 515, 560, 485, a, 4))
    out.append(line(635, 515, 650, 485, a, 4))
    out.append(circle(560, 483, 5, a))
    out.append(circle(650, 483, 5, a))
    # devices
    out.append(laptop(120, 545, 220, 145, a))
    out.append(phone(930, 530, 100, 180, a))
    out.append(panel(820, 650, 90, 55, 8, "#fff", "#d9d9e4"))
    out.append(text(230, 735, "Ordinateur", 19, 700, "#4c4c58", "middle"))
    out.append(text(980, 735, "Mobile", 19, 700, "#4c4c58", "middle"))
    out.append(text(865, 735, "TV", 19, 700, "#4c4c58", "middle"))
    # DNS gate
    out.append(panel(470, 300, 260, 56, 28, a))
    out.append(text(600, 337, "1.1.1.3", 24, 700, "#fff", "middle"))
    # blocked cards
    for i, (x, y, label) in enumerate([(90, 330, "PUB"), (90, 405, "MALWARE")]):
        out.append(panel(x, y, 190, 54, 12, "#fff", "#e5c3c8"))
        out.append(text(x + 95, y + 34, label, 18, 700, RED, "middle"))
        out.append(cross_badge(x + 190, y + 2, 13, RED))
    out.append(path("M285 360 C350 360 400 360 455 360", RED, 4, dash="8 8", marker=True))
    out.append(caption(790, "Toutes les requêtes du réseau passent par le même filtre DNS."))
    return "".join(out)


def scene_appelswifi(a):
    out = []
    out.append(phone(135, 390, 130, 240, a))
    out.append(panel(158, 445, 84, 45, 12, a, "none", 'opacity=".14"'))
    out.append(text(200, 474, "Appel", 16, 700, a, "middle"))
    out.append(text(200, 680, "Toi", 22, 700, "#4c4c58", "middle"))
    # crossed mobile signal
    for i in range(4):
        h = 10 + i * 8
        out.append(panel(285 + i * 14, 400 - h, 9, h, 3, RED, "none", 'opacity=".45"'))
    out.append(cross_badge(335, 380, 18, RED))
    out.append(text(330, 435, "pas de réseau", 18, 700, RED, "middle"))
    # router
    out.append(panel(485, 480, 230, 110, 20, "#fff", "#d9d9e4"))
    out.append(text(600, 525, "BOX", 20, 700, a, "middle"))
    out.append(line(520, 480, 495, 440, a, 5))
    out.append(line(680, 480, 705, 440, a, 5))
    out.append(circle(495, 438, 6, a))
    out.append(circle(705, 438, 6, a))
    out.append(wifi(555, 305, 90, a))
    out.append(text(600, 640, "Wi-Fi", 23, 700, a, "middle"))
    # tower
    out.append(tower(960, 350, 160, 310, a))
    out.append(text(1040, 690, "Opérateur", 21, 700, "#4c4c58", "middle"))
    out.append(path("M300 460 C380 450 430 450 475 460", a, 4, dash="9 8", marker=True))
    out.append(path("M720 520 C800 520 890 520 950 520", a, 4, dash="9 8", marker=True))
    out.append(caption(770, "L’appel passe par la box Wi-Fi, puis rejoint le réseau de l’opérateur."))
    return "".join(out)


def scene_wizmage(a):
    out = [browser(100, 320, 1000, 440, a, "les-images.fr")]
    offsets = [(150, 400), (470, 400), (790, 400), (150, 600), (470, 600), (790, 600)]
    for i, (x, y) in enumerate(offsets):
        out.append(image_tile(x, y, 250, 150, a, blur=(i != 4)))
    # sharp tile marker and cursor
    out.append(f'<rect x="470" y="600" width="250" height="150" rx="16" fill="none" stroke="{a}" stroke-width="4"/>')
    out.append(text(595, 780, "clic pour révéler", 20, 700, a, "middle"))
    out.append(f'<g><path d="M690 720 L690 770 L704 757 L715 778 L725 772 L714 752 L733 749 Z" fill="#fff" stroke="{INK}" stroke-width="3"/></g>')
    out.append(caption(800, "Les images sont floutées par défaut, une par une."))
    return "".join(out)


def scene_nsfw(a):
    out = [browser(100, 320, 700, 440, a, "image-board.test")]
    for i, (x, y) in enumerate([(145, 400), (355, 400), (565, 400), (145, 600), (355, 600)]):
        out.append(image_tile(x, y, 180, 150, a, blur=(i in (1, 3))))
    out.append(circle(560, 675, 44, "#fff", a, 4))
    out.append(text(560, 685, "IA", 24, 700, a, "middle"))
    out.append(path("M815 470 C840 470 860 470 885 470", a, 4, dash="9 8", marker=True))
    out.append(panel(885, 390, 210, 190, 22, "#fff", a))
    out.append(text(990, 430, "Analyse", 20, 700, a, "middle"))
    out.append(text(990, 458, "locale", 20, 700, a, "middle"))
    for i in range(4):
        out.append(panel(920 + i * 38, 490, 26, 26, 8, a, "none", 'opacity=".2"'))
    out.append(cross_badge(1080, 605, 22, RED))
    out.append(text(990, 650, "aucun envoi", 18, 700, RED, "middle"))
    out.append(caption(790, "L’IA examine les images dans le navigateur, puis les masque."))
    return "".join(out)


def scene_hibp(a):
    out = []
    out.append(panel(100, 360, 480, 82, 41, "#fff", "#d9d9e4"))
    out.append(text(130, 410, "toi@exemple.com", 24, 400, INK))
    out.append(text(130, 320, "Ton adresse e-mail", 18, 700, SOFT))
    out.append(path("M600 400 C660 400 700 400 745 400", a, 4, dash="9 8", marker=True))
    for i in range(3):
        x, y = 760 + i * 18, 300 + i * 30
        out.append(panel(x, y, 280, 240, 18, "#fff", "#d9d9e4"))
        out.append(text(x + 24, y + 50, "FUITE 0" + str(i + 1), 22, 700, RED))
        out.append(panel(x + 24, y + 80, 200, 10, 5, "#eeeef5"))
        out.append(panel(x + 24, y + 104, 160, 10, 5, "#eeeef5"))
    out.append(panel(760, 560, 300, 54, 27, a))
    out.append(text(910, 596, "3 fuites connues", 21, 700, "#fff", "middle"))
    out.append(panel(100, 560, 480, 82, 41, "#fff", "#e5c3c8"))
    out.append(text(130, 610, "••••••••••", 26, 700, FAINT))
    out.append(cross_badge(580, 560, 22, RED))
    out.append(text(130, 670, "Le mot de passe n’est jamais demandé", 18, 700, RED))
    out.append(caption(790, "Vérifie ton adresse, puis change les mots de passe exposés."))
    return "".join(out)


def scene_pressepapiers(a):
    out = []
    out.append(panel(300, 330, 560, 420, 26, "#fff", "#d9d9e4"))
    out.append(panel(500, 312, 160, 34, 12, a))
    entries = [("TXT", "Un texte copié", "#e8f1ff"), ("IMG", "Une capture", "#e6f9ec"), ("URL", "aribaz.com", "#fff2e2"), ("#", "Une couleur", "#f8e9ff")]
    for i, (kind, label, col) in enumerate(entries):
        y = 380 + i * 84
        out.append(panel(335, y, 490, 66, 12, col))
        out.append(text(360, y + 42, kind, 20, 700, a))
        out.append(text(430, y + 42, label, 20, 400, "#4c4c58"))
        out.append(text(790, y + 42, "↩", 22, 700, a, "middle"))
    out.append(keycap(920, 380, 200, 86, "Win + V"))
    out.append(text(1020, 520, "Windows", 21, 700, "#4c4c58", "middle"))
    out.append(text(1020, 550, "macOS : app tiers", 16, 400, FAINT, "middle"))
    out.append(caption(800, "L’historique garde plusieurs copies : tu choisis celle à coller."))
    return "".join(out)


def scene_esim(a):
    out = []
    out.append(qr(100, 350, 270, a))
    out.append(text(235, 680, "QR code", 22, 700, "#4c4c58", "middle"))
    out.append(path("M410 480 C520 480 600 480 700 480", a, 4, dash="10 9", marker=True))
    out.append(phone(780, 320, 200, 370, a))
    out.append(panel(815, 390, 130, 120, 16, "#f6f6fb"))
    out.append(panel(850, 420, 60, 46, 10, "#fff", a))
    out.append(text(880, 450, "eSIM", 16, 700, a, "middle"))
    out.append(check_badge(970, 355, 22, GREEN))
    out.append(text(880, 720, "Ligne active", 22, 700, "#4c4c58", "middle"))
    # old SIM crossed
    out.append(f'<g transform="rotate(-8 420 620)">')
    out.append(panel(330, 580, 190, 120, 16, "#fff", "#d9d9e4"))
    out.append(panel(360, 610, 130, 60, 8, a, "none", 'opacity=".14"'))
    out.append(text(425, 648, "SIM", 24, 700, a, "middle"))
    out.append('</g>')
    out.append(cross_badge(500, 590, 24, RED))
    out.append(caption(790, "Le profil eSIM se télécharge dans le téléphone, sans carte plastique."))
    return "".join(out)


SCENES = {
    "bitchat": ("Sécurité", ["Sans réseau,", "sans serveur."], scene_bitchat),
    "ublock-origin": ("Sécurité", ["La pub n’entre", "jamais."], scene_ublock),
    "signal": ("Sécurité", ["Le serveur ne lit", "rien."], scene_signal),
    "localsend": ("Alternatives", ["Deux appareils.", "Zéro cloud."], scene_localsend),
    "sharex": ("Productivité", ["Capture. Annote.", "Envoie."], scene_sharex),
    "onlyoffice": ("Productivité", ["Mêmes fichiers.", "Zéro abonnement."], scene_onlyoffice),
    "handy": ("Productivité", ["La voix reste", "chez toi."], scene_handy),
    "notebooklm": ("Productivité", ["40 pages.", "Un podcast."], scene_notebooklm),
    "owc-copy-that": ("Mobile", ["Tes photos,", "hors d’iCloud."], scene_owc),
    "family-link": ("Filtrage", ["Le cadre, sans", "l’espionnage."], scene_familylink),
    "dns-cloudflare": ("Filtrage", ["Un filtre pour", "toute la maison."], scene_dns),
    "appels-wifi": ("Mobile", ["Appeler sans", "réseau mobile."], scene_appelswifi),
    "wizmage": ("Filtrage", ["Les images attendent", "ton clic."], scene_wizmage),
    "nsfw-filter": ("Filtrage", ["L’IA regarde.", "Pas le serveur."], scene_nsfw),
    "have-i-been-pwned": ("Sécurité", ["Ton adresse a-t-elle", "fuité ?"], scene_hibp),
    "presse-papiers": ("Productivité", ["Copier plusieurs fois.", "Coller au choix."], scene_pressepapiers),
    "esim": ("Mobile", ["Une ligne, sans", "plastique."], scene_esim),
    "brave": ("Alternatives", ["Avant.", "Après."], None),
}




def scene_brave(a):
    out = []
    # left: polluted
    out.append(browser(80, 330, 500, 390, a, "site-avant.fr"))
    for x, y, w, h in [(105, 415, 220, 95), (340, 415, 210, 60), (105, 535, 430, 80), (340, 490, 210, 80)]:
        out.append(panel(x, y, w, h, 10, "#fff", "#e5c3c8"))
        out.append(text(x + 14, y + 26, "PUB", 16, 700, RED))
        out.append(panel(x + 14, y + 38, w - 28, 8, 4, "#f3d9dd"))
    out.append(cross_badge(550, 338, 20, RED))
    out.append(text(330, 620, "Sans Brave", 21, 700, FAINT, "middle"))
    # right: clean
    out.append(browser(620, 330, 500, 390, a, "site-après.fr"))
    out.append(panel(650, 415, 180, 16, 8, "#e8e8f0"))
    out.append(panel(650, 445, 380, 11, 5, "#eeeef5"))
    out.append(panel(650, 468, 320, 11, 5, "#eeeef5"))
    out.append(panel(650, 510, 430, 120, 14, "#f2f2f7"))
    out.append(circle(740, 570, 28, a))
    out.append(path("M732 556 L756 570 L732 584 Z", "#fff", 1, fill="#fff"))
    out.append(text(790, 565, "YouTube", 18, 700, SOFT))
    out.append(text(790, 590, "en fond, sans pub", 16, 400, FAINT))
    out.append(shield(700, 340, 56, a, "#fff"))
    out.append(text(728, 379, "B", 27, 700, a, "middle"))
    out.append(text(870, 620, "Avec Brave", 21, 700, "#4c4c58", "middle"))
    out.append(caption(790, "Le bouclier bloque pubs et traqueurs, sans extension à installer."))
    return "".join(out)

# make brave available to the main table
SCENES["brave"] = ("Alternatives", ["Avant.", "Après."], scene_brave)


if __name__ == "__main__":
    for slug, (cat, headline, fn) in SCENES.items():
        if fn is None:
            continue
        _, _, accent = PALETTE[cat]
        svg = frame(cat, headline, fn(accent), accent)
        with open(os.path.join(OUT, slug + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        print("ok", slug)
