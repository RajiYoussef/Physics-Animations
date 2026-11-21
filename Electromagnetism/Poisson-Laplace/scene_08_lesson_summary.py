"""Animated chapter recap for the Laplace and Poisson lesson."""

import os
os.environ.setdefault("POISSON_QUALITY", "final")

import numpy as np
from manim import *

from math_type import tex
from settings34 import BLUE, GREEN, GREY, RED, WHITE, YELLOW, run
from support34 import LessonScene, ar


class LessonSummary(LessonScene):
    def construct(self):
        self.camera.background_color = "#05080D"

        def header():
            title = ar("باختصار ", 30, WHITE).move_to([0, 3.55, 0])
            line = Line([-6.1, 3.18, 0], [6.1, 3.18, 0], color="#344151", stroke_width=1.2)
            return VGroup(title, line)

        def caption(text, color=WHITE):
            label = ar(text, 23, color)
            if label.width > 12.0:
                label.scale_to_fit_width(12.0)
            return label.move_to([0, -3.42, 0])

        def reset_scene():
            self.clear()
            self.add(header())

        # Charge, field, and potential are linked by Gauss's law and E = -grad V.
        self.beat("charge_to_potential")
        reset_scene()
        cloud = VGroup(
            *[Circle(radius=r, stroke_width=0, fill_color="#27394A", fill_opacity=0.95)
              for r in (0.62, 0.78, 0.58)]
        )
        cloud[0].move_to([-2.25, 1.65, 0])
        cloud[1].move_to([-1.65, 1.8, 0])
        cloud[2].move_to([-1.08, 1.62, 0])
        cloud.add(RoundedRectangle(width=1.9, height=0.62, corner_radius=0.24,
                                   stroke_width=0, fill_color="#27394A", fill_opacity=0.95)
                  .move_to([-1.68, 1.47, 0]))
        charges = VGroup(*[
            tex(r"+", 25, RED).move_to(p)
            for p in ([-2.1, 1.72, 0], [-1.62, 1.9, 0], [-1.22, 1.68, 0])
        ])
        ground = Line([-4.4, -1.55, 0], [1.0, -1.55, 0], color=GREEN, stroke_width=5)
        earth = VGroup(Rectangle(width=5.4, height=0.72, stroke_width=0,
                                 fill_color="#14251F", fill_opacity=0.95)
                       .move_to([-1.7, -1.92, 0]), ground)
        field_arrows = VGroup(*[
            Arrow([-3.65 + k * 0.78, 0.92, 0], [-3.65 + k * 0.78, -1.35, 0],
                  buff=0, color=BLUE, stroke_width=2, max_tip_length_to_length_ratio=0.12)
            for k in range(6)
        ])
        strike = VMobject(color=YELLOW, stroke_width=4).set_points_as_corners(
            [[-1.4, 1.1, 0], [-1.72, 0.55, 0], [-1.38, 0.28, 0], [-1.86, -0.42, 0], [-1.57, -0.74, 0]]
        )
        charge_label = ar("تولِد الشحنات مجالا كهربائيا", 22, BLUE).move_to([3.2, 1.28, 0])
        field_eq = tex(r"\mathbf{E}=-\nabla V", 37, YELLOW).move_to([3.25, 0.34, 0])
        gauss = tex(r"\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}", 34, WHITE).move_to([3.25, -0.55, 0])
        poisson = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 38, RED).move_to([3.25, -1.58, 0])
        cap = caption("من خلال توزيع الشحنات، يمكننا التوصل إلى الجهد  عبر المجال الكهربائي")
        self.play(FadeIn(cloud), FadeIn(charges), FadeIn(earth), run_time=1.3)
        self.play(LaggedStart(*[GrowArrow(a) for a in field_arrows], lag_ratio=0.1),
                  Create(strike), run_time=2.0)
        self.play(FadeIn(charge_label), Write(field_eq), Write(gauss), Write(poisson), FadeIn(cap), run_time=2.6)
        self.wait(4.5)

        # Removing interior charge gives Laplace; boundary values select the profile.
        self.beat("laplace_and_plate_example")
        reset_scene()
        plate_left = Line([-4.1, -1.35, 0], [-4.1, 1.5, 0], color=GREEN, stroke_width=6)
        plate_right = Line([-0.8, -1.35, 0], [-0.8, 1.5, 0], color=BLUE, stroke_width=6)
        plate_labels = VGroup(tex(r"V(0)=0", 25, GREEN).next_to(plate_left, UP, buff=0.18),
                              tex(r"V(L)=6\,\mathrm{V}", 25, BLUE).next_to(plate_right, UP, buff=0.18),
                              tex(r"L=3\,\mathrm{m}", 24, WHITE).move_to([-2.45, -1.7, 0]))
        no_charge = tex(r"\rho=0\quad\Longrightarrow\quad\nabla^2V=0", 36, YELLOW).move_to([2.9, 1.55, 0])
        axes = Axes(x_range=[0, 3, 1], y_range=[0, 6, 2], x_length=4.8, y_length=2.8,
                    tips=False, axis_config={"color": GREY, "stroke_width": 1.7, "include_ticks": False})
        axes.move_to([2.25, -0.62, 0])
        axes_labels = VGroup(tex(r"x\;(\mathrm{m})", 20, WHITE).next_to(axes.x_axis, DOWN, buff=0.12),
                             tex(r"V\;(\mathrm{V})", 20, WHITE).next_to(axes.y_axis, UP, buff=0.08))
        line_graph = axes.plot(lambda x: 2 * x, x_range=[0, 3], color=BLUE, stroke_width=4)
        points = VGroup(*[Dot(axes.c2p(x, 2*x), radius=0.07, color=YELLOW) for x in (0, 1, 2, 3)])
        slope = tex(r"V(x)=(2\,\mathrm{V/m})x,\quad E_x=-2\,\mathrm{V/m}", 24, YELLOW)
        slope.scale_to_fit_width(6.6).move_to([2.55, -2.82, 0])
        field_arrow = Arrow([-1.25, 0.35, 0], [-3.65, 0.35, 0], buff=0, color=YELLOW, stroke_width=3)
        cap = caption("في مثال اللوحين، تحدِد قيم الجهد المعطاة عند الحدّين شكل منحنى الجهد الذي يأخذ هيئة خط مستقيم وميل هذا الخط")
        self.play(Create(plate_left), Create(plate_right), FadeIn(plate_labels), GrowArrow(field_arrow),
                  Write(no_charge), Create(axes), FadeIn(axes_labels), FadeIn(cap), run_time=2.4)
        self.play(Create(line_graph), LaggedStart(*[GrowFromCenter(p) for p in points], lag_ratio=0.2),
                  Write(slope), run_time=2.2)
        self.play(Indicate(plate_left, color=GREEN), Indicate(plate_right, color=BLUE),
                  Indicate(field_arrow, color=YELLOW), run_time=1.2)
        self.wait(4.8)

        # Contrast initial data in time with boundary data in space.
        self.beat("initial_vs_boundary_data")
        reset_scene()
        motion_title = ar("حركة جسم", 24, BLUE).move_to([-3.1, 2.48, 0])
        motion_axes = Axes(x_range=[0, 2, 1], y_range=[0, 4, 2], x_length=4.5, y_length=2.0,
                           tips=False, axis_config={"color": GREY, "stroke_width": 1.6, "include_ticks": False})
        motion_axes.move_to([-3.0, 0.7, 0])
        motion_line = motion_axes.plot(lambda t: 2*t, x_range=[0, 2], color=BLUE, stroke_width=4)
        motion_dot = Dot(motion_axes.c2p(0, 0), color=YELLOW, radius=0.09)
        motion_labels = VGroup(tex(r"t", 21).next_to(motion_axes.x_axis, DOWN, buff=0.1),
                               tex(r"s", 21).next_to(motion_axes.y_axis, UP, buff=0.08),
                               tex(r"s(t_0),\;v(t_0)", 24, BLUE).move_to([-3.0, -0.72, 0]))
        potential_title = ar("جهد بين لوحين", 24, GREEN).move_to([3.1, 2.48, 0])
        pot_axes = Axes(x_range=[0, 3, 1], y_range=[0, 6, 2], x_length=4.5, y_length=2.0,
                        tips=False, axis_config={"color": GREY, "stroke_width": 1.6, "include_ticks": False})
        pot_axes.move_to([3.0, 0.7, 0])
        pot_line = pot_axes.plot(lambda x: 2*x, x_range=[0, 3], color=GREEN, stroke_width=4)
        endpoint_dots = VGroup(Dot(pot_axes.c2p(0, 0), color=YELLOW, radius=0.08),
                               Dot(pot_axes.c2p(3, 6), color=YELLOW, radius=0.08))
        pot_labels = VGroup(tex(r"x", 21).next_to(pot_axes.x_axis, DOWN, buff=0.1),
                            tex(r"V(0),\;V(L)", 24, GREEN).move_to([3.0, -0.72, 0]))
        separator = Line([0, -0.65, 0], [0, 2.45, 0], color="#344151", stroke_width=1.2)
        formula_motion = tex(r"\frac{d^2s}{dt^2}=0", 30, BLUE).move_to([-3.0, -1.55, 0])
        formula_pot = tex(r"\frac{d^2V}{dx^2}=0", 30, GREEN).move_to([3.0, -1.55, 0])
        cap = caption("في الحركة نبدأ من حالة ابتدائية وفي الجهد نثبت القيم على الحدود")
        self.play(FadeIn(motion_title), FadeIn(potential_title), Create(separator),
                  Create(motion_axes), Create(pot_axes), run_time=1.4)
        self.play(Create(motion_line), FadeIn(motion_dot), Create(pot_line), FadeIn(endpoint_dots), FadeIn(motion_labels),
                  FadeIn(pot_labels), Write(formula_motion), Write(formula_pot), FadeIn(cap), run_time=2.3)
        self.play(MoveAlongPath(motion_dot, motion_line, rate_func=linear), run_time=2.0)
        self.wait(4.0)

        # The same stationary equation appears in heat and diffusion.
        self.beat("steady_state_connections")
        reset_scene()
        heat = VGroup(*[
            Square(side_length=0.42, stroke_color="#344151", stroke_width=0.7,
                   fill_color=interpolate_color(ManimColor("#172A3B"), ManimColor("#F3A64A"),
                                                float(np.exp(-((i-2)**2+(j-2)**2)/3.0))), fill_opacity=1)
            .move_to([-3.5 + (i-2)*0.44, 0.35 + (j-2)*0.44, 0])
            for i in range(5) for j in range(5)
        ])
        heat_frame = Rectangle(width=2.28, height=2.28, stroke_color=GREY, stroke_width=1.2).move_to(heat)
        heat_label = ar("حرارة T", 22, YELLOW).move_to([-3.5, -1.1, 0])
        diffusion_axes = Axes(x_range=[-3, 3, 1], y_range=[0, 1, 0.25], x_length=4.6, y_length=2.15,
                              tips=False, axis_config={"color": GREY, "stroke_width": 1.5, "include_ticks": False})
        diffusion_axes.move_to([2.8, 0.35, 0])
        profile = diffusion_axes.plot(lambda x: 0.85*np.exp(-x*x/1.5), x_range=[-3,3], color=BLUE, stroke_width=4)
        profile2 = diffusion_axes.plot(lambda x: 0.48*np.exp(-x*x/5.0), x_range=[-3,3], color=BLUE,
                                       stroke_width=3, stroke_opacity=0.65)
        diffusion_label = ar("تركيز c", 22, BLUE).move_to([2.8, -1.1, 0])
        eqs = VGroup(tex(r"\frac{\partial T}{\partial t}=\alpha\nabla^2T", 28, YELLOW),
                     tex(r"\frac{\partial c}{\partial t}=D\nabla^2c", 28, BLUE)).arrange(DOWN, buff=0.3).move_to([0, -2.12, 0])
        steady_label = ar("في الحالة المستقرة", 22, WHITE).move_to([0, 2.35, 0])
        steady_equation = tex(r"\nabla^2T=0,\qquad\nabla^2c=0", 32, WHITE).move_to([0, 1.86, 0])
        cap = caption("في الحرارة والانتشار، يقود الاستقرار إلى معادلة لابلاس.")
        self.play(FadeIn(heat_frame), FadeIn(heat), FadeIn(heat_label), Create(diffusion_axes),
                  Create(profile), FadeIn(diffusion_label), Write(eqs), FadeIn(cap), run_time=2.4)
        self.play(Create(profile2), FadeIn(steady_label), Write(steady_equation),
                  Indicate(heat, color=YELLOW), run_time=2.2)
        self.wait(4.5)

        # Fixed boundary data and a maximum-principle sketch explain uniqueness.
        self.beat("boundary_data_and_uniqueness")
        reset_scene()
        region = RoundedRectangle(width=4.2, height=2.8, corner_radius=0.08, stroke_color=GREEN,
                                  stroke_width=2.2, fill_color="#10202B", fill_opacity=0.75).move_to([-2.8, 0.35, 0])
        boundary = VGroup(*[Dot(p, radius=0.055, color=GREEN) for p in
                            [*[[x, 1.75, 0] for x in np.linspace(-4.8,-0.8,7)],
                             *[[x, -1.05, 0] for x in np.linspace(-4.8,-0.8,7)],
                             [-4.9,0.35,0],[-0.7,0.35,0]]])
        interior1 = Ellipse(width=2.6, height=0.8, color=BLUE, stroke_width=3).move_to([-2.8, 0.48, 0])
        interior2 = Ellipse(width=2.0, height=1.15, color=YELLOW, stroke_width=2.5).move_to([-2.8, 0.2, 0])
        domain_label = ar("شكلان مفترضان للجهد", 20, GREEN).move_to([-2.8, -1.65, 0])
        same = tex(r"V_1|_S=V_2|_S", 28, WHITE).move_to([2.7, 1.2, 0])
        difference = tex(r"W=V_1-V_2", 30, YELLOW).move_to([2.7, 0.35, 0])
        zero_diff = tex(r"\nabla^2W=0,\quad W|_S=0", 29, BLUE).move_to([2.7, -0.48, 0])
        unique = tex(r"W=0\;\Longrightarrow\;V_1=V_2", 31, GREEN).move_to([2.7, -1.2, 0])
        maximum_principle = ar("مبدأ القيمة العظمى", 19, WHITE).move_to([2.7, -1.85, 0])
        type_labels = VGroup(ar("ديريشليه: قيمة الجهد", 18, GREEN), ar("نيومان: مشتقة عمودية", 18, BLUE))
        type_labels.arrange(DOWN, buff=0.14).move_to([2.7, -2.55, 0])
        cap = caption("إذا تطابقت الشحنة والحدود، فلا يبقى حلّان مختلفان")
        self.play(Create(region), FadeIn(boundary, lag_ratio=0.04), Create(interior1), Create(interior2),
                  FadeIn(domain_label), FadeIn(cap), run_time=2.0)
        self.play(Write(same), Write(difference), Write(zero_diff), Write(unique),
                  FadeIn(maximum_principle), FadeIn(type_labels), run_time=2.4)
        self.play(Transform(interior2, interior1.copy()), Indicate(unique, color=GREEN), run_time=1.4)
        self.wait(4.5)

        # Numerical work starts by replacing a continuous region with lattice sites.
        self.beat("numerical_grid_and_close")
        reset_scene()
        frame = Square(side_length=3.2, stroke_color=BLUE, stroke_width=2).move_to([-2.35, 0.25, 0])
        grid = VGroup()
        for k in range(1, 6):
            pos = -1.6 + k*(3.2/6)
            grid.add(Line([-3.95+pos, -1.35, 0], [-3.95+pos, 1.85, 0], color="#344151", stroke_width=0.85))
            grid.add(Line([-3.95, -1.35+pos, 0], [-0.75, -1.35+pos, 0], color="#344151", stroke_width=0.85))
        lattice = VGroup(*[
            Dot([-3.95+i*(3.2/6), -1.35+j*(3.2/6), 0], radius=0.045,
                color=GREEN if i in (0,6) or j in (0,6) else "#A5B7C8")
            for i in range(7) for j in range(7)
        ])
        selected = Dot([-3.95+3*(3.2/6), -1.35+3*(3.2/6), 0], radius=0.09, color=YELLOW)
        grid_title = ar("منطقة مستمرة", 20, GREY).move_to([-2.35, 2.05, 0])
        lattice_eq = tex(r"(x_i,y_j)=(i\Delta x,j\Delta y)", 28, YELLOW).move_to([2.85, 1.45, 0])
        laplace_eq = tex(r"\nabla^2V=0", 34, BLUE).move_to([2.85, 0.55, 0])
        poisson_eq = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 34, RED).move_to([2.85, -0.25, 0])
        grid_note = ar("قيم الحدود معلومة؛ ونحسب الجهد عند نقاط الداخل", 20, WHITE).move_to([2.85, -1.25, 0])
        close = ar("من الشحنة، إلى الجهد، إلى حلٍّ تحدده الحدود.", 27, YELLOW).move_to([0, -2.45, 0])
        cap = caption("وعندما يصعب الحل المباشر، تبدأ الطريقة العددية بشبكة النقاط.")
        self.play(Create(frame), FadeIn(grid_title), FadeIn(cap), run_time=1.0)
        self.play(Create(grid), LaggedStart(*[GrowFromCenter(d) for d in lattice], lag_ratio=0.006), run_time=3.3)
        self.play(Indicate(selected, color=YELLOW), Write(lattice_eq), Write(laplace_eq), Write(poisson_eq),
                  FadeIn(grid_note), run_time=2.0)
        self.play(FadeIn(close), run_time=1.0)
        self.wait(4.5)
        self.finish()


if __name__ == "__main__":
    run(LessonSummary)
