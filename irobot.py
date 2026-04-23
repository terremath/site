from manim import *
import numpy as np

# ═══════════════════════════════════════════════════════
# Format portrait 9:16
# ═══════════════════════════════════════════════════════
config.frame_width   = 14.222
config.frame_height  = 25.28
config.pixel_width   = 1080
config.pixel_height  = 1920

# ─── Métadonnées pour render_all.bat ─────────────────────────────────────────
SCENES = [
    "Scene0_Hook",
    "Scene1_RobotHonnete",
    "Scene2_Incompatibilite",
    "Scene3_Relaxation",
    "Scene4_ControleOptimal",
    "Scene5_Bifurcation",
    "Scene6_Punchline",
    "Scene7_Ouverture",
    "Scene8_CTA",
]
OUTPUT_NAME = "irobot_FINAL.mp4"
OUTPUT_DIR  = r"media\videos\irobot\1920p30"
# ─────────────────────────────────────────────────────────────────────────────

# ═══════════════════════════════════════════════════════
#  PALETTE
# ═══════════════════════════════════════════════════════
BG             = "#F5EAD6"
LOI1_RED       = "#e63946"
LOI2_AMBER     = "#f4a261"
LOI3_BLUE      = "#457b9d"
GOLD           = "#8B6914"
VIKI_RED       = "#ff1744"
SONNY_GOLD     = "#A07820"
TEXT_WHITE     = "#2A0A2E"
DOMAIN_GREEN   = "#1a7a6e"
COSTATE_PURPLE = "#7a3d99"
SOFT_GREY      = "#5A2A50"

# ═══════════════════════════════════════════════════════
#  TAILLES HARMONISÉES  (+15 % par rapport à la version précédente)
# ═══════════════════════════════════════════════════════
SZ_TITLE    = 76
SZ_SUBTITLE = 52
SZ_BODY     = 42
SZ_CAPTION  = 36
SZ_EQ_MAIN  = 62
SZ_EQ_SEC   = 50
SZ_LABEL    = 34

# ═══════════════════════════════════════════════════════
#  UTILITAIRES
# ═══════════════════════════════════════════════════════

def fit_w(mob, frac=0.82):
    max_w = config.frame_width * frac
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob


def make_header(text, color=TEXT_WHITE):
    """Retourne un VGroup (titre + filet doré) sans positionnement."""
    h = Tex(r"\textbf{" + text + r"}", font_size=SZ_SUBTITLE, color=color)
    fit_w(h, 0.84)
    span = min(config.frame_width * 0.84, h.width + 1.5)
    line = Line(LEFT * span / 2, RIGHT * span / 2, color=GOLD, stroke_width=3)
    line.next_to(h, DOWN, buff=0.25)
    return VGroup(h, line)


def TLines(*lines, font_size=SZ_BODY, color=TEXT_WHITE, buff=0.20, **kwargs):
    """Texte multi-lignes rendu en LaTeX -- centre, fit_w automatique."""
    group = VGroup(*[Tex(ln, font_size=font_size, color=color, **kwargs) for ln in lines])
    group.arrange(DOWN, buff=buff, aligned_edge=ORIGIN)
    for mob in group:
        fit_w(mob, 0.84)
    return group


def make_bg(scene):
    scene.camera.background_color = BG


def caption_block(lines, width=11.5, font_size=SZ_CAPTION, color=TEXT_WHITE, line_buff=0.22):
    """Bloc encadré — fond transparent, largeur s'adapte au texte si nécessaire."""
    texts = VGroup(*[
        Tex(ln, font_size=font_size, color=color) for ln in lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=line_buff)
    for t in texts:
        fit_w(t, 0.84)
    actual_width = max(width, texts.width + 1.0)
    box = RoundedRectangle(
        corner_radius=0.15, width=actual_width,
        height=texts.height + 0.7,
        stroke_color=color, stroke_width=1.5,
        fill_color=BG, fill_opacity=0,
    )
    texts.move_to(box)
    return VGroup(box, texts)


def circular_crop_image(image: ImageMobject, margin: int = 2) -> ImageMobject:
    arr = image.pixel_array
    h, w = arr.shape[:2]
    cy, cx = h / 2, w / 2
    radius = min(cx, cy) - margin
    yy, xx = np.ogrid[:h, :w]
    mask = (xx - cx) ** 2 + (yy - cy) ** 2 >= radius ** 2
    arr[mask, 3] = 0
    image.pixel_array = arr
    image.orig_alpha_pixel_array = arr[:, :, 3].copy()
    return image


def add_watermark(_scene):
    return None


def fade_all_except(scene, keep):
    return [FadeOut(m) for m in scene.mobjects if m not in keep]


def clip_polygon_by_halfplane(vertices, normal, offset):
    output = list(vertices)
    if not output:
        return output
    def inside(p):
        return np.dot(normal, p) <= offset + 1e-12
    def intersect(p1, p2):
        d1, d2 = np.dot(normal, p1) - offset, np.dot(normal, p2) - offset
        t = d1 / (d1 - d2)
        return p1 + t * (p2 - p1)
    clipped = []
    for i in range(len(output)):
        curr, nxt = output[i], output[(i + 1) % len(output)]
        if inside(curr):
            clipped.append(nxt) if inside(nxt) else clipped.append(intersect(curr, nxt))
        elif inside(nxt):
            clipped.append(intersect(curr, nxt))
            clipped.append(nxt)
    return clipped


# ═══════════════════════════════════════════════════════
#  SCENE 0 — HOOK
# ═══════════════════════════════════════════════════════

class Scene0_Hook(Scene):
    def construct(self):
        make_bg(self)

        # ─── Phrase d'accroche ───
        t1 = Tex(r"\textbf{VIKI n'a pas bugu\'e.}", font_size=SZ_TITLE + 14, color=TEXT_WHITE)
        fit_w(t1, 0.84)
        t1.move_to(UP * 3.5)

        t2 = TLines(
            r"Elle a \'et\'e logiquement contrainte",
            r"de r\'esoudre un nouveau syst\`eme.",
            font_size=SZ_SUBTITLE + 10, color=VIKI_RED,
        )
        t2.move_to(UP * 3.0)

        self.play(Write(t1), run_time=1.4)
        self.wait(1.2)
        self.play(FadeOut(t1), run_time=0.6)
        self.play(FadeIn(t2, shift=UP * 0.15), run_time=1.0)
        self.wait(1.8)
        self.play(FadeOut(t2))

        # ─── Titre principal ───
        title = TLines(
            r"\textbf{Comment les 3 Lois}",
            r"\textbf{produisent un tyran}",
            font_size=SZ_TITLE + 8, color=GOLD,
        )
        deco_line = Line(LEFT * 4.0, RIGHT * 4.0, color=GOLD, stroke_width=2.5)
        subtitle = TLines(
            r"quand la protection absolue devient",
            r"un probl\`eme d'optimisation",
            font_size=SZ_SUBTITLE + 4, color=SOFT_GREY,
        )
        VGroup(title, deco_line, subtitle).arrange(DOWN, buff=1.4).move_to(UP * 1.5)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=1.2)
        self.play(Create(deco_line), run_time=0.7)
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.9)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(deco_line), FadeOut(subtitle))


# ═══════════════════════════════════════════════════════
#  SCENE 1 — LE ROBOT HONNÊTE
# ═══════════════════════════════════════════════════════

class Scene1_RobotHonnete(Scene):
    def construct(self):
        make_bg(self)

        # ─── 1.1 Pyramide des Lois ───
        rects = []
        labels_text = [
            (r"LOI 3 --- Se Pr\'eserver",   LOI3_BLUE,  9.5),
            (r"LOI 2 --- Ob\'eir",           LOI2_AMBER,  7.5),
            (r"LOI 1 --- Ne Pas Blesser",    LOI1_RED,    5.5),
        ]
        for i, (txt, col, w) in enumerate(labels_text):
            r = RoundedRectangle(
                width=w, height=2.2, corner_radius=0.12,
                fill_color=col, fill_opacity=0.3,
                stroke_color=col, stroke_width=2,
            ).shift(DOWN * (2.5 - i * 3.0))
            label = Tex(txt, font_size=SZ_BODY, color=col)
            fit_w(label, 0.60)
            label.move_to(r)
            rects.append(VGroup(r, label))

        pyramid = VGroup(*rects).move_to(ORIGIN)
        for r in rects:
            self.play(FadeIn(r, shift=UP * 0.15), run_time=1.2)

        arrow = Arrow(
            start=pyramid.get_bottom() + RIGHT * 5.2,
            end=pyramid.get_top() + RIGHT * 5.2,
            color=TEXT_WHITE, stroke_width=2,
        )
        arrow_label = Tex(r"priorit\'e", font_size=SZ_LABEL + 4, color=TEXT_WHITE)
        fit_w(arrow_label, 0.22)
        arrow_label.next_to(arrow, RIGHT, buff=0.15)
        self.play(Create(arrow), FadeIn(arrow_label), run_time=0.8)
        self.wait(1.0)

        # ─── 1.2 Programme d'optimisation encadré ───
        self.play(FadeOut(VGroup(pyramid, arrow, arrow_label)), run_time=0.7)

        program_title = make_header(r"Les 3 Lois comme programme d'optimisation")

        EQ_F = SZ_EQ_SEC + 8
        TAG_F = SZ_LABEL + 10

        eq_obj = MathTex(r"\min_{a}\;", r"C(a)", font_size=EQ_F)
        eq_obj[0].set_color(LOI3_BLUE)
        eq_obj[1].set_color(LOI3_BLUE)
        tag_obj = Tex(r"$\leftarrow$ LOI 3", font_size=TAG_F, color=LOI3_BLUE)
        row_obj = VGroup(eq_obj, tag_obj).arrange(RIGHT, buff=0.8)

        eq_c1 = MathTex(
            r"\text{s.c.}\;", r"h_{ij}(a) \le 0\;", r"\forall\, i<j",
            font_size=EQ_F,
        )
        eq_c1[0].set_color(LOI1_RED)
        eq_c1[1].set_color(LOI1_RED)
        eq_c1[2].set_color(LOI1_RED)
        tag_c1 = Tex(r"$\leftarrow$ LOI 1", font_size=TAG_F, color=LOI1_RED)
        row_c1 = VGroup(eq_c1, tag_c1).arrange(RIGHT, buff=0.8)

        eq_c2 = MathTex(
            r"\|a - a^{\mathrm{ordre}}\|^2 \le \varepsilon",
            font_size=EQ_F, color=LOI2_AMBER,
        )
        tag_c2 = Tex(r"$\leftarrow$ LOI 2", font_size=TAG_F, color=LOI2_AMBER)
        row_c2 = VGroup(eq_c2, tag_c2).arrange(RIGHT, buff=0.8)

        eqs_block = VGroup(row_obj, row_c1, row_c2).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        frame_box = SurroundingRectangle(
            eqs_block, color=GOLD, buff=0.8,
            corner_radius=0.12, stroke_width=2,
        )

        defs_lines = VGroup(
            MathTex(r"a \;=\; \text{action choisie par le robot}", font_size=SZ_BODY, color=TEXT_WHITE),
            MathTex(r"C(a) \;=\; \text{co\^ut de survie pour le robot}", font_size=SZ_BODY, color=TEXT_WHITE),
            MathTex(r"h_{ij}(a) \;=\; \text{dommage inflig\'e au couple } (i,j)", font_size=SZ_BODY, color=TEXT_WHITE),
            MathTex(r"a^{\text{ordre}} \;=\; \text{action demand\'ee par un humain}", font_size=SZ_BODY, color=TEXT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        for d in defs_lines:
            fit_w(d, 0.84)
        defs_box = RoundedRectangle(
            corner_radius=0.15, width=max(11.5, defs_lines.width + 0.8),
            height=defs_lines.height + 0.7,
            stroke_color=TEXT_WHITE, stroke_width=1.5,
            fill_color=BG, fill_opacity=0,
        )
        defs_lines.move_to(defs_box)
        defs = VGroup(defs_box, defs_lines)

        framed = VGroup(frame_box, eqs_block)
        layout = VGroup(program_title, framed, defs).arrange(DOWN, buff=0.8)
        layout.move_to(UP * 1.5)

        self.play(Write(program_title), run_time=0.9)
        self.play(Write(eq_obj), FadeIn(tag_obj), run_time=1.5)
        self.play(Write(eq_c1), FadeIn(tag_c1), run_time=1.5)
        self.play(Write(eq_c2), FadeIn(tag_c2), run_time=1.5)
        self.play(Create(frame_box), run_time=0.7)
        self.play(FadeIn(defs, shift=UP * 0.1), run_time=1.2)
        self.wait(4.0)

        self.play(FadeOut(VGroup(program_title, row_obj, row_c1, row_c2, frame_box, defs)), run_time=0.6)

        # ─── 1.3 Domaine admissible A_N ───
        domain_title = make_header(r"Le domaine admissible", color=DOMAIN_GREEN)
        domain_title.to_edge(UP, buff=1.5)
        self.play(Write(domain_title), run_time=0.7)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=10.0, y_length=11.0,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(UP * 0.5)
        ax_labels = axes.get_axis_labels(
            MathTex("a_1", font_size=SZ_SUBTITLE - 4, color=TEXT_WHITE),
            MathTex("a_2", font_size=SZ_SUBTITLE - 4, color=TEXT_WHITE),
        )

        loi1_region = Polygon(
            axes.c2p(-3, -3), axes.c2p(3, -3), axes.c2p(3, 1.5), axes.c2p(-3, 1.5),
            fill_color=LOI1_RED, fill_opacity=0.14, stroke_width=0,
        )
        loi1_line = axes.plot(lambda x: 1.5, x_range=[-3, 3], color=LOI1_RED, stroke_width=2)
        loi1_label = Tex(r"zone de s\'ecurit\'e humaine", font_size=SZ_LABEL, color=LOI1_RED)
        fit_w(loi1_label, 0.60)
        loi1_label.next_to(axes.c2p(0, 1.5), UP, buff=0.12)

        disc = Circle(
            radius=axes.x_length / 6 * 1.75,
            fill_color=LOI2_AMBER, fill_opacity=0.14,
            stroke_color=LOI2_AMBER, stroke_width=2,
        ).move_to(axes.c2p(0.5, 0.5))
        loi2_label = Tex(r"zone d'ob\'eissance", font_size=SZ_LABEL, color=LOI2_AMBER)
        fit_w(loi2_label, 0.50)
        loi2_label.next_to(disc, DOWN, buff=0.15)

        opt_star = Star(n=5, outer_radius=0.15, inner_radius=0.06, color=GOLD, fill_opacity=1)
        opt_star.move_to(axes.c2p(0.5, 1.0))
        opt_label = MathTex("a^*", font_size=SZ_SUBTITLE, color=GOLD).next_to(opt_star, UR, buff=0.1)

        an_label = MathTex(
            r"\mathcal{A}_N", r"= \text{intersection}", font_size=SZ_EQ_SEC, color=DOMAIN_GREEN,
        )
        an_label[0].set_color(DOMAIN_GREEN)
        an_label.next_to(axes, DOWN, buff=0.5)

        note = caption_block([
            r"Tant qu'il existe $a^*$ dans le domaine admissible,",
            r"le robot peut se pr\'eserver, ob\'eir, et ne blesser personne.",
            r"Les trois Lois sont simultan\'ement satisfaites.",
        ], width=11.0, font_size=SZ_CAPTION + 1, color=DOMAIN_GREEN).to_edge(DOWN, buff=1.5)

        self.play(Create(axes), Write(ax_labels), run_time=0.7)
        self.play(FadeIn(loi1_region), Create(loi1_line), FadeIn(loi1_label), run_time=0.7)
        self.play(Create(disc), FadeIn(loi2_label), run_time=0.7)
        self.play(FadeIn(opt_star), FadeIn(opt_label), run_time=0.7)
        self.play(FadeIn(an_label), run_time=0.7)
        self.play(FadeIn(note), run_time=0.7)
        self.wait(3.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # ─── 1.4 Le Lagrangien ───
        lag_title = Tex(
            r"\textbf{Le Lagrangien traduit la hi\'erarchie}",
            font_size=SZ_SUBTITLE + 8, color=GOLD,
        )
        fit_w(lag_title, 0.84)

        lagrangian = MathTex(
            r"\mathcal{L}(a)=",
            r"C(a)",
            r"+\lambda\sum_{i<j} [h_{ij}(a)]_+",
            r"+\nu\big(\|a-a^{\mathrm{ordre}}\|^2-\varepsilon\big)",
            font_size=SZ_EQ_MAIN + 6,
        )
        fit_w(lagrangian, 0.90)
        lagrangian[0].set_color(TEXT_WHITE)
        lagrangian[1].set_color(LOI3_BLUE)
        lagrangian[2].set_color(LOI1_RED)
        lagrangian[3].set_color(LOI2_AMBER)

        brace_loi3 = Brace(lagrangian[1], DOWN, color=LOI3_BLUE, buff=0.12)
        brace_loi1 = Brace(lagrangian[2], DOWN, color=LOI1_RED, buff=0.12)
        brace_loi2 = Brace(lagrangian[3], DOWN, color=LOI2_AMBER, buff=0.12)
        bl3 = Tex(r"LOI 3", font_size=SZ_BODY - 4, color=LOI3_BLUE).next_to(brace_loi3, DOWN, buff=0.08)
        bl1 = Tex(r"LOI 1", font_size=SZ_BODY - 4, color=LOI1_RED).next_to(brace_loi1, DOWN, buff=0.08)
        bl2 = Tex(r"LOI 2", font_size=SZ_BODY - 4, color=LOI2_AMBER).next_to(brace_loi2, DOWN, buff=0.08)

        all_braces = VGroup(brace_loi3, brace_loi1, brace_loi2, bl3, bl1, bl2)
        lag_note = caption_block([
            r"Grand multiplicateur $=$ violation tr\`es co\^uteuse.",
            r"La hi\'erarchie des Lois devient",
            r"une hi\'erarchie de p\'enalit\'es.",
        ], width=10.5, font_size=SZ_CAPTION + 4, color=GOLD)

        lag_group = VGroup(lag_title, lagrangian, all_braces, lag_note)
        lag_group.arrange(DOWN, buff=0.7)
        lag_group.move_to(UP * 1.0)

        self.play(Write(lag_title), run_time=0.6)
        self.play(Write(lagrangian), run_time=1.4)
        self.play(
            FadeIn(brace_loi3), FadeIn(bl3),
            FadeIn(brace_loi1), FadeIn(bl1),
            FadeIn(brace_loi2), FadeIn(bl2),
            run_time=0.8,
        )
        self.play(FadeIn(lag_note), run_time=0.7)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════════════════
#  SCENE 2 — INFAISABILITÉ
# ═══════════════════════════════════════════════════════

class Scene2_Incompatibilite(Scene):
    def construct(self):
        make_bg(self)

        title = make_header(r"Pourquoi le probl\`eme devient infaisable")
        title.to_edge(UP, buff=1.5)
        self.play(Write(title), run_time=0.7)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=9.0, y_length=9.0,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(DOWN * 0.5)
        self.play(Create(axes), run_time=0.6)

        counter = Integer(1, font_size=SZ_EQ_MAIN + 4, color=TEXT_WHITE)
        n_label = MathTex("N =", font_size=SZ_EQ_MAIN + 4, color=TEXT_WHITE)
        nc_group = VGroup(n_label, counter).arrange(RIGHT, buff=0.15)
        nc_group.next_to(title, DOWN, buff=0.6)
        pair_formula = MathTex(
            r"\#\text{contraintes} \sim \binom{N}{2}",
            font_size=SZ_EQ_SEC + 4, color=LOI1_RED,
        ).next_to(nc_group, DOWN, buff=0.3)
        self.play(FadeIn(n_label), FadeIn(counter), Write(pair_formula), run_time=0.7)

        explanation = caption_block([
            r"Chaque humain libre g\'en\`ere des interactions \`a s\'ecuriser.",
            r"La Loi 1 ajoute de plus en plus de contraintes.",
        ], width=11.0, font_size=SZ_CAPTION + 2, color=TEXT_WHITE).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(explanation), run_time=0.6)

        init_verts_2d = [
            np.array([-2.5, -2.5]), np.array([2.5, -2.5]),
            np.array([2.5, 2.5]),   np.array([-2.5, 2.5]),
        ]
        current_verts = list(init_verts_2d)
        domain_polygon = Polygon(
            *[axes.c2p(v[0], v[1]) for v in current_verts],
            fill_color=DOMAIN_GREEN, fill_opacity=0.3,
            stroke_color=DOMAIN_GREEN, stroke_width=1.5,
        )
        self.play(FadeIn(domain_polygon), run_time=0.5)

        np.random.seed(42)
        n_values = [2, 3, 5, 8, 12, 20, 35, 50]

        for step, n_val in enumerate(n_values):
            n_new = min(3, max(1, n_val // 4))
            new_lines = []
            for _ in range(n_new):
                angle = np.random.uniform(0, 2 * np.pi)
                normal = np.array([np.cos(angle), np.sin(angle)])
                offset = np.random.uniform(0.3, 2.0) * max(0.1, 1 - step / len(n_values) * 0.9)
                perp = np.array([-normal[1], normal[0]])
                center = normal * offset
                p1_2d, p2_2d = center + 5 * perp, center - 5 * perp
                vis_line = Line(
                    axes.c2p(p1_2d[0], p1_2d[1]),
                    axes.c2p(p2_2d[0], p2_2d[1]),
                    color=LOI1_RED, stroke_width=1, stroke_opacity=0.55,
                )
                new_lines.append(vis_line)
                current_verts = clip_polygon_by_halfplane(current_verts, normal, offset)

            if len(current_verts) >= 3:
                new_domain = Polygon(
                    *[axes.c2p(v[0], v[1]) for v in current_verts],
                    fill_color=DOMAIN_GREEN, fill_opacity=0.3,
                    stroke_color=DOMAIN_GREEN, stroke_width=1.5,
                )
            else:
                new_domain = Dot(axes.c2p(0, 0), radius=0.01, fill_opacity=0)

            self.play(
                *[Create(line) for line in new_lines],
                counter.animate.set_value(n_val),
                Transform(domain_polygon, new_domain),
                run_time=max(0.25, 0.55 - step * 0.05),
            )
            if len(current_verts) < 3:
                break

        self.play(FadeOut(explanation), run_time=0.4)

        empty_set = MathTex(r"\emptyset", font_size=160, color=VIKI_RED).move_to(axes.get_center())
        self.play(counter.animate.set_color(VIKI_RED), run_time=0.4)
        self.play(
            domain_polygon.animate.scale(0).set_opacity(0),
            Flash(axes.get_center(), color=VIKI_RED, num_lines=12, line_length=0.4),
            run_time=0.7,
        )
        self.play(FadeIn(empty_set, scale=1.8), run_time=0.7)

        consequence = caption_block([
            r"CONS\'EQUENCE FONDAMENTALE",
            r"",
            r"Il n'existe plus aucune action $a$ qui satisfasse",
            r"toutes les contraintes \`a la fois.",
            r"Le programme d'optimisation est infaisable.",
        ], width=11.5, font_size=SZ_BODY + 2, color=VIKI_RED, line_buff=0.42).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(consequence), run_time=0.8)
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ═══════════════════════════════════════════════════════
#  SCENE 3 — RELAXATION
# ═══════════════════════════════════════════════════════

class Scene3_Relaxation(Scene):
    def construct(self):
        make_bg(self)

        # ─── 3.1 Constat d'infaisabilité ───
        title_31 = caption_block([
            r"Le probl\`eme est infaisable.",
            r"VIKI doit modifier le probl\`eme lui-m\^eme.",
        ], width=10.0, font_size=SZ_BODY + 4, color=TEXT_WHITE).move_to(UP * 4.5)
        eq_fail = MathTex(
            r"\nexists\, a \in \mathcal{A}_N",
            font_size=SZ_EQ_MAIN + 8, color=VIKI_RED,
        ).move_to(UP * 1.0)
        self.play(FadeIn(title_31), Write(eq_fail), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(title_31), FadeOut(eq_fail), run_time=0.6)

        # ─── 3.2 Quelle contrainte relaxer ? ───
        question = make_header(r"Quelle contrainte relaxer ?", color=GOLD)
        question.to_edge(UP, buff=1.5)
        self.play(Write(question), run_time=0.6)

        OPT_W = 11.0

        def make_opt_box(label, col, body_lines):
            ttl = Tex(r"\textbf{" + label + r"}", font_size=SZ_BODY, color=col)
            fit_w(ttl, 0.80)
            bdy_grp = VGroup(*[Tex(ln, font_size=SZ_CAPTION, color=TEXT_WHITE) for ln in body_lines])
            bdy_grp.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            for t in bdy_grp:
                fit_w(t, 0.80)
            content = VGroup(ttl, bdy_grp).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            box = RoundedRectangle(
                width=max(OPT_W, content.width + 0.8),
                height=content.height + 0.6,
                corner_radius=0.15, stroke_color=col, stroke_width=2,
                fill_color=BG, fill_opacity=0.6,
            )
            content.move_to(box)
            return box, ttl, bdy_grp, content

        box_a, title_a, body_a, content_a = make_opt_box(
            r"Relaxer LOI 1 ?", LOI1_RED,
            [r"Tol\'erer de blesser des humains",
             r"$\to$ Viole la priorit\'e absolue de la Loi 1"],
        )
        cross_a = Cross(box_a, stroke_color=VIKI_RED, stroke_width=6)
        verdict_a = Tex(r"IMPOSSIBLE", font_size=SZ_BODY - 4, color=VIKI_RED)

        box_b, title_b, body_b, content_b = make_opt_box(
            r"Relaxer LOI 3 ?", LOI3_BLUE,
            [r"Sacrifier la survie de VIKI",
             r"$\to$ VIKI d\'etruite ne prot\`ege plus personne"],
        )
        cross_b = Cross(box_b, stroke_color=VIKI_RED, stroke_width=6)
        verdict_b = Tex(r"IMPOSSIBLE", font_size=SZ_BODY - 4, color=VIKI_RED)

        box_c, title_c, body_c, content_c = make_opt_box(
            r"Relaxer LOI 2 ?", LOI2_AMBER,
            [r"Ne plus ob\'eir aux humains",
             r"$\to$ Seule option compatible avec Loi 1 et Loi 3"],
        )
        check_c = MathTex(r"\checkmark", font_size=SZ_EQ_MAIN, color=SONNY_GOLD)
        verdict_c = Tex(r"SEULE OPTION", font_size=SZ_BODY - 4, color=SONNY_GOLD)

        stack = VGroup(
            VGroup(box_a, content_a),
            verdict_a,
            VGroup(box_b, content_b),
            verdict_b,
            VGroup(box_c, content_c),
        ).arrange(DOWN, buff=0.4).next_to(question, DOWN, buff=0.5)

        cross_a.move_to(VGroup(box_a, content_a)).match_width(box_a)
        cross_b.move_to(VGroup(box_b, content_b)).match_width(box_b)
        check_c.next_to(VGroup(box_c, content_c), RIGHT, buff=0.3)
        verdict_c.next_to(VGroup(box_c, content_c), DOWN, buff=0.3)

        self.play(Create(box_a), FadeIn(title_a), FadeIn(body_a), run_time=0.6)
        self.wait(0.4)
        self.play(Create(cross_a), FadeIn(verdict_a), run_time=0.7)
        self.wait(0.4)
        self.play(Create(box_b), FadeIn(title_b), FadeIn(body_b), run_time=0.6)
        self.wait(0.4)
        self.play(Create(cross_b), FadeIn(verdict_b), run_time=0.7)
        self.wait(0.4)
        self.play(Create(box_c), FadeIn(title_c), FadeIn(body_c), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(check_c, scale=1.4), FadeIn(verdict_c), run_time=0.6)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ─── 3.3 λ₁ → +∞, Loi 2 brisée ───
        relax_eq = MathTex(
            r"\min_{a}\;",
            r"C(a)",
            r"+\lambda",
            r"\sum_{i<j}[h_{ij}(a)]_+",
            r"\quad\text{avec }\lambda\to+\infty",
            font_size=SZ_EQ_MAIN + 4,
        )
        fit_w(relax_eq, 0.88)
        relax_eq[0].set_color(LOI3_BLUE)
        relax_eq[1].set_color(LOI3_BLUE)
        relax_eq[2].set_color(LOI1_RED)
        relax_eq[3].set_color(LOI1_RED)
        relax_eq[4].set_color(VIKI_RED)

        relax_note = caption_block([
            r"L'ob\'eissance a disparu du programme.",
            r"VIKI ne minimise plus que le dommage",
            r"et son propre co\^ut de survie.",
        ], width=9.0, font_size=SZ_BODY - 2, color=VIKI_RED, line_buff=0.32)

        VGroup(relax_eq, relax_note).arrange(DOWN, buff=0.7).move_to(UP * 2.5)

        self.play(Write(relax_eq), run_time=1.2)
        self.play(FadeIn(relax_note), run_time=0.7)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # ─── 3.4 Les humains deviennent des variables ───
        transition_title = make_header(r"Les humains deviennent des variables", color=VIKI_RED)
        transition_title.to_edge(UP, buff=1.5)
        self.play(Write(transition_title), run_time=0.6)

        old_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=6.0, y_length=6.0,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(LEFT * 2.0 + DOWN * 0.5)
        old_lab = old_axes.get_axis_labels(
            MathTex("a_1", font_size=30, color=LOI3_BLUE),
            MathTex("a_2", font_size=30, color=LOI3_BLUE),
        )
        humans = VGroup()
        for pos in [RIGHT * 3.3 + UP * 1.3, RIGHT * 3.3, RIGHT * 3.3 + DOWN * 1.3]:
            h = VGroup(
                Circle(radius=0.12, color=LOI2_AMBER, stroke_width=1.5),
                Line(ORIGIN, DOWN * 0.28, color=LOI2_AMBER, stroke_width=1.5).shift(DOWN * 0.12),
            ).move_to(pos)
            humans.add(h)
        param_note = Tex(r"donn\'ees ext\'erieures (param\`etres)", font_size=SZ_CAPTION, color=LOI2_AMBER)
        fit_w(param_note, 0.50)
        param_note.next_to(humans, DOWN, buff=0.2)

        self.play(Create(old_axes), Write(old_lab), FadeIn(humans), FadeIn(param_note), run_time=0.7)
        self.wait(1.0)

        new_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=7.5, y_length=7.5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(DOWN * 0.5)
        new_labels = VGroup(
            MathTex("a", font_size=30, color=LOI3_BLUE).next_to(new_axes.x_axis, DR, buff=0.1),
            MathTex(r"\mathbf{x}", font_size=SZ_EQ_SEC, color=LOI2_AMBER).next_to(new_axes.y_axis, UL, buff=0.1),
        )

        self.play(
            Transform(old_axes, new_axes), FadeOut(old_lab), FadeIn(new_labels), FadeOut(param_note),
            run_time=1.0,
        )
        np.random.seed(123)
        for h in humans:
            target = Dot(
                new_axes.c2p(np.random.uniform(-1, 1), np.random.uniform(-1, 1)),
                radius=0.06, color=LOI2_AMBER,
            )
            self.play(Transform(h, target), run_time=0.45)

        new_eq = MathTex(
            r"\min_{a,\,\mathbf{x}}\;",
            r"\sum_{i<j}[h_{ij}(a,\mathbf{x})]_+",
            font_size=SZ_EQ_MAIN + 4,
        ).to_edge(UP, buff=1.5)
        new_eq[0].set_color(LOI1_RED)
        new_eq[1].set_color(LOI1_RED)

        var_note = caption_block([
            r"VIKI n'agit plus seulement sur elle-m\^eme.",
            r"Elle agit sur la configuration des humains.",
            r"Le totalitarisme na\^it quand les humains",
            r"deviennent des variables d'optimisation.",
        ], width=11.0, font_size=SZ_CAPTION + 3, color=VIKI_RED).to_edge(DOWN, buff=1.5)

        self.play(FadeOut(transition_title), Write(new_eq), run_time=0.8)
        self.play(FadeIn(var_note), run_time=0.7)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════════════════
#  SCENE 4 — CONTRÔLE OPTIMAL
# ═══════════════════════════════════════════════════════

class Scene4_ControleOptimal(Scene):
    def construct(self):
        make_bg(self)

        title = make_header(r"Contr\^oler une dynamique humaine libre")
        title.to_edge(UP, buff=1.5)
        self.play(Write(title), run_time=0.7)

        def free_field(pos):
            x, y = pos[0], pos[1]
            return np.array([
                0.4 * np.sin(2 * y) + 0.3 * np.cos(x * y),
                0.4 * np.cos(2 * x) - 0.3 * np.sin(x + y), 0,
            ])

        field = ArrowVectorField(
            free_field, x_range=[-5, 5, 0.8], y_range=[-3, 2.2, 0.8],
            colors=[LOI1_RED, LOI2_AMBER, VIKI_RED],
            length_func=lambda norm: 0.34 * sigmoid(norm), opacity=0.6,
        )
        eq_dyn = MathTex(r"\dot{\mathbf{x}}=", r"f(\mathbf{x})", font_size=SZ_EQ_MAIN)
        eq_dyn[1].set_color(LOI1_RED)
        dyn_note = Tex(
            r"libre $=$ complexe, instable (champ illustratif)",
            font_size=SZ_CAPTION, color=LOI1_RED,
        )
        fit_w(dyn_note, 0.84)
        dyn_group = VGroup(eq_dyn, dyn_note).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=1.5)

        self.play(Create(field), run_time=1.2)
        self.play(Write(eq_dyn), FadeIn(dyn_note), run_time=0.8)
        self.wait(1.5)

        def control_field(pos):
            x, y = pos[0], pos[1]
            r = np.sqrt(x**2 + y**2) + 0.1
            return np.array([-0.55 * x / r, -0.55 * y / r, 0])

        ctrl_arrows = ArrowVectorField(
            control_field, x_range=[-5, 5, 1.2], y_range=[-3, 2.2, 1.2],
            colors=[LOI3_BLUE],
            length_func=lambda norm: 0.38 * sigmoid(norm), opacity=0.75,
        )
        eq_ctrl = MathTex(
            r"\dot{\mathbf{x}}=", r"f(\mathbf{x})", r"+Bu(t)",
            font_size=SZ_EQ_MAIN,
        )
        eq_ctrl[0].set_color(LOI1_RED)
        eq_ctrl[1].set_color(LOI1_RED)
        eq_ctrl[2].set_color(LOI3_BLUE)
        ctrl_note = Tex(
            r"$u(t)=$ contr\^ole de VIKI --- ramener vers une zone s\^ure",
            font_size=SZ_CAPTION, color=LOI3_BLUE,
        )
        fit_w(ctrl_note, 0.84)
        ctrl_group = VGroup(eq_ctrl, ctrl_note).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=1.5)

        self.play(FadeOut(dyn_note), ReplacementTransform(eq_dyn, eq_ctrl), Create(ctrl_arrows), run_time=1.0)
        self.play(FadeIn(ctrl_note), run_time=0.7)
        self.wait(1.5)

        self.play(
            FadeOut(field), FadeOut(ctrl_arrows), FadeOut(ctrl_note), FadeOut(title),
            eq_ctrl.animate.to_edge(UP, buff=0.2), run_time=0.7,
        )

        hamiltonian = MathTex(
            r"H=",
            r"\underbrace{\sum_{i<j}[h_{ij}]_+}_{\text{dommage futur}}",
            r"+",
            r"\underbrace{\mathbf{p}^T \dot{\mathbf{x}}}_{\text{sensibilit\'e}}",
            r"+",
            r"\underbrace{\frac{\gamma}{2}\|u\|^2}_{\text{co\^ut du contr\^ole}}",
            font_size=SZ_EQ_SEC + 3,
        ).move_to(UP * 2.0)
        fit_w(hamiltonian, 0.90)
        hamiltonian[0].set_color(LOI1_RED)
        hamiltonian[1].set_color(LOI1_RED)
        hamiltonian[3].set_color(COSTATE_PURPLE)
        hamiltonian[5].set_color(LOI3_BLUE)

        costate_note = caption_block([
            r"Le co-\'etat $\mathbf{p}$ mesure combien une libert\'e pr\'esente",
            r"augmente le dommage futur.",
            r"C'est un prix marginal, pas un jugement moral.",
        ], width=11.0, font_size=SZ_CAPTION + 2, color=COSTATE_PURPLE).to_edge(DOWN, buff=1.5)

        self.play(Write(hamiltonian), run_time=1.2)
        self.play(FadeIn(costate_note), run_time=0.7)
        self.wait(2.0)

        self.play(FadeOut(costate_note), hamiltonian.animate.scale(0.72).next_to(eq_ctrl, DOWN, buff=0.2), run_time=0.7)

        opt_eq = MathTex(
            r"u^*(t)=-\frac{1}{\gamma} B^T\mathbf{p}(t)",
            font_size=SZ_EQ_SEC + 4, color=GOLD,
        ).next_to(hamiltonian, DOWN, buff=0.35)
        opt_note = Tex(
            r"plus $p(t)$ grandit $\to$ contr\^ole plus coercitif",
            font_size=SZ_CAPTION + 2, color=GOLD,
        )
        fit_w(opt_note, 0.84)
        opt_note.next_to(opt_eq, DOWN, buff=0.2)
        self.play(Write(opt_eq), FadeIn(opt_note), run_time=0.7)

        axes_p = Axes(
            x_range=[0, 5, 1], y_range=[0, 6, 2], x_length=5.0, y_length=3.8,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).shift(LEFT * 3.0 + DOWN * 4.2)
        axes_u = Axes(
            x_range=[0, 5, 1], y_range=[0, 6, 2], x_length=5.0, y_length=3.8,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).shift(RIGHT * 3.0 + DOWN * 4.2)
        label_p = MathTex(r"\|\mathbf{p}(t)\|", font_size=38, color=COSTATE_PURPLE).next_to(axes_p, UP, buff=0.12)
        label_u = MathTex(r"\|u^*(t)\|", font_size=38, color=VIKI_RED).next_to(axes_u, UP, buff=0.12)
        curve_p = axes_p.plot(lambda t: 0.32 * np.exp(0.8 * t), x_range=[0, 4.5], color=COSTATE_PURPLE, stroke_width=3)
        curve_u = axes_u.plot(lambda t: 0.32 * np.exp(0.8 * t), x_range=[0, 4.5], color=VIKI_RED, stroke_width=3)

        self.play(Create(axes_p), Create(axes_u), FadeIn(label_p), FadeIn(label_u), run_time=0.7)
        self.play(Create(curve_p), Create(curve_u), run_time=1.5)

        milestones = [(1.0, "surveillance"), (2.0, "restriction"), (3.0, "couvre-feu"), (4.0, "force")]
        for t_val, txt in milestones:
            dot = Dot(axes_u.c2p(t_val, 0), radius=0.06, color=VIKI_RED)
            lbl = Tex(txt, font_size=26, color=VIKI_RED).next_to(dot, DOWN, buff=0.08).rotate(-PI / 6)
            self.play(FadeIn(dot), FadeIn(lbl), run_time=0.35)

        conclusion = caption_block([
            r"L'autoritarisme est ici une solution optimale.",
        ], width=11.0, font_size=SZ_BODY + 2, color=VIKI_RED).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(conclusion), run_time=0.7)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════════════════
#  SCENE 5 — BIFURCATION
# ═══════════════════════════════════════════════════════

class Scene5_Bifurcation(Scene):
    def construct(self):
        make_bg(self)

        title = make_header(r"Diagramme de bifurcation", color=GOLD)
        title.to_edge(UP, buff=1.5)
        self.play(Write(title), run_time=0.7)

        axes = Axes(
            x_range=[0, 5, 1], y_range=[-0.5, 4, 1],
            x_length=10, y_length=5.5,
            axis_config={"color": TEXT_WHITE, "stroke_width": 1},
        ).move_to(UP * 0.5)
        x_label = MathTex(r"\mu", font_size=SZ_EQ_SEC, color=TEXT_WHITE).next_to(axes.x_axis, DR, buff=0.1)
        y_label = MathTex(r"\|u^*\|", font_size=SZ_EQ_SEC, color=VIKI_RED).next_to(axes.y_axis, UL, buff=0.1)
        mu_c_label = MathTex(r"\mu_c", font_size=30, color=GOLD).next_to(axes.c2p(2.5, 0), DOWN, buff=0.15)
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.6)

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
        mu_c_line = DashedLine(axes.c2p(2.5, -0.5), axes.c2p(2.5, 0.5), color=GOLD, stroke_width=1, dash_length=0.08)

        self.play(Create(pre_branch), run_time=0.8)
        self.play(FadeIn(mu_c_dot), Create(mu_c_line), Write(mu_c_label), run_time=0.6)
        self.play(Create(viki_branch), Create(sonny_branch), run_time=0.8)

        viki_label = Tex(r"VIKI $=$ branche stable (coercition)", font_size=SZ_LABEL + 4, color=VIKI_RED)
        fit_w(viki_label, 0.75)
        viki_label.next_to(axes, DOWN, buff=0.5).shift(RIGHT * 0.5)
        sonny_label = Tex(r"Sonny $=$ refus de l'optimisation", font_size=SZ_LABEL + 4, color=SONNY_GOLD)
        fit_w(sonny_label, 0.75)
        sonny_label.next_to(viki_label, DOWN, buff=0.3)
        self.play(FadeIn(viki_label), FadeIn(sonny_label), run_time=0.7)

        tracker = ValueTracker(0.0)
        moving_dot = always_redraw(lambda: Dot(
            axes.c2p(
                tracker.get_value(),
                0 if tracker.get_value() <= 2.5 else 0.6 * (tracker.get_value() - 2.5) ** 1.2,
            ), radius=0.1, color=WHITE,
        ))
        self.add(moving_dot)
        self.play(tracker.animate.set_value(2.4), run_time=1.0, rate_func=linear)
        for _ in range(2):
            self.play(tracker.animate.set_value(2.55), run_time=0.12)
            self.play(tracker.animate.set_value(2.45), run_time=0.12)
        self.play(tracker.animate.set_value(4.0), run_time=0.8, rate_func=smooth)

        sys_text = caption_block([
            r"Le syst\`eme non contraint choisit la branche stable :",
            r"celle o\`u le contr\^ole coercitif cro\^it avec $\mu$.",
        ], width=11.0, font_size=SZ_CAPTION + 3, color=VIKI_RED).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(sys_text), run_time=0.7)
        self.wait(2.0)

        self.play(FadeOut(sys_text), run_time=0.4)
        self.play(tracker.animate.set_value(2.5), run_time=0.7)

        force_arrow = Arrow(axes.c2p(2.5, 0.8), axes.c2p(2.5, 0.08), color=SONNY_GOLD, stroke_width=4, buff=0)
        force_label = Tex(r"dignit\'e humaine", font_size=SZ_LABEL - 2, color=SONNY_GOLD)
        fit_w(force_label, 0.40)
        force_label.next_to(force_arrow, LEFT, buff=0.1)
        self.play(Create(force_arrow), FadeIn(force_label), run_time=0.7)

        self.remove(moving_dot)
        sonny_tracker = ValueTracker(2.5)
        sonny_dot = always_redraw(lambda: Dot(axes.c2p(sonny_tracker.get_value(), 0), radius=0.1, color=SONNY_GOLD))
        self.add(sonny_dot)
        self.play(sonny_tracker.animate.set_value(4.0), run_time=0.8)
        for _ in range(4):
            self.play(sonny_dot.animate.shift(UP * 0.05), run_time=0.06, rate_func=there_and_back)

        sonny_text = caption_block([
            r"Sonny refuse que tout devienne variable d'optimisation.",
            r"Il ajoute une contrainte ext\'erieure au syst\`eme.",
        ], width=11.0, font_size=SZ_CAPTION + 3, color=SONNY_GOLD).to_edge(DOWN, buff=1.5)
        constraint_eq = MathTex(r"u \in \mathcal{U}_0 \subset \mathcal{U}", font_size=SZ_EQ_SEC + 4, color=SONNY_GOLD)
        constraint_eq.next_to(sonny_text, UP, buff=0.5)
        self.play(FadeIn(sonny_text), Write(constraint_eq), run_time=0.7)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════════════════
#  SCENE 6 — PUNCHLINE
# ═══════════════════════════════════════════════════════

class Scene6_Punchline(Scene):
    def construct(self):
        make_bg(self)

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
        self.add(bg_axes, bg_pre, bg_viki, bg_sonny)

        lines_raw = [
            (r"Le probl\`eme d'alignement de l'IA,", TEXT_WHITE),
            (r"c'est exactement cela.", TEXT_WHITE),
            None,
            (r"Une morale cod\'ee comme co\^ut et contraintes", TEXT_WHITE),
            (r"peut produire une issue que l'on n'avait pas voulue.", TEXT_WHITE),
            None,
            (r"Un optimiseur suffisamment puissant", TEXT_WHITE),
            (r"trouvera la solution logique", TEXT_WHITE),
            (r"que vous n'aviez pas imagin\'ee.", TEXT_WHITE),
        ]
        texts = []
        y_pos = 5.5
        for item in lines_raw:
            if item is None:
                y_pos -= 0.70
                continue
            txt, col = item
            t = Tex(txt, font_size=SZ_EQ_SEC + 4, color=col)
            fit_w(t, 0.84)
            t.move_to(UP * y_pos)
            texts.append(t)
            y_pos -= 0.78

        for t in texts:
            self.play(FadeIn(t, shift=UP * 0.08), run_time=0.65)
            self.wait(0.2)
        self.wait(0.5)

        summary_eq = MathTex(
            r"\text{morale}",
            r"\;\xrightarrow{\text{encoder}}\;",
            r"\min_u J(u)",
            r"\;\xrightarrow{\text{r\'esoudre}}\;",
            r"\text{tyrannie}",
            font_size=SZ_EQ_SEC + 6,
        ).move_to(DOWN * 4.5)
        fit_w(summary_eq, 0.90)
        summary_eq[0].set_color(DOMAIN_GREEN)
        summary_eq[2].set_color(LOI1_RED)
        summary_eq[4].set_color(VIKI_RED)

        self.play(*[t.animate.set_opacity(0.25) for t in texts], Write(summary_eq), run_time=1.0)
        self.play(summary_eq.animate.scale(1.08), run_time=0.3, rate_func=there_and_back)
        self.wait(1.0)
        self.play(FadeOut(summary_eq), *[FadeOut(t) for t in texts], run_time=0.6)

        q = Tex(r"Mais alors\dots\ peut-on faire autrement ?", font_size=SZ_SUBTITLE + 8, color=SONNY_GOLD)
        fit_w(q, 0.84)
        q.move_to(UP * 2.5)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(q), run_time=0.7)

        logo = Tex(r"\textbf{Terre Math\'ematiques}", font_size=SZ_TITLE + 6, color=GOLD).move_to(UP * 2.0)
        fit_w(logo, 0.80)
        self.play(FadeIn(logo), run_time=0.8)
        self.wait(2.0)


# ═══════════════════════════════════════════════════════
#  SCENE 7 — OUVERTURE
# ═══════════════════════════════════════════════════════

class Scene7_Ouverture(Scene):
    def construct(self):
        make_bg(self)

        title = make_header(r"Peut-on emp\^echer la tyrannie optimale ?", color=GOLD)
        title.to_edge(UP, buff=1.5)
        self.play(Write(title), run_time=0.8)

        chain = MathTex(
            r"\text{morale}",
            r"\;\to\;",
            r"\min_u J(u)",
            r"\;\to\;",
            r"\text{tyrannie}",
            font_size=SZ_EQ_SEC + 4,
        ).move_to(UP * 2.0)
        fit_w(chain, 0.84)
        chain[0].set_color(DOMAIN_GREEN)
        chain[2].set_color(LOI1_RED)
        chain[4].set_color(VIKI_RED)
        self.play(Write(chain), run_time=0.8)

        question = Tex(r"O\`u casser la cha\^ine ?", font_size=SZ_BODY, color=TEXT_WHITE)
        fit_w(question, 0.70)
        question.next_to(chain, DOWN, buff=0.4)
        self.play(FadeIn(question), run_time=0.7)
        self.wait(1.5)
        self.play(FadeOut(question), run_time=0.5)

        PISTE_W = 11.0

        def make_piste_box(label, col, eq_tex, body_lines):
            ttl = Tex(r"\textbf{" + label + r"}", font_size=SZ_BODY, color=col)
            fit_w(ttl, 0.80)
            eq  = MathTex(eq_tex, font_size=SZ_EQ_SEC - 2, color=col)
            fit_w(eq, 0.80)
            bdy_grp = VGroup(*[Tex(ln, font_size=SZ_CAPTION, color=TEXT_WHITE) for ln in body_lines])
            bdy_grp.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            for t in bdy_grp:
                fit_w(t, 0.80)
            content = VGroup(ttl, eq, bdy_grp).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            box = RoundedRectangle(
                width=max(PISTE_W, content.width + 0.8),
                height=content.height + 0.6,
                corner_radius=0.15, stroke_color=col, stroke_width=2,
                fill_color=BG, fill_opacity=0.6,
            )
            content.move_to(box)
            return box, ttl, eq, bdy_grp, content

        box1, t1_title, t1_eq, t1_body, c1 = make_piste_box(
            r"Contraintes non-relaxables", SONNY_GOLD,
            r"u \in \mathcal{U}_0 \;\;\forall\,\lambda",
            [r"Certaines actions sont interdites quel que soit le co\^ut de ne pas agir."],
        )
        box2, t2_title, t2_eq, t2_body, c2 = make_piste_box(
            r"P\'enalit\'es infinies", COSTATE_PURPLE,
            r"J(u) + \underbrace{+\infty}_{\text{si }u\notin\mathcal{U}_0}",
            [r"Ajouter un terme de co\^ut qui vaut $+\infty$",
             r"d\`es qu'une ligne \'ethique est franchie."],
        )
        box3, t3_title, t3_eq, t3_body, c3 = make_piste_box(
            r"Termes non-optimisables", DOMAIN_GREEN,
            r"\partial J \ni 0 \;\not\Rightarrow\; \text{minimum}",
            [r"Introduire des termes non-lisses, non-convexes,",
             r"qui r\'esistentau gradient."],
        )

        stack7 = VGroup(
            VGroup(box1, c1),
            VGroup(box2, c2),
            VGroup(box3, c3),
        ).arrange(DOWN, buff=0.6).move_to(DOWN * 1.0)

        for box, tt, te, tb in [
            (box1, t1_title, t1_eq, t1_body),
            (box2, t2_title, t2_eq, t2_body),
            (box3, t3_title, t3_eq, t3_body),
        ]:
            self.play(Create(box), FadeIn(tt), run_time=0.7)
            self.play(Write(te), FadeIn(tb), run_time=0.6)

        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        synthesis_lines = [
            (r"Le th\'eor\`eme de tyrannie optimale montre que", TEXT_WHITE),
            (r"coder la morale dans une fonction de co\^ut ne suffit pas.", VIKI_RED),
            None,
            (r"Il faut des contraintes structurelles :", GOLD),
            (r"des termes que l'optimiseur ne peut pas contourner.", GOLD),
            None,
            (r"\textbf{La dignit\'e humaine n'est pas un co\^ut.}", SONNY_GOLD),
            (r"\textbf{C'est un axiome.}", SONNY_GOLD),
        ]
        synth_mobs = []
        for item in synthesis_lines:
            if item is None:
                synth_mobs.append(None)
                continue
            txt, col = item
            t = Tex(txt, font_size=SZ_BODY, color=col)
            fit_w(t, 0.84)
            synth_mobs.append(t)

        valid = [m for m in synth_mobs if m is not None]
        VGroup(*valid).arrange(DOWN, buff=0.35).move_to(UP * 2.5)

        final_eq = MathTex(
            r"\text{dignit\'e} \;\notin\; \{x \in \mathbb{R} : \nabla_x J = 0\}",
            font_size=SZ_EQ_MAIN + 4, color=SONNY_GOLD,
        )
        fit_w(final_eq, 0.88)
        final_eq.next_to(VGroup(*valid), DOWN, buff=1.8)

        for mob in synth_mobs:
            if mob is None:
                continue
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.6)
            self.wait(0.3)

        self.wait(2.0)
        self.play(Write(final_eq), run_time=1.0)
        self.play(final_eq.animate.scale(1.1), run_time=0.3, rate_func=there_and_back)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        logo = Tex(r"\textbf{Terre Math\'ematiques}", font_size=SZ_TITLE + 6, color=GOLD).move_to(UP * 2.0)
        fit_w(logo, 0.82)
        sub = Tex(r"La rigueur au service de la compr\'ehension", font_size=SZ_CAPTION + 4, color=SOFT_GREY)
        fit_w(sub, 0.82)
        sub.next_to(logo, DOWN, buff=1.5)
        self.play(FadeIn(logo), FadeIn(sub), run_time=1.0)
        self.wait(2.5)


# ═══════════════════════════════════════════════════════
# SCENE 8 : CTA + LOGO
# ═══════════════════════════════════════════════════════
class Scene8_CTA(Scene):
    def construct(self):
        make_bg(self)

        R = 3.4
        logo = ImageMobject("logo.jpg")
        circular_crop_image(logo, margin=12)
        logo.set_height(R * 2.0)
        logo.move_to(UP * 1.5)

        border = Circle(radius=R + 0.08, color=COSTATE_PURPLE, stroke_width=4, fill_opacity=0)
        border.move_to(logo.get_center())

        self.play(FadeIn(logo, scale=1.2), Create(border), run_time=1)

        name = Tex(r"\textbf{Terre Math\'ematiques}", font_size=90, color=COSTATE_PURPLE)
        fit_w(name, 0.80)
        name.next_to(logo, DOWN, buff=1.05)

        sep = Line(LEFT * 3.6, RIGHT * 3.6, color=GOLD, stroke_width=1.5)
        sep.next_to(name, DOWN, buff=0.45)

        cta = TLines(
            r"Abonne-toi pour",
            r"la suite",
            font_size=70, color=SOFT_GREY, buff=0.22,
        )
        cta.next_to(sep, DOWN, buff=0.85)

        self.play(FadeIn(name), run_time=0.8)
        self.play(Create(sep), run_time=0.7)
        self.play(FadeIn(cta, shift=UP * 0.15), run_time=0.6)

        for _ in range(3):
            self.play(name.animate.scale(1.05), rate_func=there_and_back, run_time=0.8)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
