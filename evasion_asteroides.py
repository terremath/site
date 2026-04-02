"""
Évitement optimal dans un champ d'astéroïdes
Formalisation mathématique : zones interdites, coût carburant,
missiles guidés, principes d'évasion optimale.
Manim Community Edition — TerreMathématiques
"""

from manim import *
import numpy as np

# ═══════════════════════════════════════════
# MÉTADONNÉES (lues par render_all.bat)
# ═══════════════════════════════════════════
SCENES = [
    "Scene01_LeProbleme",
    "Scene02_ZonesInterdites",
    "Scene03_CoutMouvement",
    "Scene04_PrixDeviation",
    "Scene05_LesMissiles",
    "Scene06_TrouverUnChemin",
    "Scene07_TroisPrincipes",
    "Scene08_LaFlotte",
    "Scene09_Synthese",
    "Scene10_CTA",
]
OUTPUT_NAME = "evasion_asteroides_FINAL.mp4"
OUTPUT_DIR  = r"media\videos\evasion_asteroides\1920p30"

# Format portrait — cohérent avec les autres vidéos
config.frame_width  = 4.5
config.frame_height = 8.0

# ═══════════════════════════════════════════
# PALETTE
# ═══════════════════════════════════════════
BG           = "#030712"
SHIP_COL     = "#60a5fa"   # bleu clair — vaisseau
ASTEROID_COL = "#78716c"   # gris pierre — astéroïde
MISSILE_COL  = "#ef4444"   # rouge — missile / zone interdite
NAV_COL      = "#4ade80"   # vert — espace navigable / bon
THRUST_COL   = "#f97316"   # orange — poussée
GRAV_COL     = "#a78bfa"   # violet — gravité
GOLD         = "#fbbf24"   # or — équations / accent
TEXT_W       = "#f1f5f9"   # blanc — texte courant
MUTED        = "#94a3b8"   # gris — labels secondaires
LOS_COL      = "#facc15"   # jaune — ligne de visée
ENERGY_COL   = "#38bdf8"   # bleu ciel — énergie


# ═══════════════════════════════════════════
# UTILITAIRES PARTAGÉS
# ═══════════════════════════════════════════
def make_stars(n=70, seed=42):
    rng = np.random.RandomState(seed)
    return VGroup(*[
        Dot(
            point=[rng.uniform(-2.2, 2.2), rng.uniform(-4, 4), 0],
            radius=rng.uniform(0.01, 0.025),
            color=TEXT_W,
            fill_opacity=rng.uniform(0.2, 0.95),
        )
        for _ in range(n)
    ])


def make_header(text):
    h = Text(text, font_size=20, color=GOLD).to_edge(UP, buff=0.35)
    line = Line(
        h.get_left() + DOWN * 0.18,
        h.get_right() + DOWN * 0.18,
        color=GOLD, stroke_width=1.2,
    )
    return VGroup(h, line)


def sub_text(text, font_size=15):
    """Sous-titre au bas de l'écran portrait — multilignes si besoin."""
    return Text(text, font_size=font_size, color=TEXT_W,
                line_spacing=1.25).to_edge(DOWN, buff=0.35)


def ship_shape(scale=1.0):
    """Petit vaisseau triangulaire."""
    s = scale * 0.28
    return Polygon(
        [0, s * 1.25, 0], [-s, -s, 0], [0, -s * 0.4, 0], [s, -s, 0],
        fill_color=SHIP_COL, fill_opacity=0.9,
        stroke_color=TEXT_W, stroke_width=0.8,
    )


def asteroid_shape(radius=0.32, seed=0):
    """Polygone irrégulier type astéroïde."""
    rng = np.random.RandomState(seed)
    n = 9
    angles = np.linspace(0, 2 * PI, n, endpoint=False)
    radii = radius * (0.62 + 0.38 * rng.rand(n))
    pts = [[r * np.cos(a), r * np.sin(a), 0] for r, a in zip(radii, angles)]
    return Polygon(
        *pts,
        fill_color=ASTEROID_COL, fill_opacity=0.88,
        stroke_color="#a8a29e", stroke_width=1.0,
    )


def missile_dot(pos=ORIGIN):
    return Dot(point=pos, color=MISSILE_COL, radius=0.1)


def bubble(center=ORIGIN, radius=0.7, color=MISSILE_COL, opacity=0.14):
    return Circle(
        radius=radius,
        fill_color=color, fill_opacity=opacity,
        stroke_color=color, stroke_width=1.4,
    ).move_to(center)


# ═══════════════════════════════════════════
# SCÈNE 01 — Le problème
# ═══════════════════════════════════════════
class Scene01_LeProbleme(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(make_stars())

        # ── Accroche ──
        title = Text(
            "Évitement optimal\ndans un champ\nd'astéroïdes",
            font_size=30, color=GOLD, line_spacing=1.35,
        ).move_to(UP * 1.5)
        self.play(FadeIn(title, shift=UP * 0.4), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(title))

        header = make_header("Le problème")
        self.play(FadeIn(header))

        # ── Décor spatial ──
        asts = VGroup(
            asteroid_shape(0.38, seed=1).move_to([-0.8,  1.4, 0]),
            asteroid_shape(0.45, seed=2).move_to([ 1.0, -0.3, 0]),
            asteroid_shape(0.30, seed=3).move_to([ 0.2,  0.6, 0]),
            asteroid_shape(0.42, seed=4).move_to([-0.5, -1.2, 0]),
        )
        self.play(FadeIn(asts), run_time=0.8)

        # Ship entre par la gauche
        ship = ship_shape().move_to([-2.4, 0, 0])
        self.play(FadeIn(ship))

        # Sous-titre 1
        s1 = sub_text("Un vaisseau doit traverser cette zone.")
        self.play(FadeIn(s1))
        self.play(ship.animate.move_to([-1.6, 0, 0]), run_time=1.2)
        self.wait(0.8)
        self.play(FadeOut(s1))

        # Sous-titre 2 — astéroïdes
        s2 = sub_text("Astéroïdes : obstacles fixes.")
        self.play(FadeIn(s2))
        self.wait(1.8)
        self.play(FadeOut(s2))

        # Missile mobile
        mis = missile_dot([2.0, 2.2, 0])
        mis_path = ParametricFunction(
            lambda t: np.array([2.0 - t * 3.5, 2.2 - t * 1.8, 0]),
            t_range=[0, 1], color=MISSILE_COL, stroke_width=1.5, stroke_opacity=0.5,
        )
        s3 = sub_text("Missiles : menaces mobiles.")
        self.play(FadeIn(mis), Create(mis_path), FadeIn(s3))
        self.play(mis.animate.move_to([-1.5, 0.4, 0]), run_time=1.8, rate_func=linear)
        self.wait(0.5)
        self.play(FadeOut(s3))

        # Jauge carburant
        fuel_bg = Rectangle(
            width=1.4, height=0.28,
            fill_color="#1e293b", fill_opacity=1,
            stroke_color=TEXT_W, stroke_width=0.8,
        ).to_corner(UR, buff=0.45)
        fuel_bar = Rectangle(
            width=1.28, height=0.18,
            fill_color=NAV_COL, fill_opacity=0.9, stroke_width=0,
        ).move_to(fuel_bg)
        fuel_lbl = Text("Carburant", font_size=13, color=TEXT_W).next_to(fuel_bg, UP, buff=0.08)

        s4 = sub_text("Carburant limité.\nComment traverser en dépensant le moins possible ?")
        self.play(FadeIn(s4), FadeIn(fuel_bg), FadeIn(fuel_bar), FadeIn(fuel_lbl))

        # Ship se fraye un chemin
        waypoints = [
            [-1.6, 0, 0], [-0.9, 0.7, 0], [0.1, -0.2, 0],
            [0.9, 0.5, 0], [2.5, 0, 0],
        ]
        for i, wp in enumerate(waypoints[1:]):
            self.play(
                ship.animate.move_to(wp),
                fuel_bar.animate.stretch(
                    max(0.05, 1 - 0.18 * (i + 1)), 0
                ).align_to(fuel_bg.get_left() + RIGHT * 0.06, LEFT),
                run_time=0.9, rate_func=linear,
            )

        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCÈNE 02 — Les zones interdites
# ═══════════════════════════════════════════
class Scene02_ZonesInterdites(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(make_stars())
        header = make_header("Les zones interdites")
        self.play(FadeIn(header))

        # ── 2.1 Bulle autour d'un astéroïde ──
        ast = asteroid_shape(0.42, seed=2).move_to(ORIGIN)
        self.play(FadeIn(ast))

        s1 = sub_text("Autour de chaque astéroïde :\nune zone interdite.")
        self.play(FadeIn(s1))

        bub1 = bubble(ORIGIN, radius=1.0)
        self.play(Create(bub1), run_time=1.0)
        self.wait(0.5)

        eq1 = MathTex(
            r"\|r - r_{\rm ast}\| \geq R + d_{\rm sec}",
            font_size=28, color=GOLD,
        ).move_to(UP * 2.2)
        eq1_lbl = Text("Contrainte d'évitement", font_size=13, color=MUTED).next_to(eq1, DOWN, buff=0.15)
        self.play(Write(eq1), FadeIn(eq1_lbl))

        s2 = sub_text("Trop près → collision.\nOn prend une marge de sécurité.")
        self.play(Transform(s1, s2))
        self.wait(1.5)

        # Plusieurs astéroïdes avec bulles
        asts_multi = VGroup(
            asteroid_shape(0.28, seed=5).move_to([-1.4,  1.5, 0]),
            asteroid_shape(0.34, seed=6).move_to([ 1.2, -0.8, 0]),
            asteroid_shape(0.22, seed=7).move_to([-0.6, -0.9, 0]),
        )
        bubs_multi = VGroup(*[
            bubble(a.get_center(), radius=0.65 + i * 0.08)
            for i, a in enumerate(asts_multi)
        ])
        self.play(FadeIn(asts_multi), FadeIn(bubs_multi), run_time=0.9)
        self.wait(1)
        self.play(FadeOut(s1), FadeOut(eq1), FadeOut(eq1_lbl),
                  FadeOut(ast), FadeOut(bub1), FadeOut(asts_multi), FadeOut(bubs_multi))

        # ── 2.2 Bulle du missile (mobile) ──
        s3 = sub_text("Même logique pour les missiles.")
        self.play(FadeIn(s3))

        mis = missile_dot([-1.8, 1.0, 0])
        bub_mis = bubble(mis.get_center(), radius=0.65, color=MISSILE_COL)
        self.play(FadeIn(mis), Create(bub_mis))

        eq2 = MathTex(
            r"\|r(t) - r_k(t)\| \geq d_{\rm mis}",
            font_size=28, color=GOLD,
        ).move_to(UP * 2.2)
        eq2_lbl = Text("Contrainte mobile", font_size=13, color=MUTED).next_to(eq2, DOWN, buff=0.15)
        self.play(Write(eq2), FadeIn(eq2_lbl))

        s4 = sub_text("Leur bulle bouge avec eux.\nÀ chaque instant, une zone change.")
        self.play(Transform(s3, s4))

        path_pts = [[-1.8, 1.0, 0], [-0.9, 0.3, 0], [0.2, -0.2, 0], [1.4, -0.8, 0]]
        for pt in path_pts[1:]:
            self.play(
                mis.animate.move_to(pt),
                bub_mis.animate.move_to(pt),
                run_time=0.7, rate_func=linear,
            )
        self.wait(1)
        self.play(FadeOut(s3), FadeOut(eq2), FadeOut(eq2_lbl), FadeOut(mis), FadeOut(bub_mis))

        # ── 2.3 Espace navigable ──
        s5 = sub_text("L'espace libre = tout l'espace\nminus les zones interdites.")
        self.play(FadeIn(s5))

        asts3 = VGroup(
            asteroid_shape(0.35, seed=1).move_to([-1.0,  1.2, 0]),
            asteroid_shape(0.40, seed=2).move_to([ 1.0, -0.4, 0]),
            asteroid_shape(0.28, seed=3).move_to([-0.2, -1.0, 0]),
        )
        bubs3 = VGroup(*[
            bubble(a.get_center(), radius=0.78 + i * 0.07)
            for i, a in enumerate(asts3)
        ])
        nav_rect = Rectangle(
            width=4.4, height=6.0,
            fill_color=NAV_COL, fill_opacity=0.06, stroke_width=0,
        ).move_to(UP * 0.3)
        nav_lbl = Text("Espace libre", font_size=16, color=NAV_COL).move_to([1.6, -2.0, 0])
        forb_lbl = Text("Zones interdites", font_size=14, color=MISSILE_COL).move_to([-1.4, -2.0, 0])

        self.play(FadeIn(nav_rect), FadeIn(asts3), FadeIn(bubs3))
        self.play(FadeIn(nav_lbl), FadeIn(forb_lbl))

        # Chemin qui contourne tout
        path_curve = CubicBezier(
            start_anchor=[-2.2, 0.5, 0],
            start_handle=[-1.5, 2.5, 0],
            end_handle=[1.5, -2.0, 0],
            end_anchor=[2.2, 0.2, 0],
            color=SHIP_COL, stroke_width=2,
        )
        s6 = sub_text("Naviguer = rester toujours\ndans cet espace libre.")
        self.play(Transform(s5, s6))
        self.play(Create(path_curve), run_time=1.5)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCÈNE 03 — Le coût du mouvement
# ═══════════════════════════════════════════
class Scene03_CoutMouvement(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(make_stars())
        header = make_header("Le coût du mouvement")
        self.play(FadeIn(header))

        # ── 3.1 Deux forces ──
        ship = ship_shape().move_to([-0.5, 0.5, 0])
        ast  = asteroid_shape(0.45, seed=3).move_to([1.4, 1.6, 0])
        self.play(FadeIn(ship), FadeIn(ast))

        grav_arrow = Arrow(
            ship.get_center(), ship.get_center() + np.array([0.8, 0.7, 0]),
            color=GRAV_COL, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.2,
        )
        grav_lbl = Text("Gravité\n(subi)", font_size=14, color=GRAV_COL).next_to(grav_arrow.get_end(), UR, buff=0.1)

        s1 = sub_text("Le vaisseau subit deux forces.")
        self.play(FadeIn(s1), Create(grav_arrow), FadeIn(grav_lbl))
        self.wait(1)

        thrust_arrow = Arrow(
            ship.get_center(), ship.get_center() + np.array([-0.9, -0.3, 0]),
            color=THRUST_COL, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.2,
        )
        thrust_lbl = Text("Poussée\n(contrôlée)", font_size=14, color=THRUST_COL).next_to(thrust_arrow.get_end(), DL, buff=0.1)

        s2 = sub_text("Gravité des astéroïdes (subi)\n+ Poussée du pilote (contrôlée).")
        self.play(Transform(s1, s2), Create(thrust_arrow), FadeIn(thrust_lbl))

        eq_mvt = MathTex(r"m\ddot{r} = F - m\nabla\Phi", font_size=30, color=GOLD).move_to([-0.2, -1.5, 0])
        eq_lbl = Text("Équation du mouvement", font_size=13, color=MUTED).next_to(eq_mvt, DOWN, buff=0.15)
        self.play(Write(eq_mvt), FadeIn(eq_lbl))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.6)

        # ── 3.2 Coût carburant ──
        s3 = sub_text("Chaque poussée consomme du carburant.")
        self.play(FadeIn(s3))

        axes = Axes(
            x_range=[0, 2.5, 1], y_range=[0, 6.5, 2],
            x_length=3.2, y_length=3.2,
            axis_config={"color": TEXT_W, "stroke_width": 1},
        ).move_to(UP * 0.8)
        ax_lbls = axes.get_axis_labels(
            MathTex(r"\|F\|", font_size=22, color=TEXT_W),
            MathTex(r"\text{coût}", font_size=22, color=TEXT_W),
        )
        cost_curve = axes.plot(lambda x: x ** 2, x_range=[0, 2.5], color=THRUST_COL, stroke_width=2)

        self.play(Create(axes), Write(ax_lbls))
        self.play(Create(cost_curve), run_time=0.9)

        eq_J = MathTex(r"J = \int_0^T \|F(t)\|^2\, dt", font_size=28, color=GOLD).move_to(DOWN * 1.6)
        eq_J_lbl = Text("Coût à minimiser", font_size=13, color=MUTED).next_to(eq_J, DOWN, buff=0.15)
        self.play(Write(eq_J), FadeIn(eq_J_lbl))

        s4 = sub_text("Le carré pénalise les grosses poussées.\n2 petits coups < 1 grand coup.")
        self.play(Transform(s3, s4))

        # Comparaison visuelle
        big_dot = Dot(axes.c2p(2.2, 4.84), color=MISSILE_COL, radius=0.1)
        sm_dot1 = Dot(axes.c2p(1.1, 1.21), color=NAV_COL, radius=0.09)
        sm_dot2 = Dot(axes.c2p(1.1, 1.21), color=NAV_COL, radius=0.09)
        big_val = Text("coût = 4.84", font_size=13, color=MISSILE_COL).next_to(big_dot, RIGHT, buff=0.1)
        sm_val  = Text("2 × 1.21 = 2.42 ✓", font_size=13, color=NAV_COL).next_to(sm_dot1, LEFT, buff=0.1)
        self.play(FadeIn(big_dot), FadeIn(big_val))
        self.play(FadeIn(sm_dot1), FadeIn(sm_val))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.6)

        # ── 3.3 Gravité gratuite ──
        s5 = sub_text("Mais la gravité, elle, est gratuite.")
        self.play(FadeIn(s5))

        ship2 = ship_shape().move_to([-2.0, -0.5, 0])
        ast2  = asteroid_shape(0.50, seed=4).move_to([0.3, 0.8, 0])
        self.play(FadeIn(ship2), FadeIn(ast2))

        free_path = ParametricFunction(
            lambda t: np.array([-2.0 + t * 4.2, -0.5 + 2.0 * np.sin(t * PI * 0.6), 0]),
            t_range=[0, 1], color=NAV_COL, stroke_width=2,
        )
        self.play(Create(free_path), run_time=1.2)
        free_lbl = Text("ΔJ = 0", font_size=26, color=NAV_COL).move_to([1.5, -1.5, 0])
        s6 = sub_text("Utiliser la gravité pour dévier\nsans dépenser de carburant.")
        self.play(Transform(s5, s6), Write(free_lbl))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCÈNE 04 — Le prix de la déviation
# ═══════════════════════════════════════════
class Scene04_PrixDeviation(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(make_stars())
        header = make_header("Le prix de la déviation")
        self.play(FadeIn(header))

        # ── 4.1 Survol d'un astéroïde ──
        ast = asteroid_shape(0.48, seed=5).move_to([0.5, 0.8, 0])
        self.play(FadeIn(ast))

        s1 = sub_text("Passage près d'un astéroïde :\nà l'approche, on accélère…")
        self.play(FadeIn(s1))

        # Flèches de gravité croissantes le long de la trajectoire
        approach_pts = [np.array([-1.8, -1.2 + i * 0.35, 0]) for i in range(5)]
        grav_arrows = VGroup(*[
            Arrow(
                pt,
                pt + normalize(np.array([0.5 + i * 0.2, 0.8 + i * 0.2, 0])) * (0.2 + i * 0.08),
                color=GRAV_COL, stroke_width=1.5, buff=0,
                max_tip_length_to_length_ratio=0.25,
            )
            for i, pt in enumerate(approach_pts)
        ])
        flyby = ParametricFunction(
            lambda t: np.array([-1.8 + t * 4.2, -1.2 + 2.2 * t * (1 - t * 0.7), 0]),
            t_range=[0, 1], color=SHIP_COL, stroke_width=1.8, stroke_opacity=0.7,
        )
        self.play(Create(flyby), Create(grav_arrows), run_time=1.2)

        s2 = sub_text("…puis en s'éloignant, la gravité\nnous retient — on ralentit.")
        self.play(Transform(s1, s2))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.5)

        # ── 4.2 L'astéroïde n'est pas fixe ──
        ast2  = asteroid_shape(0.48, seed=5).move_to([1.0, 0.5, 0])
        ship2 = ship_shape().move_to([-1.6, 0, 0])
        ast_v = Arrow([1.0, 0.5, 0], [1.5, 0.5, 0], color=ASTEROID_COL, stroke_width=1.8, buff=0)
        v_lbl = Text("v ≈ 0", font_size=14, color=ASTEROID_COL).next_to(ast_v, UP, buff=0.08)

        s3 = sub_text("L'astéroïde n'est pas fixe — il est libre.")
        self.play(FadeIn(ast2), FadeIn(ship2), FadeIn(ast_v), FadeIn(v_lbl), FadeIn(s3))
        self.wait(1)

        new_ast_v = Arrow([0.5, 0.3, 0], [-0.2, 0.3, 0], color=MISSILE_COL, stroke_width=1.8, buff=0)
        new_v_lbl = Text("v ≠ 0 !", font_size=14, color=MISSILE_COL).next_to(new_ast_v, UP, buff=0.08)
        s4 = sub_text("On s'approche → il est attiré vers nous.\nIl prend de la vitesse.")
        self.play(
            ast2.animate.move_to([0.5, 0.3, 0]),
            ship2.animate.move_to([-0.8, 0.1, 0]),
            Transform(ast_v, new_ast_v),
            Transform(v_lbl, new_v_lbl),
            Transform(s3, s4),
            run_time=1.5,
        )
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.5)

        # ── 4.3 Transfert d'énergie ──
        s5 = sub_text("L'énergie totale est conservée.")
        self.play(FadeIn(s5))

        e_bg_s = Rectangle(width=2.8, height=0.38, fill_color="#1e293b", fill_opacity=1,
                            stroke_color=TEXT_W, stroke_width=0.8).move_to([-0.2, 1.4, 0])
        e_bar_s = Rectangle(width=2.6, height=0.28, fill_color=SHIP_COL,
                             fill_opacity=0.9, stroke_width=0).move_to(e_bg_s)
        e_lbl_s = Text("Énergie vaisseau", font_size=14, color=SHIP_COL).next_to(e_bg_s, LEFT, buff=0.15)

        e_bg_a = Rectangle(width=2.8, height=0.38, fill_color="#1e293b", fill_opacity=1,
                            stroke_color=TEXT_W, stroke_width=0.8).move_to([-0.2, 0.7, 0])
        e_bar_a = Rectangle(width=0.12, height=0.28, fill_color=ASTEROID_COL,
                             fill_opacity=0.9, stroke_width=0).align_to(e_bg_a.get_left() + RIGHT * 0.06, LEFT)
        e_lbl_a = Text("Énergie astéroïde", font_size=14, color=ASTEROID_COL).next_to(e_bg_a, LEFT, buff=0.15)

        total = Text("E_total = cte", font_size=18, color=GOLD).move_to([0.2, 2.2, 0])
        self.play(FadeIn(total), FadeIn(e_bg_s), FadeIn(e_bar_s), FadeIn(e_lbl_s),
                  FadeIn(e_bg_a), FadeIn(e_bar_a), FadeIn(e_lbl_a))

        eq_tr = MathTex(
            r"\Delta K = -\frac{m^2 M}{(m+M)^2}v_0^2(1-\cos\theta)",
            font_size=22, color=GOLD,
        ).move_to([0.2, -1.0, 0])
        eq_tr_lbl = Text("Transfert d'énergie", font_size=13, color=MUTED).next_to(eq_tr, DOWN, buff=0.12)
        self.play(Write(eq_tr), FadeIn(eq_tr_lbl))

        s6 = sub_text("Astéroïde gagne de l'énergie\n→ vaisseau en perd.")
        self.play(Transform(s5, s6))
        self.play(
            e_bar_s.animate.stretch(0.45, 0).align_to(e_bg_s.get_left() + RIGHT * 0.06, LEFT),
            e_bar_a.animate.stretch(18, 0).align_to(e_bg_a.get_left() + RIGHT * 0.06, LEFT),
            run_time=1.5,
        )
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.5)

        # ── 4.4 Assistance gravitationnelle ──
        s7 = sub_text("Mais si l'astéroïde arrive VERS nous :\nassistance gravitationnelle !")
        self.play(FadeIn(s7))

        ast3 = asteroid_shape(0.48, seed=5).move_to([1.8, 0.5, 0])
        ship3 = ship_shape().move_to([-1.5, -0.3, 0])
        ast_coming = Arrow([1.8, 0.5, 0], [0.5, 0.5, 0], color=ASTEROID_COL, stroke_width=2, buff=0)
        self.play(FadeIn(ast3), FadeIn(ship3), FadeIn(ast_coming))

        self.play(
            ast3.animate.move_to([0.0, 0.2, 0]),
            ship3.animate.move_to([-0.5, -0.1, 0]),
            run_time=1.5,
        )

        gain_lbl = Text("ΔK > 0 !!", font_size=28, color=NAV_COL).move_to([0.5, -1.6, 0])
        assist_lbl = Text("Assistance\ngravitationnelle", font_size=18, color=NAV_COL, line_spacing=1.2).move_to([0.8, -2.5, 0])
        s8 = sub_text("Sondes Voyager, Cassini…\nont utilisé ce principe.")
        self.play(Write(gain_lbl), FadeIn(assist_lbl), Transform(s7, s8))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCÈNE 05 — Les missiles
# ═══════════════════════════════════════════
class Scene05_LesMissiles(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(make_stars())
        header = make_header("Les missiles")
        self.play(FadeIn(header))

        # ── 5.1 Missile balistique ──
        s1 = sub_text("Missile balistique : trajectoire\nentièrement prévisible.")
        self.play(FadeIn(s1))

        bal_path = ParametricFunction(
            lambda t: np.array([2.0 - t * 5.0, 2.0 + t * 2.5 - t ** 2 * 3.5, 0]),
            t_range=[0, 1.2], color=MISSILE_COL, stroke_width=2, stroke_opacity=0.6,
        )
        self.play(Create(bal_path), run_time=1.0)
        predict_lbl = Text("Prédictible à 100 %", font_size=16, color=MISSILE_COL).move_to([0.5, 1.0, 0])
        self.play(FadeIn(predict_lbl))
        self.wait(1.5)
        self.play(FadeOut(s1), FadeOut(bal_path), FadeOut(predict_lbl))

        # ── 5.2 Missile guidé ──
        s2 = sub_text("Missile guidé : observe le vaisseau\net corrige en permanence.")
        self.play(FadeIn(s2))

        ship = ship_shape().move_to([-1.6, 0, 0])
        mis2 = missile_dot([1.8, 2.0, 0])
        self.play(FadeIn(ship), FadeIn(mis2))

        for sp, mp in [
            ([-1.2, 0.5, 0], [1.2, 1.2, 0]),
            ([-0.4, -0.3, 0], [0.4, 0.4, 0]),
            ([ 0.5, -0.1, 0], [-0.1, -0.1, 0]),
        ]:
            los = DashedLine(np.array(mp), np.array(sp), color=LOS_COL,
                             stroke_width=1.2, stroke_opacity=0.7)
            self.play(
                ship.animate.move_to(sp),
                mis2.animate.move_to(mp),
                Create(los),
                run_time=0.65, rate_func=linear,
            )
            self.remove(los)

        s3 = sub_text("Impossible de calculer sa trajectoire\nà l'avance — elle dépend de nous.")
        self.play(Transform(s2, s3))
        self.wait(1.5)
        self.play(FadeOut(s2), FadeOut(ship), FadeOut(mis2))

        # ── 5.3 Ligne de visée ──
        s4 = sub_text("La ligne de visée σ :\nsegment missile → vaisseau.")
        self.play(FadeIn(s4))

        ship_p = [-1.8, -0.4, 0]
        mis_p  = [ 1.6,  1.2, 0]
        ship2  = ship_shape().move_to(ship_p)
        mis3   = missile_dot(mis_p)
        los_l  = Line(np.array(mis_p), np.array(ship_p), color=LOS_COL, stroke_width=2)
        los_lbl = Text("σ", font_size=28, color=LOS_COL).move_to([0.0, 0.6, 0])

        self.play(FadeIn(ship2), FadeIn(mis3))
        self.play(Create(los_l), FadeIn(los_lbl))

        len_brace = Brace(los_l, direction=normalize(np.array([-0.8, 1.6, 0])),
                          color=TEXT_W, buff=0.05)
        len_lbl = Text("‖σ‖ = distance", font_size=13, color=TEXT_W).next_to(len_brace, UL, buff=0.08)
        s5 = sub_text("Deux infos : distance ‖σ‖\net direction σ̂.")
        self.play(Transform(s4, s5), FadeIn(len_brace), FadeIn(len_lbl))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.5)

        # ── 5.4 LOS fixe = collision / tourne = raté ──
        s6 = sub_text("Ligne fixe → collision.\nLigne qui tourne → raté.")
        self.play(FadeIn(s6))

        # Cas 1 : ligne fixe (gauche de l'écran)
        lbl1 = Text("Fixe → Collision", font_size=14, color=MISSILE_COL).move_to([-1.5, 2.8, 0])
        s_c1 = ship_shape(scale=0.8).move_to([-2.0, 0.8, 0])
        m_c1 = missile_dot([-1.0, 2.3, 0])
        l_c1 = Line(m_c1.get_center(), s_c1.get_center(), color=MISSILE_COL, stroke_width=1.8)
        self.play(FadeIn(lbl1), FadeIn(s_c1), FadeIn(m_c1), Create(l_c1))

        for t in [0.33, 0.66, 1.0]:
            ns = np.array([-2.0 + t * 2.0, 0.8 - t * 0.5, 0])
            nm = np.array([-1.0 + t * 0.7, 2.3 - t * 0.7, 0])
            self.play(
                s_c1.animate.move_to(ns),
                m_c1.animate.move_to(nm),
                Transform(l_c1, Line(nm, ns, color=MISSILE_COL, stroke_width=1.8)),
                run_time=0.4, rate_func=linear,
            )

        # Cas 2 : ligne tourne (droite de l'écran)
        lbl2 = Text("Tourne → Raté", font_size=14, color=NAV_COL).move_to([1.3, 2.8, 0])
        s_c2 = ship_shape(scale=0.8).move_to([0.5, 0.5, 0])
        m_c2 = missile_dot([1.8, 2.0, 0])
        l_c2 = Line(m_c2.get_center(), s_c2.get_center(), color=NAV_COL, stroke_width=1.8)
        self.play(FadeIn(lbl2), FadeIn(s_c2), FadeIn(m_c2), Create(l_c2))

        for (ns2, nm2) in [
            ([1.2, 0.2, 0], [1.5, 1.1, 0]),
            ([1.9, -0.3, 0], [1.2, 0.3, 0]),
            ([2.2, -0.8, 0], [0.8, -0.5, 0]),
        ]:
            self.play(
                s_c2.animate.move_to(ns2),
                m_c2.animate.move_to(nm2),
                Transform(l_c2, Line(np.array(nm2), np.array(ns2), color=NAV_COL, stroke_width=1.8)),
                run_time=0.45, rate_func=linear,
            )
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.5)

        # ── 5.5 Navigation proportionnelle ──
        s7 = sub_text("Stratégie du missile : annuler\nla vitesse de rotation de σ.")
        self.play(FadeIn(s7))

        eq_pn = MathTex(r"F_{\rm missile} \propto \dot{\sigma}_\perp", font_size=40, color=GOLD).move_to(UP * 0.5)
        eq_pn_lbl = Text("Navigation proportionnelle", font_size=15, color=MUTED).next_to(eq_pn, DOWN, buff=0.2)
        self.play(Write(eq_pn), FadeIn(eq_pn_lbl))

        obj_box = SurroundingRectangle(
            Text("Notre objectif : faire TOURNER σ.", font_size=17, color=SHIP_COL).move_to(DOWN * 1.6),
            color=SHIP_COL, buff=0.12,
        )
        obj_lbl = Text("Notre objectif : faire TOURNER σ.", font_size=17, color=SHIP_COL).move_to(DOWN * 1.6)
        self.play(FadeIn(obj_lbl), Create(obj_box))
        s8 = sub_text("S'il maintient σ fixe → collision.\nNous : faire tourner σ.")
        self.play(Transform(s7, s8))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.5)

        # ── 5.6 Poussée perpendiculaire ──
        s9 = sub_text("Poussée parallèle : change la distance.\nPoussée ⊥ : fait tourner σ !")
        self.play(FadeIn(s9))

        ship3 = ship_shape().move_to([-1.0, 0, 0])
        mis4  = missile_dot([1.0, 0, 0])
        los2  = Line([1.0, 0, 0], [-1.0, 0, 0], color=LOS_COL, stroke_width=2)
        self.play(FadeIn(ship3), FadeIn(mis4), Create(los2))

        # Mauvaise poussée (parallèle)
        bad_arr = Arrow([-1.0, 0, 0], [-2.0, 0, 0], color=MISSILE_COL,
                        stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.2)
        bad_lbl = Text("∥ : le missile compense", font_size=13, color=MISSILE_COL).move_to([-1.5, -0.45, 0])
        self.play(Create(bad_arr), FadeIn(bad_lbl))
        self.wait(1)
        self.play(FadeOut(bad_arr), FadeOut(bad_lbl))

        # Bonne poussée (perpendiculaire)
        good_arr = Arrow([-1.0, 0, 0], [-1.0, -1.1, 0], color=NAV_COL,
                         stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.2)
        new_los  = Line([1.0, 0, 0], [-1.0, -1.0, 0], color=LOS_COL, stroke_width=2)
        good_lbl = Text("⊥ : σ tourne → missile dérouté !", font_size=13, color=NAV_COL).move_to([0.4, -1.8, 0])

        eq_los = MathTex(r"\frac{d\|\sigma\|}{dt} = \frac{\sigma \cdot \dot{\sigma}}{\|\sigma\|}",
                         font_size=26, color=GOLD).move_to([0.3, 1.8, 0])
        self.play(Create(good_arr), FadeIn(good_lbl))
        self.play(Transform(los2, new_los), Write(eq_los))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCÈNE 06 — Trouver un chemin
# ═══════════════════════════════════════════
class Scene06_TrouverUnChemin(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(make_stars())
        header = make_header("Trouver un chemin")
        self.play(FadeIn(header))

        # ── 6.1 Récapitulatif du problème ──
        s1 = sub_text("Trouver une trajectoire :\n• dans l'espace libre\n• qui minimise le carburant\n• face aux missiles.", font_size=14)
        self.play(FadeIn(s1))

        asts = VGroup(
            asteroid_shape(0.32, seed=1).move_to([-0.9,  1.5, 0]),
            asteroid_shape(0.38, seed=2).move_to([ 1.1, -0.2, 0]),
            asteroid_shape(0.26, seed=3).move_to([-0.3, -0.9, 0]),
        )
        bubs = VGroup(*[bubble(a.get_center(), 0.72 + i * 0.06) for i, a in enumerate(asts)])
        ship = ship_shape(scale=0.85).move_to([-2.2, 0, 0])
        mis  = missile_dot([2.0, 1.8, 0])
        mis_b = bubble([2.0, 1.8, 0], 0.6)

        self.play(FadeIn(asts), FadeIn(bubs), FadeIn(ship), FadeIn(mis), FadeIn(mis_b))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.5)

        # ── 6.2 Liste des contraintes ──
        s2 = sub_text("Les contraintes du problème :")
        self.play(FadeIn(s2))

        items = VGroup(
            VGroup(Dot(color=ASTEROID_COL, radius=0.07),
                   Text("Éviter les astéroïdes (fixe)", font_size=16, color=TEXT_W)).arrange(RIGHT, buff=0.2),
            VGroup(Dot(color=MISSILE_COL, radius=0.07),
                   Text("Éviter les missiles (mobile)", font_size=16, color=TEXT_W)).arrange(RIGHT, buff=0.2),
            VGroup(Dot(color=THRUST_COL, radius=0.07),
                   Text("Poussée maximale bornée", font_size=16, color=TEXT_W)).arrange(RIGHT, buff=0.2),
            VGroup(Dot(color=NAV_COL, radius=0.07),
                   Text("Arriver à destination", font_size=16, color=TEXT_W)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.48, aligned_edge=LEFT).move_to(UP * 0.7)

        for item in items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(s2), FadeOut(items))

        # ── 6.3 Espace dynamique ──
        s3 = sub_text("Le vrai défi : l'espace libre\nchange à chaque instant.")
        self.play(FadeIn(s3))

        t_lbl = Text("t = 0", font_size=22, color=GOLD).to_corner(UL, buff=0.55)
        self.play(FadeIn(t_lbl))

        asts2 = VGroup(
            asteroid_shape(0.35, seed=1).move_to([-0.8, 1.2, 0]),
            asteroid_shape(0.40, seed=2).move_to([ 0.7, -0.6, 0]),
        )
        bubs2 = VGroup(*[bubble(a.get_center(), 0.75 + i * 0.08) for i, a in enumerate(asts2)])
        mis2  = missile_dot([2.0,  1.0, 0])
        mis_b2 = bubble(mis2.get_center(), 0.68)

        self.play(FadeIn(asts2), FadeIn(bubs2), FadeIn(mis2), FadeIn(mis_b2))

        # Un chemin qui semble libre à t=0
        ok_path = Line([-2.2, 0.3, 0], [2.2, 0.3, 0], color=SHIP_COL, stroke_width=2, stroke_opacity=0.5)
        check_ok = Text("✓ chemin libre", font_size=14, color=NAV_COL).move_to([0.5, 0.75, 0])
        self.play(Create(ok_path), FadeIn(check_ok))
        self.wait(1)

        # Avance dans le temps → missile coupe le chemin
        new_t_lbl = Text("t = 2", font_size=22, color=GOLD).to_corner(UL, buff=0.55)
        s4 = sub_text("Un chemin valide maintenant\npeut être interdit dans 2 s.")
        self.play(
            Transform(t_lbl, new_t_lbl),
            mis2.animate.move_to([0.2, 0.1, 0]),
            mis_b2.animate.move_to([0.2, 0.1, 0]),
            Transform(s3, s4),
            run_time=1.2,
        )
        cross = Cross(scale_factor=0.35, color=MISSILE_COL).move_to([0.2, 0.3, 0])
        blocked = Text("✗ chemin bloqué", font_size=14, color=MISSILE_COL).move_to([0.8, 0.7, 0])
        self.play(FadeOut(check_ok), FadeIn(cross), FadeIn(blocked))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCÈNE 07 — Les trois principes
# ═══════════════════════════════════════════
class Scene07_TroisPrincipes(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(make_stars())
        header = make_header("Les trois principes")
        self.play(FadeIn(header))

        # ══ Principe 1 : Poussée perpendiculaire ══
        p1 = Text("① Pousser perpendiculairement à σ", font_size=18, color=SHIP_COL).move_to(UP * 2.8)
        self.play(FadeIn(p1))

        ship1 = ship_shape().move_to([-1.2, 0.6, 0])
        mis1  = missile_dot([1.2, -0.3, 0])
        los1  = Line([1.2, -0.3, 0], [-1.2, 0.6, 0], color=LOS_COL, stroke_width=1.8)
        self.play(FadeIn(ship1), FadeIn(mis1), Create(los1))

        bad_t = Arrow([-1.2, 0.6, 0], [-2.1, 0.6, 0], color=MISSILE_COL,
                      stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.22)
        bad_l = Text("✗ Fuir : missile compense", font_size=13, color=MISSILE_COL).move_to([-0.8, -0.2, 0])
        s1 = sub_text("Fuir en ligne droite ne sert à rien.\nLe missile accélère pour compenser.")
        self.play(Create(bad_t), FadeIn(bad_l), FadeIn(s1))
        self.wait(1.5)
        self.play(FadeOut(bad_t), FadeOut(bad_l))

        good_t = Arrow([-1.2, 0.6, 0], [-1.2, -0.5, 0], color=NAV_COL,
                       stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.22)
        new_los1 = Line([1.2, -0.3, 0], [-1.2, -0.5, 0], color=LOS_COL, stroke_width=1.8)
        rot_arc = Arc(radius=0.55,
                      start_angle=angle_of_vector(np.array([-1.2, 0.6, 0]) - np.array([1.2, -0.3, 0])),
                      angle=PI / 5, color=LOS_COL).move_to([1.2, -0.3, 0])
        good_l = Text("✓ Côté : σ tourne !", font_size=13, color=NAV_COL).move_to([0.5, 0.6, 0])
        s2 = sub_text("Pousser sur le côté : σ tourne.\nLe missile doit corriger — ça lui coûte du temps.")
        self.play(Create(good_t), Transform(los1, new_los1), Create(rot_arc), FadeIn(good_l), Transform(s1, s2))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.5)

        # ══ Principe 2 : Manœuvrer tard ══
        p2 = Text("② Manœuvrer le plus tard possible", font_size=18, color=SHIP_COL).move_to(UP * 2.8)
        self.play(FadeIn(p2))

        tl = NumberLine(x_range=[0, 10, 2], length=3.8, color=TEXT_W,
                        include_numbers=False).move_to(UP * 0.8)
        t_start = Text("Départ", font_size=13, color=TEXT_W).next_to(tl.n2p(0), DOWN, buff=0.2)
        t_end   = Text("Impact", font_size=13, color=MISSILE_COL).next_to(tl.n2p(10), DOWN, buff=0.2)
        self.play(Create(tl), FadeIn(t_start), FadeIn(t_end))

        early = Dot(tl.n2p(2), color=MISSILE_COL, radius=0.1)
        early_lbl = Text("Tôt ✗\n→ missile corrige", font_size=13,
                         color=MISSILE_COL, line_spacing=1.2).move_to(tl.n2p(2) + UP * 1.1)
        s3 = sub_text("Une manœuvre tôt : le missile\na le temps de corriger.")
        self.play(FadeIn(s3), FadeIn(early), FadeIn(early_lbl))
        self.wait(1.5)

        late = Dot(tl.n2p(8.5), color=NAV_COL, radius=0.1)
        late_lbl = Text("Tard ✓\n→ plus le temps !", font_size=13,
                        color=NAV_COL, line_spacing=1.2).move_to(tl.n2p(8.5) + UP * 1.1)
        s4 = sub_text("Une manœuvre tardive le prend\nde court. Risqué, mais efficace.")
        self.play(Transform(s3, s4), FadeIn(late), FadeIn(late_lbl))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.5)

        # ══ Principe 3 : Piège gravitationnel ══
        p3 = Text("③ Utiliser les astéroïdes comme pièges", font_size=16, color=SHIP_COL).move_to(UP * 2.9)
        self.play(FadeIn(p3))

        ast_trap = asteroid_shape(0.52, seed=7).move_to(ORIGIN)
        r_cap = 1.5
        cap_circle = Circle(radius=r_cap, fill_color=GRAV_COL, fill_opacity=0.07,
                            stroke_color=GRAV_COL, stroke_width=1.5).move_to(ORIGIN)
        cap_lbl = Text("Rayon de capture", font_size=13, color=GRAV_COL).move_to([0, -1.8, 0])

        eq_cap = MathTex(
            r"b_{\rm cap} = R\sqrt{1 + \frac{2GM}{Rv_\infty^2}}",
            font_size=22, color=GOLD,
        ).move_to(UP * 2.1)
        eq_cap_lbl = Text("Rayon de capture", font_size=12, color=MUTED).next_to(eq_cap, DOWN, buff=0.1)

        s5 = sub_text("Le vaisseau passe juste à l'extérieur.\nLe missile, qui suit, est capturé.")
        self.play(FadeIn(ast_trap), Create(cap_circle), FadeIn(cap_lbl))
        self.play(Write(eq_cap), FadeIn(eq_cap_lbl), FadeIn(s5))

        # Vaisseau passe à l'extérieur
        ship_trap_path = ParametricFunction(
            lambda t: np.array([-2.1 + t * 4.3,
                                 -1.5 + t * 1.2 + np.exp(-((t - 0.5) / 0.25) ** 2) * 1.65, 0]),
            t_range=[0, 1], color=SHIP_COL, stroke_width=1.8,
        )
        ship_trap = ship_shape(scale=0.8).move_to([-2.1, -1.5, 0])
        self.play(FadeIn(ship_trap), Create(ship_trap_path), run_time=1.0)
        self.play(MoveAlongPath(ship_trap, ship_trap_path), run_time=2.0, rate_func=linear)

        # Missile capturé
        mis_trap = missile_dot([-1.8, -1.2, 0])
        mis_cap_path = ParametricFunction(
            lambda t: np.array([-1.8 + t * 3.5,
                                 -1.2 + t * 0.9 + np.exp(-((t - 0.55) / 0.22) ** 2) * (0.8 - 1.4 * t), 0]),
            t_range=[0, 1], color=MISSILE_COL, stroke_width=1.8, stroke_opacity=0.6,
        )
        self.play(FadeIn(mis_trap))
        self.play(MoveAlongPath(mis_trap, mis_cap_path), run_time=2.5, rate_func=linear)

        # Explosion
        boom = VGroup(*[
            Line(ORIGIN, rotate_vector(RIGHT * 0.55, i * PI / 4), color=MISSILE_COL, stroke_width=2.5)
            for i in range(8)
        ])
        self.play(FadeIn(boom))
        self.wait(0.8)
        self.play(FadeOut(boom))
        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCÈNE 08 — La flotte
# ═══════════════════════════════════════════
class Scene08_LaFlotte(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(make_stars())
        header = make_header("La flotte")
        self.play(FadeIn(header))

        s1 = sub_text("Avec plusieurs vaisseaux,\nles interactions se multiplient.")
        self.play(FadeIn(s1))

        # Flotte de 3 vaisseaux
        fleet_pos = [[-1.5, 0.8, 0], [-1.8, -0.3, 0], [-1.2, -1.1, 0]]
        fleet = VGroup(*[ship_shape(scale=0.85).move_to(pos) for pos in fleet_pos])
        self.play(FadeIn(fleet))

        # Liens gravitationnels entre vaisseaux
        grav_links = VGroup(
            DashedLine(fleet[0].get_center(), fleet[1].get_center(),
                       color=GRAV_COL, stroke_width=1.2, stroke_opacity=0.5),
            DashedLine(fleet[1].get_center(), fleet[2].get_center(),
                       color=GRAV_COL, stroke_width=1.2, stroke_opacity=0.5),
            DashedLine(fleet[0].get_center(), fleet[2].get_center(),
                       color=GRAV_COL, stroke_width=1.2, stroke_opacity=0.5),
        )
        peloton_lbl = Text("Effet de peloton\ngravitationnel", font_size=15,
                           color=GRAV_COL, line_spacing=1.2).move_to([0.8, 1.5, 0])
        s2 = sub_text("Les vaisseaux s'attirent mutuellement :\neffet de peloton gravitationnel.")
        self.play(Transform(s1, s2), Create(grav_links), FadeIn(peloton_lbl))
        self.wait(1.5)

        # Deux missiles entrent
        mis_a = missile_dot([2.2, 1.2, 0])
        mis_b = missile_dot([2.2, -0.2, 0])
        self.play(FadeIn(mis_a), FadeIn(mis_b))
        self.wait(0.8)

        # Vaisseau 0 = leurre
        decoy_lbl = Text("Leurre", font_size=16, color=LOS_COL).next_to(fleet[0], UP, buff=0.15)
        s3 = sub_text("Un vaisseau fait le leurre.\nIl attire les missiles pendant\nque les autres fuient.", font_size=14)
        self.play(Transform(s1, s3), FadeIn(decoy_lbl))

        # Les 2 autres fuient vers la droite
        # Les missiles foncent sur le leurre
        self.play(
            fleet[1].animate.move_to([1.2, -0.3, 0]),
            fleet[2].animate.move_to([0.8, -1.1, 0]),
            mis_a.animate.move_to([-1.4, 0.8, 0]),
            mis_b.animate.move_to([-1.5, -0.3, 0]),
            run_time=2.0, rate_func=linear,
        )

        self.play(
            fleet[1].animate.move_to([2.2, -0.3, 0]),
            fleet[2].animate.move_to([2.0, -1.1, 0]),
            run_time=1.0, rate_func=linear,
        )

        # Explosion du leurre
        boom = VGroup(*[
            Line(fleet[0].get_center(),
                 fleet[0].get_center() + rotate_vector(RIGHT * 0.6, i * PI / 4),
                 color=MISSILE_COL, stroke_width=2.5)
            for i in range(8)
        ])
        escape_lbl = Text("Échappent !", font_size=16, color=NAV_COL).move_to([2.0, -1.8, 0])
        self.play(FadeOut(fleet[0]), FadeIn(boom), FadeIn(escape_lbl))
        self.wait(1.2)
        self.play(FadeOut(boom))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCÈNE 09 — Synthèse
# ═══════════════════════════════════════════
class Scene09_Synthese(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(make_stars())

        # Carte titre
        title = Text("Synthèse", font_size=40, color=GOLD).move_to(UP * 0.5)
        self.play(FadeIn(title, shift=UP * 0.4), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(title))

        header = make_header("Synthèse")
        self.play(FadeIn(header))

        # ── Récapitulatif visuel compact ──
        s1 = sub_text("Chaque obstacle → une bulle interdite.\nNaviguer = rester dans l'espace libre.")
        self.play(FadeIn(s1))

        asts = VGroup(
            asteroid_shape(0.30, seed=1).move_to([-1.2, 1.2, 0]),
            asteroid_shape(0.36, seed=2).move_to([ 0.9, -0.2, 0]),
            asteroid_shape(0.24, seed=3).move_to([-0.3, -0.8, 0]),
        )
        bubs = VGroup(*[bubble(a.get_center(), 0.68 + i * 0.07) for i, a in enumerate(asts)])
        mis  = missile_dot([1.8, 1.5, 0])
        mis_b = bubble(mis.get_center(), 0.6)

        self.play(FadeIn(asts), FadeIn(bubs), FadeIn(mis), FadeIn(mis_b))

        for pos in [[0.8, 0.5, 0], [-0.2, -0.1, 0]]:
            self.play(mis.animate.move_to(pos), mis_b.animate.move_to(pos),
                      run_time=0.8, rate_func=linear)

        s2 = sub_text("Les déviations coûtent de l'énergie,\nsauf l'assistance gravitationnelle.")
        self.play(Transform(s1, s2))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header], run_time=0.5)

        # ── Trois principes ──
        s3 = sub_text("Contre un missile guidé :")
        self.play(FadeIn(s3))

        principles = VGroup(
            VGroup(Text("①", font_size=26, color=GOLD),
                   Text("Pousser ⊥ à la ligne\nde visée", font_size=16, color=TEXT_W, line_spacing=1.2)
                   ).arrange(RIGHT, buff=0.3),
            VGroup(Text("②", font_size=26, color=GOLD),
                   Text("Manœuvrer le plus\ntard possible", font_size=16, color=TEXT_W, line_spacing=1.2)
                   ).arrange(RIGHT, buff=0.3),
            VGroup(Text("③", font_size=26, color=GOLD),
                   Text("Utiliser les astéroïdes\ncomme pièges", font_size=16, color=TEXT_W, line_spacing=1.2)
                   ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(UP * 0.6)

        for p in principles:
            self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(1)

        punchline = Text(
            "La différence entre un bon pilote\net un pilote optimal :\nce qu'il reste dans le réservoir.",
            font_size=17, color=GOLD, line_spacing=1.35,
        ).move_to(DOWN * 2.0)
        s4 = sub_text("Survivre ne suffit pas.\nL'optimum, c'est arriver avec du carburant.")
        self.play(Transform(s3, s4), Write(punchline), run_time=1.5)
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCÈNE 10 — CTA
# ═══════════════════════════════════════════
class Scene10_CTA(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Étoiles plus denses et brillantes
        rng = np.random.RandomState(99)
        stars = VGroup(*[
            Dot(
                point=[rng.uniform(-2.2, 2.2), rng.uniform(-4, 4), 0],
                radius=rng.uniform(0.01, 0.04),
                color=TEXT_W,
                fill_opacity=rng.uniform(0.15, 1.0),
            )
            for _ in range(120)
        ])
        self.add(stars)

        # Vaisseaux qui traversent l'écran
        ship_a = ship_shape(scale=0.6).move_to([-2.5,  3.2, 0])
        ship_b = ship_shape(scale=0.5).move_to([-2.5, -3.0, 0])
        self.add(ship_a, ship_b)

        # Logo TerreMathématiques
        logo_terre = Text("Terre", font_size=52, color=GOLD, weight=BOLD)
        logo_math  = Text("Mathématiques", font_size=36, color=TEXT_W)
        logo = VGroup(logo_terre, logo_math).arrange(DOWN, buff=0.15).move_to(UP * 1.2)
        underline = Line(logo.get_left(), logo.get_right(), color=GOLD, stroke_width=1.5).next_to(logo, DOWN, buff=0.2)

        self.play(
            FadeIn(logo, shift=UP * 0.5),
            Create(underline),
            ship_a.animate.move_to([2.5, 3.2, 0]),
            ship_b.animate.move_to([2.5, -3.0, 0]),
            run_time=1.5, rate_func=linear,
        )

        # Texte abonnement
        abonne = Text("Abonnez-vous", font_size=34, color=GOLD).move_to(DOWN * 0.4)
        reason = Text(
            "pour ne pas rater les prochaines vidéos\nsur les maths qui expliquent le monde",
            font_size=19, color=TEXT_W, line_spacing=1.4,
        ).move_to(DOWN * 1.5)

        self.play(FadeIn(abonne, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(reason), run_time=0.8)

        # Cloche notification (simplifiée avec Manim)
        bell_arc   = Arc(radius=0.35, start_angle=0, angle=PI, color=GOLD, stroke_width=3)
        bell_base  = Line(LEFT * 0.35, RIGHT * 0.35, color=GOLD, stroke_width=3)
        bell_dot   = Dot(DOWN * 0.48, color=GOLD, radius=0.07)
        bell_group = VGroup(bell_arc, bell_base, bell_dot).move_to(RIGHT * 1.4 + DOWN * 0.4)
        self.play(FadeIn(bell_group), run_time=0.5)

        # Clignotement final du logo
        self.play(
            logo_terre.animate.set_color(TEXT_W),
            logo_math.animate.set_color(GOLD),
            rate_func=there_and_back, run_time=1.0,
        )

        # Nouveaux vaisseaux qui traversent
        ship_c = ship_shape(scale=0.55).move_to([-2.5, 0.8, 0])
        self.add(ship_c)
        self.play(ship_c.animate.move_to([2.5, 0.8, 0]), run_time=2.5, rate_func=linear)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.2)
