"""A visual introduction to the neural-network method for Laplace's equation.

Run this file with PyCharm's Run button. The companion narration file contains
exactly the Arabic passages supplied for this scene. This script renders the
silent animation; it does not synthesize speech.
"""

import json
import os
import sys
import uuid
from pathlib import Path

os.environ.setdefault("POISSON_QUALITY", "final")

import numpy as np
from manim import config
from manim import *

from settings34 import BLUE, GREEN, GREY, WHITE, YELLOW, ROOT, OPEN_AFTER_RENDER, _open
from support34 import ar
from math_type import tex

RAJI_ARCHIVE = Path(
    r"C:\Users\Bruker\Desktop\Creative softwares\YouTube\Library (zip)\Raji_science_anim_library_v0.3_video_only.zip"
)
if RAJI_ARCHIVE.is_file():
    sys.path.insert(0, f"{RAJI_ARCHIVE.as_posix()}/Raji_science_anim_library")

from raji_sci.presentation.choreography import emphasize, focus_camera
from raji_sci.presentation.layout import fit_inside, frame_violations
from raji_sci.physics.field_visuals import ScalarFieldImage
from raji_sci.core.colormap import diverging_rgb
from raji_sci.style import LabelBadge


NARRATION = [
    "توفر لنا طريقة الفروق المحدودة وسيلةً فعالةً لحل معادلة لابلاس؛ حيث نقوم بحساب الجهد عند نقاطٍ موزعةٍ على شبكة.",
    "ولكن، ماذا لو أردنا الحصول على دالةٍ تُمكّننا من معرفة قيمة الجهد في أي موضعٍ داخل النطاق المطلوب؟",
    "عند الاعتماد على قيمٍ محددةٍ عند نقاط الشبكة، نحتاج إلى استخدام الاستكمال لتقدير القيم بين تلك النقاط.",
    "علاوةً على ذلك، في الأبعاد الأعلى، قد يتطلب استخدام شبكةٍ دقيقةٍ عدداً هائلاً من النقاط.",
    "لذا، سنستخدم في هذا الفيديو نهجاً آخر، وهو: التعلم الآلي. سنقوم بتمثيل الجهد باستخدام شبكةٍ عصبية (neural network).",
    "تتكون الشبكة العصبية من مجموعةٍ من الوحدات الحسابية البسيطة المرتبة في طبقات. تستقبل كل وحدةٍ مجموعةً من الأرقام، وتدمجها معاً، ثم تمرر النتيجة إلى الطبقة التالية.",
    "ويُقصد بـ \"الدمج\" هنا أن كل رقمٍ واردٍ يُضرب في \"وزنٍ\" معين، وهو ما يحدد مدى تأثير ذلك الرقم في النتيجة النهائية.",
    "كما تضيف الوحدة قيمةً تُعرف بـ \"الانحياز\"—وهي إزاحةٌ قابلةٌ للتعديل— ثم تُطبق \"دالة تنشيط\" على الناتج.",
    "تصبح مخرجات إحدى الطبقات هي المدخلات للطبقة التي تليها، وتستمر هذه العملية عبر الطبقات الخفية وصولاً إلى طبقة المخرجات التي تُنتج في النهاية قيمةً عددية.",
    "في سياق مسألتنا، تُمثّل هذه القيمة \"الجهد\". فعندما نُدخل للشبكة إحداثيات موضعٍ ما فإنها تُرجع قيمةً تقريبيةً للجهد.",
    "وتتمثل عملية التعلم الآلي في ضبط أوزان الشبكة وقيم الانحياز الخاصة بها؛ حيث نعدّلها بحيث تحقق الدالة الناتجة —بدرجةٍ عاليةٍ من الدقة— معادلة لابلاس والشروط الحدية.",
    "والنتيجة هي تقريبٌ متصلٌ لدالة الجهد، يمكننا من خلاله حساب قيمته عند أي نقطةٍ داخل النطاق المحدد.",
]

CAPTIONS = [
    "الجهد عند نقاط الشبكة",
    "ماذا عن نقطةٍ بين نقاط الشبكة؟",
    "تقدير الجهد بالاستكمال",
    "في الأبعاد الأعلى، تتضاعف نقاط الشبكة",
    "نمثل الجهد بشبكة عصبية",
    "تستقبل الوحدة أعداداً، وتجمعها، ثم تمرر الناتج",
    "الوزن يحدد تأثير كل إشارة",
    "انحياز، ثم دالة تنشيط",
    "تنتقل الإشارات بين الطبقات حتى يظهر خرج واحد",
    "من (x,y) إلى قيمة الجهد",
    "نضبط الأوزان والانحياز للاقتراب من المعادلة والحدود",
    "قيمة تقريبية للجهد عند أي موضع",
]


class MachineLearningPotentialIntro(MovingCameraScene):
    """Twelve narrated beats, with a visible action tied to every passage."""

    def setup(self):
        super().setup()
        self.camera.background_color = "#000000"
        self.beats = []
        self.caption_mob = None
        self.camera.frame.save_state()

    def set_caption(self, text):
        if self.caption_mob is not None:
            self.play(FadeOut(self.caption_mob), run_time=0.22)
            self.caption_mob = None
        if text is None:
            return
        badge = LabelBadge(text, size=24, color=WHITE)
        fit_inside(badge, 12.5, 0.74, padding=0.02)
        badge.move_to([0, -3.48, 0])
        violations = frame_violations([badge], frame_width=14.222222, frame_height=8)
        if violations:
            raise ValueError("The narration caption exceeds the safe frame.")
        self.caption_mob = badge
        self.play(FadeIn(badge, shift=UP * 0.08), run_time=0.28)

    def begin_beat(self, index, name, show_caption=True):
        self.current_beat_start = float(self.time)
        self.beats.append({"name": name, "start": round(self.current_beat_start, 3)})
        if show_caption:
            self.set_caption(CAPTIONS[index])

    def end_beat(self, index):
        # Pace the visual beat to a natural spoken read, around 115 Arabic words/min.
        target = max(4.0, len(NARRATION[index].split()) * 60 / 115 + 0.35)
        remaining = target - (float(self.time) - self.current_beat_start)
        if remaining > 0:
            self.wait(remaining)
        self.beats[-1]["end"] = round(float(self.time), 3)

    def make_grid(self, center=(-3.65, 0.0), side=3.8, n=7):
        cx, cy = center
        x_values = np.linspace(cx - side / 2, cx + side / 2, n)
        y_values = np.linspace(cy - side / 2, cy + side / 2, n)
        frame = Square(side_length=side, stroke_color=BLUE, stroke_width=2.0)
        frame.set_fill("#07131B", opacity=0.45).move_to([cx, cy, 0])
        lines = VGroup()
        for x in x_values[1:-1]:
            lines.add(Line([x, y_values[0], 0], [x, y_values[-1], 0],
                           color="#344653", stroke_width=0.9))
        for y in y_values[1:-1]:
            lines.add(Line([x_values[0], y, 0], [x_values[-1], y, 0],
                           color="#344653", stroke_width=0.9))
        points = {}
        dots = VGroup()
        for i, x in enumerate(x_values):
            for j, y in enumerate(y_values):
                edge = i in (0, n - 1) or j in (0, n - 1)
                dot = Dot([x, y, 0], radius=0.043 if edge else 0.038,
                          color=GREEN if edge else "#A7B6C4")
                dots.add(dot)
                points[(i, j)] = dot
        return frame, lines, dots, points

    def make_network(self, cx=0.0, cy=0.0, scale=1.0, labels=True):
        layer_x = [-3.0, -1.0, 1.0, 3.0]
        layer_y = [
            [-0.68, 0.68],
            [-1.52, -0.52, 0.52, 1.52],
            [-1.02, 0.0, 1.02],
            [0.0],
        ]
        layer_colors = [BLUE, "#BBC7D3", "#BBC7D3", GREEN]
        layers = []
        for col, ys in enumerate(layer_y):
            nodes = VGroup()
            for y in ys:
                node = Circle(radius=0.17 * scale, stroke_color=layer_colors[col],
                              stroke_width=1.8, fill_color=layer_colors[col],
                              fill_opacity=0.13)
                node.move_to([cx + layer_x[col] * scale, cy + y * scale, 0])
                nodes.add(node)
            layers.append(nodes)
        edges = []
        wire_group = VGroup()
        for layer_index in range(len(layers) - 1):
            for source_index, source in enumerate(layers[layer_index]):
                for target_index, target in enumerate(layers[layer_index + 1]):
                    wire = Arrow(source.get_center(), target.get_center(), buff=0.18 * scale,
                                 color="#52606C", stroke_width=1.0,
                                 max_tip_length_to_length_ratio=0.12,
                                 max_stroke_width_to_length_ratio=5)
                    wire_group.add(wire)
                    edges.append({"layer": layer_index, "source_index": source_index,
                                  "target_index": target_index, "source": source,
                                  "target": target, "mob": wire})
        layer_labels = VGroup()
        if labels:
            names = ["المدخلات", "طبقة خفية", "طبقة خفية", "المخرجات"]
            for col, name in enumerate(names):
                label = ar(name, max(16, int(19 * scale)), WHITE)
                label.move_to([cx + layer_x[col] * scale, cy + 2.1 * scale, 0])
                fit_inside(label, 1.7 * scale, 0.42 * scale, padding=0.01)
                layer_labels.add(label)
        group = VGroup(wire_group, *layers, layer_labels)
        return {"layers": layers, "edges": edges, "wires": wire_group,
                "labels": layer_labels, "group": group}

    def pulse(self, edge, color=YELLOW, run_time=0.55):
        token = Dot(edge.get_start(), radius=0.065, color=color)
        self.add(token)
        self.play(MoveAlongPath(token, edge, rate_func=linear), run_time=run_time)
        self.remove(token)

    def finish_scene(self):
        review_dir = ROOT / "review"
        review_dir.mkdir(exist_ok=True)
        path = review_dir / "MachineLearningPotentialIntro_timing.json"
        path.write_text(json.dumps(self.beats, ensure_ascii=False, indent=2), encoding="utf-8")
        self.camera.get_image().save(review_dir / "MachineLearningPotentialIntro_end.png")

    def construct(self):
        # 1. Finite differences assign a value to each grid location.
        self.begin_beat(0, "grid_values")
        grid_frame, grid_lines, grid_dots, grid_points = self.make_grid()
        self.play(Create(grid_frame), LaggedStart(*[Create(line) for line in grid_lines],
                                                  lag_ratio=0.055, run_time=1.5))
        self.play(LaggedStart(*[FadeIn(dot, scale=0.45) for dot in grid_dots],
                              lag_ratio=0.008, run_time=1.8))
        sample = grid_points[(3, 4)]
        value_tag = tex("V_{ij}", 34, YELLOW).move_to([2.75, 0.85, 0])
        pointer = Arrow(value_tag.get_left() + LEFT * 0.1, sample.get_center(),
                        buff=0.13, color=YELLOW, stroke_width=1.5)
        self.play(FadeIn(value_tag), GrowArrow(pointer), run_time=0.8)
        emphasize(self, sample, color=YELLOW, run_time=0.45)
        self.end_beat(0)

        # 2. Move a probe between grid points and expose its unknown value.
        self.begin_beat(1, "interior_probe")
        start = grid_points[(3, 3)].get_center()
        end = (grid_points[(3, 3)].get_center() + grid_points[(4, 4)].get_center()) / 2
        probe = Dot(start, radius=0.09, color=YELLOW)
        self.play(FadeOut(value_tag), FadeOut(pointer), FadeIn(probe), run_time=0.5)
        arc = ArcBetweenPoints(start, end, angle=-PI / 3, color=YELLOW)
        question = tex("?", 38, YELLOW).next_to(probe, UR, buff=0.1)
        coords = tex("(x,y)", 24, BLUE).next_to(probe, DOWN + RIGHT, buff=0.12)
        self.play(MoveAlongPath(probe, arc, rate_func=linear), run_time=1.0)
        question.next_to(probe, UR, buff=0.1)
        coords.next_to(probe, DOWN + RIGHT, buff=0.12)
        self.play(FadeIn(question, scale=0.6), FadeIn(coords), run_time=0.45)
        self.end_beat(1)

        # 3. Four nearby values send signals to an estimated value at the probe.
        self.begin_beat(2, "interpolation")
        corners = [grid_points[(3, 3)], grid_points[(4, 3)],
                   grid_points[(3, 4)], grid_points[(4, 4)]]
        rings = VGroup(*[Circle(radius=0.14, color=c, stroke_width=2.2).move_to(dot)
                         for dot, c in zip(corners, [BLUE, GREEN, BLUE, GREEN])])
        estimate = tex(r"\tilde V(x,y)", 32, YELLOW).move_to([3.35, 0.15, 0])
        hint = ar("تقدير بالاستكمال", 19, WHITE).next_to(estimate, DOWN, buff=0.25)
        self.play(FadeOut(question), FadeOut(coords), Create(rings), FadeIn(estimate),
                  FadeIn(hint), run_time=0.8)
        pulse_colors = [BLUE, GREEN, BLUE, GREEN]
        for dot, color in zip(corners, pulse_colors):
            path = Line(dot.get_center(), estimate.get_center() + LEFT * 0.4)
            pulse = Dot(dot.get_center(), radius=0.06, color=color)
            self.add(pulse)
            self.play(MoveAlongPath(pulse, path, rate_func=linear), run_time=0.48)
            self.remove(pulse)
        self.play(Flash(estimate, color=YELLOW, flash_radius=0.35), run_time=0.5)
        self.end_beat(2)

        # 4. Extrude a 2D lattice and show the N^d growth symbolically.
        self.begin_beat(3, "higher_dimensions")
        self.play(FadeOut(VGroup(grid_frame, grid_lines, grid_dots, probe, rings,
                                 estimate, hint)), run_time=0.45)
        mesh_center = np.array([-3.8, -0.05, 0.0])
        side = 2.8
        mesh_layers = []
        mesh_points = []
        mesh_lines = VGroup()
        values = np.linspace(-side / 2, side / 2, 5)
        for depth in range(3):
            offset = np.array([0.34 * depth, 0.25 * depth, 0.0])
            layer_points = {}
            for i, x in enumerate(values):
                for j, y in enumerate(values):
                    point = mesh_center + np.array([x, y, 0.0]) + offset
                    layer_points[(i, j)] = point
                    mesh_points.append(Dot(point, radius=0.035, color=BLUE if depth == 0 else GREEN))
            mesh_layers.append(layer_points)
            for x in values:
                mesh_lines.add(Line(mesh_center + np.array([x, -side/2, 0]) + offset,
                                    mesh_center + np.array([x, side/2, 0]) + offset,
                                    color="#536778", stroke_width=0.8))
            for y in values:
                mesh_lines.add(Line(mesh_center + np.array([-side/2, y, 0]) + offset,
                                    mesh_center + np.array([side/2, y, 0]) + offset,
                                    color="#536778", stroke_width=0.8))
        connectors = VGroup()
        for depth in range(2):
            for key, point in mesh_layers[depth].items():
                connectors.add(Line(point, mesh_layers[depth + 1][key],
                                    color=YELLOW, stroke_width=0.75, stroke_opacity=0.55))
        mesh_dots = VGroup(*mesh_points)
        formula = tex("N\\times N", 32, WHITE).move_to([3.25, 0.8, 0])
        total = tex("N^d", 38, YELLOW).move_to([3.25, -0.55, 0])
        per_dim = ar("N نقطة في كل بُعد", 20, BLUE).next_to(formula, DOWN, buff=0.25)
        self.play(Create(mesh_lines), FadeIn(mesh_dots, lag_ratio=0.01), run_time=1.7)
        self.play(Create(connectors), FadeIn(per_dim), FadeIn(formula), run_time=0.9)
        self.play(Transform(formula, tex("N^3", 38, WHITE).move_to(formula)), run_time=0.6)
        self.play(Transform(formula, total), run_time=0.75)
        axes_tags = VGroup(tex("x", 20, BLUE).move_to(mesh_center + RIGHT * 1.65 + DOWN * 1.5),
                           tex("y", 20, BLUE).move_to(mesh_center + LEFT * 1.55 + UP * 1.45),
                           tex("z", 20, BLUE).move_to(mesh_center + RIGHT * 1.0 + UP * 1.65))
        self.play(FadeIn(axes_tags), run_time=0.35)
        self.end_beat(3)

        # 5. Let sample points lift and reorganize as a neural network.
        self.begin_beat(4, "introduce_neural_network")
        net = self.make_network(cx=1.75, cy=-0.05, scale=0.68)
        sample_dots = [mesh_dots[i] for i in (0, 4, 12, 20, 24)]
        targets = [net["layers"][0][0], net["layers"][0][1],
                   net["layers"][1][0], net["layers"][1][2], net["layers"][3][0]]
        self.play(*[dot.animate.shift(UP * 0.25) for dot in sample_dots], run_time=0.45)
        self.play(*[sample.animate.move_to(target.get_center() + UP * 0.32)
                    for sample, target in zip(sample_dots, targets)], run_time=0.8)
        self.play(LaggedStart(*[Create(edge["mob"]) for edge in net["edges"]],
                              lag_ratio=0.006, run_time=2.0),
                  LaggedStart(*[FadeIn(node, scale=0.7)
                                for layer in net["layers"] for node in layer],
                              lag_ratio=0.06, run_time=1.4),
                  LaggedStart(*[FadeIn(label) for label in net["labels"]],
                              lag_ratio=0.15, run_time=0.8))
        self.play(FadeOut(VGroup(mesh_lines, mesh_dots, connectors, formula, per_dim, axes_tags)),
                  run_time=0.5)
        # The points become a representation with coordinates as inputs and V as output.
        self.end_beat(4)

        # 6. Show separate incoming values combining in a unit, then one signal leaving.
        self.begin_beat(5, "unit_receives_combines_passes")
        active = net["layers"][1][1]
        incoming = [e for e in net["edges"] if e["layer"] == 0 and e["target"] is active]
        outgoing = next(e for e in net["edges"] if e["layer"] == 1
                        and e["source"] is active and e["target_index"] == 1)
        input_tags = VGroup(tex("a_1", 19, BLUE).next_to(net["layers"][0][0], LEFT, buff=0.12),
                            tex("a_2", 19, GREEN).next_to(net["layers"][0][1], LEFT, buff=0.12))
        halo = Circle(radius=0.3, color=YELLOW, stroke_width=2.2).move_to(active)
        self.play(FadeIn(input_tags), Create(halo), run_time=0.45)
        self.pulse(incoming[0]["mob"], BLUE, 0.65)
        self.pulse(incoming[1]["mob"], GREEN, 0.65)
        self.play(Indicate(active, color=YELLOW), run_time=0.4)
        self.pulse(outgoing["mob"], YELLOW, 0.68)
        self.end_beat(5)

        # 7. Zoom in on one unit and show each weight multiplying its signal.
        self.begin_beat(6, "weights_multiply_inputs", show_caption=False)
        self.set_caption(None)
        source_nodes = [net["layers"][0][0], net["layers"][0][1]]
        kept_nodes = {id(active), *(id(node) for node in source_nodes)}
        kept_edges = {id(edge["mob"]) for edge in incoming}
        unrelated = [edge["mob"] for edge in net["edges"]
                     if id(edge["mob"]) not in kept_edges]
        unrelated.extend(node for layer in net["layers"] for node in layer
                         if id(node) not in kept_nodes)
        unrelated.append(net["labels"])
        self.play(*[FadeOut(mob) for mob in unrelated], run_time=0.45)
        close_group = VGroup(active, *source_nodes,
                             *[edge["mob"] for edge in incoming])
        focus_camera(self, close_group, padding=1.55, run_time=0.85)
        weight_tags = VGroup()
        input_math = VGroup()
        for k, edge in enumerate(incoming[:2], start=1):
            weight = tex(f"w_{k}", 23, YELLOW).move_to(edge["mob"].get_center() + UP * 0.2)
            expression = tex(f"a_{k}\\longrightarrow w_{k}a_{k}", 21,
                             BLUE if k == 1 else GREEN)
            input_math.add(expression)
            weight_tags.add(weight)
        input_math.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fit_inside(input_math, 4.8, 0.9, padding=0.03)
        input_math.move_to(active.get_center() + DOWN * 1.1)
        self.play(FadeIn(weight_tags), Write(input_math), run_time=0.8)
        self.pulse(incoming[0]["mob"], BLUE, 0.75)
        self.pulse(incoming[1]["mob"], GREEN, 0.75)
        self.play(Indicate(weight_tags, color=YELLOW), run_time=0.55)
        self.end_beat(6)

        # 8. Show the sum, bias and activation as a clean, isolated neuron.
        self.begin_beat(7, "bias_and_activation", show_caption=False)
        self.play(FadeOut(VGroup(weight_tags, input_math, input_tags, halo, net["group"])),
                  Restore(self.camera.frame), run_time=0.75)
        self.set_caption(CAPTIONS[7])

        # Two weighted inputs and a bias enter one unit; its result passes through f.
        unit_center = np.array([-2.0, 0.55, 0.0])
        unit = Circle(radius=0.48, stroke_color=YELLOW, stroke_width=2.3,
                      fill_color="#101820", fill_opacity=1).move_to(unit_center)
        sigma = tex(r"\Sigma", 33, WHITE).move_to(unit)
        input_a1 = tex("a_1", 25, BLUE).move_to([-5.55, 1.18, 0])
        input_a2 = tex("a_2", 25, GREEN).move_to([-5.55, -0.08, 0])
        arrow_a1 = Arrow([-5.0, 1.18, 0], [-2.42, 0.77, 0], buff=0.03,
                         color=BLUE, stroke_width=2.0)
        arrow_a2 = Arrow([-5.0, -0.08, 0], [-2.42, 0.32, 0], buff=0.03,
                         color=GREEN, stroke_width=2.0)
        weight_1 = tex("w_1", 23, YELLOW).move_to([-3.7, 1.18, 0])
        weight_2 = tex("w_2", 23, YELLOW).move_to([-3.7, -0.28, 0])
        bias_arrow = Arrow([-2.0, 2.18, 0], [-2.0, 1.03, 0], buff=0.02,
                           color=YELLOW, stroke_width=2.0)
        bias_tag = tex("b", 25, YELLOW).move_to([-2.53, 2.24, 0])
        bias_label = ar("انحياز", 19, YELLOW).move_to([-1.28, 2.25, 0])
        z_arrow = Arrow([-1.5, 0.55, 0], [-0.28, 0.55, 0], buff=0.03,
                        color=WHITE, stroke_width=1.9)
        z_tag = tex("z", 22, WHITE).move_to([-0.9, 0.84, 0])
        activation_box = RoundedRectangle(width=1.0, height=0.84, corner_radius=0.1,
                                          stroke_color=GREEN, stroke_width=2,
                                          fill_color="#0B231D", fill_opacity=0.95)
        activation_box.move_to([0.22, 0.55, 0])
        f_label = tex("f", 32, GREEN).move_to(activation_box)
        activation_label = ar("دالة التنشيط", 20, GREEN).move_to([0.22, 1.35, 0])
        output_arrow = Arrow([0.75, 0.55, 0], [2.55, 0.55, 0], buff=0.03,
                             color=GREEN, stroke_width=2.0)
        output_tag = tex("a", 25, GREEN).move_to([2.95, 0.55, 0])
        calc_visual = VGroup(input_a1, input_a2, arrow_a1, arrow_a2,
                             weight_1, weight_2, unit, sigma, bias_arrow, bias_tag,
                             bias_label, z_arrow, z_tag, activation_box, f_label,
                             activation_label, output_arrow, output_tag)
        calc_visual.shift(RIGHT * 0.8)
        self.play(Create(arrow_a1), Create(arrow_a2), FadeIn(input_a1), FadeIn(input_a2),
                  FadeIn(unit), FadeIn(sigma), FadeIn(weight_1), FadeIn(weight_2),
                  run_time=0.8)
        for path, color in ((arrow_a1, BLUE), (arrow_a2, GREEN)):
            signal = Dot(path.get_start(), radius=0.07, color=color)
            self.add(signal)
            self.play(MoveAlongPath(signal, path, rate_func=linear), run_time=0.48)
            self.remove(signal)

        formula_panel = RoundedRectangle(width=10.4, height=1.42, corner_radius=0.08,
                                         stroke_color="#3E4B59", stroke_width=0.9,
                                         fill_color="#000000", fill_opacity=0.97)
        formula_panel.move_to([0.0, -1.55, 0])
        formula_1 = tex(r"z=w_1a_1+w_2a_2", 28, WHITE).move_to([0.0, -1.28, 0])
        formula_1_full = tex(r"z=w_1a_1+w_2a_2+b", 28, WHITE).move_to(formula_1)
        formula_2 = tex(r"a=f(z)", 27, GREEN).move_to([0.0, -1.91, 0])
        self.play(FadeIn(formula_panel), Write(formula_1), run_time=0.5)
        self.play(GrowArrow(bias_arrow), FadeIn(bias_tag), FadeIn(bias_label), run_time=0.55)
        bias_signal = Dot(bias_arrow.get_start(), radius=0.07, color=YELLOW)
        self.add(bias_signal)
        self.play(MoveAlongPath(bias_signal, bias_arrow, rate_func=linear), run_time=0.48)
        self.remove(bias_signal)
        self.play(Transform(formula_1, formula_1_full), run_time=0.38)
        self.play(Create(z_arrow), FadeIn(z_tag), Create(activation_box), FadeIn(f_label),
                  FadeIn(activation_label), GrowArrow(output_arrow), run_time=0.65)
        activation_signal = Dot(z_arrow.get_start(), radius=0.07, color=YELLOW)
        self.add(activation_signal)
        self.play(MoveAlongPath(activation_signal, z_arrow, rate_func=linear), run_time=0.42)
        self.remove(activation_signal)
        self.play(Write(formula_2), FadeIn(output_tag), run_time=0.45)
        self.end_beat(7)

        # 9. Pull back and send activations through successive hidden layers.
        self.beats.append({"name": "hidden_layers_to_output", "start": round(float(self.time), 3)})
        self.current_beat_start = float(self.time)
        net = self.make_network(cx=0.0, cy=0.0, scale=1.22)
        self.set_caption(CAPTIONS[8])
        self.play(LaggedStart(*[Create(edge["mob"]) for edge in net["edges"]],
                              lag_ratio=0.008, run_time=1.25),
                  LaggedStart(*[FadeIn(node, scale=0.75)
                                for layer in net["layers"] for node in layer],
                              lag_ratio=0.045, run_time=1.1),
                  LaggedStart(*[FadeIn(label) for label in net["labels"]],
                              lag_ratio=0.12, run_time=0.6),
                  FadeOut(VGroup(calc_visual, formula_panel, formula_1, formula_2)),
                  run_time=1.25)
        for edge in net["edges"]:
            if edge["layer"] in (0, 1, 2) and edge["source_index"] in (0, 1):
                self.pulse(edge["mob"], YELLOW if edge["layer"] == 1 else BLUE, 0.28)
        self.end_beat(8)

        # 10. Feed (x,y) into the network and return a potential value.
        self.begin_beat(9, "network_maps_position_to_potential")
        self.play(FadeOut(net["group"]), run_time=0.45)
        domain_frame, domain_lines, domain_dots, domain_points = self.make_grid(
            center=(-4.55, -0.05), side=2.75, n=6)
        self.play(Create(domain_frame), Create(domain_lines),
                  LaggedStart(*[FadeIn(dot, scale=0.6) for dot in domain_dots],
                              lag_ratio=0.025, run_time=1.0))
        position = Dot(domain_points[(2, 3)].get_center(), radius=0.095, color=YELLOW)
        self.play(FadeIn(position), run_time=0.25)
        small_net = self.make_network(cx=2.1, cy=-0.1, scale=0.62, labels=False)
        self.play(LaggedStart(*[Create(edge["mob"]) for edge in small_net["edges"]],
                              lag_ratio=0.008, run_time=1.25),
                  LaggedStart(*[FadeIn(node, scale=0.7)
                                for layer in small_net["layers"] for node in layer],
                              lag_ratio=0.04, run_time=1.1))
        in_tags = VGroup(tex("x", 23, BLUE).next_to(small_net["layers"][0][0], LEFT, buff=0.15),
                         tex("y", 23, GREEN).next_to(small_net["layers"][0][1], LEFT, buff=0.15))
        out_formula = tex(r"V(x,y;w_j)", 30, YELLOW).next_to(small_net["layers"][-1][0], RIGHT, buff=0.2)
        coords = tex(r"(x_1,y_1)", 21, YELLOW).next_to(position, UP + RIGHT, buff=0.12)
        self.play(FadeIn(in_tags), Write(out_formula), run_time=0.6)
        link = Arrow(position.get_center(), small_net["layers"][0][0].get_center(),
                     buff=0.12, color=BLUE, stroke_width=1.6)
        self.play(GrowArrow(link), run_time=0.4)
        input_pulse = Dot(position.get_center(), radius=0.065, color=YELLOW)
        self.add(input_pulse)
        self.play(MoveAlongPath(input_pulse, link, rate_func=linear), run_time=0.75)
        self.remove(input_pulse)
        self.play(FadeIn(coords), run_time=0.2)
        end_position = domain_points[(4, 2)].get_center()
        probe_path = ArcBetweenPoints(position.get_center(), end_position, angle=PI/4)
        coords_2 = tex(r"(x_2,y_2)", 21, YELLOW).next_to(end_position, UP + RIGHT, buff=0.12)
        formula_2 = tex(r"V(x_2,y_2;w_j)", 30, YELLOW).move_to(out_formula)
        self.play(MoveAlongPath(position, probe_path, rate_func=linear),
                  Transform(coords, coords_2), Transform(out_formula, formula_2),
                  run_time=1.0)
        self.play(Indicate(out_formula, color=YELLOW), run_time=0.45)
        self.end_beat(9)

        # 11. Vary parameters while the two residual indicators decrease.
        self.begin_beat(10, "adjust_parameters_to_constraints")
        self.play(FadeOut(VGroup(domain_frame, domain_lines, domain_dots, position,
                                 small_net["group"], in_tags, out_formula, link, coords)), run_time=0.45)
        region, rlines, rnodes, _ = self.make_grid(center=(-4.35, -0.1), side=2.7, n=6)
        self.play(Create(region), Create(rlines), FadeIn(rnodes, lag_ratio=0.018), run_time=1.1)
        boundary_ring = SurroundingRectangle(region, buff=0.04, color=GREEN, stroke_width=2.4)
        self.play(Create(boundary_ring), run_time=0.35)
        parameter_title = ar("معاملات قابلة للتعديل", 20, WHITE).move_to([2.65, 2.12, 0])
        slider_w = Line([0.95, 1.48, 0], [4.1, 1.48, 0], color="#586775", stroke_width=2)
        slider_b = Line([0.95, 0.88, 0], [4.1, 0.88, 0], color="#586775", stroke_width=2)
        knob_w = Dot([1.7, 1.48, 0], radius=0.09, color=YELLOW)
        knob_b = Dot([3.4, 0.88, 0], radius=0.09, color=BLUE)
        label_w = tex("w_j", 23, YELLOW).next_to(slider_w, LEFT, buff=0.15)
        label_b = tex("b", 23, BLUE).next_to(slider_b, LEFT, buff=0.15)
        inside_text = VGroup(ar("داخل النطاق", 19, WHITE),
                             tex(r"\nabla^2V\approx0", 23, YELLOW)).arrange(RIGHT, buff=0.22)
        boundary_text = VGroup(ar("على الحدود", 19, WHITE),
                               tex("V=V_b", 23, GREEN)).arrange(RIGHT, buff=0.22)
        inside_text.move_to([2.7, 0.15, 0])
        boundary_text.move_to([2.7, -0.72, 0])
        bar_bg_1 = RoundedRectangle(width=3.2, height=0.18, corner_radius=0.08,
                                    stroke_width=0, fill_color="#34414A", fill_opacity=1).move_to([2.8, -0.15, 0])
        bar_bg_2 = bar_bg_1.copy().move_to([2.8, -1.02, 0])
        bar_1 = Rectangle(width=2.7, height=0.12, stroke_width=0,
                          fill_color=YELLOW, fill_opacity=1).move_to(
                              bar_bg_1.get_left() + RIGHT * 1.35)
        bar_2 = Rectangle(width=2.45, height=0.12, stroke_width=0,
                          fill_color=GREEN, fill_opacity=1).move_to(
                              bar_bg_2.get_left() + RIGHT * 1.225)
        self.play(FadeIn(parameter_title), Create(slider_w), Create(slider_b),
                  FadeIn(knob_w), FadeIn(knob_b), FadeIn(label_w), FadeIn(label_b),
                  FadeIn(inside_text), FadeIn(boundary_text), FadeIn(bar_bg_1),
                  FadeIn(bar_bg_2), FadeIn(bar_1), FadeIn(bar_2), run_time=0.9)
        self.play(knob_w.animate.move_to([3.65, 1.48, 0]),
                  knob_b.animate.move_to([1.45, 0.88, 0]),
                  bar_1.animate.stretch(0.28, dim=0).align_to(bar_bg_1, LEFT),
                  bar_2.animate.stretch(0.24, dim=0).align_to(bar_bg_2, LEFT),
                  run_time=1.3)
        self.play(Indicate(inside_text, color=YELLOW), Indicate(boundary_text, color=GREEN),
                  run_time=0.6)
        self.end_beat(10)

        # 12. Replace sampled dots with a continuous scalar map and move freely.
        self.begin_beat(11, "continuous_approximation")
        self.play(FadeOut(VGroup(region, rlines, rnodes, boundary_ring,
                                 parameter_title, slider_w, slider_b, knob_w, knob_b,
                                 label_w, label_b, inside_text, boundary_text,
                                 bar_bg_1, bar_bg_2, bar_1, bar_2)), run_time=0.5)
        map_center = np.array([-3.15, -0.05, 0.0])
        map_width, map_height = 4.25, 3.5
        # V=x is a valid harmonic example (nabla^2 V = 0), used only to render
        # a continuous scalar map; no trained output or numeric training result is claimed.
        x_values = np.linspace(-1.0, 1.0, 160)
        values = np.tile(x_values, (110, 1))
        field = ScalarFieldImage(values, width=map_width, height=map_height,
                                 center=map_center, cmap=diverging_rgb, vmax=1.0, gamma=0.7)
        map_frame = Rectangle(width=map_width, height=map_height, stroke_color=BLUE,
                              stroke_width=1.8).move_to(map_center)
        contours = VGroup(*[
            Line([map_center[0] + x * map_width / 2, map_center[1] - map_height / 2, 0],
                 [map_center[0] + x * map_width / 2, map_center[1] + map_height / 2, 0],
                 color=WHITE, stroke_width=1.0, stroke_opacity=0.42)
            for x in (-0.55, 0.0, 0.55)
        ])
        x_axis = Arrow([map_center[0] - map_width/2, map_center[1] - map_height/2 - 0.2, 0],
                       [map_center[0] + map_width/2, map_center[1] - map_height/2 - 0.2, 0],
                       buff=0, color=GREY, stroke_width=1.5)
        x_label = tex("x", 22, BLUE).next_to(x_axis.get_end(), RIGHT, buff=0.08)
        y_axis = Arrow([map_center[0] - map_width/2 - 0.2, map_center[1] - map_height/2, 0],
                       [map_center[0] - map_width/2 - 0.2, map_center[1] + map_height/2, 0],
                       buff=0, color=GREY, stroke_width=1.5)
        y_label = tex("y", 22, GREEN).next_to(y_axis.get_end(), UP, buff=0.08)
        final_net = self.make_network(cx=3.15, cy=-0.05, scale=0.47, labels=False)
        final_input_labels = VGroup(tex("x", 18, BLUE).next_to(final_net["layers"][0][0], LEFT, buff=0.05),
                                    tex("y", 18, GREEN).next_to(final_net["layers"][0][1], LEFT, buff=0.05))
        final_output = tex(r"V(x_1,y_1;w_j)", 22, YELLOW).next_to(final_net["layers"][-1][0], RIGHT, buff=0.1)
        map_title = ar("تقريب متصل للجهد", 21, WHITE).move_to([map_center[0], 2.05, 0])
        self.play(FadeIn(field), Create(map_frame), Create(contours), Create(x_axis), Create(y_axis),
                  FadeIn(x_label), FadeIn(y_label), FadeIn(map_title), run_time=1.1)
        self.play(LaggedStart(*[Create(edge["mob"]) for edge in final_net["edges"]],
                              lag_ratio=0.01, run_time=1.2),
                  LaggedStart(*[FadeIn(node, scale=0.75)
                                for layer in final_net["layers"] for node in layer],
                              lag_ratio=0.05, run_time=1.0),
                  FadeIn(final_input_labels), Write(final_output), run_time=1.4)
        probe_path = ArcBetweenPoints([-4.9, -0.72, 0], [-1.55, 0.83, 0], angle=-PI/5)
        final_probe = Dot(probe_path.get_start(), radius=0.095, color=YELLOW)
        final_coords = tex(r"(x_1,y_1)", 18, YELLOW).next_to(final_probe, UP + RIGHT, buff=0.1)
        self.play(FadeIn(final_probe), FadeIn(final_coords), run_time=0.2)
        new_probe_position = probe_path.get_end()
        coords_target = tex(r"(x_2,y_2)", 18, YELLOW).next_to(new_probe_position, UP + RIGHT, buff=0.1)
        output_target = tex(r"V(x_2,y_2;w_j)", 22, YELLOW).move_to(final_output)
        self.play(MoveAlongPath(final_probe, probe_path, rate_func=linear),
                  Transform(final_coords, coords_target),
                  Transform(final_output, output_target), run_time=1.6)
        self.play(Flash(final_output, color=YELLOW, flash_radius=0.3), run_time=0.45)
        self.end_beat(11)

        self.finish_scene()


def run_isolated(scene_type, name):
    """Render through PyCharm without sharing Manim's temporary files with another run."""
    run_id = f"{os.getpid()}_{uuid.uuid4().hex[:8]}"
    work = ROOT / "media" / name / "runs" / run_id
    config.media_dir = str(work)
    config.text_dir = str(work / "texts")
    config.tex_dir = str(work / "Tex")
    config.partial_movie_dir = str(work / "partial_movie_files")
    config.images_dir = str(ROOT / "review")

    temporary_name = f"{name}__{run_id}"
    config.output_file = temporary_name
    scene = scene_type()
    scene.render()

    rendered_file = Path(scene.renderer.file_writer.movie_file_path)
    final_file = ROOT / "videos" / f"{name}.mp4"
    final_file.parent.mkdir(parents=True, exist_ok=True)
    os.replace(rendered_file, final_file)
    print(f"[{name}] video: {final_file}")

    if OPEN_AFTER_RENDER and os.environ.get("POISSON_BATCH") != "1":
        _open(final_file)
    return scene


if __name__ == "__main__":
    run_isolated(MachineLearningPotentialIntro, name="scene_11_ml_intro_highlevel")
