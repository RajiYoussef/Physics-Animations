"""S07 — Changing the surface: same flux, different convenience.

Click Run in PyCharm. An optional single S07_ar.wav or three beat files
S07_B01_ar.wav, S07_B02_ar.wav, S07_B03_ar.wav may sit beside this script.
For a single continuous recording, the planned paragraph start cues are
1, 20, 42 seconds; adjust them after measuring your recording as needed.
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

DARK = "#101820"
WHITEISH = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
VIOLET = "#C792EA"
RED = "#FF6B6B"
ARABIC_FONT = "Arial"  # Use the same Arabic-compatible font that worked in S05.
PARAGRAPH_STARTS = (1.0, 20.0, 42.0)


def wav_seconds(file: Path) -> float:
    if not file.is_file():
        return 0.0
    try:
        with contextlib.closing(wave.open(str(file), "rb")) as wav:
            return wav.getnframes() / wav.getframerate()
    except (wave.Error, OSError, ZeroDivisionError):
        return 0.0


class GaussScene07(Scene):
    def ar(self, phrase, size=25, color=WHITEISH):
        # Required on the user's setup: Text() gave missing Arabic glyphs.
        return MarkupText(escape(phrase), font=ARABIC_FONT,
                          font_size=size, color=color)

    def step(self, *animations, seconds):
        self.play(*animations, run_time=seconds)
        self.elapsed += seconds

    def pause(self, seconds):
        if seconds > 1e-6:
            self.wait(seconds)
            self.elapsed += seconds

    def begin_beat(self, number):
        self.end_beat_at = self.elapsed + self.lengths[number]
        if self.audio_mode == "beats":
            self.add_sound(str(self.audio_files[number]))

    def finish_beat(self, last=False):
        left = self.end_beat_at - self.elapsed
        if left < -0.05:
            raise RuntimeError(f"S07 animations overran beat by {-left:.2f} seconds")
        if not last:
            self.pause(max(0, left))
        else:
            self.pause(max(0, left - 0.5))
            fade = min(0.5, max(0, self.end_beat_at - self.elapsed))
            if fade:
                self.step(*[FadeOut(m) for m in list(self.mobjects)], seconds=fade)

    def construct(self):
        self.camera.background_color = DARK
        self.elapsed = 0.0
        folder = Path(__file__).resolve().parent
        whole = folder / "S07_ar.wav"
        clips = [folder / f"S07_B0{i}_ar.wav" for i in (1, 2, 3)]
        self.audio_mode = "silent"
        self.audio_files = []
        speech_holds = ((16., 3.), (19., 3.), (12., 4.))
        self.lengths = [sum(pair) for pair in speech_holds]
        if whole.is_file():
            self.audio_mode = "whole"
            self.audio_files = [whole]
            # A complete clip begins at 1 s; preserve the last 4 s as a hold.
            self.lengths[-1] += max(0., wav_seconds(whole) - (sum(self.lengths) - 4.))
            print("S07 single-audio paragraph starts (seconds):", PARAGRAPH_STARTS)
        elif all(f.is_file() for f in clips):
            self.audio_mode = "beats"
            self.audio_files = clips
            self.lengths = [max(s, wav_seconds(file)) + h
                            for file, (s, h) in zip(clips, speech_holds)]
        else:
            print("S07: silent preview (no complete audio set found).")
        self.build_objects()

        # Initial one-second scene setup, without any narration.
        self.step(FadeIn(self.title, shift=DOWN * 0.10), seconds=0.8)
        self.pause(0.2)
        if self.audio_mode == "whole":
            self.add_sound(str(whole))

        self.beat_1()
        self.beat_2()
        self.beat_3()
        expected = 1 + sum(self.lengths)
        assert abs(self.elapsed - expected) <= 0.05, (self.elapsed, expected)
        print(f"S07 duration: {self.elapsed:.2f} seconds")

    def build_objects(self):
        self.title = self.ar("تغيير السطح: التدفق نفسه، وسهولة مختلفة للحساب", 36)
        self.title.scale_to_fit_width(min(self.title.width, 11.9))
        self.title.move_to([0, 3.25, 0])
        self.divider = Line([0, 2.0, 0], [0, -2.85, 0],
                            color=WHITEISH, stroke_width=1.2, stroke_opacity=0.28)
        self.flux_badge = VGroup(
            RoundedRectangle(width=3.5, height=0.65, corner_radius=0.13,
                             stroke_color=CYAN, stroke_width=2, fill_opacity=0),
            MathTex(r"\Phi_E=\frac{Q}{\epsilon_0}", font_size=37, color=WHITEISH)
        )
        self.flux_badge[1].move_to(self.flux_badge[0])
        self.flux_badge.move_to([0, 2.47, 0])

        # Left: one positive charge with a spherical 3D schematic.
        self.left_origin = np.array([-3.30, 0.10, 0.0])
        self.radius = ValueTracker(0.79)
        self.charge = Circle(radius=0.18, color=RED, fill_color=RED,
                             fill_opacity=1, stroke_width=1.5).move_to(self.left_origin)
        self.plus = MathTex("+Q", color=WHITEISH, font_size=32)
        self.plus.next_to(self.charge, DOWN, buff=0.12)
        self.sphere = always_redraw(lambda: Circle(
            radius=self.radius.get_value(), color=CYAN,
            stroke_width=2.8).move_to(self.left_origin))
        self.equator = always_redraw(lambda: Ellipse(
            width=2 * self.radius.get_value(),
            height=0.52 * self.radius.get_value(),
            color=CYAN, stroke_width=1.5, stroke_opacity=0.48
        ).move_to(self.left_origin))

        def field_arrows():
            group = VGroup()
            rr = self.radius.get_value()
            for theta in np.linspace(0, TAU, 8, endpoint=False):
                direction = np.array([np.cos(theta), np.sin(theta), 0.])
                start = self.left_origin + rr * direction
                # Ratio of lengths is 1/4 at double radius, as required.
                arrow_len = 0.54 * (0.79 / rr) ** 2
                group.add(Arrow(start, start + direction * arrow_len,
                                buff=0, color=GOLD, stroke_width=4,
                                max_tip_length_to_length_ratio=0.25))
            return group
        self.field_arrows = always_redraw(field_arrows)
        self.radius_segment = always_redraw(lambda: Line(
            self.left_origin, self.left_origin + RIGHT * self.radius.get_value(),
            color=VIOLET, stroke_width=2.5))
        self.r_label = always_redraw(lambda: MathTex(
            "r", color=VIOLET, font_size=30
        ).move_to(self.left_origin + RIGHT * self.radius.get_value() * .50 + UP * .23))
        self.sphere_label = self.ar("كرة", 24).move_to([-3.3, -2.88, 0])
        self.eq_field = MathTex(r"E_r(2r)=\frac14 E_r(r)",
                                font_size=34, color=WHITEISH).move_to([-3.3, -2.20, 0])
        self.eq_area = MathTex(r"A(2r)=4A(r)",
                               font_size=34, color=WHITEISH).move_to([-3.3, -2.67, 0])

        # Right: a 2D SECTION THROUGH a 3D cube, never a replacement for its surface.
        self.right_origin = np.array([3.32, -0.28, 0.])
        side = 2.45
        self.cube_section = Square(side_length=side, color=CYAN,
                                   stroke_width=2.7).move_to(self.right_origin)
        self.section_label = self.ar("مقطع في مكعب", 25).move_to([3.3, -2.72, 0])
        self.cube_label = self.ar("مكعب", 24).move_to([3.32, 1.35, 0])
        self.cube_charge = Circle(radius=0.14, fill_color=RED,
                                  fill_opacity=1, stroke_color=RED).move_to(self.right_origin)
        self.cube_plus = MathTex("+Q", color=WHITEISH, font_size=28).next_to(
            self.cube_charge, DOWN, buff=0.10)
        face_x = self.right_origin[0] + side / 2
        # Two points on the right cube face: one at centre, one off-centre.
        self.face_points = [np.array([face_x, self.right_origin[1], 0]),
                            np.array([face_x, self.right_origin[1] + .68, 0])]
        self.cube_normals = VGroup()
        self.cube_fields = VGroup()
        for pt in self.face_points:
            normal = Arrow(pt, pt + RIGHT * .56, buff=0,
                           stroke_width=4, color=VIOLET)
            radial = pt - self.right_origin
            unit = radial / np.linalg.norm(radial)
            # Magnitude shrinks for the farther, off-centre point.
            # Every vector's direction is radial from +Q.
            size = .77 * (side / 2 / np.linalg.norm(radial)) ** 2
            start = pt - unit * .12
            field = Arrow(start, start + unit * size, buff=0,
                          stroke_width=4, color=GOLD,
                          max_tip_length_to_length_ratio=.19)
            self.cube_normals.add(normal)
            self.cube_fields.add(field)
        self.n_label = MathTex(r"\hat{\mathbf n}", color=VIOLET,
                               font_size=26).next_to(self.cube_normals[0], DOWN, buff=.08)
        self.e_label = MathTex(r"\mathbf E", color=GOLD,
                               font_size=27).next_to(self.cube_fields[1], UP, buff=.06)
        self.left_final = self.ar("القانون: أي سطح مغلق", 23)
        self.right_final = self.ar("لتسهيل حساب المجال: استخدم التناظر", 23)
        for label in [self.left_final, self.right_final]:
            label.scale_to_fit_width(min(label.width, 5.65))
        self.left_final.move_to([0, 1.72, 0])
        self.right_final.move_to([0, -2.52, 0])
        self.same_flux = self.ar("التدفق نفسه", 23, CYAN)
        self.same_flux.move_to([3.32, -2.14, 0])

    def beat_1(self):
        self.begin_beat(0)
        self.step(Create(self.divider), seconds=.6)
        self.step(FadeIn(self.flux_badge), seconds=.8)
        self.step(FadeIn(self.charge, self.plus), seconds=.8)
        self.add(self.sphere, self.equator, self.field_arrows,
                 self.radius_segment, self.r_label)
        self.step(FadeIn(self.sphere_label), seconds=.6)
        self.pause(.8)
        # The arrow lengths track E~1/r^2, but Q and the flux badge do not change.
        self.step(self.radius.animate.set_value(1.58), seconds=3.3)
        self.step(Write(self.eq_field), seconds=1.3)
        self.step(Write(self.eq_area), seconds=1.3)
        self.step(Indicate(self.flux_badge[1], color=CYAN), seconds=.9)
        self.finish_beat()

    def beat_2(self):
        self.begin_beat(1)
        self.step(Create(self.cube_section), seconds=1.3)
        self.step(FadeIn(self.cube_charge, self.cube_plus, self.cube_label,
                         self.section_label), seconds=1.1)
        self.step(GrowArrow(self.cube_normals[0]), seconds=.8)
        self.step(GrowArrow(self.cube_fields[0]), seconds=.8)
        self.step(FadeIn(self.n_label), seconds=.5)
        self.step(GrowArrow(self.cube_normals[1]), seconds=.8)
        self.step(GrowArrow(self.cube_fields[1]), seconds=.8)
        self.step(FadeIn(self.e_label), seconds=.5)
        self.step(Indicate(self.cube_fields[0], color=GOLD), seconds=1.0)
        self.step(Indicate(self.cube_fields[1], color=GOLD), seconds=1.0)
        self.step(Indicate(self.flux_badge[1], color=CYAN), seconds=1.0)
        self.step(FadeIn(self.same_flux), seconds=.7)
        self.finish_beat()

    def beat_3(self):
        self.begin_beat(2)
        # Top statement and bottom statement are the exact two conceptual cues.
        self.step(FadeIn(self.left_final), seconds=.9)
        self.step(Indicate(self.flux_badge[1], color=CYAN), seconds=1.0)
        self.step(Indicate(self.cube_section, color=CYAN), seconds=1.0)
        self.step(FadeOut(self.same_flux, self.eq_field, self.eq_area, self.section_label), seconds=.5)
        self.step(FadeIn(self.right_final), seconds=.9)
        self.step(Indicate(self.sphere, color=CYAN), seconds=1.0)
        self.finish_beat(last=True)


# ==========================================================
# RENDER — CLICK RUN IN PYCHARM; OPEN VIDEO AUTOMATICALLY
# ==========================================================
if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "manim", "-p", "-qh",
        "-r", "1920,1080", "--fps", "30",
        str(Path(__file__).resolve()), "GaussScene07"
    ], check=True)
