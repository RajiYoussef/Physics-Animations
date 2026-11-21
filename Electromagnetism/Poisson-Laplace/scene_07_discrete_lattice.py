"""Scene 7: introduce the discrete lattice used by finite differences."""
from pathlib import Path
import os
import sys

import numpy as np
from manim import *

os.environ.setdefault("POISSON_QUALITY", "final")

from settings34 import BLUE, GREEN, GREY, WHITE, YELLOW, run

RAJI_ARCHIVE = Path(r"C:\Users\Bruker\Desktop\Creative softwares\YouTube\Library (zip)\Raji_science_anim_library_v0.3_video_only.zip")
if not RAJI_ARCHIVE.is_file():
    raise FileNotFoundError(f"Raji science animation library not found: {RAJI_ARCHIVE}")
sys.path.insert(0, f"{RAJI_ARCHIVE.as_posix()}/Raji_science_anim_library")

from raji_sci.presentation.choreography import emphasize
from raji_sci.presentation.layout import fit_inside
from math_type import tex
from support34 import LessonScene, ar


class DiscreteLattice(LessonScene):
    def construct(self):
        title = ar("لحل المسألة عدديا، نمثل المنطقة بشبكة محدودة ونحسب الجهد عند نقاط هذه الشبكة", 29, BLUE)
        fit_inside(title, 12.4, 0.48, padding=0.02).move_to([0, 3.55, 0])
        rule = Line([-6.15, 3.18, 0], [6.15, 3.18, 0], color="#344151", stroke_width=1.3)
        self.add(title, rule)

        def caption(text, color=WHITE):
            label = ar(text, 23, color)
            fit_inside(label, 12.3, 0.55, padding=0.02)
            return label.move_to([0, -3.48, 0])

        self.beat("why_numerical_grid")
        cap = caption("في بعدين أو ثلاثة أبعاد، قد يكون من الصعب التوصل إلى حل تحليلي في حال غياب التناظر")
        region_center = np.array([-3.55, -0.1, 0])
        region = Rectangle(width=3.65, height=3.65, stroke_color=BLUE, stroke_width=2.0,
                           fill_color="#102332", fill_opacity=0.75).move_to(region_center)
        continuous_layers = VGroup(*[
            Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=opacity)
            .move_to(region_center + RIGHT * 0.22 + UP * 0.05)
            for r, opacity in ((1.25, 0.045), (0.92, 0.07), (0.58, 0.11))
        ])
        question = VGroup(
            ar("نبدأ من منطقة مستمرة", 24, WHITE),
            ar("ثم نختار طريقة عددية", 23, YELLOW),
        ).arrange(DOWN, buff=0.42).move_to([2.7, 0.45, 0])
        fit_inside(question, 5.0, 1.25, padding=0.03)
        self.play(Create(region), FadeIn(continuous_layers), FadeIn(question), FadeIn(cap), run_time=2.0)
        self.wait(6.0)

        self.play(FadeOut(cap), run_time=0.35)
        self.beat("continuous_region_to_lattice")
        cap = caption("نحوّل المنطقة إلى نقاط محددة، ونبقي الحد معروفاً.")
        grid_lines = VGroup()
        for k in range(1, 7):
            offset = -1.825 + k * (3.65 / 7)
            grid_lines.add(Line([region_center[0] + offset, -1.925, 0],
                                [region_center[0] + offset, 1.725, 0],
                                color="#30404E", stroke_width=0.8))
            grid_lines.add(Line([-5.375, region_center[1] + offset, 0],
                                [-1.725, region_center[1] + offset, 0],
                                color="#30404E", stroke_width=0.8))

        spacing = 0.455
        nodes = {}
        dots = VGroup()
        for j in range(7):
            for i in range(7):
                is_boundary = i in (0, 6) or j in (0, 6)
                point = np.array([region_center[0] - 3 * spacing + i * spacing,
                                  region_center[1] - 3 * spacing + j * spacing, 0])
                dot = Dot(point, radius=0.052 if is_boundary else 0.044,
                          color=GREEN if is_boundary else "#A5B7C8")
                nodes[(i, j)] = {"point": point, "dot": dot, "boundary": is_boundary}
                dots.add(dot)
        self.play(FadeOut(continuous_layers), FadeOut(question), Create(grid_lines), run_time=1.7)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.018),
                  run_time=4.2)
        self.play(FadeOut(grid_lines), run_time=0.55)
        self.wait(2.2)

        self.play(FadeOut(cap), run_time=0.35)
        self.beat("coordinates_and_spacing")
        cap = caption('\u202B\u2066Δx\u2069 و\u2066Δy\u2069 تحددان المسافة بين مواضع الشبكة\u202C')
        known_label = ar("قيم معلومة على الحد", 21, GREEN).move_to([2.65, 0.55, 0])
        unknown_label = ar("قيم الجهد في الداخل نبحث عنها", 20, "#A5B7C8").move_to([2.65, -0.25, 0])
        known_dot = Dot([0, 0, 0], radius=0.07, color=GREEN).move_to([0.25, 0.55, 0])
        unknown_dot = Dot([0, 0, 0], radius=0.07, color="#A5B7C8").move_to([0.25, -0.25, 0])
        coord_title = ar("إحداثيات النقطة (i,j)", 21, WHITE).move_to([2.75, 1.75, 0])
        coordinate = tex(r"(x_i,y_j)=(i\Delta x,j\Delta y)", 28, YELLOW).move_to([2.75, 1.18, 0])
        fit_inside(coordinate, 5.6, 0.55, padding=0.02)

        dx_left = nodes[(2, 6)]["point"] + UP * 0.25
        dx_right = nodes[(3, 6)]["point"] + UP * 0.25
        dx_arrow = DoubleArrow(dx_left, dx_right, buff=0, color=YELLOW, stroke_width=1.8,
                               max_tip_length_to_length_ratio=0.22)
        dx_guides = VGroup(
            DashedLine(nodes[(2, 6)]["point"], dx_left, color=YELLOW, stroke_width=1),
            DashedLine(nodes[(3, 6)]["point"], dx_right, color=YELLOW, stroke_width=1),
        )
        dx_label = tex(r"\Delta x", 22, YELLOW).next_to(dx_arrow, UP, buff=0.28)
        dy_lower = nodes[(0, 2)]["point"] + LEFT * 0.28
        dy_upper = nodes[(0, 3)]["point"] + LEFT * 0.28
        dy_arrow = DoubleArrow(dy_lower, dy_upper, buff=0, color=BLUE, stroke_width=1.8,
                               max_tip_length_to_length_ratio=0.22)
        dy_guides = VGroup(
            DashedLine(nodes[(0, 2)]["point"], dy_lower, color=BLUE, stroke_width=1),
            DashedLine(nodes[(0, 3)]["point"], dy_upper, color=BLUE, stroke_width=1),
        )
        dy_label = tex(r"\Delta y", 22, BLUE).next_to(dy_arrow, LEFT, buff=0.04)
        self.play(FadeIn(coord_title), Write(coordinate), FadeIn(known_dot), FadeIn(known_label),
                  FadeIn(unknown_dot), FadeIn(unknown_label), FadeIn(cap), run_time=2.2)
        self.wait(1.0)
        self.play(Create(dx_guides), GrowArrow(dx_arrow), FadeIn(dx_label), run_time=1.5)
        self.wait(0.8)
        self.play(Create(dy_guides), GrowArrow(dy_arrow), FadeIn(dy_label), run_time=1.5)
        self.wait(5.0)

        self.play(FadeOut(cap), run_time=0.35)
        self.beat("one_node_and_four_neighbors")
        cap = caption("عند النقطة الداخلية Vᵢ,ⱼ، نُظهر أقرب أربع نقاط إليها")
        for key in ((3, 3), (2, 3), (4, 3), (3, 2), (3, 4)):
            self.play(Indicate(nodes[key]["dot"], color=YELLOW if key == (3, 3) else BLUE),
                      run_time=0.32)
        self.wait(1.5)
        center_key = (3, 3)
        neighbor_keys = ((2, 3), (4, 3), (3, 2), (3, 4))
        focus_center = np.array([2.0, -0.1, 0])
        focus_gap = 0.7
        focus_positions = {
            center_key: focus_center,
            (2, 3): focus_center + LEFT * focus_gap,
            (4, 3): focus_center + RIGHT * focus_gap,
            (3, 4): focus_center + UP * focus_gap,
            (3, 2): focus_center + DOWN * focus_gap,
        }
        focus_dots = {key: Dot(point, radius=0.105 if key == center_key else 0.085,
                               color=YELLOW if key == center_key else BLUE)
                      for key, point in focus_positions.items()}
        focus_frame = RoundedRectangle(width=4.75, height=3.1, corner_radius=0.12,
                                       stroke_color="#455464", stroke_width=1.2).move_to(focus_center)
        labels = {
            center_key: tex(r"V_{i,j}", 25, YELLOW).move_to(focus_center + DOWN * 1.15),
            (2, 3): tex(r"V_{i-1,j}", 23, BLUE).move_to(focus_center + LEFT * 1.75),
            (4, 3): tex(r"V_{i+1,j}", 23, BLUE).move_to(focus_center + RIGHT * 1.75),
            (3, 4): tex(r"V_{i,j+1}", 23, BLUE).move_to(focus_center + UP * 1.2),
            (3, 2): tex(r"V_{i,j-1}", 23, BLUE).move_to(focus_center + DOWN * 1.75),
        }
        for label in labels.values():
            fit_inside(label, 1.45, 0.38, padding=0.015)
        self.play(FadeOut(VGroup(coord_title, coordinate, known_dot, known_label, unknown_dot,
                                 unknown_label, dx_guides, dx_arrow, dx_label,
                                 dy_guides, dy_arrow, dy_label)), run_time=0.6)
        self.play(Create(focus_frame),
                  *[TransformFromCopy(nodes[key]["dot"], focus_dots[key]) for key in focus_positions],
                  run_time=2.1)
        self.play(*[FadeIn(label) for label in labels.values()], run_time=1.0)
        emphasize(self, focus_dots[center_key], color=YELLOW, run_time=0.9)
        self.wait(3.8)

        self.play(FadeOut(cap), run_time=0.35)
        self.beat("what_the_numerical_problem_seeks")
        cap = caption("قيمة الحد معروفة, والمطلوب تحديد الجهد عند نقاط الداخل")
        boundary_text = ar("على الحد: الجهد معلوم", 20, GREEN).move_to([-3.55, -2.15, 0])
        interior_text = ar("في الداخل: قيم نريد حسابها", 20, "#C4D0DC").move_to([-3.55, -2.62, 0])
        self.play(FadeIn(boundary_text), FadeIn(interior_text), FadeIn(cap), run_time=1.0)
        self.play(Indicate(nodes[(0, 4)]["dot"], color=GREEN),
                  Indicate(nodes[(5, 3)]["dot"], color=GREEN), run_time=0.9)
        self.wait(4.5)

        self.beat("finite_difference_scope")
        self.play(*[FadeOut(m) for m in list(self.mobjects)
                    if m not in (title, rule)], run_time=0.8)
        cap = caption("توفر الفروق المحدودة وسيلة عددية لتقريب حلول معادلتي لابلاس وبواسون")
        method = ar("هذه بداية طريقة الفروق المحدودة", 27, YELLOW).move_to([0, 1.8, 0])
        left_eq = tex(r"\nabla^2V=0", 39, BLUE).move_to([-2.75, 0.3, 0])
        right_eq = tex(r"\nabla^2V=-\frac{\rho}{\epsilon_0}", 39, GREEN).move_to([2.75, 0.3, 0])
        shared = ar("الفكرة تمتد إلى معادلتي لابلاس وبواسون", 21, WHITE).move_to([0, -1.0, 0])
        fit_inside(method, 10.8, 0.55, padding=0.02)
        fit_inside(left_eq, 5.0, 0.75, padding=0.02)
        fit_inside(right_eq, 5.6, 0.75, padding=0.02)
        self.play(FadeIn(method, shift=UP * 0.12), Write(left_eq), Write(right_eq),
                  FadeIn(shared), FadeIn(cap), run_time=2.3)
        self.wait(4.8)


if __name__ == "__main__":
    run(DiscreteLattice)
