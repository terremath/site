"""
================================================================================
  Vidéo : Inégalité de Bienaymé-Tchebychev (extrait formation Bac Éclair)
  Format : portrait 9:16 (TikTok / YouTube Shorts)
================================================================================

  Architecture (7 scènes) :
    Scene01_Titre           (~6s)
    Scene02_PreuveImage     (~26s)  ← LA preuve, visuelle et complète
    Scene03a_TableauVide    (~6s)
    [INSERT TABLETTE]       preuve à la main de E[F_n] et Var(F_n)
    Scene03b_TableauRempli  (~7s)
    Scene04_Application     (~11s)
    Scene05_LoiFaible       (~10s)
    SceneCTA                (~6s)

  Données numériques de la preuve (Scene02) :
    Loi : x = -1.2, -0.6, 0, 0.6, 1.2  avec  p = 0.15, 0.25, 0.20, 0.25, 0.15
    Réordonnée par (x-μ)² décroissant pour le bar chart :
      bar |  p     |  (x-μ)²  |  hors bande ?
        1 | 0.15   |  1.44    |  oui  (or)
        2 | 0.15   |  1.44    |  oui  (or)
        3 | 0.25   |  0.36    |  non  (aubergine)
        4 | 0.25   |  0.36    |  non  (aubergine)
        5 | 0.20   |  0       |  non  (rien)
    ε = 1, ε² = 1.
    q = 0.30 ; Var(X) = 0.612.
================================================================================
"""

from manim import *
import numpy as np

# ========================================================================
# 1. MÉTADONNÉES
# ========================================================================

SCENES = [
    "Scene01_Titre",
    "Scene02_PreuveImage",
    "Scene03a_TableauVide",
    "Scene03b_TableauRempli",
    "Scene04_Application",
    "Scene05_LoiFaible",
    "SceneCTA",
]
OUTPUT_NAME = "bienayme_tchebychev.mp4"
OUTPUT_DIR  = r"media\videos\bienayme_tchebychev\1920p30"

# ========================================================================
# 2. FORMAT PORTRAIT
# ========================================================================

config.frame_width  = 4.5
config.frame_height = 8.0

# ========================================================================
# 3. PALETTE
# ========================================================================

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

# ========================================================================
# 4. TAILLES DE POLICE
# ========================================================================

HEADER_FONT       = 30
TITLE_FONT        = 54
SUBTITLE_FONT     = 38
HOOK_FONT         = 34
BODY_FONT         = 20
BODY_SMALL_FONT   = 17
MATH_FONT         = 30
MATH_SMALL_FONT   = 24

# ========================================================================
# 5. UTILITAIRES
# ========================================================================

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


# ========================================================================
# SCENE 01 — TITRE
# ========================================================================

class Scene01_Titre(Scene):
    def construct(self):
        make_bg(self)

        title = Tex(r"\textbf{Bienaym\'e--Tchebychev}",
                    font_size=46, color=AUBERGINE)
        fit_w(title, 0.86)

        subtitle = Tex(r"De la variance \`a la loi faible",
                       font_size=28, color=GOLD)
        fit_w(subtitle, 0.80)

        sep_w = min(config.frame_width * 0.76,
                    max(title.width, subtitle.width) * 1.06)
        sep = Line(LEFT * sep_w / 2, RIGHT * sep_w / 2,
                   color=GOLD, stroke_width=2)

        author = Tex(r"Terre Math\'ematiques",
                     font_size=26, color=AUBERGINE)
        fit_w(author, 0.70)

        block = VGroup(title, subtitle, sep, author).arrange(
            DOWN, buff=0.40, aligned_edge=ORIGIN
        )

        hook = TLines(
            r"Pas une astuce.",
            r"Une n\'ecessit\'e g\'eom\'etrique.",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.15,
        )
        fit_w(hook, 0.82)

        full = VGroup(block, hook).arrange(DOWN, buff=0.7, aligned_edge=ORIGIN)
        full.move_to(ORIGIN)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.7)
        self.play(Create(sep), FadeIn(author), run_time=0.6)
        self.play(FadeIn(hook, shift=UP * 0.2), run_time=0.7)
        self.wait(2.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ========================================================================
# SCENE 02 — LA PREUVE EN IMAGE
# ========================================================================
# Construction visuelle de Var(X) comme aire totale d'un bar chart
# (largeur p_i, hauteur (x_i-μ)²), puis encastrement du rectangle q·ε²
# sous les barres hors bande. La preuve EST le dessin.
# ========================================================================

class Scene02_PreuveImage(Scene):
    def construct(self):
        make_bg(self)

        header = make_header(r"L'image qui prouve")

        # ── Données ─────────────────────────────────────────
        probs    = [0.15, 0.15, 0.25, 0.25, 0.20]
        sq_devs  = [1.44, 1.44, 0.36, 0.36, 0.00]
        is_out   = [True, True,  False, False, False]
        eps_sq   = 1.0
        q        = probs[0] + probs[1]   # = 0.30

        CHART_W = 3.0
        SCALE_Y = 0.55                    # ε² = 1 → 0.55 unités Manim au-dessus baseline

        # ── Mini distribution ────────────────────────────────
        AXIS_W = 2.4
        BAND_H = 0.28
        x_to = lambda x: x * (AXIS_W / 2.6)

        x_real      = [-1.2, -0.6, 0.0, 0.6, 1.2]
        is_out_real = [True, False, False, False, True]

        axis = Line(LEFT * AXIS_W / 2, RIGHT * AXIS_W / 2,
                    color=SOFT_BLACK, stroke_width=1.2)
        mu_tick = Line(UP * 0.05, DOWN * 0.05,
                       color=AUBERGINE, stroke_width=2)
        mu_lbl = MathTex(r"\mu", font_size=16, color=AUBERGINE)
        mu_lbl.next_to(mu_tick, DOWN, buff=0.04)
        eps_band = Rectangle(
            width=2 * x_to(1.0), height=BAND_H,
            fill_color=RICE_LIGHT, fill_opacity=0.55,
            stroke_color=GOLD, stroke_width=1.0,
        )
        eps_band.move_to(UP * BAND_H / 2)
        dots = VGroup(*[
            Dot([x_to(x), 0, 0], radius=0.07,
                color=GOLD if is_out_real[i] else AUBERGINE)
            for i, x in enumerate(x_real)
        ])
        mini = VGroup(axis, mu_tick, mu_lbl, eps_band, dots)

        # ── Étiquette de définition ──────────────────────────
        def_lbl = MathTex(
            r"\mathrm{Var}(X) \;=\; \sum_i p_i\,(x_i-\mu)^2",
            font_size=22, color=AUBERGINE,
        )
        fit_w(def_lbl, 0.86)

        # ── Bar chart ───────────────────────────────────────
        baseline = Line([-CHART_W / 2, 0, 0], [CHART_W / 2, 0, 0],
                        color=SOFT_BLACK, stroke_width=1.5)

        bars = VGroup()
        cum_x = -CHART_W / 2
        for i in range(5):
            w = probs[i] * CHART_W
            h = sq_devs[i] * SCALE_Y
            if h > 0.01:
                color = GOLD if is_out[i] else AUBERGINE
                bar = Rectangle(
                    width=w, height=h,
                    fill_color=color, fill_opacity=0.55,
                    stroke_color=color, stroke_width=1.4,
                )
                bar.move_to([cum_x + w / 2, h / 2, 0])
                bars.add(bar)
            cum_x += w

        chart = VGroup(baseline, bars)

        # Étiquettes axes
        prob_axis_lbl = MathTex(r"p_i", font_size=18, color=SOFT_BLACK)
        prob_axis_lbl.next_to(baseline, RIGHT, buff=0.08)
        var_axis_lbl = MathTex(r"(x_i-\mu)^2", font_size=16, color=SOFT_BLACK)
        var_axis_lbl.next_to(baseline.get_left(), UP, buff=0.50).shift(LEFT * 0.05)

        chart_full = VGroup(chart, prob_axis_lbl, var_axis_lbl)

        # ── Conclusion symbolique ────────────────────────────
        ccl = MathTex(
            r"q\,\varepsilon^2 \;\leq\; \mathrm{Var}(X)",
            r"\;\;\Longrightarrow\;\;",
            r"q \;\leq\; \dfrac{\mathrm{Var}(X)}{\varepsilon^2}",
            font_size=22, color=AUBERGINE,
        )
        fit_w(ccl, 0.90)

        # ── Centrage global ─────────────────────────────────
        full = VGroup(header, mini, def_lbl, chart_full, ccl).arrange(
            DOWN, buff=0.30, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # ── Éléments relatifs (créés APRÈS move_to) ─────────
        bx_left  = baseline.get_left()
        bx_right = baseline.get_right()
        b_y      = baseline.get_center()[1]

        eps_line = DashedLine(
            [bx_left[0] - 0.08, b_y + eps_sq * SCALE_Y, 0],
            [bx_right[0] + 0.08, b_y + eps_sq * SCALE_Y, 0],
            color=GOLD, stroke_width=2.2, dash_length=0.08,
        )
        eps_line_lbl = MathTex(r"\varepsilon^2", font_size=20, color=GOLD)
        eps_line_lbl.next_to(eps_line.get_right(), UP, buff=0.04)

        q_w = q * CHART_W
        q_h = eps_sq * SCALE_Y
        q_rect = Rectangle(
            width=q_w, height=q_h,
            fill_color=AUBERG_DARK, fill_opacity=0.85,
            stroke_color=AUBERG_DARK, stroke_width=2,
        )
        q_rect.move_to([bx_left[0] + q_w / 2, b_y + q_h / 2, 0])

        q_lbl_rect = MathTex(r"q\,\varepsilon^2",
                             font_size=22, color=SABLE)
        q_lbl_rect.move_to(q_rect.get_center())

        brace_q = Brace(q_rect, DOWN, buff=0.05)
        q_brace_lbl = MathTex(r"q", font_size=18, color=AUBERG_DARK)
        q_brace_lbl.next_to(brace_q, DOWN, buff=0.03)

        # ─────────────────────────────────────────────────
        # ANIMATIONS
        # ─────────────────────────────────────────────────

        self.play(Write(header), run_time=0.6)

        # Phase 1 : mini distribution
        self.play(Create(axis), FadeIn(mu_tick), FadeIn(mu_lbl), run_time=0.5)
        self.play(FadeIn(eps_band), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(d, scale=1.3) for d in dots],
                              lag_ratio=0.10), run_time=0.7)
        self.wait(0.6)

        # Phase 2 : annonce de la définition
        self.play(Write(def_lbl), run_time=1.0)
        self.wait(0.5)

        # Phase 3 : construction du bar chart
        self.play(Create(baseline),
                  FadeIn(prob_axis_lbl),
                  FadeIn(var_axis_lbl),
                  run_time=0.6)
        self.play(LaggedStart(
            *[GrowFromEdge(b, DOWN) for b in bars],
            lag_ratio=0.18,
        ), run_time=1.8)
        self.wait(0.4)

        self.play(Indicate(def_lbl, color=AUBERGINE, scale_factor=1.05),
                  run_time=0.7)
        self.wait(0.4)

        # Phase 4 : ligne ε²
        self.play(Create(eps_line), FadeIn(eps_line_lbl), run_time=0.8)
        self.wait(0.6)

        # Phase 5 : insister sur les barres au-dessus
        self.play(
            Indicate(bars[0], color=GOLD, scale_factor=1.06),
            Indicate(bars[1], color=GOLD, scale_factor=1.06),
            run_time=0.9,
        )
        self.wait(0.5)

        # Phase 6 : LE COUP — rectangle q·ε² s'enchâsse
        self.play(FadeIn(q_rect, scale=0.9), run_time=0.7)
        self.play(FadeIn(q_lbl_rect), run_time=0.4)
        self.play(GrowFromCenter(brace_q), FadeIn(q_brace_lbl), run_time=0.6)
        self.wait(1.5)

        # Phase 7 : conclusion symbolique
        self.play(Write(ccl), run_time=1.4)
        self.wait(3.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ========================================================================
# SCENE 03a — TABLEAU VIDE (avant insert tablette)
# ========================================================================

class Scene03a_TableauVide(Scene):
    def construct(self):
        make_bg(self)

        header = make_header(r"Fr\'equence empirique")

        defn = MathTex(
            r"F_n \;=\; \frac{1}{n}\sum_{i=1}^{n} X_i",
            font_size=MATH_FONT, color=AUBERGINE,
        )
        fit_w(defn, 0.84)

        hyp = Tex(
            r"avec $X_1, \dots, X_n$ i.i.d., m\^eme loi que $X$",
            font_size=BODY_SMALL_FONT, color=SOFT_BLACK,
        )
        fit_w(hyp, 0.84)

        q_esp = MathTex(r"\mathbb{E}[F_n] \;=\; ?",
                        font_size=28, color=AUBERG_DARK)
        q_var = MathTex(r"\mathrm{Var}(F_n) \;=\; ?",
                        font_size=28, color=AUBERG_DARK)
        questions = VGroup(q_esp, q_var).arrange(DOWN, buff=0.35)

        frame = SurroundingRectangle(
            questions, color=GOLD, buff=0.25, stroke_width=2,
            fill_color=RICE_LIGHT, fill_opacity=0.30,
        )
        bloc = VGroup(frame, questions)

        caption = Tex(r"\`A vous de jouer.",
                      font_size=BODY_FONT, color=SOFT_BLACK)

        full = VGroup(header, defn, hyp, bloc, caption).arrange(
            DOWN, buff=0.40, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        self.play(Write(header), run_time=0.7)
        self.play(Write(defn), run_time=0.9)
        self.play(FadeIn(hyp, shift=UP * 0.1), run_time=0.6)
        self.wait(0.8)
        self.play(Create(frame), FadeIn(q_esp), FadeIn(q_var),
                  run_time=0.9)
        self.wait(0.7)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.5)
        self.wait(2.3)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ========================================================================
# SCENE 03b — TABLEAU REMPLI (après insert tablette)
# ========================================================================

class Scene03b_TableauRempli(Scene):
    def construct(self):
        make_bg(self)

        header = make_header(r"Fr\'equence empirique")

        defn = MathTex(
            r"F_n \;=\; \frac{1}{n}\sum_{i=1}^{n} X_i",
            font_size=MATH_FONT, color=AUBERGINE,
        )
        fit_w(defn, 0.84)

        hyp = Tex(
            r"avec $X_1, \dots, X_n$ i.i.d., m\^eme loi que $X$",
            font_size=BODY_SMALL_FONT, color=SOFT_BLACK,
        )
        fit_w(hyp, 0.84)

        a_esp = MathTex(r"\mathbb{E}[F_n] \;=\; \mu",
                        font_size=28, color=AUBERGINE)
        a_var = MathTex(r"\mathrm{Var}(F_n) \;=\; \dfrac{\mathrm{Var}(X)}{n}",
                        font_size=26, color=AUBERGINE)
        answers = VGroup(a_esp, a_var).arrange(DOWN, buff=0.35)

        frame = SurroundingRectangle(
            answers, color=GOLD, buff=0.25, stroke_width=2,
            fill_color=RICE_LIGHT, fill_opacity=0.40,
        )
        bloc = VGroup(frame, answers)

        caption = Tex(
            r"Cas binomial : $\mathrm{Var}(F_n) = \dfrac{p(1-p)}{n}$.",
            font_size=BODY_SMALL_FONT, color=SOFT_BLACK,
        )
        fit_w(caption, 0.86)

        full = VGroup(header, defn, hyp, bloc, caption).arrange(
            DOWN, buff=0.35, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        self.add(header, defn, hyp, frame)
        self.wait(0.2)

        self.play(Write(a_esp), run_time=0.9)
        self.wait(0.5)
        self.play(Write(a_var), run_time=1.1)
        self.wait(1.0)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.6)
        self.wait(2.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ========================================================================
# SCENE 04 — APPLICATION DIRECTE
# ========================================================================

class Scene04_Application(Scene):
    def construct(self):
        make_bg(self)

        header = make_header(r"Application directe")

        bt = MathTex(
            r"\mathbb{P}\!\left(|Y-\mathbb{E}[Y]|\geq\varepsilon\right)",
            r"\;\leq\;",
            r"\dfrac{\mathrm{Var}(Y)}{\varepsilon^2}",
            font_size=22, color=AUBERG_DARK,
        )
        fit_w(bt, 0.86)

        switch = Tex(r"On substitue $Y = F_n$.",
                     font_size=BODY_SMALL_FONT, color=AUBERGINE)

        result = MathTex(
            r"\mathbb{P}\!\left(|F_n - \mu| \geq \varepsilon\right)",
            r"\;\leq\;",
            r"\dfrac{\mathrm{Var}(X)}{n\,\varepsilon^2}",
            font_size=24, color=AUBERGINE,
        )
        fit_w(result, 0.86)

        caption = Tex(r"Sans inspiration. On applique.",
                      font_size=BODY_FONT, color=SOFT_BLACK)

        full = VGroup(header, bt, switch, result, caption).arrange(
            DOWN, buff=0.40, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        rhs = result[2]
        box_rhs = SurroundingRectangle(
            rhs, color=GOLD, buff=0.08,
            stroke_width=2, fill_opacity=0,
        )

        self.play(Write(header), run_time=0.7)
        self.play(Write(bt), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(switch, shift=UP * 0.1), run_time=0.5)
        self.play(Write(result), run_time=1.2)
        self.wait(0.6)
        self.play(
            Create(box_rhs),
            Indicate(rhs, color=GOLD, scale_factor=1.12),
            run_time=0.9,
        )
        self.wait(1.2)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.6)
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ========================================================================
# SCENE 05 — LOI FAIBLE
# ========================================================================

class Scene05_LoiFaible(Scene):
    def construct(self):
        make_bg(self)

        header = make_header(r"Loi faible des grands nombres")

        line1 = MathTex(
            r"\mathbb{P}\!\left(|F_n - \mu|\geq\varepsilon\right)"
            r"\;\leq\;\dfrac{\mathrm{Var}(X)}{n\,\varepsilon^2}",
            font_size=22, color=AUBERG_DARK,
        )
        fit_w(line1, 0.88)

        ccl = MathTex(
            r"\mathbb{P}\!\left(|F_n - \mu|\geq\varepsilon\right)"
            r"\;\xrightarrow[n\to+\infty]{}\;0",
            font_size=24, color=AUBERGINE,
        )
        fit_w(ccl, 0.88)

        end = TLines(
            r"La fr\'equence converge vers $\mu$.",
            r"Vid\'eo compl\`ete sur le site cette semaine.",
            font_size=BODY_SMALL_FONT, color=SOFT_BLACK, buff=0.13,
        )

        full = VGroup(header, line1, ccl, end).arrange(
            DOWN, buff=0.45, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        ccl_box = SurroundingRectangle(
            ccl, color=GOLD, buff=0.15, stroke_width=2,
            fill_color=RICE_LIGHT, fill_opacity=0.30,
        )

        self.play(Write(header), run_time=0.7)
        self.play(Write(line1), run_time=0.9)
        self.wait(1.5)
        self.play(Write(ccl), run_time=1.0)
        self.play(Create(ccl_box), run_time=0.5)
        self.wait(2.0)
        self.play(FadeIn(end, shift=UP * 0.1), run_time=0.7)
        self.wait(3.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ========================================================================
# SCENE CTA
# ========================================================================

class SceneCTA(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        R = 0.52
        try:
            logo = ImageMobject("logo.jpg")
            logo.set_width(R * 2)
            has_image = True
        except Exception:
            logo = Circle(radius=R, color=AUBERGINE,
                          fill_color=AUBERGINE, fill_opacity=0.18,
                          stroke_color=AUBERGINE, stroke_width=2)
            has_image = False

        border = Circle(radius=R + 0.04, color=AUBERGINE,
                        stroke_width=3, fill_opacity=0)
        mask = Cutout(
            Square(side_length=1.6, fill_color=SABLE,
                   fill_opacity=1, stroke_width=0),
            Circle(radius=R),
            fill_color=SABLE, fill_opacity=1, stroke_width=0,
        )
        logo.move_to(ORIGIN)
        border.move_to(ORIGIN)
        mask.move_to(ORIGIN)
        disc_block = Group(logo, border) if has_image else VGroup(logo, border)

        name = Tex(r"\textbf{TERRE MATH\'EMATIQUES}",
                   font_size=34, color=AUBERGINE)
        max_w = config.frame_width * 0.78
        if name.width > max_w:
            name.scale_to_fit_width(max_w)

        w_sep = min(name.width * 1.12, config.frame_width * 0.72)
        sep = Line(LEFT * w_sep / 2, RIGHT * w_sep / 2,
                   color=GOLD, stroke_width=1.4)

        cta = TLines(
            r"Pour des maths",
            r"\textbf{rigoureuses} et",
            r"\textbf{intuitives}.",
            font_size=24, color=SOFT_BLACK, buff=0.15,
        )

        text_block = VGroup(name, sep, cta).arrange(
            DOWN, buff=0.30, aligned_edge=ORIGIN,
        )
        column = Group(disc_block, text_block).arrange(
            DOWN, buff=0.95, aligned_edge=ORIGIN,
        )
        column.move_to(ORIGIN)
        mask.move_to(logo.get_center())

        self.play(FadeIn(logo, scale=1.1), FadeIn(mask),
                  Create(border), run_time=1.0)
        self.play(FadeIn(name), run_time=0.7)
        self.play(Create(sep), run_time=0.5)
        self.play(FadeIn(cta, shift=UP * 0.12), run_time=0.6)

        for _ in range(3):
            self.play(name.animate.scale(1.03),
                      rate_func=there_and_back, run_time=0.7)

        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
