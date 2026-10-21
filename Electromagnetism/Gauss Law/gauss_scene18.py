"""GaussScene18 — Three questions to carry forward.

Standalone Manim Community scene. Place optional audio next to this file:
  S18_ar.wav (entire 59-second narration after the 1-second setup), OR
  S18_B01_ar.wav, S18_B02_ar.wav, S18_B03_ar.wav.
If recordings overrun their speech windows, the corresponding beats extend.
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
WHITEISH = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
VIOLET = "#C792EA"
POSITIVE = "#FF6B6B"
NEGATIVE = "#64B5F6"
ARABIC_FONT = "Arial"


def wav_duration(path: Path) -> float:
    """Read audio length without relying on an external audio dependency."""
    if not path.is_file():
        return 0.0
    try:
        with wave.open(str(path), "rb") as recording:
            return recording.getnframes() / recording.getframerate()
    except (OSError, wave.Error, ZeroDivisionError):
        return 0.0


class GaussScene18(Scene):
    def ar(self, message: str, size: int = 26, color: str = WHITEISH,
           max_width: float | None = None):
        result = MarkupText(escape(message), font=ARABIC_FONT,
                            font_size=size, color=color)
        if max_width is not None and result.width > max_width:
            result.scale_to_fit_width(max_width)
        return result

    def play_t(self, animation, duration: float):
        self.play(animation, run_time=duration)
        self.elapsed += duration

    def wait_t(self, duration: float):
        if duration > 1e-7:
            self.wait(duration)
            self.elapsed += duration

    def begin_beat(self, index: int):
        if self.audio_mode == "beats":
            self.add_sound(str(self.audio_files[index]))
        self.end_beat_time = self.elapsed + self.beat_lengths[index]

    def end_beat(self, final=False):
        remaining = self.end_beat_time - self.elapsed
        if remaining < -0.02:
            raise RuntimeError(f"Beat overran by {-remaining:.3f} seconds")
        if final and remaining >= 0.5:
            self.wait_t(remaining - 0.5)
            self.play_t(FadeOut(Group(*list(self.mobjects))), 0.5)
        else:
            self.wait_t(max(remaining, 0.0))

    def make_layout(self):
        # Title: within a 5% horizontal safe area.
        self.heading = self.ar("ثلاثة أسئلة تذكرها", 40, max_width=10.7)
        self.heading.move_to([0, 3.32, 0])

        self.cards = VGroup()
        self.card_borders = []
        texts = [
            "إلى أين تتجه المتجهات العمودية؟",
            "ماذا يخبرنا التناظر؟",
            "ما مقدار الشحنة الصافية في الداخل؟",
        ]
        for i, (sentence, y) in enumerate(zip(texts, [1.83, 0.82, -0.19])):
            outer = RoundedRectangle(
                corner_radius=0.16, width=5.70, height=0.78,
                stroke_color=CYAN, stroke_width=1.5,
                fill_color="#1B3040", fill_opacity=0.68,
            ).move_to([-3.41, y, 0])
            number = MathTex(str(i + 1), color=GOLD, font_size=32)
            number.move_to([-5.82, y, 0])
            label = self.ar(sentence, 25, max_width=4.7)
            label.move_to([-3.15, y, 0])
            self.cards.add(VGroup(outer, number, label))
            self.card_borders.append(outer)

        # Right column: mathematical objects never share a bounding box with Arabic prose.
        self.integral_label = self.ar("سطح مغلق", 24, color=CYAN)
        self.integral_label.move_to([3.28, 2.36, 0])
        self.integral = MathTex(
            r"\oint_S\mathbf E\cdot d\mathbf S=\frac{Q_{\mathrm{in}}}{\epsilon_0}",
            font_size=38, color=WHITEISH,
        ).move_to([3.14, 1.58, 0])
        self.differential_label = self.ar("كثافة الشحنة المحلية", 24, color=VIOLET)
        self.differential_label.move_to([3.28, 0.66, 0])
        self.differential = MathTex(
            r"\nabla\cdot\mathbf E=\frac{\rho_v}{\epsilon_0}",
            font_size=40, color=WHITEISH,
        ).move_to([3.14, -0.07, 0])

        # Lower row: small schematic icons occupy a dedicated band (no equations).
        self.icons = VGroup()
        self.icon_labels = VGroup()
        xs = (-4.0, 0.0, 4.0)

        # Positive point charge and its radially directed field.
        c = np.array([xs[0], -1.60, 0])
        point_icon = VGroup(Circle(radius=0.42, color=CYAN, stroke_width=1.6).move_to(c),
                            Dot(c, radius=0.085, color=POSITIVE))
        for theta in np.linspace(0, TAU, 8, endpoint=False):
            d = np.array([np.cos(theta), np.sin(theta), 0])
            point_icon.add(Arrow(c + 0.15*d, c + 0.38*d,
                                 color=GOLD, stroke_width=2.4, buff=0,
                                 max_tip_length_to_length_ratio=0.28))
        self.icons.add(point_icon)

        # Infinite line charge, sectioned cylindrical Gaussian surface.
        cx = xs[1]
        cylinder = VGroup(
            Ellipse(width=1.05, height=0.31, color=CYAN, stroke_width=1.8).move_to([cx, -1.23, 0]),
            Ellipse(width=1.05, height=0.31, color=CYAN, stroke_width=1.8).move_to([cx, -2.0, 0]),
            Line([cx-0.525, -1.23, 0], [cx-0.525, -2.0, 0], color=CYAN, stroke_width=1.8),
            Line([cx+0.525, -1.23, 0], [cx+0.525, -2.0, 0], color=CYAN, stroke_width=1.8),
            DashedLine([cx, -1.03, 0], [cx, -2.20, 0], color=POSITIVE, stroke_width=3),
        )
        for side in (-1, 1):
            cylinder.add(Arrow([cx+side*0.55, -1.61, 0],
                               [cx+side*0.89, -1.61, 0], color=GOLD,
                               buff=0, stroke_width=2.8))
        self.icons.add(cylinder)

        # Solid uniformly charged sphere, presented as a 2D section.
        c = np.array([xs[2], -1.60, 0])
        sphere = VGroup(Circle(radius=0.50, color=CYAN, stroke_width=2,
                               fill_color=CYAN, fill_opacity=0.18).move_to(c))
        for dx, dy in [(-.22, .19), (.20, .17), (-.15, -.19), (.20, -.18)]:
            sphere.add(MathTex("+", font_size=19, color=POSITIVE)
                       .move_to(c + np.array([dx, dy, 0])))
        self.icons.add(sphere)

        for x, string in zip(xs, ["شحنة نقطية", "خط شحنة لا نهائي", "كرة مشحونة بانتظام"]):
            self.icon_labels.add(self.ar(string, 23, max_width=3.3).move_to([x, -2.35, 0]))

        self.credit = self.ar(
            "المصدر: الفصل الثالث من كتاب الكهرومغناطيسية الأولية باستخدام بايثون، Anders Malthe-Sørenssen، 2022.",
            21, color="#BCC5CE", max_width=12.2,
        ).move_to([0, -2.90, 0])

    def beat_one(self):
        self.begin_beat(0)
        for card in self.cards:
            self.play_t(FadeIn(card, shift=RIGHT*0.12), 0.9)
            self.wait_t(1.0)
        self.play_t(Indicate(self.card_borders[0], color=VIOLET), 0.8)
        self.play_t(Indicate(self.card_borders[1], color=GOLD), 0.8)
        self.play_t(Indicate(self.card_borders[2], color=CYAN), 0.8)
        self.end_beat()

    def beat_two(self):
        self.begin_beat(1)
        self.play_t(FadeIn(self.integral_label), 0.65)
        self.play_t(Write(self.integral), 1.3)
        self.wait_t(2.0)
        self.play_t(FadeIn(self.differential_label), 0.65)
        self.play_t(Write(self.differential), 1.3)
        self.play_t(Indicate(self.integral, color=CYAN), 1.0)
        self.play_t(Indicate(self.differential, color=VIOLET), 1.0)
        self.end_beat()

    def beat_three(self):
        self.begin_beat(2)
        for icon, label in zip(self.icons, self.icon_labels):
            self.play_t(FadeIn(icon, scale=0.95), 0.7)
            self.play_t(FadeIn(label), 0.5)
            self.wait_t(1.0)
        self.play_t(Indicate(self.integral, color=GOLD), 1.1)
        self.play_t(Indicate(self.differential, color=GOLD), 1.1)
        self.play_t(FadeIn(self.credit), 1.0)
        self.end_beat(final=True)

    def construct(self):
        self.camera.background_color = BG
        self.elapsed = 0.0
        self.beat_lengths = [18.0, 17.0, 24.0]
        self.audio_mode = "silent"
        root = Path(__file__).resolve().parent
        full = root / "S18_ar.wav"
        separate = [root / f"S18_B0{i}_ar.wav" for i in (1, 2, 3)]

        if full.is_file():
            self.audio_mode = "full"
            self.audio_files = [full]
            # Full recording begins at 00:01. Narration fits within 55 s;
            # keep the four-second final reading hold after the last spoken word.
            self.beat_lengths[2] += max(0.0, wav_duration(full) + 4.0 - sum(self.beat_lengths))
            print(f"Full narration: {wav_duration(full):.2f}s; manual paragraph starts: 0, 18, 35s after audio start")
        elif all(p.is_file() for p in separate):
            self.audio_mode = "beats"
            self.audio_files = separate
            for i, (p, speech, hold) in enumerate(zip(separate, (15, 14, 20), (3, 3, 4))):
                self.beat_lengths[i] = max(float(speech), wav_duration(p)) + hold
        else:
            print("No complete narration asset set: rendering silent preview.")

        print(f"S18 duration: {1+sum(self.beat_lengths):.2f} seconds")
        self.make_layout()
        self.play_t(FadeIn(self.heading), 0.8)
        self.wait_t(0.2)
        if self.audio_mode == "full":
            self.add_sound(str(self.audio_files[0]))
        self.beat_one()
        self.beat_two()
        self.beat_three()
        assert abs(self.elapsed - (1+sum(self.beat_lengths))) < 1/30


if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "manim", "-p", "-qh", "-r", "1920,1080",
        "--fps", "30", str(Path(__file__).resolve()), "GaussScene18",
    ], check=True)
