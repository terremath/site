# Manim Community Edition
from manim import *
import numpy as np


def TLines(*lines, font_size=48, color=WHITE, buff=0.12, align_center=True, **kwargs):
    """Texte multi-lignes LaTeX ; par défaut centré (lisible en portrait)."""
    group = VGroup(*[Tex(ln, font_size=font_size, color=color, **kwargs) for ln in lines])
    edge = ORIGIN if align_center else LEFT
    return group.arrange(DOWN, buff=buff, aligned_edge=edge)


# ═══════════════════════════════════════════
# MÉTADONNÉES DU PROJET (lues par render_all.bat)
# ═══════════════════════════════════════════
SCENES = [
    "Scene01_Titre",
    "Scene02_Probleme",
    "Scene03_BilanForces",
    "Scene04_OndeImpact",
    "Scene06_PourquoiMoyenne",
    "Scene07_Condition",
    "Scene08_VitesseImpossible",
    "Scene09_Gravite",
    "Scene10_Basilic",
    "Scene11_ForceDivine",
    "Scene12_Conclusion",
    "Scene13_Goethe",
    "Scene14_CTA",
]
OUTPUT_NAME = "marcher_sur_eau_FINAL.mp4"
OUTPUT_DIR  = r"media\videos\jesus_water\1920p30"

# ═══════════════════════════════════════════
# COORDONNÉES PORTRAIT 1080×1920
# ═══════════════════════════════════════════
config.frame_width = 4.5
config.frame_height = 8.0

# ═══════════════════════════════════════════
# PALETTE TERREMATHÉMATIQUES
# ═══════════════════════════════════════════
SABLE       = "#F5F0E8"
AUBERGINE   = "#4A1942"
AUBERG_DARK = "#2E0E28"
GOLD        = "#C8A951"
SOFT_BLACK  = "#2C2C2C"
WATER_DARK  = "#1B4F72"
WATER_LIGHT = "#5DADE2"
RED         = "#C0392B"
GREEN       = "#27AE60"
ORANGE      = "#E67E22"
PURPLE      = "#7D3C98"
LIGHT_BLUE  = "#2E86C1"

# ═══════════════════════════════════════════
# TYPO & ZONES (portrait 4.5 × 8) — titres lisibles, cadre rempli
# ═══════════════════════════════════════════
HEADER_FONT = 32
HEADER_BUFF = 0.55
TITLE_FONT = 56
SUBTITLE_FONT = 44
SCENE_HOOK_FONT = 34
BODY_FONT = 17
BODY_FONT_SMALL = 15
MATH_DISPLAY_FONT = 30
MATH_INLINE_FONT = 26


# ═══════════════════════════════════════════
# UTILITAIRES
# ═══════════════════════════════════════════
def make_header(text, font_size=None):
    fs = font_size if font_size is not None else HEADER_FONT
    h = Tex(r"\textbf{" + text + "}", font_size=fs, color=AUBERGINE)
    fit_mobject_width(h, fraction_of_frame=0.82)
    h.to_edge(UP, buff=HEADER_BUFF)
    span = min(config.frame_width * 0.82, max(h.width + 0.4, 2.8))
    line = Line(LEFT * span / 2, RIGHT * span / 2, color=GOLD, stroke_width=2)
    line.next_to(h, DOWN, buff=0.14)
    return VGroup(h, line)


def fit_mobject_width(mob, fraction_of_frame=0.82):
    max_w = config.frame_width * fraction_of_frame
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob


def make_water_surface(y=-1.0, width=8, n_points=200, amplitude=0.06):
    points = [
        np.array([
            -width/2 + i * width / n_points,
            y + amplitude * np.sin(4 * PI * i / n_points),
            0,
        ])
        for i in range(n_points + 1)
    ]
    wave = VMobject(color=WATER_LIGHT, stroke_width=2)
    wave.set_points_smoothly(points)
    return wave


def make_water_body(y=-1.0, width=8, height=3):
    return Rectangle(
        width=width, height=height,
        fill_color=WATER_DARK, fill_opacity=0.35,
        stroke_width=0,
    ).move_to(DOWN * (abs(y) + height / 2))


def make_silhouette(scale=1.0):
    head = Circle(radius=0.18, color=AUBERGINE, fill_opacity=1, stroke_width=0).move_to(UP * 1.6)
    body = Line(UP * 1.4, UP * 0.4, color=AUBERGINE, stroke_width=3)
    la = Line(UP * 1.2, UP * 0.9 + LEFT * 0.35, color=AUBERGINE, stroke_width=2.5)
    ra = Line(UP * 1.2, UP * 0.9 + RIGHT * 0.35, color=AUBERGINE, stroke_width=2.5)
    ll = Line(UP * 0.4, DOWN * 0.1 + LEFT * 0.25, color=AUBERGINE, stroke_width=2.5)
    rl = Line(UP * 0.4, DOWN * 0.1 + RIGHT * 0.25, color=AUBERGINE, stroke_width=2.5)
    lf = Line(DOWN * 0.1 + LEFT * 0.25, DOWN * 0.1 + LEFT * 0.45, color=AUBERGINE, stroke_width=3)
    rf = Line(DOWN * 0.1 + RIGHT * 0.25, DOWN * 0.1 + RIGHT * 0.45, color=AUBERGINE, stroke_width=3)
    return VGroup(head, body, la, ra, ll, rl, lf, rf).scale(scale)


# ═══════════════════════════════════════════
# SCENE 01 : TITRE
# ═══════════════════════════════════════════
class Scene01_Titre(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        water = make_water_body(y=0.0, height=5)
        wave = make_water_surface(y=0.0)
        self.add(water)
        self.play(Create(wave), run_time=1)

        title = Tex(r"\textbf{Marcher sur l'eau}", font_size=TITLE_FONT, color=AUBERGINE)
        fit_mobject_width(title, 0.76)

        subtitle = TLines(
            r"\'Equations et fondements",
            r"de la physique",
            font_size=SUBTITLE_FONT, color=SOFT_BLACK, buff=0.2,
        )
        fit_mobject_width(subtitle, 0.8)

        bar_w = min(config.frame_width * 0.74, max(title.width, subtitle.width) * 1.06)
        sep = Line(LEFT * bar_w / 2, RIGHT * bar_w / 2, color=GOLD, stroke_width=2)

        author = Tex(r"Terre Math\'ematiques", font_size=38, color=AUBERGINE)
        fit_mobject_width(author, 0.72)

        title_block = VGroup(title, subtitle, sep, author).arrange(
            DOWN, buff=0.42, aligned_edge=ORIGIN,
        )
        title_block.move_to(UP * 2.0)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1)
        self.play(Create(sep), FadeIn(author), run_time=0.8)

        self.play(
            wave.animate.shift(RIGHT * 0.3),
            rate_func=there_and_back, run_time=2,
        )
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCENE 02 : LE PROBLÈME — L'ACCROCHE
# ═══════════════════════════════════════════
class Scene02_Probleme(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        q1 = Tex(r"\textbf{\`A quelle vitesse}", font_size=SCENE_HOOK_FONT, color=AUBERGINE)
        q2 = Tex(r"\textbf{faudrait-il courir}", font_size=SCENE_HOOK_FONT, color=AUBERGINE)
        q3 = Tex(r"\textbf{pour marcher}", font_size=SCENE_HOOK_FONT, color=AUBERGINE)
        q4 = Tex(r"\textbf{sur l'eau ?}", font_size=SCENE_HOOK_FONT + 8, color=GOLD)
        hook = VGroup(q1, q2, q3, q4).arrange(DOWN, buff=0.2, aligned_edge=ORIGIN)
        hook.move_to(UP * 2.0)

        self.play(Write(q1), run_time=0.6)
        self.play(Write(q2), run_time=0.6)
        self.play(Write(q3), run_time=0.6)
        self.play(Write(q4), run_time=0.8)
        self.wait(2)

        teaser = TLines(
            r"Commen\c{c}ons par comprendre",
            r"les forces en jeu.",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.12,
        )
        teaser.move_to(DOWN * 2.35)
        self.play(FadeIn(teaser), run_time=0.6)
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 03 : BILAN DES FORCES
# ═══════════════════════════════════════════
class Scene03_BilanForces(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        header = make_header("Bilan des forces")
        self.play(Write(header), run_time=0.8)

        water_body = make_water_body(y=-0.5, width=10, height=4)
        wave = make_water_surface(y=-0.5, width=10)
        self.play(FadeIn(water_body), Create(wave), run_time=0.8)

        person = make_silhouette(scale=1.0).move_to(UP * 0.8)
        self.play(FadeIn(person, shift=DOWN * 0.3), run_time=0.8)

        center_mass = person.get_center()
        foot_pos = person.get_bottom()

        expl = TLines(
            r"Deux forces verticales",
            r"agissent sur le corps :",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.12,
        ).move_to(UP * 2.38)
        self.play(FadeIn(expl), run_time=0.5)

        w_arrow = Arrow(
            center_mass, center_mass + DOWN * 1.6,
            color=RED, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        w_label = MathTex(r"mg", font_size=22, color=RED).move_to(center_mass + RIGHT * 1.0 + DOWN * 0.5)
        w_desc = Tex(r"poids", font_size=11, color=RED).next_to(w_label, DOWN, buff=0.12)
        self.play(GrowArrow(w_arrow), FadeIn(w_label), FadeIn(w_desc), run_time=0.8)
        self.wait(1.5)

        f_arrow = Arrow(
            foot_pos + DOWN * 0.1, foot_pos + UP * 0.6,
            color=LIGHT_BLUE, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        f_label = MathTex(r"F_{\text{eau}}", font_size=22, color=LIGHT_BLUE).move_to(foot_pos + LEFT * 1.1 + UP * 0.3)
        f_desc = Tex(r"r\'eaction de l'eau", font_size=10, color=LIGHT_BLUE).next_to(f_label, DOWN, buff=0.12)
        self.play(GrowArrow(f_arrow), FadeIn(f_label), FadeIn(f_desc), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(expl), run_time=0.3)
        constat = MathTex(r"F_{\text{eau}} \ll mg", font_size=MATH_DISPLAY_FONT, color=RED).move_to(DOWN * 2.75)
        box = SurroundingRectangle(constat, color=RED, buff=0.12, stroke_width=1.5, corner_radius=0.08)
        self.play(Write(constat), Create(box), run_time=0.8)
        self.wait(2)

        sink_group = VGroup(person, w_arrow, w_label, w_desc, f_arrow, f_label, f_desc)
        self.play(
            sink_group.animate.shift(DOWN * 1.5),
            rate_func=rate_functions.ease_in_cubic, run_time=1.5,
        )

        verdict = Tex(r"Il coule.", font_size=MATH_DISPLAY_FONT + 2, color=RED).move_to(UP * 2.05)
        self.play(FadeIn(verdict, scale=1.3), run_time=0.6)

        question = TLines(
            r"Comment augmenter",
            r"cette force ?",
            font_size=22, color=AUBERGINE, buff=0.1,
        ).move_to(UP * 0.75)
        self.play(FadeIn(question), run_time=0.6)
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 04 : ONDE + PIED (on voit A, v)
# ═══════════════════════════════════════════
class Scene04_OndeImpact(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        header = make_header("Impact du pied sur l'eau")
        self.play(Write(header), run_time=0.8)

        expl = TLines(
            r"En frappant l'eau, le pied",
            r"acc\'el\`ere une masse de fluide.",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.12,
        ).move_to(UP * 2.28)
        self.play(FadeIn(expl), run_time=0.6)

        water_body = make_water_body(y=0, width=10, height=3.5)
        self.add(water_body)

        t_val = ValueTracker(0)
        impact_val = ValueTracker(0)

        def get_wave_pts(t, impact):
            pts = []
            for i in range(201):
                x = -5 + i * 10 / 200
                y_base = 0.04 * np.sin(3 * PI * x - 2 * t)
                r = abs(x)
                damping = np.exp(-0.5 * r)
                y_impact = impact * 0.25 * damping * np.sin(6 * r - 8 * t)
                pts.append(np.array([x, y_base + y_impact, 0]))
            return pts

        wave = VMobject(color=WATER_LIGHT, stroke_width=2.5)
        wave.set_points_smoothly(get_wave_pts(0, 0))

        def wave_upd(mob):
            mob.set_points_smoothly(get_wave_pts(t_val.get_value(), impact_val.get_value()))

        wave.add_updater(wave_upd)
        self.add(wave)

        foot = RoundedRectangle(
            width=0.8, height=0.18, corner_radius=0.04,
            color=AUBERGINE, fill_opacity=0.85, stroke_width=1,
        ).move_to(UP * 1.5)

        a_label = MathTex(r"A", font_size=22, color=ORANGE).next_to(foot, RIGHT, buff=0.5)
        a_desc = Tex(r"surface du pied", font_size=10, color=ORANGE).next_to(a_label, DOWN, buff=0.15)
        self.play(FadeIn(foot), FadeIn(a_label), FadeIn(a_desc), run_time=0.5)

        self.play(
            foot.animate.move_to(DOWN * 0.05),
            a_label.animate.shift(DOWN * 1.55),
            a_desc.animate.shift(DOWN * 1.55),
            run_time=0.4, rate_func=rate_functions.ease_in_quad,
        )

        v_arrow = Arrow(
            foot.get_top() + UP * 0.7, foot.get_top() + UP * 0.05,
            color=GREEN, stroke_width=3, buff=0,
        )
        v_label = MathTex(r"v", font_size=24, color=GREEN).next_to(v_arrow, LEFT, buff=0.4)
        v_desc = Tex(r"vitesse d'impact", font_size=10, color=GREEN).next_to(v_label, DOWN, buff=0.15)
        self.play(GrowArrow(v_arrow), FadeIn(v_label), FadeIn(v_desc), run_time=0.4)

        self.play(
            impact_val.animate.set_value(1),
            t_val.animate.set_value(2),
            run_time=2, rate_func=linear,
        )

        newton_intro = Tex(
            r"D'apr\`es la deuxi\`eme loi de Newton, on a :",
            font_size=BODY_FONT, color=SOFT_BLACK,
        ).move_to(DOWN * 1.8)
        self.play(FadeIn(newton_intro), run_time=0.8)
        self.wait(1)

        eq = MathTex(
            r"F_{\text{impact}} \sim \rho\,A\,v^2",
            font_size=MATH_DISPLAY_FONT, color=GOLD,
        ).move_to(DOWN * 2.55)
        self.play(Write(eq), run_time=0.8)
        self.wait(3)

        self.play(
            t_val.animate.set_value(4),
            impact_val.animate.set_value(0.3),
            run_time=2, rate_func=linear,
        )
        wave.remove_updater(wave_upd)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

# ═══════════════════════════════════════════
# SCENE 06 : POURQUOI LA MOYENNE ?
# ═══════════════════════════════════════════
class Scene06_PourquoiMoyenne(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        header = make_header("Pourquoi la moyenne ?")
        self.play(Write(header), run_time=0.8)

        expl1 = TLines(
            r"Le pied ne touche pas l'eau",
            r"en permanence.",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.12,
        ).move_to(UP * 2.30)
        self.play(FadeIn(expl1), run_time=0.5)

        expl2 = Tex(r"Il frappe \`a une fr\'equence $f$ :", font_size=BODY_FONT, color=PURPLE).next_to(expl1, DOWN, buff=0.22)
        self.play(FadeIn(expl2), run_time=0.4)

        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 1.2, 0.5],
            x_length=3.85, y_length=2.25,
            axis_config={"color": SOFT_BLACK, "stroke_width": 1.2, "include_ticks": False},
            tips=False,
        ).move_to(UP * 0.12)

        t_label = MathTex(r"t", font_size=16, color=SOFT_BLACK).next_to(axes.x_axis, RIGHT, buff=0.1)
        f_label = MathTex(r"F(t)", font_size=16, color=AUBERGINE).next_to(axes.y_axis, UP, buff=0.1)
        self.play(Create(axes), FadeIn(t_label), FadeIn(f_label), run_time=0.8)

        def force_func(t):
            total = 0
            for t0 in [0.5, 1.2, 1.9, 2.6, 3.3]:
                total += np.exp(-20 * (t - t0) ** 2)
            return total

        force_curve = axes.plot(
            force_func, x_range=[0, 4, 0.02],
            color=AUBERGINE, stroke_width=2.5,
        )
        self.play(Create(force_curve), run_time=2)

        brace = BraceBetweenPoints(
            axes.c2p(0.5, -0.15), axes.c2p(1.2, -0.15),
            direction=DOWN, color=PURPLE,
        )
        f_freq = MathTex(r"f", font_size=18, color=PURPLE).next_to(brace, DOWN, buff=0.08)
        self.play(Create(brace), FadeIn(f_freq), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(brace), FadeOut(f_freq), run_time=0.3)

        avg_line = DashedLine(
            axes.c2p(0, 0.35), axes.c2p(4, 0.35),
            color=GOLD, stroke_width=2, dash_length=0.08,
        )
        avg_label = MathTex(r"\overline{F}", font_size=18, color=GOLD).next_to(avg_line, RIGHT, buff=0.1)
        self.play(Create(avg_line), FadeIn(avg_label), run_time=0.8)

        expl3 = TLines(
            r"La force moyenne sur une",
            r"p\'eriode doit compenser le poids :",
            font_size=BODY_FONT_SMALL, color=SOFT_BLACK, buff=0.11,
        ).move_to(DOWN * 1.95)
        self.play(FadeIn(expl3), run_time=0.5)

        eq_int = MathTex(
            r"\frac{1}{T}\int_0^T F(t)\,\mathrm{d}t",
            r"\;\geq\;", r"mg",
            font_size=MATH_DISPLAY_FONT, color=GOLD,
        ).move_to(DOWN * 2.95)
        eq_int[2].set_color(RED)

        box = SurroundingRectangle(eq_int, color=GOLD, buff=0.15, stroke_width=1.5, corner_radius=0.08)
        self.play(Write(eq_int), run_time=1.2)
        self.wait(3)
        self.play(Create(box), run_time=0.4)

        note = Tex(r"$f$ = nombre de pas/seconde", font_size=BODY_FONT_SMALL - 2, color=PURPLE).move_to(DOWN * 3.72)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 07 : LA CONDITION \rhoAv²f ≥ mg
# ═══════════════════════════════════════════
class Scene07_Condition(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        header = make_header("La condition pour marcher")
        self.play(Write(header), run_time=0.8)

        rappel = Tex(r"On a vu :", font_size=BODY_FONT, color=SOFT_BLACK).move_to(UP * 2.50)
        self.play(FadeIn(rappel), run_time=0.3)

        fait1 = Tex(r"(1) Un impact produit $F \sim \rho A v^2$", font_size=BODY_FONT_SMALL, color=AUBERGINE)
        fait2 = Tex(r"(2) Le pied frappe $f$ fois/s", font_size=BODY_FONT_SMALL, color=PURPLE)
        fait3 = Tex(r"(3) La moyenne doit $\geq mg$", font_size=BODY_FONT_SMALL, color=RED)
        faits = VGroup(fait1, fait2, fait3).arrange(DOWN, buff=0.16, aligned_edge=ORIGIN)
        faits.move_to(UP * 1.73)

        self.play(FadeIn(fait1, shift=UP * 0.15), run_time=0.4)
        self.play(FadeIn(fait2, shift=UP * 0.15), run_time=0.4)
        self.play(FadeIn(fait3, shift=UP * 0.15), run_time=0.4)
        self.wait(2)

        donc = Tex(r"\textbf{Donc :}", font_size=22, color=AUBERGINE).move_to(UP * 0.48)
        self.play(FadeIn(donc), run_time=0.3)

        eq1 = MathTex(
            r"\overline{F}", r"\;=\;",
            r"\underbrace{\rho\,A\,v^2}_{\text{un impact}}",
            r"\times",
            r"\underbrace{f}_{\text{fr\'equence}}",
            font_size=26, color=AUBERGINE,
        ).move_to(DOWN * 0.28)
        self.play(Write(eq1), run_time=1.5)
        self.wait(2)

        fleche = MathTex(r"\Downarrow", font_size=28, color=GOLD).move_to(DOWN * 1.3)
        self.play(Write(fleche), run_time=0.3)

        eq_final = MathTex(
            r"\rho \, A \, v^2 \, f \;\geq\; m \, g",
            font_size=34, color=GOLD,
        ).move_to(DOWN * 2.15)

        box = SurroundingRectangle(eq_final, color=AUBERGINE, buff=0.18, stroke_width=2, corner_radius=0.1)
        self.play(Write(eq_final), run_time=1)
        self.wait(3)
        self.play(Create(box), run_time=0.5)

        label = TLines(
            r"Condition n\'ecessaire pour",
            r"marcher sur l'eau",
            font_size=BODY_FONT_SMALL, color=AUBERGINE, buff=0.1,
        ).next_to(box, DOWN, buff=0.2)
        self.play(FadeIn(label), run_time=0.4)
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 08 : VITESSE HORS D'ATTEINTE
# ═══════════════════════════════════════════
class Scene08_VitesseImpossible(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        header = make_header("Vitesse hors d'atteinte")
        self.play(Write(header), run_time=0.8)

        rappel = MathTex(r"\rho\,A\,v^2\,f \;\geq\; mg", font_size=MATH_INLINE_FONT, color=GOLD).move_to(UP * 2.48)
        self.play(Write(rappel), run_time=0.5)

        iso = Tex(r"On isole la vitesse minimale :", font_size=BODY_FONT, color=SOFT_BLACK).move_to(UP * 2.05)
        self.play(FadeIn(iso), run_time=0.4)

        eq_umin = MathTex(
            r"u_{\min} \;\simeq\;",
            r"\sqrt{\frac{m\,g}{\rho\,A\,f}}",
            font_size=36, color=GOLD,
        ).move_to(UP * 1.15)
        self.play(Write(eq_umin), run_time=1.2)
        self.wait(2)

        intro = Tex(r"Prenons un homme standard :", font_size=BODY_FONT, color=AUBERGINE).move_to(UP * 0.15)
        self.play(FadeIn(intro), run_time=0.4)

        vals = [
            (r"m = 75 \text{ kg}", r"masse", LIGHT_BLUE),
            (r"A = 0{,}02 \text{ m}^2", r"surface d'un pied", ORANGE),
            (r"f = 3\text{--}5 \text{ Hz}", r"fr\'equence de pas", PURPLE),
        ]
        vg = VGroup()
        for tex, desc, col in vals:
            s = MathTex(tex, font_size=18, color=col)
            d = Tex(desc, font_size=BODY_FONT_SMALL - 2, color=col)
            row = VGroup(s, d).arrange(RIGHT, buff=0.14)
            vg.add(row)
        vg.arrange(DOWN, buff=0.14, aligned_edge=ORIGIN).move_to(DOWN * 0.68)

        for v in vg:
            self.play(FadeIn(v, shift=RIGHT * 0.15), run_time=0.35)
        self.wait(1)

        result = MathTex(
            r"u_{\min} \sim 80 \text{ \`a } 110 \text{ km/h}",
            font_size=MATH_DISPLAY_FONT + 2, color=RED,
        ).move_to(DOWN * 1.95)

        flash = Rectangle(width=14, height=10, fill_color=WHITE, fill_opacity=0.1, stroke_width=0)
        self.play(FadeIn(flash, run_time=0.1), FadeOut(flash, run_time=0.3))
        self.play(Write(result), run_time=0.8)
        self.wait(2.5)

        box = SurroundingRectangle(result, color=RED, buff=0.15, stroke_width=2, corner_radius=0.1)
        self.play(Create(box), run_time=0.4)

        bolt = Tex(r"Usain Bolt : 44 km/h", font_size=BODY_FONT_SMALL, color=SOFT_BLACK).move_to(DOWN * 2.85)
        times = MathTex(r"\times\,2", font_size=22, color=RED).next_to(bolt, RIGHT, buff=0.12)
        self.play(FadeIn(bolt), FadeIn(times), run_time=0.5)

        verdict = Tex(r"Impossible pour un humain.", font_size=BODY_FONT + 4, color=RED).move_to(DOWN * 3.42)
        self.play(FadeIn(verdict, shift=UP * 0.15), run_time=0.5)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 09 : RÔLE DE g + GRAPHE
# ═══════════════════════════════════════════
class Scene09_Gravite(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        header = make_header(r"Le r\^ole d\'ecisif de la gravit\'e")
        self.play(Write(header), run_time=0.8)

        eq = MathTex(r"u_{\min} \propto \sqrt{g}", font_size=38, color=GOLD).move_to(UP * 2.35)
        self.play(Write(eq), run_time=1)
        self.wait(2)

        expl = TLines(
            r"Moins de gravit\'e =",
            r"moins de vitesse n\'ecessaire.",
            font_size=BODY_FONT_SMALL, color=SOFT_BLACK, buff=0.1,
        ).move_to(UP * 1.52)
        self.play(FadeIn(expl), run_time=0.5)

        axes = Axes(
            x_range=[0, 12, 2], y_range=[0, 130, 20],
            x_length=3.45, y_length=2.75,
            axis_config={"color": SOFT_BLACK, "stroke_width": 1.2, "include_ticks": True, "tick_size": 0.06},
            tips=False,
        ).move_to(DOWN * 0.72)

        x_lab = MathTex(r"g\;\mathrm{(m/s^2)}", font_size=11, color=SOFT_BLACK).next_to(axes.x_axis, DOWN, buff=0.18)
        y_lab = MathTex(r"u_{\min}\;\mathrm{(km/h)}", font_size=11, color=SOFT_BLACK)
        y_lab.rotate(90 * DEGREES).next_to(axes.y_axis, LEFT, buff=0.2)
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=1)

        k = 95 / np.sqrt(9.81)
        curve = axes.plot(lambda g: k * np.sqrt(max(g, 0.01)), x_range=[0.2, 11.5], color=GOLD, stroke_width=3)
        self.play(Create(curve), run_time=2)

        hl = DashedLine(axes.c2p(0, 44), axes.c2p(11.5, 44), color=GREEN, stroke_width=1.5, dash_length=0.08)
        hl_lab = Tex(r"Humain max $\sim$ 44 km/h", font_size=9, color=GREEN).next_to(hl, UP, buff=0.12)
        self.play(Create(hl), FadeIn(hl_lab), run_time=0.8)

        earth = Dot(axes.c2p(9.81, k * np.sqrt(9.81)), color=RED, radius=0.06)
        earth_l = Tex(r"Terre", font_size=10, color=RED).next_to(earth, UP + RIGHT * 0.5, buff=0.1)
        self.play(FadeIn(earth, scale=2), FadeIn(earth_l), run_time=0.5)

        moon = Dot(axes.c2p(1.62, k * np.sqrt(1.62)), color=LIGHT_BLUE, radius=0.06)
        moon_l = Tex(r"Lune", font_size=10, color=LIGHT_BLUE).next_to(moon, RIGHT, buff=0.1)
        self.play(FadeIn(moon, scale=2), FadeIn(moon_l), run_time=0.5)

        titan = Dot(axes.c2p(1.35, k * np.sqrt(1.35)), color=ORANGE, radius=0.05)
        titan_l = Tex(r"Titan", font_size=10, color=ORANGE).next_to(titan, DOWN, buff=0.1)
        self.play(FadeIn(titan), FadeIn(titan_l), run_time=0.4)

        concl = TLines(
            r"Sur la Lune ou Titan,",
            r"un humain pourrait",
            r"marcher sur l'eau.",
            font_size=BODY_FONT_SMALL, color=GREEN, buff=0.1,
        ).move_to(DOWN * 2.82)
        self.play(FadeIn(concl, shift=UP * 0.15), run_time=0.6)
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 10 : BASILIC
# ═══════════════════════════════════════════
class Scene10_Basilic(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        header = make_header("Le basilic : preuve vivante")
        self.play(Write(header), run_time=0.8)

        water_body = make_water_body(y=-0.3, width=14, height=4)
        wave = make_water_surface(y=-0.3, width=14)
        self.add(water_body)
        self.play(Create(wave), run_time=0.5)

        body = Ellipse(width=1.0, height=0.35, color=GREEN, fill_opacity=0.8, stroke_width=1)
        head = Circle(radius=0.13, color=GREEN, fill_opacity=0.8, stroke_width=1)
        head.next_to(body, RIGHT, buff=-0.04)
        tail = Line(body.get_left(), body.get_left() + LEFT * 0.5 + UP * 0.12, color=GREEN, stroke_width=2)
        eye = Dot(head.get_center() + RIGHT * 0.03 + UP * 0.03, radius=0.025, color=AUBERGINE)
        basilisk_body = VGroup(tail, body, head, eye).move_to(LEFT * 4 + UP * 0.1)

        leg1 = Line(ORIGIN, DOWN * 0.3, color=GREEN, stroke_width=2).move_to(body.get_bottom() + LEFT * 0.15 + DOWN * 0.15)
        leg2 = Line(ORIGIN, DOWN * 0.3, color=GREEN, stroke_width=2).move_to(body.get_bottom() + RIGHT * 0.15 + DOWN * 0.15)
        basilisk = VGroup(basilisk_body, leg1, leg2)
        self.play(FadeIn(basilisk), run_time=0.5)

        params_box = RoundedRectangle(
            width=2.0, height=1.6, corner_radius=0.08,
            color=SABLE, fill_opacity=0.9, stroke_color=GOLD, stroke_width=1,
        ).move_to(UP * 1.85 + RIGHT * 0.7)

        ptitle = Tex(r"Basiliscus", font_size=13, color=GOLD)
        pm = MathTex(r"m \approx 0{,}2\text{ kg}", font_size=12, color=LIGHT_BLUE)
        pa = MathTex(r"A \approx 3\text{ cm}^2", font_size=12, color=ORANGE)
        pf = MathTex(r"f \approx 10\text{--}15\text{ Hz}", font_size=12, color=PURPLE)
        pu = MathTex(r"u \approx 1{,}5\text{ m/s}", font_size=12, color=GREEN)
        pc = VGroup(ptitle, pm, pa, pf, pu).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        pc.move_to(params_box.get_center())
        self.play(FadeIn(params_box), FadeIn(pc, lag_ratio=0.1), run_time=0.8)

        for _ in range(8):
            self.play(basilisk.animate.shift(RIGHT * 0.65), run_time=0.1, rate_func=linear)
            sp = Circle(radius=0.04, color=WATER_LIGHT, fill_opacity=0.5, stroke_width=1).move_to(basilisk.get_bottom() + DOWN * 0.04)
            self.add(sp)
            self.play(sp.animate.scale(5).set_opacity(0), run_time=0.12, rate_func=rate_functions.ease_out_quad)
            self.remove(sp)

        eq = MathTex(r"\rho\,A\,v^2\,f \;\geq\; m\,g \;\checkmark", font_size=MATH_INLINE_FONT + 2, color=GOLD).move_to(DOWN * 2.48)
        note = Tex(r"Aucune violation physique.", font_size=BODY_FONT_SMALL, color=SOFT_BLACK).next_to(eq, DOWN, buff=0.22)
        self.play(Write(eq), run_time=0.8)
        self.wait(3)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 11 : FORCE DIVINE
# ═══════════════════════════════════════════
class Scene11_ForceDivine(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        header = make_header("Force divine ?")
        self.play(Write(header), run_time=0.8)

        eq = MathTex(
            r"m\ddot{z}(t)", r"=", r"F_{\text{eau}}(t)", r"+",
            r"F_{\text{divin}}(t)", r"-", r"mg",
            font_size=MATH_INLINE_FONT, color=SOFT_BLACK,
        ).move_to(UP * 2.25)

        self.play(Write(eq[:3]), run_time=1)
        self.wait(1)

        eq[4].set_color(GOLD)
        glow = eq[4].copy().set_color(GOLD).set_opacity(0.3).scale(1.4)
        self.play(Write(eq[3:]), FadeIn(glow, scale=1.5), FadeOut(glow, run_time=1.5), run_time=1.2)
        self.wait(2)

        ok = TLines(
            r"Math\'ematiquement :",
            r"rien ne l'interdit.",
            font_size=BODY_FONT, color=GREEN, buff=0.1,
        ).move_to(UP * 0.68)
        self.play(FadeIn(ok), run_time=0.5)
        self.wait(1)

        mais = Tex(r"Mais\ldots", font_size=28, color=RED).move_to(DOWN * 0.08)
        self.play(FadeIn(mais, scale=1.2), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(mais), FadeOut(ok), run_time=0.3)

        abox = RoundedRectangle(
            width=3.6, height=2.6, corner_radius=0.12,
            color=AUBERGINE, fill_color=SABLE, fill_opacity=0.95, stroke_width=1.5,
        ).move_to(DOWN * 1.5)

        at = Tex(r"\textbf{Axiome de fermeture causale}", font_size=BODY_FONT, color=AUBERGINE)
        at.move_to(abox.get_top() + DOWN * 0.32)
        sep = Line(LEFT * 1.5, RIGHT * 1.5, color=GOLD, stroke_width=0.8).next_to(at, DOWN, buff=0.12)

        criteria = VGroup(
            Tex(r"Locale", font_size=18, color=SOFT_BLACK),
            Tex(r"Universelle", font_size=18, color=SOFT_BLACK),
            Tex(r"Param\'etrable", font_size=18, color=SOFT_BLACK),
            Tex(r"R\'ep\'etable", font_size=18, color=SOFT_BLACK),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).next_to(sep, DOWN, buff=0.18)

        self.play(FadeIn(abox), Write(at), Create(sep), run_time=0.8)
        for c in criteria:
            self.play(FadeIn(c, shift=RIGHT * 0.15), run_time=0.25)
        self.wait(1)

        crosses = VGroup()
        for c in criteria:
            x = MathTex(r"\times", font_size=20, color=RED).next_to(c, LEFT, buff=0.12)
            crosses.add(x)
        self.play(FadeIn(crosses, lag_ratio=0.15), run_time=0.8)
        self.wait(2)

        th = TLines(
            r"Hors du mod\`ele physique.",
            r"Pas logiquement impossible.",
            font_size=BODY_FONT_SMALL, color=GOLD, buff=0.1,
        ).move_to(DOWN * 3.22)
        self.play(FadeIn(th, shift=UP * 0.15), run_time=0.6)
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 12 : CONCLUSION
# ═══════════════════════════════════════════
class Scene12_Conclusion(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        header = make_header("Conclusion")
        self.play(Write(header), run_time=0.8)

        items = [
            (r"Tension de surface",  r"$\times$",        RED),
            (r"Archim\`ede seul",    r"$\times$",        RED),
            (r"Vitesse n\'ecessaire", r"80--110 km/h",   RED),
            (r"Sur la Lune",          r"$\sim$35 km/h",  GREEN),
            (r"Le basilic",           r"$\checkmark$",   GREEN),
            (r"Force divine",         r"hors mod\`ele",  GOLD),
        ]

        labels = []
        vals = []
        for label, val, col in items:
            lbl = Tex(label, font_size=20, color=SOFT_BLACK)
            v = Tex(val, font_size=20, color=col)
            labels.append(lbl)
            vals.append(v)

        lbls_col = VGroup(*labels).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        vals_col = VGroup(*vals).arrange(DOWN, buff=0.35)

        table = VGroup(lbls_col, vals_col).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        table.move_to(UP * 0.1)

        for lbl, v in zip(labels, vals):
            self.play(FadeIn(VGroup(lbl, v), shift=RIGHT * 0.1), run_time=0.3)
            self.wait(0.5)

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        quote = TLines(
            r"L'impossibilit\'e d'\'ecrire",
            r"une \'equation",
            r"n'est pas une",
            r"impossibilit\'e d'existence,",
            r"mais une limite",
            r"structurelle de la loi.",
            font_size=BODY_FONT + 2, color=AUBERGINE, buff=0.14,
        ).move_to(ORIGIN)

        self.play(FadeIn(quote, lag_ratio=0.08), run_time=3)
        box = SurroundingRectangle(quote, color=GOLD, buff=0.2, stroke_width=1.2, corner_radius=0.1)
        self.play(Create(box), run_time=0.8)
        self.wait(4)
        self.play(FadeOut(quote), FadeOut(box), run_time=1)


# ═══════════════════════════════════════════
# SCENE 13 : CITATION GOETHE
# ═══════════════════════════════════════════
class Scene13_Goethe(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        open_q = Tex(r"\guillemotleft", font_size=56, color=GOLD)
        quote = TLines(
            r"Le miracle est",
            r"l'enfant ch\'eri",
            r"de la foi.",
            font_size=28, color=AUBERGINE, buff=0.18,
        )
        close_q = Tex(r"\guillemotright", font_size=56, color=GOLD)
        open_q.next_to(quote, LEFT, buff=0.28, aligned_edge=UP)
        close_q.next_to(quote, RIGHT, buff=0.28, aligned_edge=DOWN)
        quote_block = VGroup(open_q, quote, close_q)
        quote_block.move_to(UP * 0.55)
        self.play(FadeIn(open_q, scale=1.2), run_time=0.5)
        self.play(FadeIn(quote, lag_ratio=0.1), run_time=2)
        self.play(FadeIn(close_q, scale=1.2), run_time=0.35)

        sep = Line(LEFT * 1.35, RIGHT * 1.35, color=GOLD, stroke_width=1.2)
        sep.next_to(quote_block, DOWN, buff=0.55)
        author = Tex(r"Goethe", font_size=24, color=GOLD).next_to(sep, DOWN, buff=0.22)
        self.play(Create(sep), FadeIn(author), run_time=0.8)
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ═══════════════════════════════════════════
# SCENE 14 : CTA + LOGO
# ═══════════════════════════════════════════
class Scene14_CTA(Scene):
    def construct(self):
        self.camera.background_color = SABLE

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

        name = Tex(r"\textbf{TERRE MATHEMATIQUES}", font_size=34, color=AUBERGINE)
        max_w = config.frame_width * 0.78
        if name.width > max_w:
            name.scale_to_fit_width(max_w)

        w_sep = min(name.width * 1.12, config.frame_width * 0.72)
        sep = Line(LEFT * w_sep / 2, RIGHT * w_sep / 2, color=GOLD, stroke_width=1.4)
        cta = TLines(
            r"Abonne-toi pour plus",
            r"de physique rigoureuse",
            font_size=26, color=SOFT_BLACK, buff=0.16,
        )

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
