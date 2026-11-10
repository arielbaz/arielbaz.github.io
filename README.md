# ARIBAZ — arielbaz.github.io

Blog tech personnel : astuces concrètes, outils gratuits, vie privée et filtrage.
Site 100 % statique, sans dépendance, hébergé sur GitHub Pages.

**En ligne :** https://arielbaz.github.io

## Publier un nouvel article

### Sans rien installer (depuis GitHub, même sur téléphone)

1. Va sur **github.com/arielbaz/arielbaz.github.io** → dossier `content/posts/`
2. **Add file → Create new file**
3. Nomme le fichier comme l'adresse de l'article : `mon-sujet.md`
4. Copie le contenu de [`content/posts/_modele.md`](content/posts/_modele.md) et remplis-le
5. **Commit changes**

Le robot GitHub régénère le site tout seul en une minute environ : accueil, page
article, flux RSS, sitemap et image de partage. Rien d'autre à faire.

### En local (si Node est installé)

```bash
node tools/build.mjs        # régénère tout le site
git add -A && git commit -m "Nouvel article : ..." && git push
```

### Les champs de l'en-tête

| Champ | Rôle |
|---|---|
| `title` | titre affiché en gros |
| `slug` | nom du fichier et adresse : `/articles/mon-sujet.html` |
| `date` | `AAAA-MM-JJ` — sert au tri et à l'affichage |
| `category` | Productivité, Sécurité, Filtrage, Alternatives ou Mobile |
| `tags` | mots-clés (filtre la recherche) |
| `excerpt` | la phrase affichée sur la carte |
| `platforms` | `windows`, `mac`, `ios`, `android`, `chrome`, `web` |
| `logo` | nom d'un fichier de `assets/img/logos/` (facultatif : sinon un pictogramme est utilisé) |
| `icon` | pictogramme de secours : shield, lock, wifi, phone, eye, camera, text, mic, book… |
| `source` / `sourceLabel` | lien officiel affiché en bas d'article |
| `featured` | `true` pour épingler l'article en « dossier du moment » |

### Le visuel de l'article

Chaque article a une image dédiée dans `assets/img/cards/<slug>.jpg`. Sans image,
le site utilise automatiquement le visuel générique du site : l'article reste
parfaitement lisible, il n'a juste pas sa carte personnalisée.

Pour en générer une : ajoute l'accroche dans `tools/make-cards.py` (dictionnaire
`PUNCH`) puis lance `python3 tools/make-cards.py`.

## Structure

```
content/posts/   articles en markdown (source unique)
tools/build.mjs  générateur statique (Node, zéro dépendance)
assets/          CSS, JS, images
articles/        pages générées (ne pas éditer à la main)
index.html       accueil généré
feed.xml         flux RSS
```

## Visuels d'articles

Chaque article a une image dédiée (1600x900) dans `assets/img/cards/<slug>.jpg`,
utilisée en tête d'article et comme image de partage (og:image).

Pour les régénérer après avoir changé une accroche :

```bash
python3 tools/make-cards.py   # nécessite Pillow
```

Les accroches et les couleurs par catégorie sont dans `PUNCH` et `PALETTE`,
en haut du script.
