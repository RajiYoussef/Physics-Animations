"""GaussScene04 — Count net enclosed charge.

Run directly in PyCharm. The __main__ block at the end renders and opens the video.
Optional audio: ONE `S04_ar.wav` file, OR individual `S04_B01_ar.wav`,
`S04_B02_ar.wav`, `S04_B03_ar.wav` files next to this script.
No audio files are required for a 61-second silent preview.
"""
from __future__ import annotations

import contextlib
from pathlib import Path
import subprocess
import sys
import wave
import numpy as np
from manim import *

BG = "#101820"
WHITE = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
VIOLET = "#C792EA"
RED = "#FF6B6B"
BLUE = "#64B5F6"
ARABIC_FONT = "Noto Sans Arabic"  # Windows fallback below


def arabic_font():
    from manimpango import list_fonts
    names = list_fonts()
    for preferred in ("Noto Sans Arabic", "Arial", "Tahoma", "Amiri"):
        if any(preferred.casefold() in name.casefold() for name in names):
            return preferred
    raise RuntimeError("Install an Arabic-capable font (Noto Sans Arabic, Arial, or Tahoma).")


def audio_length(path):
    if not path.is_file():
        return 0.0
    with contextlib.closing(wave.open(str(path), "rb")) as f:
        return f.getnframes() / f.getframerate()


class GaussScene04(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0
        self.assets = Path(__file__).resolve().parent
        self.font = arabic_font()
        # Silent preview: 1s setup + 20s + 20s + 20s = 61 seconds.
        # Beat speech budgets: 17s, 17s, 16s; holds: 3s, 3s, 4s.
        self.speeches = [17.0, 17.0, 16.0]
        self.holds = [3.0, 3.0, 4.0]
        self.beat_paths = [self.assets / f"S04_B{i:02d}_ar.wav" for i in range(1, 4)]
        self.single_path = self.assets / "S04_ar.wav"
        self.one_clip = self.single_path.is_file()
        if self.one_clip:
            # A combined clip is anchored at second 1. Paragraph positions follow the
            # planned beat marks; for precise sync, export beat files or cue points.
            length = audio_length(self.single_path)
            self.durations = [20.0, 20.0, max(20.0, length - 40.0 + 4.0)]
            print(f"[S04] Combined audio: {length:.2f}s. Planned paragraph starts: 1, 21, 41s.")
        else:
            self.durations = [
                max(self.speeches[i], audio_length(self.beat_paths[i])) + self.holds[i]
                for i in range(3)
            ]
        print("[S04] Beat lengths:", [round(d, 2) for d in self.durations],
              "scene length:", round(1 + sum(self.durations), 2))
        self.build()
        self.animate_setup()
        self.beat1()
        self.beat2()
        self.beat3()
        expected = 1 + sum(self.durations)
        assert abs(self.t - expected) < 0.05, (self.t, expected)

    def ar(self, string, font_size=29, color=WHITE):
        return Text(string, font=self.font, font_size=font_size, color=color)

    def step(self, *actions, seconds):
        if seconds > 0:
            self.play(*actions, run_time=seconds)
            self.t += seconds

    def pause(self, seconds):
        if seconds > 0.0001:
            self.wait(seconds)
            self.t += seconds

    def start_beat(self, index):
        if not self.one_clip and self.beat_paths[index].is_file():
            self.add_sound(str(self.beat_paths[index]))
        self.end = self.t + self.durations[index]

    def finish_beat(self, fade=False):
        left = self.end - self.t
        if left < -0.001:
            raise RuntimeError(f"Beat overran its audio and timing budget by {-left:.2f}s")
        if fade:
            self.pause(max(0, left - 0.5))
            self.step(FadeOut(Group(*list(self.mobjects))), seconds=min(0.5, left))
        else:
            self.pause(left)

    def build(self):
        self.title = self.ar("احسب الشحنة الصافية داخل السطح", 40)
        self.title.move_to([0, 3.28, 0])
        self.center = np.array([-4.25, -0.10, 0.0])
        self.R = 1.72
        outline = Circle(radius=self.R, color=CYAN, stroke_width=3).move_to(self.center)
        self.surface = DashedVMobject(outline, num_dashes=38)
        self.equator = Ellipse(width=3.15, height=0.72, color=CYAN,
                               stroke_width=1.7).move_to(self.center).set_opacity(0.38)
        self.sphere_label = self.ar("داخل السطح", 25).move_to([-4.45, -2.25, 0])
        self.outside_label = self.ar("خارج السطح", 23).move_to([-1.75, -1.12, 0])

        def charge(tex, pos, color):
            disk = Circle(radius=0.32, fill_color=color, fill_opacity=0.20,
                          stroke_color=color, stroke_width=2.5).move_to(pos)
            sign = MathTex(tex, color=color, font_size=36).move_to(pos)
            return VGroup(disk, sign)

        self.plus2 = charge(r"+2q", [-4.90, 0.58, 0], RED)
        self.minus = charge(r"-q", [-3.67, -0.78, 0], BLUE)
        self.external = charge(r"+q", [-1.83, 0.49, 0], RED)
        # Distances from sphere center guarantee outside charge stays outside.
        assert np.linalg.norm(self.external.get_center() - self.center) > self.R + 0.35
        self.ledger_heading = self.ar("الشحنة الصافية المحصورة", 27)
        self.ledger_heading.move_to([2.65, 2.04, 0])
        self.eq_count = MathTex(
            r"Q_{\mathrm{in}}=\sum_{i\,\mathrm{inside}}Q_i",
            color=WHITE, font_size=38
        ).move_to([2.57, 1.24, 0])
        self.eq_arith = MathTex(r"Q_{\mathrm{in}}=2q-q=q", color=WHITE,
                                font_size=41).move_to([2.54, 0.37, 0])
        self.eq_flux = MathTex(r"\Phi_E=\frac{q}{\epsilon_0}", color=WHITE,
                               font_size=43).move_to([2.55, -0.52, 0])
        self.external_note = self.ar("تؤثر في المجال، ومساهمتها في صافي التدفق صفر", 22)
        self.external_note.scale_to_fit_width(5.7)
        self.external_note.move_to([2.48, -1.65, 0])

        self.volume_label = self.ar("الحجم المحصور", 24)
        self.volume_label.move_to([-4.25, -2.24, 0])
        self.density_label = self.ar("كثافة الشحنة الحجمية", 26)
        self.density_label.move_to([2.5, 1.98, 0])
        self.eq_density = MathTex(r"Q_{\mathrm{in}}=\int_V\rho_v\,dV",
                                  color=WHITE, font_size=42).move_to([2.57, 0.64, 0])
        self.rho_math = MathTex(r"\rho_v", color=GOLD, font_size=32).move_to([1.4, -0.35, 0])
        self.vol_math = MathTex(r"V", color=CYAN, font_size=32).move_to([3.7, -0.35, 0])
        self.cloud = VGroup()
        # Deterministic, continuous-volume schematic: overlapping translucent shapes,
        # not discrete point charges or a surface-charge shell.
        for k in range(5):
            r = 1.41 - 0.20*k
            self.cloud.add(Circle(radius=r, stroke_width=0,
                                  fill_color=RED, fill_opacity=0.045).move_to(self.center))

    def animate_setup(self):
        self.step(FadeIn(self.title), FadeIn(self.surface), FadeIn(self.equator), seconds=1.0)
        if self.one_clip:
            self.add_sound(str(self.single_path))

    def beat1(self):
        self.start_beat(0)
        self.step(FadeIn(self.plus2), seconds=1.1)
        self.step(FadeIn(self.minus), seconds=1.1)
        self.step(FadeIn(self.external), seconds=1.1)
        self.step(FadeIn(self.sphere_label), FadeIn(self.outside_label), seconds=0.9)
        self.step(Circumscribe(self.plus2, color=RED), seconds=1.1)
        self.step(Circumscribe(self.minus, color=BLUE), seconds=1.1)
        self.step(FadeIn(self.ledger_heading), seconds=0.7)
        self.step(Write(self.eq_count), seconds=1.2)
        self.step(Write(self.eq_arith), seconds=1.2)
        self.step(Indicate(self.eq_arith, color=GOLD), seconds=1.1)
        self.step(Write(self.eq_flux), seconds=1.3)
        self.step(Indicate(self.eq_flux, color=GOLD), seconds=1.0)
        self.finish_beat()

    def beat2(self):
        self.start_beat(1)
        self.step(Circumscribe(self.external, color=RED), seconds=1.4)
        self.step(FadeIn(self.external_note), seconds=1.0)
        # External charge changes the field on S but not enclosed charge;
        # symbolic field arrows show its influence on the surface without
        # implying any charge has crossed the boundary.
        arrows = VGroup()
        for y in (-0.55, -0.05, 0.45):
            start = np.array([-2.55, y, 0.0])
            end = start + np.array([-0.55, (y-0.45)*0.08, 0.0])
            arrows.add(Arrow(start, end, buff=0, color=GOLD,
                              stroke_width=3, max_tip_length_to_length_ratio=0.17))
        self.step(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25), seconds=1.6)
        self.step(Indicate(self.eq_count, color=WHITE), seconds=1.5)
        self.step(Indicate(self.eq_arith, color=GOLD), seconds=1.3)
        self.step(Indicate(self.external, color=RED), seconds=1.3)
        self.step(Indicate(self.eq_flux, color=WHITE), seconds=1.3)
        self.step(FadeOut(arrows), seconds=1.0)
        self.finish_beat()

    def beat3(self):
        self.start_beat(2)
        self.step(FadeOut(self.plus2), FadeOut(self.minus), seconds=1.0)
        self.step(FadeIn(self.cloud), seconds=1.4)
        self.step(FadeOut(self.sphere_label), FadeIn(self.volume_label), seconds=0.8)
        self.step(FadeOut(self.ledger_heading), FadeOut(self.eq_count),
                  FadeOut(self.eq_arith), FadeOut(self.eq_flux),
                  FadeOut(self.external_note), seconds=1.4)
        self.step(FadeIn(self.density_label), seconds=0.9)
        self.step(Write(self.eq_density), seconds=1.6)
        self.step(FadeIn(self.rho_math), FadeIn(self.vol_math), seconds=0.9)
        self.step(Indicate(self.rho_math, color=GOLD), seconds=1.0)
        self.step(Indicate(self.vol_math, color=CYAN), seconds=1.0)
        self.step(Indicate(self.cloud, color=RED, scale_factor=1.015), seconds=1.1)
        self.step(Indicate(self.eq_density, color=WHITE), seconds=1.0)
        self.finish_beat(fade=True)


# ==================================================
# RENDER — RUN THIS FILE DIRECTLY IN PYCHARM
# ==================================================
if __name__ == "__main__":
    subprocess.run(
        [sys.executable, "-m", "manim", "-p", "-qh", "-r", "1920,1080",
         "--fps", "30", str(Path(__file__).resolve()), "GaussScene04"],
        check=True,
    )
