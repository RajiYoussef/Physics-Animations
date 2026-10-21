"""Gauss Scene 13: reading the solid sphere's field as a graph.

Standalone Manim Community scene. Run this file in PyCharm, or use:
python -m manim -p -qh -r 1920,1080 --fps 30 gauss_scene13.py GaussScene13

Optional: S13_B01_ar.wav, S13_B02_ar.wav, S13_B03_ar.wav (all three),
or S13_ar.wav (one continuous recording aligned with the planned beat cues).
Without them the animation is a silent 60-second preview.
"""
from pathlib import Path
from html import escape
import sys
import subprocess
import wave
from contextlib import closing

from manim import *
import numpy as np

BG = '#101820'
INK = '#F5F5F5'
GOLD = '#F6C85F'
CYAN = '#58C4DD'
VIOLET = '#C792EA'
RED = '#FF6B6B'
ARABIC_FONT = 'Arial'


def wav_duration(path):
    if not path.exists():
        return 0.0
    try:
        with closing(wave.open(str(path), 'rb')) as wav:
            return wav.getnframes() / wav.getframerate()
    except (OSError, wave.Error, ZeroDivisionError):
        return 0.0


class GaussScene13(Scene):
    def ar(self, s, size=24, color=INK):
        return MarkupText(escape(s), font=ARABIC_FONT,
                          font_size=size, color=color)

    def run_anim(self, anim, duration):
        self.play(anim, run_time=duration)
        self.clock += duration

    def rest(self, duration):
        if duration > 1e-6:
            self.wait(duration)
            self.clock += duration

    def begin_beat(self, index):
        self.end_beat_time = self.clock + self.lengths[index]
        if self.audio_mode == 'beats':
            self.add_sound(str(self.clips[index]))

    def close_beat(self, fade=False):
        remaining = self.end_beat_time - self.clock
        if remaining < -0.05:
            raise RuntimeError(f'Beat exceeded its allotted time by {-remaining:.2f} seconds')
        if fade and remaining >= .5:
            self.rest(remaining - .5)
            self.run_anim(FadeOut(Group(*list(self.mobjects))), .5)
        else:
            self.rest(max(remaining, 0))

    def configure_audio(self):
        root = Path(__file__).resolve().parent
        self.clips = [root / f'S13_B0{i}_ar.wav' for i in (1, 2, 3)]
        whole = root / 'S13_ar.wav'
        self.audio_mode = 'silent'
        self.lengths = [23.0, 16.0, 20.0]
        if whole.exists():
            self.audio_mode = 'whole'
            duration = wav_duration(whole)
            # One file is aligned by the narrator to planned starts: 1, 24, 40 s.
            # Extend the final hold if the complete audio runs beyond 60 s.
            self.lengths[2] += max(0., duration - 59.)
            print(f'S13 continuous audio: {duration:.2f}s; duration: {1+sum(self.lengths):.2f}s')
        elif all(path.exists() for path in self.clips):
            self.audio_mode = 'beats'
            speech = [20., 13., 16.]
            holds = [3., 3., 4.]
            self.lengths = [max(s, wav_duration(path)) + hold
                            for path, s, hold in zip(self.clips, speech, holds)]
            print(f'S13 beat audio: {[round(wav_duration(p),2) for p in self.clips]}; '
                  f'duration: {1+sum(self.lengths):.2f}s; '
                  f'beat starts: {1:.2f}, {1+self.lengths[0]:.2f}, '
                  f'{1+self.lengths[0]+self.lengths[1]:.2f}')
        else:
            print('S13: silent preview, total 60.00s')
        return whole

    def construct(self):
        self.camera.background_color = BG
        self.clock = 0.0
        whole = self.configure_audio()
        self.setup_art()

        # Silent opening; do not start narration until second 1.
        self.run_anim(FadeIn(self.title), .7)
        self.rest(.3)
        if self.audio_mode == 'whole':
            self.add_sound(str(whole))

        self.beat_one()
        self.beat_two()
        self.beat_three()
        assert abs(self.clock - (1 + sum(self.lengths))) < 0.05

    def setup_art(self):
        self.title = self.ar('قراءة نتيجة الكرة على رسم بياني', 37)
        self.title.move_to([0, 3.25, 0])

        # Left: charged solid sphere cross-section and a movable observation point.
        self.center = np.array([-4.38, -0.08, 0])
        self.charge_rad = 1.18
        self.point_dist_per_a = 0.76  # r=3a remains safely in left panel
        self.sphere = Circle(radius=self.charge_rad, color=CYAN,
                             stroke_width=2.7, fill_color=CYAN,
                             fill_opacity=.22).move_to(self.center)
        self.plus = VGroup(*[
            MathTex('+', color=RED, font_size=23).move_to(
                self.center + np.array([x, y, 0]))
            for x, y in [(-.45,.35),(.15,.59),(-.37,-.38),(.51,-.26),(.16,.03)]
        ])
        self.r_a_segment = Line(self.center, self.center + RIGHT*self.charge_rad,
                                color=INK, stroke_width=2)
        self.a_math = MathTex('a', font_size=28, color=INK).move_to(
            self.center + np.array([.66,.21,0]))
        self.center_dot = Dot(self.center, radius=.042, color=INK)
        self.observation = ValueTracker(0)
        self.point = always_redraw(lambda: Dot(
            self.center + RIGHT*self.observation.get_value()*self.point_dist_per_a,
            color=GOLD, radius=.095))
        self.moving_radius = always_redraw(lambda: Line(
            self.center,
            self.center + RIGHT*self.observation.get_value()*self.point_dist_per_a,
            stroke_width=2.7, color=GOLD))
        self.obs_label = self.ar('نقطة الرصد', 23).move_to([-4.3, -1.77, 0])
        self.inside_label = self.ar('داخل الكرة', 24, CYAN).move_to([-4.33, 1.61, 0])
        self.outside_label = self.ar('خارج الكرة', 24, GOLD).move_to([-4.33, 1.61, 0])
        self.surface_label = self.ar('سطح الكرة', 24).move_to([-4.3, -1.94, 0])
        self.region_label = self.inside_label

        # Right: normalized graph, 0..3 and 0..1.2.
        self.axes = Axes(
            x_range=[0, 3, 1], y_range=[0, 1.2, .4],
            x_length=4.5, y_length=2.14,
            axis_config={'color': INK, 'stroke_width': 2,
                         'include_tip': True, 'tip_width': .12, 'tip_height': .14},
            x_axis_config={'include_numbers': True, 'font_size': 21},
            y_axis_config={'include_numbers': True, 'font_size': 20},
        ).move_to([3.21, -.14, 0])
        self.axes.set_z_index(2)
        # Positions strictly tied to the same axes used by the curve and marker.
        self.curve_inside = self.axes.plot(lambda x: x, x_range=[0, 1],
                                           color=GOLD, stroke_width=5)
        self.curve_outside = self.axes.plot(lambda x: 1/(x*x), x_range=[1, 3],
                                            color=GOLD, stroke_width=5)
        self.curve_inside.set_z_index(3)
        self.curve_outside.set_z_index(3)
        self.graph_dot = always_redraw(lambda: Dot(
            self.axes.c2p(self.observation.get_value(),
                          self.field_ratio(self.observation.get_value())),
            color=VIOLET, radius=.083).set_z_index(6))
        self.join_dot = Dot(self.axes.c2p(1, 1), radius=.105, color=VIOLET)
        self.surface_guide = DashedLine(self.axes.c2p(1,0), self.axes.c2p(1,1),
                                        color=VIOLET, dash_length=.13,
                                        stroke_width=2)
        self.x_prose = self.ar('المسافة مقسومة على نصف القطر', 20)
        self.x_prose.move_to([3.25, -1.65, 0])
        self.y_prose = self.ar('المجال مقسومًا على قيمته عند السطح', 20)
        self.y_prose.move_to([3.23, 1.88, 0])
        self.x_math = MathTex('r/a', font_size=27).next_to(self.axes.x_axis.get_end(),
                                                         RIGHT, buff=.08)
        self.y_math = MathTex('E_r/E_a', font_size=25).next_to(self.axes.y_axis.get_end(),
                                                              UP, buff=.08)
        self.ea = MathTex(r'E_a=\frac{Q}{4\pi\epsilon_0 a^2}\quad(Q>0)',
                          font_size=28, color=INK).move_to([3.2, 2.45, 0])
        self.piecewise = MathTex(
            r'\frac{E_r}{E_a}=\begin{cases}r/a,&0\le r/a\le1,\\'
            r'(r/a)^{-2},&r/a\ge1.\end{cases}',
            font_size=26, color=INK)
        self.piecewise.move_to([3.2, -2.24, 0])
        self.boundary = MathTex(r'E_r(a)=\frac{Q}{4\pi\epsilon_0 a^2}',
                                font_size=28, color=INK).move_to([-3.85,-2.30,0])
        self.continuity = self.ar('متصل عند السطح', 24, VIOLET).move_to([-4.25,2.08,0])

    @staticmethod
    def field_ratio(x):
        # Never evaluate 1/x^2 at zero.
        return x if x <= 1 else 1/(x*x)

    def beat_one(self):
        self.begin_beat(0)
        self.run_anim(FadeIn(self.sphere, self.plus, self.center_dot), 1.0)
        self.run_anim(Create(self.r_a_segment), .4)
        self.run_anim(FadeIn(self.a_math, self.inside_label), .6)
        self.run_anim(FadeIn(self.ea), 1.0)
        self.run_anim(Create(self.axes), 1.1)
        self.run_anim(FadeIn(self.x_math, self.y_math), .5)
        self.run_anim(FadeIn(self.x_prose), .45)
        self.run_anim(FadeIn(self.y_prose), .45)
        self.add(self.moving_radius, self.point, self.graph_dot)
        # Moving the point and tracing the linear branch are one linked action.
        self.run_anim(AnimationGroup(
            self.observation.animate.set_value(1),
            Create(self.curve_inside), lag_ratio=0), 7.0)
        self.run_anim(FadeIn(self.surface_label), .5)
        self.rest(1.0)
        self.close_beat()

    def beat_two(self):
        self.begin_beat(1)
        self.run_anim(FadeOut(self.inside_label), .35)
        self.run_anim(FadeIn(self.outside_label), .4)
        self.run_anim(AnimationGroup(
            self.observation.animate.set_value(3),
            Create(self.curve_outside), lag_ratio=0), 6.0)
        self.run_anim(FadeOut(self.x_prose), .4)
        self.run_anim(FadeIn(self.piecewise), 1.1)
        self.run_anim(Indicate(self.curve_outside, color=GOLD, scale_factor=1.01), 1.0)
        self.close_beat()

    def beat_three(self):
        self.begin_beat(2)
        self.run_anim(self.observation.animate.set_value(1), 1.7)
        self.run_anim(Create(self.surface_guide), .65)
        self.run_anim(FadeIn(self.join_dot), .4)
        self.run_anim(FadeOut(self.surface_label), .3)
        self.run_anim(FadeIn(self.boundary), .7)
        self.run_anim(FadeIn(self.continuity), .55)
        self.run_anim(Indicate(self.join_dot, color=VIOLET, scale_factor=1.3), 1.2)
        # Make the shared surface value visually explicit, without smoothing its corner.
        self.run_anim(Indicate(self.boundary, color=GOLD, scale_factor=1.04), 1.0)
        self.close_beat(fade=True)


if __name__ == '__main__':
    subprocess.run([
        sys.executable, '-m', 'manim', '-p', '-qh', '-r', '1920,1080', '--fps', '30',
        str(Path(__file__).resolve()), 'GaussScene13'
    ], check=True)
