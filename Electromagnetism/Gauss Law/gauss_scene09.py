"""S09 — Cylindrical symmetry, rebuilt as an explicit physics explanation.
Run this file with PyCharm's Run button. Opens the finished video automatically.
Optional WAV: S09_ar.wav (complete recording) OR three S09_B0*_ar.wav files.
The default one-piece WAV paragraph cues are 0, 24 and 40 seconds within
the audio (scene times 1, 25 and 41). Set WHOLE_AUDIO_CUES to measured cues.
Blue arrows are hypothetical vector components compared under reflection,
not a time-varying electric field. The line is isolated, uniform and positive.
"""
from __future__ import annotations
from pathlib import Path
from html import escape
import contextlib
import subprocess
import sys
import wave
import numpy as np
from manim import *

DARK = "#101820"
WHITEISH = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
VIOLET = "#C792EA"
RED = "#FF6B6B"
BLUE = "#64B5F6"
ARABIC_FONT = "Arial"
WHOLE_AUDIO_CUES = (0.0, 24.0, 40.0)  # Seconds within S09_ar.wav.
PLANNED_BEATS = ((21.0, 3.0), (13.0, 3.0), (13.0, 4.0))


def wav_seconds(path):
    if not path.is_file():
        return 0.0
    try:
        with contextlib.closing(wave.open(str(path), "rb")) as audio:
            return audio.getnframes() / audio.getframerate()
    except (OSError, wave.Error, ZeroDivisionError, EOFError) as exc:
        raise ValueError(f"Cannot read narration WAV: {path}") from exc


def audio_plan(folder, cues=WHOLE_AUDIO_CUES):
    """Return mode, paths, and beat durations; never trim narration."""
    clips = [folder / f"S09_B0{i}_ar.wav" for i in (1, 2, 3)]
    whole = folder / "S09_ar.wav"
    lengths = [speech + hold for speech, hold in PLANNED_BEATS]
    if whole.is_file():
        duration = wav_seconds(whole)
        if (len(cues) != 3 or not all(np.isfinite(c) for c in cues)
                or cues[0] != 0 or not 0 < cues[1] < cues[2] < duration):
            raise ValueError("Set WHOLE_AUDIO_CUES to three increasing paragraph "
                             "starts within the WAV, beginning with 0 seconds.")
        lengths = [cues[1], cues[2]-cues[1], duration-cues[2]+4.0]
        return "whole", whole, clips, lengths
    if all(p.is_file() for p in clips):
        lengths = [max(speech, wav_seconds(p)) + hold
                   for (speech, hold), p in zip(PLANNED_BEATS, clips)]
        return "beats", whole, clips, lengths
    if any(p.is_file() for p in clips):
        print("Incomplete narration set: provide all three beat clips; preview is silent.")
    return "silent", whole, clips, lengths


class GaussScene09(Scene):
    def ar(self, string, size=25, color=WHITEISH):
        # Arabic: Pango renders connected letters (Text did not on this setup).
        mob = MarkupText(escape(string), font=ARABIC_FONT,
                         font_size=size, color=color)
        if not len(mob.get_all_points()):
            raise ValueError(f"Arabic label rendered empty: {string!r}")
        return mob

    def bounded(self, mob, width, x, y):
        if mob.width > width:
            mob.scale_to_fit_width(width)
        mob.move_to([x, y, 0])
        if (mob.get_left()[0] < -6.55 or mob.get_right()[0] > 6.55
                or mob.get_bottom()[1] < -3.60 or mob.get_top()[1] > 3.70):
            raise ValueError("Off-screen label: " + str(mob))
        return mob

    def play_t(self, animation, seconds):
        self.play(animation, run_time=seconds)
        self.t += seconds

    def wait_t(self, seconds):
        if seconds > 0.00001:
            self.wait(seconds)
            self.t += seconds

    def begin(self, index):
        if self.mode == "beats":
            self.add_sound(str(self.clips[index]))
        self.deadline = self.t + self.lengths[index]

    def finish(self, final=False):
        left = self.deadline - self.t
        if left < -0.05:
            raise RuntimeError(f"S09 beat exceeds its budget by {-left:.2f} seconds")
        if final and left >= 0.5:
            self.wait_t(left - 0.5)
            self.play_t(FadeOut(Group(*list(self.mobjects))), 0.5)
        else:
            self.wait_t(max(0, left))

    def construct(self):
        self.camera.background_color = DARK
        self.t = 0.0
        folder = Path(__file__).resolve().parent
        self.mode, whole, self.clips, self.lengths = audio_plan(folder)
        if self.mode == "whole":
            print("Whole-audio paragraph cues (scene seconds):",
                  tuple(1.0 + c for c in WHOLE_AUDIO_CUES))
        elif self.mode == "silent":
            print("No complete audio set: silent preview")
        # Check that a supplied cue leaves enough time for each visual explanation.
        # Scheduled animation sums; the last includes the final half-second fade.
        for i, (budget, required) in enumerate(zip(self.lengths, (14.50, 9.20, 10.65)), 1):
            if budget < required:
                raise ValueError(f"Beat {i} needs at least {required:.2f}s for its "
                                 "animations. Adjust the measured audio/edit or scene pacing.")
        self.total = 1 + sum(self.lengths)
        print(f"S09 target duration: {self.total:.2f} s")

        self.build_objects()
        self.play_t(FadeIn(self.title), 0.8)
        self.wait_t(0.2)
        if self.mode == "whole":
            self.add_sound(str(whole))
        self.beat1()
        self.beat2()
        self.beat3()
        assert abs(self.t - self.total) < 0.06, (self.t, self.total)

    def build_objects(self):
        self.title = self.bounded(self.ar("خط شحنة لا نهائي: إثبات التناظر الأسطواني", 39),
                                  12.2, 0, 3.25)
        # Left: side-on view of the mathematical infinite line charge.
        self.line_x = -4.70
        self.line = Line([self.line_x, -2.12, 0], [self.line_x, 1.90, 0],
                         color=RED, stroke_width=5)
        self.pluses = VGroup(*[MathTex("+", color=WHITEISH, font_size=29)
                               .move_to([self.line_x, y, 0])
                               for y in (-.22 + np.arange(-3, 4)*.54)])
        self.continuation = VGroup(
            MathTex(r"\cdots", font_size=30, color=RED).rotate(PI/2)
            .move_to([self.line_x, 2.18, 0]),
            MathTex(r"\cdots", font_size=30, color=RED).rotate(PI/2)
            .move_to([self.line_x, -2.36, 0]),
        )
        self.line_label = self.bounded(self.ar("خط شحنة موجب ومنتظم لا نهائي", 23),
                                       4.5, -3.70, -2.88)
        self.axis_label = MathTex("z", color=WHITEISH, font_size=32).move_to([-4.25, 2.20, 0])
        self.rho_formula = MathTex(r"\rho_l=\frac{\text{charge}}{\text{length}}",
                                   font_size=37, color=WHITEISH).move_to([-2.45, 1.72, 0])
        self.rho_name = self.bounded(self.ar("كثافة الشحنة الخطية", 22), 3.2,
                                     -2.20, 2.40)
        # Observation P and its perpendicular distance. Distinct from 'vertical'.
        self.p_x = -2.20
        self.obs = Dot([self.p_x, -.22, 0], radius=.09, color=GOLD)
        self.obs_name = MathTex("P", font_size=33, color=WHITEISH).next_to(self.obs, RIGHT, .16)
        self.radius = Line([self.line_x, -.22, 0], [self.p_x, -.22, 0],
                           color=VIOLET, stroke_width=3)
        self.right_angle = VGroup(
            Line([self.line_x, -.02, 0], [self.line_x+.2, -.02, 0], color=WHITEISH),
            Line([self.line_x+.2, -.02, 0], [self.line_x+.2, -.22, 0], color=WHITEISH),
        )
        self.r_label = MathTex("r", color=VIOLET, font_size=34).move_to([-3.40, -.58, 0])
        self.distance_ar = self.bounded(self.ar("البعد العمودي", 22), 2.8,
                                        -3.40, -1.06)
        # Translation: a second equal-radius observation point, upper z.
        self.obs_high = Dot([self.p_x, .80, 0], radius=.09, color=GOLD)
        self.radius_high = DashedLine([self.line_x, .80, 0], [self.p_x, .80, 0],
                                      color=VIOLET, dash_length=.12)
        self.translation = Arrow([self.p_x+.26, -.10, 0], [self.p_x+.26, .69, 0],
                                 color=WHITEISH, buff=0, stroke_width=3)
        # Axial hypothetical components at the observation point (one at a time).
        self.ez_up = Arrow(self.obs.get_center(), self.obs.get_center()+UP*.55,
                           color=BLUE, buff=0, stroke_width=5)
        self.ez_down = Arrow(self.obs.get_center(), self.obs.get_center()+DOWN*.55,
                             color=BLUE, buff=0, stroke_width=5)
        self.axial_label = self.bounded(self.ar("مركبة محورية مفترضة", 23), 3.8,
                                        -3.10, -1.48)
        self.ez_zero = MathTex(r"E_z=0", font_size=31, color=GOLD).move_to([-3.10, -2.12, 0])

        # Right: projection perpendicular to the z axis (top view).
        self.tc = np.array([3.45, .20, 0.])
        self.top_circle = Circle(radius=1.33, color=CYAN, stroke_width=2.5).move_to(self.tc)
        self.top_charge = Dot(self.tc, radius=.13, color=RED)
        self.top_plus = MathTex("+", color=WHITEISH, font_size=23).move_to(self.tc)
        self.top_title = self.bounded(self.ar("منظر علوي(إذا نظرنا إلى الخط من الأعلى)", 25), 2.8, 3.45, 1.97)
        self.top_point = Dot(self.tc+RIGHT*1.33, radius=.075, color=WHITEISH)
        self.rad_line = Line(self.tc, self.top_point.get_center(), color=VIOLET,
                             stroke_width=2.5)
        self.top_r = MathTex("r", font_size=31, color=VIOLET).next_to(self.rad_line, UP, .1)
        self.rotating_point = Dot(self.tc + RIGHT*1.33, radius=.08, color=GOLD)
        self.top_reflection_axis = DashedLine(self.tc+LEFT*1.7,
                                             self.tc+RIGHT*1.7,
                                             color=WHITEISH, dash_length=.11, stroke_opacity=.5)
        self.az_up = Arrow(self.top_point.get_center(),
                           self.top_point.get_center()+UP*.70,
                           buff=0, stroke_width=4, color=BLUE)
        self.az_down = Arrow(self.top_point.get_center(),
                             self.top_point.get_center()+DOWN*.70,
                             buff=0, stroke_width=4, color=BLUE)
        self.az_label = self.bounded(self.ar("مركبة سمتية مفترضة", 22), 2.75, 3.45, -1.48)
        self.az_zero = MathTex(r"E_{\varphi}=0", color=GOLD, font_size=29)
        self.az_zero.move_to([3.45, -1.97, 0])
        self.radial_arrow = Arrow(self.top_point.get_center(),
                                  self.top_point.get_center()+RIGHT*.67,
                                  buff=0, stroke_width=5, color=GOLD)
        self.result = MathTex(r"\mathbf E=E_r(r)\hat{\mathbf u}_r",
                              color=WHITEISH, font_size=34).move_to([3.35, -2.66, 0])
        self.radial_label = self.bounded(self.ar("المركبة الشعاعية", 22),
                                         2.85, 3.43, -1.47)
        self.axial_plane = DashedLine(
            [-5.55, -.22, 0], [-1.15, -.22, 0],
            color=WHITEISH, stroke_opacity=.6, dash_length=.13)
        self.axial_plane_name = self.bounded(
            self.ar('مستوى انعكاس عمودي على الخط\nويمر بالنقطة', 21),
            3.7, -2.65, .72)
        self.axial_plane_eq = self.ar('خارج الخط', 20)
        self.axial_plane_eq.move_to([-5.60, -.57, 0])
        self.top_plane_name = self.bounded(
            self.ar('مقطع مستوى يحتوي الخط والنقطة', 21), 5.5, 3.45, 2.48)
        self.hypothesis_note = self.bounded(
            self.ar('الأسهم الزرقاء مركبات مفترضة وليست مجالا يتغير مع الزمن', 21, BLUE),
            11.8, 0, -3.40)
        self.scope_note = self.bounded(
            self.ar('لا يوجد مجال خارجي', 21), 3.5, -3.7, -3.35)
        self.equal_radius_note = self.bounded(
            self.ar('نقاط على البعد نفسه من الخط', 21), 5.2, 3.45, -1.48)
        self.rotation_radius = self.rad_line.copy().set_opacity(.5)
        self.rotation_group = VGroup(self.rotating_point, self.rotation_radius)
        self.check_layout()

    def check_layout(self):
        labels = [self.title, self.line_label, self.rho_name, self.rho_formula,
                  self.obs_name, self.r_label, self.distance_ar, self.top_title,
                  self.axial_label, self.axial_plane_name,
                  self.top_plane_name, self.az_label, self.radial_label,
                  self.hypothesis_note, self.scope_note, self.equal_radius_note,
                  self.ez_zero, self.az_zero, self.result]
        for item in labels:
            if (item.get_left()[0] < -6.6 or item.get_right()[0] > 6.6
                    or item.get_bottom()[1] < -3.65 or item.get_top()[1] > 3.70):
                raise ValueError(f"Object outside safe frame: {item}")
        # Check simultaneously visible results, not just screen boundaries.
        for upper, lower in [(self.rho_name, self.rho_formula),
                             (self.rho_formula, self.axial_plane_name),
                             (self.axial_label, self.ez_zero),
                             (self.radial_label, self.az_zero),
                             (self.az_zero, self.result),
                             (self.result, self.hypothesis_note)]:
            if upper.get_bottom()[1] < lower.get_top()[1] + .09:
                raise ValueError("Vertical labels/equations overlap")

    def beat1(self):
        self.begin(0)
        self.play_t(Create(self.line), 1.0)
        self.play_t(FadeIn(self.pluses, self.continuation), 1.1)
        self.play_t(FadeIn(self.axis_label, self.line_label, self.scope_note), .8)
        self.play_t(FadeIn(self.rho_name), .5)
        self.play_t(Write(self.rho_formula), 1.3)
        self.play_t(FadeIn(self.obs, self.obs_name), .6)
        self.play_t(Create(self.radius), .8)
        self.play_t(FadeIn(self.right_angle, self.r_label, self.distance_ar), .8)
        self.play_t(FadeIn(self.radius_high, self.obs_high), .5)
        self.play_t(GrowArrow(self.translation), .5)
        self.play_t(Indicate(self.radius, color=VIOLET, scale_factor=1.04), .7)
        self.play_t(Indicate(self.radius_high, color=VIOLET, scale_factor=1.04), .7)
        self.play_t(FadeOut(self.obs_high, self.radius_high, self.translation), .5)
        self.play_t(Create(self.top_circle), .7)
        self.play_t(FadeIn(self.top_charge, self.top_plus, self.top_title), .6)
        self.play_t(Create(self.rad_line), .45)
        self.play_t(FadeIn(self.top_r, self.rotation_group, self.equal_radius_note), .35)
        # One full revolution of a point at constant r: source remains unchanged.
        self.play_t(Rotating(self.rotation_group, angle=TAU, about_point=self.tc), 2.0)
        self.play_t(FadeOut(self.rotation_group), .35)
        self.play_t(FadeIn(self.top_point), .25)
        self.finish()

    def beat2(self):
        self.begin(1)
        # The hypothetical axial component must change sign under reflection,
        # while the infinite charge line and the observation point stay fixed.
        self.play_t(FadeOut(self.radius, self.right_angle, self.r_label,
                            self.distance_ar, self.scope_note), .5)
        self.play_t(Create(self.axial_plane), .7)
        self.play_t(FadeIn(self.axial_plane_name,
                           self.hypothesis_note), .8)
        self.play_t(FadeIn(self.axial_label), .7)
        self.play_t(GrowArrow(self.ez_up), .9)
        self.play_t(Indicate(self.line, color=RED, scale_factor=1.01), 1.0)
        self.play_t(ReplacementTransform(self.ez_up, self.ez_down), 1.4)
        self.play_t(Indicate(self.obs, color=GOLD, scale_factor=1.25), .8)
        self.play_t(FadeOut(self.ez_down), .6)
        self.play_t(Write(self.ez_zero), 1.0)
        self.play_t(Indicate(self.ez_zero, color=GOLD), .8)
        self.finish()

    def beat3(self):
        self.begin(2)
        self.play_t(FadeOut(self.equal_radius_note), .35)
        self.play_t(Create(self.top_reflection_axis), .7)
        self.play_t(FadeIn(self.top_plane_name), .7)
        self.play_t(FadeIn(self.az_label), .5)
        self.play_t(GrowArrow(self.az_up), .75)
        self.play_t(ReplacementTransform(self.az_up, self.az_down), 1.4)
        self.play_t(FadeOut(self.az_down), .45)
        self.play_t(Write(self.az_zero), .8)
        self.play_t(GrowArrow(self.radial_arrow), .8)
        self.play_t(FadeOut(self.az_label), .7)
        self.play_t(FadeIn(self.radial_label), .5)
        self.play_t(Write(self.result), 1.4)
        self.play_t(Indicate(self.result, color=GOLD, scale_factor=1.05), 1.1)
        self.finish(final=True)


# ==============================================================
# PYCHARM: RUN THIS FILE; OPEN FINISHED VIDEO AUTOMATICALLY
# ==============================================================
if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "manim", "-p", "-qh",
        "-r", "1920,1080", "--fps", "30",
        str(Path(__file__).resolve()), "GaussScene09"
    ], check=True)




