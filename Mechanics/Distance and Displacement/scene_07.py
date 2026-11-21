"""Scene 7: final distance/displacement recap and curved-space teaser.
Run from PyCharm. Requires manim, numpy; SymPy is optional for a geometry check.
Optional: SCENE07_RECORD=1 enables manim-voiceover's microphone recorder.
Optional: put narration.wav beside this script to add an existing complete voiceover.
"""
from pathlib import Path
from contextlib import nullcontext
import math
import os
import numpy as np
from manim import *

try:
    from manim_voiceover import VoiceoverScene
    from manim_voiceover.services.recorder import RecorderService
    HAS_VOICEOVER = True
except ImportError:
    VoiceoverScene = Scene
    HAS_VOICEOVER = False

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "scene07_assets"
BG, FG, MUTED = "#0D1117", "#E6EDF3", "#9CA3AF"
GOLD, CYAN, GREEN = "#F2B84B", "#58A6FF", "#3FBF91"
FONT = "Arial"
FAST = os.environ.get("SCENE07_FAST") == "1"
RECORD = os.environ.get("SCENE07_RECORD") == "1"

VOICE_1 = "بالمختصر:\nالمسافة هي مقياس عددي لطول المسار الفعلي الذي تم قطعه بين موقعين، وقد يكون هذا المسار مستقيمًا أو منحنيًا أو كلاهما. بالتالي تعتمد قيمتها اعتمادًا كليًا على المسار الذي تم سلوكه."
VOICE_2 = "أما الإزاحة فهي مقياس متجهي (شعاع) للتغير في الموقع، يمتد من الموقع الابتدائي إلى الموقع النهائي.الإزاحة لها صفتين:  الاولى هي الإتجاه  والذي يمتد من الموقع الابتدائي الى الموقع النهائي ولا تعتمد على المسار الذي تم سلوكه ، والثانية هي المقدار وأحيانا تسمى ب \"الطويلة \"وفي الفضاء الإقليدي  ، اي الفضاء المسطح الذي نتعامل مع هندسته في حياتنا اليومية ،يمثل مقدارها طول الخط المستقيم الواصل بين الموقعين، وهو اقصر مسافة بينهما ."
VOICE_3 = "لكن ماذا لو كان الفضاء نفسه ليس مسطحا بل منحنيا كما في حالة الزمكان في النسبية العامة ؟هل يبقى مفهوم  \"أقصر مسافة بين نقطتين\" بهذه البساطة؟ هنا تبدأ قصة اخرى مشوقة ولكن دعنا لا نقلق بشأنها الآن."


def prepare_svg():
    """A small reusable vector map pin; no missing external assets."""
    ASSETS.mkdir(exist_ok=True)
    target = ASSETS / "point.svg"
    target.write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 100">
      <path d="M40 5 C19 5 5 20 5 42 C5 66 40 94 40 94 C40 94 75 66 75 42 C75 20 61 5 40 5 Z"
        fill="#E6EDF3" stroke="#0D1117" stroke-width="4"/>
      <circle cx="40" cy="41" r="13" fill="#0D1117"/>
    </svg>''', encoding="utf-8")
    return target


def curved_height(x, y):
    return -1.15 * math.exp(-0.22 * (x * x + y * y))


def make_grid(bent=False):
    lines = VGroup()
    for y in np.linspace(-2.1, 2.1, 9):
        lines.add(ParametricFunction(
            lambda t, y=y: np.array([t, y, curved_height(t, y) if bent else 0.0]),
            t_range=[-3.25, 3.25], color=CYAN, stroke_width=1.8,
        ))
    for x in np.linspace(-3.2, 3.2, 11):
        lines.add(ParametricFunction(
            lambda t, x=x: np.array([x, t, curved_height(x, t) if bent else 0.0]),
            t_range=[-2.1, 2.1], color=CYAN, stroke_width=1.8,
        ))
    return lines


class Scene07Finale(ThreeDScene, VoiceoverScene):
    def ar(self, value, size=29, color=FG):
        glyphs = Text("\u200e" + value, font=FONT, font_size=size, color=color)
        if glyphs.width <= 0 or glyphs.height <= 0:
            raise RuntimeError(f"Arabic text has no visible geometry: {value!r}")
        return glyphs

    def talk(self, paragraph):
        return self.voiceover(text=paragraph) if RECORD else nullcontext(None)

    @staticmethod
    def voice_segment_seconds(tracker, fallback):
        return max(0.7, tracker.duration) if tracker is not None else fallback

    def construct(self):
        self.camera.background_color = BG
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        pin_file = prepare_svg()

        if RECORD:
            if not HAS_VOICEOVER:
                raise ImportError("Install manim-voiceover to use SCENE07_RECORD=1")
            self.set_speech_service(RecorderService())
        else:
            audio = ROOT / "narration.wav"
            if audio.is_file():
                self.add_sound(str(audio))

        heading = self.ar("بالمختصر:", 39, FG).to_edge(UP, buff=0.34)
        start = np.array([-4.55, -1.75, 0])
        finish = np.array([1.25, -1.75, 0])

        pin_a = SVGMobject(str(pin_file))
        pin_b = SVGMobject(str(pin_file))
        pin_a.scale(0.45 / pin_a.height).move_to(start)
        pin_b.scale(0.45 / pin_b.height).move_to(finish)

        a_name = self.ar("الموقع الابتدائي", 24, GREEN).next_to(pin_a, DOWN, buff=0.12)
        b_name = self.ar("الموقع النهائي", 24, GREEN).next_to(pin_b, DOWN, buff=0.12)
        a_name.add_background_rectangle(color=BG, opacity=1, buff=0.09)
        b_name.add_background_rectangle(color=BG, opacity=1, buff=0.09)

        # Same endpoints, different paths; explicit stroke-only curves.
        def route(bump, waves=1):
            return ParametricFunction(
                lambda t: start + (finish - start) * t
                + UP * bump * math.sin(math.pi * t) *
                (1 + 0.16 * math.sin(waves * TAU * t)),
                t_range=[0, 1], color=GOLD, stroke_width=7,
            ).set_fill(opacity=0)

        path = route(2.9, 2)
        #path = route(1.35, 4)
        alternative = route(2.9, 2)
        dot = Dot(start, color=GOLD, radius=0.10)

        distance_title = self.ar("المسافة", 34, GOLD)
        distance_desc = self.ar("طول المسار الفعلي", 26, FG)
        distance_caption = VGroup(distance_title, distance_desc).arrange(DOWN, buff=0.15)
        distance_caption.move_to([4.25, 1.65, 0])

        self.add_fixed_in_frame_mobjects(heading)

        with self.talk(VOICE_1) as tracker:
            t = self.voice_segment_seconds(tracker, 9)
            self.play(
                FadeIn(heading),
                FadeIn(pin_a),
                FadeIn(pin_b),
                FadeIn(a_name),
                FadeIn(b_name),
                run_time=0.15 * t,
            )
            self.play(
                Create(path),
                MoveAlongPath(dot, path),
                run_time=0.44 * t,
                rate_func=linear,
            )
            self.play(FadeIn(distance_caption), run_time=0.12 * t)
            self.play(Transform(path, alternative), run_time=0.19 * t)
            self.wait(0.10 * t)

        arrow = Arrow(
            start, finish, buff=0.12, color=CYAN,
            stroke_width=8, max_tip_length_to_length_ratio=0.11,
        )
        disp_title = self.ar("الإزاحة", 34, CYAN)
        disp_title.move_to([4.25, 1.65, 0])

        properties = VGroup(
            self.ar("الاتجاه", 27, CYAN),
            self.ar("المقدار", 27, CYAN),
        ).arrange(DOWN, buff=0.28).move_to([4.2, 0.25, 0])

        shortest = self.ar("أقصر مسافة بين النقطتين", 26, FG)
        shortest.move_to([3.80, -2.15, 0])

        with self.talk(VOICE_2) as tracker:
            t = self.voice_segment_seconds(tracker, 13)
            self.play(
                FadeOut(distance_caption),
                path.animate.set_stroke(opacity=0.25),
                GrowArrow(arrow),
                FadeIn(disp_title),
                run_time=0.26 * t,
            )
            self.play(
                FadeIn(properties[0]),
                Indicate(arrow.get_tip(), color=CYAN),
                run_time=0.22 * t,
            )
            self.play(
                FadeIn(properties[1]),
                Indicate(arrow, color=CYAN),
                run_time=0.23 * t,
            )
            self.play(
                FadeIn(shortest),
                path.animate.set_stroke(opacity=0.12),
                run_time=0.17 * t,
            )
            self.wait(0.12 * t)

        # End the flat recap cleanly before changing camera orientation.
        self.play(
            *[
                FadeOut(x)
                for x in (
                    pin_a, pin_b, a_name, b_name, path,
                    dot, arrow, disp_title, properties, shortest,
                )
            ],
            run_time=0.8,
        )
        self.play(FadeOut(heading), run_time=0.3)

        flat = make_grid(False)
        curved = make_grid(True)

        curved_surface = Surface(
            lambda u, v: np.array([u, v, curved_height(u, v)]),
            u_range=[-3.25, 3.25],
            v_range=[-2.1, 2.1],
            resolution=(18, 12),
            fill_opacity=0.12,
            checkerboard_colors=[BLUE, BLUE],
            stroke_width=0,
        )

        teaser = self.ar("ماذا لو كان الفضاء منحنيًا؟", 31, FG)
        teaser.to_edge(UP, buff=0.45)

        question = self.ar("هل تبقى أقصر مسافة بهذه البساطة؟", 29, FG)
        question.to_edge(DOWN, buff=0.47)

        finale = self.ar("قصة أخرى...ستأتي لاحقاً", 30, CYAN).move_to([0, -2.55, 0])
        self.add_fixed_in_frame_mobjects(teaser, question, finale)

        with self.talk(VOICE_3) as tracker:
            t = self.voice_segment_seconds(tracker, 12)
            self.play(Create(flat), FadeIn(teaser), run_time=0.19 * t)
            self.move_camera(
                phi=60 * DEGREES,
                theta=-55 * DEGREES,
                zoom=0.93,
                run_time=0.23 * t,
            )
            self.play(
                Transform(flat, curved),
                FadeIn(curved_surface),
                run_time=0.29 * t,
            )
            self.play(FadeIn(question), run_time=0.12 * t)
            self.play(
                FadeOut(question),
                FadeIn(finale),
                run_time=0.10 * t,
            )
            self.wait(0.07 * t)

        self.play(
            FadeOut(flat),
            FadeOut(curved_surface),
            FadeOut(teaser),
            FadeOut(finale),
            run_time=1.1,
        )
        self.wait(0.3)


if __name__ == "__main__":
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60
    config.output_file = "scene_07"
    config.preview = True
    config.quality = "high_quality"

    Scene07Finale().render()



"""  
if __name__ == "__main__":
    script = Path(__file__).resolve()
    print(f"[SCENE07] Running: {script}", flush=True)
    print(f"[SCENE07] Voiceover recording: {RECORD}", flush=True)

    with tempconfig({
        "pixel_width": 960 if FAST else 1920,
        "pixel_height": 540 if FAST else 1080,
        "frame_rate": 20 if FAST else 60,
        "media_dir": str(ROOT / "scene07_media"),
        "output_file": "scene07_PREVIEW" if FAST else "scene07_FINAL",
        "preview": True,
    }):
        scene = Scene07Finale()
        scene.render()

        movie = Path(scene.renderer.file_writer.movie_file_path)
        print(f"[SCENE07] Video: {movie}", flush=True)

        # Optional visual-review contact sheet.
        try:
            import cv2
            from PIL import Image, ImageDraw

            cap = cv2.VideoCapture(str(movie))
            count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if count > 0:
                thumbs = []

                for frac in (0.12, 0.32, 0.53, 0.75, 0.90):
                    cap.set(
                        cv2.CAP_PROP_POS_FRAMES,
                        int((count - 1) * frac),
                    )
                    ok, frame = cap.read()

                    if ok:
                        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        im = Image.fromarray(rgb)
                        im.thumbnail((480, 270))
                        thumbs.append((frac, im.copy()))

                if thumbs:
                    sheet = Image.new(
                        "RGB",
                        (480, 300 * len(thumbs)),
                        "#0D1117",
                    )
                    draw = ImageDraw.Draw(sheet)

                    for i, (frac, im) in enumerate(thumbs):
                        sheet.paste(im, (0, i * 300 + 25))
                        draw.text(
                            (10, i * 300 + 5),
                            f"Timeline {frac:.0%}",
                            fill="white",
                        )

                    review = ROOT / "scene07_review_frames.jpg"
                    sheet.save(review, quality=88)
                    print(
                        f"[SCENE07] Review frames: {review}",
                        flush=True,
                    )

            cap.release()

        except ImportError:
            print(
                "[SCENE07] Install opencv-python and pillow "
                "for automatic frame contact sheet."
            )

"""