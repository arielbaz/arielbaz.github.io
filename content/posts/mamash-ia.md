---
title: "Mamash IA : une IA qui cite la Torah depuis les textes, pas de mémoire"
slug: mamash-ia
date: 2026-11-11
category: Religion
tags: [torah, talmud, halakha, claude, mcp, sefaria, gratuit]
excerpt: "Une question de Torah posée à une IA, et une réponse sourcée, lue sur Sefaria, avec le lien pour vérifier. Gratuit, sans compte, sur le site ou dans Claude."
platforms: [web]
icon: book
source: https://mamash-ia.com
sourceLabel: mamash-ia.com
---

Poser une question de Torah à une IA, c'est pratique. C'est aussi risqué : les assistants répondent le plus souvent **de mémoire**, avec la même assurance qu'ils aient raison ou non. Une référence approximative, une citation recomposée, parfois inventée, et rien pour te dire ce qu'ils n'ont pas réellement ouvert.

**Mamash IA** part de ce constat. Le principe tient en une phrase, écrite sur le site : *ce qui n'a pas été lu n'est pas cité, et chaque citation vient avec le lien pour la vérifier.*

Le nom, **ממש** (« vraiment »), est présenté sur le site comme les initiales du Rabbi, Menahem Mendel Schneerson. C'est un projet personnel de Jonathan Bensaid, gratuit, sans compte et sans collecte de données.

## Comment ça marche

La question déclenche une **lecture** : le texte est ouvert dans l'édition **Sefaria**, cité tel qu'il est écrit, avec sa référence exacte, et relié à ses commentateurs. Quand une source manque, la réponse le dit.

D'après le site, la bibliothèque lue en direct couvre environ **6 600 titres** (Tanakh, Michna, Talmud, Midrach, Rambam, Choulhan Aroukh, responsa, hassidout et leurs commentateurs). La recherche plein texte du fonds **HebrewBooks** ajoute environ **50 000 seforim**, avec le passage, sa page et le fac-similé à ouvrir.

Il y a deux façons de s'en servir :

- **Sur le site**, sans rien installer : tu écris ta question en français, la réponse est rédigée à partir des textes lus sur Sefaria.
- **Dans Claude**, avec un connecteur (un serveur MCP) qui donne à l'assistant une méthode d'étude et seize outils en lecture seule.

## Ce que le connecteur ajoute

- **La méthode** : chargée avant toute réponse religieuse. Lire, citer depuis la lecture, signaler les désaccords (mahloket), ne jamais fabriquer de référence.
- **La havrouta** : Claude te pose des questions au lieu de répondre. Une kouchia à la fois, Rachi à défendre contre Tossafot, récapitulatif des chidouchim.
- **Le guide de paracha** : aliya par aliya, trois questions du texte départagées par deux commentateurs, l'écho de la haftara, des questions pour la table du Chabbat.
- **Le daf en page de Vilna** : la Guemara au centre, Rachi et Tossafot dépliables, la traduction au clic, ouverte dans la conversation. Sans référence, c'est le daf yomi.
- **Le quotidien** : zmanim et horaires de Chabbat, dates hébraïques, guematria, nikoud, et une fiche source prête à coller dans WhatsApp.

Trois modes s'ajustent à ton niveau : **débutant** (tout en français, chaque mot hébreu traduit), **classique** (le mode par défaut) et **avancé** (source en langue originale, richonim, nafka mina). Le registre change, la discipline des sources jamais.

:::tip Le Pro-Tip ARIBAZ — dis ton niveau dès la première phrase
« Je débute, je ne lis pas l'hébreu » ou « mode avancé » : le site comme Claude adaptent le ton et la densité. Et dans tous les cas, **clique le lien de la source** avant de t'appuyer sur une réponse. C'est justement ce que l'outil rend possible, autant s'en servir.
:::

## Installer dans Claude (2 minutes)

Dans **claude.ai**, ouvre *Settings → Connectors → Add custom connector*, colle l'adresse suivante, nomme-le « Torah » et valide :

```
https://torah-mcp.com/mcp
```

Dans **Claude Code**, depuis un terminal (pas dans la conversation) :

```
claude mcp add --transport http torah https://torah-mcp.com/mcp
```

Vérifie ensuite avec `claude mcp list` : la ligne doit se terminer par « Connected ». Le `https://` est indispensable, sans lui la commande est acceptée mais la connexion échoue. Le code est libre (licence MIT), tu peux aussi héberger ta propre instance.

## Les limites, dites franchement

- **Un outil d'étude, pas un décisionnaire.** Pour une question de halakha pratique qui engage ta vie quotidienne, la réponse sourcée aide à comprendre, mais c'est à ton rav de trancher. C'est mon avis, pas une phrase du site.
- **La page « Poser une question » envoie ton texte à Anthropic (Claude)** pour rédiger la réponse. D'après la page confidentialité, la réponse n'est pas conservée, mais un **journal statistique privé** garde le texte des questions, sans adresse IP ni identifiant. Ces questions pourront être reprises, anonymisées, dans un recueil ou un ouvrage. N'y écris pas d'informations personnelles.
- **Le site utilise Google Analytics 4** pour mesurer la fréquentation. Le connecteur MCP lui-même n'envoie rien à Google.
- **Limite de débit** côté connecteur : 60 requêtes par minute et par adresse IP.
- **Je n'ai pas testé chaque réponse.** Cet article décrit ce que le site annonce. Teste avec une question dont tu connais déjà la source avant de t'y fier.

## Verdict

L'idée est la bonne : une IA qui **ouvre le livre** au lieu de le réciter, et qui te donne le lien pour contrôler. Pour étudier une sougya, préparer la paracha ou comprendre un terme sans bluffer, c'est un vrai gain, gratuit et sans compte. Pour trancher une question pratique, ça reste un point de départ vers ton rav, pas un remplaçant.

**À essayer :** [mamash-ia.com](https://mamash-ia.com)
