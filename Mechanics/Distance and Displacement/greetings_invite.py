"""Two-page closing scene with an animated Einstein character.

Page 1: 3.00 seconds. Page 2: 11.00 seconds.
Run directly using PyCharm's Run button.
"""
from html import escape
from pathlib import Path
from manim import *

# ------------------------------------------------------------
# EASY TO EDIT
# ------------------------------------------------------------
BACKGROUND = "#0D1117"
WHITEISH = "#E6EDF3"
GOLD = "#F4B85A"
CYAN = "#46D9FF"
MUTED = "#A5B1BF"
ARABIC_FONT = "Arial"
ENGLISH_FONT = "DejaVu Sans"

FIRST_PAGE_SECONDS = 3.0
GREETING_PAGE_SECONDS = 11.0

AR_VIDEO_TITLE = " الإزاحة  و المسافة ؟"
EN_VIDEO_TITLE = "Distance vs Displacement"

EN_VIDEO_SIGNATURE = "THE PHYSICS SYMPHONY "
AR_VIDEO_SUBTITLE = "سيمفونية الفيزياء"


AR_GREETING = "مع تحيات"
YOUR_NAME = "Raji Youssef"
YOUR_NICKNAME = "The Fifth Dimension"
AR_SUBSCRIBE = "اشتركوا في قناة"
CHANNEL_NAME = "The Physics Symphony"
CHANNEL_URL = "www.youtube.com/@PhysicsSymphony_R"

# Einstein character palette
SUIT = "#26384B"
SKIN = "#F4CBA3"
SKIN_SHADOW = "#D9A782"
HAIR = "#F2F0E6"
DARK = "#253044"


def polygon(points, color):
    """Filled vector polygon, with no unintended area strokes."""
    return Polygon(*points, fill_color=color, fill_opacity=1, stroke_width=0)


def make_einstein():
    """Original vector caricature. Return (person, independently animated right arm)."""
    person = VGroup()

    torso = polygon([[-1.12, -1.28, 0], [-0.66, -0.84, 0],
                     [0.70, -0.84, 0], [1.16, -1.28, 0],
                     [1.32, -2.70, 0], [-1.32, -2.70, 0]], SUIT)
    shirt = polygon([[-0.47, -0.94, 0], [0.46, -0.94, 0],
                     [0.30, -2.46, 0], [-0.28, -2.46, 0]], WHITEISH)
    left_lapel = polygon([[-0.75, -0.95, 0], [-0.34, -1.12, 0],
                          [0, -2.15, 0], [-0.69, -1.72, 0]], "#58718A")
    right_lapel = polygon([[0.75, -0.95, 0], [0.34, -1.12, 0],
                           [0, -2.15, 0], [0.69, -1.72, 0]], "#58718A")
    tie = polygon([[0, -1.12, 0], [-0.14, -1.34, 0],
                   [0, -1.53, 0], [0.14, -1.34, 0]], GOLD)
    person.add(torso, shirt, left_lapel, right_lapel, tie)

    neck = RoundedRectangle(width=0.55, height=0.59, corner_radius=0.14,
                            fill_color=SKIN_SHADOW, fill_opacity=1,
                            stroke_width=0).move_to([0, -0.79, 0])
    person.add(neck)

    hair_back = Ellipse(width=2.32, height=2.55,
                        fill_color=HAIR, fill_opacity=1,
                        stroke_width=0).move_to([0, 0.66, 0])
    person.add(hair_back)

    hair_points = [
        [[-1.02, 0.65, 0], [-1.57, 1.34, 0], [-0.87, 1.18, 0]],
        [[-0.96, 1.13, 0], [-1.31, 2.00, 0], [-0.50, 1.46, 0]],
        [[-0.55, 1.42, 0], [-0.62, 2.34, 0], [-0.08, 1.65, 0]],
        [[-0.18, 1.57, 0], [0.22, 2.43, 0], [0.42, 1.57, 0]],
        [[0.36, 1.45, 0], [1.04, 2.17, 0], [0.79, 1.16, 0]],
        [[0.76, 1.12, 0], [1.56, 1.67, 0], [1.03, 0.58, 0]],
        [[-1.02, 0.18, 0], [-1.55, 0.48, 0], [-0.92, -0.25, 0]],
        [[1.02, 0.18, 0], [1.52, 0.50, 0], [0.92, -0.24, 0]],
    ]
    person.add(VGroup(*(polygon(points, HAIR) for points in hair_points)))

    face = Ellipse(width=1.76, height=2.06, fill_color=SKIN,
                   fill_opacity=1, stroke_color=SKIN_SHADOW,
                   stroke_width=1.2).move_to([0, 0.46, 0])
    left_ear = Ellipse(width=0.30, height=0.48, fill_color=SKIN,
                       fill_opacity=1, stroke_width=0).move_to([-0.86, 0.24, 0])
    right_ear = Ellipse(width=0.30, height=0.48, fill_color=SKIN,
                        fill_opacity=1, stroke_width=0).move_to([0.86, 0.24, 0])
    person.add(left_ear, right_ear, face)

    eyes = VGroup(
        Ellipse(width=0.37, height=0.21, fill_color=WHITEISH,
                fill_opacity=1, stroke_width=0).move_to([-0.37, 0.60, 0]),
        Ellipse(width=0.37, height=0.21, fill_color=WHITEISH,
                fill_opacity=1, stroke_width=0).move_to([0.37, 0.60, 0]),
        Dot([-0.32, 0.60, 0], radius=0.067, color=DARK),
        Dot([0.32, 0.60, 0], radius=0.067, color=DARK),
    )
    brows = VGroup(
        Arc(radius=0.29, start_angle=0.30, angle=2.35,
            color=HAIR, stroke_width=8).move_to([-0.39, 0.93, 0]),
        Arc(radius=0.29, start_angle=0.50, angle=2.35,
            color=HAIR, stroke_width=8).move_to([0.39, 0.93, 0]),
    )
    nose = VMobject()
    nose.set_points_as_corners([[0.02, 0.51, 0], [-0.11, 0.04, 0],
                                [0.13, 0.02, 0]])
    nose.set_stroke(SKIN_SHADOW, width=2.2)
    nose.set_fill(opacity=0)
    smile = Arc(radius=0.28, start_angle=PI * 1.12, angle=PI * 0.75,
                color="#804D43", stroke_width=2.1).move_to([0, -0.35, 0])
    person.add(eyes, brows, nose, smile)

    left_moustache = Ellipse(width=0.65, height=0.23,
                            fill_color=HAIR, fill_opacity=1,
                            stroke_width=0).rotate(-0.14).move_to([-0.30, -0.13, 0])
    right_moustache = Ellipse(width=0.65, height=0.23,
                             fill_color=HAIR, fill_opacity=1,
                             stroke_width=0).rotate(0.14).move_to([0.30, -0.13, 0])
    person.add(left_moustache, right_moustache)

    left_arm = Line([-0.99, -1.25, 0], [-1.36, -2.12, 0],
                    color=SUIT, stroke_width=21)
    left_hand = Circle(radius=0.17, fill_color=SKIN,
                       fill_opacity=1, stroke_width=0).move_to([-1.36, -2.16, 0])
    person.add(left_arm, left_hand)

    arm = VGroup(
        Line([0.92, -1.18, 0], [1.76, -0.44, 0],
             color=SUIT, stroke_width=22),
        Circle(radius=0.21, fill_color=SKIN,
               fill_opacity=1, stroke_width=0).move_to([1.83, -0.36, 0]),
    )
    for offset in (-0.12, -0.04, 0.04, 0.12):
        arm.add(Line([1.80 + offset, -0.28, 0],
                     [1.86 + offset, 0.09, 0], color=SKIN, stroke_width=5))
    person.add(arm)

    return person, arm


class PhysicsOutroTyping(Scene):
    def ar(self, content, font_size=30, color=WHITEISH):
        return MarkupText(escape(content), font=ARABIC_FONT,
                          font_size=font_size, color=color)

    def en(self, content, font_size=30, color=WHITEISH):
        return Text(content, font=ENGLISH_FONT,
                    font_size=font_size, color=color)

    @staticmethod
    def sized(obj, max_width):
        if obj.width > max_width:
            obj.scale_to_fit_width(max_width)
        return obj

    def type_reveal(self, obj, seconds):
        self.play(ShowIncreasingSubsets(obj, rate_func=linear), run_time=seconds)

    def fade_everything(self, seconds):
        if self.mobjects:
            self.play(FadeOut(Group(*list(self.mobjects))), run_time=seconds)
        else:
            self.wait(seconds)

    def construct(self):
        self.camera.background_color = BACKGROUND
        self.episode_page()
        self.greeting_page()

    def episode_page(self):
        arabic_title = self.sized(self.ar(AR_VIDEO_TITLE, 56, GOLD), 11.5).move_to(UP * 1.62)
        divider = Line(LEFT * 2.25, RIGHT * 2.25,
                       stroke_color=CYAN, stroke_width=2).move_to(UP * 0.72)
        english_title = self.sized(self.en(EN_VIDEO_TITLE, 35), 11.4).move_to(UP * 0.12)
        arabic_subtitle = self.sized(self.ar(AR_VIDEO_SUBTITLE, 28), 11.5).move_to(DOWN * 0.87)
        signature = self.sized(self.en(EN_VIDEO_SIGNATURE, 25, CYAN), 11.4).move_to(DOWN * 1.91)

        self.type_reveal(arabic_title, 0.55)
        self.play(Create(divider), run_time=0.20)
        self.type_reveal(english_title, 0.38)
        self.type_reveal(arabic_subtitle, 0.53)
        self.type_reveal(signature, 0.34)
        self.wait(0.65)
        self.fade_everything(0.35)
        # 0.55 + 0.20 + 0.38 + 0.53 + 0.34 + 0.65 + 0.35 = 3.00

    def greeting_page(self):
        # Reserve the right-hand portion of the frame for Einstein.
        text_x = -2.25
        text_width = 7.15

        def left_text(obj, y):
            return self.sized(obj, text_width).move_to([text_x, y, 0])

        greeting = left_text(self.ar(AR_GREETING, 37), 2.60)
        name = left_text(self.en(YOUR_NAME, 56, GOLD), 1.78)
        nickname = left_text(self.en(YOUR_NICKNAME, 32, CYAN), 0.92)
        separator = Line(LEFT * 2.15, RIGHT * 2.15,
                         color=WHITEISH, stroke_opacity=0.40,
                         stroke_width=1.5).move_to([text_x, 0.20, 0])
        invitation = left_text(self.ar(AR_SUBSCRIBE, 35), -0.65)
        channel = left_text(self.en(CHANNEL_NAME, 46, GOLD), -1.50)
        url = left_text(self.en(CHANNEL_URL, 26, CYAN), -2.38)

        einstein, waving_arm = make_einstein()
        einstein.scale(0.91)
        einstein.move_to([4.50, -0.30, 0])
        shoulder = waving_arm[0].get_start().copy()

        # All character actions happen IN PARALLEL with the original
        # text timings, preserving precisely 11 seconds for this page.
        self.play(ShowIncreasingSubsets(greeting, rate_func=linear),
                  FadeIn(einstein, shift=UP * 0.15), run_time=0.65)
        self.play(ShowIncreasingSubsets(name, rate_func=linear),
                  Rotate(waving_arm, angle=0.20, about_point=shoulder), run_time=1.10)
        self.play(ShowIncreasingSubsets(nickname, rate_func=linear),
                  Rotate(waving_arm, angle=-0.20, about_point=shoulder), run_time=0.90)
        self.play(Create(separator), run_time=0.35)
        self.type_reveal(invitation, 0.75)
        self.type_reveal(channel, 1.45)
        self.type_reveal(url, 1.45)
        self.wait(3.65)
        self.fade_everything(0.70)
        # 0.65 + 1.10 + 0.90 + 0.35 + 0.75 + 1.45 + 1.45 + 3.65 + 0.70 = 11.00

if __name__ == "__main__":
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60
    config.output_file = "greeting_final"
    config.preview = True
    config.quality = "high_quality"

    PhysicsOutroTyping().render()






"""
if __name__ == "__main__":
    source = Path(__file__).resolve()
    print(f"[OUTRO] Script: {source}", flush=True)
    with tempconfig({
        "pixel_width": 1920,
        "pixel_height": 1080,
        "frame_rate": 60,
        "background_color": BACKGROUND,
        "media_dir": str(source.parent / "outro_media"),
        "output_file": "Physics_Outro_Einstein",
        "preview": True,
        "quality": "high_quality",
    }):
        scene = PhysicsOutroTyping()
        scene.render()
        print(f"[OUTRO] Video: {scene.renderer.file_writer.movie_file_path}", flush=True)

"""