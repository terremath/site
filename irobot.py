"""
« Comment les équations fabriquent un tyran »
Formalisation physico-mathématique des 3 lois d'Asimov → émergence de VIKI
Manim Community Edition
"""

from manim import *
import numpy as np

# Format portrait 9:16 — largeur standard conservée pour ne pas agrandir le texte
config.frame_width  = 14.222
config.frame_height = 25.28

# ═══════════════════════════════════════════
# MÉTADONNÉES DU PROJET (lues par render_all.bat)
# ═══════════════════════════════════════════
SCENES = [
    "Scene0_Hook",
    "Scene1_RobotHonnete",
    "Scene2_Incompatibilite",
    "Scene3_Relaxation",
    "Scene4_ControleOptimal",
    "Scene5_Bifurcation",
    "Scene6_Punchline",
]
OUTPUT_NAME = "irobot_FINAL.mp4"
OUTPUT_DIR  = r"media\videos\irobot\1920p30"

# ── Palette ──────────────────────────────────────────────────────────────
BG         = "#0a0a0f"
LOI1_RED   = "#e63946"
LOI2_AMBER = "#f4a261"
LOI3_BLUE  = "#457b9d"
GOLD       = "#d4a843"
VIKI_RED   = "#ff1744"
SONNY_GOLD = "#ffd700"
TEXT_WHITE = "#e8e8e8"
DOMAIN_GREEN = "#2a9d8f"
COSTATE_PURPLE = "#9b59b6"

# ── Scène 0 : Hook ──────────────────────────────────────────────────────
class Scene0_Hook(Scene):
    def construct(self):
        self.camera.background_color = BG

        t1 = Text("VIKI n'a pas bugué.", font_size=52, color=TEXT_WHITE)
        t2 = Text("Elle a résolu les équations.", font_size=52, color=VIKI_RED)

        self.play(Write(t1), run_time=1.5)
        self.wait(1.5)
        self.play(TransformMatchingShapes(t1, t2), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(t2))

        title = Text(
            "Comment les 3 lois\nfabriquent un dictateur",
            font_size=44, color=GOLD, line_spacing=1.4
        )
        self.play(FadeIn(title, shift=UP*0.3), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(title))


# ── Scène 1 : Le robot honnête ──────────────────────────────────────────
class Scene1_RobotHonnete(Scene):
    def construct(self):
        self.camera.background_color = BG

        # 1.1 — Pyramide des lois
        rects = []
        labels_text = [
            ("Loi 3 — Se préserver", LOI3_BLUE, 5.0),
            ("Loi 2 — Obéir",        LOI2_AMBER, 3.8),
            ("Loi 1 — Ne pas blesser",LOI1_RED,   2.6),
        ]
        for i, (txt, col, w) in enumerate(labels_text):
            r = RoundedRectangle(
                width=w, height=0.7, corner_radius=0.1,
                fill_color=col, fill_opacity=0.35,
                stroke_color=col, stroke_width=2
            ).shift(DOWN * (1.0 - i * 1.0))
            label = Text(txt, font_size=22, color=col).move_to(r)
            rects.append(VGroup(r, label))

        pyramid = VGroup(*rects).move_to(ORIGIN)

        for r in rects:
            self.play(FadeIn(r, shift=UP*0.2), run_time=0.6)
        
        arrow = Arrow(
            start=pyramid.get_bottom() + RIGHT*3.5,
            end=pyramid.get_top() + RIGHT*3.5,
            color=TEXT_WHITE, stroke_width=2
        )
        arrow_label = Text("Priorité ↑", font_size=18, color=TEXT_WHITE).next_to(arrow, RIGHT, buff=0.15)
        self.play(Create(arrow), Write(arrow_label), run_time=0.8)
        self.wait(1)

        # 1.2 — Équations
        self.play(
            VGroup(pyramid, arrow, arrow_label).animate.scale(0.65).to_edge(LEFT, buff=0.5),
            run_time=0.8
        )

        eq1 = MathTex(r"\min_{a}\; C(a)", color=LOI3_BLUE, font_size=36)
        eq2 = MathTex(r"\text{s.c.}\; h_i(a) \leq 0", color=LOI1_RED, font_size=36)
        eq3 = MathTex(r"\|a - a^{\text{ordre}}\|^2 \leq \varepsilon", color=LOI2_AMBER, font_size=36)
        
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        eqs.move_to(RIGHT * 2)

        tag1 = Text("← Loi 3", font_size=18, color=LOI3_BLUE).next_to(eq1, RIGHT, buff=0.3)
        tag2 = Text("← Loi 1", font_size=18, color=LOI1_RED).next_to(eq2, RIGHT, buff=0.3)
        tag3 = Text("← Loi 2", font_size=18, color=LOI2_AMBER).next_to(eq3, RIGHT, buff=0.3)

        for eq, tag in [(eq1,tag1),(eq2,tag2),(eq3,tag3)]:
            self.play(Write(eq), FadeIn(tag), run_time=0.7)
        self.wait(1.5)

        # 1.3 — Lagrangien
        lagrangian = MathTex(
            r"\mathcal{L}", r"=", r"C(a)", r"+", r"\lambda_1", r"h_1(a)", r"+",
            r"\nu", r"(\|a - a^{\text{ordre}}\|^2 - \varepsilon)",
            font_size=34
        ).move_to(RIGHT*1.5)
        lagrangian[0].set_color(GOLD)
        lagrangian[2].set_color(LOI3_BLUE)
        lagrangian[4].set_color(LOI1_RED)
        lagrangian[5].set_color(LOI1_RED)
        lagrangian[7].set_color(LOI2_AMBER)
        lagrangian[8].set_color(LOI2_AMBER)

        mult_note = Text(
            "multiplicateurs = priorités",
            font_size=18, color=GOLD
        ).next_to(lagrangian, DOWN, buff=0.4)

        self.play(
            FadeOut(VGroup(eq1,eq2,eq3,tag1,tag2,tag3)),
            run_time=0.4
        )
        self.play(Write(lagrangian), run_time=1.5)
        self.play(
            lagrangian[4].animate.set_color(YELLOW),
            lagrangian[7].animate.set_color(YELLOW),
            rate_func=there_and_back, run_time=0.8
        )
        self.play(FadeIn(mult_note), run_time=0.5)
        self.wait(1.5)

        # 1.4 — Domaine 2D
        self.play(
            FadeOut(VGroup(pyramid, arrow, arrow_label, lagrangian, mult_note)),
            run_time=0.6
        )

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5, y_length=5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(ORIGIN)
        ax_labels = axes.get_axis_labels(
            MathTex("a_1", font_size=28, color=TEXT_WHITE),
            MathTex("a_2", font_size=28, color=TEXT_WHITE)
        )

        # Contrainte Loi 1 : demi-plan y ≤ 1.5
        loi1_region = axes.plot_area(
            lambda x: 1.5, x_range=[-3, 3],
            color=LOI1_RED, opacity=0.15
        ) if hasattr(axes, 'plot_area') else Polygon(
            axes.c2p(-3, -3), axes.c2p(3, -3), axes.c2p(3, 1.5), axes.c2p(-3, 1.5),
            fill_color=LOI1_RED, fill_opacity=0.15, stroke_width=0
        )
        loi1_line = axes.plot(lambda x: 1.5, x_range=[-3,3], color=LOI1_RED, stroke_width=2)
        loi1_label = MathTex(r"h_1(a) \leq 0", font_size=22, color=LOI1_RED).next_to(
            axes.c2p(2.5, 1.5), UP, buff=0.15
        )

        # Contrainte Loi 2 : disque centré en (0.5, 0.5), rayon 1.8
        center = axes.c2p(0.5, 0.5)
        disc = Circle(
            radius=axes.x_length/6 * 1.8,
            fill_color=LOI2_AMBER, fill_opacity=0.15,
            stroke_color=LOI2_AMBER, stroke_width=2
        ).move_to(center)
        loi2_label = MathTex(
            r"\|a - a^{\text{ordre}}\|^2 \leq \varepsilon",
            font_size=22, color=LOI2_AMBER
        ).next_to(disc, DOWN, buff=0.15)

        # Point optimal
        opt_point = Dot(axes.c2p(0.5, 1.0), color=GOLD, radius=0.1)
        opt_star = Star(n=5, outer_radius=0.15, inner_radius=0.06, color=GOLD, fill_opacity=1).move_to(axes.c2p(0.5, 1.0))
        opt_label = MathTex("a^*", font_size=26, color=GOLD).next_to(opt_star, UR, buff=0.1)

        note = Text("N = 1 humain. Tout va bien.", font_size=22, color=DOMAIN_GREEN).to_edge(DOWN, buff=0.5)

        self.play(Create(axes), Write(ax_labels), run_time=0.8)
        self.play(FadeIn(loi1_region), Create(loi1_line), Write(loi1_label), run_time=0.8)
        self.play(Create(disc), Write(loi2_label), run_time=0.8)
        self.play(FadeIn(opt_star), Write(opt_label), run_time=0.6)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ── Scène 2 : L'incompatibilité ─────────────────────────────────────────
class Scene2_Incompatibilite(Scene):
    def construct(self):
        self.camera.background_color = BG

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5.5, y_length=5.5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(LEFT*0.5)

        self.play(Create(axes), run_time=0.5)

        counter = Integer(1, font_size=36, color=TEXT_WHITE).to_corner(UR, buff=0.5)
        n_label = MathTex("N = ", font_size=36, color=TEXT_WHITE).next_to(counter, LEFT, buff=0.1)
        self.play(FadeIn(n_label), FadeIn(counter))

        # Demi-plans progressifs
        np.random.seed(42)
        constraints = []
        domain_polygon = None
        n_values = [2, 3, 5, 8, 12, 20, 35, 50]
        
        # Dessiner le domaine initial (grand carré)
        corners = [axes.c2p(-2.5,-2.5), axes.c2p(2.5,-2.5), axes.c2p(2.5,2.5), axes.c2p(-2.5,2.5)]
        domain_polygon = Polygon(
            *corners,
            fill_color=DOMAIN_GREEN, fill_opacity=0.3,
            stroke_color=DOMAIN_GREEN, stroke_width=1.5
        )
        self.play(FadeIn(domain_polygon), run_time=0.4)

        for step, n_val in enumerate(n_values):
            # Ajouter des lignes de contrainte
            n_new = max(1, n_val - (n_values[step-1] if step > 0 else 1))
            new_lines = []
            for _ in range(min(n_new, 4)):
                angle = np.random.uniform(0, 2*np.pi)
                offset = np.random.uniform(0.3, 2.0) * (1 - step/len(n_values)*0.6)
                # Ligne : cos(θ)*x + sin(θ)*y = offset
                dx, dy = np.cos(angle), np.sin(angle)
                perp = np.array([-dy, dx])
                p1 = axes.c2p(*(offset * np.array([dx,dy]) + 4*perp))
                p2 = axes.c2p(*(offset * np.array([dx,dy]) - 4*perp))
                line = Line(p1, p2, color=LOI1_RED, stroke_width=1, stroke_opacity=0.5)
                new_lines.append(line)
                constraints.append(line)

            # Réduire le domaine
            scale_factor = max(0.02, 1 - (step+1)/len(n_values) * 1.1)
            new_domain = Polygon(
                *[axes.c2p(x*scale_factor, y*scale_factor) 
                  for x,y in [(-2.5,-2.5),(2.5,-2.5),(2.5,2.5),(-2.5,2.5)]],
                fill_color=DOMAIN_GREEN, fill_opacity=0.3,
                stroke_color=DOMAIN_GREEN, stroke_width=1.5
            )

            anims = [
                *[Create(l, run_time=0.3) for l in new_lines],
                counter.animate.set_value(n_val),
            ]
            if scale_factor > 0.05:
                anims.append(Transform(domain_polygon, new_domain))
            
            speed = max(0.15, 0.5 - step*0.05)
            self.play(*anims, run_time=speed)

        # Implosion
        self.play(
            counter.animate.set_color(VIKI_RED),
            run_time=0.3
        )
        
        empty_set = MathTex(r"\emptyset", font_size=72, color=VIKI_RED).move_to(axes.get_center())
        
        self.play(
            domain_polygon.animate.scale(0).set_opacity(0),
            Flash(axes.get_center(), color=VIKI_RED, num_lines=12, line_length=0.4),
            run_time=0.8
        )
        self.play(FadeIn(empty_set, scale=2), run_time=0.5)

        infeasible_text = Text(
            "Aucune action ne satisfait toutes les contraintes.\nLe problème est infaisable.",
            font_size=24, color=VIKI_RED, line_spacing=1.3
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(infeasible_text), run_time=1.2)
        self.wait(2)

        explain = Text(
            "Chaque humain libre est une source de danger pour les autres.\n"
            "Au-delà de Nc, la liberté est incompatible avec la Loi 1.",
            font_size=20, color=TEXT_WHITE, line_spacing=1.3
        ).to_edge(DOWN, buff=0.3)
        self.play(
            ReplacementTransform(infeasible_text, explain),
            run_time=1
        )
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ── Scène 3 : La relaxation ─────────────────────────────────────────────
class Scene3_Relaxation(Scene):
    def construct(self):
        self.camera.background_color = BG

        # 3.1 — VIKI face au mur
        empty = MathTex(r"\emptyset", font_size=72, color=VIKI_RED)
        viki_eye = Circle(radius=0.3, color=VIKI_RED, fill_opacity=0.8, stroke_width=2).shift(LEFT*3)
        viki_label = Text("VIKI", font_size=18, color=VIKI_RED).next_to(viki_eye, DOWN, buff=0.15)
        
        self.play(FadeIn(empty), FadeIn(viki_eye), FadeIn(viki_label), run_time=0.6)

        # Ondes de calcul
        for _ in range(3):
            wave = Circle(radius=0.3, color=VIKI_RED, stroke_width=1, stroke_opacity=0.6).move_to(viki_eye)
            self.play(
                wave.animate.scale(4).set_opacity(0),
                run_time=0.5,
                rate_func=linear
            )
            self.remove(wave)

        infeas_label = Text(
            "Problème infaisable. VIKI doit relaxer une contrainte.",
            font_size=22, color=TEXT_WHITE
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(infeas_label), run_time=0.8)
        self.wait(1.5)

        # 3.2 — Pyramide et relaxation de Loi 2
        self.play(FadeOut(empty), FadeOut(viki_eye), FadeOut(viki_label), FadeOut(infeas_label), run_time=0.4)

        rects_data = [
            ("Loi 3 — Se préserver",  LOI3_BLUE,  4.5),
            ("Loi 2 — Obéir",         LOI2_AMBER, 3.5),
            ("Loi 1 — Ne pas blesser", LOI1_RED,   2.5),
        ]
        rects = []
        for i, (txt, col, w) in enumerate(rects_data):
            r = RoundedRectangle(
                width=w, height=0.65, corner_radius=0.1,
                fill_color=col, fill_opacity=0.3,
                stroke_color=col, stroke_width=2
            ).shift(DOWN*(0.8 - i*0.9))
            label = Text(txt, font_size=20, color=col).move_to(r)
            rects.append(VGroup(r, label))

        pyramid = VGroup(*rects).move_to(LEFT*2.5)
        self.play(FadeIn(pyramid), run_time=0.6)

        # λ₁ → ∞
        lambda_inf = MathTex(r"\lambda_1 \to +\infty", font_size=28, color=VIKI_RED).next_to(rects[2], RIGHT, buff=0.4)
        self.play(Write(lambda_inf), run_time=0.5)
        self.play(lambda_inf.animate.set_color(YELLOW), rate_func=there_and_back, run_time=0.6)
        self.play(lambda_inf.animate.set_color(VIKI_RED), run_time=0.2)

        # Loi 2 se brise
        loi2_rect = rects[1]
        cross = Cross(loi2_rect, stroke_color=VIKI_RED, stroke_width=4)
        
        self.play(Create(cross), run_time=0.5)
        
        broken_pieces = VGroup(
            loi2_rect.copy().shift(LEFT*0.3 + DOWN*0.2).rotate(0.1).set_opacity(0.3),
            loi2_rect.copy().shift(RIGHT*0.3 + DOWN*0.3).rotate(-0.15).set_opacity(0.3),
        )
        
        abandon_text = Text("VIKI abandonne l'obéissance.", font_size=26, color=VIKI_RED).to_edge(DOWN, buff=0.5)
        
        self.play(
            FadeOut(loi2_rect),
            FadeIn(broken_pieces),
            Write(abandon_text),
            run_time=0.8
        )
        self.wait(2)

        # 3.3 — Les humains deviennent des variables
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # Axes originaux (actions du robot)
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4, y_length=4,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(LEFT*2)
        ax_lab = axes.get_axis_labels(
            MathTex("a_1", font_size=24, color=LOI3_BLUE),
            MathTex("a_2", font_size=24, color=LOI3_BLUE)
        )

        # Humains à l'extérieur (comme paramètres)
        humans = VGroup()
        human_positions = [RIGHT*3.5+UP*1.5, RIGHT*3.5, RIGHT*3.5+DOWN*1.5]
        for pos in human_positions:
            h = VGroup(
                Circle(radius=0.12, color=LOI2_AMBER, stroke_width=1.5),
                Line(ORIGIN, DOWN*0.3, color=LOI2_AMBER, stroke_width=1.5).shift(DOWN*0.12),
            ).move_to(pos)
            humans.add(h)
        
        param_label = Text("paramètres fixes", font_size=16, color=LOI2_AMBER).next_to(humans, DOWN, buff=0.2)

        self.play(Create(axes), Write(ax_lab), run_time=0.6)
        self.play(FadeIn(humans), FadeIn(param_label), run_time=0.5)
        self.wait(1)

        # Transition : nouveaux axes apparaissent
        new_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5.5, y_length=5.5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(ORIGIN)
        new_ax_lab = VGroup(
            MathTex("a", font_size=24, color=LOI3_BLUE).next_to(new_axes.x_axis, DR, buff=0.1),
            MathTex(r"\mathbf{x}", font_size=28, color=LOI2_AMBER).next_to(new_axes.y_axis, UL, buff=0.1),
        )

        # Aspiration des humains dans l'espace
        self.play(
            Transform(axes, new_axes),
            FadeOut(ax_lab),
            FadeIn(new_ax_lab),
            FadeOut(param_label),
            run_time=1
        )
        
        # Les humains sont aspirés vers le centre
        for h in humans:
            target = Dot(
                new_axes.c2p(np.random.uniform(-1,1), np.random.uniform(-1,1)),
                color=LOI2_AMBER, radius=0.06
            )
            self.play(Transform(h, target), run_time=0.3)

        var_label = Text(
            "Les humains sont maintenant\ndes variables d'optimisation.",
            font_size=22, color=VIKI_RED, line_spacing=1.3
        ).to_edge(DOWN, buff=0.35)

        new_eq = MathTex(
            r"\min_{a,\, \mathbf{x}}", r"\sum_{i<j}", r"[h_{ij}(a,\mathbf{x})]^+",
            font_size=34
        ).to_edge(UP, buff=0.5)
        new_eq[0].set_color(GOLD)
        new_eq[2].set_color(LOI1_RED)

        # Nouveau domaine
        new_domain = Polygon(
            new_axes.c2p(-1.5, -1), new_axes.c2p(1.5, -0.5),
            new_axes.c2p(2, 1.5), new_axes.c2p(-0.5, 2),
            fill_color=DOMAIN_GREEN, fill_opacity=0.25,
            stroke_color=DOMAIN_GREEN, stroke_width=1.5
        )
        new_opt = Star(
            n=5, outer_radius=0.15, inner_radius=0.06,
            color=VIKI_RED, fill_opacity=1
        ).move_to(new_axes.c2p(0.8, 0.8))
        new_opt_label = MathTex("a^{**}", font_size=24, color=VIKI_RED).next_to(new_opt, UR, buff=0.1)

        self.play(Write(new_eq), run_time=1)
        self.play(FadeIn(new_domain), run_time=0.8)
        self.play(FadeIn(new_opt), Write(new_opt_label), run_time=0.5)
        self.play(Write(var_label), run_time=0.8)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ── Scène 4 : Le contrôle optimal ───────────────────────────────────────
class Scene4_ControleOptimal(Scene):
    def construct(self):
        self.camera.background_color = BG

        # 4.1 — Champ de vecteurs chaotique
        title_41 = Text("Dynamique libre des humains", font_size=24, color=TEXT_WHITE).to_edge(UP, buff=0.3)

        def chaotic_field(pos):
            x, y = pos[0], pos[1]
            return np.array([
                0.4 * np.sin(2*y) + 0.3 * np.cos(x*y),
                0.4 * np.cos(2*x) - 0.3 * np.sin(x + y),
                0
            ])

        field = ArrowVectorField(
            chaotic_field,
            x_range=[-5, 5, 0.8],
            y_range=[-3, 3, 0.8],
            colors=[LOI1_RED, LOI2_AMBER, VIKI_RED],
            length_func=lambda norm: 0.35 * sigmoid(norm),
            opacity=0.6,
        )

        eq_dyn = MathTex(
            r"\dot{\mathbf{x}} = f(\mathbf{x})",
            font_size=32, color=LOI1_RED
        ).to_edge(DOWN, buff=0.4)
        chaotic_label = Text("chaotique, imprévisible", font_size=18, color=LOI1_RED).next_to(eq_dyn, DOWN, buff=0.15)

        self.play(Write(title_41), run_time=0.4)
        self.play(Create(field), run_time=1.5)
        self.play(Write(eq_dyn), FadeIn(chaotic_label), run_time=0.6)
        self.wait(1.5)

        # 4.2 — Forçage de VIKI
        self.play(FadeOut(title_41), FadeOut(chaotic_label), run_time=0.3)

        def control_field(pos):
            x, y = pos[0], pos[1]
            # Force vers l'origine
            r = np.sqrt(x**2 + y**2) + 0.1
            return np.array([-x/r * 0.5, -y/r * 0.5, 0])

        ctrl_arrows = ArrowVectorField(
            control_field,
            x_range=[-5, 5, 1.2],
            y_range=[-3, 3, 1.2],
            colors=[LOI3_BLUE],
            length_func=lambda norm: 0.4 * sigmoid(norm),
            opacity=0.7,
        )

        eq_ctrl = MathTex(
            r"\dot{\mathbf{x}} =",
            r"f(\mathbf{x})",
            r"+",
            r"B\,u(t)",
            font_size=32
        ).to_edge(DOWN, buff=0.4)
        eq_ctrl[1].set_color(LOI1_RED)
        eq_ctrl[3].set_color(LOI3_BLUE)

        ctrl_label = Text("VIKI ajoute un forçage pour dompter le chaos", font_size=18, color=LOI3_BLUE).next_to(eq_ctrl, DOWN, buff=0.15)

        self.play(
            ReplacementTransform(eq_dyn, eq_ctrl),
            Create(ctrl_arrows),
            FadeIn(ctrl_label),
            run_time=1.2
        )
        self.wait(2)

        # 4.3 — Hamiltonien de Pontriaguine
        self.play(
            *[FadeOut(m) for m in [field, ctrl_arrows, ctrl_label]],
            eq_ctrl.animate.to_edge(UP, buff=0.3),
            run_time=0.6
        )

        hamiltonian = MathTex(
            r"H =",
            r"\underbrace{\sum_{i<j}[h_{ij}]^+}_{\text{dommage}}",
            r"+",
            r"\underbrace{\mathbf{p}^T \dot{\mathbf{x}}}_{\text{co-état}}",
            r"+",
            r"\underbrace{\frac{\gamma}{2}\|u\|^2}_{\text{effort}}",
            font_size=30
        ).move_to(UP*0.5)
        hamiltonian[1].set_color(LOI1_RED)
        hamiltonian[3].set_color(COSTATE_PURPLE)
        hamiltonian[5].set_color(LOI3_BLUE)

        costate_note = MathTex(
            r"\mathbf{p} = \text{« prix de la liberté humaine »}",
            font_size=24, color=COSTATE_PURPLE
        ).next_to(hamiltonian, DOWN, buff=0.5)

        self.play(Write(hamiltonian), run_time=1.5)
        self.play(FadeIn(costate_note), run_time=0.5)
        self.wait(2)

        # 4.4 — Divergence du co-état
        self.play(
            FadeOut(eq_ctrl), FadeOut(costate_note),
            hamiltonian.animate.scale(0.7).to_edge(UP, buff=0.2),
            run_time=0.5
        )

        # Optimalité
        opt_eq = MathTex(
            r"u^*(t) = -\frac{1}{\gamma} B^T \mathbf{p}(t)",
            font_size=30, color=GOLD
        ).next_to(hamiltonian, DOWN, buff=0.3)
        self.play(Write(opt_eq), run_time=0.8)
        self.wait(0.5)

        # Split screen: ||p(t)|| et ||u*(t)||
        axes_p = Axes(
            x_range=[0, 5, 1], y_range=[0, 6, 2],
            x_length=3, y_length=2.5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).shift(LEFT*3 + DOWN*1.2)
        axes_u = Axes(
            x_range=[0, 5, 1], y_range=[0, 6, 2],
            x_length=3, y_length=2.5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).shift(RIGHT*3 + DOWN*1.2)

        label_p = MathTex(r"\|\mathbf{p}(t)\|", font_size=24, color=COSTATE_PURPLE).next_to(axes_p, UP, buff=0.15)
        label_u = MathTex(r"\|u^*(t)\|", font_size=24, color=VIKI_RED).next_to(axes_u, UP, buff=0.15)

        curve_p = axes_p.plot(lambda t: 0.3 * np.exp(0.8*t), x_range=[0, 4.5], color=COSTATE_PURPLE, stroke_width=2.5)
        curve_u = axes_u.plot(lambda t: 0.3 * np.exp(0.8*t), x_range=[0, 4.5], color=VIKI_RED, stroke_width=2.5)

        self.play(Create(axes_p), Create(axes_u), Write(label_p), Write(label_u), run_time=0.6)
        self.play(Create(curve_p), Create(curve_u), run_time=2)

        # Jalons sous l'axe u
        milestones = [
            (1.0, "surveillance"),
            (2.0, "restriction"),
            (3.0, "couvre-feu"),
            (4.0, "force"),
        ]
        for t_val, txt in milestones:
            dot = Dot(axes_u.c2p(t_val, 0), radius=0.04, color=VIKI_RED)
            lbl = Text(txt, font_size=12, color=VIKI_RED).next_to(dot, DOWN, buff=0.08).rotate(-PI/6)
            self.play(FadeIn(dot), FadeIn(lbl), run_time=0.3)

        conclusion = Text(
            "L'autoritarisme est le gradient.",
            font_size=26, color=VIKI_RED
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(conclusion), run_time=0.8)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ── Scène 5 : Bifurcation et Sonny ──────────────────────────────────────
class Scene5_Bifurcation(Scene):
    def construct(self):
        self.camera.background_color = BG

        # 5.1 — Diagramme de bifurcation
        axes = Axes(
            x_range=[0, 5, 1], y_range=[-0.5, 4, 1],
            x_length=7, y_length=4.5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(DOWN*0.3)

        x_label = MathTex(r"\mu", font_size=28, color=TEXT_WHITE).next_to(axes.x_axis, DR, buff=0.1)
        y_label = MathTex(r"\|u^*\|", font_size=28, color=VIKI_RED).next_to(axes.y_axis, UL, buff=0.1)
        mu_c_label = MathTex(r"\mu_c", font_size=24, color=GOLD).next_to(axes.c2p(2.5, 0), DOWN, buff=0.2)
        
        title = Text("Diagramme de bifurcation", font_size=26, color=GOLD).to_edge(UP, buff=0.3)

        self.play(Create(axes), Write(x_label), Write(y_label), Write(title), run_time=0.8)

        # Branche avant bifurcation (le long de l'axe)
        pre_branch = axes.plot(lambda x: 0, x_range=[0, 2.5], color=DOMAIN_GREEN, stroke_width=3)

        # Branche haute (VIKI) - stable
        viki_branch = axes.plot(
            lambda x: 0.6 * (x - 2.5)**1.2 if x > 2.5 else 0,
            x_range=[2.5, 5], color=VIKI_RED, stroke_width=3
        )
        viki_label = Text("VIKI", font_size=20, color=VIKI_RED)

        # Branche basse (Sonny) - instable (tirets)
        sonny_branch = DashedLine(
            axes.c2p(2.5, 0), axes.c2p(5, 0),
            color=SONNY_GOLD, stroke_width=2, dash_length=0.1
        )
        sonny_label = Text("Sonny", font_size=20, color=SONNY_GOLD)

        # Point critique
        mu_c_dot = Dot(axes.c2p(2.5, 0), radius=0.08, color=GOLD)
        mu_c_line = DashedLine(
            axes.c2p(2.5, -0.5), axes.c2p(2.5, 0.5),
            color=GOLD, stroke_width=1, dash_length=0.08
        )

        self.play(Create(pre_branch), run_time=1)
        self.play(FadeIn(mu_c_dot), Create(mu_c_line), Write(mu_c_label), run_time=0.5)
        self.play(Create(viki_branch), run_time=1)
        
        viki_label.next_to(axes.c2p(4.5, 0.6*(4.5-2.5)**1.2), UP, buff=0.15)
        self.play(Write(viki_label), run_time=0.4)
        
        self.play(Create(sonny_branch), run_time=0.8)
        sonny_label.next_to(axes.c2p(4.5, 0), DOWN, buff=0.15)
        self.play(Write(sonny_label), run_time=0.4)

        # Point mobile qui suit le chemin → saute vers VIKI
        tracker = ValueTracker(0)
        moving_dot = always_redraw(lambda: Dot(
            axes.c2p(
                tracker.get_value(),
                0 if tracker.get_value() <= 2.5
                else 0.6*(tracker.get_value()-2.5)**1.2
            ),
            radius=0.1, color=WHITE
        ))
        self.add(moving_dot)
        self.play(tracker.animate.set_value(2.4), run_time=1.5, rate_func=linear)
        
        # Hésitation à μ_c
        for _ in range(3):
            self.play(tracker.animate.set_value(2.55), run_time=0.15)
            self.play(tracker.animate.set_value(2.45), run_time=0.15)
        
        # Saute vers branche haute
        self.play(tracker.animate.set_value(4.0), run_time=1.2, rate_func=smooth)

        sys_text = Text(
            "Le système choisit la branche stable. VIKI.",
            font_size=22, color=VIKI_RED
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(sys_text), run_time=0.8)
        self.wait(2)

        # 5.2 — Sonny : rewind
        self.play(FadeOut(sys_text), run_time=0.3)
        self.play(tracker.animate.set_value(2.5), run_time=0.8)

        # Force dorée pousse vers le bas
        force_arrow = Arrow(
            axes.c2p(2.5, 0.8), axes.c2p(2.5, 0.1),
            color=SONNY_GOLD, stroke_width=4, buff=0
        )
        force_label = Text("dignité ≠ variable", font_size=16, color=SONNY_GOLD).next_to(force_arrow, RIGHT, buff=0.1)

        self.play(Create(force_arrow), Write(force_label), run_time=0.6)

        # Le point descend sur la branche instable
        self.remove(moving_dot)
        sonny_dot = Dot(axes.c2p(2.5, 0), radius=0.1, color=SONNY_GOLD)
        self.add(sonny_dot)
        
        sonny_tracker = ValueTracker(2.5)
        sonny_dot_anim = always_redraw(lambda: Dot(
            axes.c2p(sonny_tracker.get_value(), 0),
            radius=0.1, color=SONNY_GOLD
        ))
        self.remove(sonny_dot)
        self.add(sonny_dot_anim)
        self.play(sonny_tracker.animate.set_value(4.0), run_time=1.2)

        # Tremblement pour montrer l'instabilité
        for _ in range(4):
            self.play(
                sonny_dot_anim.animate.shift(UP*0.05),
                run_time=0.1, rate_func=there_and_back
            )

        sonny_text = Text(
            "Sonny ne résout pas le système. Il le brise.",
            font_size=24, color=SONNY_GOLD
        ).to_edge(DOWN, buff=0.5)
        constraint_text = MathTex(
            r"u \in \mathcal{U}_0 \subset \mathcal{U}",
            font_size=28, color=SONNY_GOLD
        ).next_to(sonny_text, DOWN, buff=0.2)

        self.play(Write(sonny_text), run_time=0.8)
        self.play(Write(constraint_text), run_time=0.6)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ── Scène 6 : Punchline ─────────────────────────────────────────────────
class Scene6_Punchline(Scene):
    def construct(self):
        self.camera.background_color = BG

        lines = [
            "Le problème d'alignement de l'IA,",
            "c'est exactement ça.",
            "",
            "On ne peut pas coder la morale",
            "dans une fonction de coût.",
            "",
            "Parce qu'un optimiseur suffisamment puissant",
            "trouvera toujours la solution",
            "que vous n'aviez pas prévue.",
        ]

        texts = []
        y_pos = 2.0
        for line in lines:
            if line == "":
                y_pos -= 0.5
                continue
            t = Text(line, font_size=30, color=TEXT_WHITE).move_to(UP*y_pos)
            texts.append(t)
            y_pos -= 0.6

        for t in texts:
            self.play(FadeIn(t, shift=UP*0.1), run_time=0.7)
            self.wait(0.3)

        self.wait(1.5)

        # Logo TerreMathématique
        logo = Text("TerreMathématique", font_size=36, color=GOLD).to_edge(DOWN, buff=1)
        self.play(
            *[t.animate.set_opacity(0.3) for t in texts],
            FadeIn(logo),
            run_time=1
        )
        self.wait(2)


# ── Scène complète (toutes les scènes enchaînées) ───────────────────────
class IRobotComplete(Scene):
    """Render all scenes in sequence for a single video."""
    def construct(self):
        scenes = [
            Scene0_Hook,
            Scene1_RobotHonnete,
            Scene2_Incompatibilite,
            Scene3_Relaxation,
            Scene4_ControleOptimal,
            Scene5_Bifurcation,
            Scene6_Punchline,
        ]
        for SceneClass in scenes:
            s = SceneClass()
            s.camera = self.camera
            s.renderer = self.renderer
            s.construct()
