from manim import *
import numpy as np

# =============================================================================
# MÉTADONNÉES
# =============================================================================
SCENES = [
    "Scene01_Titre",
    "Scene02_EnigmaPrincipe",
    "Scene03_ReflecteurTheoreme",
    "Scene04_TuringCribs",
    "Scene05_DeLaFailleAuRenseignement",
    "Scene06_Conclusion",
    "Scene07_CTA",
]
OUTPUT_NAME = "turing_enigma_terre_maths.mp4"
OUTPUT_DIR = r"media\videos\turing_enigma_terre_maths\1920p30"

# =============================================================================
# FORMAT PORTRAIT
# =============================================================================
config.frame_width = 4.5
config.frame_height = 8.0
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

# =============================================================================
# PALETTE TERRE MATHÉMATIQUES
# =============================================================================
SABLE = "#F5F0E8"
AUBERGINE = "#4A1942"
AUBERG_DARK = "#2E0E28"
GOLD = "#C8A951"
SOFT_BLACK = "#2C2C2C"
RICE_LIGHT = "#E8D9B0"
RICE_DARK = "#A0845C"
GREEN_OK = "#27AE60"
BLUE_OK = "#2E86C1"
RED_WARN = "#C0392B"

# =============================================================================
# TAILLES DE POLICE
# =============================================================================
HEADER_FONT = 30
TITLE_FONT = 54
SUBTITLE_FONT = 38
HOOK_FONT = 34
BODY_FONT = 20
BODY_SMALL_FONT = 17
MATH_FONT = 30
MATH_SMALL_FONT = 24

# =============================================================================
# UTILITAIRES
# =============================================================================

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


def theorem_box(mob):
    box = SurroundingRectangle(
        mob,
        color=GOLD,
        buff=0.16,
        stroke_width=2,
        fill_color=RICE_LIGHT,
        fill_opacity=0.42,
    )
    return VGroup(box, mob)


# =============================================================================
# PETITS OBJETS VISUELS
# =============================================================================

class RotorBlock(VGroup):
    def __init__(self, label, width=0.58, height=0.82, **kwargs):
        super().__init__(**kwargs)
        rect = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=height,
            fill_color=RICE_LIGHT,
            fill_opacity=1,
            stroke_color=AUBERGINE,
            stroke_width=2,
        )
        txt = Tex(label, font_size=22, color=AUBERGINE)
        txt.move_to(rect.get_center())
        self.add(rect, txt)
        self.rect = rect
        self.txt = txt


class ReflectorBlock(VGroup):
    def __init__(self, width=0.78, height=0.82, **kwargs):
        super().__init__(**kwargs)
        rect = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=height,
            fill_color=AUBERGINE,
            fill_opacity=1,
            stroke_color=GOLD,
            stroke_width=2.2,
        )
        txt = Tex(r"R", font_size=28, color=SABLE)
        txt.move_to(rect.get_center())
        self.add(rect, txt)
        self.rect = rect
        self.txt = txt


class ReflectorPairing(VGroup):
    def __init__(self, radius=1.18, n=10, **kwargs):
        super().__init__(**kwargs)
        arc = Arc(radius=radius, start_angle=-PI / 2, angle=PI, color=AUBERGINE, stroke_width=3)
        contacts = VGroup()
        pts = []
        for i in range(n):
            theta = -PI / 2 + (i + 0.5) * PI / n
            p = radius * np.array([np.cos(theta), np.sin(theta), 0])
            dot = Dot(p, radius=0.036, color=GOLD)
            contacts.add(dot)
            pts.append(p)
        chords = VGroup()
        pairs = [(0, 9), (1, 6), (2, 4), (3, 8), (5, 7)]
        for a, b in pairs:
            chords.add(Line(pts[a], pts[b], color=RICE_DARK, stroke_width=2.2))
        self.add(arc, chords, contacts)
        self.arc = arc
        self.chords = chords
        self.contacts = contacts


def make_machine_row():
    p = RotorBlock(r"$P_t$", width=0.72)
    r1 = RotorBlock(r"$R_1$")
    r2 = RotorBlock(r"$R_2$")
    r3 = RotorBlock(r"$R_3$")
    ref = ReflectorBlock()
    row = VGroup(p, r1, r2, r3, ref).arrange(RIGHT, buff=0.12)
    return row, p, r1, r2, r3, ref


def collision_card(left, right, ok=True):
    bg = RoundedRectangle(
        corner_radius=0.1,
        width=2.55,
        height=0.5,
        fill_color=RICE_LIGHT if ok else "#F3D6D3",
        fill_opacity=1,
        stroke_color=GREEN_OK if ok else RED_WARN,
        stroke_width=2,
    )
    expr = Tex(
        rf"{left} $\mapsto$ {right}",
        font_size=24,
        color=SOFT_BLACK if ok else RED_WARN,
    )
    expr.move_to(bg.get_center())
    if ok:
        mark = Tex(r"compatible", font_size=16, color=GREEN_OK)
    else:
        mark = Tex(r"impossible", font_size=16, color=RED_WARN)
    mark.next_to(bg, RIGHT, buff=0.12)
    return VGroup(bg, expr, mark)


# =============================================================================
# SCÈNE 01 — TITRE / HOOK
# =============================================================================

class Scene01_Titre(Scene):
    def construct(self):
        make_bg(self)

        title = Tex(r"\textbf{Comment Turing a cass\'e Enigma}", font_size=TITLE_FONT, color=AUBERGINE)
        fit_w(title, 0.82)

        subtitle = TLines(
            r"Une contrainte alg\'ebrique,",
            r"un levier cryptanalytique.",
            font_size=SUBTITLE_FONT,
            color=GOLD,
            buff=0.16,
        )
        fit_w(subtitle, 0.78)

        sep_w = min(config.frame_width * 0.76, max(title.width, subtitle.width) * 1.04)
        sep = Line(LEFT * sep_w / 2, RIGHT * sep_w / 2, color=GOLD, stroke_width=2)

        author = Tex(r"Terre Math\'ematiques", font_size=28, color=AUBERGINE)
        fit_w(author, 0.68)

        block = VGroup(title, subtitle, sep, author).arrange(DOWN, buff=0.42, aligned_edge=ORIGIN)

        hook = TLines(
            r"Des milliards de r\'eglages.",
            r"Et pourtant, une structure la trahit.",
            font_size=BODY_FONT,
            color=SOFT_BLACK,
            buff=0.16,
        )
        fit_w(hook, 0.82)

        full = VGroup(block, hook).arrange(DOWN, buff=0.72, aligned_edge=ORIGIN)
        full.move_to(ORIGIN)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)
        self.play(Create(sep), FadeIn(author), run_time=0.7)
        self.play(FadeIn(hook, shift=UP * 0.2), run_time=0.8)
        self.wait(3.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# =============================================================================
# SCÈNE 02 — PRINCIPE D'ENIGMA
# =============================================================================

class Scene02_EnigmaPrincipe(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Le principe d'Enigma")

        top_text = TLines(
            r"Chaque lettre traverse les rotors,",
            r"rebondit sur un r\'eflecteur,",
            r"puis revient en sens inverse.",
            font_size=BODY_FONT,
            color=SOFT_BLACK,
            buff=0.17,
        )

        machine_row, p, r1, r2, r3, ref = make_machine_row()
        fit_w(machine_row, 0.86)

        bottom_text = TLines(
            r"\`A l'instant $t$, on obtient une permutation $\sigma_t$.",
            r"Mais cette permutation n'est pas quelconque.",
            font_size=BODY_SMALL_FONT,
            color=SOFT_BLACK,
            buff=0.16,
        )

        full = VGroup(header, top_text, machine_row, bottom_text).arrange(
            DOWN, buff=0.42, aligned_edge=ORIGIN
        )
        full.move_to(ORIGIN)

        dots = VGroup(*[Dot(radius=0.03, color=GOLD) for _ in range(6)])
        start = machine_row.get_left() + LEFT * 0.26
        end = machine_row.get_right() + RIGHT * 0.26
        path_points = [
            start,
            p.get_center(),
            r1.get_center(),
            r2.get_center(),
            r3.get_center(),
            ref.get_center(),
            r3.get_center() + DOWN * 0.17,
            r2.get_center() + DOWN * 0.17,
            r1.get_center() + DOWN * 0.17,
            p.get_center() + DOWN * 0.17,
            end,
        ]
        signal = Dot(path_points[0], radius=0.055, color=RED_WARN)

        sigma = MathTex(r"\sigma_t", font_size=MATH_FONT, color=AUBERGINE)
        sigma.next_to(machine_row, DOWN, buff=0.24)
        fit_w(sigma, 0.32)

        self.play(Write(header), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in top_text], lag_ratio=0.18),
            run_time=1.5,
        )
        self.play(FadeIn(machine_row, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(signal), run_time=0.2)
        for pt in path_points[1:]:
            self.play(signal.animate.move_to(pt), run_time=0.18, rate_func=linear)
        self.play(Write(sigma), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in bottom_text], lag_ratio=0.18),
            run_time=1.2,
        )
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# =============================================================================
# SCÈNE 03 — RÉFLECTEUR ET THÉORÈME
# =============================================================================

class Scene03_ReflecteurTheoreme(Scene):
    def construct(self):
        make_bg(self)

        header = make_header(r"Le r\'eflecteur")

        reflector = ReflectorPairing(radius=1.06, n=10)
        desc = TLines(
            r"Il relie les lettres deux \`a deux.",
            r"Donc une lettre repart toujours vers une autre.",
            font_size=BODY_FONT,
            color=SOFT_BLACK,
            buff=0.16,
        )

        theorem = MathTex(
            r"\sigma_t^2 = \mathrm{id}",
            r"\qquad",
            r"\sigma_t(x) \neq x",
            font_size=MATH_FONT,
            color=AUBERGINE,
        )
        fit_w(theorem, 0.86)
        theorem_full = theorem_box(theorem)

        theorem_text = TLines(
            r"Donc aucune lettre n'est chiffr\'ee par elle-m\^eme.",
            font_size=BODY_SMALL_FONT,
            color=SOFT_BLACK,
            buff=0.14,
        )

        definitions = VGroup(
            Tex(r"$P_t$ : trajet aller dans les rotors", font_size=BODY_SMALL_FONT, color=SOFT_BLACK),
            Tex(r"$R$ : r\'eflecteur", font_size=BODY_SMALL_FONT, color=SOFT_BLACK),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        for mob in definitions:
            fit_w(mob, 0.8)

        line1 = MathTex(r"\sigma_t = P_t^{-1} \circ R \circ P_t", font_size=MATH_SMALL_FONT, color=AUBERGINE)
        line2 = MathTex(
            r"\sigma_t^2 = P_t^{-1} R P_t P_t^{-1} R P_t = P_t^{-1} R^2 P_t = \mathrm{id}",
            font_size=20,
            color=AUBERGINE,
        )
        line3 = MathTex(r"\sigma_t(x)=x \Rightarrow R(P_t x)=P_t x", font_size=22, color=AUBERGINE)
        line4 = Tex(
            r"Or le r\'eflecteur \'echange des paires distinctes : pas de point fixe.",
            font_size=BODY_SMALL_FONT,
            color=RED_WARN,
        )
        for mob in [line1, line2, line3, line4]:
            fit_w(mob, 0.88)

        proof_block = VGroup(definitions, line1, line2, line3, line4).arrange(
            DOWN, buff=0.18, aligned_edge=LEFT
        )

        full = VGroup(header, reflector, desc, theorem_full, theorem_text).arrange(
            DOWN, buff=0.34, aligned_edge=ORIGIN
        )
        full.move_to(ORIGIN + UP * 0.35)

        proof_title = Tex(r"\textbf{Preuve}", font_size=24, color=AUBERGINE)
        proof_title.next_to(theorem_text, DOWN, buff=0.3)
        proof_block.next_to(proof_title, DOWN, buff=0.22)

        self.play(Write(header), run_time=0.7)
        self.play(Create(reflector.arc), FadeIn(reflector.contacts), run_time=0.8)
        self.play(LaggedStart(*[Create(c) for c in reflector.chords], lag_ratio=0.15), run_time=1.0)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in desc], lag_ratio=0.18),
            run_time=1.0,
        )
        self.wait(1.0)
        self.play(FadeIn(theorem_full, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(theorem_text, shift=UP * 0.1), run_time=0.7)
        self.wait(1.8)
        self.play(FadeIn(proof_title), run_time=0.5)
        self.play(FadeIn(definitions, shift=UP * 0.08), run_time=0.8)
        self.play(Write(line1), run_time=0.8)
        self.play(Write(line2), run_time=1.0)
        self.play(Write(line3), run_time=0.8)
        self.play(FadeIn(line4, shift=UP * 0.08), run_time=0.7)
        self.wait(3.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# =============================================================================
# SCÈNE 04 — TURING, CRIBS, COLLISIONS
# =============================================================================

class Scene04_TuringCribs(Scene):
    def construct(self):
        make_bg(self)

        header = make_header(r"L'id\'ee de Turing")

        crib_intro = TLines(
            r"On suppose qu'un mot probable appara\^it dans le message.",
            r"Alors on teste plusieurs alignements.",
            font_size=BODY_FONT,
            color=SOFT_BLACK,
            buff=0.16,
        )

        crib_word = Tex(r"\texttt{WETTERBERICHT}", font_size=28, color=AUBERGINE)
        fit_w(crib_word, 0.7)
        crib_tag = Tex(r"crib", font_size=16, color=GOLD)
        crib_group = VGroup(crib_tag, crib_word).arrange(DOWN, buff=0.06, aligned_edge=ORIGIN)

        cards = VGroup(
            collision_card("W", "Q", ok=True),
            collision_card("E", "E", ok=False),
            collision_card("T", "N", ok=True),
            collision_card("R", "R", ok=False),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        fit_w(cards, 0.9)

        rule = TLines(
            r"Si une lettre tombe sur elle-m\^eme, l'alignement est impossible.",
            r"C'est exactement la cons\'equence du th\'eor\`eme.",
            font_size=BODY_SMALL_FONT,
            color=SOFT_BLACK,
            buff=0.15,
        )

        formula = MathTex(
            r"\Pr(\text{au moins une collision}) \approx 1 - \left(\frac{25}{26}\right)^{13} \approx 39.7\%",
            font_size=19,
            color=AUBERGINE,
        )
        fit_w(formula, 0.9)
        formula_box = theorem_box(formula)

        note = Tex(
            r"Mod\`ele simplifi\'e : ind\'ependance approximative des 13 positions",
            font_size=13,
            color=RICE_DARK,
        )
        fit_w(note, 0.88)

        conclusion = TLines(
            r"Donc beaucoup d'alignements sont \`a rejeter imm\'ediatement.",
            r"Une propri\'et\'e alg\'ebrique devient un gain pratique.",
            font_size=BODY_SMALL_FONT,
            color=SOFT_BLACK,
            buff=0.15,
        )

        full = VGroup(header, crib_intro, crib_group, cards, rule, formula_box, note, conclusion).arrange(
            DOWN, buff=0.28, aligned_edge=ORIGIN
        )
        full.move_to(ORIGIN + UP * 0.15)

        bad_boxes = VGroup(
            SurroundingRectangle(cards[1][0], color=RED_WARN, buff=0.05, stroke_width=2),
            SurroundingRectangle(cards[3][0], color=RED_WARN, buff=0.05, stroke_width=2),
        )

        self.play(Write(header), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in crib_intro], lag_ratio=0.18),
            run_time=1.2,
        )
        self.play(FadeIn(crib_group, shift=UP * 0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.16), run_time=1.4)
        self.play(Create(bad_boxes[0]), Create(bad_boxes[1]), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in rule], lag_ratio=0.18),
            run_time=1.0,
        )
        self.play(FadeIn(formula_box, shift=UP * 0.08), run_time=0.8)
        self.play(FadeIn(note, shift=UP * 0.06), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in conclusion], lag_ratio=0.18),
            run_time=1.0,
        )
        self.wait(3.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)




# =============================================================================
# SCÈNE 05 — DE LA FAILLE AU RENSEIGNEMENT
# =============================================================================

class Scene05_DeLaFailleAuRenseignement(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("De la faille au renseignement")

        step1 = TLines(
            r"Le crib ne casse pas Enigma \`a lui seul.",
            r"Il sert \`a \'eliminer beaucoup de r\'eglages impossibles.",
            font_size=BODY_FONT,
            color=SOFT_BLACK,
            buff=0.16,
        )

        box_crib = RoundedRectangle(
            corner_radius=0.08, width=1.0, height=0.52,
            fill_color=RICE_LIGHT, fill_opacity=1, stroke_color=AUBERGINE, stroke_width=2
        )
        txt_crib = Tex(r"crib", font_size=20, color=AUBERGINE).move_to(box_crib.get_center())
        node_crib = VGroup(box_crib, txt_crib)

        box_bombe = RoundedRectangle(
            corner_radius=0.08, width=1.15, height=0.52,
            fill_color=AUBERGINE, fill_opacity=1, stroke_color=GOLD, stroke_width=2
        )
        txt_bombe = Tex(r"Bombe", font_size=20, color=SABLE).move_to(box_bombe.get_center())
        node_bombe = VGroup(box_bombe, txt_bombe)

        box_keys = RoundedRectangle(
            corner_radius=0.08, width=1.38, height=0.52,
            fill_color=RICE_LIGHT, fill_opacity=1, stroke_color=GREEN_OK, stroke_width=2
        )
        txt_keys = Tex(r"r\'eglages du jour", font_size=18, color=GREEN_OK).move_to(box_keys.get_center())
        node_keys = VGroup(box_keys, txt_keys)

        flow = VGroup(node_crib, node_bombe, node_keys).arrange(RIGHT, buff=0.28)
        fit_w(flow, 0.9)

        arrow1 = Arrow(node_crib.get_right() + RIGHT*0.03, node_bombe.get_left() + LEFT*0.03,
                       buff=0.02, color=GOLD, stroke_width=2.5, max_tip_length_to_length_ratio=0.18)
        arrow2 = Arrow(node_bombe.get_right() + RIGHT*0.03, node_keys.get_left() + LEFT*0.03,
                       buff=0.02, color=GOLD, stroke_width=2.5, max_tip_length_to_length_ratio=0.18)

        step2 = TLines(
            r"Une fois les bons r\'eglages trouv\'es,",
            r"les messages du jour deviennent lisibles.",
            font_size=BODY_FONT,
            color=SOFT_BLACK,
            buff=0.16,
        )

        enc = RoundedRectangle(
            corner_radius=0.08, width=3.0, height=0.58,
            fill_color="#EEE7DA", fill_opacity=1, stroke_color=RICE_DARK, stroke_width=1.6
        )
        enc_txt = Tex(r"XJQF\, LPAU\, ...", font_size=22, color=RICE_DARK).move_to(enc.get_center())
        enc_group = VGroup(enc, enc_txt)

        dec = RoundedRectangle(
            corner_radius=0.08, width=3.0, height=0.68,
            fill_color=RICE_LIGHT, fill_opacity=1, stroke_color=AUBERGINE, stroke_width=2
        )
        dec_txt = TLines(
            r"Convoi mardi, secteur nord.",
            r"Sous-marins en position.",
            font_size=16, color=AUBERGINE, buff=0.08
        )
        dec_txt.move_to(dec.get_center())
        dec_group = VGroup(dec, dec_txt)

        down_arrow = Arrow(enc_group.get_bottom()+DOWN*0.02, dec_group.get_top()+UP*0.02,
                           buff=0.04, color=GOLD, stroke_width=2.5, max_tip_length_to_length_ratio=0.18)

        step3 = TLines(
            r"On ne lit pas juste des symboles.",
            r"On lit des ordres, des routes, des positions navales.",
            r"C'est ainsi qu'on anticipe des mouvements ennemis.",
            font_size=BODY_SMALL_FONT,
            color=SOFT_BLACK,
            buff=0.15,
        )

        final = TLines(
            r"Donc : faille logique $\to$ r\'eglages plausibles $\to$ messages lisibles $\to$ renseignement.",
            font_size=BODY_SMALL_FONT,
            color=AUBERGINE,
            buff=0.14,
        )

        full = VGroup(header, step1, flow, step2, enc_group, dec_group, step3, final).arrange(
            DOWN, buff=0.3, aligned_edge=ORIGIN
        )
        full.move_to(ORIGIN + UP*0.08)

        arrow1 = Arrow(node_crib.get_right() + RIGHT*0.03, node_bombe.get_left() + LEFT*0.03,
                       buff=0.02, color=GOLD, stroke_width=2.5, max_tip_length_to_length_ratio=0.18)
        arrow2 = Arrow(node_bombe.get_right() + RIGHT*0.03, node_keys.get_left() + LEFT*0.03,
                       buff=0.02, color=GOLD, stroke_width=2.5, max_tip_length_to_length_ratio=0.18)
        down_arrow = Arrow(enc_group.get_bottom()+DOWN*0.02, dec_group.get_top()+UP*0.02,
                           buff=0.04, color=GOLD, stroke_width=2.5, max_tip_length_to_length_ratio=0.18)

        self.play(Write(header), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in step1], lag_ratio=0.18),
            run_time=1.1,
        )
        self.play(FadeIn(flow, shift=UP*0.08), run_time=0.8)
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), run_time=0.8)
        self.wait(1.2)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in step2], lag_ratio=0.18),
            run_time=1.0,
        )
        self.play(FadeIn(enc_group, shift=UP*0.06), run_time=0.6)
        self.play(GrowArrow(down_arrow), run_time=0.5)
        self.play(FadeIn(dec_group, shift=UP*0.06), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in step3], lag_ratio=0.18),
            run_time=1.2,
        )
        self.play(FadeIn(final, shift=UP*0.06), run_time=0.8)
        self.wait(4.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =============================================================================
# SCÈNE 06 — CONCLUSION
# =============================================================================

class Scene06_Conclusion(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Ce qu'ils ont obtenu")

        lines1 = TLines(
            r"Turing et Bletchley Park n'ont pas seulement trouv\'e une faille.",
            r"Ils ont retrouv\'e, jour apr\`es jour, les r\'eglages d'Enigma.",
            font_size=BODY_FONT,
            color=SOFT_BLACK,
            buff=0.16,
        )

        lines2 = TLines(
            r"Alors les messages allemands redevenaient lisibles :",
            r"ordres navals, routes, positions, d\'eparts de convois, zones d'attaque.",
            font_size=BODY_SMALL_FONT,
            color=AUBERGINE,
            buff=0.16,
        )

        impact_box_text = TLines(
            r"Cons\'equence historique :",
            r"mieux prot\'eger les convois alli\'es,",
            r"traquer les U-boots,",
            r"et acc\'el\'erer la victoire en Europe.",
            font_size=BODY_SMALL_FONT,
            color=SOFT_BLACK,
            buff=0.14,
        )
        impact_box = SurroundingRectangle(
            impact_box_text,
            color=GOLD,
            buff=0.16,
            stroke_width=2,
            fill_color=RICE_LIGHT,
            fill_opacity=0.55,
        )
        impact_full = VGroup(impact_box, impact_box_text)

        final = TLines(
            r"Une contrainte alg\'ebrique,",
            r"puis une machine logique,",
            r"puis du renseignement militaire.",
            font_size=HOOK_FONT,
            color=AUBERGINE,
            buff=0.18,
        )

        cliff = TLines(
            r"Mais Enigma avait encore un autre probl\`eme.",
            r"La cl\'e devait d\'ej\`a \^etre partag\'ee.",
            r"Comment chiffrer pour quelqu'un qu'on n'a jamais rencontr\'e ?",
            font_size=BODY_SMALL_FONT,
            color=SOFT_BLACK,
            buff=0.16,
        )

        ep2 = Tex(r"\textbf{\'Episode 2 : la cl\'e publique}", font_size=24, color=SABLE)
        fit_w(ep2, 0.78)
        ep2_box = SurroundingRectangle(
            ep2,
            color=GOLD,
            buff=0.14,
            stroke_width=2,
            fill_color=AUBERGINE,
            fill_opacity=1,
        )
        ep2_full = VGroup(ep2_box, ep2)

        full = VGroup(header, lines1, lines2, impact_full, final, cliff, ep2_full).arrange(
            DOWN, buff=0.36, aligned_edge=ORIGIN
        )
        full.move_to(ORIGIN)

        self.play(Write(header), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in lines1], lag_ratio=0.18),
            run_time=1.3,
        )
        self.wait(0.9)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in lines2], lag_ratio=0.16),
            run_time=1.2,
        )
        self.wait(0.8)
        self.play(FadeIn(impact_full, shift=UP * 0.08), run_time=0.8)
        self.wait(1.2)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in final], lag_ratio=0.18),
            run_time=1.3,
        )
        self.wait(1.0)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in cliff], lag_ratio=0.18),
            run_time=1.2,
        )
        self.play(FadeIn(ep2_full, scale=1.04), run_time=0.7)
        self.wait(4.3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# =============================================================================
# SCÈNE 06 — CTA
# =============================================================================

class Scene07_CTA(Scene):
    def construct(self):
        self.camera.background_color = SABLE

        # ── Logo rond ────────────────────────────────────────
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

        # ── Texte CTA ────────────────────────────────────────
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

        # ── Animations ───────────────────────────────────────
        self.play(FadeIn(logo, scale=1.1), FadeIn(mask), Create(border), run_time=1)
        self.play(FadeIn(name), run_time=0.8)
        self.play(Create(sep), run_time=0.5)
        self.play(FadeIn(cta, shift=UP * 0.12), run_time=0.6)

        # Pulsation du nom × 3
        for _ in range(3):
            self.play(name.animate.scale(1.03), rate_func=there_and_back, run_time=0.8)

        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

   