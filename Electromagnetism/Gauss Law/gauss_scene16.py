"""GaussScene16 — Coulomb's law to Gauss's law (point-charge source).

Optional narration beside this script:
    S16_ar.wav (single full-scene WAV starting at scene time 00:01), or
    S16_B01_ar.wav, S16_B02_ar.wav, S16_B03_ar.wav.
Without them the 68-second scene renders silently.
"""
from __future__ import annotations

import contextlib
from html import escape
from pathlib import Path
import subprocess
import sys
import wave

import numpy as np
from manim import *

BG = "#101820"
WHITEISH = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
VIOLET = "#C792EA"
POS = "#FF6B6B"
BLUE = "#64B5F6"


def wav_duration(path: Path) -> float:
    try:
        with contextlib.closing(wave.open(str(path), "rb")) as audio:
            return audio.getnframes() / audio.getframerate()
    except (OSError, wave.Error, ZeroDivisionError):
        return 0.0


class GaussScene16(Scene):
    def ar(self, words, size=26, color=WHITEISH):
        # Text(...) can fail to shape Arabic on some Windows/Pango installations.
        return MarkupText(escape(words), font="Arial", font_size=size, color=color)

    def timed(self, animation, seconds):
        self.play(animation, run_time=seconds)
        self.clock += seconds

    def hold(self, seconds):
        if seconds > 1e-5:
            self.wait(seconds)
            self.clock += seconds

    def begin_beat(self, index):
        self.stop_at = self.clock + self.beat_lengths[index]
        if self.audio_mode == "clips":
            self.add_sound(str(self.clips[index]))

    def end_beat(self, last=False):
        remaining = self.stop_at - self.clock
        if remaining < -0.04:
            raise RuntimeError(f"Scene 16 beat overran by {-remaining:.2f}s")
        if last and remaining >= 0.5:
            self.hold(remaining - 0.5)
            self.timed(FadeOut(Group(*list(self.mobjects))), 0.5)
        else:
            self.hold(max(0, remaining))

    def make_diagram(self):
        self.center = np.array([-3.73, -0.22, 0.])
        # An irregular CLOSED surface shown in section. The point-charge singularity
        # is marked independently and never treated as a smooth-field point.
        verts = []
        for theta in np.linspace(0, TAU, 101):
            radius = 1.91 + .17 * np.sin(3 * theta + .3) + .09 * np.cos(5 * theta)
            verts.append(self.center + radius * np.array([np.cos(theta), np.sin(theta), 0.]))
        self.outer = VMobject(color=CYAN, stroke_width=3.2)
        self.outer.set_points_smoothly(verts)
        self.outer.close_path()
        self.outer.set_fill(CYAN, opacity=0.045)

        self.source_exclusion = Circle(radius=.16, color=POS, stroke_width=2.3,
                                       fill_color=BG, fill_opacity=1).move_to(self.center)
        self.charge = MathTex("+q", color=POS, font_size=30).move_to(self.center + DOWN * .32)
        self.source_label = self.ar("موضع الشحنة المستبعد", 23, POS).move_to([-3.8, -2.60, 0])
        self.outer_label = MathTex("S", color=CYAN, font_size=31).move_to([-5.92, 1.10, 0])

        # A few Coulomb-field arrows; radial direction/strength is schematic.
        self.field_arrows = VGroup()
        for ang in np.linspace(0, TAU, 9, endpoint=False):
            d = np.array([np.cos(ang), np.sin(ang), 0.])
            a = self.center + .58 * d
            b = self.center + 1.43 * d
            self.field_arrows.add(Arrow(a, b, buff=0, color=GOLD, stroke_width=3.4,
                                        max_tip_length_to_length_ratio=.17))

        self.b_radius = .73
        self.small_sphere = Circle(radius=self.b_radius, color=CYAN, stroke_width=3.5,
                                   fill_color=CYAN, fill_opacity=.10).move_to(self.center)
        self.b_line = Line(self.center + UP * .06,
                           self.center + RIGHT * self.b_radius, color=WHITEISH,
                           stroke_width=2.5)
        self.b_symbol = MathTex("b", color=WHITEISH, font_size=33).move_to(
            self.center + np.array([.47, .28, 0]))
        self.sphere_label = self.ar("كرة مساعدة صغيرة", 24).move_to([-3.8, -2.22, 0])

        self.diagram_note1 = self.ar("مجال كولوم", 25, GOLD).move_to([-3.85, 2.30, 0])
        self.diagram_note2 = self.ar("التباعد صفري بعيدًا عن الشحنة", 23).move_to([-3.8, 2.30, 0])

    def make_equations(self):
        # Each row stays inside x = [0.4, 6.65] and y = [-2.75, 2.65].
        self.assumption = self.ar("فرضية البداية", 25).move_to([3.30, 2.35, 0])
        self.eq_coulomb = MathTex(
            r"\mathbf E=\frac{q}{4\pi\epsilon_0 r^2}\hat{\mathbf r}\quad(r>0)",
            color=WHITEISH, font_size=35)
        self.eq_coulomb.scale_to_fit_width(min(self.eq_coulomb.width, 5.8))
        self.eq_coulomb.move_to([3.38, 1.45, 0])

        self.eq_div = MathTex(
            r"\nabla\cdot\mathbf E=\frac{1}{r^2}\frac{d}{dr}(r^2E_r)=0\quad(r>0)",
            color=WHITEISH, font_size=32)
        if self.eq_div.width > 5.85:
            self.eq_div.scale_to_fit_width(5.85)
        self.eq_div.move_to([3.37, .10, 0])

        self.eq_const = MathTex(
            r"r^2 E_r=\frac{q}{4\pi\epsilon_0}",
            color=WHITEISH, font_size=38)
        self.eq_const.move_to([3.32, -1.10, 0])
        self.constant_label = self.ar("ثابت", 24, GOLD).move_to([3.25, -1.77, 0])

        self.eq_flux = MathTex(
            r"\Phi_b=\frac{q}{4\pi\epsilon_0 b^2}\,4\pi b^2=\frac{q}{\epsilon_0}",
            color=WHITEISH, font_size=35)
        if self.eq_flux.width > 5.85:
            self.eq_flux.scale_to_fit_width(5.85)
        self.eq_flux.move_to([3.37, -1.05, 0])
        self.cancel_hint = self.ar("اختصار نصف القطر", 23, GOLD).move_to([3.32, -1.94, 0])

    def beat1(self):
        self.begin_beat(0)
        self.timed(FadeIn(self.assumption), .65)
        self.timed(Write(self.eq_coulomb), 1.5)
        self.timed(FadeIn(self.diagram_note1), .55)
        self.timed(Create(self.outer), 1.1)
        self.timed(FadeIn(self.outer_label), .35)
        self.timed(FadeIn(self.field_arrows), .8)
        self.timed(FadeIn(self.source_exclusion), .5)
        self.timed(FadeIn(self.charge), .4)
        self.timed(FadeIn(self.source_label), .5)
        self.timed(Indicate(self.eq_coulomb, color=GOLD, scale_factor=1.03), 1.0)
        self.end_beat()

    def beat2(self):
        self.begin_beat(1)
        self.timed(Write(self.eq_div), 1.55)
        self.timed(Indicate(self.eq_div, color=GOLD, scale_factor=1.02), 1.05)
        self.timed(Write(self.eq_const), 1.25)
        self.timed(FadeIn(self.constant_label), .5)
        self.timed(Circumscribe(self.eq_const, color=GOLD), 1.1)
        self.timed(Indicate(self.eq_div, color=GOLD, scale_factor=1.02), 1.0)
        self.timed(FadeOut(self.diagram_note1), .45)
        self.timed(FadeIn(self.diagram_note2), .55)
        self.timed(Indicate(self.source_exclusion, color=POS, scale_factor=1.3), 1.0)
        self.end_beat()

    def beat3(self):
        self.begin_beat(2)
        # Clear the lower equation slot before inserting the flux formula.
        self.timed(FadeOut(VGroup(self.eq_const, self.constant_label)), .6)
        self.timed(Create(self.small_sphere), .9)
        self.timed(Create(self.b_line), .5)
        self.timed(FadeIn(self.b_symbol), .4)
        self.timed(FadeIn(self.sphere_label), .5)
        self.timed(Write(self.eq_flux), 1.6)
        self.timed(FadeIn(self.cancel_hint), .55)
        self.timed(Indicate(self.eq_flux, color=GOLD, scale_factor=1.03), 1.15)
        self.timed(Circumscribe(self.eq_flux, color=GOLD), 1.15)
        self.end_beat(last=True)

    def construct(self):
        self.camera.background_color = BG
        self.clock = 0.0
        directory = Path(__file__).resolve().parent
        self.clips = [directory / f"S16_B0{i}_ar.wav" for i in (1, 2, 3)]
        whole = directory / "S16_ar.wav"
        speech = [15.0, 20.0, 22.0]
        holds = [3.0, 3.0, 4.0]
        self.beat_lengths = [18.0, 23.0, 26.0]
        self.audio_mode = "silent"
        if whole.is_file():
            self.audio_mode = "whole"
            duration = wav_duration(whole)
            # The continuous track begins at 00:01 and lasts 67 seconds in the plan.
            self.beat_lengths[2] += max(0.0, duration - 67.0)
            print(f"S16 full narration: {duration:.2f}s; scene duration {1+sum(self.beat_lengths):.2f}s")
        elif all(p.is_file() for p in self.clips):
            self.audio_mode = "clips"
            self.beat_lengths = [max(s, wav_duration(p)) + h
                                 for s, h, p in zip(speech, holds, self.clips)]
            print("S16 beat lengths:", self.beat_lengths, "total:", 1+sum(self.beat_lengths))
        else:
            print("S16 silent preview: 68.00s")

        self.title = self.ar("لماذا يصح القانون؟ شحنة نقطية واحدة", 36)
        self.title.move_to([0, 3.27, 0])
        self.make_diagram()
        self.make_equations()
        self.timed(FadeIn(self.title, shift=DOWN*.12), .8)
        self.hold(.2)
        if self.audio_mode == "whole":
            self.add_sound(str(whole))
        self.beat1()
        self.beat2()
        self.beat3()
        expected = 1 + sum(self.beat_lengths)
        assert abs(self.clock - expected) < .04, (self.clock, expected)


if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "manim", "-p", "-qh", "-r", "1920,1080",
        "--fps", "30", str(Path(__file__).resolve()), "GaussScene16"
    ], check=True)
