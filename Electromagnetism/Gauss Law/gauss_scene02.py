"""S02 — Electric flux through one small surface patch.

Run this file using PyCharm's Run button. The rendering launcher is at the END.
Requires manim Community, a LaTeX installation and an Arabic shaping font.
Optional files alongside the script: S02_B01_ar.wav, S02_B02_ar.wav, S02_B03_ar.wav.
Silent preview: 52 seconds / 1560 frames at 30 fps.
"""
from __future__ import annotations

import math
import subprocess
import sys
import wave
from pathlib import Path

from manim import *

BG = "#101820"
WHITE_INK = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
VIOLET = "#C792EA"
POS = "#FF6B6B"
NEG = "#64B5F6"
MUTED = "#9CAEBB"
ROOT = Path(__file__).resolve().parent
# Select an installed font with complete Arabic coverage and Pango shaping.
ARABIC_FONT_CANDIDATES = (
    "Noto Naskh Arabic", "Noto Sans Arabic", "Amiri", "DejaVu Sans"
)


def arabic_font():
    try:
        import manimpango
        installed = set(manimpango.list_fonts())
        for font in ARABIC_FONT_CANDIDATES:
            if font in installed:
                return font
    except Exception:
        pass
    return "DejaVu Sans"


def audio_seconds(path: Path):
    if not path.is_file():
        return None
    try:
        with wave.open(str(path), "rb") as f:
            return f.getnframes() / f.getframerate()
    except (wave.Error, OSError, ZeroDivisionError):
        print(f"Audio not read as standard PCM WAV: {path.name}; silent beat used.")
        return None


class GaussScene02(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.font_ar = arabic_font()
        self.clock = 0.0
        self.shift_accum = 0.0
        self.beats = [("S02_B01_ar.wav", 1, 9, 3),
                      ("S02_B02_ar.wav", 13, 16, 3),
                      ("S02_B03_ar.wav", 32, 16, 4)]
        self.audio_lengths = [audio_seconds(ROOT / x[0]) for x in self.beats]
        self.current_target = 0.0

        # Fixed educational layout: left diagram, right formulas / signed flux bar.
        title = self.ar("التدفق عبر عنصر مساحة صغير", 35).move_to([0, 3.18, 0])
        title.set_opacity(0)
        self.add(title)

        self.center = np.array([-3.25, -0.45, 0.0])
        self.angle = ValueTracker(0.0)
        # theta measured from +E (right) to the violet unit normal.
        self.patch = always_redraw(self.make_patch)
        self.normal = always_redraw(self.make_normal)
        self.normal_tip = always_redraw(
            lambda: MathTex(r"\hat{\mathbf n}", color=VIOLET, font_size=33)
            .move_to(self.center + 1.74 * self.normal_unit() + 0.22 * self.tangent_unit())
        )
        self.field = Arrow(self.center, self.center + RIGHT * 2.25,
                           buff=0, color=GOLD, stroke_width=8,
                           max_tip_length_to_length_ratio=0.13)
        self.field_label = MathTex(r"\mathbf E", color=GOLD, font_size=40)
        self.field_label.next_to(self.field.get_end(), UP, buff=0.12)
        self.area_label = MathTex(r"dS", color=CYAN, font_size=35)
        self.area_label.move_to(self.center + DOWN * 1.35 + LEFT * 0.30)
        self.patch_prose = self.ar("عنصر سطح مستوٍ، منظر جانبي", 24)
        self.patch_prose.move_to([-3.25, -2.62, 0])
        self.normal_prose = self.ar("متجه الوحدة العمودي", 24)
        self.normal_prose.move_to([-3.25, 1.60, 0])
        self.angle_arc = always_redraw(self.make_angle)
        self.projection = always_redraw(self.make_projection)

        self.eq1 = MathTex(r"d\mathbf S=\hat{\mathbf n}\,dS",
                           font_size=48, color=WHITE_INK).move_to([3.00, 1.65, 0])
        self.eq2parts = MathTex(r"d\Phi_E", r"=", r"\mathbf E\cdot d\mathbf S",
                                r"=", r"E\,dS\cos\theta",
                                font_size=43, color=WHITE_INK)
        self.eq2parts.move_to([2.72, 0.72, 0])
        self.angle_label = MathTex(r"\theta", font_size=31, color=WHITE_INK)
        self.angle_label.add_updater(
            lambda m: m.move_to(self.center + 0.79 * np.array([
                math.cos(self.angle.get_value() / 2),
                math.sin(self.angle.get_value() / 2), 0
            ]) + UP * 0.05)
        )
        self.component_label = self.ar("مركبة المجال العمودية على السطح", 22)
        self.component_label.move_to([2.9, -0.10, 0])

        # Flux scale is SIGNED; the bar stretches from the vertical zero line.
        self.bar_axis = Line([0.60, -1.55, 0], [5.75, -1.55, 0],
                             color=MUTED, stroke_width=2)
        self.zero_x = 3.18
        self.zero_line = Line([self.zero_x, -1.22, 0],
                              [self.zero_x, -1.87, 0], color=WHITE_INK, stroke_width=2)
        self.bar = always_redraw(self.make_signed_bar)
        self.flux_formula = MathTex(r"d\Phi_E=+E\,dS", font_size=37,
                                    color=CYAN).move_to([3.15, -2.18, 0])
        self.flux_status = self.ar("تدفق موجب", 30).move_to([3.15, -2.77, 0])

        # 1-second silent setup. No narrated concepts are displayed early.
        self.pause(1)

        # B01: patch -> perpendicular normal -> scalar area -> equation.
        self.begin_beat(0)
        self.play_timed(FadeIn(title, shift=DOWN * 0.08), 0.8)
        self.add(self.patch)
        self.pause(1.2)  # Updater-driven patch: add rather than Create.
        self.play_timed(FadeIn(self.patch_prose), 0.6)
        self.add(self.normal)
        self.pause(1.0)  # Updater-driven normal: add rather than GrowArrow.
        self.add(self.normal_tip)
        self.play_timed(FadeIn(self.normal_prose), 0.5)
        self.play_timed(FadeIn(self.area_label), 0.6)
        self.play_timed(Write(self.eq1), 1.3)
        self.play_timed(Indicate(self.eq1, color=CYAN, scale_factor=1.03), 0.9)
        self.end_beat()

        # B02: turn the normal / patch to 45 degrees, E stays fixed.
        self.begin_beat(1)
        self.play_timed(self.angle.animate.set_value(PI / 4), 1.0)
        self.play_timed(GrowArrow(self.field), 1.0)
        self.play_timed(FadeIn(self.field_label), 0.5)
        self.add(self.angle_arc, self.angle_label)
        self.pause(0.5)  # Angle arc is updater-driven; reveal without FadeIn interpolation.
        self.play_timed(Write(self.eq2parts[0:3]), 1.5)
        self.add(self.projection)
        self.pause(0.6)  # Projection is always_redraw; FadeIn causes family mismatch.
        self.play_timed(Write(self.eq2parts[3:]), 1.2)
        self.play_timed(FadeIn(self.component_label), 0.7)
        self.play_timed(Indicate(self.eq2parts[-1], color=GOLD), 0.9)
        self.end_beat()

        # B03: same patch, constant E and dS; theta = 0°, 90°, 180°.
        self.begin_beat(2)
        self.remove(self.projection, self.angle_arc, self.angle_label)
        self.play_timed(FadeOut(self.component_label), 0.6)
        self.play_timed(self.angle.animate.set_value(0), 0.8)
        self.add(self.bar_axis, self.zero_line, self.bar)
        self.play_timed(FadeIn(self.flux_formula, self.flux_status), 0.7)
        self.play_timed(Indicate(self.flux_formula, color=CYAN), 0.7)
        self.pause(1.0)
        self.play_timed(self.angle.animate.set_value(PI / 2), 1.1)
        self.set_flux_text(r"d\Phi_E=0", "تدفق صفري", WHITE_INK)
        self.pause(1.0)
        self.play_timed(self.angle.animate.set_value(PI), 1.1)
        self.set_flux_text(r"d\Phi_E=-E\,dS", "تدفق سالب", NEG)
        self.play_timed(Indicate(self.eq2parts[-1], color=GOLD), 0.9)
        self.end_beat(last=True)
        print(f"S02 finished: {self.clock:.3f}s; audio extension: {self.shift_accum:.3f}s")

    def ar(self, string: str, size: int):
        return Text(string, font=self.font_ar, font_size=size, color=WHITE_INK)

    def normal_unit(self):
        t = self.angle.get_value()
        return np.array([math.cos(t), math.sin(t), 0.0])

    def tangent_unit(self):
        t = self.angle.get_value()
        return np.array([-math.sin(t), math.cos(t), 0.0])

    def make_patch(self):
        t = self.tangent_unit()
        return Line(self.center - 0.82 * t, self.center + 0.82 * t,
                    color=CYAN, stroke_width=13)

    def make_normal(self):
        return Arrow(self.center, self.center + 1.40 * self.normal_unit(),
                     buff=0, color=VIOLET, stroke_width=7,
                     max_tip_length_to_length_ratio=0.18)

    def make_angle(self):
        a = max(self.angle.get_value(), 0.001)
        return Arc(radius=0.64, start_angle=0, angle=a,
                   arc_center=self.center, color=WHITE_INK, stroke_width=3)

    def make_projection(self):
        u = self.normal_unit()
        endpoint = self.center + u * (2.25 * math.cos(self.angle.get_value()))
        # Projection of E onto the normal, plus a geometric guide.
        projected = Arrow(self.center, endpoint, buff=0, color=GOLD,
                          stroke_width=5, max_tip_length_to_length_ratio=0.17)
        guide = DashedLine(self.field.get_end(), endpoint,
                           color=MUTED, dash_length=0.11, stroke_width=2)
        label = MathTex(r"E\cos\theta", font_size=29, color=GOLD)
        label.move_to(endpoint + LEFT * 0.12 + UP * 0.31)
        return VGroup(guide, projected, label)

    def make_signed_bar(self):
        value = math.cos(self.angle.get_value())
        if abs(value) < 0.008:
            return Dot([self.zero_x, -1.55, 0], radius=0.06, color=WHITE_INK)
        width = 2.25 * abs(value)
        begin = self.zero_x if value >= 0 else self.zero_x - width
        return Rectangle(width=width, height=0.30, stroke_width=0,
                         fill_color=CYAN if value >= 0 else NEG,
                         fill_opacity=0.94).move_to([begin + width / 2, -1.55, 0])

    def set_flux_text(self, formula, prose, tint):
        next_formula = MathTex(formula, font_size=37, color=tint)
        next_formula.move_to([3.15, -2.18, 0])
        next_prose = self.ar(prose, 30).move_to([3.15, -2.77, 0])
        self.play_timed(Transform(self.flux_formula, next_formula), 0.6)
        self.play_timed(Transform(self.flux_status, next_prose), 0.6)

    def pause(self, seconds):
        self.wait(seconds)
        self.clock += seconds

    def play_timed(self, *animations, duration=None):
        # Accept either play_timed(animation, 0.8) or duration=0.8.
        if duration is None:
            *animations, duration = animations
        self.play(*animations, run_time=duration)
        self.clock += duration

    def begin_beat(self, index):
        self.index = index
        filename, start, speech, hold = self.beats[index]
        actual = self.audio_lengths[index]
        self.speech_len = max(float(speech), actual or 0.0)
        self.beat_start = self.clock
        self.beat_length = self.speech_len + hold
        if actual is not None:
            self.add_sound(str(ROOT / filename))
        print(f"{filename}: speech window={speech:.1f}s, actual={actual}, "
              f"scheduled={self.beat_length:.3f}s, starts={self.beat_start:.3f}s")

    def end_beat(self, last=False):
        elapsed = self.clock - self.beat_start
        remaining = self.beat_length - elapsed
        if remaining < -1e-6:
            raise RuntimeError(f"Beat {self.index+1} animations exceeded budget by {-remaining:.3f}s")
        # Hold the completed concept on screen; fading is optional per the brief.
        self.pause(remaining)
        _, _, speech, hold = self.beats[self.index]
        self.shift_accum += self.beat_length - (speech + hold)


# ===============================================================
# PYCHARM: CLICK RUN. RENDER AND OPEN THE FINISHED VIDEO.
# ===============================================================
if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "manim", "-p", "-qh",
        "-r", "1920,1080", "--fps", "30",
        str(Path(__file__).resolve()), "GaussScene02",
    ], check=True)
