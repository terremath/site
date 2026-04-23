from manim import *
import numpy as np

# ═══════════════════════════════════════════
# MÉTADONNÉES (lues par render_all.bat)
# ═══════════════════════════════════════════
SCENES = [
    "Scene01_Titre",
    "Scene00_Legende",
    "Scene00b_Demande",
    "Scene02_Echiquier",
    "Scene03_TotalGrains",
    "Scene04_MasseRiz",
    "Scene05_Comparaison",
    "Scene06_Conclusion",
    "Scene07_CTA",
]
OUTPUT_NAME = "rice_chess_legend.mp4"
OUTPUT_DIR  = r"media\videos\new\1920p30"

# ═══════════════════════════════════════════
# FORMAT PORTRAIT 1080×1920
# ═══════════════════════════════════════════
config.frame_width  = 4.5
config.frame_height = 8.0

# ═══════════════════════════════════════════
# PALETTE
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

# ═══════════════════════════════════════════
# TAILLES DE POLICE
# ═══════════════════════════════════════════
HEADER_FONT       = 30
TITLE_FONT        = 54
SUBTITLE_FONT     = 38
HOOK_FONT         = 34
BODY_FONT         = 20
BODY_SMALL_FONT   = 17
MATH_FONT         = 30
MATH_SMALL_FONT   = 24

# ═══════════════════════════════════════════
# UTILITAIRES COMMUNS
# ═══════════════════════════════════════════
def fit_w(mob, frac=0.82):
    max_w = config.frame_width * frac
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob


def make_header(text):
    """Retourne un VGroup (titre + filet) sans positionnement —
    chaque scène le centre elle-même dans un VGroup global."""
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


# ═══════════════════════════════════════════
# SCENE 00 : LA LÉGENDE
# ═══════════════════════════════════════════
class Scene00_Legende(Scene):
    def construct(self):
        make_bg(self)

        # ── Accroche ──────────────────────────────────────────
        hook = Tex(
            r"\textbf{Il y a tr\`es longtemps\dots}",
            font_size=HOOK_FONT, color=AUBERGINE,
        )
        fit_w(hook, 0.84)

        # ── Le roi ────────────────────────────────────────────
        crown = Tex(r"\textbf{$\bigstar$ Le Roi $\bigstar$}", font_size=BODY_FONT + 4, color=GOLD)
        fit_w(crown, 0.55)
        king_box = RoundedRectangle(
            corner_radius=0.2, width=2.0, height=1.0,
            fill_color=AUBERG_DARK, fill_opacity=1,
            stroke_color=GOLD, stroke_width=2,
        )
        crown.move_to(king_box.get_center())
        king = VGroup(king_box, crown)
        king_lbl = Tex(r"Royaume d'Inde", font_size=BODY_SMALL_FONT, color=SOFT_BLACK)
        king_lbl.next_to(king, DOWN, buff=0.12)
        king_group = VGroup(king, king_lbl)

        # ── Le sage ───────────────────────────────────────────
        sage_icon = Tex(r"\textbf{$\sim$ Le Sage $\sim$}", font_size=BODY_FONT + 4, color=RICE_DARK)
        fit_w(sage_icon, 0.55)
        sage_box = RoundedRectangle(
            corner_radius=0.2, width=2.0, height=1.0,
            fill_color="#3A2A18", fill_opacity=1,
            stroke_color=RICE_DARK, stroke_width=2,
        )
        sage_icon.move_to(sage_box.get_center())
        sage = VGroup(sage_box, sage_icon)
        sage_lbl = Tex(r"Inventeur", font_size=BODY_SMALL_FONT, color=SOFT_BLACK)
        sage_lbl.next_to(sage, DOWN, buff=0.12)
        sage_group = VGroup(sage, sage_lbl)

        # ── Récit ─────────────────────────────────────────────
        bored = Tex(
            r"\textit{S'ennuyait profond\'ement.}",
            font_size=BODY_SMALL_FONT + 1, color=SOFT_BLACK,
        )
        fit_w(bored, 0.82)

        expl_sage = Tex(
            r"Il inventa l'\'echiquier pour divertir le roi.",
            font_size=BODY_FONT, color=SOFT_BLACK,
        )
        fit_w(expl_sage, 0.88)

        expl_reward = Tex(
            r"Le roi, ravi, lui offrit une r\'ecompense.",
            font_size=BODY_FONT, color=SOFT_BLACK,
        )
        fit_w(expl_reward, 0.88)

        teaser = Tex(
            r"\textit{Le sage lui demande\dots\ du riz.}",
            font_size=BODY_FONT, color=GOLD,
        )
        fit_w(teaser, 0.82)

        # ── Centrage global ───────────────────────────────────
        full = VGroup(hook, king_group, bored, sage_group, expl_sage, expl_reward, teaser).arrange(
            DOWN, buff=0.30,
        )
        full.move_to(ORIGIN)

        # ── Animations ────────────────────────────────────────
        self.play(FadeIn(hook, shift=UP * 0.2), run_time=0.9)
        self.wait(1.5)
        self.play(FadeIn(king_group, shift=UP * 0.1), run_time=0.7)
        self.wait(0.8)
        self.play(FadeIn(bored, shift=UP * 0.1), run_time=0.7)
        self.wait(1.5)
        self.play(FadeIn(sage_group, shift=UP * 0.1), run_time=0.7)
        self.wait(0.8)
        self.play(FadeIn(expl_sage, shift=UP * 0.1), run_time=0.7)
        self.wait(1.5)
        self.play(FadeIn(expl_reward, shift=UP * 0.1), run_time=0.7)
        self.wait(1.5)
        self.play(FadeIn(teaser, shift=UP * 0.1), run_time=0.7)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ═══════════════════════════════════════════
# SCENE 00b : LA DEMANDE DU SAGE
# ═══════════════════════════════════════════
class Scene00b_Demande(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("La demande du sage")

        req_lines = TLines(
            r"$\bullet$ 1 grain de riz sur la 1\textsuperscript{re} case,",
            r"$\bullet$ 2 grains sur la 2\textsuperscript{e},",
            r"$\bullet$ 4 grains sur la 3\textsuperscript{e}\dots",
            r"\textit{en doublant chaque case.}",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.18,
        )
        fit_w(req_lines, 0.82)

        reaction = Tex(
            r"\textit{`` Quelle modestie ! Je l'accorde ais\'ement. ''}",
            font_size=BODY_SMALL_FONT, color=GOLD,
        )
        fit_w(reaction, 0.84)

        dash = Line(
            LEFT * config.frame_width * 0.38,
            RIGHT * config.frame_width * 0.38,
            color=GOLD, stroke_width=1,
        )

        punch = Tex(
            r"\textbf{Mais avait-il raison ?}",
            font_size=BODY_FONT + 2, color=AUBERGINE,
        )
        fit_w(punch, 0.84)

        # ── Centrage global ───────────────────────────────────
        full = VGroup(header, req_lines, reaction, dash, punch).arrange(
            DOWN, buff=0.45, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # ── Animations ────────────────────────────────────────
        self.play(Write(header), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in req_lines], lag_ratio=0.18),
            run_time=1.6,
        )
        self.wait(1.6)
        self.play(FadeIn(reaction, shift=UP * 0.1), run_time=0.7)
        self.wait(1.5)
        self.play(Create(dash), run_time=0.3)
        self.play(Write(punch), run_time=0.8)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)


# ═══════════════════════════════════════════
# SCENE 01 : TITRE
# ═══════════════════════════════════════════
class Scene01_Titre(Scene):
    def construct(self):
        make_bg(self)

        title = Tex(
            r"\textbf{Le roi, l'\'echiquier}",
            font_size=TITLE_FONT, color=AUBERGINE,
        )
        fit_w(title, 0.80)

        subtitle = TLines(
            r"et 851 ans de riz",
            font_size=SUBTITLE_FONT, color=GOLD,
        )
        fit_w(subtitle, 0.78)

        sep_w = min(config.frame_width * 0.76,
                    max(title.width, subtitle.width) * 1.06)
        sep = Line(LEFT * sep_w / 2, RIGHT * sep_w / 2,
                   color=GOLD, stroke_width=2)

        author = Tex(r"Terre Math\'ematiques",
                     font_size=32, color=AUBERGINE)
        fit_w(author, 0.70)

        block = VGroup(title, subtitle, sep, author).arrange(
            DOWN, buff=0.45, aligned_edge=ORIGIN,
        )

        hook = TLines(
            r"Une l\'egende c\'el\`ebre\dots",
            r"et un choc exponentiel.",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.15,
        )
        fit_w(hook, 0.82)

        full = VGroup(block, hook).arrange(DOWN, buff=0.8, aligned_edge=ORIGIN)
        full.move_to(ORIGIN)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)
        self.play(Create(sep), FadeIn(author), run_time=0.7)
        self.play(FadeIn(hook, shift=UP * 0.2), run_time=0.8)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 02 : L'ÉCHIQUIER
# ═══════════════════════════════════════════
class Scene02_Echiquier(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("La r\\`egle du doublement")

        # ── échiquier ─────────────────────────────────────────
        sq_size = 0.46
        squares = []
        for row in range(8):
            for col in range(8):
                c = "#C8A060" if (row + col) % 2 == 0 else "#7A4A20"
                sq = Square(
                    side_length=sq_size,
                    fill_opacity=1, fill_color=c,
                    stroke_width=0.5, stroke_color="#3A2010",
                )
                sq.move_to(np.array([
                    (col - 3.5) * sq_size,
                    (3.5 - row) * sq_size,
                    0,
                ]))
                squares.append(sq)
        board = VGroup(*squares)

        last_sq = MathTex(
            r"\text{64}^{\text{e}}\text{ case} = 2^{63}",
            font_size=MATH_SMALL_FONT, color=GOLD,
        )
        fit_w(last_sq, 0.82)

        # ── Centrage global ───────────────────────────────────
        full = VGroup(header, board, last_sq).arrange(
            DOWN, buff=0.85, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # ── Étiquettes (après déplacement du board) ───────────
        values = ["1", "2", "4", "8", "16", "32", "64", "128"]
        labels = VGroup()
        for col, val in enumerate(values):
            lbl = Tex(val, font_size=17, color=SABLE)
            lbl.move_to(board[col].get_center())
            labels.add(lbl)

        # Labels rangées 2-8 (2^8 → 2^62, apparition rapide)
        remaining_rows = []
        for row in range(1, 8):
            row_lbls = VGroup()
            for col in range(8):
                n = row * 8 + col
                lbl = MathTex(r"2^{%d}" % n, font_size=9, color=SABLE)
                lbl.move_to(squares[n].get_center())
                row_lbls.add(lbl)
            remaining_rows.append(row_lbls)

        # Label de la 64e case
        label_64 = MathTex(r"2^{63}", font_size=14, color=SOFT_BLACK)
        label_64.move_to(squares[63].get_center())

        # ── Animations ────────────────────────────────────────
        self.play(Write(header), run_time=0.7)

        # Échiquier complet d'un coup
        self.play(FadeIn(board), run_time=0.7)
        self.wait(0.5)

        # Chiffres un par un sur la première rangée
        for col in range(8):
            self.play(FadeIn(labels[col]), run_time=0.22)
        self.wait(0.3)

        # Rangées 2-8 : apparition rapide rangée par rangée
        for row_lbls in remaining_rows:
            self.play(
                LaggedStart(*[FadeIn(l) for l in row_lbls], lag_ratio=0.05),
                run_time=0.18,
            )
        self.wait(0.4)

        # Label de la 64e case : grossit et descend sous le plateau
        target_64 = np.array([
            board.get_center()[0],
            (board.get_bottom()[1] + last_sq.get_top()[1]) / 2,
            0,
        ])
        self.play(FadeIn(label_64), run_time=0.4)
        self.wait(0.3)
        self.play(
            label_64.animate.scale(5).move_to(target_64),
            run_time=0.7,
        )
        self.wait(1.8)
        self.play(Write(last_sq), run_time=0.8)
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 03 : TOTAL DES GRAINS
# ═══════════════════════════════════════════
class Scene03_TotalGrains(Scene):
    def construct(self):
        make_bg(self)

        header = make_header(r"Le total de grains sur l'\'echiquier")

        sum_formula = MathTex(
            r"1 + 2 + 4 + \cdots + 2^{63}",
            r"= 2^{64} - 1",
            font_size=MATH_FONT, color=SOFT_BLACK,
        )
        fit_w(sum_formula, 0.84)

        approx = MathTex(
            r"2^{64} - 1 \approx 1.84 \times 10^{19}",
            font_size=MATH_FONT, color=AUBERGINE,
        )
        fit_w(approx, 0.84)

        words = TLines(
            r"$\approx$ dix-huit milliards",
            r"de milliards de grains",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.14,
        )

        # ── Centrage global ───────────────────────────────────
        full = VGroup(header, sum_formula, approx, words).arrange(
            DOWN, buff=0.65, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        box = SurroundingRectangle(
            approx, color=GOLD, buff=0.18, stroke_width=2,
            fill_color=RICE_LIGHT, fill_opacity=0.4,
        )

        # ── Animations ────────────────────────────────────────
        self.play(Write(header), run_time=0.7)
        self.play(Write(sum_formula[0]), run_time=1.0)
        self.play(Write(sum_formula[1]), run_time=0.8)
        self.wait(3)
        self.play(Write(approx), run_time=0.8)
        self.play(Create(box), run_time=0.5)
        self.wait(3)
        self.play(FadeIn(words, shift=UP * 0.2), run_time=0.7)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 04 : PASSAGE À LA MASSE RÉELLE
# ═══════════════════════════════════════════
class Scene04_MasseRiz(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Passage au monde r\\'{e}el")

        # ── rangée grain → masse ──────────────────────────────
        grain_dot = Ellipse(
            width=0.28, height=0.16,
            fill_color=RICE_DARK, fill_opacity=1, stroke_width=0,
        )
        grain_lbl = Tex(r"1 grain", font_size=BODY_SMALL_FONT, color=SOFT_BLACK)
        grain_lbl.next_to(grain_dot, DOWN, buff=0.1)
        grain = VGroup(grain_dot, grain_lbl)

        mass_grain = MathTex(
            r"\approx 25\ \text{mg}",
            font_size=MATH_FONT, color=AUBERGINE,
        )
        top_row = VGroup(grain, mass_grain).arrange(RIGHT, buff=0.8)

        # ── reste du contenu ──────────────────────────────────
        sep = Line(
            LEFT * config.frame_width * 0.38,
            RIGHT * config.frame_width * 0.38,
            color=GOLD, stroke_width=1.5,
        )
        calc = MathTex(
            r"(2^{64}-1)\times 25\ \text{mg}",
            font_size=MATH_SMALL_FONT, color=SOFT_BLACK,
        )
        fit_w(calc, 0.84)

        result = MathTex(
            r"\approx 4.61 \times 10^{11}\ \text{tonnes}",
            font_size=MATH_FONT, color=AUBERGINE,
        )
        fit_w(result, 0.84)

        words = TLines(
            r"$\approx$ 461 milliards de tonnes",
            font_size=BODY_FONT, color=SOFT_BLACK,
        )

        # ── Centrage global ───────────────────────────────────
        full = VGroup(header, top_row, sep, calc, result, words).arrange(
            DOWN, buff=0.45, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Flèche et box après positionnement
        arrow = Arrow(
            grain.get_right() + RIGHT * 0.05,
            mass_grain.get_left() + LEFT * 0.05,
            buff=0.05, color=GOLD, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.18,
        )
        result_box = SurroundingRectangle(
            result, color=GOLD, buff=0.16, stroke_width=2,
            fill_color=RICE_LIGHT, fill_opacity=0.45,
        )

        # ── Animations ────────────────────────────────────────
        self.play(Write(header), run_time=0.7)
        self.play(FadeIn(grain), run_time=0.6)
        self.play(GrowArrow(arrow), Write(mass_grain), run_time=0.8)
        self.wait(1.3)
        self.play(Create(sep), run_time=0.4)
        self.play(Write(calc), run_time=0.9)
        self.play(Write(result), Create(result_box), run_time=0.9)
        self.wait(3)
        self.play(FadeIn(words, shift=UP * 0.15), run_time=0.7)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 05 : COMPARAISON USDA
# ═══════════════════════════════════════════
class Scene05_Comparaison(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Comparaison mondiale")

        # ── bloc gauche ───────────────────────────────────────
        label_left = Tex(r"\textbf{\'Echiquier}", font_size=BODY_FONT, color=AUBERGINE)
        val_left   = MathTex(r"4.61 \times 10^{11}\ \text{t}", font_size=MATH_SMALL_FONT, color=AUBERGINE)
        fit_w(val_left, 0.40)
        col_left = VGroup(label_left, val_left).arrange(DOWN, buff=0.16)

        # ── bloc droit ────────────────────────────────────────
        label_right = Tex(r"\textbf{Monde / an}", font_size=BODY_FONT, color=BLUE_OK)
        val_right   = MathTex(r"541.9 \times 10^{6}\ \text{t}", font_size=MATH_SMALL_FONT, color=BLUE_OK)
        fit_w(val_right, 0.40)
        col_right = VGroup(label_right, val_right).arrange(DOWN, buff=0.16)

        vs  = Tex(r"\textbf{vs}", font_size=BODY_FONT, color=GOLD)
        row = VGroup(col_left, vs, col_right).arrange(RIGHT, buff=0.35, aligned_edge=ORIGIN)
        fit_w(row, 0.88)

        source = Tex(r"Source : USDA 2025/26", font_size=BODY_SMALL_FONT, color=SOFT_BLACK)

        sep = Line(
            LEFT * config.frame_width * 0.38,
            RIGHT * config.frame_width * 0.38,
            color=GOLD, stroke_width=1.5,
        )

        div = MathTex(
            r"\frac{4.61\times 10^{11}}{541.9\times 10^{6}}",
            font_size=MATH_FONT, color=SOFT_BLACK,
        )
        fit_w(div, 0.50)

        equals = MathTex(r"\approx\ 851", font_size=MATH_FONT + 8, color=AUBERGINE)
        fit_w(equals, 0.60)

        verdict = TLines(
            r"La quantit\'e totale de l'\'echiquier",
            r"suffit pour nourrir la plan\`ete",
            r"pendant \textbf{851 ans}",
            font_size=BODY_FONT, color=SOFT_BLACK, buff=0.14,
        )

        joke = Tex(
            r"Le sage nourrit encore sa famille aujourd'hui.",
            font_size=BODY_FONT + 5, color=AUBERGINE,
        )
        fit_w(joke, 0.82)

        # ── Centrage global ───────────────────────────────────
        full = VGroup(header, row, source, sep, div, equals, verdict).arrange(
            DOWN, buff=0.35, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        joke.next_to(verdict, DOWN, buff=0.60)

        box = SurroundingRectangle(
            verdict, color=GOLD, buff=0.16, stroke_width=2,
            fill_color=RICE_LIGHT, fill_opacity=0.45,
        )
        joke_box = SurroundingRectangle(
            joke, color=AUBERGINE, buff=0.20, stroke_width=2,
            fill_color=RICE_LIGHT, fill_opacity=0.35,
        )

        # ── Animations ────────────────────────────────────────
        self.play(Write(header), run_time=0.7)
        self.play(FadeIn(row, shift=UP * 0.2), run_time=0.9)
        self.wait(3.0)
        self.play(FadeIn(source), run_time=0.5)
        self.wait(1.5)
        self.play(Create(sep), run_time=0.4)
        self.play(Write(div), run_time=0.9)
        self.play(Write(equals), run_time=0.7)
        self.wait(2.8)
        self.play(FadeIn(verdict), Create(box), run_time=0.7)
        self.wait(2.5)
        self.play(FadeIn(joke, shift=UP * 0.1), Create(joke_box), run_time=0.7)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ═══════════════════════════════════════════
# SCENE 06 : CONCLUSION — L'EXPONENTIELLE
# ═══════════════════════════════════════════
class Scene06_Conclusion(Scene):
    def construct(self):
        make_bg(self)

        header = make_header("Ce que le roi n'avait pas prévu")

        line1 = Tex(
            r"\textbf{Le probl\`eme n'est pas le riz.}",
            font_size=BODY_FONT + 2, color=SOFT_BLACK,
        )
        fit_w(line1, 0.84)

        line2 = Tex(
            r"\textbf{C'est le ph\'enom\`ene} \\ \textbf{exponentiel.}",
            font_size=HOOK_FONT + 6, color=AUBERGINE,
        )
        fit_w(line2, 0.72)

        text_block = VGroup(line1, line2).arrange(DOWN, buff=0.28)

        conclu = TLines(
            r"\`A chaque \'etape, la valeur \textbf{double}.",
            r"Ce qui para\^it anodin devient \textbf{colossal}.",
            font_size=BODY_SMALL_FONT + 1, color=SOFT_BLACK, buff=0.15,
        )
        fit_w(conclu, 0.82)

        # ── Axes ──────────────────────────────────────────────
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 130, 32],
            x_length=3.6,
            y_length=2.8,
            tips=False,
            axis_config={"color": SOFT_BLACK, "stroke_width": 1.5},
        )

        # ── Centrage global ───────────────────────────────────
        full = VGroup(header, text_block, conclu, axes).arrange(
            DOWN, buff=0.45, aligned_edge=ORIGIN,
        )
        full.move_to(ORIGIN)

        # Courbes et labels APRÈS déplacement des axes
        lin  = axes.plot(lambda x: 5 * x,  x_range=[0, 7], color=BLUE_OK,  stroke_width=2.5)
        quad = axes.plot(lambda x: x ** 2,  x_range=[0, 7], color=GREEN_OK, stroke_width=2.5)
        expo = axes.plot(lambda x: 2 ** x,  x_range=[0, 7], color=RED_WARN, stroke_width=2.5)

        lbl_lin  = Tex(r"lin\'eaire",    font_size=14, color=BLUE_OK)
        lbl_quad = Tex(r"quadratique",   font_size=14, color=GREEN_OK)
        lbl_expo = Tex(r"exponentielle", font_size=14, color=RED_WARN)

        lbl_lin.next_to(axes.c2p(7, 35), UP,   buff=0.10)
        lbl_quad.next_to(axes.c2p(7, 49), UP,  buff=0.10)
        lbl_expo.next_to(axes.c2p(5.8, 56), LEFT, buff=0.12)

        box2 = SurroundingRectangle(line2, color=GOLD, buff=0.14, stroke_width=2.5)

        # ── Animations ────────────────────────────────────────
        self.play(Write(header), run_time=0.7)
        self.play(Write(line1), run_time=0.8)
        self.play(Write(line2), run_time=0.8)
        self.play(Create(box2), run_time=0.5)
        self.wait(1.8)
        self.play(Create(axes), run_time=0.6)
        self.play(Create(lin),  FadeIn(lbl_lin),  run_time=0.8)
        self.play(Create(quad), FadeIn(lbl_quad), run_time=0.8)
        self.play(Create(expo), FadeIn(lbl_expo), run_time=0.8)
        self.wait(2.5)
        self.play(FadeIn(conclu, shift=UP * 0.1), run_time=0.8)
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ═══════════════════════════════════════════
# SCENE 07 : CTA + LOGO
# ═══════════════════════════════════════════
class Scene07_CTA(Scene):
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

        self.play(FadeIn(logo, scale=1.1), FadeIn(mask), Create(border), run_time=1)
        self.play(FadeIn(name), run_time=0.8)
        self.play(Create(sep), run_time=0.5)
        self.play(FadeIn(cta, shift=UP * 0.12), run_time=0.6)

        for _ in range(3):
            self.play(name.animate.scale(1.03), rate_func=there_and_back, run_time=0.8)

        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
