"""Introduction to the neural-network approach in section 5.9."""

from manim import *

from settings34 import BLUE, GREEN, GREY, WHITE, YELLOW, run
from support34 import LessonScene, ar
from math_type import tex


class MachineLearningIntro(LessonScene):
    def construct(self):
        title = ar("من قيم على شبكة إلى دالة مستمرة", 30, BLUE).move_to([0, 3.55, 0])
        rule = Line([-6.1, 3.18, 0], [6.1, 3.18, 0], color="#344151", stroke_width=1.3)
        self.play(FadeIn(title), Create(rule), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(VGroup(title, rule)), run_time=0.5)

        region = Square(side_length=3.6, stroke_color=BLUE, stroke_width=2.2,
                        fill_color="#102332", fill_opacity=0.52).move_to([-3.55, 0.0, 0])
        grid = VGroup()
        for k in range(1, 6):
            q = -1.8 + 3.6 * k / 6
            grid.add(Line([-5.35 + q + 1.8, -1.8, 0], [-5.35 + q + 1.8, 1.8, 0],
                          color="#344151", stroke_width=0.8))
            grid.add(Line([-5.35, q, 0], [-1.75, q, 0], color="#344151", stroke_width=0.8))
        dots = VGroup()
        for j in range(7):
            for i in range(7):
                boundary = i in (0, 6) or j in (0, 6)
                dots.add(Dot([-5.35 + 0.6 * i, -1.8 + 0.6 * j, 0],
                             radius=0.045 if boundary else 0.035,
                             color=GREEN if boundary else GREY))
        lattice_label = ar("الفروق المحدودة: قيم عند نقاط الشبكة", 22, WHITE).move_to([-3.55, -2.25, 0])
        self.beat("lattice_values")
        self.say("في الفروق المحدودة، نحسب الجهد نقطةً نقطة على شبكة، ونختار القيم بحيث تحقق معادلة لابلاس بصيغتها المتقطعة.")
        self.play(Create(region), Create(grid), FadeIn(dots, lag_ratio=0.012),
                  FadeIn(lattice_label), run_time=2.6)
        self.wait(1.2)

        self.beat("a_different_representation")
        self.say("لكن في هذا القسم، الكتاب يقترح طريقة ثانية: نمثل الجهد بدالة واحدة تعطينا قيمته عند أي نقطة.")
        continuous_region = RoundedRectangle(width=3.7, height=3.6, corner_radius=0.08,
                    stroke_color=BLUE, stroke_width=2.2, fill_color="#102332",
                    fill_opacity=0.52).move_to([-3.55, 0, 0])
        contours = VGroup(*[
            Ellipse(width=w, height=h, color=c, stroke_width=1.6).move_to([-3.55, 0, 0])
            for w, h, c in ((0.9, 0.55, YELLOW), (1.8, 1.15, BLUE), (2.8, 1.85, GREEN))
        ])
        self.play(FadeOut(grid), FadeOut(dots), FadeOut(lattice_label),
                  Transform(region, continuous_region), FadeIn(contours), run_time=2.0)
        self.play(FadeIn(ar("منطقة مستمرة", 22, WHITE).move_to([-3.55, -2.25, 0])),
                  run_time=0.7)
        self.wait(0.8)

        self.beat("network_represents_the_function")
        self.say("نمثل الدالة بشبكة عصبية. أوزان الشبكة وانحيازاتها هي المعاملات التي سنختارها.")
        input_nodes = VGroup(*[Circle(radius=0.20, color=BLUE, fill_opacity=0.18).move_to([-0.3, y, 0])
                               for y in (0.65, -0.35)])
        hidden_nodes = VGroup(*[Circle(radius=0.19, color=GREY, fill_opacity=0.18).move_to([1.5, y, 0])
                                for y in (1.0, 0.25, -0.5, -1.25)])
        output_node = Circle(radius=0.22, color=GREEN, fill_opacity=0.18).move_to([3.4, -0.1, 0])
        wires = VGroup(*[
            Line(a.get_center(), b.get_center(), color="#506172", stroke_width=1.1)
            for a in input_nodes for b in hidden_nodes
        ], *[Line(n.get_center(), output_node.get_center(), color="#506172", stroke_width=1.1)
             for n in hidden_nodes])
        input_labels = VGroup(tex("x", 27, BLUE).next_to(input_nodes[0], LEFT, buff=0.2),
                              tex("y", 27, BLUE).next_to(input_nodes[1], LEFT, buff=0.2))
        output_label = tex("V(x,y; w_j)", 28, GREEN).next_to(output_node, RIGHT, buff=0.18)
        network_caption = ar("الأوزان والانحيازات هي المعاملات", 20, WHITE).move_to([1.55, -2.1, 0])
        self.play(Create(wires), FadeIn(input_nodes), FadeIn(hidden_nodes), FadeIn(output_node),
                  FadeIn(input_labels), FadeIn(output_label), FadeIn(network_caption), run_time=2.0)
        self.play(Indicate(hidden_nodes, color=YELLOW), run_time=0.9)
        self.wait(0.8)

        self.beat("fit_equation_and_boundaries")
        self.say("نضبط الأوزان والانحيازات بحيث تقترب الدالة من تحقيق معادلة لابلاس، وتوافق القيم المطلوبة على الحدود.")
        boundary_marks = VGroup(*[
            Dot(p, radius=0.055, color=GREEN)
            for p in [[-5.35 + 0.6*i, 1.8, 0] for i in range(7)]
            + [[-5.35 + 0.6*i, -1.8, 0] for i in range(7)]
        ])
        eq_label = ar("انحراف المعادلة", 19, YELLOW).move_to([3.75, 1.3, 0])
        bc_label = ar("انحراف الشروط الحدية", 18, GREEN).move_to([3.75, 0.25, 0])
        eq_bar = RoundedRectangle(width=2.3, height=0.22, corner_radius=0.1,
                                  stroke_width=0, fill_color="#344151", fill_opacity=1).move_to([3.7, 0.85, 0])
        bc_bar = eq_bar.copy().move_to([3.7, -0.15, 0])
        eq_fill = RoundedRectangle(width=1.9, height=0.16, corner_radius=0.08,
                                  stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([3.45, 0.85, 0])
        bc_fill = RoundedRectangle(width=1.75, height=0.16, corner_radius=0.08,
                                  stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to([3.52, -0.15, 0])
        parameter_label = tex("w_j", 28, YELLOW).move_to([1.55, -1.55, 0])
        self.play(FadeIn(boundary_marks), FadeIn(eq_label), FadeIn(bc_label),
                  FadeIn(eq_bar), FadeIn(bc_bar), FadeIn(eq_fill), FadeIn(bc_fill),
                  FadeIn(parameter_label), run_time=1.2)
        fitted_contours = VGroup(*[
            Ellipse(width=w, height=h, color=c, stroke_width=1.6).move_to([-3.55, 0, 0])
            for w, h, c in ((0.65, 0.42, YELLOW), (1.55, 0.96, BLUE), (2.65, 1.62, GREEN))
        ])
        self.play(eq_fill.animate.stretch(0.26, dim=0).align_to(eq_bar, LEFT),
                  bc_fill.animate.stretch(0.22, dim=0).align_to(bc_bar, LEFT),
                  Transform(contours, fitted_contours),
                  Indicate(boundary_marks, color=GREEN), run_time=2.0)
        self.play(Indicate(parameter_label, color=YELLOW), run_time=0.8)
        self.wait(0.8)

        self.beat("continuous_output")
        self.say("لن نتوقع تطابقاً تاماً؛ نبحث عن أفضل تقريب يحقق الشرطين معاً.")
        self.play(FadeOut(VGroup(wires, input_nodes, hidden_nodes, output_node,
                                 input_labels, output_label, network_caption,
                                 eq_label, bc_label, eq_bar, bc_bar, eq_fill, bc_fill,
                                 parameter_label, boundary_marks)), run_time=1.0)
        probe = Dot([-4.8, 0.3, 0], radius=0.075, color=YELLOW)
        readout = tex("V(x,y; w_j)", 30, YELLOW).move_to([2.8, 0.5, 0])
        grid_return = VGroup(*[
            Dot([-5.35 + .6*i, -1.8 + .6*j, 0], radius=.035, color=GREY)
            for i in range(1, 6) for j in range(1, 6)
        ])
        self.play(FadeIn(grid_return), FadeIn(probe), FadeIn(readout), run_time=1.0)
        self.play(MoveAlongPath(probe, Line([-4.8, 0.3, 0], [-2.3, 0.8, 0])),
                  Indicate(contours[1], color=YELLOW), run_time=2.2)
        self.say("ما نتوقع مطابقة تامة. نختار المعاملات بحيث نقلل انحراف الدالة عن المعادلة وعن الشروط الحدية.")
        self.say("وهكذا نحصل على دالة مستمرة. نقدر نطلب منها قيمة الجهد عند أي نقطة، حتى لو كانت بين نقاط الشبكة.")
        self.play(FadeOut(grid_return), run_time=0.6)
        self.wait(1.0)
        self.finish()


if __name__ == "__main__":
    run(MachineLearningIntro)
