"""S12 — Uniformly charged solid sphere: interior (Manim Community).

Optional sound, stored next to this script:
  S12_B01_ar.wav, S12_B02_ar.wav, S12_B03_ar.wav (all three), or S12_ar.wav.
Without audio, the exact preview duration is 60 seconds at 30 fps.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import subprocess
import sys
import wave

import numpy as np
from manim import *

BG = "#101820"
INK = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
VIOLET = "#C792EA"
POSITIVE = "#FF6B6B"


def wav_length(path: Path) -> float:
    """Return WAV duration or 0 if unavailable/invalid."""
    if not path.is_file():
        return 0.0
    try:
        with wave.open(str(path), "rb") as f:
            return f.getnframes() / f.getframerate()
    except (OSError, wave.Error, ZeroDivisionError):
        return 0.0


class GaussScene12(Scene):
    def arabic(self, content: str, size: int = 28, color=INK):
        # Shaping + RTL are handled by Pango; don't reverse strings.
        return MarkupText(escape(content), font="Arial", font_size=size, color=color)

    def play_t(self, animation, duration):
        self.play(animation, run_time=duration)
        self.clock += duration

    def hold(self, duration):
        if duration > 1e-7:
            self.wait(duration)
            self.clock += duration

    def begin_beat(self, index):
        if self.mode == "clips":
            self.add_sound(str(self.clips[index]))
        self.beat_finish = self.clock + self.beat_lengths[index]

    def end_beat(self, last=False):
        spare = self.beat_finish - self.clock
        if spare < -0.05:
            raise RuntimeError(f"S12 exceeded beat time by {-spare:.2f}s")
        if last and spare >= 0.5:
            self.hold(spare - 0.5)
            self.play_t(FadeOut(Group(*list(self.mobjects))), 0.5)
        else:
            self.hold(max(0.0, spare))

    def make_visuals(self):
        # All objects stay inside ±6.65 horizontally and above -2.75 vertically.
        self.title = self.arabic("الكرة المشحونة بانتظام: المجال داخلها", 38)
        self.title.move_to([0, 3.23, 0])

        # Dedicated left column. 2D disks explicitly represent SECTIONS,
        # not the volumes used when calculating enclosed charge.
        self.origin = np.array([-3.50, -0.15, 0.0])
        self.a_vis = 1.63
        self.r_vis = 0.92
        self.outer = Circle(radius=self.a_vis, color=CYAN, stroke_width=3,
                            fill_color=CYAN, fill_opacity=0.14).move_to(self.origin)
        self.inner_fill = Circle(radius=self.r_vis, color=GOLD, stroke_width=0,
                                 fill_color=GOLD, fill_opacity=0.18).move_to(self.origin)
        self.inner_border = DashedVMobject(
            Circle(radius=self.r_vis, color=CYAN, stroke_width=3).move_to(self.origin),
            num_dashes=30,
        )
        # Mark charges throughout the full sphere, including the material
        # between Gaussian and physical radii.
        locations = [(-1.18, .34), (-1.08, -.57), (-.66, 1.07), (.38, 1.10),
                     (1.10, .56), (1.12, -.48), (.48, -1.15), (-.48, -1.13),
                     (-.53, .32), (.31, .40), (-.28, -.43), (.41, -.31)]
        self.charges = VGroup(*[
            MathTex("+", font_size=22, color=POSITIVE).move_to(self.origin + [x, y, 0])
            for x, y in locations
        ])

        # Separate radius rays: a to left-up, r to right-up.
        a_direction = np.array([-0.84, 0.54, 0.0]); a_direction /= np.linalg.norm(a_direction)
        r_direction = np.array([0.92, 0.39, 0.0]); r_direction /= np.linalg.norm(r_direction)
        self.a_ray = Line(self.origin, self.origin + self.a_vis*a_direction,
                          color=INK, stroke_width=2.6)
        self.r_ray = Line(self.origin, self.origin + self.r_vis*r_direction,
                          color=VIOLET, stroke_width=3)
        self.a_math = MathTex("a", color=INK, font_size=34).move_to(
            self.origin + self.a_vis*a_direction*0.68 + [-0.10, .20, 0])
        self.r_math = MathTex("r", color=VIOLET, font_size=34).move_to(
            self.origin + self.r_vis*r_direction*0.73 + [0.12, .24, 0])
        self.q_math = MathTex("Q", color=POSITIVE, font_size=31).move_to([-5.20, 1.70, 0])
        self.r_less_a = MathTex("r<a", color=INK, font_size=30).move_to([-3.45, -2.23, 0])

        # One explanatory caption at a time, in a reserved left-only strip.
        self.left_caption = self.arabic("رسم مقطعي فقط", 27).move_to([-3.45, 2.20, 0])
        self.volume_caption = self.arabic("الحجم الداخلي المحصور", 25, GOLD).move_to([-3.45, 2.20, 0])
        self.remain_caption = self.arabic("بقية المادة المشحونة", 25).move_to([-3.45, 2.20, 0])
        self.ratio_caption = self.arabic("نسبة الحجمين", 27).move_to([-3.45, 2.20, 0])
        self.field_caption = self.arabic("المجال الداخلي", 27).move_to([-3.45, 2.20, 0])
        self.center_caption = self.arabic("عند المركز", 27).move_to([-3.45, 2.20, 0])

        # Right column: equations deliberately swapped between beats,
        # never all four densely stacked on screen.
        self.eq_q = MathTex(
            r"Q_{\mathrm{in}}=\rho_v\frac{4\pi r^3}{3}=Q\left(\frac{r}{a}\right)^3",
            font_size=36, color=INK,
        )
        self.eq_flux = MathTex(
            r"E_r(r)4\pi r^2=\frac{Qr^3}{\epsilon_0 a^3}",
            font_size=38, color=INK,
        )
        self.eq_field = MathTex(
            r"\mathbf E=\frac{Qr}{4\pi\epsilon_0 a^3}\hat{\mathbf r}\quad(0<r\le a)",
            font_size=37, color=INK,
        )
        self.eq_zero = MathTex(r"\mathbf E(0)=\mathbf 0", font_size=40, color=INK)
        # The narrowest safe right panel spans x in [0.25, 6.4].
        for eq in [self.eq_q, self.eq_flux, self.eq_field, self.eq_zero]:
            if eq.width > 5.90:
                eq.scale_to_fit_width(5.90)
        self.eq_q.move_to([3.30, .40, 0])
        self.eq_flux.move_to([3.30, 1.14, 0])
        self.eq_field.move_to([3.30, -.18, 0])
        self.eq_zero.move_to([3.30, -1.42, 0])

        # Small outward arrows on the INSIDE Gaussian sphere illustrate
        # direction without suggesting a surface charge or conducting material.
        self.inner_arrows = VGroup()
        for degrees in (15, 100, 195, 280):
            angle = degrees * DEGREES
            d = np.array([np.cos(angle), np.sin(angle), 0.])
            start = self.origin + self.r_vis * .66 * d
            self.inner_arrows.add(Arrow(start, start + .28*d, buff=0,
                                        color=GOLD, stroke_width=3,
                                        max_tip_length_to_length_ratio=.28))
        self.center_dot = Dot(self.origin, radius=.065, color=INK)

    def beat_1(self):
        self.begin_beat(0)  # 01–16: 15 seconds
        self.play_t(FadeIn(self.outer), 1.0)
        self.play_t(FadeIn(self.charges), .7)
        self.play_t(FadeIn(self.q_math), .35)
        self.play_t(Create(self.a_ray), .6)
        self.play_t(FadeIn(self.a_math), .3)
        self.play_t(FadeIn(self.left_caption), .5)
        self.play_t(FadeIn(self.inner_fill), .7)
        self.play_t(Create(self.inner_border), 1.0)
        self.play_t(Create(self.r_ray), .55)
        self.play_t(FadeIn(self.r_math), .3)
        self.play_t(FadeIn(self.r_less_a), .4)
        self.play_t(ReplacementTransform(self.left_caption, self.volume_caption), .7)
        self.play_t(Indicate(self.inner_fill, color=GOLD, scale_factor=1.035), .9)
        self.play_t(ReplacementTransform(self.volume_caption, self.remain_caption), .7)
        self.end_beat()

    def beat_2(self):
        self.begin_beat(1)  # 16–38: 22 seconds
        self.play_t(ReplacementTransform(self.remain_caption, self.volume_caption), .6)
        self.play_t(Write(self.eq_q), 1.7)
        self.play_t(Indicate(self.inner_border, color=GOLD, scale_factor=1.04), 1.0)
        self.play_t(Indicate(self.outer, color=CYAN, scale_factor=1.035), 1.0)
        self.play_t(ReplacementTransform(self.volume_caption, self.ratio_caption), .65)
        self.play_t(Indicate(self.eq_q, color=GOLD, scale_factor=1.025), 1.25)
        self.end_beat()

    def beat_3(self):
        self.begin_beat(2)  # 38–60: 22 seconds
        self.play_t(FadeOut(self.eq_q), .6)
        self.play_t(ReplacementTransform(self.ratio_caption, self.field_caption), .65)
        self.play_t(Write(self.eq_flux), 1.55)
        self.play_t(FadeIn(self.inner_arrows), .75)
        # The r^3 on the right divided by r^2 on the left leaves r.
        self.play_t(Indicate(self.eq_flux, color=GOLD, scale_factor=1.02), .95)
        self.play_t(Write(self.eq_field), 1.75)
        self.play_t(Indicate(self.eq_field, color=GOLD, scale_factor=1.025), 1.2)
        self.play_t(ReplacementTransform(self.field_caption, self.center_caption), .65)
        self.play_t(FadeOut(self.inner_arrows), .35)
        self.play_t(FadeIn(self.center_dot), .3)
        self.play_t(Write(self.eq_zero), 1.0)
        self.play_t(Indicate(self.eq_zero, color=CYAN, scale_factor=1.05), .9)
        self.end_beat(last=True)

    def construct(self):
        self.camera.background_color = BG
        self.clock = 0.0
        folder = Path(__file__).resolve().parent
        self.clips = [folder / f"S12_B0{i}_ar.wav" for i in (1, 2, 3)]
        whole = folder / "S12_ar.wav"
        self.mode = "silent"
        # Planned beat lengths: speech + silent reading hold.
        beat_speech = [12., 19., 18.]
        beat_holds = [3., 3., 4.]
        self.beat_lengths = [15., 22., 22.]
        if all(c.is_file() and wav_length(c) > 0 for c in self.clips):
            self.mode = "clips"
            self.beat_lengths = [max(s, wav_length(c)) + h for s, h, c
                                 in zip(beat_speech, beat_holds, self.clips)]
        elif whole.is_file() and wav_length(whole) > 0:
            self.mode = "whole"
            # Continuous track begins after the 1 s setup. It needs timestamps
            # matching the paragraph beats: +0s, +15s, +37s.
            # Protect the final narration tail instead of truncating it.
            self.beat_lengths[2] += max(0., wav_length(whole) - 59.)
            print("One-file S12 narration: paragraphs should start at 0, 15, 37 s within WAV")
        print(f"S12 mode={self.mode}; total={1 + sum(self.beat_lengths):.2f}s; "
              f"beat lengths={self.beat_lengths}")

        self.make_visuals()
        self.play_t(FadeIn(self.title), .8)
        self.hold(.2)  # exactly 1 second silent setup
        if self.mode == "whole":
            self.add_sound(str(whole))
        self.beat_1()
        self.beat_2()
        self.beat_3()
        expected = 1 + sum(self.beat_lengths)
        assert abs(self.clock - expected) < 1/30 + 0.001, (self.clock, expected)


if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "manim", "-p", "-qh", "-r", "1920,1080",
        "--fps", "30", str(Path(__file__).resolve()), "GaussScene12"
    ], check=True)
