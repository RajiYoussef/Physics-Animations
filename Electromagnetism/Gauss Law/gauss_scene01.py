"""Gauss's law | Arabic Scene S01

Run this file directly in PyCharm. The __main__ block renders and opens the video.
Requires: manim Community, a working LaTeX installation, and Noto Sans Arabic
(or change ARABIC_FONT to an installed Arabic-shaping font).

Optional audio: put S01_B01_ar.wav, S01_B02_ar.wav, S01_B03_ar.wav
next to this script. Without them, this renders a silent 56-second animatic.
"""

from pathlib import Path
import math
import wave

from manim import (
    Scene, Text, MathTex, Circle, Ellipse, Dot, Arrow, VGroup, DashedVMobject,
    FadeIn, FadeOut, Create, Write, Indicate, AnimationGroup,
    WHITE, config, linear,
)
import numpy as np

# Exact video specification
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.frame_width = 14.2222222222
config.frame_height = 8.0
config.background_color = "#101820"

WHITE_TEXT = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
VIOLET = "#C792EA"
POSITIVE = "#FF6B6B"
ARABIC_FONT = "Noto Sans Arabic"  # Pango/Manim Text shapes Arabic contextually.

HERE = Path(__file__).resolve().parent
AUDIO_FILES = [HERE / f"S01_B0{i}_ar.wav" for i in (1, 2, 3)]
SPEECH_WINDOWS = [14.0, 14.0, 17.0]
HOLDS = [3.0, 3.0, 4.0]


def clip_duration(path: Path):
    """WAV duration, or None if unavailable; no audio file is required."""
    if not path.is_file():
        return None
    try:
        with wave.open(str(path), "rb") as sound:
            return sound.getnframes() / sound.getframerate()
    except (wave.Error, EOFError, OSError, ZeroDivisionError) as exc:
        print(f"Audio {path.name} could not be read ({exc}); using silence.")
        return None


class GaussScene01(Scene):
    def construct(self):
        # Local scene clock makes timing auditable. No external scene state.
        self.elapsed = 0.0
        center = np.array([-3.65, -0.25, 0.0])
        sphere_radius = 1.72

        def wait_to(moment):
            delta = moment - self.elapsed
            if delta > 0.00001:
                self.wait(delta)
                self.elapsed += delta

        def play_for(duration, *animations):
            self.play(*animations, run_time=duration)
            self.elapsed += duration

        def ar(text, font_size=30, color=WHITE_TEXT):
            # Keep Arabic words entirely separate from LTR MathTex objects.
            return Text(text, font=ARABIC_FONT, font_size=font_size,
                        color=color, disable_ligatures=False)

        # All positions avoid the lowest 12% of the screen (y < -3.04).
        title = ar("سطح مغلق يكشف الشحنة المحصورة", 39).move_to([0, 3.08, 0])
        sphere_caption = ar("سطح كروي مغلق", 26).move_to([-3.65, -2.44, 0])

        charge = Dot(center, radius=0.185, color=POSITIVE)
        charge_plus = MathTex("+", color=WHITE_TEXT, font_size=36).move_to(center)
        charge_group = VGroup(charge, charge_plus)

        # This is explicitly a *projection* of a spherical SURFACE, not a 2D
        # integration contour. The ellipse indicates the sphere's equator.
        outline = Circle(radius=sphere_radius, color=CYAN, stroke_width=3.0)
        outline.set_stroke(opacity=0.95)
        outline.set_fill(CYAN, opacity=0.045)
        outline.move_to(center)
        outline = DashedVMobject(outline, num_dashes=36, dashed_ratio=0.57)
        equator = Ellipse(width=2 * sphere_radius, height=0.70,
                          color=CYAN, stroke_width=1.4).move_to(center)
        equator.set_stroke(opacity=0.44)

        field_arrows = VGroup()
        for j in range(10):
            angle = (2 * math.pi * j / 10) + math.pi / 10
            vector = np.array([math.cos(angle), math.sin(angle), 0.0])
            field_arrows.add(Arrow(
                center + 0.49 * vector,
                center + 2.05 * vector,
                buff=0,
                color=GOLD,
                stroke_width=4.0,
                max_tip_length_to_length_ratio=0.15,
                tip_length=0.17,
            ))

        # A single local outward normal, tied visually to the surface patch.
        normal_dir = np.array([math.cos(math.pi / 5), math.sin(math.pi / 5), 0])
        normal = Arrow(center + 1.70 * normal_dir,
                       center + 2.33 * normal_dir,
                       buff=0, color=VIOLET, stroke_width=5,
                       tip_length=0.15)

        # EXACT requested LaTeX, split into fragments only for selective reveals.
        # Concatenating fragments gives:
        # \Phi_E=\oint_S\mathbf E\cdot d\mathbf S=\frac{Q_{\mathrm{in}}}{\epsilon_0}
        equation = MathTex(
            r"\Phi_E", r"=", r"\oint_S", r"\mathbf E\cdot d\mathbf S",
            r"=", r"\frac{Q_{\mathrm{in}}}{\epsilon_0}",
            font_size=48, color=WHITE_TEXT,
        ).move_to([2.27, 0.86, 0])
        equation.scale_to_fit_width(min(equation.width, 6.00))
        # With width 6, the rightmost x remains inside the 5% screen margin.

        learning_items = VGroup(
            ar("التدفق", 31),
            ar("التناظر", 31),
            ar("الشحنة المحصورة", 31),
        )
        for item, y in zip(learning_items, (-0.65, -1.35, -2.05)):
            item.move_to([2.25, y, 0])

        # PRELOAD AUDIO DURATIONS, but add clips at each beat start only.
        measured = [clip_duration(p) for p in AUDIO_FILES]
        actual_speech = [max(expected, measured[i] or 0.0)
                         for i, expected in enumerate(SPEECH_WINDOWS)]
        beat_durations = [actual_speech[i] + HOLDS[i] for i in range(3)]
        print("S01 audio/timing budget (seconds):")
        cursor = 1.0
        for i in range(3):
            print(f"  B0{i+1}: start={cursor:.2f}, speech={actual_speech[i]:.2f}, "
                  f"hold={HOLDS[i]:.2f}, end={cursor + beat_durations[i]:.2f}; "
                  f"audio={'yes' if measured[i] is not None else 'no'}")
            cursor += beat_durations[i]
        print(f"  Total scheduled duration: {cursor:.2f}s (silent default: 56.00s)")

        # Initial 1-second silent preparation: blank, steady camera.
        wait_to(1.0)

        # BEAT 1: 00:01-00:18 in silent preview.
        b1 = self.elapsed
        if measured[0] is not None:
            self.add_sound(str(AUDIO_FILES[0]))
        play_for(0.65, FadeIn(charge_group))
        play_for(1.25, Create(outline), FadeIn(equator))
        play_for(0.75, FadeIn(sphere_caption))
        play_for(1.20, AnimationGroup(*[Create(a) for a in field_arrows], lag_ratio=0.05))
        play_for(1.0, FadeIn(title))
        # Physically meaningful cues, not endlessly moving ornamentation.
        wait_to(b1 + 7.4)
        play_for(0.85, Indicate(charge_group, color=POSITIVE, scale_factor=1.15))
        wait_to(b1 + 11.5)
        play_for(0.90, Indicate(outline, color=CYAN, scale_factor=1.025))
        wait_to(b1 + actual_speech[0])  # remainder of actual narration window
        wait_to(b1 + beat_durations[0])  # explicitly silent 3-second hold

        # BEAT 2: equation is built LEFT TO RIGHT; all mathematical notation
        # remains LTR, and no explanatory English/narration text is displayed.
        b2 = self.elapsed
        if measured[1] is not None:
            self.add_sound(str(AUDIO_FILES[1]))
        play_for(0.70, Write(equation[0]))
        play_for(0.35, Write(equation[1]))
        play_for(0.75, Write(equation[2]))
        play_for(0.95, Write(equation[3]))
        play_for(0.35, Write(equation[4]))
        play_for(0.95, Write(equation[5]))
        wait_to(b2 + 5.25)
        play_for(0.90, Indicate(equation[2], color=CYAN, scale_factor=1.13))
        wait_to(b2 + 7.1)
        play_for(0.70, FadeIn(normal))
        play_for(0.90, Indicate(equation[3], color=VIOLET, scale_factor=1.06))
        wait_to(b2 + 10.1)
        play_for(0.90, Indicate(equation[5], color=POSITIVE, scale_factor=1.07))
        play_for(0.65, Indicate(charge_group, color=POSITIVE, scale_factor=1.20))
        wait_to(b2 + actual_speech[1])
        wait_to(b2 + beat_durations[1])

        # BEAT 3: only the exact audience-facing labels appear.
        b3 = self.elapsed
        if measured[2] is not None:
            self.add_sound(str(AUDIO_FILES[2]))
        wait_to(b3 + 0.9)
        play_for(0.75, FadeIn(learning_items[0]))
        wait_to(b3 + 5.0)
        play_for(0.75, FadeIn(learning_items[1]))
        wait_to(b3 + 9.5)
        play_for(0.75, FadeIn(learning_items[2]))
        wait_to(b3 + 13.0)
        play_for(0.85, Indicate(equation, color=WHITE_TEXT, scale_factor=1.025))
        wait_to(b3 + actual_speech[2])
        # Final hold is static; optional fade ONLY in its last 0.5 seconds.
        wait_to(b3 + beat_durations[2] - 0.5)
        all_visible = VGroup(title, sphere_caption, charge_group, outline,
                             equator, field_arrows, normal, equation, learning_items)
        play_for(0.50, FadeOut(all_visible))

        planned = 1 + sum(14 + 3 if k < 2 else 17 + 4 for k in range(3))
        assert abs(planned - 56) < 1e-6
        print(f"S01 final scheduled timeline: {self.elapsed:.3f}s")


# =============================================================
# PYCHARM: CLICK RUN TO RENDER AND AUTOMATICALLY OPEN THE VIDEO
# =============================================================
if __name__ == "__main__":
    import subprocess
    import sys

    subprocess.run(
        [
            sys.executable, "-m", "manim",
            "-p",            # Automatically open completed video
            "-qh",           # High-quality rendering
            "-r", "1920,1080",
            "--fps", "30",
            str(Path(__file__).resolve()),
            "GaussScene01",
        ],
        cwd=str(HERE),
        check=True,
    )
