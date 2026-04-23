# Guide Manim — Terre Mathématiques
> Structure de référence pour créer une vidéo TikTok/Shorts avec Manim.
> A donner avant de commencer une nouvelle vidéo.

---

## 1. Structure d'un fichier `.py`

```
from manim import *
import numpy as np

# 1. MÉTADONNÉES
# 2. FORMAT PORTRAIT
# 3. PALETTE
# 4. TAILLES DE POLICE
# 5. UTILITAIRES (fit_w, make_header, TLines, make_bg)
# 6. SCÈNES (Scene00 → SceneCTA)
```

---

## 2. Métadonnées (lues par `render_all.bat`)

```python
SCENES = [
    "Scene01_Titre",
    "Scene02_...",
    # ... toutes les scènes dans l'ordre de montage
    "SceneN_CTA",
]
OUTPUT_NAME = "mon_sujet.mp4"
OUTPUT_DIR  = r"media\videos\mon_fichier\1920p30"
```

- `SCENES` doit lister **toutes** les scènes dans l'ordre exact du montage final.
- `OUTPUT_NAME` = nom du fichier MP4 assemblé.
- `OUTPUT_DIR` = dossier où Manim dépose les scènes rendues (`mon_fichier` = nom du `.py` sans extension).

---

## 3. Format portrait TikTok / Shorts

```python
config.frame_width  = 4.5
config.frame_height = 8.0
```

Toujours en tête du fichier, avant toute scène.
Ratio 9:16 — correspond à 1080×1920 px rendu en `1920p30`.

> **⚠️ Marges de sécurité TikTok — à respecter impérativement**
> L'interface TikTok masque les bords de la vidéo : boutons like/partage à droite, nom du compte et description en bas, barre de progression en bas, décorations en haut. **Laisser une zone vide d'au moins ~0.5 unité Manim sur chaque bord (haut, bas, gauche, droite).** En pratique :
> - Horizontal : `fit_w(mob, 0.82)` au maximum — ne pas dépasser.
> - Vertical : ne jamais placer d'élément au-dessus de `y = 3.3` ni en dessous de `y = -3.3` (sur un frame de hauteur 8.0).
> - Éviter de remplir toute la hauteur : garder le contenu dans la plage `y ∈ [-3.0, 3.0]` pour être sûr.
> Un contenu trop proche du bord sera coupé ou invisible à la lecture TikTok.

---

## 4. Palette standard

```python
SABLE       = "#F5F0E8"   # fond, texte principal
AUBERGINE   = "#4A1942"   # titres, accents forts
AUBERG_DARK = "#2E0E28"   # boîtes sombres
GOLD        = "#C8A951"   # séparateurs, highlights
SOFT_BLACK  = "#2C2C2C"   # corps de texte sur fond clair
RICE_LIGHT  = "#E8D9B0"   # fill des boxes surlignées
RICE_DARK   = "#A0845C"   # éléments secondaires chauds
GREEN_OK    = "#27AE60"   # graphe / validation
BLUE_OK     = "#2E86C1"   # graphe / info
RED_WARN    = "#C0392B"   # graphe / alerte
```

Fond de scène par défaut : `SABLE`.
Ne jamais utiliser du texte blanc car pas visible sur le fond SABLE
---

## 5. Tailles de police

```python
HEADER_FONT       = 30   # titre de section (make_header)
TITLE_FONT        = 54   # titre principal (scène titre)
SUBTITLE_FONT     = 38   # sous-titre
HOOK_FONT         = 34   # accroche forte
BODY_FONT         = 20   # corps de texte normal
BODY_SMALL_FONT   = 17   # corps secondaire / légendes
MATH_FONT         = 30   # formules principales
MATH_SMALL_FONT   = 24   # formules secondaires / inline
```

---

## 6. Utilitaires

### `fit_w` — éviter les débordements latéraux
```python
def fit_w(mob, frac=0.82):
    max_w = config.frame_width * frac
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob
```
- Appeler sur **chaque** `Tex`, `MathTex`, ou `VGroup` qui pourrait dépasser.
- `frac=0.82` par défaut — utiliser `0.70` pour les titres très larges, `0.88` pour du texte court.
- **Ne jamais** laisser un élément sans `fit_w` si son contenu peut varier.

### `make_header` — titre de scène centré
```python
def make_header(text):
    h = Tex(r"\textbf{" + text + "}", font_size=HEADER_FONT, color=AUBERGINE)
    fit_w(h, 0.84)
    span = min(config.frame_width * 0.84, h.width + 0.6)
    line = Line(LEFT * span / 2, RIGHT * span / 2, color=GOLD, stroke_width=2)
    line.next_to(h, DOWN, buff=0.12)
    return VGroup(h, line)
```
- Retourne un `VGroup(titre, filet)` **sans position** — le positionnement se fait dans le `VGroup` global de la scène.
- **Ne pas** appeler `.move_to()` sur le header séparément.
- Animer avec `Write(header)`.

### `TLines` — plusieurs lignes de texte empilées
```python
def TLines(*lines, font_size=BODY_FONT, color=SOFT_BLACK, buff=0.14, **kwargs):
    group = VGroup(*[Tex(ln, font_size=font_size, color=color, **kwargs) for ln in lines])
    group.arrange(DOWN, buff=buff, aligned_edge=ORIGIN)
    for mob in group:
        fit_w(mob, 0.84)
    return group
```
- Passer chaque ligne comme argument séparé : `TLines(r"ligne 1", r"ligne 2")`.
- Ajuster `buff` : `0.14` standard, `0.18–0.22` si les lignes sont longues ou si on veut de l'air.

### `make_bg` — fond de scène
```python
def make_bg(scene):
    scene.camera.background_color = SABLE
```
- À appeler en **première ligne** de chaque `construct()`.

Règle simple : toute chaîne qui contient des commandes LaTeX (\', \a, \^e...) doit être une raw string r"..." à l'endroit où tu l'écris. Surtout dans les make_header.
# Avec r"" dans l'appel :
make_header(r"Le r\'eflecteur")
---

## 7. Centrage global — règle d'or

**Toujours** assembler tous les éléments dans un `VGroup` global, puis `move_to(ORIGIN)`.

```python
full = VGroup(header, element1, element2, element3).arrange(
    DOWN, buff=0.45, aligned_edge=ORIGIN,
)
full.move_to(ORIGIN)
```

- `buff=0.35–0.50` entre blocs principaux.
- `buff=0.14–0.22` entre lignes d'un même bloc.
- Les éléments positionnés relativement (`next_to`, `move_to`) doivent être créés **après** le `move_to(ORIGIN)` du groupe principal (ex : flèches, boxes de surligna).
- Le titre (`make_header`) doit être **dans** le `VGroup` global — c'est ce qui garantit qu'il reste au centre vertical de l'écran, pas en haut.

---

## 8. Règles `self.wait` — timing des pauses

| Type de contenu | Durée conseillée |
|---|---|
| Header seul affiché | `0.3 – 0.5` |
| Texte court (≤ 5 mots) | `0.8 – 1.2` |
| Texte normal (1–2 lignes) | `1.5 – 2.0` |
| Texte long (3+ lignes) | `2.5 – 3.5` |
| Formule mathématique simple | `2.5 – 3.0` |
| Formule mathématique complexe | `3.5 – 4.5` |
| Punch final / conclusion | `3.5 – 5.0` |
| Avant un FadeOut général | `≥ 3.0` |

**Principe :** le spectateur lit sur mobile, souvent sans son. Laisser le temps.

---

## 9. Animations — bonnes pratiques

### FadeIn pour le texte
```python
self.play(FadeIn(element, shift=UP * 0.1), run_time=0.7)
```
Le `shift=UP * 0.1` donne un léger mouvement d'entrée naturel.

### Write pour les titres et formules
```python
self.play(Write(header), run_time=0.7)
self.play(Write(formule), run_time=0.9)
```

### LaggedStart pour les listes
```python
self.play(
    LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in liste], lag_ratio=0.18),
    run_time=1.6,
)
```

### FadeOut général en fin de scène
```python
self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
```
Toujours terminer par un FadeOut propre — facilite le montage.

### Flèches
```python
arrow = Arrow(
    depart.get_right() + RIGHT * 0.05,
    arrivee.get_left() + LEFT * 0.05,
    buff=0.05, color=GOLD, stroke_width=2.5,
    max_tip_length_to_length_ratio=0.18,
)
self.play(GrowArrow(arrow), run_time=0.8)
```
Créer la flèche **après** `move_to(ORIGIN)` pour que les coordonnées soient correctes.

### Boîtes de surligna
```python
box = SurroundingRectangle(
    element, color=GOLD, buff=0.16, stroke_width=2,
    fill_color=RICE_LIGHT, fill_opacity=0.4,
)
self.play(Create(box), run_time=0.5)
```

---

## 10. Structure type d'une scène

```python
class SceneXX_NomScene(Scene):
    def construct(self):
        make_bg(self)

        # ── Construire les éléments ──────────────────────────
        header = make_header("Titre de la scène")

        texte = TLines(
            r"Première ligne",
            r"Deuxième ligne",
            font_size=BODY_FONT, color=SOFT_BLACK,
        )

        formule = MathTex(r"E = mc^2", font_size=MATH_FONT, color=AUBERGINE)
        fit_w(formule, 0.84)

        # ── Centrage global ─────────────────────────────────
        full = VGroup(header, texte, formule).arrange(
            DOWN, buff=0.45, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Éléments relatifs créés APRÈS le move_to
        box = SurroundingRectangle(formule, color=GOLD, buff=0.16, stroke_width=2,
                                   fill_color=RICE_LIGHT, fill_opacity=0.4)

        # ── Animations ──────────────────────────────────────
        self.play(Write(header), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in texte], lag_ratio=0.18),
            run_time=1.4,
        )
        self.wait(2.0)
        self.play(Write(formule), run_time=0.9)
        self.play(Create(box), run_time=0.5)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
```

---

## 11. Scène Titre (Scene01)

```python
class Scene01_Titre(Scene):
    def construct(self):
        make_bg(self)

        title = Tex(r"\textbf{Titre principal}", font_size=TITLE_FONT, color=AUBERGINE)
        fit_w(title, 0.80)

        subtitle = TLines(r"Sous-titre accrocheur", font_size=SUBTITLE_FONT, color=GOLD)
        fit_w(subtitle, 0.78)

        sep_w = min(config.frame_width * 0.76, max(title.width, subtitle.width) * 1.06)
        sep = Line(LEFT * sep_w / 2, RIGHT * sep_w / 2, color=GOLD, stroke_width=2)

        author = Tex(r"Terre Math\'ematiques", font_size=32, color=AUBERGINE)
        fit_w(author, 0.70)

        block = VGroup(title, subtitle, sep, author).arrange(DOWN, buff=0.45, aligned_edge=ORIGIN)

        hook = TLines(
            r"Accroche ligne 1\dots",
            r"Accroche ligne 2.",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.15,
        )
        fit_w(hook, 0.82)

        full = VGroup(block, hook).arrange(DOWN, buff=0.8, aligned_edge=ORIGIN)
        full.move_to(ORIGIN)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)
        self.play(Create(sep), FadeIn(author), run_time=0.7)
        self.play(FadeIn(hook, shift=UP * 0.2), run_time=0.8)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
```

---

## 12. Scène CTA finale (toujours la dernière)

```python
class SceneN_CTA(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        # ── Logo rond ────────────────────────────────────────
        R = 0.52
        logo = ImageMobject("logo.jpg")
        logo.set_width(R * 2)
        border = Circle(radius=R + 0.04, color=AUBERGINE, stroke_width=3, fill_opacity=0)
        mask = Cutout(
            Square(side_length=1.6, fill_color=SABLE, fill_opacity=1, stroke_width=0),
            Circle(radius=R),
            fill_color=SABLE, fill_opacity=1, stroke_width=0,
        )
        logo.move_to(ORIGIN)
        border.move_to(ORIGIN)
        mask.move_to(ORIGIN)
        disc_block = Group(logo, border)

        # ── Texte CTA ────────────────────────────────────────
        name = Tex(r"\textbf{TERRE MATH\'EMATIQUES}", font_size=34, color=AUBERGINE)
        max_w = config.frame_width * 0.78
        if name.width > max_w:
            name.scale_to_fit_width(max_w)

        w_sep = min(name.width * 1.12, config.frame_width * 0.72)
        sep = Line(LEFT * w_sep / 2, RIGHT * w_sep / 2, color=GOLD, stroke_width=1.4)

        cta = TLines(
            r"Abonne-toi pour plus",
            r"de maths \textbf{amusantes}",
            r"\& surprenantes !",
            font_size=26, color=SOFT_BLACK, buff=0.16,
        )

        text_block = VGroup(name, sep, cta).arrange(DOWN, buff=0.34, aligned_edge=ORIGIN)
        column = Group(disc_block, text_block).arrange(DOWN, buff=1.02, aligned_edge=ORIGIN)
        column.move_to(ORIGIN)
        mask.move_to(logo.get_center())

        # ── Animations ───────────────────────────────────────
        self.play(FadeIn(logo, scale=1.1), FadeIn(mask), Create(border), run_time=1)
        self.play(FadeIn(name), run_time=0.8)
        self.play(Create(sep), run_time=0.5)
        self.play(FadeIn(cta, shift=UP * 0.12), run_time=0.6)

        # Pulsation du nom × 3
        for _ in range(3):
            self.play(name.animate.scale(1.03), rate_func=there_and_back, run_time=0.8)

        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
```

- `logo.jpg` doit être dans le même dossier que le `.py`.
- La pulsation `scale(1.03)` avec `there_and_back` donne un effet "respiration" subtil.
- `Cutout` masque les coins du logo pour le rendre circulaire.

---

## 13. Checklist avant de rendre

- [ ] `SCENES` liste toutes les scènes dans le bon ordre
- [ ] `OUTPUT_NAME` et `OUTPUT_DIR` corrects (nom du `.py` dans le chemin)
- [ ] `config.frame_width = 4.5` / `config.frame_height = 8.0` présents
- [ ] Chaque scène appelle `make_bg(self)` en première ligne
- [ ] Chaque élément a un `fit_w(...)` adapté (≤ 0.82)
- [ ] Aucun élément ne dépasse `y = ±3.0` (marges de sécurité TikTok haut/bas)
- [ ] `make_header` utilisé pour tous les titres de scène
- [ ] `VGroup(...).arrange(DOWN, ...).move_to(ORIGIN)` dans chaque scène
- [ ] Éléments relatifs (flèches, boxes) créés **après** `move_to(ORIGIN)`
- [ ] Chaque scène se termine par `FadeOut` sur tous les mobjects
- [ ] `logo.jpg` présent si la scène CTA est incluse

---

## 14. Pièges courants

| Problème | Cause | Fix |
|---|---|---|
| Texte coupé sur les bords | Pas de `fit_w` | Appeler `fit_w(mob, 0.82)` |
| Éléments tous en haut | `move_to` manquant | `full.move_to(ORIGIN)` sur le VGroup global |
| Flèche mal positionnée | Créée avant `move_to` | La créer après le centrage global |
| Scène manquante dans la vidéo | Absente de `SCENES` | Ajouter dans la liste |
| Logo pas rond | `Cutout` absent ou mal positionné | `mask.move_to(logo.get_center())` après `column.move_to(ORIGIN)` |
| Formule qui déborde | `MathTex` sans `fit_w` | Toujours `fit_w(formule, 0.84)` |
| Contenu coupé sur TikTok | Trop proche des bords | Rester dans `y ∈ [-3.0, 3.0]` et `fit_w ≤ 0.82` — l'UI TikTok masque les bords haut/bas/gauche/droite |
