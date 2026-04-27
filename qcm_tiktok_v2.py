from manim import *
import numpy as np

# ─── Palette TerreMathématiques ───────────────────────────────────────────────
AUBERGINE  = "#4A235A"
GOLD       = "#BF953F"
SAND       = "#F2E6CB"
SLATE      = "#32323C"
NOIR       = "#0A0A0A"
BLANC      = "#F5F0E8"   # blanc cassé chaud, pas pur
ROUGE      = "#6B1515"

# ─── Config TikTok vertical ───────────────────────────────────────────────────
config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60
config.background_color = NOIR

# ─────────────────────────────────────────────────────────────────────────────
# SCÈNE 1 — Ouverture choc : fond noir, une seule ligne blanche qui coupe
# Durée : ~2s
# ─────────────────────────────────────────────────────────────────────────────
class Scene1_Ouverture(Scene):
    def construct(self):
        self.camera.background_color = NOIR

        # "QCM" en très grand — remplissage blanc sur noir
        qcm_label = Text(
            "QCM",
            font="Palatino",
            color=BLANC,
            font_size=260,
            weight=BOLD,
        )
        qcm_label.move_to(UP * 1.2)

        # Sous-titre éditorial
        sub = Text(
            "Test de raisonnement",
            font="Palatino",
            color=GOLD,
            font_size=38,
            slant=ITALIC,
        )
        sub.next_to(qcm_label, DOWN, buff=0.1)

        # Séquence : tout arrive en cut (pas de fade, instantané ou presque)
        self.play(
            Write(qcm_label),
            run_time=0.4,
            rate_func=linear,
        )
        self.play(
            FadeIn(sub, shift=UP * 0.1),
            run_time=0.3,
        )
        self.wait(0.8)

        # Sortie : la ligne remonte et efface tout
        self.play(
            FadeOut(qcm_label),
            FadeOut(sub),
            run_time=0.4,
            rate_func=rush_into,
        )


# ─────────────────────────────────────────────────────────────────────────────
# SCÈNE 2 — La question : fond BLANC CASSÉ, texte noir monumental
# Durée : ~3.5s
# ─────────────────────────────────────────────────────────────────────────────
class Scene2_Question(Scene):
    def construct(self):
        self.camera.background_color = BLANC

        # Bande aubergine en haut — style en-tête journal
        header = Rectangle(
            width=config.frame_width + 1,
            height=1.4,
            fill_color=AUBERGINE,
            fill_opacity=1,
            stroke_width=0,
        )
        header.to_edge(UP, buff=0)

        brand = Text(
            "TERRE MATHÉMATIQUES",
            font="Palatino",
            color=GOLD,
            font_size=30,
            weight=BOLD,
        )
        brand.move_to(header.get_center())

        # Question — énorme, noir sur blanc, sans chichis
        q1 = Text(
            "Une balle tombe",
            font="Palatino",
            color=NOIR,
            font_size=88,
            weight=BOLD,
        )
        q2 = Text(
            "d'un train",
            font="Palatino",
            color=NOIR,
            font_size=88,
            weight=BOLD,
        )
        q3 = Text(
            "en mouvement.",
            font="Palatino",
            color=NOIR,
            font_size=88,
            weight=BOLD,
        )

        q_group = VGroup(q1, q2, q3).arrange(DOWN, buff=3.15, aligned_edge=LEFT)
        q_group.move_to(UP * 1.8)
        q_group.to_edge(LEFT, buff=0.45)

        # Ligne fine dorée sous la question
        sep = Line(
            LEFT * 0.5, RIGHT * 4.5,
            color=GOLD,
            stroke_width=2,
        )
        sep.next_to(q_group, DOWN, buff=1.35)
        sep.to_edge(LEFT, buff=0.45)

        # Sous-question — petit, italique, couleur slate
        sous_q = Text(
            "Que voit le voyageur à bord ?",
            font="Palatino",
            color=SLATE,
            font_size=44,
            slant=ITALIC,
        )
        sous_q.next_to(sep, DOWN, buff=3.3)
        sous_q.to_edge(LEFT, buff=0.45)

        # Numéro flottant en bas à droite — style magazine
        num_deco = Text(
            "07 / 21",
            font="Palatino",
            color=AUBERGINE,
            font_size=100,
            weight=BOLD,
        )
        num_deco.to_corner(DR, buff=0.4)

        # --- Animation : tout en cut rapide ---
        self.add(header, brand)
        self.wait(0.05)

        # La question arrive ligne par ligne avec de tout petits décalages
        self.play(FadeIn(q1, shift=UP * 0.08), run_time=0.2)
        self.play(FadeIn(q2, shift=UP * 0.08), run_time=0.2)
        self.play(FadeIn(q3, shift=UP * 0.08), run_time=0.2)

        self.play(
            GrowFromPoint(sep, sep.get_left()),
            run_time=0.4,
        )
        self.play(
            FadeIn(sous_q, shift=UP * 0.1),
            FadeIn(num_deco, shift=LEFT * 0.1),
            run_time=0.3,
        )
        self.wait(1.5)

        # Sortie brutale
        self.play(
            *[FadeOut(m) for m in [q_group, sep, sous_q, num_deco, header, brand]],
            run_time=0.25,
        )


# ─────────────────────────────────────────────────────────────────────────────
# SCÈNE 3 — Les choix : style bulletin, noir/blanc, lettre en or
# Durée : ~3s
# ─────────────────────────────────────────────────────────────────────────────
class Scene3_Choix(Scene):
    def construct(self):
        self.camera.background_color = BLANC

        # Header identique
        header = Rectangle(
            width=config.frame_width + 1,
            height=1.1,
            fill_color=AUBERGINE,
            fill_opacity=1,
            stroke_width=0,
        )
        header.to_edge(UP, buff=0)
        brand = Text(
            "TERREMATHÉMATIQUES",
            font="Palatino",
            color=GOLD,
            font_size=28,
            weight=BOLD,
        )
        brand.move_to(header.get_center())
        self.add(header, brand)

        choices = [
            ("A", "Une droite verticale"),
            ("B", "Une parabole"),
            ("C", "Une droite oblique"),
            ("D", "Un arc de cercle"),
        ]

        mobs = []
        start_y = 2.6
        for i, (letter, txt) in enumerate(choices):
            y = start_y - i * 1.55

            # Ligne séparatrice fine
            sep = Line(
                LEFT * 3.8, RIGHT * 3.8,
                stroke_width=0.8,
                color=SLATE,
            )
            sep.move_to(UP * (y + 0.68))

            # Lettre monumentale en or
            letter_mob = Text(
                letter,
                font="Palatino",
                color=GOLD,
                font_size=80,
                weight=BOLD,
            )
            letter_mob.move_to(LEFT * 3.2 + UP * y)

            # Texte du choix
            choice_mob = Text(
                txt,
                font="Palatino",
                color=NOIR,
                font_size=50,
                weight=BOLD,
            )
            choice_mob.move_to(RIGHT * 0.6 + UP * y)

            mobs.append(VGroup(sep, letter_mob, choice_mob))

        # Chaque choix arrive en cut depuis la droite
        for mob in mobs:
            self.play(
                FadeIn(mob, shift=LEFT * 0.3),
                run_time=1.25,
            )
            self.wait(1.05)

        self.wait(1.0)

        # Sortie
        self.play(
            *[FadeOut(m) for m in mobs],
            FadeOut(header), FadeOut(brand),
            run_time=1.25,
        )


# ─────────────────────────────────────────────────────────────────────────────
# SCÈNE 4 — Le mauvais choix sélectionné : fond qui vire rouge foncé
# Durée : ~2.5s
# ─────────────────────────────────────────────────────────────────────────────
class Scene4_ErreurChoc(Scene):
    def construct(self):
        self.camera.background_color = BLANC

        # Rappel de la question compact
        q_rappel = Text(
            "Que voit le voyageur ?",
            font="Palatino",
            color=SLATE,
            font_size=36,
            slant=ITALIC,
        )
        q_rappel.move_to(UP * 3.8)

        # Choix C mis en évidence — style "sélectionné"
        # Rectangle plein rouge foncé
        wrong_bg = Rectangle(
            width=8.8,
            height=1.35,
            fill_color=ROUGE,
            fill_opacity=1,
            stroke_width=0,
        )
        wrong_bg.move_to(UP * 0.3)

        letter_wrong = Text(
            "C",
            font="Palatino",
            color=BLANC,
            font_size=90,
            weight=BOLD,
        )
        letter_wrong.move_to(wrong_bg.get_left() + RIGHT * 1.0)

        text_wrong = Text(
            "Une droite oblique",
            font="Palatino",
            color=BLANC,
            font_size=52,
            weight=BOLD,
        )
        text_wrong.move_to(wrong_bg.get_center() + RIGHT * 0.8)

        # Croix — pas animée, instantanée, brutale
        cross_v = Line(UP * 0.4, DOWN * 0.4, color=BLANC, stroke_width=6)
        cross_h = Line(LEFT * 0.4, RIGHT * 0.4, color=BLANC, stroke_width=6)
        cross_v.move_to(wrong_bg.get_right() + LEFT * 0.7)
        cross_h.move_to(wrong_bg.get_right() + LEFT * 0.7)
        cross_v.rotate(PI / 4)
        cross_h.rotate(PI / 4)

        # Texte "FAUX" en grand — sobre
        faux_text = Text(
            "FAUX.",
            font="Palatino",
            color=ROUGE,
            font_size=200,
            weight=BOLD,
        )
        faux_text.move_to(DOWN * 2.0)

        # Ligne fine blanche sous "FAUX"
        faux_line = Line(LEFT * 2.5, RIGHT * 2.5, color=ROUGE, stroke_width=2)
        faux_line.next_to(faux_text, DOWN, buff=0.2)

        self.play(FadeIn(q_rappel), run_time=0.2)
        self.wait(0.1)

        # Le bloc rouge arrive en cut
        self.play(
            FadeIn(wrong_bg),
            FadeIn(letter_wrong),
            FadeIn(text_wrong),
            run_time=0.15,
        )
        self.play(
            Create(cross_v),
            Create(cross_h),
            run_time=0.2,
        )

        # "FAUX" frappe
        self.play(
            Write(faux_text),
            GrowFromCenter(faux_line),
            run_time=0.35,
        )
        self.wait(1.2)

        self.play(
            *[FadeOut(m) for m in [
                q_rappel, wrong_bg, letter_wrong, text_wrong,
                cross_v, cross_h, faux_text, faux_line
            ]],
            run_time=0.2,
        )


# ─────────────────────────────────────────────────────────────────────────────
# SCÈNE 5 — "Et toi ?" : fond noir, or, typographie monumentale
# Durée : ~3s
# ─────────────────────────────────────────────────────────────────────────────
class Scene5_EtToi(Scene):
    def construct(self):
        self.camera.background_color = NOIR

        # Ligne décorative fine en or — arrive en premier
        ligne_top = Line(LEFT * 3.5, RIGHT * 3.5, color=GOLD, stroke_width=1.5)
        ligne_top.move_to(UP * 0.8)

        # "ET TOI ?" — blanc sur noir, massif
        et_toi = Text(
            "ET TOI ?",
            font="Palatino",
            color=BLANC,
            font_size=170,
            weight=BOLD,
        )
        et_toi.move_to(DOWN * 0.3)

        ligne_bot = Line(LEFT * 3.5, RIGHT * 3.5, color=GOLD, stroke_width=1.5)
        ligne_bot.move_to(DOWN * 1.5)

        # Sous-ligne — sobre, italic, or
        sous = Text(
            "21 questions. Aucune formule.",
            font="Palatino",
            color=GOLD,
            font_size=38,
            slant=ITALIC,
        )
        sous.move_to(DOWN * 2.2)

        self.play(
            GrowFromCenter(ligne_top),
            GrowFromCenter(ligne_bot),
            run_time=0.3,
        )
        self.play(
            Write(et_toi),
            run_time=0.4,
        )
        self.play(
            FadeIn(sous, shift=UP * 0.1),
            run_time=0.3,
        )
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(ligne_top, ligne_bot, et_toi, sous)),
            run_time=0.2,
        )


# ─────────────────────────────────────────────────────────────────────────────
# SCÈNE 6 — CTA : fond aubergine, bouton or, minimaliste
# Durée : ~2s
# ─────────────────────────────────────────────────────────────────────────────
class Scene6_CTA(Scene):
    def construct(self):
        self.camera.background_color = AUBERGINE

        brand = Text(
            "TerreMathématiques",
            font="Palatino",
            color=GOLD,
            font_size=44,
            weight=BOLD,
        )
        brand.move_to(UP * 3.5)

        tag = Text(
            "La pensée en mouvement.",
            font="Palatino",
            color=SAND,
            font_size=30,
            slant=ITALIC,
        )
        tag.next_to(brand, DOWN, buff=0.15)

        sep = Line(LEFT * 2.5, RIGHT * 2.5, color=GOLD, stroke_width=1)
        sep.next_to(tag, DOWN, buff=0.3)

        # Bouton CTA — rectangle plein blanc cassé
        btn = Rectangle(
            width=7.8,
            height=1.3,
            fill_color=BLANC,
            fill_opacity=1,
            stroke_width=0,
        )
        btn.move_to(DOWN * 0.5)

        btn_text = Text(
            "Teste-toi → Lien en bio",
            font="Palatino",
            color=AUBERGINE,
            font_size=44,
            weight=BOLD,
        )
        btn_text.move_to(btn.get_center())

        # Gratuit badge
        gratuit = Text(
            "100 % GRATUIT",
            font="Palatino",
            color=GOLD,
            font_size=34,
            weight=BOLD,
        )
        gratuit.next_to(btn, DOWN, buff=0.45)

        self.play(
            FadeIn(brand),
            FadeIn(tag),
            GrowFromCenter(sep),
            run_time=0.4,
        )
        self.play(
            GrowFromCenter(btn),
            run_time=0.3,
        )
        self.play(
            FadeIn(btn_text),
            run_time=0.2,
        )
        self.play(
            FadeIn(gratuit, shift=UP * 0.1),
            run_time=0.25,
        )

        # Pulsation subtile du bouton
        self.play(btn.animate.scale(1.03), btn_text.animate.scale(1.03), run_time=0.2)
        self.play(btn.animate.scale(1/1.03), btn_text.animate.scale(1/1.03), run_time=0.2)

        self.wait(1.0)


# ─────────────────────────────────────────────────────────────────────────────
# SCÈNE MAÎTRESSE — Enchaîne tout avec des cuts nets (pas de fade entre scènes)
# C'est cette scène qu'on rend pour l'export final.
# ─────────────────────────────────────────────────────────────────────────────
class QCMEditorial(Scene):
    """
    Rendu final complet.
    Commande :
        manim -pqh qcm_tiktok_v2.py QCMEditorial -r 1080,1920
    """

    def construct(self):

        # ── helpers ──────────────────────────────────────────────────────────
        def clear(run_time=0.18):
            self.play(
                *[FadeOut(m, run_time=run_time) for m in self.mobjects],
            )

        def header_bar():
            bar = Rectangle(
                width=config.frame_width + 1,
                height=1.1,
                fill_color=AUBERGINE,
                fill_opacity=1,
                stroke_width=0,
            )
            bar.to_edge(UP, buff=0)
            brand = Text(
                "TERREMATHÉMATIQUES",
                font="Palatino",
                color=GOLD,
                font_size=28,
                weight=BOLD,
            )
            brand.move_to(bar.get_center())
            return VGroup(bar, brand)

        # ════════════════════════════════════════════════════════════════════
        # BEAT 1 — Accroche choc  (fond noir)
        # ════════════════════════════════════════════════════════════════════
        self.camera.background_color = NOIR

        ligne = Line(
            LEFT * config.frame_width, RIGHT * config.frame_width,
            color=BLANC, stroke_width=1,
        ).move_to(ORIGIN)

        qcm_label = Text("QCM", font="Palatino", color=BLANC,
                         font_size=260, weight=BOLD).move_to(UP * 1.2)
        sub = Text("Test de raisonnement", font="Palatino", color=GOLD,
                   font_size=38, slant=ITALIC).next_to(qcm_label, DOWN, buff=0.1)
        num = Text("N° 07", font="Palatino", color=GOLD, font_size=28)
        num.to_corner(UL, buff=0.5)

        self.add(ligne)
        self.play(Write(qcm_label), run_time=0.35, rate_func=linear)
        self.play(FadeIn(sub, shift=UP * 0.08), FadeIn(num), run_time=0.25)
        self.wait(0.9)
        clear()

        # ════════════════════════════════════════════════════════════════════
        # BEAT 2 — La question  (fond blanc cassé)
        # ════════════════════════════════════════════════════════════════════
        self.camera.background_color = BLANC

        hbar = header_bar()
        self.add(hbar)

        q1 = Text("Une balle tombe", font="Palatino",
                  color=NOIR, font_size=88, weight=BOLD)
        q2 = Text("d'un train", font="Palatino",
                  color=NOIR, font_size=88, weight=BOLD)
        q3 = Text("en mouvement.", font="Palatino",
                  color=NOIR, font_size=88, weight=BOLD)
        q_group = VGroup(q1, q2, q3).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        q_group.move_to(UP * 0.9).to_edge(LEFT, buff=0.45)

        sep_q = Line(LEFT * 0.5, RIGHT * 4.5, color=GOLD, stroke_width=2)
        sep_q.next_to(q_group, DOWN, buff=0.3).to_edge(LEFT, buff=0.45)

        sous_q = Text("Que voit le voyageur à bord ?", font="Palatino",
                      color=SLATE, font_size=44, slant=ITALIC)
        sous_q.next_to(sep_q, DOWN, buff=0.25).to_edge(LEFT, buff=0.45)

        num_deco = Text("07 / 21", font="Palatino", color=AUBERGINE,
                        font_size=100, weight=BOLD)
        num_deco.to_corner(DR, buff=0.4)

        for q in [q1, q2, q3]:
            self.play(FadeIn(q, shift=UP * 0.06), run_time=0.18)
        self.play(
            GrowFromPoint(sep_q, sep_q.get_left()),
            run_time=0.3,
        )
        self.play(
            FadeIn(sous_q, shift=UP * 0.08),
            FadeIn(num_deco, shift=LEFT * 0.08),
            run_time=0.28,
        )
        self.wait(1.4)
        clear()

        # ════════════════════════════════════════════════════════════════════
        # BEAT 3 — Les 4 choix  (fond blanc cassé)
        # ════════════════════════════════════════════════════════════════════
        self.camera.background_color = BLANC

        hbar2 = header_bar()
        self.add(hbar2)

        choices = [
            ("A", "Une droite verticale"),
            ("B", "Une parabole"),
            ("C", "Une droite oblique"),
            ("D", "Un arc de cercle"),
        ]

        choice_mobs = []
        start_y = 2.5
        for i, (letter, txt) in enumerate(choices):
            y = start_y - i * 1.5
            s = Line(LEFT * 3.8, RIGHT * 3.8, stroke_width=0.7, color=SLATE)
            s.move_to(UP * (y + 0.62))
            lm = Text(letter, font="Palatino", color=GOLD,
                      font_size=80, weight=BOLD).move_to(LEFT * 3.2 + UP * y)
            tm = Text(txt, font="Palatino", color=NOIR,
                      font_size=50, weight=BOLD).move_to(RIGHT * 0.6 + UP * y)
            mob = VGroup(s, lm, tm)
            choice_mobs.append(mob)
            self.play(FadeIn(mob, shift=LEFT * 0.25), run_time=0.22)

        self.wait(0.9)
        clear()

        # ════════════════════════════════════════════════════════════════════
        # BEAT 4 — Mauvais choix + FAUX  (fond blanc → rouge)
        # ════════════════════════════════════════════════════════════════════
        self.camera.background_color = BLANC

        q_rappel = Text("Que voit le voyageur ?", font="Palatino",
                        color=SLATE, font_size=36, slant=ITALIC)
        q_rappel.move_to(UP * 3.8)
        self.add(q_rappel)

        # Bloc rouge — le mauvais choix
        wrong_bg = Rectangle(
            width=8.8, height=1.35,
            fill_color=ROUGE, fill_opacity=1, stroke_width=0,
        ).move_to(UP * 0.4)

        lw = Text("C", font="Palatino", color=BLANC,
                  font_size=90, weight=BOLD)
        lw.move_to(wrong_bg.get_left() + RIGHT * 1.0)

        tw = Text("Une droite oblique", font="Palatino",
                  color=BLANC, font_size=52, weight=BOLD)
        tw.move_to(wrong_bg.get_center() + RIGHT * 0.8)

        # Croix
        cx = Cross(wrong_bg, color=BLANC, stroke_width=5)

        faux = Text("FAUX.", font="Palatino", color=ROUGE,
                    font_size=190, weight=BOLD).move_to(DOWN * 2.0)
        faux_l = Line(LEFT * 2.2, RIGHT * 2.2, color=ROUGE, stroke_width=2)
        faux_l.next_to(faux, DOWN, buff=0.15)

        self.play(FadeIn(wrong_bg), FadeIn(lw), FadeIn(tw), run_time=0.15)
        self.play(Create(cx), run_time=0.25)
        self.play(Write(faux), GrowFromCenter(faux_l), run_time=0.35)
        self.wait(1.2)
        clear()

        # ════════════════════════════════════════════════════════════════════
        # BEAT 5 — "ET TOI ?"  (fond noir)
        # ════════════════════════════════════════════════════════════════════
        self.camera.background_color = NOIR

        l_top = Line(LEFT * 3.5, RIGHT * 3.5, color=GOLD, stroke_width=1.5)
        l_top.move_to(UP * 0.9)
        l_bot = Line(LEFT * 3.5, RIGHT * 3.5, color=GOLD, stroke_width=1.5)
        l_bot.move_to(DOWN * 1.5)

        et_toi = Text("ET TOI ?", font="Palatino", color=BLANC,
                      font_size=160, weight=BOLD).move_to(DOWN * 0.25)
        sous_et = Text("21 questions. Aucune formule.", font="Palatino",
                       color=GOLD, font_size=38, slant=ITALIC).move_to(DOWN * 2.25)

        self.play(GrowFromCenter(l_top), GrowFromCenter(l_bot), run_time=0.25)
        self.play(Write(et_toi), run_time=0.4)
        self.play(FadeIn(sous_et, shift=UP * 0.08), run_time=0.3)
        self.wait(1.5)
        clear()

        # ════════════════════════════════════════════════════════════════════
        # BEAT 6 — CTA  (fond aubergine)
        # ════════════════════════════════════════════════════════════════════
        self.camera.background_color = AUBERGINE

        brand_cta = Text("TerreMathématiques", font="Palatino",
                         color=GOLD, font_size=44, weight=BOLD).move_to(UP * 3.5)
        tag_cta = Text("La pensée en mouvement.", font="Palatino",
                       color=SAND, font_size=30, slant=ITALIC)
        tag_cta.next_to(brand_cta, DOWN, buff=0.15)

        sep_cta = Line(LEFT * 2.5, RIGHT * 2.5, color=GOLD, stroke_width=1)
        sep_cta.next_to(tag_cta, DOWN, buff=0.3)

        btn = Rectangle(
            width=7.8, height=1.3,
            fill_color=BLANC, fill_opacity=1, stroke_width=0,
        ).move_to(DOWN * 0.5)
        btn_txt = Text("Teste-toi → Lien en bio", font="Palatino",
                       color=AUBERGINE, font_size=44, weight=BOLD)
        btn_txt.move_to(btn.get_center())

        gratuit = Text("100 % GRATUIT", font="Palatino",
                       color=GOLD, font_size=34, weight=BOLD)
        gratuit.next_to(btn, DOWN, buff=0.45)

        self.play(FadeIn(brand_cta), FadeIn(tag_cta),
                  GrowFromCenter(sep_cta), run_time=0.35)
        self.play(GrowFromCenter(btn), run_time=0.28)
        self.play(FadeIn(btn_txt), run_time=0.2)
        self.play(FadeIn(gratuit, shift=UP * 0.08), run_time=0.22)

        # Pulsation
        self.play(btn.animate.scale(1.03), btn_txt.animate.scale(1.03), run_time=0.2)
        self.play(btn.animate.scale(1/1.03), btn_txt.animate.scale(1/1.03), run_time=0.2)

        self.wait(1.2)


# ─────────────────────────────────────────────────────────────────────────────
# COMMANDE DE RENDU
# manim -pqh qcm_tiktok_v2.py QCMEditorial -r 1080,1920
#
# DURÉE TOTALE ESTIMÉE : ~16–17 secondes
#
# EFFETS SONORES SUGGÉRÉS (à ajouter en post sur DaVinci Resolve) :
#   Beat 1 → whoosh grave au démarrage du "QCM"
#   Beat 4 → impact court + basse sourde sur "FAUX."
#   Beat 5 → silence total — le "ET TOI ?" doit frapper à froid
#   Beat 6 → ding léger sur l'apparition du bouton
# ─────────────────────────────────────────────────────────────────────────────
