from manim import *
import numpy as np

# ─── Palette TerreMathématiques ───────────────────────────────────────────────
AUBERGINE   = "#4A235A"
GOLD        = "#BF953F"
SAND        = "#F2E6CB"
SLATE       = "#32323C"
WHITE       = "#FFFFFF"
RED_WRONG   = "#8B1A1A"
GREEN_RIGHT = "#1A5C2E"

# ─── Config TikTok vertical ───────────────────────────────────────────────────
config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60


class QCMTikTok(Scene):
    """
    Scénario 5 — Animation TikTok QCM TerreMathématiques
    Durée cible : ~18 secondes
    Structure :
      0–2s   Accroche logo + tagline
      2–6s   La question apparaît
      6–10s  Les 4 choix défilent
      10–14s Le curseur hésite → choisit le mauvais → rouge
      14–17s Flash + texte "Et toi ?"
      17–18s CTA lien en bio
    """

    def construct(self):
        self.camera.background_color = AUBERGINE

        # ── 1. ACCROCHE LOGO ──────────────────────────────────────────────────
        logo_text = Text(
            "TerreMathématiques",
            font="Palatino",
            color=GOLD,
            font_size=52,
            weight=BOLD,
        )
        logo_sub = Text(
            "La pensée en mouvement.",
            font="Palatino",
            color=SAND,
            font_size=28,
            slant=ITALIC,
        )
        logo_group = VGroup(logo_text, logo_sub).arrange(DOWN, buff=0.25)
        logo_group.move_to(UP * 3.5)

        # Ligne décorative dorée
        deco_line = Line(LEFT * 2.5, RIGHT * 2.5, color=GOLD, stroke_width=1.5)
        deco_line.next_to(logo_group, DOWN, buff=0.2)

        self.play(
            FadeIn(logo_text, shift=DOWN * 0.3),
            run_time=0.8,
        )
        self.play(
            FadeIn(logo_sub, shift=DOWN * 0.2),
            GrowFromCenter(deco_line),
            run_time=0.7,
        )
        self.wait(0.5)

        # ── 2. LA QUESTION ────────────────────────────────────────────────────
        question_label = Text(
            "Question 7 / 21",
            font="Palatino",
            color=GOLD,
            font_size=32,
            slant=ITALIC,
        )
        question_label.move_to(UP * 1.8)

        question_line1 = Text(
            "Une balle tombe d'un train",
            font="Palatino",
            color=SAND,
            font_size=40,
        )
        question_line2 = Text(
            "en mouvement.",
            font="Palatino",
            color=SAND,
            font_size=40,
        )
        question_line3 = Text(
            "Que voit le voyageur ?",
            font="Palatino",
            color=WHITE,
            font_size=42,
            weight=BOLD,
        )
        question_block = VGroup(
            question_line1, question_line2, question_line3
        ).arrange(DOWN, buff=0.18)
        question_block.move_to(UP * 0.6)

        self.play(
            FadeIn(question_label, shift=LEFT * 0.3),
            run_time=0.5,
        )
        self.play(
            Write(question_line1),
            Write(question_line2),
            run_time=1.0,
        )
        self.play(
            Write(question_line3),
            run_time=0.8,
        )
        self.wait(0.4)

        # ── 3. LES 4 CHOIX ───────────────────────────────────────────────────
        choices = [
            ("A", "Une droite verticale"),
            ("B", "Une parabole"),          # ← bonne réponse
            ("C", "Une droite oblique"),
            ("D", "Un arc de cercle"),
        ]

        choice_mobs = []
        choice_boxes = []

        start_y = -1.1
        for i, (letter, text_str) in enumerate(choices):
            box = RoundedRectangle(
                width=8.5,
                height=0.85,
                corner_radius=0.12,
                color=GOLD,
                fill_color=SLATE,
                fill_opacity=0.85,
                stroke_width=1.5,
            )
            box.move_to(UP * (start_y - i * 1.05))

            letter_mob = Text(
                letter,
                font="Palatino",
                color=GOLD,
                font_size=36,
                weight=BOLD,
            )
            letter_mob.move_to(box.get_left() + RIGHT * 0.6)

            choice_mob = Text(
                text_str,
                font="Palatino",
                color=SAND,
                font_size=32,
            )
            choice_mob.move_to(box.get_center() + RIGHT * 0.5)

            choice_boxes.append(box)
            choice_mobs.append(VGroup(box, letter_mob, choice_mob))

        for mob in choice_mobs:
            self.play(FadeIn(mob, shift=RIGHT * 0.3), run_time=0.35)

        self.wait(0.5)

        # ── 4. LE CURSEUR HÉSITE ─────────────────────────────────────────────
        # Curseur = petit triangle pointant vers la droite
        cursor = Triangle(color=WHITE, fill_color=WHITE, fill_opacity=1)
        cursor.scale(0.18)
        cursor.rotate(-PI / 2)

        # Part du choix A
        cursor.move_to(choice_boxes[0].get_left() + LEFT * 0.3)
        self.play(FadeIn(cursor), run_time=0.3)

        # Hésite : A → C → A → D → C  (faux mouvement)
        hesitation_targets = [2, 0, 3, 2]
        for idx in hesitation_targets:
            target_pos = choice_boxes[idx].get_left() + LEFT * 0.3
            self.play(cursor.animate.move_to(target_pos), run_time=0.35)

        # Clique sur C (mauvais choix)
        wrong_idx = 2
        target_pos = choice_boxes[wrong_idx].get_left() + LEFT * 0.3
        self.play(cursor.animate.move_to(target_pos), run_time=0.25)

        # Flash de sélection → fond rouge sur la mauvaise réponse
        wrong_box = choice_boxes[wrong_idx]
        self.play(
            wrong_box.animate.set_fill(RED_WRONG, opacity=1.0),
            wrong_box.animate.set_stroke(color="#FF4444", width=3),
            Flash(wrong_box.get_center(), color="#FF4444", line_length=0.25, num_lines=8),
            run_time=0.5,
        )

        # Croix animée sur le mauvais choix
        cross = Cross(wrong_box, color="#FF4444", stroke_width=4)
        self.play(Create(cross), run_time=0.4)
        self.wait(0.3)

        # ── 5. "ET TOI ?" ─────────────────────────────────────────────────────
        # Tout disparaît sauf le fond
        everything = VGroup(
            logo_group, deco_line,
            question_label, question_block,
            *choice_mobs, cursor, cross,
        )
        self.play(FadeOut(everything), run_time=0.5)

        # Fond flash blanc puis retour aubergine
        flash_rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        )
        self.play(FadeIn(flash_rect), run_time=0.15)
        self.play(FadeOut(flash_rect), run_time=0.2)

        # Grand texte centré
        et_toi = Text(
            "Et toi ?",
            font="Palatino",
            color=GOLD,
            font_size=130,
            weight=BOLD,
        )
        et_toi.move_to(UP * 1.5)

        sous_toi = Text(
            "21 questions.\nAucune formule à réciter.",
            font="Palatino",
            color=SAND,
            font_size=42,
            line_spacing=1.3,
        )
        sous_toi.move_to(DOWN * 0.3)

        self.play(
            Write(et_toi),
            run_time=0.7,
        )
        self.play(
            FadeIn(sous_toi, shift=UP * 0.2),
            run_time=0.6,
        )
        self.wait(0.5)

        # ── 6. CTA ────────────────────────────────────────────────────────────
        cta_box = RoundedRectangle(
            width=7.5,
            height=1.0,
            corner_radius=0.2,
            fill_color=GOLD,
            fill_opacity=1,
            stroke_width=0,
        )
        cta_box.move_to(DOWN * 2.4)

        cta_text = Text(
            "Lien en bio → Gratuit",
            font="Palatino",
            color=AUBERGINE,
            font_size=40,
            weight=BOLD,
        )
        cta_text.move_to(cta_box.get_center())

        self.play(
            GrowFromCenter(cta_box),
            run_time=0.4,
        )
        self.play(
            FadeIn(cta_text),
            run_time=0.3,
        )

        # Pulsation finale du CTA
        self.play(
            cta_box.animate.scale(1.04),
            run_time=0.25,
        )
        self.play(
            cta_box.animate.scale(1 / 1.04),
            cta_text.animate.scale(1 / 1.04),
            run_time=0.25,
        )
        self.wait(0.8)


# ─── Commande de rendu ────────────────────────────────────────────────────────
# manim -pqh qcm_tiktok.py QCMTikTok -r 1080,1920
