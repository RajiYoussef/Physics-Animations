"""S15 — What the local law says. Standalone Manim Community scene.

Run this file with PyCharm's Run button, or:
    python -m manim -p -qh -r 1920,1080 --fps 30 gauss_scene15.py GaussScene15

Optional audio beside this file: S15_ar.wav (full timeline, starting after the
1-second setup), or S15_B01_ar.wav, S15_B02_ar.wav, S15_B03_ar.wav.
Otherwise the scene renders silently. Arabic is shaped via MarkupText/Arial.
"""
from pathlib import Path
from html import escape
import contextlib
import subprocess
import sys
import wave
import numpy as np
from manim import *

DARK = '#101820'
WHITEISH = '#F5F5F5'
GOLD = '#F6C85F'
CYAN = '#58C4DD'
VIOLET = '#C792EA'
RED = '#FF6B6B'
BLUE = '#64B5F6'


def wav_duration(path):
    try:
        with contextlib.closing(wave.open(str(path), 'rb')) as sound:
            return sound.getnframes() / float(sound.getframerate())
    except (OSError, wave.Error, ZeroDivisionError):
        return 0.0


class GaussScene15(Scene):
    """Two side-by-side local-field comparisons; exactly 57 s when silent."""

    def ar(self, text, size=27, color=WHITEISH, max_width=None):
        result = MarkupText(escape(text), font='Arial', font_size=size, color=color)
        if max_width is not None and result.width > max_width:
            result.scale_to_fit_width(max_width)
        return result

    def play_t(self, animation, duration):
        self.play(animation, run_time=duration)
        self.clock += duration

    def wait_t(self, duration):
        if duration > 0.00001:
            self.wait(duration)
            self.clock += duration

    def start_beat(self, index):
        if self.audio_mode == 'beats':
            self.add_sound(str(self.beat_audio[index]))
        self.beat_end = self.clock + self.lengths[index]

    def end_beat(self, last=False):
        remaining = self.beat_end - self.clock
        if remaining < -0.001:
            raise ValueError(f'Beat animation overran its allowance by {-remaining:.2f}s')
        if last and remaining >= 0.5:
            self.wait_t(remaining - 0.5)
            self.play_t(FadeOut(Group(*list(self.mobjects))), 0.5)
        else:
            self.wait_t(max(0.0, remaining))

    def make_layout(self):
        # Video geometry: 14.22 x 8.0. All substantive text above y=-2.85.
        self.title = self.ar('ماذا تخبرنا الصيغة المحلية؟', size=37, max_width=11.7)
        self.title.move_to([0, 3.25, 0])

        self.left_x, self.right_x = -3.40, 3.40
        self.panel_y = 0.53
        self.panel_w, self.panel_h = 6.28, 3.80
        self.left_panel = RoundedRectangle(corner_radius=0.14, width=self.panel_w,
                         height=self.panel_h, stroke_color=CYAN, stroke_width=2,
                         fill_color=CYAN, fill_opacity=0.035).move_to([self.left_x, self.panel_y, 0])
        self.right_panel = RoundedRectangle(corner_radius=0.14, width=self.panel_w,
                         height=self.panel_h, stroke_color=CYAN, stroke_width=2,
                         fill_color=CYAN, fill_opacity=0.035).move_to([self.right_x, self.panel_y, 0])

        self.left_name = self.ar('كثافة شحنة موجبة', 28, max_width=5.7).move_to([self.left_x, 1.98, 0])
        self.right_name = self.ar('منطقة خالية من الشحنة', 28, max_width=5.7).move_to([self.right_x, 1.98, 0])
        self.uniform_name = self.ar('مجال منتظم', 24, max_width=5.5).move_to([self.right_x, 1.48, 0])
        self.positive_name = self.ar('تباعد موجب', 23, color=RED).move_to([self.left_x, -0.99, 0])
        self.zero_name = self.ar('تباعد صفري', 23, color=BLUE).move_to([self.right_x, -0.99, 0])

        # Positive uniform volume density: E = k * position in a small region.
        # All arrows point away from the center; longer arrows start farther away.
        self.left_origin = np.array([self.left_x, 0.50, 0.])
        self.charges = VGroup()
        for dx, dy in [(-1.45,.62), (-.65,.85), (.15,.85), (1.1,.7),
                       (-1.25,-.55), (-.4,-.4), (.6,-.6), (1.4,-.4)]:
            plus = MathTex('+', color=RED, font_size=19)
            plus.move_to(self.left_origin + np.array([dx, dy, 0]))
            self.charges.add(plus)

        self.outward = VGroup()
        for dx, dy in [(-1.7,.65),(-1.0,-.85),(-.55,.9),(.50,-.85),
                       (1.7,.60),(1.55,-.60),(.65,.95),(-1.6,-.20)]:
            vec = np.array([dx, dy, 0.], dtype=float)
            unit = vec / np.linalg.norm(vec)
            # A transparent arrow origin at the sample location, not a point source.
            start = self.left_origin + vec * .69
            length = .22 + .21 * np.linalg.norm(vec)
            self.outward.add(Arrow(start, start + length * unit, buff=0,
                            color=GOLD, stroke_width=4.0,
                            max_tip_length_to_length_ratio=.28))
        self.local_region = DashedVMobject(Circle(radius=.40, color=VIOLET,
                                                 stroke_width=2).move_to(self.left_origin),
                                            num_dashes=16)

        # Charge-free uniform field: parallel, nonzero arrows of equal length.
        self.parallel = VGroup()
        for yy in (-.30, .12, .54, .96):
            for xx in (-1.65, -.35, .95):
                point = np.array([self.right_x + xx, yy, 0])
                self.parallel.add(Arrow(point, point + .66 * RIGHT,
                                       color=GOLD, buff=0, stroke_width=4.0,
                                       max_tip_length_to_length_ratio=.24))
        self.right_local_region = DashedVMobject(Circle(radius=.40,
                    color=VIOLET, stroke_width=2).move_to([self.right_x, .45, 0]), num_dashes=16)

        # Dedicated math baseline below each panel; no objects share this space.
        self.positive_eq = MathTex(r'\rho_v>0\ \Longrightarrow\ \nabla\cdot\mathbf E>0',
                                   font_size=34, color=WHITEISH).move_to([self.left_x, -1.77, 0])
        self.zero_eq = MathTex(r'\rho_v=0\ \Longrightarrow\ \nabla\cdot\mathbf E=0',
                               font_size=34, color=WHITEISH).move_to([self.right_x, -1.77, 0])
        self.constant_eq = MathTex(r'\mathbf E=\text{constant}\ \Longrightarrow\ \nabla\cdot\mathbf E=0',
                                  font_size=29, color=WHITEISH).move_to([self.right_x, -1.77, 0])
        for equation in (self.positive_eq, self.zero_eq, self.constant_eq):
            if equation.width > 6.05:
                equation.scale_to_fit_width(6.05)

        # Question is shown only in the hold of B02, and remains in B03.
        self.question = self.ar('هل يمكن لكثافة شحنة موجبة ومنتظمة أن تقترن بمجال كهربائي منتظم؟',
                                size=27, max_width=12.6).move_to([0, -2.44, 0])
        self.answer = self.ar('لا', size=37, color=RED).move_to([0, -2.81, 0])

    def beat1(self):
        self.start_beat(0)
        self.play_t(Create(self.left_panel), 0.8)
        self.play_t(FadeIn(self.left_name), 0.55)
        self.play_t(FadeIn(self.charges), 0.85)
        self.play_t(FadeIn(self.outward), 1.0)
        self.play_t(Create(self.local_region), 0.7)
        self.play_t(Write(self.positive_eq), 1.3)
        self.play_t(FadeIn(self.positive_name), 0.6)
        self.play_t(Indicate(self.positive_eq, color=RED, scale_factor=1.03), 1.2)
        # The spoken negative-density comparison is conceptual; no new equation.
        self.end_beat()

    def beat2(self):
        self.start_beat(1)
        self.play_t(Create(self.right_panel), 0.8)
        self.play_t(FadeIn(self.right_name), 0.55)
        self.play_t(FadeIn(self.uniform_name), 0.5)
        self.play_t(FadeIn(self.parallel), 1.1)
        self.play_t(Create(self.right_local_region), 0.65)
        self.play_t(Write(self.zero_eq), 1.4)
        self.play_t(FadeIn(self.zero_name), 0.55)
        self.play_t(Indicate(self.parallel, color=GOLD, scale_factor=1.0), 1.1)
        # Display the question during the final three-second reading hold.
        self.wait_t(max(0., self.beat_end - self.clock - 3.0))
        self.play_t(FadeIn(self.question), 0.7)
        self.end_beat()

    def beat3(self):
        self.start_beat(2)
        self.play_t(FadeIn(self.answer, scale=.85), 0.75)
        self.play_t(ReplacementTransform(self.zero_eq, self.constant_eq), 1.5)
        self.play_t(Indicate(self.constant_eq, color=BLUE, scale_factor=1.03), 1.2)
        self.play_t(Indicate(self.positive_eq, color=RED, scale_factor=1.03), 1.2)
        self.play_t(Circumscribe(self.answer, color=RED, fade_out=True), 1.2)
        self.end_beat(last=True)

    def construct(self):
        self.camera.background_color = DARK
        self.clock = 0.0
        base = Path(__file__).resolve().parent
        self.audio_mode = 'silent'
        self.lengths = [15.0, 18.0, 23.0]
        self.beat_audio = [base / f'S15_B0{i}_ar.wav' for i in (1, 2, 3)]
        whole = base / 'S15_ar.wav'
        if whole.exists():
            self.audio_mode = 'whole'
            self.lengths[-1] += max(0.0, wav_duration(whole) - 56.0)
        elif all(p.exists() for p in self.beat_audio):
            self.audio_mode = 'beats'
            self.lengths = [max(sp, wav_duration(path)) + hold for path, sp, hold in zip(
                            self.beat_audio, (12., 15., 19.), (3., 3., 4.))]
        else:
            print('S15: optional narration missing; silent preview mode.')
        print(f'S15 duration: {1 + sum(self.lengths):.3f} seconds; beats {self.lengths}')

        self.make_layout()
        self.play_t(FadeIn(self.title), .8)
        self.wait_t(.2)
        if self.audio_mode == 'whole':
            self.add_sound(str(whole))
        self.beat1()
        self.beat2()
        self.beat3()
        expected = 1.0 + sum(self.lengths)
        assert abs(self.clock - expected) < .06, (self.clock, expected)


if __name__ == '__main__':
    subprocess.run([
        sys.executable, '-m', 'manim', '-p', '-qh', '-r', '1920,1080',
        '--fps', '30', str(Path(__file__).resolve()), 'GaussScene15'
    ], check=True)
