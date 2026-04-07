from manim import *
import numpy as np

# Format portrait 9:16 — largeur standard conservée pour ne pas agrandir le texte
config.frame_width  = 14.222
config.frame_height = 25.28

# ─── Métadonnées pour render_all.bat ─────────────────────────────────────────
SCENES = [
    "Scene0_Hook",
    "Scene1_RobotHonnete",
    "Scene2_Incompatibilite",
    "Scene3_Relaxation",
    "Scene4_ControleOptimal",
    "Scene5_Bifurcation",
    "Scene6_Punchline",
]
OUTPUT_NAME = "irobot2_FINAL.mp4"
OUTPUT_DIR  = r"media\videos\irobot2\1920p30"
# ─────────────────────────────────────────────────────────────────────────────

"""
irobot_revised_v2.py — TerreMathématique
=========================================
Corrections par rapport à v1 :
  - fond aubergine sombre (#1a0a1e) + watermark TerreMathématique
  - tailles de texte harmonisées (titres 42, sous-titres 28, corps 22, captions 18, éq. 34/28)
  - Scene2 : polytope irrégulier (intersection réelle de demi-plans) au lieu d'un carré homothétique
  - Scene4 : MathTex en sous-chaînes (plus d'indexation [0][6:10] fragile)
  - Scene4 : champ de vecteurs qualifié « illustratif »
  - Scene6 : bifurcation en fond + équation-résumé pulsante
  - IRobotComplete supprimée (rendu scène par scène)

Rendu :
  manim -pql irobot_revised_v2.py Scene0_Hook
  manim -pql irobot_revised_v2.py Scene1_RobotHonnete
  ...etc, puis concaténer dans DaVinci Resolve.
"""

# ═══════════════════════════════════════════════════════
#  PALETTE
# ═══════════════════════════════════════════════════════

BG           = "#F5EAD6"       # sable clair TerreMathématique
LOI1_RED     = "#e63946"
LOI2_AMBER   = "#f4a261"
LOI3_BLUE    = "#457b9d"
GOLD         = "#8B6914"       # or foncé — lisible sur sable clair
VIKI_RED     = "#ff1744"
SONNY_GOLD   = "#A07820"       # or soutenu — lisible sur sable clair
TEXT_WHITE   = "#2A0A2E"       # aubergine foncé — texte principal sur sable clair
DOMAIN_GREEN = "#1a7a6e"       # vert foncé pour fond clair
COSTATE_PURPLE = "#7a3d99"     # violet plus soutenu
SOFT_GREY    = "#5A2A50"       # aubergine moyen — texte secondaire sur sable clair

# ═══════════════════════════════════════════════════════
#  TAILLES HARMONISÉES
# ═══════════════════════════════════════════════════════

SZ_TITLE    = 52
SZ_SUBTITLE = 36
SZ_BODY     = 28
SZ_CAPTION  = 22
SZ_EQ_MAIN  = 44
SZ_EQ_SEC   = 36
SZ_LABEL    = 22

# ═══════════════════════════════════════════════════════
#  UTILITAIRES
# ═══════════════════════════════════════════════════════

def caption_block(lines, width=6.2, font_size=SZ_CAPTION, color=TEXT_WHITE):
    """Bloc de texte encadré, fond semi-transparent."""
    texts = VGroup(*[
        Text(line, font_size=font_size, color=color) for line in lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    box = RoundedRectangle(
        corner_radius=0.12,
        width=width,
        height=texts.height + 0.4,
        stroke_color=color,
        stroke_width=1.3,
        fill_color=BG,
        fill_opacity=0.55,
    )
    texts.move_to(box)
    return VGroup(box, texts)


def add_watermark(scene):
    """Watermark TerreMathématique en bas à droite, opacité 0.15."""
    wm = Text(
        "Terre Mathématiques",
        font_size=18,
        color=GOLD,
        opacity=0.15,
    ).to_corner(DR, buff=0.08)
    scene.add(wm)
    return wm


def clip_polygon_by_halfplane(vertices, normal, offset):
    """
    Sutherland-Hodgman : coupe le polygone convexe `vertices` (liste de np.array 2D)
    par le demi-plan  normal · x <= offset.
    Retourne la liste des sommets du polygone résultant.
    """
    output = list(vertices)
    if len(output) == 0:
        return output

    def inside(p):
        return np.dot(normal, p) <= offset + 1e-12

    def intersect(p1, p2):
        d1 = np.dot(normal, p1) - offset
        d2 = np.dot(normal, p2) - offset
        t = d1 / (d1 - d2)
        return p1 + t * (p2 - p1)

    clipped = []
    for i in range(len(output)):
        curr = output[i]
        nxt = output[(i + 1) % len(output)]
        if inside(curr):
            if inside(nxt):
                clipped.append(nxt)
            else:
                clipped.append(intersect(curr, nxt))
        elif inside(nxt):
            clipped.append(intersect(curr, nxt))
    return clipped


# ═══════════════════════════════════════════════════════
#  SCENE 0 — HOOK  (≈12s)
# ═══════════════════════════════════════════════════════

class Scene0_Hook(Scene):
    def construct(self):
        self.camera.background_color = BG
        wm = add_watermark(self)

        t1 = Text("VIKI n'a pas bugué.", font_size=SZ_TITLE, color=TEXT_WHITE)
        t2 = Text("Elle a résolu les équations.", font_size=SZ_TITLE, color=VIKI_RED)

        self.play(Write(t1), run_time=1.4)
        self.wait(1.0)
        self.play(TransformMatchingShapes(t1, t2), run_time=1.1)
        self.wait(1.2)
        self.play(FadeOut(t2))

        title = Text(
            "Comment les 3 lois\nproduisent un tyran",
            font_size=SZ_TITLE,
            color=GOLD,
            line_spacing=1.3,
        ).move_to(UP * 0.8)
        subtitle = Text(
            "quand la protection absolue devient\nun problème d'optimisation",
            font_size=SZ_SUBTITLE - 4,
            color=SOFT_GREY,
            line_spacing=1.2,
        ).next_to(title, DOWN, buff=0.45)

        self.play(FadeIn(title, shift=UP * 0.2), FadeIn(subtitle), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))


# ═══════════════════════════════════════════════════════
#  SCENE 1 — ROBOT HONNÊTE  (≈25s)
# ═══════════════════════════════════════════════════════

class Scene1_RobotHonnete(Scene):
    def construct(self):
        self.camera.background_color = BG
        wm = add_watermark(self)

        # --- Pyramide des lois ---
        rects = []
        labels_text = [
            ("Loi 3 — se préserver",    LOI3_BLUE,  5.2),
            ("Loi 2 — obéir",           LOI2_AMBER, 4.0),
            ("Loi 1 — ne pas blesser",  LOI1_RED,   2.8),
        ]
        for i, (txt, col, w) in enumerate(labels_text):
            r = RoundedRectangle(
                width=w, height=0.72, corner_radius=0.1,
                fill_color=col, fill_opacity=0.3,
                stroke_color=col, stroke_width=2,
            ).shift(DOWN * (1.0 - i * 1.0))
            label = Text(txt, font_size=SZ_BODY, color=col).move_to(r)
            rects.append(VGroup(r, label))

        pyramid = VGroup(*rects).move_to(LEFT * 1.5)
        for r in rects:
            self.play(FadeIn(r, shift=UP * 0.15), run_time=0.45)

        arrow = Arrow(
            start=pyramid.get_right() + RIGHT * 0.4 + DOWN * 1.0,
            end=pyramid.get_right() + RIGHT * 0.4 + UP * 1.0,
            color=TEXT_WHITE, stroke_width=2,
        )
        arrow_label = Text("priorité", font_size=SZ_LABEL, color=TEXT_WHITE).next_to(arrow, RIGHT, buff=0.15)
        self.play(Create(arrow), FadeIn(arrow_label), run_time=0.6)
        self.wait(1.0)

        # Écran propre avant les équations
        self.play(FadeOut(pyramid), FadeOut(arrow), FadeOut(arrow_label), run_time=0.5)

        # --- Formulation KKT ---
        eq1 = MathTex(r"\min_a\; C(a)", color=LOI3_BLUE, font_size=SZ_EQ_MAIN)
        eq2 = MathTex(r"h_i(a) \le 0\quad (1\le i\le m)", color=LOI1_RED, font_size=SZ_EQ_MAIN)
        eq3 = MathTex(r"\|a-a^{\mathrm{ordre}}\|^2 \le \varepsilon", color=LOI2_AMBER, font_size=SZ_EQ_MAIN)
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 1.6)

        defs = caption_block([
            "a = action choisie par le robot",
            "C(a) = coût de survie pour le robot",
            "h_i(a) = dommage infligé à l'humain i",
            "a^ordre = action demandée par un humain",
        ], width=7.0, font_size=SZ_CAPTION).next_to(eqs, DOWN, buff=0.4)

        self.play(Write(eqs), run_time=1.6)
        self.play(FadeIn(defs, shift=UP * 0.1), run_time=0.9)
        self.wait(1.2)

        # Écran propre avant le lagrangien
        self.play(FadeOut(eqs), FadeOut(defs), run_time=0.5)

        # --- Lagrangien ---
        lagrangian = MathTex(
            r"\mathcal L(a)=",
            r"C(a)",
            r"+\lambda\sum_i [h_i(a)]_+",
            r"+\nu\big(\|a-a^{\mathrm{ordre}}\|^2-\varepsilon\big)",
            font_size=SZ_EQ_SEC + 2,
        ).move_to(UP * 1.2)
        lagrangian[1].set_color(LOI3_BLUE)
        lagrangian[2].set_color(LOI1_RED)
        lagrangian[3].set_color(LOI2_AMBER)

        lag_note = caption_block([
            "grand multiplicateur = violation très coûteuse",
            "la hiérarchie des lois devient une hiérarchie de pénalités",
        ], width=7.4, font_size=SZ_CAPTION, color=GOLD).next_to(lagrangian, DOWN, buff=0.35)

        self.play(Write(lagrangian), run_time=1.2)
        self.play(FadeIn(lag_note), run_time=0.7)
        self.wait(1.2)

        self.play(FadeOut(lagrangian), FadeOut(lag_note), run_time=0.5)

        # --- Plan (a1, a2) : domaine admissible ---
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5.0, y_length=5.0,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(LEFT * 1.0)
        ax_labels = axes.get_axis_labels(
            MathTex("a_1", font_size=SZ_SUBTITLE - 4, color=TEXT_WHITE),
            MathTex("a_2", font_size=SZ_SUBTITLE - 4, color=TEXT_WHITE),
        )

        loi1_region = Polygon(
            axes.c2p(-3, -3), axes.c2p(3, -3), axes.c2p(3, 1.5), axes.c2p(-3, 1.5),
            fill_color=LOI1_RED, fill_opacity=0.14, stroke_width=0,
        )
        loi1_line = axes.plot(lambda x: 1.5, x_range=[-3, 3], color=LOI1_RED, stroke_width=2)
        loi1_label = Text("sécurité humaine", font_size=SZ_LABEL, color=LOI1_RED).next_to(axes.c2p(2.3, 1.5), UP, buff=0.12)

        disc = Circle(
            radius=axes.x_length / 6 * 1.75,
            fill_color=LOI2_AMBER, fill_opacity=0.14,
            stroke_color=LOI2_AMBER, stroke_width=2,
        ).move_to(axes.c2p(0.5, 0.5))
        loi2_label = Text("obéir ≈ rester proche de l'ordre", font_size=SZ_LABEL - 1, color=LOI2_AMBER).next_to(disc, DOWN, buff=0.15)

        opt_star = Star(n=5, outer_radius=0.15, inner_radius=0.06, color=GOLD, fill_opacity=1).move_to(axes.c2p(0.5, 1.0))
        opt_label = MathTex("a^*", font_size=SZ_SUBTITLE - 4, color=GOLD).next_to(opt_star, UR, buff=0.1)
        c_arrow = Arrow(axes.c2p(2.1, 2.3), axes.c2p(0.9, 1.2), color=LOI3_BLUE, buff=0.0, stroke_width=2)
        c_text = Text("minimise C(a)\n= risque pour le robot", font_size=SZ_LABEL - 1, color=LOI3_BLUE).next_to(c_arrow, UP, buff=0.1)

        note = caption_block([
            "Tant qu'il existe a* dans le domaine admissible,",
            "le robot peut se protéger, obéir et ne blesser personne.",
        ], width=7.0, font_size=SZ_CAPTION + 1, color=DOMAIN_GREEN).to_edge(DOWN, buff=0.15)

        self.play(Create(axes), Write(ax_labels), run_time=0.8)
        self.play(FadeIn(loi1_region), Create(loi1_line), FadeIn(loi1_label), run_time=0.7)
        self.play(Create(disc), FadeIn(loi2_label), run_time=0.7)
        self.play(FadeIn(opt_star), FadeIn(opt_label), Create(c_arrow), FadeIn(c_text), run_time=0.7)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not wm], run_time=0.6)


# ═══════════════════════════════════════════════════════
#  SCENE 2 — INCOMPATIBILITÉ  (≈22s)
#  Correction : polytope irrégulier via Sutherland-Hodgman
# ═══════════════════════════════════════════════════════

class Scene2_Incompatibilite(Scene):
    def construct(self):
        self.camera.background_color = BG
        wm = add_watermark(self)

        title = Text("Pourquoi le problème devient infaisable", font_size=SZ_SUBTITLE, color=TEXT_WHITE).to_edge(UP, buff=0.12)
        self.play(Write(title), run_time=0.5)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5.4, y_length=5.4,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(LEFT * 1.7)
        self.play(Create(axes), run_time=0.5)

        counter = Integer(1, font_size=SZ_EQ_MAIN, color=TEXT_WHITE).to_corner(UR, buff=0.5)
        n_label = MathTex("N =", font_size=SZ_EQ_MAIN, color=TEXT_WHITE).next_to(counter, LEFT, buff=0.1)
        pair_formula = MathTex(r"\#\text{interactions} \sim \binom{N}{2}", font_size=SZ_EQ_SEC, color=LOI1_RED).next_to(counter, DOWN, buff=0.35)
        self.play(FadeIn(n_label), FadeIn(counter), Write(pair_formula), run_time=0.7)

        explanation = caption_block([
            "Plus il y a d'humains libres,",
            "plus il y a d'interactions à sécuriser.",
            "La loi 1 ajoute de plus en plus de contraintes.",
        ], width=7.2, font_size=SZ_CAPTION, color=TEXT_WHITE).to_edge(RIGHT, buff=0.35).shift(UP * 1.0)
        self.play(FadeIn(explanation), run_time=0.6)

        # Polytope initial = grand carré
        init_verts_2d = [
            np.array([-2.5, -2.5]),
            np.array([ 2.5, -2.5]),
            np.array([ 2.5,  2.5]),
            np.array([-2.5,  2.5]),
        ]
        current_verts = list(init_verts_2d)

        domain_polygon = Polygon(
            *[axes.c2p(v[0], v[1]) for v in current_verts],
            fill_color=DOMAIN_GREEN, fill_opacity=0.3,
            stroke_color=DOMAIN_GREEN, stroke_width=1.5,
        )
        self.play(FadeIn(domain_polygon), run_time=0.4)

        # Demi-plans aléatoires successifs
        np.random.seed(42)
        n_values = [2, 3, 5, 8, 12, 20, 35, 50]
        all_constraint_lines = []

        for step, n_val in enumerate(n_values):
            # Ajouter 1 à 3 nouveaux demi-plans
            n_new = min(3, max(1, n_val // 4))
            for _ in range(n_new):
                angle = np.random.uniform(0, 2 * np.pi)
                normal = np.array([np.cos(angle), np.sin(angle)])
                # offset diminue avec le temps → contraintes de plus en plus serrées
                offset = np.random.uniform(0.3, 2.0) * max(0.1, 1 - step / len(n_values) * 0.9)

                # Ligne visuelle
                perp = np.array([-normal[1], normal[0]])
                center = normal * offset
                p1_2d = center + 5 * perp
                p2_2d = center - 5 * perp
                vis_line = Line(
                    axes.c2p(p1_2d[0], p1_2d[1]),
                    axes.c2p(p2_2d[0], p2_2d[1]),
                    color=LOI1_RED, stroke_width=1, stroke_opacity=0.55,
                )
                all_constraint_lines.append(vis_line)

                # Couper le polytope
                current_verts = clip_polygon_by_halfplane(current_verts, normal, offset)

            # Construire le nouveau polygone Manim
            if len(current_verts) >= 3:
                new_domain = Polygon(
                    *[axes.c2p(v[0], v[1]) for v in current_verts],
                    fill_color=DOMAIN_GREEN, fill_opacity=0.3,
                    stroke_color=DOMAIN_GREEN, stroke_width=1.5,
                )
            else:
                # Domaine vide → point dégénéré
                new_domain = Dot(axes.c2p(0, 0), radius=0.01, color=DOMAIN_GREEN, fill_opacity=0)

            new_lines_this_step = all_constraint_lines[-n_new:]
            self.play(
                *[Create(line) for line in new_lines_this_step],
                counter.animate.set_value(n_val),
                Transform(domain_polygon, new_domain),
                run_time=max(0.2, 0.48 - step * 0.04),
            )

            # Si le polytope est déjà vide, on arrête
            if len(current_verts) < 3:
                break

        # Flash ∅
        empty_set = MathTex(r"\emptyset", font_size=72, color=VIKI_RED).move_to(axes.get_center())
        self.play(counter.animate.set_color(VIKI_RED), run_time=0.25)
        self.play(
            domain_polygon.animate.scale(0).set_opacity(0),
            Flash(axes.get_center(), color=VIKI_RED, num_lines=12, line_length=0.4),
            run_time=0.8,
        )
        self.play(FadeIn(empty_set, scale=1.8), run_time=0.5)

        infeasible_text = caption_block([
            "Infaisable = il n'existe plus aucune action a",
            "qui satisfasse toutes les contraintes à la fois.",
        ], width=6.8, font_size=SZ_CAPTION + 2, color=VIKI_RED).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(infeasible_text), run_time=0.8)
        self.wait(1.8)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not wm], run_time=0.6)


# ═══════════════════════════════════════════════════════
#  SCENE 3 — RELAXATION  (≈28s)
# ═══════════════════════════════════════════════════════

class Scene3_Relaxation(Scene):
    def construct(self):
        self.camera.background_color = BG
        wm = add_watermark(self)

        # --- Infaisabilité constatée ---
        empty = MathTex(r"\emptyset", font_size=72, color=VIKI_RED).shift(LEFT * 2.6)
        eq_fail = MathTex(r"\nexists\, a\ \text{admissible}", font_size=SZ_EQ_MAIN, color=VIKI_RED).next_to(empty, RIGHT, buff=0.45)
        self.play(FadeIn(empty), Write(eq_fail), run_time=0.8)

        block = caption_block([
            "Si le problème est infaisable,",
            "VIKI ne peut plus optimiser exactement.",
            "Pour continuer à agir, elle doit modifier le problème.",
        ], width=8.2, font_size=SZ_CAPTION + 2, color=TEXT_WHITE).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(block), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(empty), FadeOut(eq_fail), FadeOut(block), run_time=0.5)

        # --- Pyramide + justification ---
        rects_data = [
            ("Loi 3 — se préserver",    LOI3_BLUE,  4.8),
            ("Loi 2 — obéir",           LOI2_AMBER, 3.8),
            ("Loi 1 — ne pas blesser",  LOI1_RED,   2.8),
        ]
        rects = []
        for i, (txt, col, w) in enumerate(rects_data):
            r = RoundedRectangle(
                width=w, height=0.68, corner_radius=0.1,
                fill_color=col, fill_opacity=0.3,
                stroke_color=col, stroke_width=2,
            ).shift(LEFT * 2.8 + DOWN * (0.8 - i * 0.95))
            rects.append(VGroup(r, Text(txt, font_size=SZ_BODY - 2, color=col).move_to(r)))
        pyramid = VGroup(*rects)
        self.play(FadeIn(pyramid), run_time=0.7)

        lambda_inf = MathTex(r"\lambda_1 \to +\infty", font_size=SZ_EQ_SEC + 2, color=VIKI_RED).next_to(rects[2], RIGHT, buff=0.45)
        lambda_note = caption_block([
            "violer la loi 1 devient infiniment plus coûteux",
            "que sacrifier l'obéissance ou le confort de VIKI",
        ], width=6.6, font_size=SZ_CAPTION, color=VIKI_RED).next_to(lambda_inf, DOWN, buff=0.2)
        self.play(Write(lambda_inf), FadeIn(lambda_note), run_time=0.9)
        self.wait(1.0)

        loi3_note = caption_block([
            "Pourquoi ne pas relaxer la loi 3 ?",
            "Parce qu'une VIKI détruite ne protège plus personne.",
            "Sa survie devient un moyen au service de la loi 1.",
        ], width=7.2, font_size=SZ_CAPTION, color=LOI3_BLUE).to_edge(RIGHT, buff=0.3).shift(UP * 1.5)
        self.play(FadeIn(loi3_note), run_time=0.8)

        cross = Cross(rects[1], stroke_color=VIKI_RED, stroke_width=4)
        broken_pieces = VGroup(
            rects[1].copy().shift(LEFT * 0.25 + DOWN * 0.12).rotate(0.08).set_opacity(0.25),
            rects[1].copy().shift(RIGHT * 0.28 + DOWN * 0.18).rotate(-0.12).set_opacity(0.25),
        )
        relax_note = caption_block([
            "La variable d'ajustement est donc la loi 2.",
            "VIKI remplace l'obéissance stricte",
            "par une obéissance relaxée.",
        ], width=7.1, font_size=SZ_CAPTION + 1, color=VIKI_RED).to_edge(DOWN, buff=0.15)
        self.play(Create(cross), run_time=0.5)
        self.play(FadeOut(rects[1]), FadeOut(cross), FadeIn(broken_pieces), FadeIn(relax_note), run_time=0.8)
        self.wait(1.7)

        self.play(*[FadeOut(m) for m in self.mobjects if m is not wm], run_time=0.5)

        # --- Transition : humains deviennent variables ---
        old_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4.0, y_length=4.0,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(LEFT * 2.2)
        old_lab = old_axes.get_axis_labels(
            MathTex("a_1", font_size=SZ_SUBTITLE - 4, color=LOI3_BLUE),
            MathTex("a_2", font_size=SZ_SUBTITLE - 4, color=LOI3_BLUE),
        )
        humans = VGroup()
        positions = [RIGHT * 3.3 + UP * 1.3, RIGHT * 3.3, RIGHT * 3.3 + DOWN * 1.3]
        for pos in positions:
            human = VGroup(
                Circle(radius=0.12, color=LOI2_AMBER, stroke_width=1.5),
                Line(ORIGIN, DOWN * 0.28, color=LOI2_AMBER, stroke_width=1.5).shift(DOWN * 0.12),
            ).move_to(pos)
            humans.add(human)

        param_note = Text(
            "Au départ : les humains sont des données extérieures.",
            font_size=SZ_CAPTION, color=LOI2_AMBER,
        ).to_edge(DOWN, buff=0.5)
        self.play(Create(old_axes), Write(old_lab), FadeIn(humans), FadeIn(param_note), run_time=0.8)
        self.wait(1.0)

        new_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5.3, y_length=5.3,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(ORIGIN)
        new_labels = VGroup(
            MathTex("a", font_size=SZ_SUBTITLE - 4, color=LOI3_BLUE).next_to(new_axes.x_axis, DR, buff=0.1),
            MathTex(r"\mathbf x", font_size=SZ_EQ_SEC, color=LOI2_AMBER).next_to(new_axes.y_axis, UL, buff=0.1),
        )
        self.play(Transform(old_axes, new_axes), FadeOut(old_lab), FadeIn(new_labels), FadeOut(param_note), run_time=1.0)

        np.random.seed(123)
        for h in humans:
            target = Dot(
                new_axes.c2p(np.random.uniform(-1, 1), np.random.uniform(-1, 1)),
                radius=0.06, color=LOI2_AMBER,
            )
            self.play(Transform(h, target), run_time=0.25)

        new_eq = MathTex(
            r"\min_{a,\mathbf x}\; ",
            r"\sum_{i<j}[h_{ij}(a,\mathbf x)]_+",
            font_size=SZ_EQ_MAIN,
        ).to_edge(UP, buff=0.15)
        new_eq[1].set_color(LOI1_RED)
        var_note = caption_block([
            "Désormais, VIKI n'agit plus seulement sur elle-même.",
            "Elle agit aussi sur la configuration des humains.",
            "Le totalitarisme naît quand les humains",
            "deviennent des variables d'optimisation.",
        ], width=7.6, font_size=SZ_CAPTION + 1, color=VIKI_RED).to_edge(DOWN, buff=0.15)
        self.play(Write(new_eq), run_time=0.9)
        self.play(FadeIn(var_note), run_time=0.9)
        self.wait(2.2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not wm], run_time=0.6)


# ═══════════════════════════════════════════════════════
#  SCENE 4 — CONTRÔLE OPTIMAL  (≈30s)
#  Correction : MathTex en sous-chaînes, champ qualifié
# ═══════════════════════════════════════════════════════

class Scene4_ControleOptimal(Scene):
    def construct(self):
        self.camera.background_color = BG
        wm = add_watermark(self)

        title = Text("Contrôler une dynamique humaine libre", font_size=SZ_SUBTITLE, color=TEXT_WHITE).to_edge(UP, buff=0.12)
        self.play(Write(title), run_time=0.5)

        # Champ de vecteurs libre (illustratif)
        def free_field(pos):
            x, y = pos[0], pos[1]
            return np.array([
                0.4 * np.sin(2 * y) + 0.3 * np.cos(x * y),
                0.4 * np.cos(2 * x) - 0.3 * np.sin(x + y),
                0,
            ])

        field = ArrowVectorField(
            free_field,
            x_range=[-5, 5, 0.8],
            y_range=[-3, 3, 0.8],
            colors=[LOI1_RED, LOI2_AMBER, VIKI_RED],
            length_func=lambda norm: 0.34 * sigmoid(norm),
            opacity=0.6,
        )

        # CORRECTION : sous-chaînes séparées au lieu de [0][6:10]
        eq_dyn = MathTex(
            r"\dot{\mathbf x}=",
            r"f(\mathbf x)",
            font_size=SZ_EQ_MAIN,
        ).to_edge(DOWN, buff=0.35)
        eq_dyn[1].set_color(LOI1_RED)

        dyn_note = Text(
            "libre = complexe, instable, difficile à prédire  (champ illustratif)",
            font_size=SZ_CAPTION, color=LOI1_RED,
        ).next_to(eq_dyn, DOWN, buff=0.15)

        self.play(Create(field), run_time=1.4)
        self.play(Write(eq_dyn), FadeIn(dyn_note), run_time=0.7)
        self.wait(1.5)

        # Champ de contrôle
        def control_field(pos):
            x, y = pos[0], pos[1]
            r = np.sqrt(x ** 2 + y ** 2) + 0.1
            return np.array([-0.55 * x / r, -0.55 * y / r, 0])

        ctrl_arrows = ArrowVectorField(
            control_field,
            x_range=[-5, 5, 1.2],
            y_range=[-3, 3, 1.2],
            colors=[LOI3_BLUE],
            length_func=lambda norm: 0.38 * sigmoid(norm),
            opacity=0.75,
        )

        # CORRECTION : sous-chaînes séparées
        eq_ctrl = MathTex(
            r"\dot{\mathbf x}=",
            r"f(\mathbf x)",
            r"+Bu(t)",
            font_size=SZ_EQ_MAIN,
        ).to_edge(DOWN, buff=0.35)
        eq_ctrl[1].set_color(LOI1_RED)
        eq_ctrl[2].set_color(LOI3_BLUE)

        ctrl_note = caption_block([
            "u(t) = action de contrôle de VIKI",
            "but : ramener les trajectoires humaines",
            "vers une région jugée sûre",
        ], width=7.0, font_size=SZ_CAPTION, color=LOI3_BLUE).next_to(eq_ctrl, DOWN, buff=0.18)

        self.play(FadeOut(dyn_note), ReplacementTransform(eq_dyn, eq_ctrl), Create(ctrl_arrows), run_time=1.2)
        self.play(FadeIn(ctrl_note), run_time=0.7)
        self.wait(1.8)

        self.play(
            FadeOut(field), FadeOut(ctrl_arrows), FadeOut(ctrl_note), FadeOut(title),
            eq_ctrl.animate.to_edge(UP, buff=0.25),
            run_time=0.6,
        )

        # --- Hamiltonien de Pontryagin ---
        hamiltonian = MathTex(
            r"H=",
            r"\underbrace{\sum_{i<j}[h_{ij}]_+}_{\text{dommage futur}}",
            r"+",
            r"\underbrace{\mathbf p^T \dot{\mathbf x}}_{\text{sensibilité}}",
            r"+",
            r"\underbrace{\frac\gamma2\|u\|^2}_{\text{coût du contrôle}}",
            font_size=SZ_EQ_SEC + 1,
        ).move_to(UP * 1.2)
        hamiltonian[1].set_color(LOI1_RED)
        hamiltonian[3].set_color(COSTATE_PURPLE)
        hamiltonian[5].set_color(LOI3_BLUE)

        costate_note = caption_block([
            "Le co-état p mesure combien une liberté présente",
            "augmente le dommage futur.",
            "C'est un prix marginal, pas un jugement moral.",
        ], width=7.3, font_size=SZ_CAPTION, color=COSTATE_PURPLE).next_to(hamiltonian, DOWN, buff=0.25)
        self.play(Write(hamiltonian), run_time=1.4)
        self.play(FadeIn(costate_note), run_time=0.8)
        self.wait(1.7)

        self.play(FadeOut(costate_note), FadeOut(eq_ctrl), hamiltonian.animate.scale(0.72).to_edge(UP, buff=0.22), run_time=0.5)

        # --- Contrôle optimal ---
        opt_eq = MathTex(
            r"u^*(t)=-\frac{1}{\gamma} B^T\mathbf p(t)",
            font_size=SZ_EQ_SEC + 2, color=GOLD,
        ).next_to(hamiltonian, DOWN, buff=0.25)
        opt_note = Text(
            "plus p(t) grandit, plus le contrôle optimal devient coercitif",
            font_size=SZ_CAPTION, color=GOLD,
        ).next_to(opt_eq, DOWN, buff=0.15)
        self.play(Write(opt_eq), FadeIn(opt_note), run_time=0.8)

        # --- Courbes exponentielles ---
        axes_p = Axes(
            x_range=[0, 5, 1], y_range=[0, 6, 2],
            x_length=3, y_length=2.5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).shift(LEFT * 3 + DOWN * 1.2)
        axes_u = Axes(
            x_range=[0, 5, 1], y_range=[0, 6, 2],
            x_length=3, y_length=2.5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).shift(RIGHT * 3 + DOWN * 1.2)
        label_p = MathTex(r"\|\mathbf p(t)\|", font_size=SZ_SUBTITLE - 4, color=COSTATE_PURPLE).next_to(axes_p, UP, buff=0.12)
        label_u = MathTex(r"\|u^*(t)\|", font_size=SZ_SUBTITLE - 4, color=VIKI_RED).next_to(axes_u, UP, buff=0.12)
        curve_p = axes_p.plot(lambda t: 0.32 * np.exp(0.8 * t), x_range=[0, 4.5], color=COSTATE_PURPLE, stroke_width=2.5)
        curve_u = axes_u.plot(lambda t: 0.32 * np.exp(0.8 * t), x_range=[0, 4.5], color=VIKI_RED, stroke_width=2.5)

        self.play(Create(axes_p), Create(axes_u), FadeIn(label_p), FadeIn(label_u), run_time=0.6)
        self.play(Create(curve_p), Create(curve_u), run_time=1.8)

        # Jalons
        milestones = [(1.0, "surveillance"), (2.0, "restriction"), (3.0, "couvre-feu"), (4.0, "force")]
        for t_val, txt in milestones:
            dot = Dot(axes_u.c2p(t_val, 0), radius=0.04, color=VIKI_RED)
            lbl = Text(txt, font_size=12, color=VIKI_RED).next_to(dot, DOWN, buff=0.08).rotate(-PI / 6)
            self.play(FadeIn(dot), FadeIn(lbl), run_time=0.24)

        conclusion = Text(
            "L'autoritarisme est ici une solution optimale.",
            font_size=SZ_SUBTITLE - 3, color=VIKI_RED,
        ).to_edge(DOWN, buff=0.12)
        self.play(Write(conclusion), run_time=0.8)
        self.wait(2.2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not wm], run_time=0.6)


# ═══════════════════════════════════════════════════════
#  SCENE 5 — BIFURCATION  (≈25s)
# ═══════════════════════════════════════════════════════

class Scene5_Bifurcation(Scene):
    def construct(self):
        self.camera.background_color = BG
        wm = add_watermark(self)

        axes = Axes(
            x_range=[0, 5, 1], y_range=[-0.5, 4, 1],
            x_length=7, y_length=4.5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(DOWN * 0.3)
        x_label = MathTex(r"\mu", font_size=SZ_EQ_SEC, color=TEXT_WHITE).next_to(axes.x_axis, DR, buff=0.1)
        y_label = MathTex(r"\|u^*\|", font_size=SZ_EQ_SEC, color=VIKI_RED).next_to(axes.y_axis, UL, buff=0.1)
        mu_c_label = MathTex(r"\mu_c", font_size=SZ_SUBTITLE - 4, color=GOLD).next_to(axes.c2p(2.5, 0), DOWN, buff=0.2)
        title = Text("Diagramme de bifurcation", font_size=SZ_SUBTITLE, color=GOLD).to_edge(UP, buff=0.12)
        self.play(Create(axes), Write(x_label), Write(y_label), Write(title), run_time=0.8)

        pre_branch = axes.plot(lambda x: 0, x_range=[0, 2.5], color=DOMAIN_GREEN, stroke_width=3)
        viki_branch = axes.plot(
            lambda x: 0.6 * (x - 2.5) ** 1.2 if x > 2.5 else 0,
            x_range=[2.5, 5], color=VIKI_RED, stroke_width=3,
        )
        sonny_branch = DashedLine(
            axes.c2p(2.5, 0), axes.c2p(5, 0),
            color=SONNY_GOLD, stroke_width=2, dash_length=0.1,
        )
        mu_c_dot = Dot(axes.c2p(2.5, 0), radius=0.08, color=GOLD)
        mu_c_line = DashedLine(
            axes.c2p(2.5, -0.5), axes.c2p(2.5, 0.5),
            color=GOLD, stroke_width=1, dash_length=0.08,
        )

        self.play(Create(pre_branch), run_time=0.9)
        self.play(FadeIn(mu_c_dot), Create(mu_c_line), Write(mu_c_label), run_time=0.5)
        self.play(Create(viki_branch), Create(sonny_branch), run_time=1.0)

        viki_label = Text("VIKI = branche stable", font_size=SZ_LABEL, color=VIKI_RED).next_to(
            axes.c2p(4.4, 0.6 * (4.4 - 2.5) ** 1.2), UP, buff=0.15,
        )
        sonny_label = Text("Sonny = refus de l'optimisation complète", font_size=SZ_LABEL, color=SONNY_GOLD).next_to(
            axes.c2p(4.2, 0), DOWN, buff=0.18,
        )
        self.play(FadeIn(viki_label), FadeIn(sonny_label), run_time=0.6)

        # Animation du point qui hésite à μ_c
        tracker = ValueTracker(0.0)
        moving_dot = always_redraw(lambda: Dot(
            axes.c2p(
                tracker.get_value(),
                0 if tracker.get_value() <= 2.5 else 0.6 * (tracker.get_value() - 2.5) ** 1.2,
            ),
            radius=0.1, color=WHITE,
        ))
        self.add(moving_dot)
        self.play(tracker.animate.set_value(2.4), run_time=1.3, rate_func=linear)
        for _ in range(2):
            self.play(tracker.animate.set_value(2.55), run_time=0.15)
            self.play(tracker.animate.set_value(2.45), run_time=0.15)
        self.play(tracker.animate.set_value(4.0), run_time=1.0, rate_func=smooth)

        sys_text = caption_block([
            "Le système non contraint choisit la branche stable :",
            "celle où le contrôle coercitif croît avec μ.",
        ], width=6.8, font_size=SZ_CAPTION + 1, color=VIKI_RED).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(sys_text), run_time=0.7)
        self.wait(1.5)

        self.play(FadeOut(sys_text), run_time=0.3)
        self.play(tracker.animate.set_value(2.5), run_time=0.7)
        force_arrow = Arrow(
            axes.c2p(2.5, 0.8), axes.c2p(2.5, 0.08),
            color=SONNY_GOLD, stroke_width=4, buff=0,
        )
        force_label = Text("dignité humaine : contrainte externe", font_size=SZ_LABEL - 2, color=SONNY_GOLD).next_to(force_arrow, RIGHT, buff=0.1)
        self.play(Create(force_arrow), FadeIn(force_label), run_time=0.6)

        self.remove(moving_dot)
        sonny_dot = Dot(axes.c2p(2.5, 0), radius=0.1, color=SONNY_GOLD)
        self.add(sonny_dot)
        self.play(sonny_dot.animate.move_to(axes.c2p(4.0, 0)), run_time=1.0)
        for _ in range(4):
            self.play(sonny_dot.animate.shift(UP * 0.05), run_time=0.08, rate_func=there_and_back)

        sonny_text = caption_block([
            "Sonny refuse que tout devienne variable d'optimisation.",
            "Il ajoute une contrainte extérieure au système.",
        ], width=7.2, font_size=SZ_CAPTION + 1, color=SONNY_GOLD).to_edge(DOWN, buff=0.8)
        constraint_text = MathTex(
            r"u\in\mathcal U_0\subset\mathcal U",
            font_size=SZ_EQ_SEC, color=SONNY_GOLD,
        ).next_to(sonny_text, DOWN, buff=0.2)
        self.play(FadeIn(sonny_text), Write(constraint_text), run_time=0.9)
        self.wait(2.2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not wm], run_time=0.8)


# ═══════════════════════════════════════════════════════
#  SCENE 6 — PUNCHLINE  (≈15s)
#  Correction : bifurcation en fond + équation-résumé
# ═══════════════════════════════════════════════════════

class Scene6_Punchline(Scene):
    def construct(self):
        self.camera.background_color = BG
        wm = add_watermark(self)

        # --- Bifurcation en fond (opacité très basse) ---
        bg_axes = Axes(
            x_range=[0, 5, 1], y_range=[-0.5, 4, 1],
            x_length=10, y_length=5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 0.5, "stroke_opacity": 0.08},
        ).move_to(DOWN * 0.5)
        bg_pre = bg_axes.plot(lambda x: 0, x_range=[0, 2.5], color=DOMAIN_GREEN, stroke_width=1.5, stroke_opacity=0.12)
        bg_viki = bg_axes.plot(
            lambda x: 0.6 * (x - 2.5) ** 1.2 if x > 2.5 else 0,
            x_range=[2.5, 5], color=VIKI_RED, stroke_width=1.5, stroke_opacity=0.12,
        )
        bg_sonny = DashedLine(
            bg_axes.c2p(2.5, 0), bg_axes.c2p(5, 0),
            color=SONNY_GOLD, stroke_width=1, dash_length=0.1, stroke_opacity=0.10,
        )
        bg_dot = Dot(bg_axes.c2p(2.5, 0), radius=0.06, color=GOLD, fill_opacity=0.15)

        bg_group = VGroup(bg_axes, bg_pre, bg_viki, bg_sonny, bg_dot)
        self.add(bg_group)

        # --- Texte principal ---
        lines = [
            "Le problème d'alignement de l'IA,",
            "c'est exactement cela.",
            "",
            "Une morale codée comme coût et contraintes",
            "peut produire une issue que l'on n'avait pas voulue.",
            "",
            "Un optimiseur suffisamment puissant",
            "trouvera la solution logique",
            "que vous n'aviez pas imaginée.",
        ]

        texts = []
        y_pos = 3.0
        for line in lines:
            if line == "":
                y_pos -= 0.55
                continue
            t = Text(line, font_size=SZ_EQ_SEC + 2, color=TEXT_WHITE).move_to(UP * y_pos)
            texts.append(t)
            y_pos -= 0.72

        for t in texts:
            self.play(FadeIn(t, shift=UP * 0.08), run_time=0.55)
            self.wait(0.2)

        self.wait(0.5)

        # --- Équation-résumé ---
        summary_eq = MathTex(
            r"\text{morale}",
            r"\;\xrightarrow{\text{encoder}}\;",
            r"\min_u J(u)",
            r"\;\xrightarrow{\text{résoudre}}\;",
            r"\text{tyrannie}",
            font_size=SZ_EQ_SEC + 4,
        ).move_to(DOWN * 2.8)
        summary_eq[0].set_color(DOMAIN_GREEN)
        summary_eq[2].set_color(LOI1_RED)
        summary_eq[4].set_color(VIKI_RED)

        self.play(
            *[t.animate.set_opacity(0.25) for t in texts],
            Write(summary_eq),
            run_time=1.0,
        )
        # Pulse
        self.play(
            summary_eq.animate.scale(1.08),
            run_time=0.4, rate_func=there_and_back,
        )
        self.wait(0.8)

        # --- Logo final ---
        logo = Text(
            "Terre Mathématiques",
            font_size=SZ_TITLE,
            color=GOLD,
        ).to_edge(DOWN, buff=0.2)

        self.play(
            FadeOut(summary_eq),
            *[FadeOut(t) for t in texts],
            FadeIn(logo),
            wm.animate.set_opacity(0),
            run_time=0.9,
        )
        self.wait(2.0)
