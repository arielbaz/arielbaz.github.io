---
title: "Bitchat : la messagerie qui marche même quand tout le réseau tombe"
slug: bitchat
date: 2026-11-10
category: Sécurité
tags: [messagerie, bluetooth, chiffrement, hors-ligne]
excerpt: "Zéro internet, zéro compte, zéro numéro. Tes messages passent de téléphone en téléphone par Bluetooth, et personne ne peut couper la conversation."
platforms: [ios, android, mac]
icon: lock
logo: bitchat
source: https://bitchat.free
sourceLabel: bitchat.free
featured: true
---

Stade bondé où le réseau sature, panne d'internet, coupure pendant une manifestation, avion ou voyage hors couverture : dans ces moments-là, WhatsApp et Signal deviennent muets.

**Bitchat** est la messagerie qui continue de fonctionner quand tout le reste s'éteint. Elle envoie tes messages directement de téléphone en téléphone, par Bluetooth. Pas d'internet, pas de forfait, pas de compte, pas de serveur central à éteindre.

## Ce que tu gagnes

- **Discuter sans internet** : chaque téléphone relaie les messages vers les appareils voisins, jusqu'à 7 sauts de distance.
- **Zéro compte, zéro numéro** : un pseudo, et c'est tout. Rien à créer, rien à valider.
- **Chiffré de bout en bout** : les messages privés passent par le protocole Noise — même les téléphones qui relaient ne peuvent pas les lire.
- **Un canal public et des messages privés** : le canal `#mesh` est ouvert à tous les appareils à portée, les MP sont réservés à ton destinataire.
- **Un mode panique** : trois taps sur le logo effacent tout, immédiatement.

## Pourquoi tout le monde en parle

L'idée est de **Doris Lima**, le développement est mené par **Jack Dorsey** (cofondateur de Twitter) avec Block, et tout est publié en open source. Bitchat a été adoptée massivement lors de coupures internet : manifestations à Madagascar, en Inde, zones sinistrées, réseaux saturés.

Au point que l'Inde a ordonné à GitHub de bloquer le dépôt du projet — la meilleure preuve que l'outil fonctionne.

Sur internet, elle complète le maillage avec le protocole **Nostr** : quand le Bluetooth ne suffit plus, les messages continuent par les relais Nostr, et des canaux géolocalisés permettent de discuter avec les gens de son quartier.

:::tip Le Pro-Tip ARIBAZ — les trois limites à connaître
**Le maillage n'existe que si les autres ont l'app.** Chaque saut Bluetooth couvre une dizaine de mètres : sans relais humains autour de toi, Bitchat ne parle qu'à ton voisinage direct. C'est une messagerie de foule, pas de salon.

**Sur iPhone, garde l'app ouverte.** iOS bride le Bluetooth en arrière-plan : l'application doit rester affichée pour émettre et recevoir. Côté Android, c'est beaucoup plus souple.

**Sois honnête avec toi-même : l'app est jeune.** Lancée en juillet 2025, elle n'a pas encore passé d'audit de sécurité indépendant complet, et ses créateurs le disent eux-mêmes. Pour les conversations sensibles du quotidien, Signal reste la référence. Bitchat, c'est l'assurance pour le jour où le réseau tombe.
:::

## Mise en place

1. Installe **Bitchat Mesh** depuis l'App Store (iPhone, macOS) ou le Play Store (Android). Sur Android, tu peux aussi prendre l'APK officiel sur GitHub — méfie-toi des imitations.
2. Active le Bluetooth, ouvre l'app et choisis un pseudo.
3. Rejoins le canal `#mesh` pour discuter avec tous les appareils à portée, ou envoie un message privé à quelqu'un à proximité.
4. Fais un vrai test avec un proche à côté de toi, avant d'en avoir besoin.

## Verdict

C'est une trousse de secours numérique : tu l'installes avant d'en avoir besoin, parce qu'au moment où internet tombe, il est trop tard pour la télécharger. Deux minutes aujourd'hui, une conversation possible demain.

**À télécharger :** [bitchat.free](https://bitchat.free)
