#!/usr/bin/env python3
"""Génère les schémas explicatifs insérés dans chaque article.

Sortie : assets/img/articles/<slug>.jpg (1600x900).
Usage  : python3 tools/make-article-figures.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "articles")
os.makedirs(OUT, exist_ok=True)

W, H = 1600, 900
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

PALETTE = {
    "Productivité": ((232, 241, 255), (185, 212, 255), (11, 100, 199)),
    "Sécurité": ((236, 235, 255), (195, 192, 255), (74, 71, 196)),
    "Filtrage": ((230, 249, 236), (174, 232, 196), (20, 133, 74)),
    "Alternatives": ((255, 242, 226), (255, 208, 161), (184, 86, 10)),
    "Mobile": ((248, 233, 255), (226, 193, 251), (140, 53, 192)),
}

INK = (24, 24, 28)
SOFT = (92, 92, 99)
FAINT = (132, 132, 140)

ARTICLES = {
    "ublock-origin": {
        "cat": "Sécurité",
        "headline": "La pub bloquée\navant l’affichage.",
        "summary": "uBlock Origin coupe les requêtes publicitaires et les traqueurs avant qu’ils n’encombrent la page.",
        "steps": [
            ("01", "Tu ouvres un site", "Le navigateur demande les pubs, scripts et images de suivi."),
            ("02", "Les listes filtrent", "Les domaines connus comme publicitaires sont bloqués."),
            ("03", "La page reste propre", "Moins de pub, moins de traqueurs, plus de vitesse."),
        ],
        "takeaway": "Efficace sur Firefox ; dans Chrome, Manifest V3 limite le blocage.",
    },
    "brave": {
        "cat": "Alternatives",
        "headline": "Un navigateur qui\nbloque avant d’afficher.",
        "summary": "Brave intègre un bouclier anti-pub et anti-traqueur, sans extension à installer.",
        "steps": [
            ("01", "Tu navigues", "Tu ouvres un site comme dans n’importe quel navigateur."),
            ("02", "Le bouclier agit", "Pubs, traqueurs et scripts sont arrêtés à la source."),
            ("03", "YouTube en fond", "La lecture peut continuer même écran éteint."),
        ],
        "takeaway": "Un Chromium sans les pubs : le compromis le plus simple.",
    },
    "signal": {
        "cat": "Sécurité",
        "headline": "Le serveur ne peut\npas lire le message.",
        "summary": "Signal chiffre les messages de bout en bout : seuls les téléphones concernés peuvent les déchiffrer.",
        "steps": [
            ("01", "Tu écris", "Le message est chiffré directement sur ton appareil."),
            ("02", "Signal relaie", "Le serveur transporte un contenu qu’il ne peut pas ouvrir."),
            ("03", "Ton contact lit", "Seul son téléphone possède la clé de déchiffrement."),
        ],
        "takeaway": "Gratuit, open source, et le chiffrement est activé par défaut.",
    },
    "localsend": {
        "cat": "Alternatives",
        "headline": "Un transfert direct,\nsans cloud.",
        "summary": "LocalSend envoie tes fichiers d’un appareil à l’autre sur le même réseau Wi-Fi.",
        "steps": [
            ("01", "Même réseau", "Les deux appareils sont connectés au même Wi-Fi."),
            ("02", "Tu choisis", "Fichier, dossier, texte ou presse-papiers."),
            ("03", "Transfert direct", "Aucun serveur, aucun compte, aucun détour."),
        ],
        "takeaway": "Rapide chez soi ; hors du réseau local, il faut une autre solution.",
    },
    "sharex": {
        "cat": "Productivité",
        "headline": "Capturer, annoter,\npartager.",
        "summary": "ShareX enchaîne capture d’écran, retouche, GIF, OCR et envoi dans un seul outil.",
        "steps": [
            ("01", "Capture", "Écran, fenêtre, zone ou page qui défile."),
            ("02", "Retouche", "Flèches, texte, flou, recadrage : tout est intégré."),
            ("03", "Export", "Fichier, presse-papiers, dossier ou lien de partage."),
        ],
        "takeaway": "Windows uniquement, gratuit et open source.",
    },
    "onlyoffice": {
        "cat": "Productivité",
        "headline": "Word, Excel, PowerPoint\nsans abonnement.",
        "summary": "OnlyOffice ouvre et enregistre les formats Office en gardant la mise en page.",
        "steps": [
            ("01", "Tu ouvres", "Un .docx, .xlsx ou .pptx existant."),
            ("02", "Tu modifies", "Les styles, formules et tableaux restent en place."),
            ("03", "Tu enregistres", "Le fichier reste compatible avec Microsoft Office."),
        ],
        "takeaway": "La compatibilité est le vrai argument, pas seulement le prix.",
    },
    "handy": {
        "cat": "Productivité",
        "headline": "Ta voix devient du texte,\nen local.",
        "summary": "Handy transcrit la dictée sur ta machine, sans envoyer l’audio à un serveur.",
        "steps": [
            ("01", "Tu parles", "Un raccourci lance l’écoute, sans changer d’application."),
            ("02", "L’IA transcrit", "Le modèle tourne directement sur ton ordinateur."),
            ("03", "Le texte s’insère", "Il apparaît dans le champ où tu écrivais."),
        ],
        "takeaway": "La qualité dépend du modèle local et de la puissance de la machine.",
    },
    "notebooklm": {
        "cat": "Productivité",
        "headline": "Un PDF devient\nun podcast.",
        "summary": "NotebookLM résume tes documents et génère une conversation audio à deux voix.",
        "steps": [
            ("01", "Tu déposes", "PDF, notes, liens ou texte dans le carnet."),
            ("02", "L’IA analyse", "Elle relie les passages importants de tes sources."),
            ("03", "Tu écoutes", "Un podcast pour réviser ailleurs, hors écran."),
        ],
        "takeaway": "À vérifier : l’IA peut simplifier ou oublier une nuance.",
    },
    "owc-copy-that": {
        "cat": "Mobile",
        "headline": "Tes photos quittent\niCloud.",
        "summary": "Copy That copie la galerie iPhone vers un disque USB, sans passer par le cloud.",
        "steps": [
            ("01", "Branche", "Le disque ou la clé USB se connecte à l’iPhone."),
            ("02", "Copie", "Photos et vidéos, par album ou en vrac."),
            ("03", "Vérifie", "Les fichiers sont bien sur ton support, chez toi."),
        ],
        "takeaway": "Une sauvegarde locale ne protège pas d’un vol ou d’un incendie.",
    },
    "family-link": {
        "cat": "Filtrage",
        "headline": "Un Android sous\nsurveillance douce.",
        "summary": "Family Link règle le temps d’écran, valide les installations et localise l’appareil.",
        "steps": [
            ("01", "Compte enfant", "Un profil Google dédié est créé sur l’appareil."),
            ("02", "Règles", "Temps d’écran, applications et filtres sont choisis."),
            ("03", "Suivi", "Localisation et demandes d’accès arrivent au parent."),
        ],
        "takeaway": "À installer avant de donner le téléphone, pas après.",
    },
    "dns-cloudflare": {
        "cat": "Filtrage",
        "headline": "Toute la maison\nfiltrée en 2 minutes.",
        "summary": "Le DNS 1.1.1.3 bloque les domaines malveillants et adultes pour tous les appareils.",
        "steps": [
            ("01", "Changer le DNS", "Sur la box, le routeur ou chaque appareil."),
            ("02", "1.1.1.3", "Le filtre s’applique à chaque requête DNS."),
            ("03", "Profiter", "Tous les appareils du réseau suivent la même règle."),
        ],
        "takeaway": "Efficace, mais facile à contourner avec un autre DNS.",
    },
    "appels-wifi": {
        "cat": "Mobile",
        "headline": "Appeler quand le\nréseau mobile manque.",
        "summary": "La VoWiFi fait passer les appels par le Wi-Fi, avec ton numéro habituel.",
        "steps": [
            ("01", "Wi-Fi actif", "Une connexion internet stable suffit."),
            ("02", "Appel", "Le téléphone passe par la box, pas par l’antenne."),
            ("03", "Ton numéro", "Le correspondant voit le même numéro qu’avant."),
        ],
        "takeaway": "Vérifie que l’opérateur et le forfait autorisent la VoWiFi.",
    },
    "wizmage": {
        "cat": "Filtrage",
        "headline": "Les images arrivent\nfloutées.",
        "summary": "Wizmage masque toutes les images d’une page jusqu’à ce que tu cliques.",
        "steps": [
            ("01", "Tu navigues", "Les images sont remplacées par un flou uniforme."),
            ("02", "Tu choisis", "Un clic révèle uniquement celle qui t’intéresse."),
            ("03", "Tu continues", "Le reste de la page reste propre et lisible."),
        ],
        "takeaway": "Utile au bureau ou en famille, pas un contrôle parental complet.",
    },
    "nsfw-filter": {
        "cat": "Filtrage",
        "headline": "L’IA filtre sans\nenvoyer l’image.",
        "summary": "NSFW Filter analyse les images localement et masque celles jugées inappropriées.",
        "steps": [
            ("01", "Page chargée", "Les images de la page sont examinées."),
            ("02", "Analyse locale", "Le modèle tourne dans le navigateur, pas sur un serveur."),
            ("03", "Masquage", "Le contenu sensible est caché automatiquement."),
        ],
        "takeaway": "Aucun filtre n’est parfait : garde un adulte dans la boucle.",
    },
    "have-i-been-pwned": {
        "cat": "Sécurité",
        "headline": "Ton adresse a-t-elle\nfuité ?",
        "summary": "HIBP compare ton adresse aux bases de fuites connues, sans demander ton mot de passe.",
        "steps": [
            ("01", "Saisis l’e-mail", "Une adresse suffit, aucun mot de passe."),
            ("02", "Comparaison", "Les fuites connues sont vérifiées dans la base."),
            ("03", "Résultat", "Change les mots de passe des services concernés."),
        ],
        "takeaway": "Active la double authentification, surtout sur la boîte mail.",
    },
    "presse-papiers": {
        "cat": "Productivité",
        "headline": "Copier plusieurs choses,\nsans écraser.",
        "summary": "L’historique du presse-papiers garde tes dernières copies et te laisse choisir.",
        "steps": [
            ("01", "Copie", "Ctrl+C ou Cmd+C comme d’habitude."),
            ("02", "Rappelle", "Win+V sur Windows, un outil tiers sur Mac."),
            ("03", "Colle", "Choisis l’élément dans la liste, sans recommencer."),
        ],
        "takeaway": "Sur Mac, cette fonction n’est pas native : il faut une app.",
    },
    "esim": {
        "cat": "Mobile",
        "headline": "Une ligne, sans\ncarte à découper.",
        "summary": "L’eSIM est un profil numérique installé par QR code ou directement par l’opérateur.",
        "steps": [
            ("01", "Commande", "Un forfait eSIM chez ton opérateur."),
            ("02", "Scanne", "Le QR code ajoute le profil au téléphone."),
            ("03", "Active", "La ligne est prête, sans plastique à insérer."),
        ],
        "takeaway": "Garde ta ligne principale et ajoute un forfait local en voyage.",
    },
    "bitchat": {
        "cat": "Sécurité",
        "headline": "Le message passe de\ntéléphone en téléphone.",
        "summary": "Bitchat crée un maillage Bluetooth : aucun serveur, aucun internet, aucun compte.",
        "steps": [
            ("01", "Tu écris", "Le message part en Bluetooth vers les appareils proches."),
            ("02", "Le maillage relaie", "Les téléphones voisins le transmettent de proche en proche."),
            ("03", "Il arrive", "Le destinataire le reçoit, chiffré de bout en bout."),
        ],
        "takeaway": "Il faut d’autres utilisateurs à portée : c’est une messagerie de foule.",
    },
}


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def gradient(w, h, c1, c2):
    small = Image.new("RGB", (160, 90))
    px = small.load()
    for y in range(90):
        for x in range(160):
            t = x / 159 * 0.58 + y / 89 * 0.42
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return small.resize((w, h), Image.BICUBIC).convert("RGBA")


def wrap(draw, text, f, maxw):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            test = (cur + " " + word).strip()
            if draw.textlength(test, font=f) <= maxw:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def fit(draw, text, maxw, maxlines, start, minimum, bold=True):
    size = start
    while size >= minimum:
        f = font(size, bold)
        lines = wrap(draw, text, f, maxw)
        if len(lines) <= maxlines:
            return f, lines
        size -= 2
    f = font(minimum, bold)
    return f, wrap(draw, text, f, maxw)[:maxlines]


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_arrow(draw, x, y1, y2, color):
    draw.line([(x, y1), (x, y2)], fill=color, width=4)
    draw.line([(x - 8, y2 - 12), (x, y2), (x + 8, y2 - 12)], fill=color, width=4, joint="curve")


def make(entry, slug):
    c1, c2, accent = PALETTE[entry["cat"]]
    img = gradient(W, H, c1, c2)

    # halo
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-300, -360, 900, 680], fill=(255, 255, 255, 150))
    gd.ellipse([980, 260, 1900, 1080], fill=(255, 255, 255, 80))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(120)))

    d = ImageDraw.Draw(img)

    # panneau principal + ombre
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([72, 84, 1528, 840], radius=52, fill=(30, 30, 55, 55))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(img)
    rounded(d, [72, 72, 1528, 828], 52, (255, 255, 255, 240), (255, 255, 255, 120), 2)

    # en-tête
    d.ellipse([128, 128, 142, 142], fill=accent)
    fc = font(20, True)
    d.text((154, 121), entry["cat"].upper(), font=fc, fill=accent)
    ftag = font(17, True)
    tag = "ARIBAZ  ·  SCHÉMA"
    d.text((1420 - d.textlength(tag, font=ftag), 124), tag, font=ftag, fill=FAINT)

    # colonne gauche
    fh, lines = fit(d, entry["headline"], 650, 2, 64, 48, True)
    y = 184
    for line in lines:
        d.text((128, y), line, font=fh, fill=INK)
        y += int(fh.size * 1.16)

    fs, slines = fit(d, entry["summary"], 650, 3, 25, 20, False)
    y += 10
    for line in slines:
        d.text((128, y), line, font=fs, fill=SOFT)
        y += int(fs.size * 1.42)

    # encadré à retenir
    rounded(d, [120, 628, 800, 756], 24, (*c1, 120), (255, 255, 255, 110), 1)
    fl = font(15, True)
    d.text((148, 651), "À RETENIR", font=fl, fill=accent)
    ft, tlines = fit(d, entry["takeaway"], 616, 2, 23, 18, True)
    ty = 682
    for line in tlines:
        d.text((148, ty), line, font=ft, fill=INK)
        ty += int(ft.size * 1.28)

    # séparateur
    d.line([(842, 150), (842, 758)], fill=(30, 30, 50, 18), width=2)

    # colonne droite : 3 étapes
    x0, x1 = 900, 1472
    tops = [150, 352, 554]
    for i, (num, title, detail) in enumerate(entry["steps"]):
        top = tops[i]
        rounded(d, [x0, top, x1, top + 150], 24, (255, 255, 255, 255), (30, 30, 50, 22), 2)
        d.ellipse([x0 + 28, top + 28, x0 + 76, top + 76], fill=accent)
        fn = font(20, True)
        nw = d.textlength(num, font=fn)
        d.text((x0 + 52 - nw / 2, top + 37), num, font=fn, fill=(255, 255, 255))
        fst = font(27, True)
        d.text((x0 + 98, top + 24), title, font=fst, fill=INK)
        fd, dlines = fit(d, detail, 438, 2, 21, 17, False)
        dy = top + 71
        for line in dlines:
            d.text((x0 + 98, dy), line, font=fd, fill=SOFT)
            dy += int(fd.size * 1.34)
        if i < 2:
            draw_arrow(d, (x0 + x1) // 2, top + 150, tops[i + 1] - 2, accent)

    # signature
    fsig = font(23, True)
    sig = "ARIBAZ"
    d.text((1472 - d.textlength(sig, font=fsig), 770), sig, font=fsig, fill=(30, 30, 36, 110))

    img.convert("RGB").save(os.path.join(OUT, slug + ".jpg"), quality=90, optimize=True, progressive=True)
    print("ok", slug)




# ---------------------------------------------------------------------------
# Variante mobile : même contenu, mise en page verticale et texte plus gros.
# ---------------------------------------------------------------------------
MW, MH = 900, 1350


def make_mobile(entry, slug):
    c1, c2, accent = PALETTE[entry["cat"]]
    img = gradient(MW, MH, c1, c2)

    glow = Image.new("RGBA", (MW, MH), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-260, -240, 620, 540], fill=(255, 255, 255, 150))
    gd.ellipse([520, 820, 1200, 1500], fill=(255, 255, 255, 85))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(100)))

    d = ImageDraw.Draw(img)
    shadow = Image.new("RGBA", (MW, MH), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([36, 46, 864, 1320], radius=46, fill=(30, 30, 55, 60))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(24)))
    d = ImageDraw.Draw(img)
    rounded(d, [36, 36, 864, 1314], 46, (255, 255, 255, 242), (255, 255, 255, 120), 2)

    d.ellipse([70, 78, 84, 92], fill=accent)
    fc = font(22, True)
    d.text((96, 70), entry["cat"].upper(), font=fc, fill=accent)
    ftag = font(16, True)
    d.text((794 - d.textlength("ARIBAZ · SCHÉMA", font=ftag), 74), "ARIBAZ · SCHÉMA", font=ftag, fill=FAINT)

    fh, lines = fit(d, entry["headline"], 760, 3, 58, 42, True)
    y = 120
    for line in lines:
        d.text((70, y), line, font=fh, fill=INK)
        y += int(fh.size * 1.14)

    fs, slines = fit(d, entry["summary"], 760, 3, 26, 20, False)
    y += 10
    for line in slines:
        d.text((70, y), line, font=fs, fill=SOFT)
        y += int(fs.size * 1.4)

    x0, x1 = 70, 830
    tops = [470, 680, 890]
    for i, (num, title, detail) in enumerate(entry["steps"]):
        top = tops[i]
        rounded(d, [x0, top, x1, top + 190], 24, (255, 255, 255, 255), (30, 30, 50, 24), 2)
        d.ellipse([x0 + 24, top + 24, x0 + 80, top + 80], fill=accent)
        fn = font(22, True)
        nw = d.textlength(num, font=fn)
        d.text((x0 + 52 - nw / 2, top + 36), num, font=fn, fill=(255, 255, 255))
        fst = font(35, True)
        d.text((x0 + 96, top + 24), title, font=fst, fill=INK)
        fd, dlines = fit(d, detail, 636, 2, 25, 19, False)
        dy = top + 82
        for line in dlines:
            d.text((x0 + 96, dy), line, font=fd, fill=SOFT)
            dy += int(fd.size * 1.36)

    rounded(d, [70, 1110, 830, 1238], 24, (*c1, 120), (255, 255, 255, 110), 1)
    fl = font(16, True)
    d.text((96, 1134), "À RETENIR", font=fl, fill=accent)
    ft, tlines = fit(d, entry["takeaway"], 676, 2, 24, 18, True)
    ty = 1166
    for line in tlines:
        d.text((96, ty), line, font=ft, fill=INK)
        ty += int(ft.size * 1.25)

    fsig = font(20, True)
    sig = "ARIBAZ"
    d.text((794 - d.textlength(sig, font=fsig), 1268), sig, font=fsig, fill=(30, 30, 36, 110))

    img.convert("RGB").save(os.path.join(OUT, slug + "-mobile.jpg"), quality=90, optimize=True, progressive=True)
    print("ok mobile", slug)


if __name__ == "__main__":
    for slug, entry in ARTICLES.items():
        make(entry, slug)
        make_mobile(entry, slug)
