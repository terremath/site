"""
=============================================================================
  TerreMathématique — Série Cryptographie
  Épisode 1 : Comment Turing a cassé Enigma
  -----------------------------------------------------------------------
  Format : 1080x1920 (9:16 vertical), 30 fps, ~90 secondes
  Manim Community >= 0.18
  -----------------------------------------------------------------------
  Rendu :
      manim -pqh turing_enigma.py Scene01_Hook
      manim -pqh turing_enigma.py Scene02_Enigma3D
      manim -pqh turing_enigma.py Scene03_Reflecteur
      manim -pqh turing_enigma.py Scene04_Cribs
      manim -pqh turing_enigma.py Scene05_Outro
  Pour itérer rapidement, remplacer -qh par -qm (qualité moyenne).
=============================================================================
"""

from manim import *
import numpy as np

# =============================================================================
#  CONFIGURATION GLOBALE — format vertical TikTok
# =============================================================================

config.frame_width   = 14.222
config.frame_height  = 25.28
config.pixel_width   = 1080
config.pixel_height  = 1920
config.frame_rate    = 30
config.background_color = "#32323C"  # ardoise

# ─── Métadonnées pour render_all.bat ─────────────────────────────────────────
SCENES = [
    "Scene01_Hook",
    "Scene02_Enigma3D",
    "Scene03_Reflecteur",
    "Scene04_Cribs",
    "Scene05_Outro",
]
OUTPUT_NAME = "turing_enigma_FINAL.mp4"
OUTPUT_DIR  = r"media\videos\turing_enigma\1920p30"
# ─────────────────────────────────────────────────────────────────────────────

# =============================================================================
#  PALETTE TERREMATHÉMATIQUE
# =============================================================================

AUBERGINE = "#4A235A"
AUBERGINE_CLAIR = "#6C3483"
OR = "#BF953F"
OR_CLAIR = "#D4AC5A"
SABLE = "#F2E6CB"
SABLE_FONCE = "#D9C99E"
ARDOISE = "#32323C"
ROUGE_ALERTE = "#C0392B"
BLANC_DOUX = "#F5F5F0"

# Police : Cormorant Garamond si dispo, sinon fallback automatique
FONT_TITLE = "Cormorant Garamond"
FONT_BODY = "Cormorant Garamond"


# =============================================================================
#  HELPERS — fabriques de texte cohérent avec la charte
# =============================================================================

def title_text(text, **kwargs):
    """Texte de titre, aubergine, gros."""
    return Text(
        text,
        font=FONT_TITLE,
        color=AUBERGINE,
        weight=BOLD,
        **kwargs,
    )


def body_text(text, **kwargs):
    """Texte de corps, sable clair, taille moyenne."""
    return Text(
        text,
        font=FONT_BODY,
        color=SABLE,
        **kwargs,
    )


def gold_text(text, **kwargs):
    """Texte or, pour accents et théorèmes."""
    return Text(
        text,
        font=FONT_TITLE,
        color=OR,
        weight=BOLD,
        **kwargs,
    )


def math(formula, color=SABLE, **kwargs):
    """Formule mathématique avec couleur cohérente."""
    return MathTex(formula, color=color, **kwargs)


def theorem_box(content_mobj, width=7.5, padding=0.4):
    """
    Encadre un contenu (Mobject) dans une boîte stylisée TerreMathématique :
    fond sable, bordure aubergine, légère épaisseur.
    """
    box = SurroundingRectangle(
        content_mobj,
        color=AUBERGINE,
        fill_color=SABLE,
        fill_opacity=0.95,
        buff=padding,
        stroke_width=4,
        corner_radius=0.15,
    )
    return VGroup(box, content_mobj)


# =============================================================================
#  SCENE 01 — HOOK (0–8s)
# =============================================================================

class Scene01_Hook(Scene):
    """
    Phrase d'accroche typographique. Pas de voix-off ici, juste du texte qui
    se construit lentement, avec le mot 'un point' qui s'illumine en or à
    la fin pour créer la tension.
    """

    def construct(self):
        # ---- Ligne 1 : "En 1940, une machine allemande" ----
        line1 = Text(
            "En 1940, une machine allemande",
            font=FONT_BODY,
            color=SABLE,
            font_size=50,
        )
        line2 = Text(
            "chiffrait les messages de la Wehrmacht.",
            font=FONT_BODY,
            color=SABLE,
            font_size=50,
        )
        line3 = Text(
            "Elle était mathématiquement parfaite.",
            font=FONT_BODY,
            color=SABLE,
            font_size=50,
        )
        # Dernière ligne avec mot 'un point' à mettre en or après coup
        line4 = Text(
            "Sauf sur un point.",
            font=FONT_BODY,
            color=SABLE,
            font_size=60,
            weight=BOLD,
        )

        block = VGroup(line1, line2, line3, line4).arrange(
            DOWN, buff=0.45, aligned_edge=LEFT
        )
        block.move_to(ORIGIN)

        # Apparition séquentielle ligne par ligne
        self.play(FadeIn(line1, shift=UP * 0.2), run_time=0.8)
        self.wait(0.4)
        self.play(FadeIn(line2, shift=UP * 0.2), run_time=0.8)
        self.wait(0.4)
        self.play(FadeIn(line3, shift=UP * 0.2), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(line4, shift=UP * 0.2), run_time=1.0)
        self.wait(0.6)

        # Mise en valeur de "un point" en or
        # On reconstruit line4 colorée par fragments pour isoler "un point"
        line4_colored = Text(
            "Sauf sur un point.",
            font=FONT_BODY,
            font_size=82,
            weight=BOLD,
            t2c={"un point": OR},
        )
        line4_colored.move_to(line4.get_center())

        self.play(Transform(line4, line4_colored), run_time=0.8)
        self.wait(1.4)

        # Fondu de sortie
        self.play(FadeOut(block), run_time=0.6)
        self.wait(0.2)


# =============================================================================
#  OBJET 3D — MACHINE ENIGMA LOW-POLY
# =============================================================================

class EnigmaMachine3D(VGroup):
    """
    Machine Enigma stylisée low-poly. Inspirée de l'Enigma M3 :
    - base aubergine parallélépipédique,
    - trois rotors cylindriques or côtelés,
    - réflecteur (cylindre tronqué) à gauche,
    - clavier suggéré par grille de petits cubes sable,
    - lampes (sphères) au-dessus du clavier.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ---- Base de la machine ----
        base = Prism(
            dimensions=[4.0, 2.5, 0.6],
            fill_color=AUBERGINE,
            fill_opacity=1.0,
            stroke_color=AUBERGINE_CLAIR,
            stroke_width=1.5,
        )
        base.move_to([0, 0, 0])

        # ---- Trois rotors (cylindres or, axe selon X) ----
        rotors = VGroup()
        for i, x in enumerate([-0.8, 0.0, 0.8]):
            rotor = Cylinder(
                radius=0.35,
                height=0.5,
                direction=RIGHT,
                fill_color=OR,
                fill_opacity=1.0,
                stroke_color=OR_CLAIR,
                stroke_width=1.0,
                resolution=(12, 12),
            )
            rotor.move_to([x, 0, 0.55])
            rotors.add(rotor)
        self.rotors = rotors

        # ---- Réflecteur (petit cylindre court à l'extrémité gauche des rotors) ----
        reflecteur = Cylinder(
            radius=0.42,
            height=0.25,
            direction=RIGHT,
            fill_color=AUBERGINE_CLAIR,
            fill_opacity=1.0,
            stroke_color=OR,
            stroke_width=1.5,
            resolution=(12, 12),
        )
        reflecteur.move_to([-1.45, 0, 0.55])
        self.reflecteur = reflecteur

        # ---- Clavier : grille 4x7 de petits cubes sable ----
        clavier = VGroup()
        for i in range(4):
            for j in range(7):
                if i == 3 and j >= 6:
                    continue  # 26 touches, pas 28
                key = Cube(
                    side_length=0.18,
                    fill_color=SABLE,
                    fill_opacity=1.0,
                    stroke_color=SABLE_FONCE,
                    stroke_width=0.5,
                )
                key.move_to([
                    -1.3 + j * 0.32,
                    -0.85 + i * 0.28,
                    0.32,
                ])
                clavier.add(key)
        self.clavier = clavier

        # ---- Lampes : grille 4x7 de petites sphères au-dessus du clavier ----
        lampes = VGroup()
        for i in range(4):
            for j in range(7):
                if i == 3 and j >= 6:
                    continue
                lampe = Sphere(
                    radius=0.08,
                    fill_color=SABLE_FONCE,
                    fill_opacity=0.9,
                    resolution=(8, 8),
                )
                lampe.move_to([
                    -1.3 + j * 0.32,
                    -0.85 + i * 0.28,
                    0.55,
                ])
                lampes.add(lampe)
        self.lampes = lampes

        # Assemblage
        self.add(base, reflecteur, rotors, clavier, lampes)

    def get_signal_path(self):
        """
        Renvoie une liste de points 3D représentant le trajet d'un signal
        électrique : entrée par une touche, traversée des 3 rotors, réflecteur,
        retour, sortie par une lampe différente.
        """
        return [
            np.array([0.5, -0.5, 0.32]),   # touche d'entrée
            np.array([0.8, 0.0, 0.55]),    # rotor 3
            np.array([0.0, 0.0, 0.55]),    # rotor 2
            np.array([-0.8, 0.0, 0.55]),   # rotor 1
            np.array([-1.45, 0.0, 0.55]),  # réflecteur (rebond)
            np.array([-0.8, 0.0, 0.55]),   # rotor 1 (retour)
            np.array([0.0, 0.0, 0.55]),    # rotor 2 (retour)
            np.array([0.8, 0.0, 0.55]),    # rotor 3 (retour)
            np.array([-0.6, 0.5, 0.55]),   # lampe de sortie
        ]


# =============================================================================
#  SCENE 02 — PRÉSENTATION ENIGMA EN 3D (8–22s)
# =============================================================================

class Scene02_Enigma3D(ThreeDScene):
    """
    Présentation 3D low-poly de la machine Enigma.
    La caméra est fixe avec micro-oscillation. Les textes 2D sont superposés
    via add_fixed_in_frame_mobjects pour rester lisibles en vertical.
    """

    def construct(self):
        # ---- Setup caméra : vue isométrique légère ----
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-55 * DEGREES,
            distance=10,
        )

        # ---- Titre 2D fixe en haut de l'écran ----
        title = Text(
            "ENIGMA",
            font=FONT_TITLE,
            color=OR,
            weight=BOLD,
            font_size=114,
        )
        title.to_edge(UP, buff=0.8)
        self.add_fixed_in_frame_mobjects(title)

        # ---- Apparition de la machine ----
        machine = EnigmaMachine3D()
        machine.shift(IN * 0.5)  # léger décalage pour cadrage vertical
        self.play(
            FadeIn(machine, shift=UP * 0.5),
            run_time=1.5,
        )

        # Légère rotation continue de la caméra (effet "vivant")
        self.begin_ambient_camera_rotation(rate=0.05, about="theta")

        # ---- Sous-titre 2D fixe : description ----
        subtitle1 = Text(
            "Chaque lettre est chiffrée",
            font=FONT_BODY,
            color=SABLE,
            font_size=60,
        )
        subtitle2 = Text(
            "par une permutation de l'alphabet.",
            font=FONT_BODY,
            color=SABLE,
            font_size=60,
        )
        subtitle_block = VGroup(subtitle1, subtitle2).arrange(DOWN, buff=0.2)
        subtitle_block.to_edge(DOWN, buff=2.5)
        self.add_fixed_in_frame_mobjects(subtitle_block)
        self.play(FadeIn(subtitle_block), run_time=0.8)
        self.wait(1.5)

        # ---- Animation : signal traverse la machine ----
        path_points = machine.get_signal_path()
        signal = Sphere(
            radius=0.08,
            fill_color=OR,
            fill_opacity=1.0,
            resolution=(8, 8),
        )
        signal.move_to(path_points[0])
        self.play(FadeIn(signal), run_time=0.3)

        # Le signal suit le chemin point par point, avec accélération
        for i in range(1, len(path_points)):
            self.play(
                signal.animate.move_to(path_points[i]),
                run_time=0.25,
                rate_func=linear,
            )

        # Flash final : la lampe d'arrivée s'illumine
        self.play(
            signal.animate.scale(1.8).set_color(OR_CLAIR),
            run_time=0.3,
        )
        self.play(FadeOut(signal), run_time=0.3)

        # ---- Changement de sous-titre : la combinatoire ----
        subtitle_block2 = VGroup(
            Text(
                "À chaque frappe, les rotors avancent.",
                font=FONT_BODY,
                color=SABLE,
                font_size=60,
            ),
            Text(
                "Plus de 10²⁰ configurations.",
                font=FONT_BODY,
                color=SABLE,
                font_size=66,
                weight=BOLD,
                t2c={"10²⁰": OR},
            ),
        ).arrange(DOWN, buff=0.25)
        subtitle_block2.to_edge(DOWN, buff=2.3)
        self.add_fixed_in_frame_mobjects(subtitle_block2)

        self.play(
            FadeOut(subtitle_block),
            FadeIn(subtitle_block2),
            run_time=0.6,
        )

        # Petite rotation des rotors pour suggérer leur fonctionnement
        self.play(
            Rotate(machine.rotors[0], angle=PI / 3, axis=RIGHT),
            Rotate(machine.rotors[1], angle=PI / 6, axis=RIGHT),
            Rotate(machine.rotors[2], angle=PI / 4, axis=RIGHT),
            run_time=1.5,
        )
        self.wait(1.0)

        # ---- Punchline : "Inviolable, en théorie." ----
        punchline = Text(
            "Inviolable, en théorie.",
            font=FONT_TITLE,
            color=OR,
            weight=BOLD,
            font_size=82,
            slant=ITALIC,
        )
        punchline.to_edge(DOWN, buff=1.0)
        self.add_fixed_in_frame_mobjects(punchline)
        self.play(FadeIn(punchline, shift=UP * 0.3), run_time=0.8)
        self.wait(1.2)

        self.stop_ambient_camera_rotation()

        # Fondu de sortie de tout
        self.play(
            FadeOut(machine),
            FadeOut(title),
            FadeOut(subtitle_block2),
            FadeOut(punchline),
            run_time=0.8,
        )
        self.wait(0.2)


# =============================================================================
#  OBJET 2D — RÉFLECTEUR
# =============================================================================

class Reflector2D(VGroup):
    """
    Représentation 2D du réflecteur d'Enigma : un demi-cercle avec 13 cordes
    qui relient les 26 contacts deux à deux. C'est l'objet visuel central
    de l'Acte III, où l'on démontre l'involution sans point fixe.
    """

    def __init__(self, radius=2.2, **kwargs):
        super().__init__(**kwargs)

        # ---- Demi-cercle (orienté vers la gauche) ----
        arc = Arc(
            radius=radius,
            start_angle=-PI / 2,
            angle=PI,
            color=AUBERGINE,
            stroke_width=5,
        )
        self.arc = arc

        # ---- 26 points de contact répartis sur le demi-cercle ----
        contacts = VGroup()
        contact_positions = []
        for i in range(26):
            theta = -PI / 2 + (i + 0.5) * PI / 26
            pos = radius * np.array([np.cos(theta), np.sin(theta), 0])
            dot = Dot(
                point=pos,
                radius=0.06,
                color=OR,
            )
            contacts.add(dot)
            contact_positions.append(pos)
        self.contacts = contacts
        self.contact_positions = contact_positions

        # ---- 13 cordes reliant les contacts par paires (pairing aléatoire) ----
        # Pour la lisibilité, on utilise un appariement fixe (i, 25-i) au début
        # puis on shuffle visuellement avec un seed reproductible
        rng = np.random.default_rng(seed=42)
        indices = list(range(26))
        rng.shuffle(indices)
        pairs = [(indices[2 * k], indices[2 * k + 1]) for k in range(13)]

        cordes = VGroup()
        for a, b in pairs:
            line = Line(
                contact_positions[a],
                contact_positions[b],
                color=OR,
                stroke_width=2.5,
                stroke_opacity=0.85,
            )
            cordes.add(line)
        self.cordes = cordes
        self.pairs = pairs

        self.add(arc, cordes, contacts)


# =============================================================================
#  SCENE 03 — RÉFLECTEUR ET PREUVE DU THÉORÈME (22–45s)
# =============================================================================

class Scene03_Reflecteur(Scene):
    """
    Cœur mathématique de l'épisode. On zoome sur le réflecteur, on énonce
    le théorème (involution sans point fixe), et on le démontre en trois
    lignes animées.
    """

    def construct(self):
        # ---- Phase 3a : apparition du réflecteur 2D ----
        intro = Text(
            "Le réflecteur",
            font=FONT_TITLE,
            color=OR,
            weight=BOLD,
            font_size=88,
        )
        intro.to_edge(UP, buff=1.2)
        self.play(FadeIn(intro), run_time=0.6)

        reflector = Reflector2D(radius=2.0)
        reflector.move_to(ORIGIN + UP * 0.5)
        self.play(
            Create(reflector.arc),
            FadeIn(reflector.contacts),
            run_time=1.2,
        )
        self.play(
            *[Create(c) for c in reflector.cordes],
            run_time=1.5,
        )
        self.wait(0.5)

        # Sous-titre explicatif
        sub = VGroup(
            Text(
                "13 fils, 26 contacts.",
                font=FONT_BODY,
                color=SABLE,
                font_size=88,
            ),
            Text(
                "Chaque lettre en croise une autre.",
                font=FONT_BODY,
                color=SABLE,
                font_size=55,
            ),
        ).arrange(DOWN, buff=0.2)
        sub.to_edge(DOWN, buff=3.5)
        self.play(FadeIn(sub), run_time=0.6)
        self.wait(1.5)

        # ---- Phase 3b : énoncé du théorème ----
        # On fait disparaître le sous-titre et on rapproche le réflecteur
        self.play(
            FadeOut(sub),
            reflector.animate.scale(0.65).to_edge(UP, buff=2.2),
            FadeOut(intro),
            run_time=0.8,
        )

        theoreme_titre = Text(
            "Théorème",
            font=FONT_TITLE,
            color=OR,
            weight=BOLD,
            font_size=70,
        )

        theoreme_formule = MathTex(
            r"\sigma_t^{\,2} = \mathrm{id}",
            r"\quad\text{et}\quad",
            r"\sigma_t(x) \neq x",
            color=AUBERGINE,
            font_size=82,
        )

        theoreme_block = VGroup(theoreme_titre, theoreme_formule).arrange(
            DOWN, buff=0.35
        )
        theoreme_box = SurroundingRectangle(
            theoreme_block,
            color=AUBERGINE,
            fill_color=SABLE,
            fill_opacity=0.95,
            buff=0.4,
            stroke_width=4,
            corner_radius=0.15,
        )
        full_theorem = VGroup(theoreme_box, theoreme_block)
        full_theorem.move_to(ORIGIN + DOWN * 0.5)

        self.play(FadeIn(full_theorem, shift=UP * 0.3), run_time=1.0)
        self.wait(0.4)

        sub_thm = Text(
            "Aucune lettre n'est jamais",
            font=FONT_BODY,
            color=SABLE,
            font_size=54,
        )
        sub_thm2 = Text(
            "chiffrée par elle-même.",
            font=FONT_BODY,
            color=SABLE,
            font_size=54,
            weight=BOLD,
            t2c={"elle-même": OR},
        )
        sub_thm_block = VGroup(sub_thm, sub_thm2).arrange(DOWN, buff=0.15)
        sub_thm_block.next_to(full_theorem, DOWN, buff=0.5)
        self.play(FadeIn(sub_thm_block), run_time=0.6)
        self.wait(1.8)

        # ---- Phase 3c : preuve en trois lignes ----
        self.play(
            FadeOut(reflector),
            FadeOut(sub_thm_block),
            full_theorem.animate.scale(0.7).to_edge(UP, buff=1.0),
            run_time=0.8,
        )

        proof_title = Text(
            "Preuve",
            font=FONT_TITLE,
            color=OR,
            weight=BOLD,
            font_size=70,
        )
        proof_title.next_to(full_theorem, DOWN, buff=0.6)
        self.play(FadeIn(proof_title), run_time=0.4)

        # Ligne 1 : décomposition de sigma_t
        line1 = MathTex(
            r"\sigma_t \;=\; P_t^{-1} \circ R \circ P_t",
            color=SABLE,
            font_size=70,
        )
        # Ligne 2 : carré
        line2 = MathTex(
            r"\sigma_t^{\,2} \;=\; P_t^{-1} R^{\,2} P_t \;=\; \mathrm{id}",
            color=SABLE,
            font_size=70,
        )
        # Ligne 3 : pas de point fixe
        line3 = MathTex(
            r"\sigma_t(x)=x \;\Longrightarrow\; R(P_t x)=P_t x",
            color=SABLE,
            font_size=64,
        )
        line3_conclusion = MathTex(
            r"\text{mais } R \text{ n'a pas de point fixe.} \;\;\bot",
            color=ROUGE_ALERTE,
            font_size=88,
        )

        proof_block = VGroup(line1, line2, line3, line3_conclusion).arrange(
            DOWN, buff=0.45, aligned_edge=LEFT
        )
        proof_block.next_to(proof_title, DOWN, buff=0.6)

        self.play(Write(line1), run_time=1.0)
        self.wait(0.6)
        self.play(Write(line2), run_time=1.0)
        self.wait(0.6)
        self.play(Write(line3), run_time=1.0)
        self.wait(0.3)
        self.play(FadeIn(line3_conclusion, shift=UP * 0.2), run_time=0.6)
        self.wait(0.4)

        # QED
        qed = MathTex(r"\blacksquare", color=OR, font_size=82)
        qed.next_to(proof_block, DOWN, buff=0.4).align_to(proof_block, RIGHT)
        self.play(FadeIn(qed, scale=1.5), run_time=0.4)
        self.wait(1.5)

        # Fondu de sortie
        self.play(
            FadeOut(VGroup(full_theorem, proof_title, proof_block, qed)),
            run_time=0.8,
        )
        self.wait(0.2)


# =============================================================================
#  SCENE 04 — CRIBS, COLLISIONS ET LES 40 % (45–72s)
# =============================================================================

class Scene04_Cribs(Scene):
    """
    Exploitation pratique du théorème : la méthode des cribs de Turing.
    On montre une bande crib qui glisse, on visualise les collisions, et
    on explique d'où viennent les 40 % d'alignements éliminés grâce au calcul
    1 - (25/26)^13.
    """

    def construct(self):
        # ---- Titre ----
        titre = Text(
            "L'attaque de Turing",
            font=FONT_TITLE,
            color=OR,
            weight=BOLD,
            font_size=82,
        )
        titre.to_edge(UP, buff=0.8)
        self.play(FadeIn(titre), run_time=0.5)

        # ---- Phase 4a : présentation du crib ----
        explication = VGroup(
            Text(
                "Turing devine qu'un mot connu",
                font=FONT_BODY,
                color=SABLE,
                font_size=54,
            ),
            Text(
                "se cache dans le message chiffré.",
                font=FONT_BODY,
                color=SABLE,
                font_size=54,
            ),
        ).arrange(DOWN, buff=0.15)
        explication.next_to(titre, DOWN, buff=0.6)
        self.play(FadeIn(explication), run_time=0.6)

        crib_label = Text(
            "Crib :",
            font=FONT_BODY,
            color=OR,
            font_size=80,
            weight=BOLD,
        )
        crib_text = Text(
            "WETTERBERICHT",
            font="Courier New",
            color=SABLE,
            font_size=74,
            weight=BOLD,
        )
        crib_group = VGroup(crib_label, crib_text).arrange(RIGHT, buff=0.3)
        crib_group.next_to(explication, DOWN, buff=0.7)
        self.play(FadeIn(crib_group), run_time=0.6)
        self.wait(1.0)

        # ---- Phase 4b : bande de chiffré et alignement ----
        # On crée une "bande" de positions candidates : 20 cases
        n_positions = 20
        case_size = 0.32
        cases = VGroup()
        for i in range(n_positions):
            case = Square(
                side_length=case_size,
                fill_color=SABLE_FONCE,
                fill_opacity=0.6,
                stroke_color=SABLE,
                stroke_width=1,
            )
            case.move_to([
                -3.0 + i * (case_size + 0.05),
                0,
                0,
            ])
            cases.add(case)

        cases.move_to(ORIGIN + DOWN * 0.5)

        bande_label = Text(
            "20 alignements possibles",
            font=FONT_BODY,
            color=SABLE,
            font_size=48,
        )
        bande_label.next_to(cases, UP, buff=0.4)

        self.play(
            FadeOut(explication),
            FadeIn(cases),
            FadeIn(bande_label),
            crib_group.animate.scale(0.7).next_to(cases, DOWN, buff=0.5),
            run_time=0.8,
        )
        self.wait(0.6)

        # ---- Phase 4c : test des alignements et collisions ----
        # On simule : pour chaque position, avec proba ~40% on a une collision
        # (rouge), sinon gris clair (survit). On utilise un seed pour
        # reproductibilité et pour atteindre exactement ~40%.
        rng = np.random.default_rng(seed=7)
        n_collisions_target = 8  # 8/20 = 40%
        collision_indices = sorted(
            rng.choice(n_positions, size=n_collisions_target, replace=False)
        )

        # Compteur de collisions
        compteur_label = Text(
            "Éliminées :",
            font=FONT_BODY,
            color=SABLE,
            font_size=48,
        )
        compteur_value = Text(
            "0",
            font=FONT_BODY,
            color=ROUGE_ALERTE,
            font_size=66,
            weight=BOLD,
        )
        compteur_total = Text(
            "/ 20",
            font=FONT_BODY,
            color=SABLE,
            font_size=48,
        )
        compteur = VGroup(compteur_label, compteur_value, compteur_total).arrange(
            RIGHT, buff=0.15
        )
        compteur.next_to(crib_group, DOWN, buff=0.7)
        self.play(FadeIn(compteur), run_time=0.4)

        # Test séquentiel rapide
        n_eliminated = 0
        for i in range(n_positions):
            highlight = SurroundingRectangle(
                cases[i], color=OR, stroke_width=3, buff=0.02
            )
            self.play(Create(highlight), run_time=0.06)
            if i in collision_indices:
                # Collision : la case devient rouge
                self.play(
                    cases[i].animate.set_fill(ROUGE_ALERTE, opacity=0.9),
                    run_time=0.08,
                )
                n_eliminated += 1
                new_value = Text(
                    str(n_eliminated),
                    font=FONT_BODY,
                    color=ROUGE_ALERTE,
                    font_size=66,
                    weight=BOLD,
                )
                new_value.move_to(compteur_value.get_center())
                self.remove(compteur_value)
                compteur_value = new_value
                self.add(compteur_value)
            self.play(FadeOut(highlight), run_time=0.04)

        self.wait(0.6)

        # ---- Phase 4d : la formule explicative ----
        formule = MathTex(
            r"\Pr[\text{collision}] \;=\; 1 - \left(\frac{25}{26}\right)^{13} \;\approx\; 39{,}7\,\%",
            color=AUBERGINE,
            font_size=64,
        )
        formule_box = SurroundingRectangle(
            formule,
            color=AUBERGINE,
            fill_color=SABLE,
            fill_opacity=0.95,
            buff=0.3,
            stroke_width=3,
            corner_radius=0.1,
        )
        formule_full = VGroup(formule_box, formule)
        formule_full.next_to(compteur, DOWN, buff=0.6)

        self.play(FadeIn(formule_full, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)

        # ---- Phase 4e : la conclusion ----
        # Les 8 cases rouges s'effacent en cascade
        self.play(
            *[FadeOut(cases[i]) for i in collision_indices],
            run_time=0.8,
        )

        conclusion = Text(
            "40 % éliminés gratuitement.",
            font=FONT_BODY,
            color=OR,
            weight=BOLD,
            font_size=64,
        )
        conclusion.move_to(formule_full.get_center())
        self.play(
            FadeOut(formule_full),
            FadeIn(conclusion, shift=UP * 0.2),
            run_time=0.6,
        )
        self.wait(1.0)

        suite = Text(
            "Le reste : la Bombe.",
            font=FONT_BODY,
            color=SABLE,
            font_size=54,
            slant=ITALIC,
        )
        suite.next_to(conclusion, DOWN, buff=0.4)
        self.play(FadeIn(suite), run_time=0.5)
        self.wait(1.5)

        # Fondu de sortie
        self.play(
            FadeOut(VGroup(
                titre, cases, bande_label, crib_group,
                compteur_label, compteur_value, compteur_total,
                conclusion, suite,
            )),
            run_time=0.7,
        )
        self.wait(0.2)


# =============================================================================
#  SCENE 05 — OUTRO PHILOSOPHIQUE ET CLIFFHANGER (72–90s)
# =============================================================================

class Scene05_Outro(Scene):
    """
    Conclusion : la leçon philosophique 'toute structure est une dette',
    puis cliffhanger pour l'épisode 2 sur Diffie-Hellman et les corps finis.
    """

    def construct(self):
        # ---- Phase 1 : la leçon principale ----
        ligne1 = Text(
            "Le réflecteur fut ajouté",
            font=FONT_BODY,
            color=SABLE,
            font_size=66,
        )
        ligne2 = Text(
            "pour le confort des opérateurs.",
            font=FONT_BODY,
            color=SABLE,
            font_size=66,
        )
        ligne3 = Text(
            "Il a coûté la guerre",
            font=FONT_TITLE,
            color=OR,
            weight=BOLD,
            font_size=80,
        )
        ligne4 = Text(
            "à l'Allemagne.",
            font=FONT_TITLE,
            color=OR,
            weight=BOLD,
            font_size=80,
        )

        block1 = VGroup(ligne1, ligne2, ligne3, ligne4).arrange(
            DOWN, buff=0.35, aligned_edge=LEFT
        )
        block1.move_to(ORIGIN + UP * 1.5)

        self.play(FadeIn(ligne1, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(ligne2, shift=UP * 0.2), run_time=0.7)
        self.wait(0.4)
        self.play(FadeIn(ligne3, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(ligne4, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)

        # ---- Phase 2 : la leçon générale ----
        principe = Text(
            "En cryptographie,",
            font=FONT_BODY,
            color=SABLE,
            font_size=64,
            slant=ITALIC,
        )
        principe2 = Text(
            "toute structure est une dette.",
            font=FONT_BODY,
            color=OR,
            weight=BOLD,
            font_size=65,
            slant=ITALIC,
        )
        principe_block = VGroup(principe, principe2).arrange(DOWN, buff=0.25)
        principe_block.next_to(block1, DOWN, buff=1.0)

        self.play(FadeIn(principe_block, shift=UP * 0.3), run_time=1.0)
        self.wait(2.5)

        # ---- Phase 3 : cliffhanger épisode 2 ----
        self.play(
            FadeOut(block1),
            FadeOut(principe_block),
            run_time=0.6,
        )

        cliff1 = Text(
            "Mais Enigma avait un autre défaut,",
            font=FONT_BODY,
            color=SABLE,
            font_size=60,
        )
        cliff2 = Text(
            "plus profond.",
            font=FONT_BODY,
            color=SABLE,
            font_size=60,
            weight=BOLD,
        )
        cliff3 = Text(
            "Alice et Bob devaient se rencontrer",
            font=FONT_BODY,
            color=SABLE,
            font_size=40,
        )
        cliff4 = Text(
            "pour partager la clé.",
            font=FONT_BODY,
            color=SABLE,
            font_size=40,
        )
        cliff5 = Text(
            "Et si on pouvait chiffrer pour",
            font=FONT_BODY,
            color=SABLE,
            font_size=40,
            slant=ITALIC,
        )
        cliff6 = Text(
            "quelqu'un qu'on n'a jamais vu ?",
            font=FONT_TITLE,
            color=OR,
            weight=BOLD,
            font_size=40,
            slant=ITALIC,
        )

        cliff_block = VGroup(
            cliff1, cliff2, cliff3, cliff4, cliff5, cliff6
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        cliff_block.move_to(ORIGIN + UP * 0.5)

        for line in cliff_block:
            self.play(FadeIn(line, shift=UP * 0.15), run_time=0.5)

        self.wait(1.5)

        # Bouton "Épisode 2"
        ep2_label = Text(
            "ÉPISODE 2",
            font=FONT_TITLE,
            color=ARDOISE,
            weight=BOLD,
            font_size=70,
        )
        ep2_box = SurroundingRectangle(
            ep2_label,
            color=OR,
            fill_color=OR,
            fill_opacity=1.0,
            buff=0.35,
            stroke_width=3,
            corner_radius=0.2,
        )
        ep2_button = VGroup(ep2_box, ep2_label)
        ep2_button.next_to(cliff_block, DOWN, buff=1.0)

        self.play(FadeIn(ep2_button, scale=1.2), run_time=0.7)
        self.wait(2.0)

        # Fondu final
        self.play(
            FadeOut(cliff_block),
            FadeOut(ep2_button),
            run_time=1.0,
        )
        self.wait(0.3)
