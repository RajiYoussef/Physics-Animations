"""Short visual explanation of why Laplace's equation appears in many fields."""

import os
os.environ.setdefault("POISSON_QUALITY", "final")

from manim import *
import numpy as np

from math_type import tex
from settings34 import BLUE, GREEN, GREY, WHITE, YELLOW, run
from support34 import LessonScene, ar


class WhyLaplaceCommon(LessonScene):
    def construct(self):
        self.beat("laplace_equation_reappears")
        title = ar("لماذا تظهر معادلة لابلاس في مجالات كثيرة؟", 30)
        laplace = tex(r"\nabla^2 u=0", 43, YELLOW)
        opening = VGroup(title, laplace).arrange(DOWN, buff=0.16).move_to([0, 3.02, 0])
        self.play(FadeIn(title, shift=DOWN * 0.15), Write(laplace), run_time=2.2)
        self.wait(0.7)

        concentration_title = ar("انتشار التركيز", 25, BLUE)
        concentration_equation = tex(r"\frac{\partial c}{\partial t}=D\nabla^2c", 29, BLUE)
        concentration_head = VGroup(concentration_title, concentration_equation).arrange(DOWN, buff=0.12)
        concentration_head.move_to([-3.4, 1.75, 0])

        temperature_title = ar("انتشار الحرارة", 25, YELLOW)
        temperature_equation = tex(r"\frac{\partial T}{\partial t}=\alpha\nabla^2T", 29, YELLOW)
        temperature_head = VGroup(temperature_title, temperature_equation).arrange(DOWN, buff=0.12)
        temperature_head.move_to([3.4, 1.75, 0])

        graph_axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 1, 0.25],
            x_length=4.5, y_length=2.45, tips=False,
            axis_config={"color": GREY, "stroke_width": 1.8, "include_ticks": False},
        ).move_to([-3.4, -0.38, 0])
        x_label = tex(r"r", 23, WHITE).next_to(graph_axes.x_axis.get_end(), RIGHT, buff=0.08)
        y_label = tex(r"c(r,t)", 22, BLUE).next_to(graph_axes.y_axis.get_end(), UP, buff=0.08)
        spread = ValueTracker(0.0)

        def concentration_profile(r):
            sigma = 0.34 + 0.76 * spread.get_value()
            return 0.88 * (0.34 / sigma) * np.exp(-(r * r) / (2 * sigma * sigma))

        profile = always_redraw(
            lambda: graph_axes.plot(
                concentration_profile, x_range=[-3, 3], color=BLUE, stroke_width=4,
            )
        )
        profile_area = always_redraw(
            lambda: graph_axes.get_area(
                profile, x_range=(-3, 3), color=BLUE, opacity=0.16,
            )
        )

        heat_center = np.array([3.4, -0.38, 0])
        grid_size = 11
        cell_step = 0.245
        cell_side = 0.224
        cells = VGroup()
        cell_data = []
        thermal_spread = ValueTracker(0.0)
        for row in range(grid_size):
            for column in range(grid_size):
                x = (column - (grid_size - 1) / 2) * cell_step
                y = ((grid_size - 1) / 2 - row) * cell_step
                cell = Square(
                    side_length=cell_side,
                    stroke_color="#45515F", stroke_width=0.55,
                    fill_color="#211A18", fill_opacity=0.98,
                ).move_to(heat_center + np.array([x, y, 0]))
                cells.add(cell)
                cell_data.append((cell, x, y))

        def update_heatmap(_tracker):
            sigma = 0.30 + 0.78 * thermal_spread.get_value()
            for cell, x, y in cell_data:
                amplitude = (0.30 / sigma) * np.exp(-(x*x + y*y) / (2 * sigma*sigma))
                color = interpolate_color(ManimColor("#162336"), ManimColor("#F6A640"), float(amplitude))
                cell.set_fill(color, opacity=0.98)

        cells.add_updater(update_heatmap)
        heat_frame = RoundedRectangle(
            width=3.02, height=3.02, corner_radius=0.08,
            stroke_color=GREY, stroke_width=1.2,
        ).move_to(heat_center)
        position_label = ar("الموضع", 18, GREY).move_to([-3.4, -1.96, 0])
        heat_label = ar("درجة الحرارة T(r,t)", 19, YELLOW).move_to([3.4, -1.96, 0])

        self.beat("time_dependent_transport")
        self.play(
            FadeIn(concentration_head), FadeIn(temperature_head),
            Create(graph_axes), FadeIn(x_label), FadeIn(y_label),
            Create(heat_frame), FadeIn(cells), FadeIn(position_label),
            FadeIn(heat_label), Create(profile_area), Create(profile),
            run_time=3.0,
        )
        diffusivity = ar("D: معامل الانتشار", 20, BLUE).move_to([-3.4, -2.45, 0])
        thermal_diffusivity = ar("α: الانتشارية الحرارية", 20, YELLOW).move_to([3.4, -2.45, 0])
        self.play(FadeIn(diffusivity), FadeIn(thermal_diffusivity), run_time=0.9)
        self.play(
            spread.animate.set_value(1), thermal_spread.animate.set_value(1),
            run_time=11.0, rate_func=linear,
        )
        self.wait(1.0)

        self.beat("steady_state_becomes_laplace")
        steady_title = ar("عندما يستقر النظام، تبقى الحرارة أو التركيز عند كل موضع ثابت مع الزمن", 25, GREEN)
        steady_title.move_to([0, 2.2, 0])
        concentration_zero = tex(r"0=D\nabla^2c", 34, BLUE).move_to(concentration_equation)
        temperature_zero = tex(r"0=\alpha\nabla^2T", 34, YELLOW).move_to(temperature_equation)
        self.play(
            FadeOut(diffusivity), FadeOut(thermal_diffusivity),
            FadeOut(concentration_title), FadeOut(temperature_title),
            FadeOut(title), FadeOut(laplace), FadeIn(steady_title),
            TransformMatchingShapes(concentration_equation, concentration_zero),
            TransformMatchingShapes(temperature_equation, temperature_zero),
            run_time=3.0,
        )
        self.wait(2.0)

        concentration_stationary = tex(r"\nabla^2c=0", 34, BLUE).move_to([-3.35, -2.75, 0])
        temperature_stationary = tex(r"\nabla^2T=0", 34, YELLOW).move_to([3.35, -2.75, 0])
        self.play(
            TransformMatchingShapes(concentration_zero, concentration_stationary),
            TransformMatchingShapes(temperature_zero, temperature_stationary),
            Indicate(profile, color=BLUE), Indicate(cells, color=YELLOW),
            run_time=3.0,
        )
        self.wait(2.0)

        self.beat("common_equation")
        body = VGroup(
            ar("التركيز والحرارة والجهد كميات مختلفة, لكن توزيعها يحقق معادلة لابلاس في هذه الحالات", 26, WHITE),
            tex(r"\nabla^2 c=0\quad\nabla^2 T=0\quad\nabla^2 V=0", 38, YELLOW, width=12.4),
            ar("تصف معادلة لابلاس التوزيعات في حالة الاستقرار لكل من درجة الحرارة والتركيز. كما تصف الجهد الكهربائي في منطقة تخلو من الشحنات", 23, BLUE),
        ).arrange(DOWN, buff=0.48).move_to([0, 0.15, 0])
        visuals = VGroup(
            steady_title, concentration_zero, temperature_zero, concentration_stationary, temperature_stationary,
            graph_axes, profile, profile_area, x_label, y_label,
            heat_frame, cells, position_label, heat_label,
        )
        self.play(FadeOut(visuals), FadeIn(body), run_time=2.2)
        self.wait(3.0)
        self.finish()


if __name__ == "__main__":
    run(WhyLaplaceCommon)
