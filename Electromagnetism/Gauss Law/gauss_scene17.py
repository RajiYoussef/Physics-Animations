"""GaussScene17 — arbitrary closed surfaces and superposition.

Click Run in PyCharm to render and open. Optional audio beside this script:
S17_ar.wav, or all of S17_B01_ar.wav, S17_B02_ar.wav, S17_B03_ar.wav.
A silent preview lasts exactly 76 seconds (at 30 fps).
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import contextlib
import subprocess
import sys
import wave

import numpy as np
from manim import *

BG = '#101820'
WHITEISH = '#F5F5F5'
GOLD = '#F6C85F'
CYAN = '#58C4DD'
VIOLET = '#C792EA'
POS = '#FF6B6B'
NEG = '#64B5F6'


def audio_duration(path: Path) -> float:
    if not path.is_file():
        return 0.0
    try:
        with contextlib.closing(wave.open(str(path), 'rb')) as wav:
            return wav.getnframes() / wav.getframerate()
    except (OSError, wave.Error, ZeroDivisionError):
        return 0.0


class GaussScene17(Scene):
    def arabic(self, s, size=25, color=WHITEISH, max_width=None):
        obj = MarkupText(escape(s), font='Arial', font_size=size, color=color)
        if max_width and obj.width > max_width:
            obj.scale_to_fit_width(max_width)
        return obj

    def equation(self, latex, size=34, max_width=6.00):
        obj = MathTex(latex, font_size=size, color=WHITEISH)
        if obj.width > max_width:
            obj.scale_to_fit_width(max_width)
        return obj

    def play_for(self, animation, duration):
        self.play(animation, run_time=duration)
        self.clock += duration

    def hold(self, duration):
        if duration > 1e-5:
            self.wait(duration)
            self.clock += duration

    def start_beat(self, index):
        if self.audio_mode == 'beats':
            self.add_sound(str(self.beat_clips[index]))
        self.beat_deadline = self.clock + self.beat_lengths[index]

    def end_beat(self, final=False):
        remaining = self.beat_deadline - self.clock
        if remaining < -0.06:
            raise RuntimeError(f'Beat exceeds allotted time by {-remaining:.2f}s')
        if final and remaining >= 0.5:
            self.hold(remaining - 0.5)
            self.play_for(FadeOut(Group(*list(self.mobjects))), 0.5)
        else:
            self.hold(max(0., remaining))

    def irregular(self, center, sx=2.0, sy=1.67):
        # Section of a closed 3D surface; not a line-integral path.
        polar = [(0, 1.0), (25, 1.01), (51, .88), (78, 1.05),
                 (105, .99), (132, .90), (161, 1.08), (190, .96),
                 (218, 1.03), (248, .92), (278, 1.09), (306, .98),
                 (332, .89), (354, 1.01)]
        pts = [np.array(center) + np.array([
            sx * rr * np.cos(aa * DEGREES),
            sy * rr * np.sin(aa * DEGREES), 0]) for aa, rr in polar]
        curve = VMobject()
        curve.set_points_smoothly(pts + [pts[0], pts[1]])
        curve.set_stroke(CYAN, width=3)
        curve.set_fill(CYAN, opacity=.14)
        return curve

    def build(self):
        self.title = self.arabic('سطح عام ومبدأ التراكب', 38).move_to([0, 3.28, 0])
        self.left_center = np.array([-3.67, -.18, 0])
        self.outer = self.irregular(self.left_center)
        self.source = self.left_center + np.array([-.20, .12, 0])
        self.small_r = .57
        self.ball_mask = Circle(self.small_r, stroke_width=0, fill_color=BG,
                                fill_opacity=1).move_to(self.source)
        self.small_sphere = Circle(self.small_r, color=CYAN, stroke_width=2.5).move_to(self.source)
        self.q_dot = Dot(self.source, radius=.105, color=POS)
        self.q_text = MathTex('+q', color=POS, font_size=26).next_to(self.q_dot, DOWN, buff=.10)
        self.outer_S = MathTex('S', color=CYAN, font_size=32).move_to([-1.73, .84, 0])
        self.inner_S = MathTex('S_b', color=CYAN, font_size=29).move_to([-2.72, .30, 0])
        self.b_line = Line(self.source, self.source + RIGHT * self.small_r,
                           color=WHITEISH, stroke_width=2)
        self.b_math = MathTex('b', font_size=26, color=WHITEISH).next_to(self.b_line, DOWN, buff=.05)
        self.outer_normals = VGroup()
        for ang in (45, 140, 228, 312):
            rad = ang * DEGREES
            p = self.left_center + np.array([1.97*np.cos(rad), 1.65*np.sin(rad), 0])
            direction = np.array([np.cos(rad), np.sin(rad), 0])
            self.outer_normals.add(Arrow(p, p+.42*direction, buff=0,
                                         color=VIOLET, stroke_width=3.0,
                                         max_tip_length_to_length_ratio=.32))
        self.inner_normals = VGroup()
        for ang in (60, 160, 285):
            vec = np.array([np.cos(ang*DEGREES), np.sin(ang*DEGREES), 0])
            p = self.source + .80*vec
            self.inner_normals.add(Arrow(p, p-.31*vec, buff=0,
                                         color=VIOLET, stroke_width=3.2,
                                         max_tip_length_to_length_ratio=.35))
        # A single label slot avoids accumulation under the illustration.
        self.label_between = self.arabic('المنطقة بين الحدّين', 25, max_width=5.3).move_to([-3.65, -2.68, 0])
        self.label_outer = self.arabic('السطح الخارجي', 25, max_width=5.3).move_to([-3.65, -2.68, 0])
        self.label_inner = self.arabic('السطح الداخلي', 25, max_width=5.3).move_to([-3.65, -2.68, 0])
        self.label_excluded = self.arabic('الكرة المستبعدة', 25, max_width=5.3).move_to([-3.65, -2.68, 0])
        self.label_outward = self.arabic('إلى خارج المنطقة المتبقية', 24, max_width=5.3).move_to([-3.65, -2.68, 0])
        self.label_outside = self.arabic('شحنة خارج السطح', 25, max_width=5.3).move_to([-3.65, -2.68, 0])
        self.label_superposition = self.arabic('التراكب', 26, max_width=5.3).move_to([-3.65, -2.68, 0])

        self.header = self.arabic('قانون غاوس', 29).move_to([3.28, 2.32, 0])
        self.eq1 = self.equation(r'0=\int_{V_{\mathrm{between}}}\nabla\cdot\mathbf E\,dV=\Phi_S-\Phi_b', 35).move_to([3.20, .55, 0])
        self.eq2 = self.equation(r'\Phi_S=\Phi_b=\frac{q}{\epsilon_0}', 38).move_to([3.20, .55, 0])
        self.eq3 = self.equation(r'q\text{ outside }S\ \Longrightarrow\ \Phi_S=0', 34).move_to([3.20, -.70, 0])
        self.eq4 = self.equation(r'\oint_S\left(\sum_i\mathbf E_i\right)\cdot d\mathbf S=\frac{1}{\epsilon_0}\sum_{i\,\mathrm{inside}}q_i=\frac{Q_{\mathrm{in}}}{\epsilon_0}',
                                  36, max_width=6.10).move_to([3.17, .22, 0])
        self.note = self.arabic('السطح المحيط مغلق في ثلاثة أبعاد', 22,
                                max_width=5.4).move_to([-3.65, 2.38, 0])

        self.outside_boundary = self.irregular([-3.98, -.20, 0], sx=1.60, sy=1.42)
        self.outside_q = Dot([-1.63, .28, 0], color=POS, radius=.11)
        self.outside_q_text = MathTex('+q', color=POS, font_size=28).next_to(self.outside_q, RIGHT, buff=.10)

        self.multi_boundary = self.irregular([-3.95, -.20, 0], sx=1.78, sy=1.48)
        self.charges = VGroup(
            Dot([-4.64, .27, 0], radius=.11, color=POS),
            Dot([-3.22, -.75, 0], radius=.11, color=NEG),
            Dot([-1.58, .55, 0], radius=.11, color=POS),
        )
        self.charge_names = VGroup(
            MathTex('q_1', color=POS, font_size=28).next_to(self.charges[0], UP, buff=.10),
            MathTex('q_2', color=NEG, font_size=28).next_to(self.charges[1], DOWN, buff=.10),
            MathTex('q_3', color=POS, font_size=28).next_to(self.charges[2], RIGHT, buff=.10),
        )
        self.field_sum = MathTex(r'\mathbf E=\sum_i\mathbf E_i', font_size=35, color=GOLD).move_to([3.2, 1.24, 0])
        self.final_box = SurroundingRectangle(self.eq4, buff=.19, color=CYAN, stroke_width=2.7)
        self.active_label = None

    def set_label(self, obj, duration=.5):
        if self.active_label is None:
            self.play_for(FadeIn(obj), duration)
        else:
            self.play_for(ReplacementTransform(self.active_label, obj), duration)
        self.active_label = obj

    def beat1(self):
        self.start_beat(0)
        self.play_for(FadeIn(self.note), .65)
        self.play_for(FadeIn(self.outer), 1.0)
        self.play_for(FadeIn(self.ball_mask), .25)
        self.play_for(Create(self.small_sphere), .60)
        self.play_for(FadeIn(self.q_dot, self.q_text), .50)
        self.play_for(FadeIn(self.outer_S, self.inner_S), .45)
        self.set_label(self.label_between, .55)
        self.play_for(FadeIn(self.outer_normals), .95)
        self.set_label(self.label_outer, .45)
        self.play_for(FadeIn(self.inner_normals), .85)
        self.set_label(self.label_outward, .55)
        self.play_for(Write(self.eq1), 1.45)
        self.play_for(Indicate(self.inner_normals, color=VIOLET), .85)
        self.set_label(self.label_excluded, .55)
        self.end_beat()

    def beat2(self):
        self.start_beat(1)
        self.play_for(ReplacementTransform(self.eq1, self.eq2), 1.25)
        self.play_for(Create(self.b_line), .45)
        self.play_for(FadeIn(self.b_math), .30)
        self.play_for(Indicate(self.small_sphere, color=CYAN), .85)
        self.play_for(Indicate(self.eq2, color=GOLD), .85)
        old_figure = Group(self.outer, self.ball_mask, self.small_sphere, self.q_dot,
                           self.q_text, self.outer_S, self.inner_S, self.outer_normals,
                           self.inner_normals, self.b_line, self.b_math)
        self.play_for(FadeOut(old_figure), .75)
        self.play_for(FadeIn(self.outside_boundary), .75)
        self.play_for(FadeIn(self.outside_q, self.outside_q_text), .65)
        self.set_label(self.label_outside, .50)
        self.play_for(Write(self.eq3), 1.35)
        self.play_for(Indicate(self.eq3, color=CYAN), 1.0)
        self.end_beat()

    def beat3(self):
        self.start_beat(2)
        self.play_for(FadeOut(Group(self.outside_boundary, self.outside_q,
                                    self.outside_q_text)), .70)
        self.play_for(FadeIn(self.multi_boundary), .75)
        self.play_for(FadeIn(self.charges, self.charge_names), .85)
        self.set_label(self.label_superposition, .50)
        self.play_for(FadeOut(self.eq2, self.eq3), .70)
        self.play_for(Write(self.field_sum), 1.0)
        self.play_for(Write(self.eq4), 2.0)
        self.play_for(Create(self.final_box), .9)
        self.play_for(Indicate(self.charges[:2], color=GOLD), 1.2)
        self.play_for(Indicate(self.charges[2], color=CYAN), .8)
        self.play_for(Indicate(self.eq4, color=GOLD), 1.25)
        self.end_beat(final=True)

    def construct(self):
        self.camera.background_color = BG
        self.clock = 0.0
        directory = Path(__file__).resolve().parent
        whole = directory / 'S17_ar.wav'
        self.beat_clips = [directory / f'S17_B0{i}_ar.wav' for i in (1, 2, 3)]
        spoken = [22., 20., 23.]
        holds = [3., 3., 4.]
        self.beat_lengths = [25., 23., 27.]
        self.audio_mode = 'silent'
        if whole.is_file():
            self.audio_mode = 'whole'
            duration = audio_duration(whole)
            if duration > sum(self.beat_lengths):
                self.beat_lengths[-1] += duration - sum(self.beat_lengths)
            print('S17 full narration duration:', duration,
                  's; paragraph cues are manually aligned to 1, 26 and 49 seconds.')
        elif all(x.is_file() for x in self.beat_clips):
            self.audio_mode = 'beats'
            self.beat_lengths = [max(spoken[i], audio_duration(self.beat_clips[i])) + holds[i]
                                 for i in range(3)]
        print('S17', self.audio_mode, 'timeline:', 1 + sum(self.beat_lengths), 'seconds')
        self.build()
        self.play_for(FadeIn(self.title), .8)
        self.hold(.2)
        if self.audio_mode == 'whole':
            self.add_sound(str(whole))
        self.beat1()
        self.beat2()
        self.beat3()
        assert abs(self.clock - (1 + sum(self.beat_lengths))) < .05


if __name__ == '__main__':
    subprocess.run([
        sys.executable, '-m', 'manim', '-p', '-qh',
        '-r', '1920,1080', '--fps', '30',
        str(Path(__file__).resolve()), 'GaussScene17'
    ], check=True)
