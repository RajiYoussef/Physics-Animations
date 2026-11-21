"""Scene 6: boundary data and uniqueness for Laplace/Poisson problems."""
from pathlib import Path
import os
import sys

import numpy as np
from manim import *

os.environ.setdefault("POISSON_QUALITY", "final")

from settings34 import BLUE, GREEN, GREY, RED, WHITE, YELLOW, run

RAJI_ARCHIVE = Path(r"C:\Users\Bruker\Desktop\Creative softwares\YouTube\Library (zip)\Raji_science_anim_library_v0.3_video_only.zip")
if not RAJI_ARCHIVE.is_file():
    raise FileNotFoundError(f"Raji science animation library not found: {RAJI_ARCHIVE}")
sys.path.insert(0, f"{RAJI_ARCHIVE.as_posix()}/Raji_science_anim_library")

from raji_sci.core.colormap import diverging_rgb
from raji_sci.physics.field_visuals import ScalarFieldImage
from raji_sci.presentation.layout import fit_inside
from math_type import tex
from support34 import LessonScene, ar


class BoundaryConditionsUniqueness(LessonScene):
    def construct(self):
        title = ar("الشروط الحدية: متى يكون الحل وحيدً؟", 29, BLUE)
        fit_inside(title, 12.4, 0.48, padding=0.02).move_to([0, 3.55, 0])
        rule = Line([-6.15, 3.18, 0], [6.15, 3.18, 0], color="#344151", stroke_width=1.3)
        self.add(title, rule)

        def caption(text, color=WHITE):
            label = ar(text, 23, color)
            fit_inside(label, 12.3, 0.55, padding=0.02)
            return label.move_to([0, -3.48, 0])

        self.beat("boundary_data_and_two_questions")
        pde = tex(r"\nabla^2 V=-\frac{\rho}{\epsilon_0}", 43, YELLOW).move_to([-3.45, 2.45, 0])
        domain = RoundedRectangle(width=4.2, height=3.1, corner_radius=0.15,
                                  stroke_color=BLUE, stroke_width=2.2,
                                  fill_color="#0B1822", fill_opacity=0.9).move_to([-3.45, -0.15, 0])
        boundary_points = VGroup()
        for t in np.linspace(-1, 1, 9):
            for p in (domain.get_left() + RIGHT * (t + 1) * 2.1,
                      domain.get_right() + LEFT * (1 - t) * 2.1,
                      domain.get_top() + DOWN * (t + 1) * 1.55,
                      domain.get_bottom() + UP * (1 - t) * 1.55):
                boundary_points.add(Dot(p, radius=0.035, color=GREEN))
        interior = VGroup(*[
            Dot([-4.25 + i * 0.53, -0.95 + j * 0.53, 0], radius=0.05, color="#6F8191")
            for i in range(4) for j in range(4)
        ])
        domain_tag = ar("المنطقة Ω", 22, WHITE).move_to([-3.45, -0.15, 0])
        boundary_tag = tex(r"S", 24, GREEN).next_to(domain.get_top(), UP, buff=0.08)
        fixed_data = VGroup(
            ar("المصدر ρ", 23, YELLOW),
            ar("والجهد على الحد", 22, GREEN),
        ).arrange(DOWN, buff=0.15).move_to([2.85, 1.35, 0])
        fixed_equation = tex(r"V|_S\;\mathrm{fixed}", 29, GREEN).move_to([2.85, 0.52, 0])
        question1 = ar("هل يوجد حل؟", 27, WHITE).move_to([2.75, -0.55, 0])
        question2 = ar("وهل هو وحيد؟", 29, YELLOW).move_to([2.75, -1.45, 0])
        cap = caption("المعادلة تصف الداخل, والحد يزوّدنا بما يلزم لتحديد المسألة")
        self.play(Write(pde), Create(domain), FadeIn(boundary_points, lag_ratio=0.035),
                  FadeIn(interior, lag_ratio=0.05), run_time=2.8)
        self.play(FadeIn(domain_tag), FadeIn(boundary_tag), FadeIn(fixed_data),
                  Write(fixed_equation), run_time=1.5)
        self.play(FadeIn(question1, shift=RIGHT * 0.15), FadeIn(question2, shift=RIGHT * 0.15),
                  FadeIn(cap), run_time=1.2)
        self.play(Indicate(question2, color=YELLOW), run_time=1.0)
        self.wait(7.5)

        self.beat("two_candidates_same_data")
        old = VGroup(pde, domain, boundary_points, interior, domain_tag, boundary_tag,
                     fixed_data, fixed_equation, question1, question2, cap)
        self.play(FadeOut(old), run_time=0.8)
        cap = caption("لإثبات أن الحل وحيد، نفترض حلّين للجهد لهما توزيع الشحنة نفسه ويحققان قيم الجهد نفسها على حدود المنطقة")

        coordinates = np.linspace(-1, 1, 72)
        X, Y = np.meshgrid(coordinates, coordinates)
        edge = np.clip(1 - X**2, 0, 1) * np.clip(1 - Y**2, 0, 1)
        v1_data = edge * (0.75 * np.exp(-((X + 0.28) ** 2 + (Y - 0.08) ** 2) / 0.42)
                          + 0.22 * np.exp(-((X - 0.42) ** 2 + (Y + 0.28) ** 2) / 0.65))
        v2_data = edge * (0.72 * np.exp(-((X - 0.25) ** 2 + (Y + 0.08) ** 2) / 0.42)
                          + 0.22 * np.exp(-((X + 0.42) ** 2 + (Y - 0.28) ** 2) / 0.65))
        map_width, map_height = 3.75, 2.5
        first_map = ScalarFieldImage(v1_data, map_width, map_height, center=[-2.45, -0.1, 0],
                                     cmap=diverging_rgb, vmax=1.0, positive="#78DBAC", negative=BLUE)
        second_map = ScalarFieldImage(v2_data, map_width, map_height, center=[2.45, -0.1, 0],
                                      cmap=diverging_rgb, vmax=1.0, positive="#FFB65C", negative=BLUE)
        frame1 = Rectangle(width=map_width, height=map_height, stroke_color=GREEN,
                           stroke_width=1.8).move_to(first_map)
        frame2 = Rectangle(width=map_width, height=map_height, stroke_color=GREEN,
                           stroke_width=1.8).move_to(second_map)
        head1 = VGroup(ar("الحل المفترض الأول", 23, GREEN),
                       tex(r"\nabla^2V_1=-\rho/\epsilon_0", 28, GREEN)).arrange(DOWN, buff=0.14).move_to([-2.45, 1.65, 0])
        head2 = VGroup(ar("الحل المفترض الثاني", 23, YELLOW),
                       tex(r"\nabla^2V_2=-\rho/\epsilon_0", 28, YELLOW)).arrange(DOWN, buff=0.14).move_to([2.45, 1.65, 0])
        same_boundary = tex(r"V_1|_S=V_2|_S", 30, WHITE).move_to([0, -1.82, 0])
        for obj, w, h in ((head1, 4.5, 0.95), (head2, 4.5, 0.95), (same_boundary, 4.0, 0.48)):
            fit_inside(obj, w, h, padding=0.02)
        self.play(FadeIn(head1), FadeIn(head2), FadeIn(first_map), FadeIn(second_map),
                  Create(frame1), Create(frame2), FadeIn(same_boundary), FadeIn(cap), run_time=2.3)
        self.play(Indicate(frame1, color=GREEN), Indicate(frame2, color=GREEN), run_time=1.0)
        self.wait(5.7)

        self.beat("subtract_candidate_equations")
        self.play(FadeOut(Group(head1, head2, first_map, second_map, frame1, frame2,
                                same_boundary, cap)), run_time=0.8)
        cap = caption("نطرح المعادلتين فيُلغى حد الشحنة المشترك.")
        eq1 = tex(r"\nabla^2V_1=-\frac{\rho}{\epsilon_0}", 39, GREEN).move_to([0, 1.35, 0])
        eq2 = tex(r"\nabla^2V_2=-\frac{\rho}{\epsilon_0}", 39, YELLOW).move_to([0, 0.15, 0])
        source_box1 = SurroundingRectangle(eq1, color=BLUE, buff=0.13, stroke_width=1.7)
        source_box2 = SurroundingRectangle(eq2, color=BLUE, buff=0.13, stroke_width=1.7)
        subtract = tex(r"W=V_1-V_2", 36, WHITE).move_to([0, -1.05, 0])
        result = tex(r"\nabla^2W=0\qquad W|_S=0", 42, BLUE).move_to([0, -2.05, 0])
        for obj, w, h in ((eq1, 8.2, 0.65), (eq2, 8.2, 0.65), (result, 11.0, 0.7)):
            fit_inside(obj, w, h, padding=0.02)
        self.play(Write(eq1), Write(eq2), Create(source_box1), Create(source_box2), FadeIn(cap), run_time=2.2)
        self.play(Indicate(source_box1, color=BLUE), Indicate(source_box2, color=BLUE), run_time=1.2)
        self.play(FadeOut(source_box1), FadeOut(source_box2), Write(subtract), run_time=1.0)
        self.play(TransformFromCopy(VGroup(eq1, eq2), result), run_time=1.6)
        self.wait(3.8)

        self.beat("maximum_principle")
        self.play(FadeOut(VGroup(eq1, eq2, subtract, result, cap)), run_time=0.7)
        cap = caption("لو كان الفرق غير صفري، لظهر له داخل المنطقة حدٌّ أقصى أو أدنى.")
        laplace_w = tex(r"\nabla^2W=0", 35, BLUE).move_to([0, 2.45, 0])
        principle = ar("لا يمكن لدالة توافقية غير ثابتة أن تبلغ قيمة عظمى أو صغرى داخل المنطقة", 25, WHITE).move_to([0, 1.83, 0])
        fit_inside(principle, 11.8, 0.45, padding=0.02)
        w_base = 0.85 * edge * (
            np.exp(-((X + 0.38) ** 2 + (Y - 0.02) ** 2) / 0.22)
            - np.exp(-((X - 0.38) ** 2 + (Y + 0.02) ** 2) / 0.22)
        )
        w_image = ScalarFieldImage(w_base, 4.8, 2.65, center=[0, -0.18, 0],
                                   cmap=diverging_rgb, vmax=0.34, positive="#FFB65C",
                                   negative="#64C9EE", zero="#05080D")
        w_frame = Rectangle(width=4.8, height=2.65, stroke_color="#4B5A68", stroke_width=1.4).move_to(w_image)
        max_point = Dot([-0.9, -0.05, 0], radius=0.075, color=YELLOW)
        min_point = Dot([0.9, -0.05, 0], radius=0.075, color=BLUE)
        max_tag = ar("قيمة عظمى مفترضة", 19, YELLOW).move_to([-3.35, 0.53, 0])
        min_tag = ar(" قيمة صغرى مفترضة", 19, BLUE).move_to([3.35, 0.53, 0])
        zero_boundary = tex(r"W|_S=0", 26, GREEN).move_to([0, -1.78, 0])
        self.play(Write(laplace_w), FadeIn(principle), FadeIn(w_image), Create(w_frame),
                  FadeIn(max_point), FadeIn(min_point), FadeIn(max_tag), FadeIn(min_tag),
                  Write(zero_boundary), FadeIn(cap), run_time=2.5)
        self.wait(5.5)
        collapse = ValueTracker(0)
        w_image.add_updater(lambda image: image.update_values(w_base * (1 - collapse.get_value())))
        self.play(collapse.animate.set_value(1), FadeOut(max_point), FadeOut(min_point),
                  FadeOut(max_tag), FadeOut(min_tag), run_time=5.5, rate_func=smooth)
        w_image.clear_updaters()
        zero_result = tex(r"W=0\quad\Longrightarrow\quad V_1=V_2", 41, GREEN).move_to([0, -2.35, 0])
        fit_inside(zero_result, 9.8, 0.62, padding=0.02)
        self.play(Write(zero_result), run_time=1.3)
        self.wait(7.8)

        self.beat("dirichlet_and_neumann")
        self.play(*[FadeOut(m) for m in list(self.mobjects)
                    if m not in (title, rule)], run_time=0.8)
        cap = caption("يعتمد نوع الشرط الحدّي على ما نحدده على حدود المنطقة: الجهد أم مشتقته العمودية")
        card_y = -0.03
        card_w, card_h = 5.65, 3.65
        left_card = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.12,
                                     stroke_color=GREEN, stroke_width=1.8,
                                     fill_color="#0A1118", fill_opacity=0.75).move_to([-3.12, card_y, 0])
        right_card = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.12,
                                      stroke_color=BLUE, stroke_width=1.8,
                                      fill_color="#0A1118", fill_opacity=0.75).move_to([3.12, card_y, 0])
        dir_title = ar("ديريشليه: نعرف الجهد", 23, GREEN).move_to([-3.12, 1.24, 0])
        neu_title = ar("نيومان: نعرف المشتقة العمودية", 22, BLUE).move_to([3.12, 1.24, 0])
        dir_formula = tex(r"V|_S=V_b", 34, GREEN).move_to([-3.12, 0.65, 0])
        neu_formula = tex(r"\left.\frac{\partial V}{\partial n}\right|_S=g_n", 31, BLUE).move_to([3.12, 0.65, 0])

        left_box = Rectangle(width=2.55, height=1.24, stroke_color="#657381", stroke_width=1.2).move_to([-3.12, -0.43, 0])
        left_dots = VGroup()
        for t in np.linspace(-1, 1, 7):
            for p in (left_box.get_left() + RIGHT * (t + 1) * 1.275,
                      left_box.get_right() + LEFT * (1 - t) * 1.275,
                      left_box.get_top() + DOWN * (t + 1) * 0.62,
                      left_box.get_bottom() + UP * (1 - t) * 0.62):
                left_dots.add(Dot(p, radius=0.035, color=GREEN))
        left_text = ar("قيمة معلومة على S", 19, GREEN).move_to([-3.12, -1.28, 0])
        right_box = Rectangle(width=2.55, height=1.24, stroke_color="#657381", stroke_width=1.2).move_to([3.12, -0.43, 0])
        normals = VGroup(*[
            Arrow(right_box.get_top() + LEFT * x + UP * 0.08,
                  right_box.get_top() + LEFT * x + UP * 0.42, buff=0,
                  color=YELLOW, stroke_width=2.1, max_tip_length_to_length_ratio=0.28)
            for x in (-0.8, 0, 0.8)
        ])
        right_text = VGroup(
            tex(r"E_n=-\frac{\partial V}{\partial n}", 25, YELLOW),
            ar("إذا كانت المشتقة صفر، فالمركبة العمودية صفر.", 17, WHITE),
        ).arrange(DOWN, buff=0.16).move_to([3.12, -1.35, 0])
        fit_inside(right_text, 4.95, 0.72, padding=0.02)
        self.play(Create(left_card), Create(right_card), FadeIn(dir_title), FadeIn(neu_title),
                  Write(dir_formula), Write(neu_formula), Create(left_box), Create(right_box),
                  FadeIn(left_dots, lag_ratio=0.02),
                  LaggedStart(*[GrowArrow(arrow) for arrow in normals], lag_ratio=0.22), FadeIn(left_text),
                  FadeIn(right_text), FadeIn(cap), run_time=3.5)
        self.wait(5.5)


if __name__ == "__main__":
    run(BoundaryConditionsUniqueness)
