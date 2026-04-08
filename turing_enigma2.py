from manim import *
import numpy as np

# ------------------------------------------------------------
# Global render config
# ------------------------------------------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#32323C"

# ─── Métadonnées pour render_all.bat ─────────────────────────────────────────
SCENES = [
    "Scene01_Hook",
    "Scene02_Enigma",
    "Scene03_Reflecteur",
    "Scene04_Cribs",
    "Scene05_Outro",
]
OUTPUT_NAME = "turing_enigma2_FINAL.mp4"
OUTPUT_DIR  = r"media\videos\turing_enigma2\1920p30"
# ─────────────────────────────────────────────────────────────────────────────


class TerreMathColors:
    AUBERGINE = "#4A235A"
    OR = "#BF953F"
    SABLE = "#F2E6CB"
    ARDOISE = "#32323C"
    ROUGE_ALERTE = "#C0392B"
    VERT_DOUX = "#9FBF9F"
    GRIS = "#8C8C93"
    NOIR = "#111111"


FONT_SERIF = "Cormorant Garamond"
FONT_SANS = "DejaVu Sans"


def soft_title(text, size=42, color=TerreMathColors.SABLE, weight=BOLD):
    return Text(text, font=FONT_SERIF, font_size=size, color=color, weight=weight)


def soft_text(text, size=32, color=TerreMathColors.SABLE, weight=MEDIUM):
    return Text(text, font=FONT_SANS, font_size=size, color=color, weight=weight)


def theorem_panel(math_tex, width=7.6, height=1.6):
    box = RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=height,
        fill_color=TerreMathColors.SABLE,
        fill_opacity=1,
        stroke_color=TerreMathColors.OR,
        stroke_width=3,
    )
    eq = MathTex(math_tex, color=TerreMathColors.AUBERGINE, font_size=48)
    eq.move_to(box.get_center())
    return VGroup(box, eq)


class EnigmaMachine3D(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        base = Prism(dimensions=[4.8, 2.8, 0.55])
        base.set_fill(TerreMathColors.AUBERGINE, opacity=0.95)
        base.set_stroke(TerreMathColors.OR, width=1.5, opacity=0.6)
        base.shift(DOWN * 0.1)

        lid = Prism(dimensions=[4.8, 0.25, 1.55])
        lid.set_fill("#5a2f6e", opacity=0.35)
        lid.set_stroke(TerreMathColors.OR, width=1.0, opacity=0.4)
        lid.shift(UP * 0.78 + OUT * 0.3)

        rotors = VGroup()
        rotor_centers = []
        for x in [-1.0, 0.0, 1.0]:
            c = Cylinder(radius=0.38, height=1.2, direction=RIGHT, resolution=(20, 24))
            c.set_fill(TerreMathColors.OR, opacity=0.92)
            c.set_stroke(TerreMathColors.SABLE, width=0.6, opacity=0.7)
            c.rotate(PI / 2, axis=UP)
            c.move_to(np.array([x, 0.7, 0.62]))
            rings = VGroup(*[
                Circle(radius=0.38, stroke_color=TerreMathColors.ARDOISE, stroke_width=1.0)
                .rotate(PI / 2, axis=UP)
                .move_to(c.get_center() + RIGHT * (t - 0.5) * 0.95)
                for t in np.linspace(0.05, 0.95, 7)
            ])
            rotor = VGroup(c, rings)
            rotors.add(rotor)
            rotor_centers.append(c.get_center())

        lamp_row = VGroup()
        for x in np.linspace(-1.7, 1.7, 8):
            s = Sphere(radius=0.12, resolution=(10, 14))
            s.set_fill(TerreMathColors.SABLE, opacity=0.65)
            s.set_stroke(TerreMathColors.OR, width=0.5, opacity=0.5)
            s.move_to(np.array([x, 1.45, 0.35]))
            lamp_row.add(s)

        keyboard = VGroup()
        xs = np.linspace(-1.7, 1.7, 7)
        ys = [0.15, -0.2, -0.55, -0.9]
        for j, y in enumerate(ys):
            for i, x in enumerate(xs):
                p = Prism(dimensions=[0.22, 0.18, 0.09])
                p.set_fill(TerreMathColors.SABLE, opacity=0.9)
                p.set_stroke(TerreMathColors.ARDOISE, width=0.6)
                offset = 0.12 if j % 2 else 0.0
                p.move_to(np.array([x + offset, y, 0.32]))
                keyboard.add(p)

        reflector = Cylinder(radius=0.36, height=0.22, direction=UP, resolution=(16, 20))
        reflector.set_fill(TerreMathColors.OR, opacity=0.9)
        reflector.set_stroke(TerreMathColors.SABLE, width=0.8)
        reflector.move_to(np.array([1.95, 0.85, 0.62]))
        reflector.rotate(PI / 2, axis=RIGHT)

        self.base = base
        self.lid = lid
        self.rotors = rotors
        self.lamp_row = lamp_row
        self.keyboard = keyboard
        self.reflector = reflector
        self.rotor_centers = rotor_centers

        self.add(base, lid, keyboard, lamp_row, rotors, reflector)
        self.scale(0.9)

    def signal_path(self):
        pts = [
            np.array([-2.0, -0.15, 0.55]),
            np.array([-1.45, 0.15, 0.6]),
            self.rotor_centers[0] + np.array([0.0, 0.0, -0.05]),
            self.rotor_centers[1] + np.array([0.0, 0.0, 0.05]),
            self.rotor_centers[2] + np.array([0.0, 0.0, -0.05]),
            np.array([1.95, 0.85, 0.62]),
            self.rotor_centers[2] + np.array([0.0, 0.0, 0.18]),
            self.rotor_centers[1] + np.array([0.0, 0.0, 0.28]),
            self.rotor_centers[0] + np.array([0.0, 0.0, 0.22]),
            np.array([-1.55, 1.35, 0.55]),
        ]
        path = VMobject()
        path.set_points_as_corners(pts)
        path.set_stroke(TerreMathColors.OR, width=6, opacity=1)
        return path

    def keyboard_flash(self, index=2):
        if index < len(self.keyboard):
            return self.keyboard[index].copy().set_fill(TerreMathColors.OR, opacity=1)
        return None

    def lamp_flash(self, index=5):
        if index < len(self.lamp_row):
            return self.lamp_row[index].copy().set_fill(TerreMathColors.OR, opacity=1)
        return None


class Reflector2D(VGroup):
    def __init__(self, radius=3.2, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius

        arc = Arc(radius=radius, start_angle=-PI / 2, angle=PI, color=TerreMathColors.OR, stroke_width=5)
        back = VMobject()
        back.set_points_as_corners([
            arc.point_from_proportion(0),
            ORIGIN,
            arc.point_from_proportion(1),
        ])
        fill_shape = Sector(
            outer_radius=radius,
            start_angle=-PI / 2,
            angle=PI,
            fill_color=TerreMathColors.SABLE,
            fill_opacity=0.16,
            stroke_width=0,
        )

        contacts = VGroup()
        labels = VGroup()
        angles = np.linspace(-PI / 2 + 0.08, PI / 2 - 0.08, 26)
        self.contact_points = []
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        for i, ang in enumerate(angles):
            p = radius * np.array([np.cos(ang), np.sin(ang), 0])
            self.contact_points.append(p)
            d = Dot(p, radius=0.05, color=TerreMathColors.OR)
            contacts.add(d)
            t = Text(alphabet[i], font=FONT_SANS, font_size=20, color=TerreMathColors.SABLE)
            t.move_to((radius + 0.35) * np.array([np.cos(ang), np.sin(ang), 0]))
            labels.add(t)

        # 13 pairings, visual only. They need only be pairwise and fixed-point free.
        pairs = [(0, 13), (1, 19), (2, 7), (3, 24), (4, 9), (5, 16), (6, 22), (8, 12), (10, 18), (11, 25), (14, 20), (15, 23), (17, 21)]
        chords = VGroup()
        for i, j in pairs:
            line = Line(self.contact_points[i], self.contact_points[j], color=TerreMathColors.OR, stroke_width=2.2)
            chords.add(line)

        center = Dot(ORIGIN, radius=0.04, color=TerreMathColors.OR)
        self.arc = arc
        self.fill_shape = fill_shape
        self.contacts = contacts
        self.labels = labels
        self.chords = chords
        self.pairs = pairs

        self.add(fill_shape, arc, chords, contacts, labels, center)

    def highlight_pair(self, idx):
        i, j = self.pairs[idx]
        line = self.chords[idx].copy().set_color(TerreMathColors.ROUGE_ALERTE).set_stroke(width=6)
        di = self.contacts[i].copy().scale(1.8).set_color(TerreMathColors.ROUGE_ALERTE)
        dj = self.contacts[j].copy().scale(1.8).set_color(TerreMathColors.ROUGE_ALERTE)
        return VGroup(line, di, dj)


class CribBand(VGroup):
    def __init__(self, word, box_w=0.42, box_h=0.52, fill=TerreMathColors.SABLE, text_color=TerreMathColors.AUBERGINE, **kwargs):
        super().__init__(**kwargs)
        self.word = word
        boxes = VGroup()
        letters = VGroup()
        for i, ch in enumerate(word):
            r = RoundedRectangle(
                corner_radius=0.08,
                width=box_w,
                height=box_h,
                fill_color=fill,
                fill_opacity=0.96,
                stroke_color=TerreMathColors.OR,
                stroke_width=1.5,
            )
            r.shift(RIGHT * i * (box_w + 0.04))
            t = Text(ch, font=FONT_SANS, font_size=22, color=text_color, weight=BOLD)
            t.move_to(r.get_center())
            boxes.add(r)
            letters.add(t)
        group = VGroup(boxes, letters)
        group.move_to(ORIGIN)
        self.boxes = boxes
        self.letters = letters
        self.add(group)

    def slot_center(self, idx):
        return self.boxes[idx].get_center()

    def collision_mark(self, idx):
        x = Cross(self.boxes[idx], stroke_color=TerreMathColors.ROUGE_ALERTE, stroke_width=5)
        return x


class BombeMachine(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        frame = RoundedRectangle(
            width=6.2,
            height=2.1,
            corner_radius=0.15,
            fill_color="#2c2430",
            fill_opacity=0.9,
            stroke_color=TerreMathColors.OR,
            stroke_width=2,
        )
        drums = VGroup()
        for x in np.linspace(-2.0, 2.0, 4):
            drum = VGroup(
                Circle(radius=0.48, stroke_color=TerreMathColors.OR, stroke_width=3, fill_color=TerreMathColors.AUBERGINE, fill_opacity=1),
                *[
                    Line(np.array([x - 0.4, y, 0]), np.array([x + 0.4, y, 0]), color=TerreMathColors.SABLE, stroke_width=1)
                    for y in np.linspace(-0.26, 0.26, 5)
                ]
            )
            drum[0].move_to(RIGHT * x)
            for line in drum[1:]:
                line.shift(RIGHT * x)
            drums.add(drum)
        axle = Line(LEFT * 2.7, RIGHT * 2.7, color=TerreMathColors.SABLE, stroke_width=2)
        label = Text("BOMBE", font=FONT_SERIF, font_size=28, color=TerreMathColors.SABLE, weight=BOLD).move_to(frame.get_center() + DOWN * 0.72)
        self.frame = frame
        self.drums = drums
        self.axle = axle
        self.label = label
        self.add(frame, axle, drums, label)

    def spinning_overlays(self):
        overlays = VGroup()
        for drum in self.drums:
            c = drum[0].copy().set_fill(opacity=0).set_stroke(TerreMathColors.OR, width=5)
            overlays.add(c)
        return overlays


class CribAlignmentVisualizer(VGroup):
    def __init__(self, n=100, columns=10, **kwargs):
        super().__init__(**kwargs)
        rows = int(np.ceil(n / columns))
        cells = VGroup()
        for i in range(n):
            r = RoundedRectangle(
                corner_radius=0.04,
                width=0.5,
                height=0.36,
                fill_color=TerreMathColors.GRIS,
                fill_opacity=0.45,
                stroke_color=TerreMathColors.SABLE,
                stroke_width=0.6,
            )
            row = i // columns
            col = i % columns
            r.move_to(np.array([col * 0.58, -row * 0.44, 0]))
            cells.add(r)
        cells.move_to(ORIGIN)
        self.cells = cells
        self.add(cells)

    def red_indices(self):
        # 40 deterministic positions to match the ~39.7% story.
        return [0, 2, 4, 7, 9, 12, 15, 18, 20, 23, 25, 27, 30, 31, 34, 36, 39, 41, 44, 46,
                49, 51, 54, 57, 59, 61, 64, 66, 68, 71, 74, 77, 79, 81, 84, 87, 90, 93, 96, 98]


class Scene01_Hook(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        sentence = VGroup(
            soft_title("En 1940, une machine allemande", size=44),
            soft_title("chiffrait les messages de la Wehrmacht.", size=44),
            soft_title("Elle était mathématiquement parfaite.", size=44),
        ).arrange(DOWN, buff=0.28)
        sentence.move_to(UP * 1.0)

        final_line_left = soft_title("Sauf sur ", size=50)
        final_line_right = soft_title("un point.", size=50, color=TerreMathColors.OR)
        final_line = VGroup(final_line_left, final_line_right).arrange(RIGHT, buff=0.06)
        final_line.move_to(DOWN * 1.3)

        cursor = Rectangle(width=0.05, height=0.5, fill_color=TerreMathColors.SABLE, fill_opacity=1, stroke_width=0)
        cursor.next_to(sentence[0], RIGHT, buff=0.12)

        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.15) for line in sentence], lag_ratio=0.18, run_time=3.4))
        self.play(Blink(cursor), run_time=0.6)
        self.remove(cursor)
        self.play(Write(final_line_left), run_time=0.8)
        self.play(Write(final_line_right), run_time=0.7)
        glow = final_line_right.copy().set_color(TerreMathColors.OR).set_stroke(width=10, opacity=0.3)
        self.play(FadeIn(glow, scale=1.12), run_time=0.4)
        self.play(FadeOut(glow), run_time=0.3)
        self.wait(1.5)


class Scene02_Enigma(ThreeDScene):
    def construct(self):
        self.camera.background_color = TerreMathColors.ARDOISE
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=1.15)

        machine = EnigmaMachine3D()
        machine.shift(DOWN * 0.4)
        self.add(machine)

        title = soft_title("Enigma", size=48)
        subtitle = soft_text("Une permutation qui change à chaque frappe", size=28)
        title.to_edge(UP).shift(DOWN * 0.55)
        subtitle.next_to(title, DOWN, buff=0.12)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=1.0)

        labels = VGroup(
            soft_text("Clavier", size=24),
            soft_text("Rotor I", size=22),
            soft_text("Rotor II", size=22),
            soft_text("Rotor III", size=22),
            soft_text("Reflector", size=22),
            soft_text("Lampes", size=24),
        )
        labels.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        labels.scale(0.78)
        labels.to_edge(LEFT).shift(RIGHT * 0.4 + UP * 1.4)
        for mob in labels:
            mob.set_color(TerreMathColors.SABLE)
        self.add_fixed_in_frame_mobjects(labels)
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.12) for m in labels], lag_ratio=0.12), run_time=1.0)

        flash_key = machine.keyboard_flash(3)
        flash_lamp = machine.lamp_flash(5)
        if flash_key is not None:
            self.play(FadeIn(flash_key), run_time=0.3)
        path = machine.signal_path()
        self.play(Create(path), run_time=2.3)
        if flash_lamp is not None:
            self.play(FadeIn(flash_lamp), run_time=0.25)

        rotor_spin_anims = []
        for rotor in machine.rotors:
            rotor_spin_anims.append(Rotate(rotor, angle=0.45 * PI, axis=RIGHT, about_point=rotor[0].get_center()))
        self.play(*rotor_spin_anims, run_time=1.1)

        big_number = MathTex(r"10^{20}", color=TerreMathColors.OR, font_size=76)
        big_number.to_corner(UR).shift(LEFT * 0.8 + DOWN * 2.2)
        theory = soft_text("Inviolable, en théorie.", size=28, color=TerreMathColors.SABLE)
        theory.next_to(big_number, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(big_number, theory)
        self.play(FadeIn(big_number, scale=0.7), run_time=0.6)
        self.play(Wiggle(big_number, scale_value=1.08), run_time=0.9)
        self.play(FadeIn(theory, shift=UP * 0.1), run_time=0.5)

        micro = ValueTracker(-45)

        def updater(m):
            self.move_camera(theta=m.get_value() * DEGREES, phi=65 * DEGREES, zoom=1.15, frame_center=ORIGIN, run_time=0)

        micro.add_updater(updater)
        self.add(micro)
        self.play(micro.animate.set_value(-42), run_time=1.5, rate_func=there_and_back)
        self.remove(micro)

        self.wait(2.2)
        self.play(FadeOut(VGroup(path, flash_key if flash_key else VGroup(), flash_lamp if flash_lamp else VGroup())), run_time=0.5)
        self.wait(1.1)


class Scene03_Reflecteur(Scene):
    def construct(self):
        self.camera.background_color = TerreMathColors.ARDOISE

        intro = soft_text(
            "Le réflecteur a été ajouté pour que la même machine\nserve à chiffrer et à déchiffrer.",
            size=30,
        )
        intro.to_edge(UP).shift(DOWN * 0.75)

        reflector = Reflector2D(radius=2.85)
        reflector.shift(DOWN * 0.25)

        self.play(FadeIn(intro, shift=UP * 0.2), run_time=0.8)
        self.play(Create(reflector.arc), FadeIn(reflector.fill_shape), run_time=1.0)
        self.play(LaggedStart(*[Create(ch) for ch in reflector.chords], lag_ratio=0.04), run_time=1.8)
        self.play(FadeIn(reflector.contacts), FadeIn(reflector.labels), run_time=0.8)
        self.wait(0.6)

        theorem = theorem_panel(r"\sigma_t^2 = \mathrm{id} \qquad \text{et} \qquad \sigma_t(x) \neq x\ \forall x")
        theorem.scale(0.92)
        theorem.move_to(DOWN * 4.9)
        theorem.to_edge(DOWN).shift(UP * 1.2)
        self.play(FadeIn(theorem, scale=0.9), run_time=0.9)
        self.wait(0.9)

        proof_title = soft_title("Pourquoi ?", size=34, color=TerreMathColors.OR)
        proof_title.to_edge(LEFT).shift(RIGHT * 0.55 + UP * 2.2)

        line1 = MathTex(r"\sigma_t = P_t^{-1} \circ R \circ P_t", color=TerreMathColors.SABLE, font_size=42)
        line2 = MathTex(r"\sigma_t^2 = P_t^{-1} R^2 P_t = \mathrm{id}", color=TerreMathColors.SABLE, font_size=42)
        line3 = MathTex(r"\sigma_t(x)=x \Rightarrow R(P_t x)=P_t x\ \text{ impossible}", color=TerreMathColors.SABLE, font_size=40)
        lines = VGroup(line1, line2, line3).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        lines.next_to(proof_title, DOWN, aligned_edge=LEFT, buff=0.35)
        lines.shift(RIGHT * 0.1)

        visual_box = RoundedRectangle(
            width=3.1,
            height=4.0,
            corner_radius=0.12,
            fill_color="#2A2430",
            fill_opacity=0.65,
            stroke_color=TerreMathColors.OR,
            stroke_width=2,
        )
        visual_box.to_edge(RIGHT).shift(LEFT * 0.65 + DOWN * 0.2)

        miniature_machine = VGroup(
            RoundedRectangle(width=2.4, height=1.1, corner_radius=0.1, fill_color=TerreMathColors.AUBERGINE, fill_opacity=0.9, stroke_color=TerreMathColors.OR, stroke_width=1.5),
            *[
                Circle(radius=0.2, stroke_color=TerreMathColors.OR, stroke_width=2, fill_color=TerreMathColors.OR, fill_opacity=0.9).shift(np.array([x, 0.18, 0]))
                for x in [-0.5, 0.0, 0.5]
            ],
            Circle(radius=0.18, stroke_color=TerreMathColors.SABLE, stroke_width=2, fill_color=TerreMathColors.OR, fill_opacity=0.95).shift(RIGHT * 0.95 + UP * 0.18),
        )
        miniature_machine.move_to(visual_box.get_center() + UP * 1.0)

        path = VMobject(color=TerreMathColors.OR)
        path.set_points_as_corners([
            miniature_machine.get_center() + LEFT * 1.0 + DOWN * 0.1,
            miniature_machine.get_center() + LEFT * 0.55 + UP * 0.1,
            miniature_machine.get_center() + RIGHT * 0.95 + UP * 0.18,
            miniature_machine.get_center() + LEFT * 0.1 + UP * 0.32,
            miniature_machine.get_center() + LEFT * 0.95 + UP * 0.42,
        ])
        path.set_stroke(width=5)

        contradiction = VGroup(
            MathTex(r"R(y)=y", color=TerreMathColors.ROUGE_ALERTE, font_size=46),
            Cross(stroke_color=TerreMathColors.ROUGE_ALERTE, stroke_width=5).scale(0.45),
            soft_text("pas de point fixe", size=24, color=TerreMathColors.ROUGE_ALERTE),
        ).arrange(DOWN, buff=0.12)
        contradiction.move_to(visual_box.get_center() + DOWN * 1.0)

        frame = SurroundingRectangle(lines, buff=0.2, color=TerreMathColors.OR, stroke_width=2)

        self.play(FadeIn(proof_title), FadeIn(visual_box), run_time=0.7)
        self.play(Write(line1), FadeIn(miniature_machine, scale=0.92), run_time=1.1)
        self.play(Create(path), run_time=0.9)
        self.play(Write(line2), run_time=0.9)
        pulse = reflector.highlight_pair(0)
        self.play(FadeIn(pulse), run_time=0.45)
        self.play(FadeOut(pulse), run_time=0.35)
        self.play(Write(line3), run_time=1.1)
        self.play(FadeIn(contradiction, scale=0.92), run_time=0.6)
        self.play(Create(frame), run_time=0.6)
        self.wait(2.8)


class Scene04_Cribs(Scene):
    def construct(self):
        self.camera.background_color = TerreMathColors.ARDOISE

        title = soft_title("Le coup de Turing : le crib", size=42)
        title.to_edge(UP).shift(DOWN * 0.55)
        subtitle = soft_text("Supposer un mot probable et le faire glisser sur le message chiffré", size=26)
        subtitle.next_to(title, DOWN, buff=0.12)

        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.8)

        crib = CribBand("WETTERBERICHT")
        cipher = CribBand("QJLEETXVBXEPMT", fill="#26222a", text_color=TerreMathColors.SABLE)
        crib.scale(0.9)
        cipher.scale(0.9)
        crib.move_to(UP * 2.15)
        cipher.next_to(crib, DOWN, buff=0.85)

        crib_label = soft_text("hypothèse de texte clair", size=24, color=TerreMathColors.SABLE)
        cipher_label = soft_text("message chiffré observé", size=24, color=TerreMathColors.SABLE)
        crib_label.next_to(crib, UP, buff=0.2)
        cipher_label.next_to(cipher, DOWN, buff=0.2)

        self.play(FadeIn(crib_label), FadeIn(cipher_label), FadeIn(cipher), FadeIn(crib), run_time=1.0)
        self.play(crib.animate.shift(LEFT * 0.9), run_time=0.7)
        self.play(crib.animate.shift(RIGHT * 0.85), run_time=0.7)

        collision_idx_crib = 4
        collision_idx_cipher = 4
        crib_collision = crib.boxes[collision_idx_crib].copy().set_fill(TerreMathColors.ROUGE_ALERTE, opacity=0.95)
        cipher_collision = cipher.boxes[collision_idx_cipher].copy().set_fill(TerreMathColors.ROUGE_ALERTE, opacity=0.95)
        red_x = Cross(VGroup(crib.boxes[collision_idx_crib], cipher.boxes[collision_idx_cipher]), stroke_color=TerreMathColors.ROUGE_ALERTE, stroke_width=6)
        impossible = soft_title("Impossible : E ne peut pas devenir E.", size=32, color=TerreMathColors.ROUGE_ALERTE)
        impossible.next_to(cipher, DOWN, buff=1.0)

        self.play(FadeIn(crib_collision), FadeIn(cipher_collision), run_time=0.35)
        self.play(Create(red_x), run_time=0.35)
        self.play(FadeIn(impossible, shift=UP * 0.1), run_time=0.45)
        self.wait(0.8)

        self.play(
            FadeOut(VGroup(crib, cipher, crib_label, cipher_label, crib_collision, cipher_collision, red_x, impossible, subtitle)),
            title.animate.to_edge(UP).shift(DOWN * 0.25),
            run_time=0.9,
        )

        grid = CribAlignmentVisualizer(n=100, columns=10)
        grid.scale(0.95)
        grid.move_to(DOWN * 1.25)
        grid_label = soft_text("100 alignements candidats", size=28)
        grid_label.next_to(grid, UP, buff=0.35)
        formula = MathTex(
            r"1-\left(\frac{25}{26}\right)^{13}\approx 39.7\%",
            color=TerreMathColors.OR,
            font_size=48,
        )
        formula.to_edge(RIGHT).shift(LEFT * 1.0 + UP * 0.7)
        formula_box = SurroundingRectangle(formula, buff=0.18, corner_radius=0.1, color=TerreMathColors.OR)
        explanation = soft_text("au moins une collision lettre-à-lettre", size=24)
        explanation.next_to(formula, DOWN, buff=0.18)

        counter_label = soft_text("Éliminées", size=28, color=TerreMathColors.SABLE)
        counter_num = Integer(0, color=TerreMathColors.ROUGE_ALERTE, font_size=52)
        counter = VGroup(counter_label, counter_num).arrange(DOWN, buff=0.08)
        counter.to_edge(LEFT).shift(RIGHT * 0.85 + UP * 0.85)

        self.play(FadeIn(grid_label), FadeIn(grid), FadeIn(counter), run_time=0.9)

        red_ids = grid.red_indices()
        animations = []
        for step, idx in enumerate(red_ids, start=1):
            animations.append(grid.cells[idx].animate.set_fill(TerreMathColors.ROUGE_ALERTE, opacity=0.9).set_stroke(TerreMathColors.ROUGE_ALERTE))
            animations.append(counter_num.animate.set_value(step))
            if step % 5 == 0 or step == len(red_ids):
                self.play(*animations, run_time=0.6)
                animations = []
        if animations:
            self.play(*animations, run_time=0.4)

        self.play(FadeIn(formula_box), FadeIn(formula), FadeIn(explanation), run_time=0.8)
        note = soft_text(
            "Ce ne sont pas 40 % des bonnes clés.\nCe sont 40 % des alignements éliminés gratuitement.",
            size=24,
            color=TerreMathColors.SABLE,
        )
        note.next_to(grid, DOWN, buff=0.35)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)
        self.wait(1.0)

        survivors = VGroup(*[grid.cells[i] for i in range(len(grid.cells)) if i not in red_ids])
        survivor_label = soft_text("≈ 60 alignements restent à tester", size=28, color=TerreMathColors.SABLE)
        survivor_label.next_to(grid, UP, buff=0.35)
        self.play(
            FadeOut(grid_label),
            Transform(counter_label, soft_text("Restent", size=28, color=TerreMathColors.SABLE).move_to(counter_label)),
            counter_num.animate.set_value(len(survivors)),
            FadeIn(survivor_label),
            run_time=0.9,
        )

        loop_graph = VGroup(
            Dot(LEFT * 1.7 + DOWN * 0.3, color=TerreMathColors.OR),
            Dot(RIGHT * 1.7 + DOWN * 0.2, color=TerreMathColors.OR),
            Dot(UP * 1.4 + DOWN * 0.2, color=TerreMathColors.OR),
        )
        labels = VGroup(
            soft_text("A", size=28, color=TerreMathColors.SABLE).move_to(loop_graph[0].get_center() + DOWN * 0.35),
            soft_text("B", size=28, color=TerreMathColors.SABLE).move_to(loop_graph[1].get_center() + DOWN * 0.35),
            soft_text("C", size=28, color=TerreMathColors.SABLE).move_to(loop_graph[2].get_center() + UP * 0.35),
        )
        edges = VGroup(
            Line(loop_graph[0].get_center(), loop_graph[1].get_center(), color=TerreMathColors.SABLE),
            Line(loop_graph[1].get_center(), loop_graph[2].get_center(), color=TerreMathColors.SABLE),
            Line(loop_graph[2].get_center(), loop_graph[0].get_center(), color=TerreMathColors.SABLE),
        )
        edge_tags = VGroup(
            MathTex(r"t_1", color=TerreMathColors.OR, font_size=30).move_to(edges[0].get_center() + DOWN * 0.25),
            MathTex(r"t_2", color=TerreMathColors.OR, font_size=30).move_to(edges[1].get_center() + RIGHT * 0.3),
            MathTex(r"t_3", color=TerreMathColors.OR, font_size=30).move_to(edges[2].get_center() + LEFT * 0.3),
        )
        graph_group = VGroup(edges, loop_graph, labels, edge_tags)
        graph_group.scale(0.8)
        graph_group.to_edge(LEFT).shift(RIGHT * 1.5 + DOWN * 4.2)

        bombe = BombeMachine().scale(0.7)
        bombe.to_edge(RIGHT).shift(LEFT * 1.2 + DOWN * 4.05)
        bombe_title = soft_text("Boucles + Bombe", size=28, color=TerreMathColors.OR)
        bombe_title.next_to(VGroup(graph_group, bombe), UP, buff=0.2)

        speed = MathTex(r"17\,576\ \text{tests / seconde}", color=TerreMathColors.OR, font_size=40)
        speed.next_to(bombe, DOWN, buff=0.2)

        self.play(FadeIn(graph_group), FadeIn(bombe), FadeIn(bombe_title), run_time=1.0)
        self.play(LaggedStart(*[Indicate(e, color=TerreMathColors.OR, scale_factor=1.06) for e in edges], lag_ratio=0.15), run_time=1.0)
        spin_overlays = bombe.spinning_overlays()
        self.play(LaggedStart(*[Rotate(o, angle=PI, run_time=0.8) for o in spin_overlays], lag_ratio=0.06), FadeIn(speed), run_time=1.1)
        halt_ring = SurroundingRectangle(bombe.frame, buff=0.1, color=TerreMathColors.OR, stroke_width=3)
        self.play(Create(halt_ring), run_time=0.45)
        self.wait(2.0)


class Scene05_Outro(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        line1 = soft_title("Le réflecteur fut ajouté", size=48, color=TerreMathColors.SABLE)
        line2 = soft_title("pour le confort des opérateurs.", size=48, color=TerreMathColors.SABLE)
        line3 = soft_title("Il a coûté la guerre à l'Allemagne.", size=50, color=TerreMathColors.OR)
        block = VGroup(line1, line2, line3).arrange(DOWN, buff=0.24)
        block.move_to(UP * 1.2)

        debt = soft_title("En cryptographie, toute structure est une dette.", size=42, color=TerreMathColors.OR)
        debt.move_to(DOWN * 1.4)

        ep2 = VGroup(
            soft_text("Épisode 2 : partager une clé sans se rencontrer ?", size=30, color=TerreMathColors.SABLE),
            RoundedRectangle(width=3.0, height=0.7, corner_radius=0.18, fill_color=TerreMathColors.AUBERGINE, fill_opacity=0.95, stroke_color=TerreMathColors.OR, stroke_width=2),
        )
        button_text = soft_text("Épisode 2", size=28, color=TerreMathColors.OR, weight=BOLD)
        button_text.move_to(ep2[1].get_center())
        ep2_group = VGroup(ep2[0], ep2[1], button_text).arrange(DOWN, buff=0.28)
        ep2_group.move_to(DOWN * 4.6)

        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.18) for line in [line1, line2]], lag_ratio=0.16), run_time=1.4)
        self.play(FadeIn(line3, scale=0.95), run_time=0.8)
        self.wait(1.7)
        self.play(FadeIn(debt, shift=UP * 0.15), run_time=0.9)
        self.wait(1.6)
        self.play(FadeIn(ep2_group[0], shift=UP * 0.12), FadeIn(ep2_group[1], scale=0.92), FadeIn(ep2_group[2]), run_time=1.0)
        self.play(Indicate(ep2_group[1], color=TerreMathColors.OR, scale_factor=1.05), run_time=0.7)
        self.wait(2.3)


# ------------------------------------------------------------
# Optional voice-over text block (for copy/paste in post-prod)
# ------------------------------------------------------------
VOICEOVER_FR = {
    "Scene01_Hook": (
        "En 1940, une machine allemande chiffrait les messages de la Wehrmacht. "
        "Elle était mathématiquement parfaite. Sauf sur un point."
    ),
    "Scene02_Enigma": (
        "Enigma chiffre chaque lettre par une permutation des vingt-six lettres. "
        "À chaque frappe, les rotors avancent : la permutation change. "
        "Le nombre de configurations dépasse dix puissance vingt. Inviolable, en théorie."
    ),
    "Scene03_Reflecteur": (
        "Le réflecteur a été ajouté pour une raison pratique : permettre à la même machine "
        "de chiffrer et de déchiffrer. Mais ce confort cache un théorème. "
        "La permutation d'Enigma est une involution, sans aucun point fixe. "
        "Aucune lettre n'est jamais chiffrée par elle-même. "
        "Pourquoi ? Parce que sigma t égale P t inverse, puis le réflecteur, puis P t. "
        "Donc sigma t carré vaut l'identité. Et si sigma t de x valait x, alors le réflecteur "
        "aurait un point fixe. Impossible par construction."
    ),
    "Scene04_Cribs": (
        "Turing devine qu'un bulletin météo se cache dans le message. "
        "Il essaie tous les alignements possibles. Dès qu'une lettre du texte clair supposé "
        "tombe sur la même lettre dans le chiffré, l'alignement est impossible : une lettre ne peut jamais devenir elle-même. "
        "Pourquoi environ quarante pour cent ? Parce que sur treize positions, la probabilité d'éviter toute collision vaut "
        "vingt-cinq sur vingt-six à la puissance treize, environ soixante pour cent. "
        "Donc près de quarante pour cent des alignements sont éliminés instantanément. "
        "Sur les survivants, Turing exploite des cycles entre lettres. Sa machine, la Bombe, ne garde que les configurations cohérentes avec toutes les contraintes."
    ),
    "Scene05_Outro": (
        "Le réflecteur fut ajouté pour le confort des opérateurs. Il a coûté la guerre à l'Allemagne. "
        "En cryptographie, toute structure est une dette. "
        "Épisode deux : comment chiffrer pour quelqu'un qu'on n'a jamais vu ?"
    ),
}


# Example render commands:
# manim -qh turing_enigma.py Scene01_Hook
# manim -qh turing_enigma.py Scene02_Enigma
# manim -qh turing_enigma.py Scene03_Reflecteur
# manim -qh turing_enigma.py Scene04_Cribs
# manim -qh turing_enigma.py Scene05_Outro
