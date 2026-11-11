---
title: "Plume : un cours de Guemara transformé en Word, sans passer par le cloud"
slug: plume
date: 2026-11-11
category: Productivité
tags: [transcription, hébreu, talmud, open source, whisper, word]
excerpt: "Un shiur d'une heure, un MP3, et un document Word propre en hébreu RTL. Plume transcrit en local, suit l'audio et apprend de tes corrections."
logo: plume
platforms: [mac, windows]
icon: book
source: https://github.com/arielbaz/plume
sourceLabel: github.com/arielbaz/plume
---

Écouter un shiur, c'est bien. Retrouver la sugya trois semaines plus tard, dans un fichier audio d'une heure, c'est autre chose. Les applications de transcription existent, mais elles envoient l'enregistrement sur un serveur, facturent à la minute, ou refusent tout simplement l'hébreu et l'araméen du Talmud.

**Plume** part d'un principe simple : le fichier audio ne quitte pas l'ordinateur. On glisse un MP3, un M4A ou un WAV, et on récupère un **document Word mis en page**, avec les paragraphes hébraïques en lecture de droite à gauche.

C'est un projet open source, gratuit, construit sur **Whisper** (le moteur d'OpenAI) qui tourne en local via whisper.cpp, avec une interface **Tauri/Rust**.

## Ce qu'il fait vraiment

- **Import de fichiers** : MP3, M4A/AAC, WAV, FLAC, OGG, AIFF, MP4, MOV… glisser-déposer ou sélection multiple.
- **Transcription locale** : modèles Whisper de Tiny à Large v3 Turbo. Sur un Mac Apple Silicon, le GPU Metal est utilisé ; sur Windows, le CPU.
- **Word propre** : titre, date, source, durée, langue, modèle, paragraphes justifiés, pied de page numéroté, propriétés du document.
- **Hébreu RTL** : les paragraphes en hébreu sont détectés et composés de droite à gauche ; le français reste LTR.
- **Lecteur synchronisé** : lecture/pause, −10 s, +10 s, curseur. Le paragraphe en cours est surligné et le texte suit l'audio. Cliquer un paragraphe déplace la lecture.
- **Mots incertains** : les mots transcrits avec peu de confiance sont soulignés en rouge. Un clic propose une correction ; acceptée, elle est apprise pour les prochaines transcriptions.
- **Sujet du cours** : le nom du fichier est analysé (`baba-kama-42a.mp3`), le traité et la page sont détectés, et les termes probables sont préparés.
- **Lexique** : 291 termes talmudiques/halakha curatés avec leurs champs lexicaux, plus une banque de **8 980 mots** (Strong pour l'hébreu biblique, Jastrow pour l'araméen talmudique) consultable dans l'application.

## Le détail qui change tout pour un cours de Guemara

Whisper, seul, ne sait pas qu'on étudie Baba Kama plutôt que Berakhot. Plume lui donne un contexte : traité, page, notions liées, glossaire personnel, termes techniques, corrections apprises.

Trois choses font la différence :

1. **Le bon modèle** : Large v3 Turbo (574 Mo) est nettement plus fiable que Small sur l'hébreu. Le téléchargement se fait une fois, ensuite tout est hors ligne.
2. **Le vocabulaire** : les noms de Rabbanim, les expressions araméennes (`איבעיא להו`, `תא שמע`, `מאי טעמא`…), les titres de sefarim. Les champs lexicaux du lexique proposent automatiquement les termes voisins d'un traité.
3. **La correction** : quand un mot est souligné, on écoute, on accepte la suggestion, et Plume la réapplique aux cours suivants. C'est un apprentissage réel, pas un réglage oublié.

:::tip Le Pro-Tip ARIBAZ — nomme tes fichiers comme des références
`baba-kama-42a.mp3`, `chabbat-15b.m4a`, `yoreh-deah-kashrout.mp3` : Plume reconnaît le traité, la page ou le thème, et prépare les termes correspondants avant même la transcription. Deux secondes de rigueur au nommage, des heures de relecture en moins.
:::

## Les limites, dites franchement

- **Une langue principale par transcription.** Un cours en français avec des citations hébraïques se transcrit bien en choisissant « Français » ; un cours en hébreu avec des explications en français se transcrit en « Hébreu », avec parfois des termes français rendus en caractères hébraïques. La détection automatique par segment est le prochain chantier.
- **L'araméen du Talmud reste difficile.** Il n'existe pas de modèle Whisper araméen. Le lexique, le contexte et un futur modèle affiné aident, mais il faut relire.
- **Pas de séparation des intervenants** (diarisation) pour l'instant.
- **Le lecteur audio fonctionne pendant la session** ; l'historique persistant des transcriptions n'est pas encore là.

Sur de vrais enregistrements, la qualité dépend beaucoup du micro, du bruit de fond et de l'élocution. Un test de 5 à 10 minutes reste la meilleure façon de régler glossaire et modèle.

## Télécharger

- **macOS (Apple Silicon)** : [Plume-0.2.0-arm64.dmg](https://github.com/arielbaz/plume/releases/download/v0.2.0/Plume-0.2.0-arm64.dmg) — ouvrir le DMG, glisser Plume dans `Applications`.
- **Windows** : [installateur .exe](https://github.com/arielbaz/plume/releases/download/v0.2.0/Plume_0.2.0_x64-setup.exe) (recommandé) ou [paquet .msi](https://github.com/arielbaz/plume/releases/download/v0.2.0/Plume_0.2.0_x64_en-US.msi).
- **Toutes les versions** : [github.com/arielbaz/plume/releases](https://github.com/arielbaz/plume/releases).
- **Code source** : [github.com/arielbaz/plume](https://github.com/arielbaz/plume) — licence MIT.

Les binaires ne sont pas signés : sous macOS, clic droit → **Ouvrir** au premier lancement ; sous Windows, SmartScreen peut demander de confirmer (« Informations complémentaires » → « Exécuter quand même »).

L'application n'est pas notariée par Apple : au premier lancement, clic droit sur l'icône → **Ouvrir**. Le modèle est téléchargé depuis l'application, une seule fois.

## Verdict

Plume ne remplace pas une relecture attentive — rien ne remplace une relecture attentive. Mais il transforme un enregistrement brut en document de travail : un Word hébraïque lisible, un lecteur pour vérifier, des mots incertains signalés, et un vocabulaire qui s'améliore à chaque cours.

Pour un étudiant en yéchiva, un rav qui prépare ses chiourim, ou quiconque accumule des heures de Guemara sans jamais les relire : c'est le chaînon manquant entre l'audio et la page.
