"""Gauss law, scene 06. Run this file from PyCharm.

Optional narration: S06_ar.wav (whole narration) OR S06_B01_ar.wav,
S06_B02_ar.wav, S06_B03_ar.wav in the same directory.
Exact paragraph sync with a whole-scene WAV requires paragraph timestamps;
this version uses the planned intervals for its animations.
"""
from pathlib import Path
from html import escape
import contextlib
import math
import subprocess
import sys
import wave

import numpy as np
from manim import *

BG = "#101820"
WHITE_TEXT = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
PURPLE = "#C792EA"
RED_CHARGE = "#FF6B6B"
BLUE_CHARGE = "#64B5F6"
ARABIC_FONT = "Arial"  # Windows: choose an Arabic-shaping-capable installed font


def wav_seconds(path):
    if not path.is_file():
        return 0.0
    try:
        with contextlib.closing(wave.open(str(path), "rb")) as wav:
            return wav.getnframes() / wav.getframerate()
    except (wave.Error, OSError, ZeroDivisionError):
        return 0.0


class GaussScene06(Scene):
    def ar(self, text, font_size=26, color=WHITE_TEXT):
        """Pango/MarkupText Arabic shaping confirmed by user's S05 fix."""
        return MarkupText(
            escape(text), font=ARABIC_FONT,
            font_size=font_size, color=color,
        )

    def construct(self):
        self.camera.background_color = BG
        self.elapsed = 0.0
        self.folder = Path(__file__).resolve().parent
        self.budget = [17.0, 23.0, 25.0]  # starts at 1, 18, 41; ends at 66
        names = ["S06_B01_ar.wav", "S06_B02_ar.wav", "S06_B03_ar.wav"]
        self.clips = [self.folder / n for n in names]
        whole = self.folder / "S06_ar.wav"
        self.whole_audio = whole if whole.is_file() else None
        self.clip_lengths = [wav_seconds(p) for p in self.clips]
        if self.whole_audio:
            # Preserve the animation's beat plan; extend final hold if whole audio overruns.
            self.budget[-1] += max(0.0, wav_seconds(whole) + 1.0 - 66.0)
        else:
            speech = [14.0, 20.0, 21.0]
            holds = [3.0, 3.0, 4.0]
            self.budget = [max(s, m) + h for s, m, h in zip(speech, self.clip_lengths, holds)]

        self.title = self.ar("شحنة نقطية: التناظر يبسط المجال", font_size=40)
        self.title.to_edge(UP, buff=0.30)
        self.title.scale_to_fit_width(min(self.title.width, 11.6))
        self.center = np.array([-3.55, -0.28, 0.0])
        self.R = 1.67
        self.charge_disc = Circle(radius=0.21, fill_color=RED_CHARGE,
                                  fill_opacity=1, stroke_width=0).move_to(self.center)
        self.q_mark = MathTex("+Q", color=WHITE_TEXT, font_size=28).move_to(self.center)
        self.charge = VGroup(self.charge_disc, self.q_mark)
        self.sphere = DashedVMobject(Circle(radius=self.R, color=CYAN,
                                           stroke_width=3).move_to(self.center), num_dashes=48)
        self.equator = Ellipse(width=2*self.R, height=0.65, color=CYAN,
                               stroke_width=1.5).move_to(self.center).set_opacity(0.4)
        self.sphere_label = self.ar("تناظر كروي", 27).move_to([-3.55, -2.67, 0])
        self.radius_text = self.ar("نصف القطر", 23).move_to([-4.66, -1.05, 0])
        self.radius_symbol = MathTex("r", font_size=32, color=CYAN).move_to([-3.0, -0.95, 0])
        self.radius_tracker = ValueTracker(0.0)

        def radius_segment():
            a = self.radius_tracker.get_value()
            end = self.center + self.R * np.array([math.cos(a), math.sin(a), 0])
            return Line(self.center, end, color=CYAN, stroke_width=3)
        self.radius_line = always_redraw(radius_segment)
        angles = np.linspace(0, TAU, 10, endpoint=False)
        self.field_arrows = VGroup()
        for a in angles:
            vec = np.array([math.cos(a), math.sin(a), 0])
            start = self.center + (self.R-0.10)*vec
            end = self.center + (self.R+0.50)*vec
            self.field_arrows.add(Arrow(start, end, buff=0, color=GOLD,
                                         stroke_width=4, max_tip_length_to_length_ratio=0.25))
        self.normal_arrows = VGroup()
        for idx in [1, 6]:
            vec = np.array([math.cos(angles[idx]), math.sin(angles[idx]), 0])
            self.normal_arrows.add(Arrow(self.center+(self.R+0.12)*vec,
                                         self.center+(self.R+0.74)*vec,
                                         buff=0, stroke_width=3, color=PURPLE,
                                         max_tip_length_to_length_ratio=0.24))
        self.normal_tag = MathTex(r"\hat{\mathbf n}", color=PURPLE,
                                  font_size=30).next_to(self.normal_arrows[0], RIGHT, buff=0.08)
        self.same_size = self.ar("مقدار متساوٍ", 26).move_to([-3.55, 2.30, 0])
        self.radial_tag = self.ar("مجال شعاعي", 24).move_to([-3.55, -2.65, 0])
        self.normal_text = self.ar("المتجه العمودي إلى الخارج", 22).move_to([-3.55, -3.22, 0])

        # Fixed right-side equation column, one formula per line.
        eq_strings = [
            r"\mathbf E=E_r(r)\hat{\mathbf r}",
            r"\hat{\mathbf n}=\hat{\mathbf r}",
            r"E_r(r)\,4\pi r^2=\frac{Q}{\epsilon_0}",
            r"\mathbf E=\frac{Q}{4\pi\epsilon_0 r^2}\hat{\mathbf r}\quad(r>0)",
        ]
        eq_sizes = [37, 37, 37, 32]
        eq_y = [1.42, 0.37, -0.75, -1.94]
        self.eqs = []
        for expression, size, y in zip(eq_strings, eq_sizes, eq_y):
            eq = MathTex(expression, color=WHITE_TEXT, font_size=size)
            eq.move_to([3.05, y, 0])
            # Respect safety bounds irrespective of TeX font metrics.
            if eq.width > 5.95:
                eq.scale_to_fit_width(5.95)
            self.eqs.append(eq)
        self.positive_q = self.ar("شحنة نقطية", 25).move_to([-3.55, 2.30, 0])

        # One second of silent setup.
        self.play(FadeIn(self.title), run_time=0.7)
        self.elapsed += 0.7
        self.pause(0.3)
        if self.whole_audio:
            self.add_sound(str(self.whole_audio))

        self.start_beat(0)
        self.do( FadeIn(self.charge), duration=0.9)
        self.do(FadeIn(self.positive_q), duration=0.5)
        self.add(self.radius_line)  # dynamic tracker; avoid FadeIn on always_redraw
        self.do(self.radius_tracker.animate.set_value(TAU), duration=3.6)
        self.do(Write(self.eqs[0]), duration=1.35)
        self.do(Indicate(self.eqs[0], color=GOLD), duration=1.0)
        self.finish_beat()

        self.start_beat(1)
        self.do(Create(self.sphere), duration=1.5)
        self.do(Create(self.equator), duration=0.85)
        self.do(FadeIn(self.sphere_label), duration=0.6)
        self.do(FadeOut(self.positive_q), duration=0.45)
        self.do(FadeIn(self.radius_text), FadeIn(self.radius_symbol), duration=0.75)
        self.do(LaggedStart(*[GrowArrow(a) for a in self.field_arrows], lag_ratio=0.08), duration=2.7)
        self.do(FadeIn(self.same_size), duration=0.7)
        self.do(Indicate(self.same_size, color=GOLD), duration=0.7)
        self.do(LaggedStart(*[GrowArrow(a) for a in self.normal_arrows], lag_ratio=0.3), duration=1.6)
        self.do(FadeIn(self.normal_tag), duration=0.45)
        self.do(ReplacementTransform(self.sphere_label, self.normal_text),
                FadeIn(self.radial_tag), duration=0.65)
        self.do(Write(self.eqs[1]), duration=1.0)
        self.do(Indicate(self.eqs[1], color=PURPLE), duration=1.1)
        self.finish_beat()

        self.start_beat(2)
        self.do(Write(self.eqs[2]), duration=1.6)
        self.do(Indicate(self.eqs[2], color=GOLD), duration=1.0)
        self.do(Write(self.eqs[3]), duration=1.8)
        self.do(Circumscribe(self.eqs[3], color=CYAN), duration=1.3)
        # Highlight the denominator r^2 by indicating the final formula and its falloff.
        self.do(Indicate(self.eqs[3], color=GOLD), duration=1.2)
        self.finish_beat(final=True)

        total_expected = 1.0 + sum(self.budget)
        # without audio: exactly 66 seconds (1 + 17 + 23 + 25)
        print(f"S06 scheduled scene duration: {total_expected:.2f} seconds")

    def pause(self, seconds):
        if seconds > 1e-6:
            self.wait(seconds)
            self.elapsed += seconds

    def do(self, *animations, duration):
        self.play(*animations, run_time=duration)
        self.elapsed += duration

    def start_beat(self, index):
        self.end_at = self.elapsed + self.budget[index]
        if not self.whole_audio and self.clips[index].is_file():
            self.add_sound(str(self.clips[index]))

    def finish_beat(self, final=False):
        remaining = self.end_at - self.elapsed
        if remaining < -0.02:
            raise RuntimeError(f"Scene S06 animation overran beat by {-remaining:.2f} s")
        if final:
            # Never cut the narration: fade after the final static reading hold.
            self.pause(max(0.0, remaining - 0.5))
            rest = min(0.5, remaining)
            if rest > 0:
                # Group, not VGroup: supports all scene mobject types.
                self.do(FadeOut(Group(*list(self.mobjects))), duration=rest)
        else:
            self.pause(remaining)


# ==================================================
# RENDER FROM PYCHARM — AUTOMATIC VIDEO OPENING
# ==================================================
if __name__ == "__main__":
    subprocess.run(
        [sys.executable, "-m", "manim", "-p", "-qh", "-r", "1920,1080",
         "--fps", "30", str(Path(__file__).resolve()), "GaussScene06"],
        check=True,
    )
