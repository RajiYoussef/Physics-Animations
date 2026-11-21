"""A short, cinematic trailer for the Laplace and Poisson lesson."""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("POISSON_QUALITY", "final")

import numpy as np
from manim import *

from math_type import tex
from settings34 import BLUE, GREEN, GREY, RED, WHITE, YELLOW, run
from support34 import ar, number

RAJI_ARCHIVE = Path(
    r"C:\Users\Bruker\Desktop\Creative softwares\YouTube\Library (zip)\Raji_science_anim_library_v0.3_video_only.zip"
)
if not RAJI_ARCHIVE.is_file():
    raise FileNotFoundError(f"Raji v0.3 library not found: {RAJI_ARCHIVE}")
sys.path.insert(0, f"{RAJI_ARCHIVE.as_posix()}/Raji_science_anim_library")

from raji_sci.core.colormap import diverging_rgb
from raji_sci.em.field_lines import FieldLines
from raji_sci.em.geometry import Charge, coulomb_field
from raji_sci.physics.field_visuals import ScalarFieldImage, field_arrows
from raji_sci.presentation.choreography import emphasize, focus_camera


class LaplacePoissonTrailer90s(MovingCameraScene):
    """Trailer sequence: charge → field → potential → boundaries → numerical grid."""

    def title(self, text):
        heading = ar(text, 30, WHITE).move_to([0, 3.52, 0])
        rule = Line([-6.1, 3.16, 0], [6.1, 3.16, 0], color="#344151", stroke_width=1.3)
        return VGroup(heading, rule)

    def caption(self, text, color=WHITE, size=23):
        label = ar(text, size, color)
        if label.width > 12.0:
            label.scale_to_fit_width(12.0)
        return label.move_to([0, -3.42, 0])

    @staticmethod
    def formula(text, size, color):
        """Unicode math text avoids SVG glyph clipping in long MathText strings."""
        return Text(text, font="Cambria Math", font_size=size, color=color)

    def next_beat(self, heading):
        self.clear()
        frame = self.camera.frame
        if abs(frame.width - 14.222222) > 0.02 or np.linalg.norm(frame.get_center()) > 0.02:
            self.play(frame.animate.move_to(ORIGIN).set(width=14.222222), run_time=0.45)
        self.add(self.title(heading))

    def construct(self):
        self.camera.background_color = "#05080D"

        # 1. Open on lightning, then push in for a quick cinematic hook.
        self.next_beat("من السحابة إلى الجهد الكهربائي")
        cloud = VGroup(
            Circle(radius=0.52, fill_color="#263D50", fill_opacity=1, stroke_width=0).move_to([-1.15, 2.2, 0]),
            Circle(radius=0.68, fill_color="#263D50", fill_opacity=1, stroke_width=0).move_to([-0.45, 2.35, 0]),
            Circle(radius=0.55, fill_color="#263D50", fill_opacity=1, stroke_width=0).move_to([0.27, 2.17, 0]),
            RoundedRectangle(width=2.05, height=0.62, corner_radius=0.25,
                             fill_color="#263D50", fill_opacity=1, stroke_width=0).move_to([-0.45, 2.0, 0]),
        )
        cloud_charge = VGroup(*[
            tex(r"+", 23, RED).move_to(p)
            for p in ([-0.95, 2.25, 0], [-0.42, 2.42, 0], [0.05, 2.24, 0])
        ])
        earth = Rectangle(width=12.4, height=0.95, fill_color="#13251F", fill_opacity=1,
                          stroke_width=0).move_to([0, -3.05, 0])
        ground_line = Line([-6.22, -2.56, 0], [6.22, -2.56, 0], color=GREEN, stroke_width=5)
        ground_label = ar("الأرض", 21, GREEN).move_to([4.9, -2.1, 0])
        lightning = VMobject(color=YELLOW, stroke_width=5).set_points_as_corners(
            [[-0.42, 1.65, 0], [-0.8, 0.92, 0], [-0.2, 0.58, 0], [-0.78, -0.16, 0], [-0.32, -0.52, 0], [-0.62, -2.45, 0]]
        )
        field_hint = VGroup(*[
            Arrow([x, 1.15, 0], [x, -2.35, 0], buff=0, color=BLUE,
                  stroke_width=1.5, max_tip_length_to_length_ratio=0.1).set_opacity(0.52)
            for x in (-4.2, -3.0, -1.7, 0.7, 2.1, 3.5, 4.7)
        ])
        opening_line = self.caption("شحنات السحابة والأرض تُنشئ المجال الكهربائي بينهما.", size=22)
        self.play(FadeIn(cloud), FadeIn(cloud_charge), FadeIn(earth), Create(ground_line), FadeIn(ground_label),
                  FadeIn(opening_line), run_time=1.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in field_hint], lag_ratio=0.08), run_time=1.6)
        self.play(Create(lightning), Flash(lightning.get_end(), color=YELLOW, flash_radius=0.42), run_time=1.1)
        self.play(FadeOut(opening_line), run_time=0.35)
        focus_camera(self, lightning, padding=1.45, run_time=1.0)
        self.wait(2.4)

        # 2. Replace the lightning sketch with a computed dipole field diagram.
        self.next_beat("من الشحنات إلى المجال والجهد")
        positions = np.array([[-1.0, 0.0], [1.0, 0.0]])
        charges = np.array([1.0, -1.0])
        field_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=7.1, y_length=4.55,
            tips=False, axis_config={"color": "#263744", "stroke_width": 1.0, "include_ticks": False},
        ).move_to([-2.45, -0.05, 0])

        field_x = np.linspace(-3, 3, 128)
        field_y = np.linspace(-2, 2, 82)
        field_X, field_Y = np.meshgrid(field_x, field_y)
        potential_values = (
            1 / np.sqrt((field_X + 1) ** 2 + field_Y ** 2 + 0.012)
            - 1 / np.sqrt((field_X - 1) ** 2 + field_Y ** 2 + 0.012)
        )
        potential_map = ScalarFieldImage(
            potential_values, width=7.1, height=4.55,
            center=field_axes.get_center(), cmap=diverging_rgb, vmax=2.8,
            positive="#FFB65C", negative=BLUE, zero="#05080D", opacity=0.88,
        )

        def dipole_field(point):
            p = np.asarray(point, dtype=float)
            if np.min(np.linalg.norm(p - positions, axis=1)) < 0.14:
                return np.zeros(2)
            return coulomb_field(p, positions, charges)

        seeds = [[-1 + 0.19*np.cos(a), 0.19*np.sin(a)]
                 for a in np.linspace(0, 2*np.pi, 14, endpoint=False)]
        lines = FieldLines(field_axes, dipole_field, seeds, step=0.035, steps=250,
                           bounds=[[-3, 3], [-2, 2]], color=BLUE, arrows=True)
        plus = Charge(1, radius=0.19).move_to(field_axes.c2p(-1, 0))
        minus = Charge(-1, radius=0.19).move_to(field_axes.c2p(1, 0))
        samples = np.array([[x, y] for x in (-2.5, -1.8, -0.2, 0.4, 2.0, 2.6)
                            for y in (-1.3, -0.65, 0.65, 1.3)])
        sample_vectors = np.array([dipole_field(p) for p in samples])
        glyphs = field_arrows(
            np.array([field_axes.c2p(*p) for p in samples]), sample_vectors,
            max_length=0.22, color="#9CE8F6", stroke_width=1.4,
        )
        relation = tex(r"\mathbf{E}=-\nabla V", 42, YELLOW).move_to([4.25, 1.05, 0])
        field_note = ar("الأسهم تبيّن اتجاه المجال", 21, BLUE).move_to([4.25, 0.25, 0])
        field_caption = self.caption("اللون يرمز للجهد؛ والأسهم تبيّن اتجاه المجال.", size=22)
        self.play(FadeIn(potential_map), Create(field_axes), FadeIn(plus), FadeIn(minus),
                  FadeIn(field_caption), run_time=1.6)
        self.play(Create(lines), run_time=3.2)
        self.play(FadeIn(glyphs, lag_ratio=0.015), Write(relation), FadeIn(field_note), run_time=1.6)
        emphasize(self, plus, color=YELLOW, run_time=0.8)
        probe_path = Line(field_axes.c2p(-2.5, 0.55), field_axes.c2p(2.5, 0.55),
                          color=YELLOW, stroke_width=1.4).set_opacity(0.65)
        probe = Dot(field_axes.c2p(-2.5, 0.55), radius=0.075, color=YELLOW)
        probe_value = number(0, size=22, color=YELLOW, decimals=2)
        probe_label = VGroup(tex(r"V(P)=", 25, YELLOW), probe_value).arrange(RIGHT, buff=0.12)
        probe_label.move_to([4.25, -0.65, 0])

        def update_probe_value(mob):
            p = field_axes.p2c(probe.get_center())[:2]
            value = np.sum(charges / np.sqrt(np.sum((positions - p) ** 2, axis=1) + 0.012))
            mob.set_value(value)

        probe_value.add_updater(update_probe_value)
        self.play(Create(probe_path), FadeIn(probe_label), FadeIn(probe), run_time=0.7)
        self.play(MoveAlongPath(probe, probe_path, rate_func=linear), run_time=3.3)
        probe_value.clear_updaters()
        self.wait(1.0)

        # 3. Gauss's law and E = -grad V lead to Poisson's equation.
        self.next_beat("من قانون غاوس إلى بواسون")
        gauss = tex(r"\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}", 39, WHITE).move_to([0, 1.45, 0])
        field_def = tex(r"\mathbf{E}=-\nabla V", 37, BLUE).move_to([0, 0.45, 0])
        substitution = tex(r"\nabla\cdot(-\nabla V)=\frac{\rho}{\varepsilon_0}", 35, YELLOW).move_to([0, -0.55, 0])
        laplacian_step = tex(r"-\nabla^2V=\frac{\rho}{\varepsilon_0}", 39, BLUE).move_to([0, -1.3, 0])
        poisson = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 47, RED).move_to([0, -1.85, 0])
        derivation_caption = self.caption("كثافة الشحنة تحدد انحناء الجهد داخل المنطقة.", size=22)
        source_pair = VGroup(Charge(1, 0.15), Charge(-1, 0.15)).arrange(RIGHT, buff=0.34).move_to([0, 2.38, 0])
        self.play(FadeIn(source_pair), Write(gauss), FadeIn(derivation_caption), run_time=1.5)
        self.play(Write(field_def), run_time=1.1)
        self.play(Write(substitution), run_time=1.4)
        self.play(TransformMatchingShapes(substitution, laplacian_step), run_time=1.2)
        self.play(TransformMatchingShapes(laplacian_step, poisson),
                  Indicate(source_pair, color=RED), run_time=1.4)
        self.wait(2.0)

        # 4. With no interior charge, Poisson reduces to Laplace.
        self.next_beat("من بواسون إلى لابلاس")
        region = RoundedRectangle(width=5.4, height=3.45, corner_radius=0.08, stroke_color=GREEN,
                                  stroke_width=2.0, fill_color="#0D1721", fill_opacity=0.88).move_to([-2.65, -0.05, 0])
        boundary_nodes = VGroup(*[
            Dot(p, radius=0.055, color=GREEN)
            for p in [*[[x, 1.675, 0] for x in np.linspace(-5.35, 0.05, 8)],
                      *[[x, -1.775, 0] for x in np.linspace(-5.35, 0.05, 8)],
                      [-5.35, -0.05, 0], [0.05, -0.05, 0]]
        ])
        outside_charge = Charge(1, radius=0.22).move_to([-5.95, 0.2, 0])
        inside_arrows = VGroup(*[
            Arrow([-5.0, y, 0], [-0.35, y, 0], buff=0, color=BLUE, stroke_width=1.7,
                  max_tip_length_to_length_ratio=0.12).set_opacity(0.66)
            for y in (-1.05, -0.35, 0.35, 1.05)
        ])
        zero_rho = tex(r"\rho=0", 34, YELLOW).move_to([1.9, 1.2, 0])
        laplace_eq = tex(r"\nabla^2V=0", 34, WHITE).move_to([1.9, 0.35, 0])
        boundary_note = ar("شحنات الخارج تؤثر داخل المنطقة", 21, WHITE).move_to([1.9, -0.5, 0])
        laplace_caption = self.caption("داخل المنطقة خالٍ من الشحنة؛ والحدود تحدد ما يجري فيها.", size=22)
        self.play(Create(region), FadeIn(boundary_nodes, lag_ratio=0.03), FadeIn(outside_charge),
                  FadeIn(laplace_caption), run_time=1.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in inside_arrows], lag_ratio=0.12),
                  Write(zero_rho), Write(laplace_eq), FadeIn(boundary_note), run_time=2.0)
        self.wait(2.3)

        # 5. An animated one-dimensional plate problem makes V's slope physical.
        self.next_beat("ميل الجهد يكشف المجال بين اللوحين")
        left_plate = Line([-5.25, -1.35, 0], [-5.25, 1.45, 0], color=GREEN, stroke_width=7)
        right_plate = Line([-1.75, -1.35, 0], [-1.75, 1.45, 0], color=BLUE, stroke_width=7)
        labels = VGroup(tex(r"V(0)=0\,\mathrm{V}", 23, GREEN).move_to([-5.0, 1.82, 0]),
                        tex(r"V(L)=6\,\mathrm{V}", 23, BLUE).move_to([-2.0, 1.82, 0]),
                        tex(r"L=3\,\mathrm{m}", 22, WHITE).move_to([-3.5, -1.7, 0]))
        plate_field = VGroup(*[
            Arrow([-1.98, y, 0], [-5.02, y, 0], buff=0, color=YELLOW,
                  stroke_width=2, max_tip_length_to_length_ratio=0.12)
            for y in (-0.8, 0.0, 0.8)
        ])
        axes = Axes(x_range=[0, 3, 1], y_range=[0, 6, 2], x_length=4.65, y_length=2.6,
                    tips=False, axis_config={"color": GREY, "stroke_width": 1.5, "include_ticks": False}).move_to([2.7, -0.15, 0])
        graph = axes.plot(lambda x: 2*x, x_range=[0, 3], color=BLUE, stroke_width=4)
        endpoint_marks = VGroup(Dot(axes.c2p(0, 0), radius=0.075, color=GREEN),
                                Dot(axes.c2p(3, 6), radius=0.075, color=BLUE))
        graph_labels = VGroup(tex(r"x\;(\mathrm{m})", 18, WHITE).next_to(axes.x_axis, DOWN, buff=0.08),
                              tex(r"V\;(\mathrm{V})", 18, WHITE).next_to(axes.y_axis, UP, buff=0.08))
        slope = tex(r"V(x)=\frac{6\,\mathrm{V}}{3\,\mathrm{m}}x,\qquad E_x=-2\,\mathrm{V/m}", 26, YELLOW)
        slope.scale_to_fit_width(6.5).move_to([2.65, -2.55, 0])
        plate_caption = self.caption("ميل الجهد يحدد مقدار المجال واتجاهه.", size=22)
        x_tracker = ValueTracker(0)
        probe = always_redraw(
            lambda: Dot(axes.c2p(x_tracker.get_value(), 2*x_tracker.get_value()),
                        radius=0.09, color=YELLOW)
        )
        guide = always_redraw(
            lambda: DashedLine(axes.c2p(x_tracker.get_value(), 0),
                               axes.c2p(x_tracker.get_value(), 2*x_tracker.get_value()),
                               color=YELLOW, stroke_width=1.6, dash_length=0.07)
        )
        self.play(Create(left_plate), Create(right_plate), FadeIn(labels),
                  LaggedStart(*[GrowArrow(a) for a in plate_field], lag_ratio=0.16),
                  Create(axes), FadeIn(graph_labels), FadeIn(plate_caption), run_time=2.1)
        self.play(Create(graph), FadeIn(endpoint_marks), Write(slope), run_time=1.8)
        self.add(probe, guide)
        self.play(x_tracker.animate.set_value(3), run_time=3.4, rate_func=linear)
        self.play(Indicate(plate_field, color=YELLOW), run_time=0.8)
        self.wait(2.2)

        # 6. Tease the difference between initial data and spatial boundary data.
        self.next_beat("بيانات عند لحظة، أم على حدود المكان؟")
        divider = Line([0, -1.85, 0], [0, 2.35, 0], color="#344151", stroke_width=1.4)
        motion_title = ar("مسألة حركة", 24, BLUE).move_to([-3.2, 2.45, 0])
        motion_axes = Axes(x_range=[0, 2, 1], y_range=[0, 4, 2], x_length=4.4, y_length=2.15,
                           tips=False, axis_config={"color": GREY, "stroke_width": 1.4, "include_ticks": False}).move_to([-3.15, 0.55, 0])
        motion_graph = motion_axes.plot(lambda t: 2*t, x_range=[0, 2], color=BLUE, stroke_width=3.5)
        initial_dot = Dot(motion_axes.c2p(0, 0), radius=0.085, color=YELLOW)
        initial_data = tex(r"s(t_0),\quad \dot s(t_0)", 27, BLUE).move_to([-3.15, -1.15, 0])
        potential_title = ar("جهد بين لوحين", 24, GREEN).move_to([3.15, 2.45, 0])
        potential_axes = Axes(x_range=[0, 3, 1], y_range=[0, 6, 2], x_length=4.4, y_length=2.15,
                              tips=False, axis_config={"color": GREY, "stroke_width": 1.4, "include_ticks": False}).move_to([3.15, 0.55, 0])
        potential_graph = potential_axes.plot(lambda x: 2*x, x_range=[0, 3], color=GREEN, stroke_width=3.5)
        endpoint_dots = VGroup(Dot(potential_axes.c2p(0, 0), radius=0.08, color=GREEN),
                               Dot(potential_axes.c2p(3, 6), radius=0.08, color=GREEN))
        boundary_data = tex(r"V(0),\quad V(L)", 27, GREEN).move_to([3.15, -1.15, 0])
        comparison_caption = self.caption("في الحركة نحدد الحالة عند البداية؛ وفي الجهد نحدد القيم على الحدود.", size=21)
        self.play(Create(divider), FadeIn(motion_title), FadeIn(potential_title),
                  Create(motion_axes), Create(potential_axes), FadeIn(comparison_caption), run_time=1.6)
        self.play(Create(motion_graph), FadeIn(initial_dot), Write(initial_data),
                  Create(potential_graph), FadeIn(endpoint_dots), Write(boundary_data), run_time=2.1)
        velocity_arrow = Arrow(motion_axes.c2p(0.12, 0.24), motion_axes.c2p(0.72, 1.44),
                               buff=0, color=YELLOW, stroke_width=2.2,
                               max_tip_length_to_length_ratio=0.16)
        self.play(GrowArrow(velocity_arrow), run_time=0.8)
        self.play(MoveAlongPath(initial_dot, motion_graph, rate_func=linear), run_time=2.2)
        self.wait(2.2)

        # 7. Heat and concentration spread, then settle into Laplace's equation.
        self.next_beat("الحرارة والانتشار يقودان إلى لابلاس")
        coord = np.linspace(-1, 1, 64)
        X, Y = np.meshgrid(coord, coord)
        sigma = ValueTracker(0.24)

        def heat_values(width):
            return np.exp(-(X*X + Y*Y) / (2*width*width)) / (width*width)

        heat_map = ScalarFieldImage(heat_values(sigma.get_value()), width=3.6, height=3.6,
                                    center=[-3.25, 0.0, 0], cmap=diverging_rgb,
                                    vmax=12, positive="#FFB65C", negative=BLUE, zero="#101722")
        heat_map.add_updater(lambda m: m.update_values(heat_values(sigma.get_value())))
        heat_frame = Square(side_length=3.6, stroke_color="#536372", stroke_width=1.4).move_to(heat_map)
        heat_label = ar("حرارة تنتشر", 21, YELLOW).move_to([-3.25, -2.05, 0])
        diffusion = tex(r"\frac{\partial T}{\partial t}=\alpha\nabla^2T", 29, YELLOW).move_to([2.75, 1.35, 0])
        steady_label = ar("حين يستقر التوزيع", 21, WHITE).move_to([2.75, 0.35, 0])
        steady_eq = tex(r"\frac{\partial T}{\partial t}=0\quad\Longrightarrow\quad\nabla^2T=0", 27, BLUE)
        steady_eq.scale_to_fit_width(6.0).move_to([2.75, -0.55, 0])
        concentration = tex(r"\nabla^2c=0", 32, GREEN).move_to([2.75, -1.45, 0])
        heat_caption = self.caption("مع الزمن تنتشر الحرارة؛ وعند الاستقرار يثبت توزيعها.", size=21)
        self.play(FadeIn(heat_frame), FadeIn(heat_map), FadeIn(heat_label), Write(diffusion),
                  FadeIn(heat_caption), run_time=1.7)
        self.play(sigma.animate.set_value(0.73), run_time=4.8, rate_func=smooth)
        heat_map.clear_updaters()
        self.play(FadeIn(steady_label), Write(steady_eq), Write(concentration), run_time=1.8)
        self.wait(2.4)

        # 8. Fixed boundary data, uniqueness, and the two named boundary types.
        self.next_beat("لماذا يكون الحل وحيداً؟")
        domain = RoundedRectangle(width=4.0, height=3.25, corner_radius=0.06, stroke_color=GREEN,
                                  stroke_width=2.1, fill_color="#0D1721", fill_opacity=0.82).move_to([-3.15, 0.15, 0])
        rim = VGroup(*[
            Dot(p, radius=0.055, color=GREEN)
            for p in [*[[x, 1.775, 0] for x in np.linspace(-5.15, -1.15, 7)],
                      *[[x, -1.475, 0] for x in np.linspace(-5.15, -1.15, 7)],
                      [-5.15, 0.15, 0], [-1.15, 0.15, 0]]
        ])
        interior = VGroup(*[
            Dot([-4.4 + i*0.62, -0.8 + j*0.62, 0], radius=0.045, color="#71879A")
            for i in range(5) for j in range(4)
        ])
        selected = Dot([-3.15, 0.15, 0], radius=0.105, color=YELLOW)
        prescribed = self.formula("V₁|S = V₂|S", 29, WHITE).move_to([2.0, 1.45, 0])
        difference = self.formula("W = V₁ − V₂", 30, YELLOW).move_to([2.0, 0.7, 0])
        zero_boundary_difference = self.formula("W|S = 0", 27, BLUE).move_to([2.0, 0.0, 0])
        uniqueness = self.formula("∇²W = 0  ⟹  W = 0", 27, BLUE)
        uniqueness.scale_to_fit_width(4.7).move_to([2.0, -0.55, 0])
        same_solution = self.formula("V₁ = V₂", 36, GREEN).move_to([2.0, -1.15, 0])
        bc_types = VGroup(ar("ديريشليه: قيمة الجهد", 18, GREEN),
                          ar("نيومان: مشتقته العمودية", 18, BLUE)).arrange(DOWN, buff=0.12)
        bc_types.move_to([2.0, -2.18, 0])
        normal = Arrow([-1.65, 0.25, 0], [-1.05, 0.25, 0], buff=0, color=BLUE, stroke_width=2)
        boundary_caption = self.caption("مع المصدر والحدود نفسيهما، لا نحصل على حلّين مختلفين.", size=21)
        self.play(Create(domain), FadeIn(rim, lag_ratio=0.025), FadeIn(interior, lag_ratio=0.02),
                  FadeIn(boundary_caption), run_time=1.7)
        self.play(GrowArrow(normal), FadeIn(selected), Write(prescribed), Write(difference), run_time=1.5)
        self.play(Write(zero_boundary_difference), Write(uniqueness),
                  Write(same_solution), FadeIn(bc_types), run_time=2.0)
        emphasize(self, selected, color=YELLOW, run_time=0.65)
        self.play(Indicate(same_solution, color=GREEN), run_time=0.8)
        self.wait(2.3)

        # 9. Turn the continuous region into a lattice and close with a clear CTA.
        self.next_beat("من المعادلة إلى شبكة حسابية")
        grid_center = np.array([-3.2, 0.12, 0])
        grid_width = 4.2
        grid_frame = Square(side_length=grid_width, stroke_color=BLUE, stroke_width=2.0).move_to(grid_center)
        grid_lines = VGroup()
        step = grid_width / 6
        for k in range(1, 6):
            offset = -grid_width/2 + k*step
            grid_lines.add(Line(grid_center + np.array([offset, -grid_width/2, 0]),
                                grid_center + np.array([offset, grid_width/2, 0]),
                                color="#344151", stroke_width=0.85))
            grid_lines.add(Line(grid_center + np.array([-grid_width/2, offset, 0]),
                                grid_center + np.array([grid_width/2, offset, 0]),
                                color="#344151", stroke_width=0.85))
        lattice = VGroup(*[
            Dot(grid_center + np.array([-grid_width/2 + i*step, -grid_width/2 + j*step, 0]),
                radius=0.055,
                color=GREEN if i == 0 and j not in (0, 6) else
                BLUE if i in (0, 6) or j in (0, 6) else "#A7B8C7")
            for i in range(7) for j in range(7)
        ])
        focus = lattice[3*7 + 3]
        neighbor_keys = (3*7 + 2, 3*7 + 4, 2*7 + 3, 4*7 + 3)
        neighbor_glow = VGroup(*[Circle(radius=0.13, color=BLUE, stroke_width=2).move_to(lattice[k])
                                 for k in neighbor_keys])
        focus.set_color(YELLOW).scale(1.45)
        coords = self.formula("xᵢ = i h,   yⱼ = j h", 27, YELLOW).move_to([2.8, 1.35, 0])
        laplace_grid_eq = self.formula("∇²V = 0", 30, WHITE).move_to([2.8, 0.8, 0])
        poisson_grid_eq = self.formula("∇²V = −ρ/ε₀", 28, WHITE).move_to([2.8, 0.2, 0])
        stencil_label = ar("في حالة لابلاس", 19, BLUE).move_to([2.8, -0.35, 0])
        stencil = self.formula("Vᵢⱼ ≈ (Vᵢ₊₁,ⱼ + Vᵢ₋₁,ⱼ + Vᵢ,ⱼ₊₁ + Vᵢ,ⱼ₋₁)/4",
                               22, YELLOW).move_to([2.8, -0.85, 0])
        finite_difference = ar("الجهد عند كل نقطة يوازن قيم جيرانها", 19, WHITE).move_to([2.8, -1.45, 0])
        value_label = tex(r"V_{i,j}", 25, YELLOW).next_to(focus, DOWN, buff=0.13)
        grid_caption = self.caption("نثبّت الجهد على الحدود، ثم نحدّث قيم الداخل.", size=22)
        self.play(Create(grid_frame), Create(grid_lines), FadeIn(grid_caption), run_time=1.4)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in lattice], lag_ratio=0.008), run_time=2.4)
        neighbor_arrows = VGroup(*[
            Arrow(focus.get_center(), lattice[k].get_center(), buff=0.12, color=BLUE,
                  stroke_width=1.8, max_tip_length_to_length_ratio=0.18)
            for k in neighbor_keys
        ])
        self.play(FadeIn(neighbor_glow), FadeIn(value_label), Write(coords),
                  Write(laplace_grid_eq), Write(poisson_grid_eq), run_time=1.7)
        self.play(LaggedStart(*[GrowArrow(a) for a in neighbor_arrows], lag_ratio=0.12),
                  FadeIn(stencil_label), Write(stencil), FadeIn(finite_difference), run_time=2.4)
        boundary_values = np.zeros((7, 7), dtype=float)
        boundary_values[0, 1:6] = 1.0
        snapshots = [boundary_values.copy()]
        for _ in range(10):
            next_values = snapshots[-1].copy()
            current_values = snapshots[-1]
            next_values[1:6, 1:6] = 0.25 * (
                current_values[0:5, 1:6] + current_values[2:7, 1:6]
                + current_values[1:6, 0:5] + current_values[1:6, 2:7]
            )
            snapshots.append(next_values)
        for values in snapshots[1:]:
            color_changes = []
            for i in range(1, 6):
                for j in range(1, 6):
                    if (i, j) != (3, 3):
                        index = i * 7 + j
                        color = interpolate_color(ManimColor("#66798B"), ManimColor("#FFB65C"),
                                                  float(values[i, j]))
                        color_changes.append(lattice[index].animate.set_color(color))
            self.play(*color_changes, run_time=0.4, rate_func=linear)
        self.play(FadeOut(grid_caption), FadeIn(ar("شاهد الدرس الكامل", 32, WHITE).move_to([2.8, -2.15, 0])),
                  FadeIn(ar("معادلتَا لابلاس وبواسون", 26, YELLOW).move_to([2.8, -2.7, 0])), run_time=1.2)
        self.wait(2.8)


if __name__ == "__main__":
    run(LaplacePoissonTrailer90s)
