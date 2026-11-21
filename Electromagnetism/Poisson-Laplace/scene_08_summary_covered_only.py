"""Visual recap of material already covered in the Laplace/Poisson scenes."""

import sys
from pathlib import Path

import numpy as np
from manim import *


PROJECT_DIR = Path(__file__).resolve().parent
if not (PROJECT_DIR / "settings34.py").exists():
    PROJECT_DIR = Path(r"C:\Users\Bruker\PycharmProjects\Youtube\Laplace and Poisson equation")
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from math_type import tex
from settings34 import BLUE, GREEN, GREY, RED, WHITE, YELLOW, run
from support34 import ar


class CoveredSummary(Scene):
    def construct(self):
        self.camera.background_color = "#05080D"
        self.caption = None

        self.say("ماذا تعلّمنا عن الشحنة والجهد والمجال؟")
        self.charge_to_field()
        self.gauss_law()
        self.poisson_equation()
        self.laplace_equation()
        self.boundary_conditions()
        self.uniqueness()
        self.covered_relations()

    def say(self, text):
        label = ar(text, 25, WHITE)
        if label.width > 12.4:
            label.scale_to_fit_width(12.4)
        label.move_to([0, 3.34, 0])
        if self.caption is None:
            self.play(FadeIn(label, shift=DOWN * 0.1), run_time=0.6)
        else:
            self.play(FadeOut(self.caption), FadeIn(label, shift=DOWN * 0.1), run_time=0.6)
        self.caption = label

    def clear_diagram(self):
        objects = [m for m in self.mobjects if m is not self.caption]
        if objects:
            self.play(*[FadeOut(m) for m in objects], run_time=0.55)

    def charge_to_field(self):
        self.say("من توزيع الشحنة نحسب المجال الكهربائي عند أي نقطة.")
        source = VGroup(
            *[Dot(p, radius=0.13, color=RED) for p in
              [(-4.4, 0.55, 0), (-3.65, 0.8, 0), (-3.0, 0.45, 0),
               (-3.75, -0.1, 0), (-4.25, -0.65, 0)]]
        )
        signs = VGroup(*[tex("+", 19, WHITE).move_to(d) for d in source])
        source_label = tex(r"\rho(\mathbf{r}')", 28, RED).move_to([-3.75, 1.25, 0])
        field_arrows = VGroup(*[
            Arrow(start, end, buff=0.12, color=BLUE, stroke_width=2.5,
                  max_tip_length_to_length_ratio=0.14)
            for start, end in [
                [(-2.7, 0.25, 0), (-1.65, 0.8, 0)],
                [(-2.7, -0.1, 0), (-1.45, -0.1, 0)],
                [(-2.7, -0.45, 0), (-1.65, -0.95, 0)],
                [(-3.45, 0.85, 0), (-2.95, 1.55, 0)],
                [(-3.65, -0.65, 0), (-3.35, -1.45, 0)],
            ]
        ])
        formula = tex(
            r"\mathbf{E}(\mathbf{r})=\frac{1}{4\pi\varepsilon_0}"
            r"\int_v\frac{\rho(\mathbf{r}')\,\hat{\mathbf{R}}}{R^2}\,dv'",
            28, YELLOW, width=6.2,
        ).move_to([2.25, 0.35, 0])
        formula_label = ar("نجمع مساهمة كل جزء من الشحنة", 21, YELLOW).move_to([2.3, 1.25, 0])
        self.play(FadeIn(source), FadeIn(signs), FadeIn(source_label), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in field_arrows], lag_ratio=0.12), run_time=1.7)
        self.play(FadeIn(formula_label), Write(formula), run_time=1.3)
        self.wait(1.8)

    def gauss_law(self):
        self.clear_diagram()
        self.say("من تباعد المجال نعرف كثافة الشحنة عند كل نقطة.")
        volume = Rectangle(width=4.3, height=2.6, color=GREEN, stroke_width=3).move_to([-2.65, 0.1, 0])
        charge = VGroup(Circle(radius=0.27, color=RED, fill_opacity=0.95), tex("+", 28, WHITE))
        charge.move_to([-2.65, 0.1, 0])
        arrows = VGroup(*[
            Arrow(a, b, buff=0.02, color=BLUE, stroke_width=2.3,
                  max_tip_length_to_length_ratio=0.15)
            for a, b in [
                [(-2.0, 0.1, 0), (-0.35, 0.1, 0)],
                [(-3.3, 0.1, 0), (-4.95, 0.1, 0)],
                [(-2.65, 0.55, 0), (-2.65, 1.15, 0)],
                [(-2.65, -0.35, 0), (-2.65, -0.95, 0)],
            ]
        ])
        boundary_label = ar("سطح مغلق يحيط بالشحنة", 20, GREEN).move_to([-2.65, 1.75, 0])
        gauss = tex(r"\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}", 42, YELLOW).move_to([2.8, 0.65, 0])
        curl = tex(r"\nabla\times\mathbf{E}=0", 36, BLUE).move_to([2.8, -0.45, 0])
        curl_label = ar("في الكهروستاتيكا", 19, BLUE).move_to([2.8, -1.05, 0])
        self.play(Create(volume), FadeIn(boundary_label), FadeIn(charge), run_time=1.1)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.5)
        self.play(Write(gauss), run_time=0.9)
        self.play(Write(curl), FadeIn(curl_label), run_time=0.9)
        self.wait(1.6)

    def poisson_equation(self):
        self.clear_diagram()
        self.say("نستبدل المجال بعلاقته بالجهد في قانون غاوس.")
        source = Dot([-3.3, 0.15, 0], radius=0.11, color=RED)
        contours = VGroup(*[
            Circle(radius=r, color=c, stroke_width=2.1).move_to(source)
            for r, c in [(0.48, YELLOW), (0.88, BLUE), (1.28, GREEN)]
        ])
        field_arrows = VGroup(*[
            Arrow(source.get_center() + d * 0.7, source.get_center() + d * 1.35,
                  buff=0, color=BLUE, stroke_width=2.2,
                  max_tip_length_to_length_ratio=0.16)
            for d in [UP, DOWN, LEFT, RIGHT]
        ])
        gauss = tex(r"\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}", 35, WHITE).move_to([2.75, 1.35, 0])
        field = tex(r"\mathbf{E}=-\nabla V", 35, BLUE).move_to([2.75, 0.5, 0])
        combined = tex(r"\nabla\cdot(-\nabla V)=\frac{\rho}{\varepsilon_0}", 35, WHITE, width=5.8).move_to([2.75, 0.9, 0])
        poisson = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 43, YELLOW).move_to([2.75, 0.15, 0])
        self.play(FadeIn(source), Create(contours), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in field_arrows], lag_ratio=0.12), run_time=1.1)
        self.play(Write(gauss), Write(field), run_time=1.1)
        self.play(Indicate(gauss, color=YELLOW), Indicate(field, color=BLUE), run_time=0.9)
        self.play(FadeOut(gauss), FadeOut(field), Write(combined), run_time=0.8)
        self.play(ReplacementTransform(combined, poisson), run_time=1.0)
        self.wait(1.8)

    def laplace_equation(self):
        self.clear_diagram()
        self.say("عندما تكون كثافة الشحنة صفراً، تصبح معادلة بواسون معادلة لابلاس.")
        left_plate = Line([-5.0, -1.15, 0], [-5.0, 1.3, 0], color=GREEN, stroke_width=6)
        right_plate = Line([-2.0, -1.15, 0], [-2.0, 1.3, 0], color=BLUE, stroke_width=6)
        left_value = tex(r"V(0)=0", 25, GREEN).next_to(left_plate, UP, buff=0.16)
        right_value = tex(r"V(L)=V_1", 25, BLUE).next_to(right_plate, UP, buff=0.16)
        region = Rectangle(width=2.65, height=1.75, color=GREY, stroke_width=1.4).move_to([-3.5, 0.05, 0])
        no_charge = ar("المنطقة خالية من الشحنات", 19, WHITE).move_to([-3.5, -0.65, 0])
        equation = tex(r"\rho=0\quad\Longrightarrow\quad\nabla^2V=0", 38, YELLOW).move_to([2.3, 1.15, 0])
        graph_axes = Axes(x_range=[0, 3, 1], y_range=[0, 6, 2], x_length=4.6, y_length=2.5,
                          tips=False, axis_config={"color": GREY, "stroke_width": 1.4, "include_ticks": False})
        graph_axes.move_to([2.2, -0.7, 0])
        graph = graph_axes.plot(lambda x: 2 * x, x_range=[0, 3], color=BLUE, stroke_width=4)
        graph_labels = VGroup(tex(r"x", 22).next_to(graph_axes.x_axis, DOWN, buff=0.08),
                              tex(r"V", 22).next_to(graph_axes.y_axis, UP, buff=0.08))
        field_arrow = Arrow([-2.15, 0.05, 0], [-4.85, 0.05, 0], buff=0.05, color=YELLOW, stroke_width=3)
        self.play(Create(left_plate), Create(right_plate), FadeIn(left_value), FadeIn(right_value),
                  Create(region), GrowArrow(field_arrow), FadeIn(no_charge), run_time=1.4)
        self.play(Write(equation), Create(graph_axes), Create(graph), FadeIn(graph_labels), run_time=1.6)
        self.wait(2.0)

    def boundary_conditions(self):
        self.clear_diagram()
        self.say("في شرط ديريشليه نحدد الجهد على الحدود. وفي شرط نيومان نحدد مشتقة الجهد باتجاه عمودي عليها.")
        left_box = Rectangle(width=3.15, height=2.25, color=GREEN, stroke_width=2.5).move_to([-3.25, 0.05, 0])
        right_box = Rectangle(width=3.15, height=2.25, color=BLUE, stroke_width=2.5).move_to([3.25, 0.05, 0])
        left_points = VGroup(*[Dot([x, y, 0], radius=0.055, color=GREEN)
                               for x in np.linspace(-4.72, -1.78, 7)
                               for y in (-1.0, 1.1)])
        right_normals = VGroup(*[
            Arrow([x, y, 0], [x + dx, y + dy, 0], buff=0, color=YELLOW, stroke_width=2,
                  max_tip_length_to_length_ratio=0.22)
            for x, y, dx, dy in [(1.68, 0, -0.4, 0), (4.82, 0, 0.4, 0),
                                 (3.25, 1.18, 0, 0.35), (3.25, -1.08, 0, -0.35)]
        ])
        dir_title = ar("ديريشليه", 23, GREEN).move_to([-3.25, 1.55, 0])
        neu_title = ar("نيومان", 23, BLUE).move_to([3.25, 1.55, 0])
        dir_eq = tex(r"V|_S=V_b", 32, GREEN).move_to([-3.25, -0.65, 0])
        neu_eq = tex(r"\left.\frac{\partial V}{\partial n}\right|_S=g_n", 31, BLUE).move_to([3.25, -0.65, 0])
        self.play(Create(left_box), FadeIn(left_points), FadeIn(dir_title), Write(dir_eq), run_time=1.2)
        self.play(Create(right_box), FadeIn(neu_title),
                  LaggedStart(*[GrowArrow(arrow) for arrow in right_normals], lag_ratio=0.12),
                  Write(neu_eq), run_time=1.5)
        self.wait(1.8)

    def uniqueness(self):
        self.clear_diagram()
        self.say("إذا تطابقت كثافة الشحنة والجهود على الحدود، فالحل واحد.")
        region = RoundedRectangle(width=4.2, height=2.55, corner_radius=0.08,
                                  color=GREEN, stroke_width=2.3, fill_color="#10202B",
                                  fill_opacity=0.38).move_to([-2.75, 0.05, 0])
        boundary_marks = VGroup(*[
            Dot(p, radius=0.045, color=GREEN)
            for p in [*[[x, 1.32, 0] for x in np.linspace(-4.75, -0.75, 8)],
                      *[[x, -1.22, 0] for x in np.linspace(-4.75, -0.75, 8)]]
        ])
        candidate_a = Ellipse(width=2.55, height=0.78, color=BLUE, stroke_width=3).move_to([-2.75, 0.12, 0])
        candidate_b = Ellipse(width=1.8, height=1.18, color=YELLOW, stroke_width=2.7).move_to([-2.75, 0.12, 0])
        label_a = tex(r"V_1", 26, BLUE).move_to([-4.2, 0.45, 0])
        label_b = tex(r"V_2", 26, YELLOW).move_to([-1.2, 0.45, 0])
        same_source = tex(r"\nabla^2V_1=\nabla^2V_2=-\rho/\varepsilon_0", 25, WHITE,
                          width=5.5).move_to([2.7, 2.1, 0])
        same_boundary = tex(r"V_1|_S=V_2|_S", 29, WHITE).move_to([2.7, 1.45, 0])
        difference = tex(r"W=V_1-V_2", 30, YELLOW).move_to([2.7, 0.62, 0])
        harmonic = tex(r"\nabla^2W=0,\quad W|_S=0", 29, BLUE, width=5.2).move_to([2.7, -0.18, 0])
        result = tex(r"W=0\quad\Longrightarrow\quad V_1=V_2", 31, GREEN, width=5.5).move_to([2.7, -1.05, 0])
        principle = ar("مبدأ القيمة العظمى", 19, WHITE).move_to([2.7, -1.72, 0])
        self.play(Create(region), FadeIn(boundary_marks), Create(candidate_a), Create(candidate_b),
                  FadeIn(label_a), FadeIn(label_b), run_time=1.4)
        self.play(Write(same_source), Write(same_boundary), Write(difference),
                  Write(harmonic), FadeIn(principle), run_time=1.5)
        self.play(Transform(candidate_b, candidate_a.copy()), Write(result), run_time=1.5)
        self.play(Indicate(result, color=GREEN), run_time=0.8)
        self.wait(1.8)

    def covered_relations(self):
        self.clear_diagram()
        self.say("نحسب المجال من الشحنة أو الجهد، ونستخرج الشحنة من المجال أو الجهد.")
        cards = []
        entries = [
            (r"\rho\;\longrightarrow\;\mathbf{E}",
             r"\mathbf{E}=\frac{1}{4\pi\varepsilon_0}\int_v\frac{\rho\hat{\mathbf{R}}}{R^2}\,dv'",
             "قانون كولوم لشحنة موزعة باستمرار", YELLOW),
            (r"\mathbf{E}\;\longrightarrow\;\rho",
             r"\nabla\cdot\mathbf{E}=\rho/\varepsilon_0,\quad\nabla\times\mathbf{E}=0",
             "قانون غاوس والمجال الكهروستاتيكي", BLUE),
            (r"V\;\longrightarrow\;\rho",
             r"\nabla^2V=-\rho/\varepsilon_0",
             "معادلة بواسون", RED),
            (r"V\;\longrightarrow\;\mathbf{E}",
             r"\mathbf{E}=-\nabla V",
             "المجال يساوي سالب تدرج الجهد", GREEN),
        ]
        positions = [(-3.25, 1.05, 0), (3.25, 1.05, 0), (-3.25, -1.25, 0), (3.25, -1.25, 0)]
        for (relation, equation, note, color), pos in zip(entries, positions):
            card = RoundedRectangle(width=5.85, height=1.85, corner_radius=0.12,
                                    stroke_color=color, stroke_width=1.8,
                                    fill_color="#0D1520", fill_opacity=0.82).move_to(pos)
            heading = tex(relation, 27, color).move_to([pos[0], pos[1] + 0.48, 0])
            formula = tex(equation, 23, WHITE, width=5.35).move_to([pos[0], pos[1] - 0.08, 0])
            description = ar(note, 17, GREY).move_to([pos[0], pos[1] - 0.58, 0])
            cards.append(VGroup(card, heading, formula, description))
        for card in cards:
            self.play(FadeIn(card[0]), Write(card[1]), Write(card[2]), FadeIn(card[3]), run_time=0.65)
        self.wait(2.5)


if __name__ == "__main__":
    run(CoveredSummary)
