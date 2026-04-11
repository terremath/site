# 🎵 Sound Design — Marcher sur l'eau

Fichier de référence pour le montage DaVinci Resolve. Pas de voix off pour cette v1.
Objectif : la vidéo doit rester intéressante **avec et sans son**.

---

## 🎼 Piste musicale de fond (toute la vidéo)

**Style** : Ambient cinématique contemplatif, piano + nappes orchestrales minimales.
**Mots-clés de recherche** : `contemplative piano`, `cinematic minimal`, `orchestral ambient`, `thoughtful score`
**Sources gratuites** : Pixabay Music, Freesound, YouTube Audio Library, Uppbeat
**Volume** : -18 dB LUFS en fond, duckée à -24 dB pendant les SFX clés

**Progression émotionnelle suggérée** :
- Scènes 01–06 : nappe calme, piano doux (contemplation, construction)
- Scènes 07–08 : montée dramatique (tension, impossibilité)
- Scènes 09–11 : retour apaisé (résolution, réflexion)
- Scènes 12–14 : solennel, presque sacré (Goethe + CTA)

**Astuce ducking** : dans DaVinci, applique un compresseur side-chain sur la piste musique,
déclenché par la piste SFX. Ratio 4:1, threshold -20dB, release 500ms.
→ la musique baisse automatiquement quand un SFX important joue.

---

## 🔊 Palette de SFX par type

| Type | Usage | Mots-clés recherche |
|---|---|---|
| **Whoosh doux** | Apparition de texte/titre | `whoosh soft`, `ui transition` |
| **Impact grave** | Flèches de force, verdicts rouges | `thud deep`, `cinematic hit` |
| **Splash eau** | Onde, pied qui frappe l'eau | `water splash small`, `water drop` |
| **Ambiance eau** | Fond des scènes avec eau | `water ambient`, `ocean calm` |
| **Cristallin / chime** | Équations clés en or, révélations | `magic chime`, `bell soft`, `sparkle` |
| **Drone basse** | Tension, axiome, impossibilité | `deep drone`, `dark ambient pad` |
| **Ticking léger** | Rythme des pas du basilic | `water tap`, `light tick` |

---

## 📋 Cue sheet par scène

### Scene01_Titre (~6s)
- `0.0s` — **whoosh doux** (apparition du titre)
- `1.5s` — **ambiance eau calme** (fond, boucle courte)
- `3.5s` — **chime cristallin** (apparition "TerreMathématiques")

### Scene02_Probleme (~6s)
- `0.0s` — **drone mystérieux** léger (question qui monte)
- `0.5s / 1.1s / 1.7s / 2.3s` — 4x **tick doux** (chaque ligne de la question)
- `3.2s` — **chime** (apparition du "?")

### Scene03_BilanForces (~12s)
- `0.0s` — **ambiance eau** (démarrage)
- `3.0s` — **impact grave rouge** (flèche mg)
- `4.5s` — **petit splash / reverse** (flèche F_eau)
- `7.0s` — **sub drop grave** (constat F_eau ≪ mg)
- `8.5s` — **big splash + gloup** (silhouette qui coule)
- `10.0s` — **whoosh** (apparition "Il coule")

### Scene04_OndeImpact (~8s)
- `0.0s` — **ambiance eau calme**
- `2.0s` — **swoosh descendant** (pied qui tombe)
- `2.5s` — **🌟 SPLASH MAJEUR** (impact, moment clé de la scène)
- `4.5s` — **chime** (apparition de F ~ ρAv²)

### Scene05_DoOuVientF (~14s) ⭐ NOUVELLE SCÈNE
- `0.0s` — **drone calme mathématique**
- `1.5s` — **tick** (étape 1, volume balayé)
- `4.5s` — **tick** (étape 2, masse)
- `7.5s` — **tick** (étape 3, quantité de mouvement)
- `10.0s` — **chime cristallin + sub grave** (équation finale F = ρAv² encadrée)
- `12.0s` — **chime doux** (insight "Pourquoi v²")

### Scene06_PourquoiMoyenne (~12s)
- `0.0s` — **continuation drone**
- `2.0s–5.0s` — 5x **tick water tap** (pics de force, un par pas)
- `6.0s` — **whoosh** (apparition ligne moyenne)
- `9.0s` — **chime + sub** (apparition de l'intégrale)

### Scene07_Condition (~10s)
- `0.0s` — **tick x3** (les 3 faits)
- `5.0s` — **sub drop** (apparition de "Donc")
- `7.0s` — **🌟 CHIME MAJEUR + sub** (équation finale ρAv²f ≥ mg encadrée)

### Scene08_VitesseImpossible (~12s)
- `0.0s` — **montée tension** (drone qui monte)
- `3.0s` — **tick x3** (les valeurs numériques)
- `6.5s` — **whoosh flash** (flash blanc)
- `6.8s` — **🌟 IMPACT CINÉMATIQUE** (80-110 km/h apparaît)
- `8.5s` — **sub grave descendant** ("×2 Bolt")
- `10.0s` — **verdict drop** ("Impossible")

### Scene09_Gravite (~12s)
- `0.0s` — **retour calme**, drone léger
- `2.0s` — **chime** (formule u_min ∝ √g)
- `4.0s` — **swoosh montant** (dessin de la courbe)
- `7.0s / 7.5s / 8.0s` — 3x **tick** (points Terre, Lune, Titan)
- `10.0s` — **chime d'espoir** (conclusion "Sur la Lune ou Titan...")

### Scene10_Basilic (~10s)
- `0.0s` — **ambiance eau vive**
- `2.0s–6.0s` — **boucle de petits taps rythmés** (basilic qui court — 8 splashs)
- `7.0s` — **chime check ✓** (équation validée)

### Scene11_ForceDivine (~14s)
- `0.0s` — **drone mystérieux éthéré**
- `2.0s` — **shimmer céleste** (glow sur F_divin)
- `4.0s` — **stop net** ("Mais...")
- `5.0s` — **drone grave froid** (apparition axiome)
- `7.0s–9.0s` — 4x **sub-tick** (chaque critère)
- `10.0s` — **4x tick sec** (les 4 croix)

### Scene12_Conclusion (~14s)
- `0.0s` — **retour musique contemplative**
- `1.0s–5.0s` — 6x **tick doux** (chaque ligne du tableau)
- `7.0s` — **silence musical court**
- `8.0s` — **chime solennel** (apparition de la citation)

### Scene13_Goethe (~8s) — MOMENT SACRÉ
- `0.0s` — **silence musical 1s**
- `1.0s` — **chime cathédrale / bell profonde**
- `2.0s` — **nappe orchestrale montante**
- `5.0s` — **chime doux** ("Goethe")

### Scene14_CTA (~8s)
- `0.0s` — **whoosh final**
- `1.0s` — **chime TerreMathématiques** (logo)
- `2.0s` — **musique pleine** (fin orchestrale)
- `4.0s–6.0s` — 3x **pulse sub** (pulsation du nom)

---

## 🛠 Workflow DaVinci Resolve

1. **Import** des 14 MP4 depuis `media\videos\jesus_water\1920p30\` sur V1
2. **Piste musique** sur A1 (longue boucle ambient)
3. **Piste SFX** sur A2 (tous les effets ponctuels)
4. **Piste ambiance** sur A3 (eau en fond des scènes 01, 03, 04, 06, 10)
5. **Compresseur side-chain** sur A1, déclenché par A2 (ducking auto)
6. **Fairlight → Bus master** : limiteur à -1 dBFS, LUFS cible -14 (standard TikTok)

## 🎯 Règle d'or

**Pas plus d'1 SFX majeur par scène.** Les "🌟" marquent les moments où un son fort
peut vraiment frapper. Tout le reste doit rester subtil, sinon on sature l'oreille.

## 📚 Sources gratuites recommandées

- **Pixabay Music** — pixabay.com/music/ (licence libre, pas d'attribution requise)
- **Freesound** — freesound.org (SFX, attribution selon licence CC)
- **YouTube Audio Library** — studio.youtube.com (intégré YouTube)
- **Uppbeat** — uppbeat.io (free tier pour créateurs)
- **Zapsplat** — zapsplat.com (free avec compte)
