from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

import json
OUT = "assets/img/cards"
MANIFEST = json.load(open("assets/img/logos/manifest.json"))
os.makedirs(OUT, exist_ok=True)

PUNCH = {
 "ublock-origin": "Les pubs bloquées\navant même d'arriver.",
 "brave": "YouTube en fond,\nzéro pub.",
 "signal": "La messagerie que\npersonne ne peut lire.",
 "localsend": "Tes fichiers,\nsans le cloud.",
 "sharex": "Capture, annote,\npartage.",
 "onlyoffice": "Word et Excel,\nsans abonnement.",
 "handy": "Tu parles,\nça s'écrit.",
 "notebooklm": "Tes PDF deviennent\nun podcast.",
 "owc-copy-that": "Tes photos\nquittent iCloud.",
 "family-link": "Un Android sous\nsurveillance douce.",
 "dns-cloudflare": "Toute la maison\nfiltrée en 2 minutes.",
 "appels-wifi": "Appelle même\nsans réseau.",
 "wizmage": "Les images,\nen flou.",
 "nsfw-filter": "L'indésirable,\nmasqué.",
 "have-i-been-pwned": "Ton adresse a fuité ?\nVérifie.",
 "presse-papiers": "Copier-coller,\nen série.",
 "esim": "Une ligne,\nsans carte à découper.",
 "bitchat": "Sans réseau,\nsans compte.",
 "appels-wifi": "Appelle même\nsans réseau.",
}

PALETTE = {
 "Productivité": ((232, 241, 255), (185, 212, 255)),
 "Sécurité": ((236, 235, 255), (195, 192, 255)),
 "Filtrage": ((230, 249, 236), (174, 232, 196)),
 "Alternatives": ((255, 242, 226), (255, 208, 161)),
 "Mobile": ((248, 233, 255), (226, 193, 251)),
 "Religion": ((252, 245, 224), (236, 212, 142)),
}

CAT = {
 "ublock-origin":"Sécurité","brave":"Alternatives","signal":"Sécurité","localsend":"Alternatives",
 "sharex":"Productivité","onlyoffice":"Productivité","handy":"Productivité","notebooklm":"Productivité",
 "owc-copy-that":"Mobile","family-link":"Filtrage","dns-cloudflare":"Filtrage","appels-wifi":"Mobile",
 "wizmage":"Filtrage","nsfw-filter":"Filtrage","have-i-been-pwned":"Sécurité","presse-papiers":"Productivité",
 "esim":"Mobile","bitchat":"Sécurité",
}

def font(size, bold=True):
    cands = ["/System/Library/Fonts/HelveticaNeue.ttc", "/System/Library/Fonts/SFNS.ttf"]
    if bold:
        cands = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] + cands
    for p in cands:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def gradient(w, h, c1, c2):
    base = Image.new("RGB", (164, 92))
    px = base.load()
    for y in range(92):
        for x in range(164):
            t = (x / 163 * 0.55 + y / 91 * 0.45)
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return base.resize((w, h), Image.BICUBIC).convert("RGBA")

def wrap(draw, text, f, maxw):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if draw.textlength(test, font=f) <= maxw:
                cur = test
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
    return lines

W, H = 1600, 900
for slug, text in PUNCH.items():
    cat = CAT.get(slug, "Productivité")
    c1, c2 = PALETTE[cat]
    img = gradient(W, H, c1, c2)

    # halo
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-260, -320, 900, 700], fill=(255, 255, 255, 120))
    gd.ellipse([1000, 300, 1900, 1100], fill=(255, 255, 255, 70))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(120)))

    d = ImageDraw.Draw(img)

    # tuile logo + ombre
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([132, 322, 408, 616], radius=80, fill=(35, 35, 55, 110))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(34)))

    logo_path = f"assets/img/logos/{slug}.png"
    is_full = MANIFEST.get(slug, {}).get("full", False)
    if is_full and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA").resize((300, 300), Image.LANCZOS)
        mask = Image.new("L", (300, 300), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, 299, 299], radius=74, fill=255)
        img.paste(logo, (120, 300), mask)
    else:
        tile = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        ImageDraw.Draw(tile).rounded_rectangle([0, 0, 299, 299], radius=74, fill=(255, 255, 255, 255))
        img.alpha_composite(tile, (120, 300))
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((186, 186), Image.LANCZOS)
            img.alpha_composite(logo, (120 + (300 - logo.width) // 2, 300 + (300 - logo.height) // 2))

    # catégorie
    fcat = font(24, True)
    d.text((500, 268), cat.upper(), font=fcat, fill=(70, 66, 64, 165))
    d.line([(500, 308), (500 + d.textlength(cat.upper(), font=fcat), 308)], fill=(70, 66, 64, 90), width=2)

    # punchline
    fp = font(80, True)
    lines = wrap(d, text, fp, 980)
    lh = 96
    total = len(lines) * lh
    y = 470 - total // 2 + 20
    for ln in lines:
        d.text((498, y), ln, font=fp, fill=(24, 24, 28))
        y += lh

    # signature
    fs = font(26, True)
    d.text((W - 120 - d.textlength("ARIBAZ", font=fs), H - 92), "ARIBAZ", font=fs, fill=(30, 30, 36, 90))

    img.convert("RGB").save(f"{OUT}/{slug}.jpg", quality=88, optimize=True, progressive=True)
    print("ok", slug)
