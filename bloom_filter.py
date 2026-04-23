"""
Bloom Filter — TikTok TerreMathématique
Format vertical 1080x1920, 60 fps.
Rendu : manim -pqh bloom_filter.py <SceneName>
Pour la version finale : manim -pqh --resolution 1920,1080 ... (à adapter selon ta config TikTok)
"""

from manim import *
import numpy as np
import re


# ---------------------------------------------------------------------------
# PALETTE TERREMATHÉMATIQUE — style inspiré de new.py
# ---------------------------------------------------------------------------
SABLE       = "#F5F0E8"
AUBERGINE   = "#4A1942"
AUBERG_DARK = "#2E0E28"
GOLD        = "#C8A951"
SOFT_BLACK  = "#2C2C2C"
SLATE       = "#5C6B7A"
RED_TM      = "#A8423F"
GREEN_TM    = "#2E8B57"
YELLOW_TM   = "#D9B84A"

# Alias conservé pour compatibilité avec les scènes existantes
SAND = SOFT_BLACK

# Format vertical TikTok
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.background_color = SABLE

# ---------------------------------------------------------------------------
# TAILLES DE POLICE
# ---------------------------------------------------------------------------
HEADER_FONT = 30
BODY_FONT = 28
BODY_SMALL_FONT = 22
MATH_FONT = 34

# ---------------------------------------------------------------------------
# MÉTADONNÉES — lues par render_all.bat
# ---------------------------------------------------------------------------
SCENES = [
    "HookScene",
    "TwoWorldsScene",
    "HashFunctionScene",   # NEW — ce qu'est une fonction de hachage
    "BuildFilterScene",
    "BitMeaningScene",     # NEW — pourquoi 0 garantit l'absence
    "QueryScene",
    "WhyItMattersScene",
    "OutroScene",
]
OUTPUT_NAME = "bloom_filter.mp4"
OUTPUT_DIR  = "media/videos/bloom_filter/1920p30"


# ---------------------------------------------------------------------------
# UTILITAIRES
# ---------------------------------------------------------------------------
def fit_w(mob, frac=0.84):
    max_w = config.frame_width * frac
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob


def make_bg(scene):
    scene.camera.background_color = SABLE


def _escape_tex(s: str) -> str:
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    return "".join(repl.get(ch, ch) for ch in s)


def _unicode_to_tex(s: str) -> str:
    sub_map = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
    s = re.sub(
        r"([A-Za-z])([₀₁₂₃₄₅₆₇₈₉]+)",
        lambda m: f"${m.group(1)}_{{{m.group(2).translate(sub_map)}}}$",
        s,
    )
    replacements = {
        "→": r"$\to$",
        "≤": r"$\leq$",
        "≥": r"$\geq$",
        "÷": r"$\div$",
        "×": r"$\times$",
        "…": r"\ldots{}",
        "—": r"---",
        "–": r"--",
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    return s


def tm_text(s, size=BODY_FONT, color=SOFT_BLACK, weight=NORMAL, font=None, italic=False):
    s = _unicode_to_tex(s)
    parts = re.split(r"(\$.*?\$)", s)
    body_parts = []
    for part in parts:
        if not part:
            continue
        if part.startswith("$") and part.endswith("$"):
            body_parts.append(part)
        else:
            body_parts.append(_escape_tex(part).replace("\n", r"\ "))
    body = "".join(body_parts)
    if font == "Courier":
        body = rf"\texttt{{{body}}}"
    if italic:
        body = rf"\textit{{{body}}}"
    if weight == BOLD:
        body = rf"\textbf{{{body}}}"
    mob = Tex(body, font_size=size, color=color)
    return fit_w(mob, 0.84)


def tm_math(s, size=MATH_FONT, color=SOFT_BLACK):
    mob = MathTex(s, font_size=size, color=color)
    return fit_w(mob, 0.84)


def TLines(*lines, font_size=BODY_FONT, color=SOFT_BLACK, buff=0.18, **kwargs):
    group = VGroup(*[Tex(ln, font_size=font_size, color=color, **kwargs) for ln in lines])
    group.arrange(DOWN, buff=buff, aligned_edge=ORIGIN)
    for mob in group:
        fit_w(mob, 0.84)
    return group


def make_header(text):
    h = Tex(r"\textbf{" + text + "}", font_size=HEADER_FONT, color=AUBERGINE)
    fit_w(h, 0.84)
    span = min(config.frame_width * 0.84, h.width + 0.6)
    line = Line(LEFT * span / 2, RIGHT * span / 2, color=GOLD, stroke_width=2)
    line.next_to(h, DOWN, buff=0.12)
    return VGroup(h, line)


def make_bit_array(m=10, bit_size=0.55, spacing=0.05):
    """Crée un ruban de m cases binaires, toutes à 0."""
    cases = VGroup()
    for i in range(m):
        sq = Square(side_length=bit_size, color=SLATE, fill_color=SABLE,
                    fill_opacity=1, stroke_width=2)
        zero = tm_math("0", size=28, color=SLATE)
        zero.move_to(sq.get_center())
        case = VGroup(sq, zero)
        cases.add(case)
    cases.arrange(RIGHT, buff=spacing)
    return cases


def light_bit(case, color=GOLD):
    """Anime une case qui passe de 0 à 1."""
    sq, digit = case[0], case[1]
    new_digit = tm_math("1", size=28, color=SABLE).move_to(sq.get_center())
    return AnimationGroup(
        sq.animate.set_fill(color, opacity=1).set_stroke(color),
        Transform(digit, new_digit),
        lag_ratio=0
    )


# ---------------------------------------------------------------------------
# SCÈNE 1 — HookScene
# ---------------------------------------------------------------------------
class HookScene(Scene):
    def construct(self):
        make_bg(self)
        field_bg = RoundedRectangle(width=7, height=1.2, corner_radius=0.15,
                                    color=SAND, stroke_width=3, fill_opacity=0)
        field_bg.shift(UP * 1)

        label = tm_text("Choisissez votre nom d'utilisateur", size=32, color=SAND)
        label.next_to(field_bg, UP, buff=0.3)

        typed = tm_text("john.smith", size=42, color=AUBERGINE, font="Courier")
        typed.move_to(field_bg.get_center())

        verdict = tm_text("Pseudonyme déjà pris", size=44, color=RED_TM, weight=BOLD)
        verdict.next_to(field_bg, DOWN, buff=0.6)

        # Question d'accroche — 4 lignes, crescendo
        q1 = tm_text("Gmail a 2 milliards de comptes.", size=32, color=SAND)
        q2 = tm_text("Il a répondu en 3 millisecondes.", size=32, color=SAND)
        q3 = tm_text("Sans chercher dans la base.", size=34, color=GOLD, weight=BOLD)
        q4 = tm_text("Comment c'est possible ?", size=38, color=GOLD, weight=BOLD)
        q5 = tm_text("Un Bloom filter.", size=44, color=SAND, weight=BOLD)
        q1.shift(DOWN * 2.8)
        q2.next_to(q1, DOWN, buff=0.3)
        q3.next_to(q2, DOWN, buff=0.35)
        q4.next_to(q3, DOWN, buff=0.5)
        q5.next_to(q4, DOWN, buff=0.55)

        self.play(FadeIn(label), Create(field_bg), run_time=0.8)
        self.play(Write(typed), run_time=1.5)
        self.wait(0.8)
        self.play(FadeIn(verdict, shift=UP * 0.2), run_time=0.8)
        self.wait(1.2)

        self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(q3, shift=UP * 0.2), run_time=0.9)
        self.wait(1.0)
        self.play(Write(q4), run_time=1.4)
        self.wait(1.5)
        self.play(FadeIn(q5, shift=UP * 0.2, scale=1.05), run_time=1.0)
        self.wait(3.0)


# ---------------------------------------------------------------------------
# SCÈNE 2 — TwoWorldsScene
# ---------------------------------------------------------------------------
class TwoWorldsScene(Scene):
    def construct(self):
        make_bg(self)
        db_label = tm_text("Base de données", size=38, color=GOLD)
        db_label.shift(UP * 6)

        fiches = VGroup()
        names = ["alice", "marc", "julie", "leo", "sara", "tom"]
        for i, name in enumerate(names):
            fiche = RoundedRectangle(width=4.5, height=0.55, corner_radius=0.08,
                                     color=SAND, fill_color=SAND, fill_opacity=0.15,
                                     stroke_width=1.5)
            txt = tm_text(name, size=24, color=AUBERGINE, font="Courier")
            txt.move_to(fiche.get_center())
            fiches.add(VGroup(fiche, txt))
        fiches.arrange(DOWN, buff=0.08)
        fiches.shift(UP * 3.2)

        db_tag = tm_text("exacte · lente", size=26, color=SLATE)
        db_tag.next_to(fiches, DOWN, buff=0.3)

        sep = Line(LEFT * 4, RIGHT * 4, color=SLATE, stroke_width=1).shift(DOWN * 0.5)

        filter_label = tm_text("Bloom filter", size=38, color=GOLD)
        filter_label.shift(DOWN * 1.5)

        bits = make_bit_array(m=12, bit_size=0.5, spacing=0.06)
        bits.next_to(filter_label, DOWN, buff=0.5)

        filter_tag = tm_text("approximatif · instantané", size=26, color=SLATE)
        filter_tag.next_to(bits, DOWN, buff=0.3)

        ram_note = tm_text("en mémoire vive", size=24, color=GOLD, weight=BOLD)
        ram_note.next_to(filter_tag, DOWN, buff=0.5)

        self.play(FadeIn(db_label, shift=DOWN * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(f, shift=LEFT * 0.3) for f in fiches],
                              lag_ratio=0.12), run_time=2.0)
        self.play(FadeIn(db_tag), run_time=0.7)
        self.wait(1.5)

        self.play(Create(sep), run_time=0.6)

        self.play(FadeIn(filter_label, shift=UP * 0.3), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(bits), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(filter_tag), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(ram_note, shift=UP * 0.2), run_time=0.8)
        self.wait(5)


# ---------------------------------------------------------------------------
# SCÈNE 2b — HashFunctionScene — "c'est quoi une fonction de hachage ?"
# ---------------------------------------------------------------------------
class HashFunctionScene(Scene):
    def construct(self):
        make_bg(self)
        title = make_header(r"C'est quoi une fonction de hachage ?")
        title.to_edge(UP, buff=0.55)
        self.play(FadeIn(title), run_time=0.8)
        self.wait(0.8)

        # Boîte noire "h"
        box = RoundedRectangle(width=2.2, height=1.4, corner_radius=0.2,
                               color=GOLD, fill_color=AUBERG_DARK, fill_opacity=1,
                               stroke_width=3)
        box.shift(UP * 3.5)
        box_label = tm_math("h", size=52, color=GOLD)
        box_label.move_to(box.get_center())
        self.play(Create(box), FadeIn(box_label), run_time=0.8)
        self.wait(0.5)

        # "alice" entre dans la boîte
        word_in = tm_text("alice", size=32, color=AUBERGINE, font="Courier")
        word_in.next_to(box, LEFT, buff=1.3)
        arrow_in = Arrow(word_in.get_right(), box.get_left(),
                         color=SLATE, stroke_width=2, buff=0.1)
        self.play(FadeIn(word_in), run_time=0.8)
        self.play(GrowArrow(arrow_in), run_time=0.8)
        self.wait(0.5)

        # Calcul étape par étape — SOUS la boîte, pas dedans
        step1_txt = tm_text("Chaque lettre a un numéro :", size=26, color=SLATE)
        step1_val = tm_text("a=1   l=12   i=9   c=3   e=5", size=24, color=AUBERGINE, font="Courier")
        step1_txt.next_to(box, DOWN, buff=0.9)
        step1_val.next_to(step1_txt, DOWN, buff=0.18)

        self.play(FadeIn(step1_txt, shift=UP * 0.1), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(step1_val, shift=UP * 0.1), run_time=0.8)
        self.wait(1.5)

        step2_txt = tm_text("On les additionne :", size=26, color=SLATE)
        step2_val = tm_text("1+12+9+3+5 = 30", size=26, color=SAND)
        step2_txt.next_to(step1_val, DOWN, buff=0.45)
        step2_val.next_to(step2_txt, DOWN, buff=0.18)

        self.play(FadeIn(step2_txt, shift=UP * 0.1), run_time=0.8)
        self.wait(0.4)
        self.play(FadeIn(step2_val, shift=UP * 0.1), run_time=0.8)
        self.wait(1.2)

        step3_txt = tm_text("Le filtre a 12 cases.", size=26, color=SLATE)
        step3_sub = tm_text("30 ÷ 12 = 2,  reste  6", size=26, color=SAND)
        step3_exp = tm_text("(on garde juste le reste)", size=22, color=SLATE)
        step3_result = tm_text("→  position  6", size=30, color=GOLD, weight=BOLD)
        step3_txt.next_to(step2_val, DOWN, buff=0.45)
        step3_sub.next_to(step3_txt, DOWN, buff=0.18)
        step3_exp.next_to(step3_sub, DOWN, buff=0.12)
        step3_result.next_to(step3_exp, DOWN, buff=0.3)

        self.play(FadeIn(step3_txt, shift=UP * 0.1), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(step3_sub, shift=UP * 0.1), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(step3_exp, shift=UP * 0.1), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(step3_result, shift=UP * 0.15, scale=1.05), run_time=0.9)
        self.wait(2.5)

        # La boîte sort "position 6" sur la droite
        out_txt = tm_text("position  6", size=32, color=GOLD)
        out_txt.next_to(box, RIGHT, buff=1.0)
        arrow_out = Arrow(box.get_right(), out_txt.get_left(),
                          color=SLATE, stroke_width=2, buff=0.1)
        self.play(GrowArrow(arrow_out), run_time=0.8)
        self.play(FadeIn(out_txt), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(step1_txt), FadeOut(step1_val),
                  FadeOut(step2_txt), FadeOut(step2_val),
                  FadeOut(step3_txt), FadeOut(step3_sub),
                  FadeOut(step3_exp), FadeOut(step3_result), run_time=0.5)

        # Propriété clé : déterministe
        det = tm_text("même mot  →  toujours même résultat", size=26, color=SLATE)
        det.next_to(box, DOWN, buff=1.0)
        self.play(FadeIn(det, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)

        self.play(FadeOut(word_in), FadeOut(arrow_in),
                  FadeOut(arrow_out), FadeOut(out_txt), FadeOut(det), run_time=0.5)
        self.wait(0.4)

        # On utilise 3 fonctions → 3 positions différentes
        three_lbl = tm_text("Pour un Bloom filter, on utilise plusieurs fonctions", size=28, color=SAND)
        three_lbl2 = tm_text("de hachage pour allumer plusieurs cases.", size=28, color=SAND)
        three_lbl.next_to(box, DOWN, buff=0.7)
        three_lbl2.next_to(three_lbl, DOWN, buff=0.18)
        self.play(FadeIn(three_lbl), FadeIn(three_lbl2), run_time=0.8)
        self.wait(1.0)

        word2 = tm_text("alice", size=30, color=AUBERGINE, font="Courier")
        word2.next_to(box, LEFT, buff=1.2)
        self.play(FadeIn(word2), run_time=0.8)
        self.wait(0.5)

        formula_lines = VGroup(
            tm_text("h₁(x) = (somme des numéros) mod 12", size=26, color=SLATE),
            tm_text("h₂(x) = (somme × position) mod 12", size=26, color=SLATE),
            tm_text("h₃(x) = (somme + index) mod 12", size=26, color=SLATE),
        ).arrange(DOWN, buff=0.22)
        formula_lines.next_to(three_lbl2, DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in formula_lines],
                               lag_ratio=0.4), run_time=1.2)
        self.wait(1.0)

        pos_lines = VGroup(
            tm_text("h₁(alice) → case 6", size=28, color=GOLD),
            tm_text("h₂(alice) → case 3", size=28, color=GOLD),
            tm_text("h₃(alice) → case 9", size=28, color=GOLD),
        ).arrange(DOWN, buff=0.35)
        pos_lines.next_to(box, RIGHT, buff=0.9)
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in pos_lines],
                               lag_ratio=0.6), run_time=2.0)
        self.wait(2.0)

        # Mini ruban pour visualiser les 3 cases allumées
        mini_bits = make_bit_array(m=12, bit_size=0.42, spacing=0.04)
        mini_bits.shift(DOWN * 2.2)
        mini_idx = VGroup()
        for i, case in enumerate(mini_bits):
            lbl = tm_math(str(i), size=16, color=SLATE)
            lbl.next_to(case, UP, buff=0.08)
            mini_idx.add(lbl)

        self.play(FadeIn(mini_bits), FadeIn(mini_idx), run_time=0.8)
        self.wait(0.4)
        self.play(*[light_bit(mini_bits[p]) for p in [3, 6, 9]], run_time=1.0)
        self.wait(0.8)

        # Flèches reliant les étiquettes aux cases
        arrows_to_bits = VGroup()
        for line, pos in zip(pos_lines, [6, 3, 9]):
            a = Arrow(
                start=line.get_bottom() + DOWN * 0.05,
                end=mini_bits[pos].get_top() + UP * 0.05,
                color=GOLD, stroke_width=1.5, buff=0.05,
                max_tip_length_to_length_ratio=0.15,
            )
            arrows_to_bits.add(a)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows_to_bits],
                               lag_ratio=0.35), run_time=1.5)
        self.wait(0.8)

        recap = tm_text("→ 3 cases allumées dans le filtre", size=28, color=GOLD)
        recap.shift(DOWN * 4)
        self.play(FadeIn(recap, shift=UP * 0.15), run_time=0.8)
        self.wait(3.5)


# ---------------------------------------------------------------------------
# SCÈNE 3b — BitMeaningScene — pourquoi 0 garantit l'absence (le cœur logique)
# ---------------------------------------------------------------------------
class BitMeaningScene(Scene):
    def construct(self):
        make_bg(self)
        title = make_header("Ce que dit le filtre")
        title.to_edge(UP, buff=0.55)
        self.play(FadeIn(title), run_time=0.8)
        self.wait(0.8)

        # Filtre rempli
        m = 12
        bits = make_bit_array(m=m, bit_size=0.52, spacing=0.05)
        bits.shift(UP * 4.2)
        already_lit = {0, 1, 2, 3, 6, 7, 9}
        for p in already_lit:
            sq = bits[p][0]
            sq.set_fill(GOLD, opacity=1).set_stroke(GOLD)
            new_digit = tm_math("1", size=26, color=SABLE).move_to(sq.get_center())
            bits[p][1].become(new_digit)
        idx_labels = VGroup()
        for i, case in enumerate(bits):
            lbl = tm_math(str(i), size=16, color=SLATE)
            lbl.next_to(case, UP, buff=0.08)
            idx_labels.add(lbl)
        self.play(FadeIn(bits), FadeIn(idx_labels), run_time=0.8)
        self.wait(0.8)

        # ── Cas 1 : bit à 0 ──────────────────────────────────────────────
        halo0 = Square(side_length=0.75, color=GREEN_TM, stroke_width=4, fill_opacity=0)
        halo0.move_to(bits[4].get_center())
        self.play(Create(halo0), run_time=0.7)
        self.wait(0.5)

        expl0 = VGroup(
            tm_text("La case 4 est à 0.", size=30, color=GREEN_TM, weight=BOLD),
            tm_text("Si quelqu'un était enregistré", size=26, color=SAND),
            tm_text("avec h₂ → 4,", size=26, color=SAND),
            tm_text("cette case serait à 1.", size=26, color=SAND),
            tm_text("Elle est à 0  →", size=28, color=GREEN_TM),
            tm_text("personne n'a ce hash.", size=28, color=GREEN_TM),
            tm_text("Absent. Garanti.", size=36, color=GREEN_TM, weight=BOLD),
        ).arrange(DOWN, buff=0.25)
        expl0.shift(DOWN * 1.2)
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.1) for e in expl0],
                               lag_ratio=0.35), run_time=4.5)
        self.wait(3.5)
        self.play(FadeOut(halo0), FadeOut(expl0), run_time=0.6)
        self.wait(0.5)

        # ── Cas 2 : tous les bits à 1 ────────────────────────────────────
        halos1 = VGroup()
        for p in [3, 6, 9]:
            h = Square(side_length=0.75, color=YELLOW_TM, stroke_width=4, fill_opacity=0)
            h.move_to(bits[p].get_center())
            halos1.add(h)
        self.play(LaggedStart(*[Create(h) for h in halos1], lag_ratio=0.3), run_time=1.0)
        self.wait(0.5)

        expl1 = VGroup(
            tm_text("Les cases 3, 6, 9 sont à 1.", size=28, color=YELLOW_TM, weight=BOLD),
            tm_text("Elles ont été allumées par", size=26, color=SAND),
            tm_text("alice, marc, ou julie…", size=26, color=SAND),
            tm_text("ou quelqu'un d'autre.", size=26, color=SAND),
            tm_text("Peut-être ton pseudo,", size=28, color=YELLOW_TM),
            tm_text("peut-être une coïncidence.", size=28, color=YELLOW_TM),
            tm_text("→ On ne sait pas encore.", size=30, color=SLATE, weight=BOLD),
        ).arrange(DOWN, buff=0.25)
        expl1.shift(DOWN * 1.2)
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.1) for e in expl1],
                               lag_ratio=0.35), run_time=4.5)
        self.wait(4.0)


# ---------------------------------------------------------------------------
# SCÈNE 3 — BuildFilterScene
# ---------------------------------------------------------------------------
class BuildFilterScene(Scene):
    def construct(self):
        make_bg(self)
        title = make_header("Construction du filtre")
        title.to_edge(UP, buff=0.55)

        m = 12
        bits = make_bit_array(m=m, bit_size=0.55, spacing=0.06)
        bits.shift(DOWN * 1.5)

        idx_labels = VGroup()
        for i, case in enumerate(bits):
            lbl = tm_math(str(i), size=18, color=SLATE)
            lbl.next_to(case, UP, buff=0.1)
            idx_labels.add(lbl)

        # Rappel des fonctions de hachage
        hash_expl = tm_text("3 fonctions de hachage =", size=30, color=SLATE)
        hash_expl2 = tm_text("mot  →  3 cases à allumer", size=30, color=GOLD)
        hash_expl.shift(UP * 4.5)
        hash_expl2.next_to(hash_expl, DOWN, buff=0.25)

        self.play(FadeIn(title), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(hash_expl), FadeIn(hash_expl2), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(hash_expl), FadeOut(hash_expl2), run_time=0.5)
        self.play(FadeIn(bits), FadeIn(idx_labels), run_time=0.8)
        self.wait(0.8)

        # Insertions successives
        insertions = [
            ("alice", [3, 6, 9]),
            ("marc",  [2, 5, 9]),
            ("julie", [0, 5, 7]),
        ]

        for name, positions in insertions:
            word = tm_text(name, size=36, color=AUBERGINE, font="Courier")
            word.shift(UP * 1.5)
            self.play(Write(word), run_time=0.8)
            self.wait(0.4)

            arrows = VGroup()
            for p in positions:
                arrow = Arrow(start=word.get_bottom() + DOWN * 0.1,
                              end=bits[p].get_top() + UP * 0.05,
                              color=GOLD, stroke_width=3, buff=0.05,
                              max_tip_length_to_length_ratio=0.1)
                arrows.add(arrow)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows],
                                  lag_ratio=0.25), run_time=1.0)
            self.wait(0.3)

            self.play(*[light_bit(bits[p]) for p in positions], run_time=0.9)
            self.wait(0.8)

            self.play(FadeOut(word), FadeOut(arrows), run_time=0.5)
            self.wait(0.3)

        # Pluie de pseudos — accélération volontaire
        rain_names = ["leo", "sara", "tom", "iris", "paul", "emma", "lou", "max"]
        for name in rain_names:
            word = tm_text(name, size=28, color=AUBERGINE, font="Courier")
            word.shift(UP * 1.5 + LEFT * np.random.uniform(-1.5, 1.5))
            positions = list(np.random.choice(m, 3, replace=False))
            self.play(
                FadeIn(word, shift=DOWN * 0.3),
                *[light_bit(bits[p]) for p in positions],
                run_time=0.3
            )
            self.play(FadeOut(word), run_time=0.2)

        # Règle de construction
        rule = tm_text("Pour chaque pseudo enregistré,", size=30, color=SAND)
        rule2 = tm_text("on allume 3 cases dans le filtre.", size=30, color=GOLD)
        rule.shift(UP * 1.5)
        rule2.next_to(rule, DOWN, buff=0.25)
        self.play(FadeIn(rule, shift=UP * 0.2), run_time=0.9)
        self.wait(0.5)
        self.play(FadeIn(rule2, shift=UP * 0.2), run_time=0.9)
        self.wait(3.0)


# ---------------------------------------------------------------------------
# SCÈNE 4 — QueryScene  — LE PIVOT
# ---------------------------------------------------------------------------
class QueryScene(Scene):
    def construct(self):
        make_bg(self)
        # État initial : filtre rempli
        m = 12
        bits = make_bit_array(m=m, bit_size=0.55, spacing=0.06)
        bits.shift(UP * 1.5)

        already_lit = {0, 1, 2, 5, 7, 8, 9}
        for p in already_lit:
            sq = bits[p][0]
            sq.set_fill(GOLD, opacity=1).set_stroke(GOLD)
            new_digit = tm_math("1", size=28, color=SABLE).move_to(sq.get_center())
            bits[p][1].become(new_digit)

        idx_labels = VGroup()
        for i, case in enumerate(bits):
            lbl = tm_math(str(i), size=18, color=SLATE)
            lbl.next_to(case, UP, buff=0.1)
            idx_labels.add(lbl)

        self.add(bits, idx_labels)

        # Règle du filtre — affichée en haut
        rule_absent = tm_text("un bit à 0  →  absent à 100 %", size=26, color=GREEN_TM)
        rule_maybe  = tm_text("tous à 1    →  peut-être présent", size=26, color=YELLOW_TM)
        rule_absent.shift(UP * 6.8)
        rule_maybe.next_to(rule_absent, DOWN, buff=0.3)
        self.play(FadeIn(rule_absent), run_time=0.9)
        self.wait(1.0)
        self.play(FadeIn(rule_maybe), run_time=0.9)
        self.wait(2.0)

        # Champ de saisie
        field_bg = RoundedRectangle(width=5, height=0.9, corner_radius=0.1,
                                    color=SAND, stroke_width=2, fill_opacity=0)
        field_bg.shift(UP * 4.5)
        self.play(Create(field_bg), run_time=0.5)

        # ── CAS 1 : "zara" — positions [3, 6, 10], toutes à 0 → absent ──
        typed1 = tm_text("zara", size=36, color=AUBERGINE, font="Courier")
        typed1.move_to(field_bg.get_center())
        self.play(Write(typed1), run_time=0.9)
        self.wait(0.5)

        zara_positions = [3, 6, 10]
        halos1 = VGroup()
        for p in zara_positions:
            halo = Square(side_length=0.7, color=RED_TM, stroke_width=4, fill_opacity=0)
            halo.move_to(bits[p].get_center())
            halos1.add(halo)
        self.play(LaggedStart(*[Create(h) for h in halos1], lag_ratio=0.3), run_time=1.0)
        self.wait(0.8)

        zero_arrow = Arrow(
            start=bits[3].get_bottom() + DOWN * 0.05,
            end=bits[3].get_bottom() + DOWN * 0.6,
            color=RED_TM, stroke_width=3, buff=0.0,
            max_tip_length_to_length_ratio=0.2
        )
        zero_note = tm_text("0 !", size=28, color=RED_TM, weight=BOLD)
        zero_note.next_to(zero_arrow, DOWN, buff=0.1)
        self.play(GrowArrow(zero_arrow), run_time=0.7)
        self.play(FadeIn(zero_note), run_time=0.6)
        self.wait(1.0)

        verdict1_box = RoundedRectangle(width=7.8, height=1.4, corner_radius=0.15,
                                        color=GREEN_TM, stroke_width=3, fill_opacity=0.1)
        verdict1_box.shift(DOWN * 1.2)
        verdict1 = tm_text("ABSENT — pas de requête SQL", size=32, color=GREEN_TM, weight=BOLD)
        verdict1.move_to(verdict1_box.get_center())
        self.play(Create(verdict1_box), run_time=0.6)
        self.play(Write(verdict1), run_time=1.0)
        self.wait(0.8)

        saved = tm_text("→ 0 accès base de données", size=26, color=GREEN_TM)
        saved.next_to(verdict1_box, DOWN, buff=0.35)
        self.play(FadeIn(saved, shift=UP * 0.15), run_time=0.8)
        self.wait(3.0)

        self.play(
            FadeOut(typed1), FadeOut(halos1),
            FadeOut(zero_arrow), FadeOut(zero_note),
            FadeOut(verdict1_box), FadeOut(verdict1), FadeOut(saved),
            run_time=0.6
        )
        self.wait(0.5)

        # ── CAS 2 : "john" — positions [1, 2, 8], tous à 1 → peut-être ──
        typed2 = tm_text("john", size=36, color=AUBERGINE, font="Courier")
        typed2.move_to(field_bg.get_center())
        self.play(Write(typed2), run_time=0.9)
        self.wait(0.5)

        john_positions = [1, 2, 8]
        halos2 = VGroup()
        for p in john_positions:
            halo = Square(side_length=0.7, color=YELLOW_TM, stroke_width=4, fill_opacity=0)
            halo.move_to(bits[p].get_center())
            halos2.add(halo)
        self.play(LaggedStart(*[Create(h) for h in halos2], lag_ratio=0.3), run_time=1.0)
        self.wait(0.8)

        verdict2_box = RoundedRectangle(width=6, height=1.4, corner_radius=0.12,
                                        color=YELLOW_TM, stroke_width=3, fill_opacity=0.1)
        verdict2_box.shift(DOWN * 1.2)
        verdict2 = tm_text("peut-être → on vérifie", size=36, color=YELLOW_TM, weight=BOLD)
        verdict2.move_to(verdict2_box.get_center())
        self.play(Create(verdict2_box), run_time=0.6)
        self.play(Write(verdict2), run_time=1.0)
        self.wait(0.8)

        fp_note = tm_text("(faux positif possible — c'est normal)", size=22, color=SLATE)
        fp_note.next_to(verdict2_box, DOWN, buff=0.35)
        self.play(FadeIn(fp_note), run_time=0.7)
        self.wait(2.5)

        self.play(FadeOut(halos2), FadeOut(fp_note), run_time=0.5)

        sql_text = Text("SELECT 1 FROM users\nWHERE username = 'john';",
                        font="Courier", font_size=22, color=SOFT_BLACK)
        sql_box = RoundedRectangle(width=6, height=1.2, corner_radius=0.1,
                                   color=SLATE, stroke_width=2, fill_opacity=0.15)
        sql_box.shift(DOWN * 3.5)
        sql_text.move_to(sql_box.get_center())

        arrow_to_db = Arrow(verdict2_box.get_bottom(), sql_box.get_top(),
                            color=GOLD, stroke_width=3, buff=0.1)
        self.play(GrowArrow(arrow_to_db), run_time=0.7)
        self.play(Create(sql_box), run_time=0.6)
        self.play(Write(sql_text), run_time=1.5)
        self.wait(0.8)

        result = tm_text("→ pseudo pris", size=30, color=RED_TM, weight=BOLD)
        result.next_to(sql_box, DOWN, buff=0.35)
        self.play(FadeIn(result, shift=UP * 0.2), run_time=0.8)
        self.wait(3.0)


# ---------------------------------------------------------------------------
# SCÈNE 5 — WhyItMattersScene
# ---------------------------------------------------------------------------
class WhyItMattersScene(Scene):
    def construct(self):
        make_bg(self)
        title = make_header("Pourquoi ça change tout")
        title.to_edge(UP, buff=0.55)

        col_left_label  = tm_text("sans filtre", size=30, color=RED_TM)
        col_right_label = tm_text("avec filtre", size=30, color=GREEN_TM)
        col_left_label.shift(LEFT * 2.2 + UP * 4.5)
        col_right_label.shift(RIGHT * 2.2 + UP * 4.5)

        req_l = tm_text("requête", size=24, color=SAND).shift(LEFT * 2.2 + UP * 3)
        db_l = RoundedRectangle(width=2.5, height=1, corner_radius=0.1,
                                color=RED_TM, stroke_width=2, fill_opacity=0.2)
        db_l_label = tm_text("base", size=24, color=SAND)
        db_l.shift(LEFT * 2.2 + UP * 1)
        db_l_label.move_to(db_l.get_center())
        arrow_l = Arrow(req_l.get_bottom(), db_l.get_top(), color=RED_TM,
                        stroke_width=2, buff=0.1)

        req_r = tm_text("requête", size=24, color=SAND).shift(RIGHT * 2.2 + UP * 3)
        filt_r = RoundedRectangle(width=2.5, height=0.7, corner_radius=0.08,
                                  color=GOLD, stroke_width=2, fill_opacity=0.2)
        filt_r_label = tm_text("filtre", size=22, color=SAND)
        filt_r.shift(RIGHT * 2.2 + UP * 1.5)
        filt_r_label.move_to(filt_r.get_center())
        db_r = RoundedRectangle(width=2.5, height=0.7, corner_radius=0.08,
                                color=SLATE, stroke_width=2, fill_opacity=0.15)
        db_r_label = tm_text("base", size=22, color=SAND)
        db_r.shift(RIGHT * 2.2 + DOWN * 0.2)
        db_r_label.move_to(db_r.get_center())
        arrow_r1 = Arrow(req_r.get_bottom(), filt_r.get_top(), color=GOLD,
                         stroke_width=2, buff=0.1)
        arrow_r2 = Arrow(filt_r.get_bottom(), db_r.get_top(), color=SLATE,
                         stroke_width=1.5, buff=0.1)
        rare_note = tm_text("(rare)", size=20, color=SLATE)
        rare_note.next_to(arrow_r2, RIGHT, buff=0.1)

        self.play(FadeIn(title), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(col_left_label), FadeIn(col_right_label), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(req_l), FadeIn(req_r), run_time=0.7)
        self.wait(0.3)
        self.play(GrowArrow(arrow_l), GrowArrow(arrow_r1), run_time=0.9)
        self.wait(0.3)
        self.play(Create(db_l), FadeIn(db_l_label),
                  Create(filt_r), FadeIn(filt_r_label), run_time=0.9)
        self.wait(0.5)
        self.play(GrowArrow(arrow_r2), FadeIn(rare_note),
                  Create(db_r), FadeIn(db_r_label), run_time=0.9)
        self.wait(2.0)

        intro_chiffres = tm_text("Exemple concret :", size=30, color=SAND)
        intro_chiffres.next_to(db_r, DOWN, buff=1.6)

        chiffres = VGroup(
            tm_text("1 milliard de comptes à surveiller", size=26, color=GOLD),
            tm_text("1 % de faux positifs tolérés", size=26, color=GOLD),
            tm_text("→ seulement 1,2 Go de RAM", size=26, color=SAND),
            tm_text("    avec 7 fonctions de hachage", size=26, color=SAND),
            tm_text("réponse en ~100 nanosecondes", size=28, color=GREEN_TM, weight=BOLD),
        ).arrange(DOWN, buff=0.28)
        chiffres.next_to(intro_chiffres, DOWN, buff=0.45)

        self.play(FadeIn(intro_chiffres, shift=UP * 0.1), run_time=0.8)
        self.wait(0.8)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chiffres],
                              lag_ratio=0.45), run_time=4.0)
        self.wait(4.0)


# ---------------------------------------------------------------------------
# SCÈNE 6 — OutroScene
# ---------------------------------------------------------------------------
class OutroScene(Scene):
    def construct(self):
        make_bg(self)
        punchline1 = tm_text("Le filtre ne remplace pas la base.", size=42, color=SAND)
        punchline2 = tm_text("Il la protège.", size=48, color=GOLD, weight=BOLD)
        punchline1.shift(UP * 1.5)
        punchline2.next_to(punchline1, DOWN, buff=0.7)

        logo = tm_text("Terre Mathématiques", size=36, color=AUBERGINE, weight=BOLD)
        logo.shift(DOWN * 4)

        self.play(Write(punchline1), run_time=2.0)
        self.wait(1.5)
        self.play(Write(punchline2), run_time=1.8)
        self.wait(1.5)
        self.play(FadeIn(logo, shift=UP * 0.3), run_time=1.0)
        self.wait(4.0)
