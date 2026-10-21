"""S14 — From integral Gauss law to differential Gauss law.
Standalone Manim Community scene. Run this file directly in PyCharm.
Optional audio in the same folder: S14_ar.wav OR all of
S14_B01_ar.wav, S14_B02_ar.wav, S14_B03_ar.wav.
Silent preview: exactly 53 seconds (1 + 14 + 17 + 21).
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import subprocess
import sys
import wave

import numpy as np
from manim import *

BG = '#101820'
INK = '#F5F5F5'
GOLD = '#F6C85F'
CYAN = '#58C4DD'
VIOLET = '#C792EA'
RED = '#FF6B6B'
BLUE = '#64B5F6'


def duration_wav(path):
    try:
        with wave.open(str(path), 'rb') as f:
            return f.getnframes() / f.getframerate()
    except (OSError, wave.Error, ZeroDivisionError):
        return 0.0


class GaussScene14(Scene):
    def ar(self, s, size=25, color=INK):
        # MarkupText is required for Arabic shaping on this Windows/Manim setup.
        return MarkupText(escape(s), font='Arial', font_size=size, color=color)

    def timed(self, anim, seconds):
        self.play(anim, run_time=seconds)
        self.clock += seconds

    def pause(self, seconds):
        if seconds > 1e-6:
            self.wait(seconds)
            self.clock += seconds

    def begin_beat(self, index):
        self.beat_finish = self.clock + self.beats[index]
        if self.mode == 'clips':
            self.add_sound(str(self.clips[index]))

    def end_beat(self, last=False):
        remaining = self.beat_finish - self.clock
        if remaining < -0.04:
            raise RuntimeError(f'Beat exceeds allotted time: {-remaining:.3f} s')
        if last and remaining >= 0.5:
            self.pause(remaining - 0.5)
            self.timed(FadeOut(Group(*list(self.mobjects))), 0.5)
        else:
            self.pause(max(0, remaining))

    def setup_audio(self):
        parent = Path(__file__).resolve().parent
        self.clips = [parent / f'S14_B0{i}_ar.wav' for i in range(1, 4)]
        whole = parent / 'S14_ar.wav'
        self.mode = 'silent'
        self.beats = [14.0, 17.0, 21.0]
        if whole.is_file():
            self.mode = 'whole'
            full_length = duration_wav(whole)
            # Whole narration is one file, beginning at t=1. Scheduled beat
            # cues remain at 1,15,32 seconds. Preserve any longer recording.
            self.beats[-1] += max(0.0, full_length - sum(self.beats))
            self.whole_file = whole
            print(f'S14 continuous WAV: {full_length:.2f}s; scene: {1+sum(self.beats):.2f}s')
            print('Continuous-clip narration cue starts are 1, 15, 32 seconds (planned).')
        elif all(p.is_file() for p in self.clips):
            self.mode = 'clips'
            speech = (11.0, 14.0, 17.0)
            holds = (3.0, 3.0, 4.0)
            self.beats = [max(s, duration_wav(p)) + h
                          for s, h, p in zip(speech, holds, self.clips)]
            starts = [1, 1+self.beats[0], 1+self.beats[0]+self.beats[1]]
            print('S14 beat clip durations:', [round(duration_wav(p), 2) for p in self.clips])
            print('Adjusted scene duration:', round(1+sum(self.beats), 2), 's; cue starts:', starts)
        else:
            print('S14 silent preview; duration 53.00s (1s setup + 14s + 17s + 21s).')

    def create_objects(self):
        self.title = self.ar('من الصيغة التكاملية إلى الصيغة التفاضلية', 37)
        self.title.move_to([0, 3.27, 0])
        if self.title.width > 11.7:
            self.title.scale_to_fit_width(11.7)

        # Diagram region: x in [-6.15, -1.20], y in [-1.95, 2.25].
        center = np.array([-3.75, 0.25, 0])
        theta = np.linspace(0, TAU, 38)
        points = [center + np.array([1.83*np.cos(t)*(1+0.065*np.sin(3*t)),
                                    1.29*np.sin(t)*(1+0.06*np.cos(2*t)), 0])
                  for t in theta]
        self.region = VMobject()
        self.region.set_points_smoothly(points)
        self.region.close_path()
        self.region.set_fill(CYAN, opacity=0.17)
        self.region.set_stroke(CYAN, width=4)
        self.Vmark = MathTex('V', color=INK, font_size=44).move_to(center + LEFT*.28)
        self.Smark = MathTex('S', color=CYAN, font_size=40).move_to([-1.78, 0.60, 0])

        self.boundary_caption = self.ar('السطح المحيط', 24, CYAN).move_to([-3.7, -1.76, 0])
        self.volume_caption = self.ar('الحجم المحصور', 24, INK).move_to([-3.7, -1.76, 0])
        self.theorem_caption = self.ar('مبرهنة التباعد', 26).move_to([2.75, 2.18, 0])
        self.surface_caption = self.ar('تكامل سطحي', 22, CYAN).move_to([1.02, 1.29, 0])
        self.volume_int_caption = self.ar('تكامل حجمي', 22, GOLD).move_to([4.70, 1.29, 0])
        self.every_caption = self.ar('كل حجم', 26, INK).move_to([-3.70, -1.82, 0])
        self.differential_caption = self.ar('الصيغة التفاضلية', 25, INK).move_to([2.75, -1.90, 0])

        # Colored outward normals and field arrows (smooth field; no singularity).
        self.normals = VGroup()
        for t in [0.15, 1.11, 2.34, 3.54, 4.53, 5.67]:
            p = center + np.array([1.82*np.cos(t), 1.28*np.sin(t), 0])
            vec = np.array([np.cos(t)/1.82, np.sin(t)/1.28, 0])
            vec /= np.linalg.norm(vec)
            self.normals.add(Arrow(p, p + .42*vec, buff=0, color=VIOLET,
                                  stroke_width=3.5, max_tip_length_to_length_ratio=.3))
        self.field = VGroup(*[
            Arrow(np.array([-4.75, y, 0]), np.array([-3.95, y+.06, 0]), buff=0,
                  color=GOLD, stroke_width=3.1, max_tip_length_to_length_ratio=.25)
            for y in (-.43, .35, 1.08)
        ])
        # The left-hand example regions replace the big illustrative volume in B03.
        self.small_regions = VGroup()
        for x, y, rx, ry in [(-5.05,.59,.48,.50), (-3.60,.58,.55,.38), (-2.75,-.57,.45,.52)]:
            shape = Ellipse(width=2*rx, height=2*ry, stroke_color=CYAN,
                            stroke_width=3, fill_color=CYAN, fill_opacity=.21)
            shape.move_to([x,y,0])
            self.small_regions.add(shape)
        self.small_Vs = VGroup(*[
            MathTex('V', color=INK, font_size=25).move_to(shape.get_center())
            for shape in self.small_regions
        ])

        # Fixed right equation region. No equation ever extends below -1.6.
        self.eq1 = MathTex(
            r'\oint_S\mathbf E\cdot d\mathbf S=\int_V\nabla\cdot\mathbf E\,dV',
            font_size=36, color=INK)
        self.eq2 = MathTex(
            r'\int_V\nabla\cdot\mathbf E\,dV=\frac{1}{\epsilon_0}\int_V\rho_v\,dV',
            font_size=34, color=INK)
        self.eq3 = MathTex(
            r'\int_V\left(\nabla\cdot\mathbf E-\frac{\rho_v}{\epsilon_0}\right)dV=0',
            font_size=34, color=INK)
        self.eq4 = MathTex(
            r'\nabla\cdot\mathbf E=\frac{\rho_v}{\epsilon_0}',
            font_size=41, color=INK)
        for eq in (self.eq1, self.eq2, self.eq3, self.eq4):
            if eq.width > 5.95:
                eq.scale_to_fit_width(5.95)
        self.eq1.move_to([2.75, .70, 0])
        self.eq2.move_to([2.75, -.55, 0])
        self.eq3.move_to([2.75, .83, 0])
        self.eq4.move_to([2.75, -.66, 0])
        self.answer_box = SurroundingRectangle(self.eq4, buff=.19, color=GOLD, stroke_width=3)

        # Color the integral terms, but not their mathematical meaning.
        self.eq1.set_color_by_tex(r'\oint_S', CYAN)
        self.eq1.set_color_by_tex(r'\int_V', GOLD)
        self.eq2.set_color_by_tex(r'\nabla\cdot\mathbf E', GOLD)
        self.eq2.set_color_by_tex(r'\rho_v', RED)
        self.eq3.set_color_by_tex(r'\rho_v', RED)
        self.eq4.set_color_by_tex(r'\rho_v', RED)

    def beat1(self):
        self.begin_beat(0)
        self.timed(Create(self.region), 1.25)
        self.timed(FadeIn(self.Vmark), .6)
        self.timed(FadeIn(self.Smark), .5)
        self.timed(FadeIn(self.boundary_caption), .5)
        self.timed(FadeIn(self.field), .8)
        self.timed(FadeIn(self.normals), .75)
        self.timed(FadeIn(self.theorem_caption), .5)
        self.timed(Write(self.eq1), 1.65)
        self.timed(FadeIn(self.surface_caption), .5)
        self.timed(FadeIn(self.volume_int_caption), .5)
        self.timed(Indicate(self.region, color=CYAN, scale_factor=1.02), 1.3)
        self.timed(ReplacementTransform(self.boundary_caption, self.volume_caption), .7)
        self.timed(Indicate(self.Vmark, color=GOLD, scale_factor=1.2), 1.0)
        self.end_beat()

    def beat2(self):
        self.begin_beat(1)
        self.timed(FadeOut(self.surface_caption), .5)
        self.timed(FadeOut(self.volume_int_caption), .5)
        self.timed(Write(self.eq2), 1.8)
        self.timed(Indicate(self.eq2, color=GOLD, scale_factor=1.015), 1.4)
        self.timed(Indicate(self.Vmark, color=CYAN, scale_factor=1.2), 1.2)
        self.end_beat()

    def beat3(self):
        self.begin_beat(2)
        self.timed(FadeOut(VGroup(self.region,self.normals,self.field,self.Smark,self.Vmark)), .9)
        self.timed(FadeOut(self.volume_caption), .4)
        self.timed(FadeIn(self.small_regions), .9)
        self.timed(FadeIn(self.small_Vs), .5)
        self.timed(FadeIn(self.every_caption), .5)
        self.timed(FadeOut(VGroup(self.eq1,self.eq2)), .75)
        self.timed(Write(self.eq3), 1.5)
        self.timed(Indicate(self.small_regions[0], color=CYAN), .7)
        self.timed(Indicate(self.small_regions[1], color=CYAN), .7)
        self.timed(Indicate(self.small_regions[2], color=CYAN), .7)
        self.timed(Write(self.eq4), 1.5)
        self.timed(Create(self.answer_box), .8)
        self.timed(FadeIn(self.differential_caption), .5)
        self.timed(Indicate(self.eq4, color=GOLD, scale_factor=1.035), 1.1)
        self.end_beat(last=True)

    def construct(self):
        self.camera.background_color = BG
        self.clock = 0.0
        self.setup_audio()
        self.create_objects()
        self.timed(FadeIn(self.title), .8)
        self.pause(.2)
        if self.mode == 'whole':
            self.add_sound(str(self.whole_file))
        self.beat1()
        self.beat2()
        self.beat3()
        assert abs(self.clock - (1+sum(self.beats))) < (1/30), (self.clock,self.beats)


if __name__ == '__main__':
    subprocess.run([
        sys.executable, '-m', 'manim', '-p', '-qh', '-r', '1920,1080',
        '--fps', '30', str(Path(__file__).resolve()), 'GaussScene14'
    ], check=True)
