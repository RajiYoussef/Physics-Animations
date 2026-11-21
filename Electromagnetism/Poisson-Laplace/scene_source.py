import sys
from pathlib import Path

from manim import *


PROJECT_DIR = Path(__file__).resolve().parent
if not (PROJECT_DIR / "settings34.py").exists():
    PROJECT_DIR = Path(r"C:\Users\Bruker\PycharmProjects\Youtube\Laplace and Poisson equation")
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from settings34 import BLUE, GREEN, GREY, WHITE, YELLOW, run
from support34 import ar


class SourceScene(Scene):
    def construct(self):
        self.camera.background_color = "#05080D"

        cover = RoundedRectangle(
            width=10.6,
            height=4.65,
            corner_radius=0.15,
            stroke_color="#314457",
            stroke_width=1.8,
            fill_color="#0B1522",
            fill_opacity=0.96,
        )
        spine = Line([-4.85, -2.03, 0], [-4.85, 2.03, 0], color=YELLOW, stroke_width=4)
        section_label = ar(":المرجع المستخدم في هذا الفيديو هو الفصل الخامس من كتاب", 34, GREEN).move_to([0, 3.05, 0])
        title = Text(
            "Elementary Electromagnetism\nUsing Python",
            font_size=39,
            line_spacing=0.9,
            weight="BOLD",
            color=WHITE,
        ).move_to([0.3, 0.62, 0])
        author = Text(
            "Anders Malthe-Sørenssen",
            font_size=25,
            color=BLUE,
        ).move_to([0.3, -0.52, 0])
        divider = Line([-3.55, -1.0, 0], [3.95, -1.0, 0], color="#314457", stroke_width=1.5)
        chapter = VGroup(
            Text("CHAPTER  5", font_size=21, color=YELLOW),
            Text("|", font_size=23, color=GREY),
            Text("LAPLACE EQUATION", font_size=21, color=YELLOW),
        ).arrange(RIGHT, buff=0.28).move_to([0.3, -1.55, 0])

        self.play(Create(cover), run_time=0.9)
        self.play(Create(spine), FadeIn(section_label), run_time=1.1)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(author, shift=UP * 0.12), run_time=0.75)
        self.play(Create(divider), FadeIn(chapter, shift=UP * 0.1), run_time=0.95)
        self.wait(1.8)
        self.play(FadeOut(VGroup(cover, spine, section_label, title, author, divider, chapter)), run_time=0.6)


if __name__ == "__main__":
    run(SourceScene)
