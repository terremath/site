# Manim Community Edition
from manim import *
import numpy as np

# Force le système de coordonnées portrait 1080×1920
# (Manim garde sinon frame=14.222×25.284 au lieu de 4.5×8)
config.frame_width = 4.5
config.frame_height = 8.0

# ═══════════════════════════════════════════
# PALETTE & CONSTANTES
# ═══════════════════════════════════════════
BG           = "#080820"
GOLD         = "#f4d03f"
SOFT_WHITE   = "#ecf0f1"
LIGHT_BLUE   = "#85c1e9"
WATER_DARK   = "#0e3d5c"
WATER_MID    = "#1a6a9a"
WATER_LIGHT  = "#3498db"
RED          = "#e74c3c"
GREEN        = "#2ecc71"
ORANGE       = "#e67e22"
PURPLE       = "#9b59b6"
DARK_SURFACE = "#1a1a3e"


# ═══════════════════════════════════════════
# UTILITAIRES PARTAGÉS
# ═══════════════════════════════════════════
def make_header(text):
    """En-tête de section doré avec soulignement."""
    h = Text(text, font_size=18, color=GOLD).to_edge(UP, buff=0.4)
    line = Line(
        h.get_left() + DOWN * 0.18,
        h.get_right() + DOWN * 0.18,
        color=GOLD, stroke_width=1.2,
    )
    return VGroup(h, line)


def make_water_surface(y=-1.0, width=8, n_points=200, amplitude=0.06):
    """Crée une ligne d'eau ondulée."""
    points = [
        np.array([
            -width/2 + i * width / n_points,
            y + amplitude * np.sin(4 * PI * i / n_points),
            0
        ])
        for i in range(n_points + 1)
    ]
    wave = VMobject(color=WATER_LIGHT, stroke_width=2)
    wave.set_points_smoothly(points)
    return wave


def make_water_body(y=-1.0, width=8, height=3):
    """Crée le corps d'eau (rectangle bleu semi-transparent)."""
    rect = Rectangle(
        width=width, height=height,
        fill_color=WATER_DARK, fill_opacity=0.5,
        stroke_width=0,
    ).move_to(DOWN * (abs(y) + height / 2))
    return rect


def make_silhouette(scale=1.0):
    """Silhouette humaine simplifiée (stick figure améliorée)."""
    head = Circle(radius=0.18, color=SOFT_WHITE, fill_opacity=1, stroke_width=0)
    head.move_to(UP * 1.6)

    body = Line(UP * 1.4, UP * 0.4, color=SOFT_WHITE, stroke_width=3)

    left_arm = Line(UP * 1.2, UP * 0.9 + LEFT * 0.35, color=SOFT_WHITE, stroke_width=2.5)
    right_arm = Line(UP * 1.2, UP * 0.9 + RIGHT * 0.35, color=SOFT_WHITE, stroke_width=2.5)

    left_leg = Line(UP * 0.4, DOWN * 0.1 + LEFT * 0.25, color=SOFT_WHITE, stroke_width=2.5)
    right_leg = Line(UP * 0.4, DOWN * 0.1 + RIGHT * 0.25, color=SOFT_WHITE, stroke_width=2.5)

    left_foot = Line(
        DOWN * 0.1 + LEFT * 0.25,
        DOWN * 0.1 + LEFT * 0.45,
        color=SOFT_WHITE, stroke_width=3,
    )
    right_foot = Line(
        DOWN * 0.1 + RIGHT * 0.25,
        DOWN * 0.1 + RIGHT * 0.45,
        color=SOFT_WHITE, stroke_width=3,
    )

    person = VGroup(head, body, left_arm, right_arm, left_leg, right_leg, left_foot, right_foot)
    person.scale(scale)
    return person


# ═══════════════════════════════════════════
# SCENE 01 : TITRE
# ═══════════════════════════════════════════
class Scene01_Titre(Scene):
    def construct(self):
        self.camera.background_color = BG

        water = make_water_body(y=0.0, height=5)
        wave = make_water_surface(y=0.0)

        self.add(water)
        self.play(Create(wave), run_time=1)

        title = Text(
            "Marcher sur l'eau",
            font_size=32,
            color=GOLD,
            weight=BOLD,
        ).to_edge(UP, buff=0.4)

        subtitle = Text(
            "Équations et fondements\nde la physique",
            font_size=20,
            color=SOFT_WHITE,
            line_spacing=1.6,
        ).next_to(title, DOWN, buff=0.4)

        sep = Line(LEFT * 1.8, RIGHT * 1.8, color=GOLD, stroke_width=1).next_to(subtitle, DOWN, buff=0.3)

        author = Text(
            "TerreMathématiques",
            font_size=18,
            color=LIGHT_BLUE,
        ).next_to(sep, DOWN, buff=0.3)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1)
        self.play(Create(sep), FadeIn(author), run_time=0.8)

        # Onde douce
        self.play(
            wave.animate.shift(RIGHT * 0.3),
            rate_func=there_and_back,
            run_time=2,
        )
        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCENE 02 : CONDITION MÉCANIQUE (§1)
# ═══════════════════════════════════════════
class Scene02_ConditionMecanique(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = make_header("§1 — Condition mécanique minimale")
        self.play(Write(header), run_time=0.8)

        context = Text(
            "Pour qu'un corps de masse m\nne coule pas, il faut que la force\nverticale moyenne compense le poids :",
            font_size=15,
            color=SOFT_WHITE,
            line_spacing=1.6,
        ).move_to(UP * 1.8)
        self.play(FadeIn(context), run_time=0.8)

        # Équation avec surlignage
        eq = MathTex(
            r"\frac{1}{T}",        # 0
            r"\int_0^T",           # 1
            r"F(t)",               # 2
            r"\,\mathrm{d}t",     # 3
            r"\;\geq\;",          # 4
            r"mg",                 # 5
            font_size=30,
            color=GOLD,
        ).move_to(ORIGIN)

        box = SurroundingRectangle(eq, color=GOLD, buff=0.25, stroke_width=1.5, corner_radius=0.1)

        self.play(Write(eq), run_time=2)
        self.play(Create(box), run_time=0.5)

        # Surligner
        self.play(eq[2].animate.set_color(LIGHT_BLUE), run_time=0.4)
        self.play(eq[5].animate.set_color(RED), run_time=0.4)

        label_f = Text("Force de l'eau", font_size=10, color=LIGHT_BLUE).next_to(eq[2], UP, buff=0.3)
        label_mg = Text("Poids", font_size=10, color=RED).next_to(eq[5], DOWN, buff=0.3)

        self.play(FadeIn(label_f), FadeIn(label_mg), run_time=0.5)
        self.wait(1)

        note = Text(
            "Condition nécessaire,\nindépendante de toute interprétation.",
            font_size=15,
            color=LIGHT_BLUE,
            line_spacing=1.6,
        ).move_to(DOWN * 3.2)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 03 : MODÈLE D'IMPACT (§2)
# ═══════════════════════════════════════════
class Scene03_ModeleImpact(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = make_header("§2 — Modèle d'impact sur l'eau")
        self.play(Write(header), run_time=0.8)

        intro = Text(
            "Lors d'un pas, le pied accélère\nune masse d'eau. Force moyenne :",
            font_size=15,
            color=SOFT_WHITE,
            line_spacing=1.6,
        ).move_to(UP * 2.0)
        self.play(FadeIn(intro), run_time=0.8)

        # Paramètres apparaissant un par un
        params = [
            (r"\rho", "masse volumique", LIGHT_BLUE),
            (r"A", "surface du pied", ORANGE),
            (r"v^2", "vitesse d'impact²", GREEN),
            (r"f", "fréquence des pas", PURPLE),
        ]

        for i, (sym, desc, col) in enumerate(params):
            sym_tex = MathTex(sym, font_size=52, color=col).move_to(UP * 0.2)
            desc_text = Text(desc, font_size=18, color=col).next_to(sym_tex, DOWN, buff=0.3)
            grp = VGroup(sym_tex, desc_text)

            self.play(FadeIn(grp, scale=1.2), run_time=0.5)
            self.wait(0.6)
            self.play(FadeOut(grp), run_time=0.3)

        # Produit final
        self.play(FadeOut(intro), run_time=0.3)

        product = MathTex(
            r"\rho", r"\cdot", r"A", r"\cdot", r"v^2", r"\cdot", r"f",
            font_size=42, color=SOFT_WHITE,
        ).move_to(UP * 0.8)
        product[0].set_color(LIGHT_BLUE)
        product[2].set_color(ORANGE)
        product[4].set_color(GREEN)
        product[6].set_color(PURPLE)

        self.play(FadeIn(product), run_time=0.6)
        self.wait(0.5)

        # Condition complète
        full_eq = MathTex(
            r"\rho \, A \, v^2 \, f \;\geq\; m \, g",
            font_size=42, color=GOLD,
        ).move_to(DOWN * 1.5)

        box = SurroundingRectangle(full_eq, color=RED, buff=0.2, stroke_width=1.5, corner_radius=0.1)
        label = Text("Condition nécessaire", font_size=18, color=RED).next_to(box, DOWN, buff=0.3)

        self.play(
            ReplacementTransform(product, full_eq),
            run_time=1,
        )
        self.play(Create(box), FadeIn(label), run_time=0.6)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 04 : SILHOUETTE + VECTEURS DE FORCES
# ═══════════════════════════════════════════
class Scene04_ForcesAnimees(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = make_header("Bilan des forces")
        self.play(Write(header), run_time=0.8)

        # Eau
        water_body = make_water_body(y=-0.5, width=10, height=4)
        wave = make_water_surface(y=-0.5, width=10)
        self.play(FadeIn(water_body), Create(wave), run_time=0.8)

        # Silhouette
        person = make_silhouette(scale=1.1).move_to(UP * 0.8)
        self.play(FadeIn(person, shift=DOWN * 0.3), run_time=0.8)

        foot_pos = person.get_bottom()
        center_mass = person.get_center()

        # POIDS (rouge, vers le bas)
        weight_arrow = Arrow(
            center_mass,
            center_mass + DOWN * 1.8,
            color=RED, stroke_width=4,
            max_tip_length_to_length_ratio=0.15, buff=0,
        )
        weight_label = MathTex(r"m\vec{g}", font_size=28, color=RED)
        weight_label.next_to(weight_arrow, RIGHT, buff=0.15)

        self.play(GrowArrow(weight_arrow), FadeIn(weight_label), run_time=0.8)
        self.wait(0.5)

        # RÉACTION EAU (bleu, vers le haut, PETITE)
        water_arrow = Arrow(
            foot_pos + DOWN * 0.1,
            foot_pos + UP * 0.7,
            color=LIGHT_BLUE, stroke_width=4,
            max_tip_length_to_length_ratio=0.15, buff=0,
        )
        water_label = MathTex(r"F_{\text{eau}}", font_size=28, color=LIGHT_BLUE)
        water_label.next_to(water_arrow, LEFT, buff=0.15)

        self.play(GrowArrow(water_arrow), FadeIn(water_label), run_time=0.8)
        self.wait(0.5)

        # Comparaison
        comparison = MathTex(
            r"F_{\text{eau}} \ll mg",
            font_size=36, color=RED,
        ).move_to(DOWN * 3.0)
        box = SurroundingRectangle(comparison, color=RED, buff=0.15, stroke_width=1.5, corner_radius=0.08)

        self.play(Write(comparison), Create(box), run_time=0.8)
        self.wait(1)

        # Animation : la personne coule
        sink_group = VGroup(person, weight_arrow, weight_label, water_arrow, water_label)
        self.play(
            sink_group.animate.shift(DOWN * 1.5),
            rate_func=rate_functions.ease_in_cubic,
            run_time=1.5,
        )

        verdict = Text("Il coule.", font_size=32, color=RED).move_to(UP * 2.0)
        self.play(FadeIn(verdict, scale=1.3), run_time=0.6)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 05 : ONDE DE SURFACE (PIED QUI FRAPPE)
# ═══════════════════════════════════════════
class Scene05_OndeEau(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = make_header("Impact du pied sur l'eau")
        self.play(Write(header), run_time=0.8)

        # Surface d'eau
        water_body = make_water_body(y=0, width=10, height=3.5)
        self.add(water_body)

        # Onde paramétrique avec updaters
        t_val = ValueTracker(0)
        impact_val = ValueTracker(0)

        def get_wave_points(t, impact):
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
        wave.set_points_smoothly(get_wave_points(0, 0))

        def wave_updater(mob):
            t = t_val.get_value()
            imp = impact_val.get_value()
            mob.set_points_smoothly(get_wave_points(t, imp))

        wave.add_updater(wave_updater)
        self.add(wave)

        # Pied
        foot = RoundedRectangle(
            width=0.8, height=0.2, corner_radius=0.05,
            color=SOFT_WHITE, fill_opacity=0.9, stroke_width=1,
        ).move_to(UP * 2)

        foot_label = MathTex(r"A \approx 0{,}02\,\text{m}^2", font_size=20, color=ORANGE)
        foot_label.next_to(foot, RIGHT, buff=0.3)

        self.play(FadeIn(foot), FadeIn(foot_label), run_time=0.5)

        # Descente
        self.play(
            foot.animate.move_to(DOWN * 0.05),
            foot_label.animate.shift(DOWN * 2.05),
            run_time=0.4,
            rate_func=rate_functions.ease_in_quad,
        )

        # Vitesse
        v_arrow = Arrow(
            foot.get_top() + UP * 0.6, foot.get_top() + UP * 0.05,
            color=GREEN, stroke_width=3, buff=0,
        )
        v_label = MathTex(r"v", font_size=28, color=GREEN).next_to(v_arrow, LEFT, buff=0.15)
        self.play(GrowArrow(v_arrow), FadeIn(v_label), run_time=0.3)

        # Impact — onde se propage
        self.play(
            impact_val.animate.set_value(1),
            t_val.animate.set_value(2),
            run_time=2,
            rate_func=linear,
        )

        # Équation
        eq = MathTex(r"F \sim \rho\,A\,v^2", font_size=36, color=GOLD).move_to(DOWN * 2.8)
        self.play(Write(eq), run_time=0.8)

        # Continue
        self.play(
            t_val.animate.set_value(4),
            impact_val.animate.set_value(0.3),
            run_time=2,
            rate_func=linear,
        )

        self.wait(1)
        wave.remove_updater(wave_updater)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 06 : VITESSE HORS D'ATTEINTE (§3)
# ═══════════════════════════════════════════
class Scene06_VitesseImpossible(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = make_header("§3 — Vitesse hors d'atteinte")
        self.play(Write(header), run_time=0.8)

        eq_umin = MathTex(
            r"u_{\min}", r"\;\simeq\;",
            r"\sqrt{\frac{m\,g}{\rho\,A\,f}}",
            font_size=42, color=GOLD,
        ).move_to(UP * 2.2)
        self.play(Write(eq_umin), run_time=1.5)
        self.wait(0.8)

        vals = [
            (r"m = 75 \text{ kg}", LIGHT_BLUE),
            (r"A = 0{,}02 \text{ m}^2", ORANGE),
            (r"f = 3\text{--}5 \text{ Hz}", PURPLE),
        ]
        val_mobs = VGroup(*[MathTex(t, font_size=22, color=c) for t, c in vals])
        val_mobs.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(UP * 0.3)

        for v in val_mobs:
            self.play(FadeIn(v, shift=RIGHT * 0.3), run_time=0.4)
        self.wait(0.5)

        # Flash + résultat
        result = MathTex(
            r"u_{\min} \sim 80 \text{ à } 110 \text{ km/h}",
            font_size=34, color=RED,
        ).move_to(DOWN * 1.2)

        flash = Rectangle(
            width=14, height=10,
            fill_color=WHITE, fill_opacity=0.15, stroke_width=0,
        )
        self.play(FadeIn(flash, run_time=0.1), FadeOut(flash, run_time=0.4))
        self.play(Write(result), run_time=0.8)

        box = SurroundingRectangle(result, color=RED, buff=0.2, stroke_width=2, corner_radius=0.1)
        self.play(Create(box), run_time=0.4)

        # Comparaison Bolt
        usain = Text("Usain Bolt : 44 km/h", font_size=22, color=SOFT_WHITE).move_to(DOWN * 2.3)
        times = MathTex(r"\times\,2", font_size=28, color=RED).next_to(usain, RIGHT, buff=0.2)
        self.play(FadeIn(usain), FadeIn(times), run_time=0.6)
        self.wait(0.8)

        verdict = Text("Mécaniquement impossible.", font_size=20, color=RED).move_to(DOWN * 3.3)
        self.play(FadeIn(verdict, shift=UP * 0.2), run_time=0.6)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 07 : GRAPHE u_min vs g (§4)
# ═══════════════════════════════════════════
class Scene07_GrapheGravite(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = make_header("§4 — Le rôle décisif de g")
        self.play(Write(header), run_time=0.8)

        eq_prop = MathTex(r"u_{\min} \propto \sqrt{g}", font_size=44, color=GOLD).move_to(UP * 2.5)
        self.play(Write(eq_prop), run_time=1)
        self.wait(0.5)

        # Axes
        axes = Axes(
            x_range=[0, 12, 2],
            y_range=[0, 130, 20],
            x_length=4.0,
            y_length=3.5,
            axis_config={
                "color": SOFT_WHITE,
                "stroke_width": 1.5,
                "include_ticks": True,
                "tick_size": 0.07,
            },
            tips=False,
        ).move_to(DOWN * 1)

        x_lab = MathTex(r"g\;\text{(m/s}^2\text{)}", font_size=18, color=SOFT_WHITE)
        x_lab.next_to(axes.x_axis, DOWN, buff=0.3)
        y_lab = MathTex(r"u_{\min}\;\text{(km/h)}", font_size=18, color=SOFT_WHITE)
        y_lab.next_to(axes.y_axis, LEFT, buff=0.3).shift(UP * 0.5)

        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=1)

        # Courbe
        k = 95 / np.sqrt(9.81)  # calibré : u_min(9.81) ≈ 95 km/h

        curve = axes.plot(
            lambda g: k * np.sqrt(max(g, 0.01)),
            x_range=[0.2, 11.5],
            color=GOLD, stroke_width=3,
        )
        self.play(Create(curve), run_time=2)

        # Ligne humaine max
        human_line = DashedLine(
            axes.c2p(0, 44), axes.c2p(11.5, 44),
            color=GREEN, stroke_width=1.5, dash_length=0.1,
        )
        human_label = Text("Humain max ~ 44 km/h", font_size=14, color=GREEN)
        human_label.next_to(human_line, UP, buff=0.1).shift(LEFT * 0.5)

        self.play(Create(human_line), FadeIn(human_label), run_time=0.8)

        # Point Terre
        earth_dot = Dot(axes.c2p(9.81, k * np.sqrt(9.81)), color=RED, radius=0.08)
        earth_lab = Text("Terre", font_size=16, color=RED).next_to(earth_dot, UR, buff=0.12)
        self.play(FadeIn(earth_dot, scale=2), FadeIn(earth_lab), run_time=0.5)

        # Point Lune
        moon_dot = Dot(axes.c2p(1.62, k * np.sqrt(1.62)), color=LIGHT_BLUE, radius=0.08)
        moon_lab = Text("Lune", font_size=16, color=LIGHT_BLUE).next_to(moon_dot, UP, buff=0.12)
        self.play(FadeIn(moon_dot, scale=2), FadeIn(moon_lab), run_time=0.5)

        # Point Titan
        titan_dot = Dot(axes.c2p(1.35, k * np.sqrt(1.35)), color=ORANGE, radius=0.06)
        titan_lab = Text("Titan", font_size=14, color=ORANGE).next_to(titan_dot, LEFT, buff=0.12)
        self.play(FadeIn(titan_dot), FadeIn(titan_lab), run_time=0.4)

        # Zone
        zone = Text("Atteignable !", font_size=16, color=GREEN).move_to(axes.c2p(3, 25))
        self.play(FadeIn(zone), run_time=0.6)

        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 08 : BASILIC ANIMÉ (§5)
# ═══════════════════════════════════════════
class Scene08_Basilic(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = make_header("§5 — Le basilic : preuve vivante")
        self.play(Write(header), run_time=0.8)

        # Eau
        water_body = make_water_body(y=-0.3, width=14, height=4)
        wave = make_water_surface(y=-0.3, width=14)
        self.add(water_body)
        self.play(Create(wave), run_time=0.5)

        # Basilic simplifié
        body = Ellipse(width=1.2, height=0.4, color=GREEN, fill_opacity=0.8, stroke_width=1)
        head = Circle(radius=0.15, color=GREEN, fill_opacity=0.8, stroke_width=1)
        head.next_to(body, RIGHT, buff=-0.05)
        tail = Line(body.get_left(), body.get_left() + LEFT * 0.6 + UP * 0.15, color=GREEN, stroke_width=2)

        # Oeil
        eye = Dot(head.get_center() + RIGHT * 0.04 + UP * 0.03, radius=0.03, color=WHITE)

        basilisk_body = VGroup(tail, body, head, eye).move_to(LEFT * 5 + UP * 0.1)

        # Pattes
        leg1 = Line(ORIGIN, DOWN * 0.35, color=GREEN, stroke_width=2)
        leg2 = Line(ORIGIN, DOWN * 0.35, color=GREEN, stroke_width=2)
        leg1.move_to(body.get_bottom() + LEFT * 0.2 + DOWN * 0.175)
        leg2.move_to(body.get_bottom() + RIGHT * 0.2 + DOWN * 0.175)

        basilisk = VGroup(basilisk_body, leg1, leg2)

        self.play(FadeIn(basilisk), run_time=0.5)

        # Paramètres temps réel
        params_box = RoundedRectangle(
            width=2.2, height=2.0, corner_radius=0.1,
            color=DARK_SURFACE, fill_opacity=0.85,
            stroke_color=GOLD, stroke_width=1,
        ).move_to(UP * 2.2 + RIGHT * 0.8)

        params_title = Text("Basiliscus", font_size=16, color=GOLD)
        m_v = MathTex(r"m \approx 0{,}2\text{ kg}", font_size=16, color=LIGHT_BLUE)
        a_v = MathTex(r"A_{\text{patte}} \approx 3\text{ cm}^2", font_size=16, color=ORANGE)
        f_v = MathTex(r"f \approx 10\text{--}15\text{ Hz}", font_size=16, color=PURPLE)
        u_v = MathTex(r"u \approx 1{,}5\text{ m/s}", font_size=16, color=GREEN)

        params_content = VGroup(params_title, m_v, a_v, f_v, u_v).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        params_content.move_to(params_box.get_center())

        self.play(FadeIn(params_box), FadeIn(params_content, lag_ratio=0.1), run_time=0.8)

        # Animation : basilic court avec splashs
        for step in range(8):
            # Avancer
            self.play(
                basilisk.animate.shift(RIGHT * 0.7),
                run_time=0.12,
                rate_func=linear,
            )

            # Splash
            splash_pos = basilisk.get_bottom() + DOWN * 0.05
            splash = Circle(
                radius=0.05, color=WATER_LIGHT,
                fill_opacity=0.5, stroke_width=1,
            ).move_to(splash_pos)

            self.add(splash)
            self.play(
                splash.animate.scale(5).set_opacity(0),
                run_time=0.15,
                rate_func=rate_functions.ease_out_quad,
            )
            self.remove(splash)

        self.wait(0.5)

        # Rappel équation
        eq_rappel = MathTex(
            r"\rho\,A\,v^2\,f \;\geq\; m\,g \quad \checkmark",
            font_size=30, color=GOLD,
        ).move_to(DOWN * 2.8)

        note = Text(
            "Aucune violation des lois physiques.\nCombinaison morphologique extrême.",
            font_size=16, color=LIGHT_BLUE, line_spacing=1.6,
        ).next_to(eq_rappel, DOWN, buff=0.3)

        self.play(Write(eq_rappel), run_time=0.8)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 09 : FORCE DIVINE (§6 & §7)
# ═══════════════════════════════════════════
class Scene09_ForceDivine(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = make_header("§6 — Force divine ?")
        self.play(Write(header), run_time=0.8)

        # Équation dynamique
        eq = MathTex(
            r"m\ddot{z}(t)",      # 0
            r"=",                  # 1
            r"F_{\text{eau}}(t)",  # 2
            r"+",                  # 3
            r"F_{\text{divin}}(t)",# 4
            r"-",                  # 5
            r"mg",                 # 6
            font_size=30, color=SOFT_WHITE,
        ).move_to(UP * 2.2)

        self.play(Write(eq[:3]), run_time=1)
        self.wait(0.3)

        # F_divin avec glow
        eq[4].set_color(GOLD)
        glow = eq[4].copy().set_color(GOLD).set_opacity(0.3).scale(1.4)
        self.play(
            Write(eq[3:]),
            FadeIn(glow, scale=1.5),
            FadeOut(glow, run_time=1.5),
            run_time=1.2,
        )

        note_ok = Text("Mathématiquement : rien ne l'interdit.", font_size=15, color=GREEN).move_to(UP * 0.6)
        self.play(FadeIn(note_ok), run_time=0.6)
        self.wait(1)

        mais = Text("Mais...", font_size=28, color=RED).move_to(DOWN * 0.2)
        self.play(FadeIn(mais, scale=1.2), run_time=0.5)
        self.wait(0.4)
        self.play(FadeOut(mais), FadeOut(note_ok), run_time=0.3)

        # Axiome encadré
        axiom_box = RoundedRectangle(
            width=4.0, height=3.2, corner_radius=0.15,
            color=RED, fill_color=DARK_SURFACE, fill_opacity=0.7,
            stroke_width=1.5,
        ).move_to(DOWN * 1.5)

        axiom_title = Text("Axiome de fermeture causale", font_size=15, color=RED)
        axiom_title.move_to(axiom_box.get_top() + DOWN * 0.35)

        sep = Line(LEFT * 1.7, RIGHT * 1.7, color=RED, stroke_width=0.8).next_to(axiom_title, DOWN, buff=0.15)

        criteria = VGroup(
            Text("Locale", font_size=15, color=SOFT_WHITE),
            Text("Universelle", font_size=15, color=SOFT_WHITE),
            Text("Paramétrable", font_size=15, color=SOFT_WHITE),
            Text("Répétable", font_size=15, color=SOFT_WHITE),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(sep, DOWN, buff=0.15)

        self.play(FadeIn(axiom_box), Write(axiom_title), Create(sep), run_time=0.8)
        for c in criteria:
            self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.3)
        self.wait(0.8)

        # Croix
        crosses = VGroup()
        for c in criteria:
            cross = Text("✗", font_size=22, color=RED).next_to(c, LEFT, buff=0.15)
            crosses.add(cross)
        self.play(FadeIn(crosses, lag_ratio=0.15), run_time=0.8)
        self.wait(1)

        # Conclusion
        theorem = Text(
            "Hors du modèle physique.\nMais pas logiquement impossible.",
            font_size=18, color=GOLD, line_spacing=1.6,
        ).move_to(DOWN * 3.5)
        self.play(FadeIn(theorem, shift=UP * 0.2), run_time=0.8)
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 10 : CONCLUSION
# ═══════════════════════════════════════════
class Scene10_Conclusion(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = make_header("Conclusion")
        self.play(Write(header), run_time=0.8)

        items = [
            ("Tension de surface", "✗", RED),
            ("Archimède seul", "✗", RED),
            ("Vitesse nécessaire", "80–110 km/h", RED),
            ("Sur la Lune", "~35 km/h", GREEN),
            ("Le basilic", "✓ morphologie", GREEN),
            ("Force divine", "? hors modèle", GOLD),
        ]

        table = VGroup()
        for i, (label, val, col) in enumerate(items):
            lbl = Text(label, font_size=18, color=SOFT_WHITE)
            v = Text(val, font_size=18, color=col)
            lbl.move_to(LEFT * 1.5 + DOWN * (i * 1.1 - 2.2))
            v.move_to(RIGHT * 1.8 + DOWN * (i * 1.1 - 2.2))
            row = VGroup(lbl, v)
            table.add(row)

        for row in table:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.4)
            self.wait(0.3)

        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # Citation finale
        quote = Text(
            "L'impossibilité d'écrire\nune équation\nn'est pas une impossibilité\nd'existence,\nmais une limite structurelle\nde la loi.",
            font_size=20, color=GOLD, line_spacing=1.5,
        ).move_to(ORIGIN)

        self.play(FadeIn(quote, lag_ratio=0.08), run_time=3)

        box = SurroundingRectangle(quote, color=GOLD, buff=0.2, stroke_width=1, corner_radius=0.15)
        self.play(Create(box), run_time=0.8)
        self.wait(3)
        self.play(FadeOut(quote), FadeOut(box), run_time=1)


# ═══════════════════════════════════════════
# SCENE 11 : CTA
# ═══════════════════════════════════════════
class Scene11_CTA(Scene):
    def construct(self):
        self.camera.background_color = BG

        name = Text(
            "TerreMathématiques",
            font_size=30, color=GOLD, weight=BOLD,
        ).move_to(UP * 1.5)

        sep = Line(LEFT * 2.0, RIGHT * 2.0, color=GOLD, stroke_width=1)
        sep.next_to(name, DOWN, buff=0.4)

        cta = Text(
            "Abonne-toi pour plus de\nphysique rigoureuse",
            font_size=24, color=SOFT_WHITE, line_spacing=1.6,
        ).next_to(sep, DOWN, buff=0.5)

        self.play(FadeIn(name, scale=1.3), run_time=1)
        self.play(Create(sep), run_time=0.5)
        self.play(FadeIn(cta, shift=UP * 0.2), run_time=0.8)

        # Pulse
        for _ in range(3):
            self.play(
                name.animate.scale(1.05),
                rate_func=there_and_back,
                run_time=0.8,
            )

        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
