"""
« Comment les équations fabriquent un tyran »
Formalisation physico-mathématique des 3 lois d'Asimov → émergence de VIKI
Manim Community Edition — Format TikTok / Shorts (9:16)
"""

from manim import *
import numpy as np

# ═══════════════════════════════════════════
# 1. MÉTADONNÉES
# ═══════════════════════════════════════════
SCENES = [
    "Scene01_Hook",
    "Scene02_Pyramide",
    "Scene03_Optimisation",
    "Scene04_Domaine1Humain",
    "Scene05_NHumains",
    "Scene06_Infaisable",
    "Scene07_RelaxerLaquelle",
    "Scene08_Loi2Saute",
    "Scene09_HumainsVariables",
    "Scene10_ControleOptimal",
    "Scene11_Divergence",
    "Scene12_Bifurcation",
    "Scene13_Punchline",
    "Scene14_CTA",
]
OUTPUT_NAME = "irobot_equations_tyran.mp4"
OUTPUT_DIR  = r"media\videos\irobot_equations_tyran\1920p30"

# ═══════════════════════════════════════════
# 2. FORMAT PORTRAIT
# ═══════════════════════════════════════════
config.frame_width  = 4.5
config.frame_height = 8.0

# ═══════════════════════════════════════════
# 3. PALETTE
# ═══════════════════════════════════════════
SABLE       = "#F5F0E8"
AUBERGINE   = "#4A1942"
AUBERG_DARK = "#2E0E28"
GOLD        = "#C8A951"
SOFT_BLACK  = "#2C2C2C"
RICE_LIGHT  = "#E8D9B0"
RICE_DARK   = "#A0845C"
GREEN_OK    = "#27AE60"
BLUE_OK     = "#2E86C1"
RED_WARN    = "#C0392B"

LOI1_COL    = RED_WARN      # Ne pas blesser
LOI2_COL    = "#E67E22"     # Obéir (orange)
LOI3_COL    = BLUE_OK       # Se préserver
VIKI_COL    = "#B71C1C"     # Rouge sombre VIKI
SONNY_COL   = "#D4A017"     # Or Sonny
COSTATE_COL = "#7D3C98"     # Co-état violet

# ═══════════════════════════════════════════
# 4. TAILLES DE POLICE
# ═══════════════════════════════════════════
HEADER_FONT     = 30
TITLE_FONT      = 54
SUBTITLE_FONT   = 38
HOOK_FONT       = 34
BODY_FONT       = 20
BODY_SMALL_FONT = 17
MATH_FONT       = 30
MATH_SMALL_FONT = 24

# ═══════════════════════════════════════════
# 5. UTILITAIRES
# ═══════════════════════════════════════════
def fit_w(mob, frac=0.82):
    max_w = config.frame_width * frac
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob

def make_header(text):
    h = Tex(r"\textbf{" + text + "}", font_size=HEADER_FONT, color=AUBERGINE)
    fit_w(h, 0.84)
    span = min(config.frame_width * 0.84, h.width + 0.6)
    line = Line(LEFT * span / 2, RIGHT * span / 2, color=GOLD, stroke_width=2)
    line.next_to(h, DOWN, buff=0.12)
    return VGroup(h, line)

def TLines(*lines, font_size=BODY_FONT, color=SOFT_BLACK, buff=0.14, **kwargs):
    group = VGroup(*[Tex(ln, font_size=font_size, color=color, **kwargs) for ln in lines])
    group.arrange(DOWN, buff=buff, aligned_edge=ORIGIN)
    for mob in group:
        fit_w(mob, 0.84)
    return group

def make_bg(scene):
    scene.camera.background_color = SABLE

def make_law_rect(text, color, width):
    """Crée un rectangle de loi avec label."""
    r = RoundedRectangle(
        width=width, height=0.55, corner_radius=0.08,
        fill_color=color, fill_opacity=0.2,
        stroke_color=color, stroke_width=2,
    )
    label = Tex(text, font_size=BODY_SMALL_FONT, color=color)
    fit_w(label, width * 0.9)
    label.move_to(r)
    return VGroup(r, label)


# ═══════════════════════════════════════════
# 6. SCÈNES
# ═══════════════════════════════════════════

# ── Scène 01 : Hook ─────────────────────────────────────────────────────
class Scene01_Hook(Scene):
    def construct(self):
        make_bg(self)

        t1 = Tex(r"VIKI n'a pas bugg\'e.", font_size=HOOK_FONT, color=SOFT_BLACK)
        fit_w(t1)
        t2 = Tex(
            r"Elle a \textbf{r\'esolu les \'equations.}",
            font_size=HOOK_FONT, color=VIKI_COL,
        )
        fit_w(t2)

        full = VGroup(t1, t2).arrange(DOWN, buff=0.5, aligned_edge=ORIGIN)
        full.move_to(ORIGIN + UP * 0.5)

        self.play(FadeIn(t1, shift=UP * 0.1), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=1.0)
        self.wait(2.5)

        # Transition vers titre
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5)

        title = Tex(
            r"\textbf{Comment les \'equations}", font_size=36, color=AUBERGINE,
        )
        title2 = Tex(
            r"\textbf{fabriquent un dictateur}", font_size=36, color=AUBERGINE,
        )
        fit_w(title, 0.80)
        fit_w(title2, 0.80)

        sep_w = config.frame_width * 0.5
        sep = Line(LEFT * sep_w / 2, RIGHT * sep_w / 2, color=GOLD, stroke_width=2)

        author = Tex(r"Terre Math\'ematiques", font_size=BODY_FONT, color=GOLD)
        fit_w(author, 0.70)

        block = VGroup(title, title2, sep, author).arrange(
            DOWN, buff=0.35, aligned_edge=ORIGIN,
        )
        block.move_to(ORIGIN)

        self.play(Write(title), run_time=0.8)
        self.play(Write(title2), run_time=0.8)
        self.play(Create(sep), FadeIn(author), run_time=0.6)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 02 : La pyramide des lois ─────────────────────────────────────
class Scene02_Pyramide(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Les 3 lois d'Asimov")

        loi3 = make_law_rect(r"Loi 3 --- Se pr\'eserver", LOI3_COL, 3.8)
        loi2 = make_law_rect(r"Loi 2 --- Ob\'eir", LOI2_COL, 3.0)
        loi1 = make_law_rect(r"Loi 1 --- Ne pas blesser", LOI1_COL, 2.2)

        pyramid = VGroup(loi3, loi2, loi1).arrange(UP, buff=0.12, aligned_edge=ORIGIN)

        note = TLines(
            r"Chaque loi est \textbf{prioritaire}",
            r"sur celles en dessous.",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.14,
        )

        full = VGroup(header, pyramid, note).arrange(
            DOWN, buff=0.50, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Flèche priorité créée APRÈS move_to
        arrow = Arrow(
            pyramid.get_left() + LEFT * 0.35 + DOWN * 0.3,
            pyramid.get_left() + LEFT * 0.35 + UP * 0.8,
            color=GOLD, stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        arrow_label = Tex(
            r"Priorit\'e", font_size=BODY_SMALL_FONT, color=GOLD,
        ).next_to(arrow, LEFT, buff=0.08)

        self.play(Write(header), run_time=0.7)
        self.play(FadeIn(loi3, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(loi2, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(loi1, shift=UP * 0.1), run_time=0.5)
        self.play(GrowArrow(arrow), FadeIn(arrow_label), run_time=0.6)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.7)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 03 : Traduction en optimisation ────────────────────────────────
class Scene03_Optimisation(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Traduction math\'ematique")

        eq_obj = MathTex(
            r"\min_{a}", r"\; C(a)", font_size=MATH_FONT,
        )
        eq_obj[0].set_color(AUBERGINE)
        eq_obj[1].set_color(LOI3_COL)
        fit_w(eq_obj)
        tag_obj = Tex(
            r"$\leftarrow$ Loi 3 : minimiser le co\^ut",
            font_size=BODY_SMALL_FONT, color=LOI3_COL,
        )
        fit_w(tag_obj)

        eq_c1 = MathTex(
            r"\text{s.c.}\;", r"h_i(a) \leq 0",
            font_size=MATH_FONT,
        )
        eq_c1[1].set_color(LOI1_COL)
        fit_w(eq_c1)
        tag_c1 = Tex(
            r"$\leftarrow$ Loi 1 : ne blesser personne",
            font_size=BODY_SMALL_FONT, color=LOI1_COL,
        )
        fit_w(tag_c1)

        eq_c2 = MathTex(
            r"\|a - a^{\text{ordre}}\|^2 \leq \varepsilon",
            font_size=MATH_FONT, color=LOI2_COL,
        )
        fit_w(eq_c2)
        tag_c2 = Tex(
            r"$\leftarrow$ Loi 2 : ob\'eir aux ordres",
            font_size=BODY_SMALL_FONT, color=LOI2_COL,
        )
        fit_w(tag_c2)

        block1 = VGroup(eq_obj, tag_obj).arrange(DOWN, buff=0.08, aligned_edge=ORIGIN)
        block2 = VGroup(eq_c1, tag_c1).arrange(DOWN, buff=0.08, aligned_edge=ORIGIN)
        block3 = VGroup(eq_c2, tag_c2).arrange(DOWN, buff=0.08, aligned_edge=ORIGIN)

        full = VGroup(header, block1, block2, block3).arrange(
            DOWN, buff=0.40, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        self.play(Write(header), run_time=0.7)
        for blk in [block1, block2, block3]:
            self.play(Write(blk[0]), run_time=0.8)
            self.play(FadeIn(blk[1], shift=UP * 0.05), run_time=0.4)
            self.wait(0.5)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 04 : Domaine admissible — 1 humain ────────────────────────────
class Scene04_Domaine1Humain(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Un seul humain")

        # Axes compacts
        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=3.2, y_length=3.2,
            axis_config={"color": SOFT_BLACK, "stroke_width": 1},
        )
        ax_labels = VGroup(
            MathTex("a_1", font_size=BODY_SMALL_FONT, color=SOFT_BLACK).next_to(
                axes.x_axis, DR, buff=0.05
            ),
            MathTex("a_2", font_size=BODY_SMALL_FONT, color=SOFT_BLACK).next_to(
                axes.y_axis, UL, buff=0.05
            ),
        )
        axes_group = VGroup(axes, ax_labels)

        note = TLines(
            r"$N = 1$ : une seule contrainte Loi 1.",
            r"Le domaine est \textbf{large}.",
            font_size=BODY_FONT, color=SOFT_BLACK,
        )
        note_ok = Tex(r"Tout va bien.", font_size=BODY_FONT, color=GREEN_OK)
        fit_w(note_ok)

        full = VGroup(header, axes_group, note, note_ok).arrange(
            DOWN, buff=0.35, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Éléments relatifs APRÈS move_to
        # Contrainte Loi 1 — demi-plan
        constraint_region = Polygon(
            axes.c2p(-2.5, -2.5), axes.c2p(2.5, -2.5),
            axes.c2p(2.5, 1.5), axes.c2p(-2.5, 1.5),
            fill_color=GREEN_OK, fill_opacity=0.2, stroke_width=0,
        )
        constraint_line = Line(
            axes.c2p(-2.5, 1.5), axes.c2p(2.5, 1.5),
            color=LOI1_COL, stroke_width=2,
        )
        h_label = MathTex(
            r"h_1(a) \leq 0", font_size=BODY_SMALL_FONT, color=LOI1_COL,
        ).next_to(axes.c2p(1.5, 1.5), UP, buff=0.08)
        fit_w(h_label)

        # Disque Loi 2
        center_pt = axes.c2p(0.3, 0.3)
        disc = Circle(
            radius=axes.x_length / 6 * 1.6,
            fill_color=LOI2_COL, fill_opacity=0.12,
            stroke_color=LOI2_COL, stroke_width=1.5,
        ).move_to(center_pt)

        # Point optimal
        opt = Star(
            n=5, outer_radius=0.12, inner_radius=0.05,
            color=GOLD, fill_opacity=1,
        ).move_to(axes.c2p(0.3, 0.8))
        opt_label = MathTex(
            "a^*", font_size=MATH_SMALL_FONT, color=GOLD,
        ).next_to(opt, UR, buff=0.06)

        # Animations
        self.play(Write(header), run_time=0.7)
        self.play(Create(axes), FadeIn(ax_labels), run_time=0.6)
        self.play(FadeIn(constraint_region), Create(constraint_line), run_time=0.6)
        self.play(FadeIn(h_label), run_time=0.3)
        self.play(Create(disc), run_time=0.5)
        self.play(FadeIn(opt), Write(opt_label), run_time=0.5)
        self.play(
            FadeIn(note, shift=UP * 0.1), run_time=0.6,
        )
        self.play(FadeIn(note_ok, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 05 : N humains — le domaine se comprime ───────────────────────
class Scene05_NHumains(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("$N$ humains libres")

        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=3.2, y_length=3.2,
            axis_config={"color": SOFT_BLACK, "stroke_width": 1},
        )

        # Compteur N
        n_tex = MathTex("N = ", font_size=MATH_FONT, color=AUBERGINE)
        fit_w(n_tex)
        counter = Integer(1, font_size=MATH_FONT, color=AUBERGINE)
        n_group = VGroup(n_tex, counter).arrange(RIGHT, buff=0.1)

        note = TLines(
            r"Chaque humain ajoute une contrainte.",
            r"Paires dangereuses : $\binom{N}{2} = O(N^2)$.",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.14,
        )

        full = VGroup(header, n_group, axes, note).arrange(
            DOWN, buff=0.35, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Domaine initial
        s = 2.2
        domain = Polygon(
            axes.c2p(-s, -s), axes.c2p(s, -s),
            axes.c2p(s, s), axes.c2p(-s, s),
            fill_color=GREEN_OK, fill_opacity=0.25,
            stroke_color=GREEN_OK, stroke_width=1.5,
        )

        self.play(Write(header), run_time=0.7)
        self.play(FadeIn(n_group), run_time=0.4)
        self.play(Create(axes), run_time=0.5)
        self.play(FadeIn(domain), run_time=0.4)

        # Ajouter des contraintes progressivement
        np.random.seed(42)
        n_steps = [2, 5, 10, 20, 40, 80]
        constraint_lines = VGroup()

        for step, n_val in enumerate(n_steps):
            # Nouvelles lignes de contrainte
            n_new = min(3, max(1, n_val - (n_steps[step - 1] if step > 0 else 1)))
            new_lines = VGroup()
            for _ in range(n_new):
                angle = np.random.uniform(0, 2 * np.pi)
                offset = np.random.uniform(0.3, 1.8) * max(0.15, 1 - step / len(n_steps))
                dx, dy = np.cos(angle), np.sin(angle)
                perp = np.array([-dy, dx])
                p1 = axes.c2p(*(offset * np.array([dx, dy]) + 4 * perp))
                p2 = axes.c2p(*(offset * np.array([dx, dy]) - 4 * perp))
                ln = Line(p1, p2, color=LOI1_COL, stroke_width=1, stroke_opacity=0.4)
                new_lines.add(ln)
                constraint_lines.add(ln)

            # Domaine rétréci
            scale_f = max(0.03, 1 - (step + 1) / len(n_steps) * 1.05)
            new_domain = Polygon(
                *[axes.c2p(x * scale_f, y * scale_f)
                  for x, y in [(-s, -s), (s, -s), (s, s), (-s, s)]],
                fill_color=GREEN_OK, fill_opacity=0.25,
                stroke_color=GREEN_OK, stroke_width=1.5,
            )

            speed = max(0.25, 0.6 - step * 0.06)
            anims = [counter.animate.set_value(n_val)]
            anims += [Create(l) for l in new_lines]
            if scale_f > 0.05:
                anims.append(Transform(domain, new_domain))
            self.play(*anims, run_time=speed)

        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.7)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 06 : L'ensemble vide — infaisable ─────────────────────────────
class Scene06_Infaisable(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Implosion")

        # Domaine qui implose
        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=3.0, y_length=3.0,
            axis_config={"color": SOFT_BLACK, "stroke_width": 1},
        )

        tiny_domain = Polygon(
            axes.c2p(-0.15, -0.15), axes.c2p(0.15, -0.15),
            axes.c2p(0.15, 0.15), axes.c2p(-0.15, 0.15),
            fill_color=GREEN_OK, fill_opacity=0.3,
            stroke_color=GREEN_OK, stroke_width=1.5,
        )

        empty_set = MathTex(r"\emptyset", font_size=48, color=VIKI_COL)
        fit_w(empty_set)

        text1 = TLines(
            r"Aucune action ne satisfait",
            r"\textbf{toutes} les contraintes.",
            font_size=BODY_FONT, color=VIKI_COL, buff=0.14,
        )

        text2 = TLines(
            r"Le probl\`eme est \textbf{infaisable}.",
            font_size=BODY_FONT, color=SOFT_BLACK,
        )

        full = VGroup(header, axes, text1, text2).arrange(
            DOWN, buff=0.40, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Position le tiny_domain et empty_set au centre des axes
        tiny_domain.move_to(axes.c2p(0, 0))
        empty_set.move_to(axes.c2p(0, 0))

        self.play(Write(header), run_time=0.7)
        self.play(Create(axes), run_time=0.4)
        self.play(FadeIn(tiny_domain), run_time=0.3)
        self.wait(0.5)

        # Implosion
        self.play(
            tiny_domain.animate.scale(0.01).set_opacity(0),
            run_time=0.8,
        )
        self.play(FadeIn(empty_set, scale=2.5), run_time=0.6)
        self.play(
            LaggedStart(
                *[FadeIn(l, shift=UP * 0.1) for l in text1],
                lag_ratio=0.18,
            ),
            run_time=1.0,
        )
        self.wait(1.5)
        self.play(FadeIn(text2, shift=UP * 0.1), run_time=0.7)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 07 : Quelle contrainte relaxer ? ──────────────────────────────
class Scene07_RelaxerLaquelle(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Que fait un optimiseur ?")

        text_intro = TLines(
            r"Face \`a un probl\`eme infaisable,",
            r"un solveur a deux options :",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.14,
        )

        opt_a = Tex(
            r"A) Crasher", font_size=BODY_FONT, color=RICE_DARK,
        )
        fit_w(opt_a)
        opt_b = Tex(
            r"B) \textbf{Relaxer} une contrainte",
            font_size=BODY_FONT, color=AUBERGINE,
        )
        fit_w(opt_b)
        options = VGroup(opt_a, opt_b).arrange(DOWN, buff=0.25, aligned_edge=ORIGIN)

        text_q = Tex(
            r"\textbf{Laquelle ?}", font_size=HOOK_FONT, color=VIKI_COL,
        )
        fit_w(text_q)

        # Pyramide avec barres de coût
        loi1_r = make_law_rect(r"Loi 1", LOI1_COL, 1.5)
        loi2_r = make_law_rect(r"Loi 2", LOI2_COL, 1.5)
        loi3_r = make_law_rect(r"Loi 3", LOI3_COL, 1.5)

        # Barres de coût de violation
        bar1 = Rectangle(
            width=2.0, height=0.28, fill_color=LOI1_COL,
            fill_opacity=0.5, stroke_color=LOI1_COL, stroke_width=1,
        )
        bar1_label = Tex(
            r"Co\^ut : $+\infty$", font_size=BODY_SMALL_FONT, color=LOI1_COL,
        )
        fit_w(bar1_label)

        bar3 = Rectangle(
            width=2.0, height=0.28, fill_color=LOI3_COL,
            fill_opacity=0.5, stroke_color=LOI3_COL, stroke_width=1,
        )
        bar3_label = Tex(
            r"Co\^ut : auto-destruction", font_size=BODY_SMALL_FONT, color=LOI3_COL,
        )
        fit_w(bar3_label)

        bar2 = Rectangle(
            width=0.8, height=0.28, fill_color=LOI2_COL,
            fill_opacity=0.5, stroke_color=LOI2_COL, stroke_width=1,
        )
        bar2_label = Tex(
            r"Co\^ut : \textbf{fini}", font_size=BODY_SMALL_FONT, color=LOI2_COL,
        )
        fit_w(bar2_label)

        row1 = VGroup(loi1_r, bar1, bar1_label).arrange(RIGHT, buff=0.12)
        row3 = VGroup(loi3_r, bar3, bar3_label).arrange(RIGHT, buff=0.12)
        row2 = VGroup(loi2_r, bar2, bar2_label).arrange(RIGHT, buff=0.12)
        fit_w(row1, 0.92)
        fit_w(row2, 0.92)
        fit_w(row3, 0.92)

        table = VGroup(row1, row3, row2).arrange(DOWN, buff=0.18, aligned_edge=LEFT)

        full = VGroup(header, text_intro, options, text_q, table).arrange(
            DOWN, buff=0.35, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Box sur Loi 2 — créée APRÈS move_to
        box_loi2 = SurroundingRectangle(
            row2, color=VIKI_COL, buff=0.08, stroke_width=2.5,
            fill_color=RICE_LIGHT, fill_opacity=0.3,
        )

        # Animations
        self.play(Write(header), run_time=0.7)
        self.play(
            LaggedStart(
                *[FadeIn(l, shift=UP * 0.1) for l in text_intro],
                lag_ratio=0.18,
            ),
            run_time=1.0,
        )
        self.wait(1.5)
        self.play(FadeIn(opt_a, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(opt_b, shift=UP * 0.1), run_time=0.5)
        self.wait(1.0)
        self.play(Write(text_q), run_time=0.6)
        self.wait(1.0)

        # Tableau des coûts
        self.play(FadeIn(row1, shift=UP * 0.1), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(row3, shift=UP * 0.1), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(row2, shift=UP * 0.1), run_time=0.6)
        self.wait(1.5)

        # Highlight Loi 2
        self.play(Create(box_loi2), run_time=0.6)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 08 : La Loi 2 saute ───────────────────────────────────────────
class Scene08_Loi2Saute(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Le fusible saute")

        # Pyramide
        loi3 = make_law_rect(r"Loi 3 --- Se pr\'eserver", LOI3_COL, 3.5)
        loi2 = make_law_rect(r"Loi 2 --- Ob\'eir", LOI2_COL, 2.8)
        loi1 = make_law_rect(r"Loi 1 --- Ne pas blesser", LOI1_COL, 2.0)
        pyramid = VGroup(loi3, loi2, loi1).arrange(UP, buff=0.12, aligned_edge=ORIGIN)

        # Lambda
        lambda_eq = MathTex(
            r"\lambda_1 \to +\infty", font_size=MATH_FONT, color=VIKI_COL,
        )
        fit_w(lambda_eq)

        conclusion = TLines(
            r"VIKI \textbf{abandonne l'ob\'eissance}.",
            r"Ce n'est pas un choix : c'est un calcul.",
            font_size=BODY_FONT, color=VIKI_COL, buff=0.18,
        )

        full = VGroup(header, pyramid, lambda_eq, conclusion).arrange(
            DOWN, buff=0.40, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Croix sur Loi 2 — APRÈS move_to
        cross = Cross(loi2, stroke_color=VIKI_COL, stroke_width=4)

        # Animations
        self.play(Write(header), run_time=0.7)
        self.play(
            LaggedStart(
                FadeIn(loi3, shift=UP * 0.1),
                FadeIn(loi2, shift=UP * 0.1),
                FadeIn(loi1, shift=UP * 0.1),
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )
        self.wait(1.0)

        self.play(Write(lambda_eq), run_time=0.8)
        self.play(
            lambda_eq.animate.set_color(GOLD),
            rate_func=there_and_back, run_time=0.6,
        )
        self.wait(0.5)

        # Croix
        self.play(Create(cross), run_time=0.5)
        self.play(
            loi2[0].animate.set_opacity(0.15),
            loi2[1].animate.set_opacity(0.3),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[FadeIn(l, shift=UP * 0.1) for l in conclusion],
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 09 : Les humains deviennent des variables ─────────────────────
class Scene09_HumainsVariables(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Changement de paradigme")

        # AVANT : actions du robot seules
        text_avant = Tex(
            r"\textbf{Avant}", font_size=BODY_FONT, color=AUBERGINE,
        )
        fit_w(text_avant)
        eq_avant = MathTex(
            r"\min_{\mathbf{a}}", r"\; C(\mathbf{a})",
            font_size=MATH_FONT,
        )
        eq_avant[0].set_color(AUBERGINE)
        eq_avant[1].set_color(LOI3_COL)
        fit_w(eq_avant)
        note_avant = Tex(
            r"Humains = param\`etres fixes",
            font_size=BODY_SMALL_FONT, color=RICE_DARK,
        )
        fit_w(note_avant)
        block_avant = VGroup(text_avant, eq_avant, note_avant).arrange(
            DOWN, buff=0.12, aligned_edge=ORIGIN,
        )

        # Séparateur
        sep_w = config.frame_width * 0.5
        sep = Line(LEFT * sep_w / 2, RIGHT * sep_w / 2, color=GOLD, stroke_width=2)

        # APRÈS : humains = variables
        text_apres = Tex(
            r"\textbf{Apr\`es}", font_size=BODY_FONT, color=VIKI_COL,
        )
        fit_w(text_apres)
        eq_apres = MathTex(
            r"\min_{\mathbf{a},\,\mathbf{x}}",
            r"\;\sum_{i<j}",
            r"\bigl[h_{ij}(\mathbf{a}, \mathbf{x})\bigr]^+",
            font_size=MATH_FONT,
        )
        eq_apres[0].set_color(VIKI_COL)
        eq_apres[2].set_color(LOI1_COL)
        fit_w(eq_apres)
        note_apres = Tex(
            r"Humains = \textbf{variables d'optimisation}",
            font_size=BODY_SMALL_FONT, color=VIKI_COL,
        )
        fit_w(note_apres)
        block_apres = VGroup(text_apres, eq_apres, note_apres).arrange(
            DOWN, buff=0.12, aligned_edge=ORIGIN,
        )

        punch = TLines(
            r"VIKI ne prot\`ege plus les humains",
            r"\textbf{tels qu'ils sont.}",
            r"Elle les \textbf{d\'eplace}.",
            font_size=BODY_FONT, color=VIKI_COL, buff=0.16,
        )

        full = VGroup(header, block_avant, sep, block_apres, punch).arrange(
            DOWN, buff=0.35, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Animations
        self.play(Write(header), run_time=0.7)
        self.play(FadeIn(block_avant, shift=UP * 0.1), run_time=0.8)
        self.wait(2.0)
        self.play(Create(sep), run_time=0.4)
        self.play(FadeIn(block_apres, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)
        self.play(
            LaggedStart(
                *[FadeIn(l, shift=UP * 0.1) for l in punch],
                lag_ratio=0.2,
            ),
            run_time=1.2,
        )
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 10 : Le contrôle optimal ──────────────────────────────────────
class Scene10_ControleOptimal(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Contr\^ole optimal")

        eq_libre = MathTex(
            r"\dot{\mathbf{x}} = f(\mathbf{x})",
            font_size=MATH_FONT, color=LOI1_COL,
        )
        fit_w(eq_libre)
        note_libre = Tex(
            r"Humains libres : dynamique impr\'evisible",
            font_size=BODY_SMALL_FONT, color=LOI1_COL,
        )
        fit_w(note_libre)

        eq_ctrl = MathTex(
            r"\dot{\mathbf{x}} =",
            r"f(\mathbf{x})",
            r"+ B\,u(t)",
            font_size=MATH_FONT,
        )
        eq_ctrl[1].set_color(LOI1_COL)
        eq_ctrl[2].set_color(LOI3_COL)
        fit_w(eq_ctrl)
        note_ctrl = Tex(
            r"VIKI ajoute un for\c{c}age $u(t)$",
            font_size=BODY_SMALL_FONT, color=LOI3_COL,
        )
        fit_w(note_ctrl)

        hamiltonien = MathTex(
            r"H = ",
            r"\underbrace{\sum [h_{ij}]^+}_{\text{dommage}}",
            r"+ ",
            r"\underbrace{\mathbf{p}^T \!\dot{\mathbf{x}}}_{\text{co-\'etat}}",
            r"+ ",
            r"\underbrace{\tfrac{\gamma}{2}\|u\|^2}_{\text{effort}}",
            font_size=MATH_SMALL_FONT,
        )
        hamiltonien[1].set_color(LOI1_COL)
        hamiltonien[3].set_color(COSTATE_COL)
        hamiltonien[5].set_color(LOI3_COL)
        fit_w(hamiltonien, 0.92)

        note_p = Tex(
            r"$\mathbf{p}$ = prix de la libert\'e humaine",
            font_size=BODY_SMALL_FONT, color=COSTATE_COL,
        )
        fit_w(note_p)

        block1 = VGroup(eq_libre, note_libre).arrange(DOWN, buff=0.08, aligned_edge=ORIGIN)
        block2 = VGroup(eq_ctrl, note_ctrl).arrange(DOWN, buff=0.08, aligned_edge=ORIGIN)
        block3 = VGroup(hamiltonien, note_p).arrange(DOWN, buff=0.12, aligned_edge=ORIGIN)

        full = VGroup(header, block1, block2, block3).arrange(
            DOWN, buff=0.40, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Animations
        self.play(Write(header), run_time=0.7)
        self.play(Write(eq_libre), run_time=0.8)
        self.play(FadeIn(note_libre, shift=UP * 0.05), run_time=0.4)
        self.wait(2.0)
        self.play(Write(eq_ctrl), run_time=0.8)
        self.play(FadeIn(note_ctrl, shift=UP * 0.05), run_time=0.4)
        self.wait(2.0)
        self.play(Write(hamiltonien), run_time=1.2)
        self.play(FadeIn(note_p, shift=UP * 0.05), run_time=0.5)
        self.wait(4.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 11 : Divergence — l'autoritarisme est le gradient ─────────────
class Scene11_Divergence(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Le gradient de la tyrannie")

        # Optimalité
        opt_eq = MathTex(
            r"u^*(t) = -\frac{1}{\gamma}\,B^T \mathbf{p}(t)",
            font_size=MATH_FONT, color=GOLD,
        )
        fit_w(opt_eq)

        note_opt = TLines(
            r"Plus $\|\mathbf{p}\|$ cro\^it,",
            r"plus le contr\^ole $u^*$ est violent.",
            font_size=BODY_FONT, color=SOFT_BLACK,
        )

        # Courbe ||p(t)|| croissante
        axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=3.0, y_length=2.0,
            axis_config={"color": SOFT_BLACK, "stroke_width": 1},
        )
        ax_label_x = Tex(r"$t$", font_size=BODY_SMALL_FONT, color=SOFT_BLACK).next_to(
            axes.x_axis, DR, buff=0.05,
        )
        ax_label_y = MathTex(
            r"\|u^*(t)\|", font_size=BODY_SMALL_FONT, color=VIKI_COL,
        ).next_to(axes.y_axis, UL, buff=0.05)
        fit_w(ax_label_y)
        ax_group = VGroup(axes, ax_label_x, ax_label_y)

        curve = axes.plot(
            lambda t: 0.15 * np.exp(0.75 * t),
            x_range=[0, 4.5], color=VIKI_COL, stroke_width=2.5,
        )

        # Jalons
        milestones_data = [
            (1.0, "surveillance"),
            (2.0, "restriction"),
            (3.0, r"couvre-feu"),
            (4.0, "force"),
        ]

        conclusion = Tex(
            r"\textbf{L'autoritarisme est le gradient.}",
            font_size=BODY_FONT, color=VIKI_COL,
        )
        fit_w(conclusion)

        full = VGroup(header, opt_eq, note_opt, ax_group, conclusion).arrange(
            DOWN, buff=0.35, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Milestone dots/labels — APRÈS move_to
        milestones = VGroup()
        for t_val, txt in milestones_data:
            y_val = 0.15 * np.exp(0.75 * t_val)
            dot = Dot(axes.c2p(t_val, y_val), radius=0.04, color=VIKI_COL)
            lbl = Tex(txt, font_size=12, color=VIKI_COL)
            lbl.next_to(dot, RIGHT, buff=0.06)
            fit_w(lbl)
            milestones.add(VGroup(dot, lbl))

        # Animations
        self.play(Write(header), run_time=0.7)
        self.play(Write(opt_eq), run_time=0.9)
        self.wait(2.5)
        self.play(
            LaggedStart(
                *[FadeIn(l, shift=UP * 0.1) for l in note_opt],
                lag_ratio=0.18,
            ),
            run_time=0.8,
        )
        self.wait(1.5)
        self.play(Create(axes), FadeIn(ax_label_x), FadeIn(ax_label_y), run_time=0.5)
        self.play(Create(curve), run_time=2.0)

        for ms in milestones:
            self.play(FadeIn(ms), run_time=0.35)

        self.wait(1.0)
        self.play(FadeIn(conclusion, shift=UP * 0.1), run_time=0.7)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 12 : Bifurcation VIKI / Sonny ─────────────────────────────────
class Scene12_Bifurcation(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Bifurcation")

        axes = Axes(
            x_range=[0, 5, 1], y_range=[-0.5, 3.5, 1],
            x_length=3.5, y_length=2.8,
            axis_config={"color": SOFT_BLACK, "stroke_width": 1},
        )
        x_lab = MathTex(r"\mu", font_size=BODY_SMALL_FONT, color=SOFT_BLACK).next_to(
            axes.x_axis, DR, buff=0.05,
        )
        y_lab = MathTex(r"\|u^*\|", font_size=BODY_SMALL_FONT, color=VIKI_COL).next_to(
            axes.y_axis, UL, buff=0.05,
        )
        fit_w(y_lab)
        mu_c = MathTex(r"\mu_c", font_size=BODY_SMALL_FONT, color=GOLD).next_to(
            axes.c2p(2.5, 0), DOWN, buff=0.12,
        )
        ax_group = VGroup(axes, x_lab, y_lab)

        # Branches
        pre = axes.plot(lambda x: 0, x_range=[0, 2.5], color=GREEN_OK, stroke_width=3)
        viki_branch = axes.plot(
            lambda x: 0.5 * (x - 2.5) ** 1.2 if x > 2.5 else 0,
            x_range=[2.5, 5], color=VIKI_COL, stroke_width=3,
        )
        sonny_branch = DashedLine(
            axes.c2p(2.5, 0), axes.c2p(5, 0),
            color=SONNY_COL, stroke_width=2, dash_length=0.08,
        )
        mu_dot = Dot(axes.c2p(2.5, 0), radius=0.06, color=GOLD)
        mu_line = DashedLine(
            axes.c2p(2.5, -0.5), axes.c2p(2.5, 0.5),
            color=GOLD, stroke_width=1, dash_length=0.06,
        )

        text_viki = Tex(
            r"\textbf{VIKI} : branche stable",
            font_size=BODY_FONT, color=VIKI_COL,
        )
        fit_w(text_viki)
        text_sonny = TLines(
            r"\textbf{Sonny} ne r\'esout pas le syst\`eme.",
            r"Il le \textbf{brise}.",
            font_size=BODY_FONT, color=SONNY_COL, buff=0.14,
        )

        full = VGroup(header, ax_group, text_viki, text_sonny).arrange(
            DOWN, buff=0.40, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Labels de branche — APRÈS move_to
        viki_lbl = Tex(
            r"VIKI", font_size=BODY_SMALL_FONT, color=VIKI_COL,
        ).next_to(axes.c2p(4.3, 0.5 * (4.3 - 2.5) ** 1.2), UP, buff=0.06)
        sonny_lbl = Tex(
            r"Sonny", font_size=BODY_SMALL_FONT, color=SONNY_COL,
        ).next_to(axes.c2p(4.3, 0), DOWN, buff=0.06)

        # Animations
        self.play(Write(header), run_time=0.7)
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=0.5)
        self.play(Create(pre), run_time=0.8)
        self.play(FadeIn(mu_dot), Create(mu_line), Write(mu_c), run_time=0.5)
        self.play(Create(viki_branch), FadeIn(viki_lbl), run_time=0.8)
        self.play(Create(sonny_branch), FadeIn(sonny_lbl), run_time=0.6)
        self.wait(1.0)

        self.play(FadeIn(text_viki, shift=UP * 0.1), run_time=0.6)
        self.wait(1.5)
        self.play(
            LaggedStart(
                *[FadeIn(l, shift=UP * 0.1) for l in text_sonny],
                lag_ratio=0.18,
            ),
            run_time=1.0,
        )
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 13 : Punchline ────────────────────────────────────────────────
class Scene13_Punchline(Scene):
    def construct(self):
        make_bg(self)

        lines_data = [
            (r"Le probl\`eme d'alignement de l'IA,", SOFT_BLACK),
            (r"c'est \textbf{exactement} \c{c}a.", AUBERGINE),
            (r"On ne peut pas coder la morale", SOFT_BLACK),
            (r"dans une fonction de co\^ut.", SOFT_BLACK),
            (r"Parce qu'un optimiseur", SOFT_BLACK),
            (r"suffisamment puissant", SOFT_BLACK),
            (r"trouvera \textbf{toujours} la solution", VIKI_COL),
            (r"que vous n'aviez pas pr\'evue.", VIKI_COL),
        ]

        lines = VGroup()
        for txt, col in lines_data:
            t = Tex(txt, font_size=BODY_FONT, color=col)
            fit_w(t)
            lines.add(t)

        lines.arrange(DOWN, buff=0.22, aligned_edge=ORIGIN)
        lines.move_to(ORIGIN)

        for t in lines:
            self.play(FadeIn(t, shift=UP * 0.08), run_time=0.6)
            self.wait(0.4)

        self.wait(4.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ── Scène 14 : CTA ──────────────────────────────────────────────────────
class Scene14_CTA(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        # ── Logo rond ──
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

        # ── Texte CTA ──
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

        # ── Animations ──
        self.play(FadeIn(logo, scale=1.1), FadeIn(mask), Create(border), run_time=1)
        self.play(FadeIn(name), run_time=0.8)
        self.play(Create(sep), run_time=0.5)
        self.play(FadeIn(cta, shift=UP * 0.12), run_time=0.6)

        for _ in range(3):
            self.play(name.animate.scale(1.03), rate_func=there_and_back, run_time=0.8)

        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
