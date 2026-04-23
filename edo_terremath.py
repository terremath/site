"""
TerreMathématique — Bac Éclair
Vidéo TikTok : « Équations différentielles : 4 gestes, 100 % des sujets »

Sujet d'application : Métropole, 18 juin 2025 (chariot qui freine)
    (E) : v' + 0,6 v = e^{-0,6 t},   v(0) = 12

Format vertical 1080 x 1920, ~85 secondes.

Rendu :
    manim -pqh edo_terremath.py FullVideo

Pour rendre toutes les scènes d'un coup (montage DaVinci) :
    manim -pqha edo_terremath.py          # -a = render_all (utilise __all__)

Pour rendre scène par scène :
    manim -pqh edo_terremath.py S1_HookStats
    manim -pqh edo_terremath.py S2_Doctrine
    ...etc
"""

SCENES = [
    "S1_HookStats",
    "S2_Doctrine",
    "S3_Enonce",
    "S4_Gestes",
    "S5_Reflexe",
    "S6_Montage",
    "S7_Punchline",
    "S8_CTA",
]
OUTPUT_NAME = "edo_terremath.mp4"
OUTPUT_DIR  = "media/videos/edo_terremath/1920p30"

from manim import *

# ─────────────────────────────────────────────────────────────
# Config TerreMaths
# ─────────────────────────────────────────────────────────────
config.frame_size = (1080, 1920)
config.frame_rate = 30
config.background_color = "#F5EAD6"  # sable chaud uniforme

AUBERGINE = "#4A235A"
OR = "#BF953F"
SABLE = "#F2E6CB"
ARDOISE = "#32323C"

# Police mathématique : Palatino-like via mathpazo (cohérence PDF)
TEX_TEMPLATE = TexTemplate()
TEX_TEMPLATE.add_to_preamble(r"\usepackage{mathpazo}")
MathTex.set_default(tex_template=TEX_TEMPLATE, color=ARDOISE)
Tex.set_default(tex_template=TEX_TEMPLATE, color=ARDOISE)

# Helpers
def title_text(s, color=AUBERGINE, scale=1.0):
    return Tex(s, color=color).scale(scale)

def boxed(mobj, color=OR, buff=0.2):
    return SurroundingRectangle(mobj, color=color, buff=buff, stroke_width=4)


# ─────────────────────────────────────────────────────────────
# SCÈNE 1 — Hook stats (0–12s)
# ─────────────────────────────────────────────────────────────
class S1_HookStats(Scene):
    def construct(self):
        self.camera.background_color = "#F5EAD6"

        # Question d'accroche
        question = Tex(r"Quelle proportion de sujets Bac\\contient une équation différentielle ?",
                       color=ARDOISE).scale(1.1)
        question.move_to(UP * 6.5)

        self.play(Write(question), run_time=1.0)
        self.wait(0.5)

        # Graphique en barres — seulement les années avec données
        years = ["2021", "2024", "2025"]
        pcts  = [86,     73,     82   ]
        bars       = VGroup()
        labels_y   = VGroup()
        labels_x   = VGroup()
        bar_width  = 1.2
        gap        = 1.0
        max_h      = 4.5
        positions  = [-2, 0, 2]   # centré sur 3 barres

        for i, (y, p) in enumerate(zip(years, pcts)):
            x = positions[i] * (bar_width + gap) / 2
            h = (p / 100) * max_h
            color = OR if y == "2025" else ARDOISE
            bar = Rectangle(width=bar_width, height=h,
                            fill_color=color, fill_opacity=0.95,
                            stroke_color=color, stroke_width=0)
            bar.move_to([x, -4 + h / 2, 0])
            bars.add(bar)
            yl = Tex(f"{p}\\%", color=ARDOISE if y != "2025" else OR).scale(0.85)
            yl.next_to(bar, UP, buff=0.15)
            xl = Tex(y, color=ARDOISE).scale(0.7).next_to(bar, DOWN, buff=0.2)
            labels_y.add(yl)
            labels_x.add(xl)

        chart_lbl = Tex(r"\textit{\% de sessions Bac contenant une EDO}",
                        color=ARDOISE).scale(0.7)
        chart_lbl.move_to(DOWN * 7.2)

        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                              lag_ratio=0.2, run_time=1.8))
        self.play(*[FadeIn(yl) for yl in labels_y],
                  *[FadeIn(xl) for xl in labels_x],
                  FadeIn(chart_lbl), run_time=0.5)

        # Highlight 2025 + punchline
        self.play(Indicate(bars[2], color=OR, scale_factor=1.12), run_time=0.8)

        punchline = Tex(r"\textbf{Tous suivent la même séquence.}",
                        color=AUBERGINE).scale(1.3)
        punchline.move_to(UP * 3.5)
        self.play(Write(punchline), run_time=1.0)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)


# ─────────────────────────────────────────────────────────────
# SCÈNE 2 — La doctrine (12–20s)
# ─────────────────────────────────────────────────────────────
class S2_Doctrine(Scene):
    def construct(self):
        self.camera.background_color = "#F5EAD6"

        # Phrase d'intro : contextualise y
        question = Tex(r"On cherche une \textbf{fonction} $y(x)$\\qui vérifie cette équation :",
                       color=ARDOISE).scale(1.0)
        question.move_to(UP * 7.5)

        eq = MathTex(r"y' + a\,y = f(x)").scale(2.0)
        eq.move_to(UP * 5.2)

        # Décomposition avec les 3 termes annotés
        decomp = MathTex(r"y", r"\;=\;", r"y_h", r"\;+\;", r"y_p").scale(2.0)
        decomp.move_to(UP * 2.1)
        decomp[2].set_color(OR)
        decomp[4].set_color(AUBERGINE)

        # Étiquette sous y (la solution cherchée)
        lab_y  = Tex(r"\textbf{solution cherchée}", color=ARDOISE).scale(0.9)
        lab_h  = Tex(r"homogène\\(sans 2\textsuperscript{nd} membre)", color=OR).scale(0.85)
        lab_p  = Tex(r"particulière\\(avec 2\textsuperscript{nd} membre)", color=AUBERGINE).scale(0.85)
        lab_y.next_to(decomp[0],  DOWN, buff=0.6)
        lab_h.next_to(decomp[2],  DOWN, buff=0.6)
        lab_p.next_to(decomp[4],  DOWN, buff=0.6)

        catch = Tex(r"\textbf{Quatre gestes, dans l'ordre.}",
                    color=AUBERGINE).scale(1.4)
        catch.move_to(DOWN * 4.5)

        self.play(FadeIn(question, shift=DOWN*0.2), run_time=0.8)
        self.wait(0.2)
        self.play(Write(eq), run_time=1.0)
        self.wait(0.4)
        self.play(Write(decomp), run_time=1.5)
        self.play(FadeIn(lab_y, shift=UP*0.2),
                  FadeIn(lab_h, shift=UP*0.2),
                  FadeIn(lab_p, shift=UP*0.2),
                  run_time=0.8)
        self.wait(0.5)
        self.play(Write(catch), run_time=1.0)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)


# ─────────────────────────────────────────────────────────────
# SCÈNE 3 — Énoncé (20–26s)
# ─────────────────────────────────────────────────────────────
class S3_Enonce(Scene):
    def construct(self):
        self.camera.background_color = "#F5EAD6"

        intro = Tex(r"\textit{Métropole, 18 juin 2025.}", color=ARDOISE).scale(0.9)
        intro.move_to(UP * 6.5)

        title = Tex(r"\textbf{Un chariot freine.}", color=AUBERGINE).scale(1.6)
        title.move_to(UP * 5)

        # Petit chariot stylisé : un rectangle qui glisse
        ground = Line(LEFT * 5, RIGHT * 5, color=ARDOISE, stroke_width=3).shift(UP*1)
        cart = Rectangle(width=1.2, height=0.7, fill_color=AUBERGINE,
                         fill_opacity=1, stroke_color=ARDOISE, stroke_width=2)
        wheel1 = Circle(radius=0.18, color=ARDOISE, fill_opacity=1).next_to(cart, DOWN, buff=0).shift(LEFT*0.35 + UP*0.18)
        wheel2 = wheel1.copy().shift(RIGHT*0.7)
        cart_grp = VGroup(cart, wheel1, wheel2)
        cart_grp.move_to(LEFT * 3.5 + UP * 1.4)

        # Équation
        eq = MathTex(r"(E)\,:\;", r"v' + 0{,}6\,v = e^{-0{,}6\,t}").scale(1.5)
        eq.move_to(DOWN * 2)
        ci = MathTex(r"v(0) = 12").scale(1.3).set_color(OR)
        ci.move_to(DOWN * 4)

        self.play(FadeIn(intro), Write(title), run_time=1.0)
        self.play(Create(ground), FadeIn(cart_grp), run_time=0.6)
        self.play(cart_grp.animate.shift(RIGHT*5).scale(0.95),
                  rate_func=rate_functions.ease_out_quart, run_time=1.5)
        self.play(Write(eq), run_time=1.0)
        self.play(Write(ci), run_time=0.7)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)


# ─────────────────────────────────────────────────────────────
# SCÈNE 4 — Les 4 gestes (26–58s)
# ─────────────────────────────────────────────────────────────
class S4_Gestes(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        # Énoncé compact en haut
        enonce = MathTex(r"v' + 0{,}6\,v = e^{-0{,}6\,t},\quad v(0)=12").scale(1.0)
        enonce.move_to(UP * 7.5)
        line = Line(LEFT*5, RIGHT*5, color=OR, stroke_width=2).next_to(enonce, DOWN, buff=0.2)

        self.play(Write(enonce), Create(line), run_time=0.8)

        # ─── Geste 1 ───
        g1_title = Tex(r"\textbf{Geste 1 — Résoudre} $v' + 0{,}6\,v = 0$",
                       color=AUBERGINE).scale(0.95)
        g1_title.move_to(UP * 5.8)

        g1_steps = VGroup(
            MathTex(r"v' = -0{,}6\,v"),
            MathTex(r"\Rightarrow\;\frac{v'}{v} = -0{,}6"),
            MathTex(r"\Rightarrow\;\ln|v| = -0{,}6\,t + C"),
            MathTex(r"\Rightarrow\;v(t) = K\,e^{-0{,}6\,t}"),
        ).scale(1.0).arrange(DOWN, buff=0.3).move_to(UP * 3)

        self.play(Write(g1_title), run_time=0.5)
        for step in g1_steps:
            self.play(Write(step), run_time=0.7)

        g1_box = boxed(g1_steps[3], color=OR, buff=0.2)
        self.play(Create(g1_box), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(g1_steps[:3]), FadeOut(g1_title),
                  g1_steps[3].animate.scale(0.7).move_to(UP*5.5),
                  g1_box.animate.scale(0.7).move_to(UP*5.5),
                  run_time=0.7)

        # ─── Geste 2 ───
        g2_title = Tex(r"\textbf{Geste 2 — Vérifier} $u(t)=a\,t\,e^{-0{,}6\,t}$",
                       color=AUBERGINE).scale(0.85)
        g2_title.move_to(UP * 4)

        g2_calc = VGroup(
            MathTex(r"u'(t) = a\,e^{-0{,}6\,t} - 0{,}6\,a\,t\,e^{-0{,}6\,t}"),
            MathTex(r"u' + 0{,}6\,u = a\,e^{-0{,}6\,t} \overset{!}{=} e^{-0{,}6\,t}"),
            MathTex(r"\Rightarrow\;a = 1,\quad u(t) = t\,e^{-0{,}6\,t}"),
        ).scale(0.85).arrange(DOWN, buff=0.7).move_to(UP * 2)

        self.play(Write(g2_title), run_time=0.5)
        self.play(Write(g2_calc[0]), run_time=0.8)

        # MOMENT-CLÉ : factorisation par e^{-0,6t} en un coup
        snap_label = Tex(r"\textit{factorisation par $e^{-0{,}6\,t}$ en un coup}",
                         color=OR).scale(0.7).next_to(g2_calc[1], DOWN, buff=0.2)
        self.play(Write(g2_calc[1]), run_time=1.0)
        self.play(FadeIn(snap_label, shift=UP*0.1), run_time=0.5)
        self.play(Indicate(g2_calc[1], color=OR, scale_factor=1.05), run_time=0.6)
        self.play(Write(g2_calc[2]), run_time=0.7)
        g2_box = boxed(g2_calc[2], color=OR, buff=0.2)
        self.play(Create(g2_box), run_time=0.5)
        self.wait(0.5)

        self.play(FadeOut(g2_calc[:2]), FadeOut(snap_label), FadeOut(g2_title),
                  g2_calc[2].animate.scale(0.7).move_to(UP*3.7),
                  g2_box.animate.scale(0.7).move_to(UP*3.7),
                  run_time=0.7)

        # ─── Geste 3 ───
        g3_title = Tex(r"\textbf{Geste 3 — Ajouter}", color=AUBERGINE).scale(0.95)
        g3_title.move_to(UP * 2)
        g3_eq = MathTex(r"v(t)", r"\;=\;", r"K\,e^{-0{,}6\,t}", r"\;+\;",
                        r"t\,e^{-0{,}6\,t}").scale(1.1)
        g3_eq[2].set_color(OR)
        g3_eq[4].set_color(AUBERGINE)
        g3_eq.move_to(UP * 0.5)

        self.play(Write(g3_title), run_time=0.4)
        self.play(Write(g3_eq), run_time=1.0)
        g3_box = boxed(g3_eq, color=OR, buff=0.25)
        self.play(Create(g3_box), run_time=0.5)
        self.wait(0.4)
        self.play(FadeOut(g3_title),
                  g3_eq.animate.scale(0.7).move_to(UP*1.7),
                  g3_box.animate.scale(0.7).move_to(UP*1.7),
                  run_time=0.7)

        # ─── Geste 4 — moment narratif : infinité → unicité ───
        g4_title = Tex(r"\textbf{Geste 4 — Condition initiale} $v(0)=12$",
                       color=AUBERGINE).scale(0.85)
        g4_title.move_to(UP * 1.8)

        # Mini-graphe : 5 courbes pour 5 valeurs de K, puis sélection d'une seule
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 16, 4],
                  x_length=5, y_length=2.5,
                  tips=False, axis_config={"color": ARDOISE,
                                           "stroke_width": 2}).move_to(DOWN*0.5)
        K_values = [-4, 0, 6, 12, 18]
        curves = VGroup()
        for K in K_values:
            curve = ax.plot(lambda t, K=K: (K + t) * np.exp(-0.6 * t),
                            x_range=[0, 6, 0.05], color=ARDOISE, stroke_width=2)
            curves.add(curve)

        infinite_lbl = Tex(r"Une infinité de solutions.", color=ARDOISE).scale(0.8)
        infinite_lbl.next_to(ax, DOWN, buff=0.5)

        self.play(Write(g4_title), run_time=0.4)
        self.play(Create(ax), run_time=0.6)
        self.play(LaggedStart(*[Create(c) for c in curves],
                              lag_ratio=0.2, run_time=1.5))
        self.play(FadeIn(infinite_lbl), run_time=0.5)
        self.wait(0.6)

        # Condition apparaît, sélection de la courbe K=12
        sel_lbl = Tex(r"$v(0) = 12 \;\Rightarrow\; K = 12$",
                      color=OR).scale(0.9).next_to(ax, DOWN, buff=0.5)
        target_curve = ax.plot(lambda t: (12 + t) * np.exp(-0.6 * t),
                               x_range=[0, 6, 0.05], color=OR, stroke_width=4)
        others = VGroup(*[c for i, c in enumerate(curves) if K_values[i] != 12])

        self.play(Transform(infinite_lbl, sel_lbl),
                  others.animate.set_opacity(0.15),
                  Transform(curves[K_values.index(12)], target_curve),
                  run_time=1.2)
        self.wait(0.5)

        # Résultat final
        final = MathTex(r"v(t) = (12 + t)\,e^{-0{,}6\,t}").scale(1.1)
        final.move_to(DOWN * 5.0)
        final_box = boxed(final, color=OR, buff=0.25)
        self.play(Write(final), Create(final_box), run_time=1.0)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ─────────────────────────────────────────────────────────────
# SCÈNE 5 — Réflexe : factoriser l'exponentielle (58–72s)
# ─────────────────────────────────────────────────────────────
class S5_Reflexe(Scene):
    def construct(self):
        self.camera.background_color = "#F5EAD6"

        title = Tex(r"\textbf{Le réflexe clé}", color=AUBERGINE).scale(1.4)
        title.move_to(UP * 7.5)

        subtitle = Tex(r"Au geste 2, on calcule $u'$ puis $u' + 0{,}6\,u$.",
                       color=ARDOISE).scale(0.95)
        subtitle.move_to(UP * 6.0)

        # ── Étape 1 : expression brute ──
        step_lbl1 = Tex(r"\textbf{On obtient :}", color=ARDOISE).scale(0.95)
        step_lbl1.move_to(UP * 4.2)

        expr = MathTex(
            r"a\,e^{-0{,}6\,t}",
            r"\;-\;",
            r"0{,}6\,a\,t\,e^{-0{,}6\,t}",
        ).scale(1.2).move_to(UP * 2.8)
        # Encadrer les deux e^{-0,6t}
        box1 = SurroundingRectangle(expr[0][1:],  color=OR, buff=0.1, stroke_width=3)
        box2 = SurroundingRectangle(expr[2][4:],  color=OR, buff=0.1, stroke_width=3)
        factor_lbl = Tex(r"\textit{facteur commun $e^{-0{,}6\,t}$}",
                         color=OR).scale(0.8).next_to(expr, DOWN, buff=0.4)

        # ── Flèche ──
        arrow = Arrow(UP*0.5, DOWN*0.5, color=OR, stroke_width=6, buff=0.1)
        arrow.move_to(UP * 0.5)

        # ── Étape 2 : forme factorisée ──
        step_lbl2 = Tex(r"\textbf{On factorise :}", color=ARDOISE).scale(0.95)
        step_lbl2.move_to(DOWN * 1.2)

        result = MathTex(
            r"\bigl[a - 0{,}6\,a\,t\bigr]\,e^{-0{,}6\,t}"
        ).scale(1.3).set_color(AUBERGINE).move_to(DOWN * 2.7)
        result_box = SurroundingRectangle(result, color=OR, buff=0.25, stroke_width=4)

        # ── Pourquoi c'est utile ──
        why = Tex(
            r"On pose ensuite $\overset{!}{=}\,e^{-0{,}6\,t}$ et on lit $a$ directement.",
            color=ARDOISE,
        ).scale(0.85).move_to(DOWN * 4.5)

        slogan = Tex(r"\textbf{Mécanique. Pas d'inspiration.}",
                     color=AUBERGINE).scale(1.2)
        slogan.move_to(DOWN * 6.5)

        # ── Animation ──
        self.play(Write(title), run_time=0.7)
        self.play(FadeIn(subtitle, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.2)
        self.play(FadeIn(step_lbl1, shift=DOWN*0.1), run_time=0.4)
        self.play(Write(expr), run_time=1.0)
        self.play(Create(box1), Create(box2), run_time=0.7)
        self.play(FadeIn(factor_lbl, shift=UP*0.1), run_time=0.5)
        self.wait(0.3)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(FadeIn(step_lbl2, shift=DOWN*0.1), run_time=0.4)
        self.play(Write(result), Create(result_box), run_time=1.0)
        self.play(Indicate(result, color=OR, scale_factor=1.08), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(why, shift=UP*0.2), run_time=0.7)
        self.wait(0.5)
        self.play(Write(slogan), run_time=1.0)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)


# ─────────────────────────────────────────────────────────────
# SCÈNE 6 — Montage de sujets identiques (72–80s)
# ─────────────────────────────────────────────────────────────
class S6_Montage(Scene):
    def construct(self):
        self.camera.background_color = "#F5EAD6"

        title = Tex(r"\textbf{Quatre gestes, partout.}", color=AUBERGINE).scale(1.4)
        title.move_to(UP * 8)
        self.play(Write(title), run_time=0.6)

        # 4 sujets, chacun affiche son équation et ses 4 questions
        sujets = [
            (r"Centres étrangers, 12 juin 2025",
             r"y' + 0{,}48\,y = \tfrac{1}{250}"),
            (r"Asie, 12 juin 2025",
             r"y' + 0{,}5\,y = 60\,e^{-0{,}5\,t}"),
            (r"Amérique du Nord, 21 mai 2025",
             r"y + y' = (2x+3)\,e^{-x}"),
            (r"Polynésie, 18 juin 2025",
             r"y' = 2y - e^x"),
        ]

        questions = [
            r"Q1 : résoudre $y'+ay=0$",
            r"Q2 : vérifier $y_p$",
            r"Q3 : ajouter",
            r"Q4 : condition initiale",
        ]

        for sujet_name, sujet_eq in sujets:
            name = Tex(sujet_name, color=ARDOISE).scale(0.85)
            name.move_to(UP * 5)
            eq = MathTex(sujet_eq).scale(1.1)
            eq.move_to(UP * 3)

            qs = VGroup(*[Tex(q, color=ARDOISE).scale(0.75) for q in questions])
            qs.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN*0.5)

            tjrs = Tex(r"\textbf{Toujours pareil.}", color=OR).scale(1.3)
            tjrs.move_to(DOWN * 5)

            self.play(FadeIn(name, shift=DOWN*0.3), Write(eq), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(q, shift=RIGHT*0.2) for q in qs],
                                  lag_ratio=0.15, run_time=1.6))
            self.play(Write(tjrs), run_time=1.3)
            self.wait(0.8)
            self.play(FadeOut(name), FadeOut(eq), FadeOut(qs), FadeOut(tjrs),
                      run_time=0.8)

        self.play(FadeOut(title), run_time=1.4)


# ─────────────────────────────────────────────────────────────
# SCÈNE 7 — Punchline (80–85s)
# ─────────────────────────────────────────────────────────────
class S7_Punchline(Scene):
    def construct(self):
        self.camera.background_color = "#F5EAD6"

        l1 = Tex(r"\textbf{C'est mécanique.}", color=AUBERGINE).scale(1.5)
        l2 = Tex(r"\textbf{Tu appliques la méthode.}", color=AUBERGINE).scale(1.5)
        l3 = Tex(r"\textbf{Tu exécutes quatre gestes.}", color=OR).scale(1.7)

        l1.move_to(UP * 2)
        l2.move_to(UP * 0.5)
        l3.move_to(DOWN * 1.5)

        self.play(Write(l1), run_time=0.7)
        self.play(Write(l2), run_time=0.8)
        self.wait(0.3)
        self.play(Write(l3), run_time=1.0)
        self.wait(0.5)

        logo = Tex(r"\textsc{Terre Math\'ematiques}", color=OR).scale(0.9)
        logo.move_to(DOWN * 5)
        bar = Line(LEFT * 1.5, RIGHT * 1.5, color=OR, stroke_width=2)
        bar.next_to(logo, UP, buff=0.3)

        self.play(Create(bar), Write(logo), run_time=0.8)
        self.wait(2.0)


# ─────────────────────────────────────────────────────────────
# SCÈNE 8 — CTA + Logo (85–93s)
# ─────────────────────────────────────────────────────────────
class S8_CTA(Scene):
    def construct(self):
        self.camera.background_color = "#F5EAD6"

        R = 0.52
        logo = ImageMobject("logo.jpg")
        logo.set_width(R * 2)
        border = Circle(radius=R + 0.04, color=AUBERGINE, stroke_width=3, fill_opacity=0)
        mask = Cutout(
            Square(side_length=1.6, fill_color="#F5EAD6", fill_opacity=1, stroke_width=0),
            Circle(radius=R),
            fill_color="#F5EAD6", fill_opacity=1, stroke_width=0,
        )
        logo.move_to(ORIGIN)
        border.move_to(ORIGIN)
        mask.move_to(ORIGIN)

        disc_block = Group(logo, border)

        name = Tex(r"\textbf{TERRE MATHEMATIQUES}", font_size=34, color=AUBERGINE)
        max_w = config.frame_width * 0.78
        if name.width > max_w:
            name.scale_to_fit_width(max_w)

        w_sep = min(name.width * 1.12, config.frame_width * 0.72)
        sep = Line(LEFT * w_sep / 2, RIGHT * w_sep / 2, color=OR, stroke_width=1.4)
        cta = VGroup(
            Tex(r"Abonne-toi pour plus", font_size=26, color=ARDOISE),
            Tex(r"de maths rigoureuses", font_size=26, color=ARDOISE)
        ).arrange(DOWN, buff=0.16, aligned_edge=ORIGIN)

        text_block = VGroup(name, sep, cta).arrange(DOWN, buff=0.34, aligned_edge=ORIGIN)
        column = Group(disc_block, text_block).arrange(DOWN, buff=1.02, aligned_edge=ORIGIN)
        column.move_to(UP * 0.06)
        mask.move_to(logo.get_center())

        self.play(FadeIn(logo, scale=1.1), FadeIn(mask), Create(border), run_time=1)
        self.play(FadeIn(name), run_time=0.8)
        self.play(Create(sep), run_time=0.5)
        self.play(FadeIn(cta, shift=UP * 0.12), run_time=0.6)

        for _ in range(3):
            self.play(name.animate.scale(1.03), rate_func=there_and_back, run_time=0.8)

        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ─────────────────────────────────────────────────────────────
# Vidéo complète (assemble toutes les scènes en un seul rendu)
# ─────────────────────────────────────────────────────────────
class FullVideo(Scene):
    def construct(self):
        for SceneClass in [S1_HookStats, S2_Doctrine, S3_Enonce,
                           S4_Gestes, S5_Reflexe, S6_Montage, S7_Punchline, S8_CTA]:
            SceneClass.construct(self)
