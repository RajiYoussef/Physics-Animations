from __future__ import annotations

from manim import *
from pathlib import Path
import subprocess
import sys
import wave
import contextlib


# ==================================================
# Configuration
# ==================================================
BG = "#101820"
FG = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
VIOLET = "#C792EA"
POS_RED = "#FF6B6B"
NEG_BLUE = "#64B5F6"
ARABIC_FONT = "Arial"


class GaussScene03(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.clock = 0.0
        self.audio_dir = Path(__file__).resolve().parent

        # Planned beat structure: (filename, planned_speech_seconds, hold_seconds)
        self.beat_specs = {
            "B01": ("S03_B01_ar.wav", 14.0, 3.0),
            "B02": ("S03_B02_ar.wav", 15.0, 3.0),
            "B03": ("S03_B03_ar.wav", 17.0, 4.0),
        }
        self.beat_durations = {}
        for key, (filename, speech, hold) in self.beat_specs.items():
            audio_path = self.audio_dir / filename
            measured = self.get_wav_duration(audio_path)
            total = max(speech, measured) + hold
            self.beat_durations[key] = {
                "file": audio_path,
                "speech": speech,
                "hold": hold,
                "measured": measured,
                "total": total,
            }

        self.build_static_layout()
        self.initial_setup()
        self.beat_1()
        self.beat_2()
        self.beat_3()

    # --------------------------------------------------
    # Scene construction
    # --------------------------------------------------
    def build_static_layout(self):
        # Title
        self.title = Text(
            "من عناصر المساحة إلى السطح المغلق",
            font=ARABIC_FONT,
            color=FG,
            font_size=42,
        ).to_edge(UP, buff=0.25)

        # Left-side sphere schematic
        self.sphere_center = LEFT * 3.9 + DOWN * 0.2
        self.sphere_radius = 2.0
        self.sphere_outline = Circle(
            radius=self.sphere_radius,
            color=CYAN,
            stroke_width=3,
        ).move_to(self.sphere_center)
        self.sphere_outline_dashed = DashedVMobject(self.sphere_outline.copy(), num_dashes=36)
        self.equator = Ellipse(
            width=3.55,
            height=0.9,
            color=CYAN,
            stroke_width=2,
        ).move_to(self.sphere_center).set_stroke(opacity=0.55).set_fill(opacity=0)

        self.surface_label = Text(
            "سطح مغلق",
            font=ARABIC_FONT,
            color=FG,
            font_size=26,
        ).next_to(self.sphere_outline, DOWN, buff=0.35)

        self.patches_label = Text(
            "عناصر المساحة",
            font=ARABIC_FONT,
            color=FG,
            font_size=26,
        ).move_to(self.sphere_center + UP * 2.55)

        self.outward_normal_text = Text(
            "المتجه العمودي إلى الخارج",
            font=ARABIC_FONT,
            color=FG,
            font_size=24,
        ).move_to(self.sphere_center + DOWN * 2.6)

        # Sample patches around the sphere
        patch_angles_deg = [20, 60, 110, 160, 210, 250, 300, 335]
        self.patches = VGroup()
        self.normals = VGroup()
        for ang_deg in patch_angles_deg:
            ang = ang_deg * DEGREES
            radial = np.array([np.cos(ang), np.sin(ang), 0])
            point = self.sphere_center + radial * self.sphere_radius
            tangent_angle = ang + PI / 2

            patch = Rectangle(
                width=0.24,
                height=0.16,
                stroke_color=CYAN,
                stroke_width=2,
                fill_color=CYAN,
                fill_opacity=0.18,
            ).rotate(tangent_angle).move_to(point - radial * 0.04)
            self.patches.add(patch)

            arrow = Arrow(
                start=point,
                end=point + radial * 0.65,
                buff=0.0,
                stroke_width=4,
                color=VIOLET,
                max_tip_length_to_length_ratio=0.20,
            )
            self.normals.add(arrow)

        # One representative n-hat label
        ref_idx = 1
        ref_tip = self.normals[ref_idx].get_end()
        self.nhat_label = MathTex(r"\hat{\mathbf n}", color=VIOLET, font_size=34).next_to(
            ref_tip, RIGHT, buff=0.12
        )

        # Representative field arrows: one outward, one inward
        out_idx = 0
        in_idx = 5
        out_patch_center = self.patches[out_idx].get_center()
        out_dir = normalize(self.normals[out_idx].get_end() - self.normals[out_idx].get_start())
        self.field_out = Arrow(
            start=out_patch_center - out_dir * 0.35,
            end=out_patch_center + out_dir * 0.55,
            buff=0.0,
            color=GOLD,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )
        self.field_out_label = MathTex(r"\mathbf E_i", color=GOLD, font_size=30).next_to(
            self.field_out.get_end(), UR, buff=0.08
        )
        self.positive_tag = Text(
            "+",
            font=ARABIC_FONT,
            color=POS_RED,
            font_size=34,
            weight=BOLD,
        ).next_to(self.field_out.get_center(), UP, buff=0.1)

        in_patch_center = self.patches[in_idx].get_center()
        in_dir = -normalize(self.normals[in_idx].get_end() - self.normals[in_idx].get_start())
        self.field_in = Arrow(
            start=in_patch_center - in_dir * 0.45,
            end=in_patch_center + in_dir * 0.25,
            buff=0.0,
            color=GOLD,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )
        self.negative_tag = Text(
            "−",
            font=ARABIC_FONT,
            color=NEG_BLUE,
            font_size=34,
            weight=BOLD,
        ).next_to(self.field_in.get_center(), DOWN, buff=0.05)

        # Right-side equations and labels
        self.eq_sum = MathTex(
            r"\Phi_E\approx",
            r"\sum_i",
            r"\mathbf E_i\cdot\hat{\mathbf n}_i",
            r"\,\Delta S_i",
            color=FG,
            font_size=38,
        )
        self.eq_int = MathTex(
            r"\Phi_E=",
            r"\oint_S",
            r"\mathbf E\cdot\hat{\mathbf n}",
            r"\,dS",
            color=FG,
            font_size=38,
        )
        self.eq_sum.move_to(RIGHT * 3.25 + UP * 1.1)
        self.eq_int.move_to(self.eq_sum)

        self.net_flux_label = Text(
            "صافي التدفق إلى الخارج",
            font=ARABIC_FONT,
            color=FG,
            font_size=28,
        ).next_to(self.eq_int, DOWN, buff=0.45)

        # Tiny reminder labels for local geometry
        self.deltaS_label = MathTex(r"\Delta S_i", color=CYAN, font_size=30)
        self.closed_surface_note = Text(
            "الدائرة على رمز التكامل: سطح مغلق",
            font=ARABIC_FONT,
            color=FG,
            font_size=22,
        ).next_to(self.eq_int, DOWN, buff=1.2)

        # Invisible grouping used for final fade
        self.main_group = VGroup(
            self.title,
            self.sphere_outline_dashed,
            self.equator,
            self.surface_label,
            self.patches_label,
            self.outward_normal_text,
            self.patches,
            self.normals,
            self.nhat_label,
            self.field_out,
            self.field_out_label,
            self.positive_tag,
            self.field_in,
            self.negative_tag,
            self.eq_sum,
            self.eq_int,
            self.net_flux_label,
            self.closed_surface_note,
        )

    def initial_setup(self):
        # 1-second silent setup before beat 1
        self.play(
            FadeIn(self.title, shift=DOWN * 0.15),
            FadeIn(self.sphere_outline_dashed),
            FadeIn(self.equator),
            FadeIn(self.surface_label),
            run_time=0.8,
        )
        self.clock += 0.8
        self.wait(0.2)
        self.clock += 0.2

    def beat_1(self):
        self.begin_beat("B01")

        self.play_timed(FadeIn(self.patches_label), 0.7)
        self.play_timed(
            LaggedStart(*[FadeIn(patch, scale=0.8) for patch in self.patches], lag_ratio=0.12),
            2.0,
        )
        self.play_timed(
            LaggedStart(*[GrowArrow(arrow) for arrow in self.normals], lag_ratio=0.10),
            3.8,
        )
        self.play_timed(FadeIn(self.nhat_label), 0.6)
        self.play_timed(FadeIn(self.outward_normal_text), 0.7)

        # Positive and negative local contributions
        self.play_timed(GrowArrow(self.field_out), 0.8)
        self.play_timed(FadeIn(self.field_out_label), 0.4)
        self.play_timed(FadeIn(self.positive_tag), 0.4)
        self.play_timed(GrowArrow(self.field_in), 0.8)
        self.play_timed(FadeIn(self.negative_tag), 0.4)
        self.play_timed(
            AnimationGroup(
                Indicate(self.positive_tag, color=POS_RED, scale_factor=1.15),
                Indicate(self.field_out, color=GOLD, scale_factor=1.04),
                lag_ratio=0.0,
            ),
            0.9,
        )
        self.play_timed(
            AnimationGroup(
                Indicate(self.negative_tag, color=NEG_BLUE, scale_factor=1.15),
                Indicate(self.field_in, color=GOLD, scale_factor=1.04),
                lag_ratio=0.0,
            ),
            0.9,
        )

        self.hold_to_end(final=False)

    def beat_2(self):
        self.begin_beat("B02")

        # Highlight sample patches while introducing the finite sum
        sample_indices = [0, 3, 6]
        sample_rects = VGroup(*[
            SurroundingRectangle(self.patches[i], color=CYAN, buff=0.05, stroke_width=2.5)
            for i in sample_indices
        ])

        self.play_timed(Write(self.eq_sum[0]), 0.7)
        self.play_timed(Write(self.eq_sum[1]), 0.8)

        for i, rect in enumerate(sample_rects):
            target_patch = self.patches[sample_indices[i]]
            delta_label = self.deltaS_label.copy().next_to(target_patch, LEFT if i == 0 else RIGHT, buff=0.14)
            self.play_timed(FadeIn(rect), 0.35)
            self.play_timed(FadeIn(delta_label), 0.35)
            self.play_timed(
                AnimationGroup(
                    Indicate(target_patch, color=CYAN, scale_factor=1.06),
                    Indicate(self.eq_sum[2], color=FG, scale_factor=1.02),
                    Indicate(self.eq_sum[3], color=FG, scale_factor=1.02),
                    lag_ratio=0.0,
                ),
                0.8,
            )
            self.play_timed(FadeOut(delta_label), 0.25)
            self.play_timed(FadeOut(rect), 0.25)

        self.play_timed(Write(self.eq_sum[2]), 0.9)
        self.play_timed(Write(self.eq_sum[3]), 0.7)
        self.play_timed(Indicate(self.eq_sum, color=FG, scale_factor=1.02), 0.8)

        # Replace the finite sum by the closed-surface integral
        self.play_timed(TransformMatchingTex(self.eq_sum, self.eq_int), 1.8)
        self.remove(self.eq_sum)
        self.add(self.eq_int)
        self.play_timed(Indicate(self.eq_int[1], color=FG, scale_factor=1.10), 0.9)
        self.play_timed(FadeIn(self.closed_surface_note), 0.8)

        self.hold_to_end(final=False)

    def beat_3(self):
        self.begin_beat("B03")

        tracing_circle = self.sphere_outline.copy().set_stroke(color=CYAN, width=5)
        tracing_equator = self.equator.copy().set_stroke(color=CYAN, width=4).set_opacity(0.8)
        self.play_timed(
            AnimationGroup(
                ShowPassingFlash(tracing_circle, time_width=0.35),
                ShowPassingFlash(tracing_equator, time_width=0.35),
                lag_ratio=0.1,
            ),
            2.0,
        )

        self.play_timed(FadeIn(self.net_flux_label), 0.8)
        self.play_timed(Indicate(self.positive_tag, color=POS_RED, scale_factor=1.15), 0.7)
        self.play_timed(Indicate(self.negative_tag, color=NEG_BLUE, scale_factor=1.15), 0.7)
        self.play_timed(
            AnimationGroup(
                Circumscribe(self.sphere_outline_dashed, color=CYAN, fade_out=True, time_width=0.8),
                Circumscribe(self.eq_int, color=FG, fade_out=True, time_width=0.8),
                lag_ratio=0.0,
            ),
            1.5,
        )
        self.play_timed(Indicate(self.net_flux_label, color=FG, scale_factor=1.05), 0.8)

        self.hold_to_end(final=True)

    # --------------------------------------------------
    # Timing and audio helpers
    # --------------------------------------------------
    def get_wav_duration(self, path: Path) -> float:
        if not path.exists():
            return 0.0
        try:
            with contextlib.closing(wave.open(str(path), "rb")) as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                if rate > 0:
                    return frames / float(rate)
        except Exception:
            return 0.0
        return 0.0

    def begin_beat(self, beat_key: str):
        spec = self.beat_durations[beat_key]
        audio_path = spec["file"]
        if audio_path.exists():
            self.add_sound(str(audio_path))
        self.current_beat_end = self.clock + spec["total"]

    def play_timed(self, *animations, duration=None):
        if duration is None:
            *animations, duration = animations
        self.play(*animations, run_time=duration)
        self.clock += duration

    def wait_timed(self, duration: float):
        if duration > 0:
            self.wait(duration)
            self.clock += duration

    def hold_to_end(self, final: bool = False):
        remaining = max(0.0, self.current_beat_end - self.clock)
        if final:
            fade_time = min(0.5, remaining)
            static_hold = max(0.0, remaining - fade_time)
            if static_hold > 0:
                self.wait_timed(static_hold)
            if fade_time > 0:
                self.play(FadeOut(self.main_group), run_time=fade_time)
                self.clock += fade_time
        else:
            self.wait_timed(remaining)


# ==================================================
# RENDER SCENE — RUN DIRECTLY FROM PYCHARM
# ==================================================
if __name__ == "__main__":
    subprocess.run(
        [
            sys.executable,
            "-m",
            "manim",
            "-p",                  # Automatically open video
            "-qh",                 # High quality
            "-r",
            "1920,1080",
            "--fps",
            "30",
            str(Path(__file__).resolve()),
            "GaussScene03",
        ],
        check=True,
    )
