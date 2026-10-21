"""Standalone Arabic Gauss's Law teaser for The Physics Symphony.

Silent, 30-second 16:9 Manim Community trailer.
No external images, other scenes, or audio are required.

Click Run in PyCharm to render and open the video.
"""
from html import escape
from pathlib import Path
import subprocess
import sys
import numpy as np
from manim import *

BG = "#101820"
WHITEISH = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
VIOLET = "#C792EA"
POS = "#FF6B6B"


class GaussLawTrailer(Scene):
    def ar(self, words, size=30, color=WHITEISH):
        """Use contextual shaping for Arabic on Windows."""
        return MarkupText(escape(words), font="Arial", font_size=size, color=color)

    def play_s(self, *anims, seconds=1.0, **kwargs):
        self.play(*anims, run_time=seconds, **kwargs)
        self.clock += seconds

    def wait_s(self, seconds):
        if seconds > 0:
            self.wait(seconds)
            self.clock += seconds

    def until(self, target):
        remaining = target - self.clock
        if remaining < -0.05:
            raise RuntimeError(
                f"Animation exceeded the {target:.1f}-second cue by {-remaining:.2f}s"
            )
        self.wait_s(max(0, remaining))

    def clear_stage(self, *objects, seconds=0.6):
        # Explicit cleanup prevents elements from remaining in later segments.
        self.play_s(*[FadeOut(o) for o in objects], seconds=seconds)

    def construct(self):
        self.camera.background_color = BG
        self.clock = 0.0
        self.wait_s(1.0)  # deliberate silent lead-in

        # -----------------------------------------
        # 1–6s: question / introduction
        # -----------------------------------------
        halo = Circle(radius=1.38, stroke_color=CYAN, stroke_width=2.7,
                      fill_color=CYAN, fill_opacity=0.055)
        charge = MathTex("+q", color=POS, font_size=56)
        ray_arrows = VGroup()
        for degree in range(0, 360, 45):
            a = degree * DEGREES
            u = np.array([np.cos(a), np.sin(a), 0])
            ray_arrows.add(Arrow(u * 0.39, u * 1.95,
                                  buff=0, stroke_width=3.4, color=GOLD,
                                  max_tip_length_to_length_ratio=0.13))
        picture = VGroup(halo, charge, ray_arrows).move_to(UP * 0.65)
        intro = self.ar("قانون غاوس", 58).move_to(DOWN * 1.65)
        intro_sub = self.ar("كيف ترتبط الشحنة بالمجال الكهربائي؟", 29, CYAN)
        intro_sub.move_to(DOWN * 2.34)
        self.play_s(FadeIn(charge), Create(halo), seconds=1.1)
        self.play_s(LaggedStart(*[GrowArrow(a) for a in ray_arrows], lag_ratio=0.08), seconds=1.0)
        self.play_s(FadeIn(intro, shift=UP * 0.12), seconds=0.75)
        self.play_s(FadeIn(intro_sub), seconds=0.55)
        self.until(6.0)
        self.clear_stage(picture, intro, intro_sub, seconds=0.65)

        # -----------------------------------------
        # 6–13s: point charge / spherical symmetry
        # -----------------------------------------
        header = self.ar("سطح مغلق ... وتدفق كهربائي", 36)
        header.move_to(UP * 3.12)
        center = np.array([-2.65, -0.10, 0.0])
        inner_q = MathTex("+q", font_size=43, color=POS).move_to(center)
        sphere = Circle(radius=1.68, color=CYAN, stroke_width=3.0)
        sphere.move_to(center)
        normals = VGroup()
        field_arrows = VGroup()
        for deg in (0, 45, 90, 135, 180, 225, 270, 315):
            angle = deg * DEGREES
            unit = np.array([np.cos(angle), np.sin(angle), 0])
            field_arrows.add(Arrow(center + unit * 0.42, center + unit * 1.28,
                                    buff=0, stroke_width=3.2, color=GOLD,
                                    max_tip_length_to_length_ratio=0.19))
        for deg in (20, 110, 200, 290):
            angle = deg * DEGREES
            unit = np.array([np.cos(angle), np.sin(angle), 0])
            normals.add(Arrow(center + unit * 1.65, center + unit * 2.05,
                              buff=0, stroke_width=3.0, color=VIOLET,
                              max_tip_length_to_length_ratio=0.33))
        gauss_eq = MathTex(
            r"\oint_S\mathbf{E}\cdot d\mathbf{S}",
            r"=", r"\frac{Q_{\mathrm{in}}}{\epsilon_0}",
            font_size=42,
        ).move_to([2.70, 0.20, 0])
        sphere_caption = self.ar("الشحنة داخل السطح", 27, CYAN).move_to([2.70, -1.10, 0])
        self.play_s(FadeIn(header), seconds=0.6)
        self.play_s(FadeIn(inner_q), Create(sphere), seconds=1.0)
        self.play_s(LaggedStart(*[GrowArrow(a) for a in field_arrows], lag_ratio=0.09), seconds=1.0)
        self.play_s(LaggedStart(*[GrowArrow(a) for a in normals], lag_ratio=0.14), seconds=0.85)
        self.play_s(Write(gauss_eq), seconds=1.2)
        self.play_s(FadeIn(sphere_caption), seconds=0.55)
        self.until(13.0)
        self.clear_stage(header, inner_q, sphere, normals, field_arrows,
                         gauss_eq, sphere_caption, seconds=0.65)

        # -----------------------------------------
        # 13–20s: a line charge and a Gaussian cylinder
        # -----------------------------------------
        header2 = self.ar("التناظر يجعل الحساب أبسط", 36).move_to(UP * 3.12)
        cx = -2.70
        top = 1.50
        bottom = -1.50
        cyl = VGroup(
            Ellipse(width=2.48, height=0.64, stroke_color=CYAN, stroke_width=2.7,
                    fill_color=CYAN, fill_opacity=0.12).move_to([cx, top, 0]),
            Ellipse(width=2.48, height=0.64, stroke_color=CYAN, stroke_width=2.7,
                    fill_color=CYAN, fill_opacity=0.12).move_to([cx, bottom, 0]),
            Line([cx-1.24, top, 0], [cx-1.24, bottom, 0], color=CYAN, stroke_width=2.7),
            Line([cx+1.24, top, 0], [cx+1.24, bottom, 0], color=CYAN, stroke_width=2.7),
        )
        center_line = DashedLine([cx, -1.95, 0], [cx, 1.95, 0],
                                  dash_length=0.14, color=POS, stroke_width=4)
        pluses = VGroup(*[
            MathTex("+", color=POS, font_size=32).move_to([cx, y, 0])
            for y in (-1.15, -0.36, 0.43, 1.22)
        ])
        side_arrows = VGroup()
        for y in (-1.10, -0.15, 0.80):
            for direction in (-1, 1):
                side_arrows.add(Arrow([cx+direction*1.34, y, 0],
                                       [cx+direction*2.03, y, 0],
                                       buff=0, stroke_width=3.6, color=GOLD,
                                       max_tip_length_to_length_ratio=0.22))
        eq_line = MathTex(
            r"\mathbf{E}=\frac{\rho_l}{2\pi\epsilon_0r}\hat{\mathbf{u}}_r",
            font_size=43,
        ).move_to([2.65, 0.36, 0])
        line_caption = self.ar("خط شحنة لا نهائي", 29, CYAN).move_to([2.65, -0.85, 0])
        self.play_s(FadeIn(header2), seconds=0.55)
        self.play_s(Create(cyl), Create(center_line), seconds=1.1)
        self.play_s(FadeIn(pluses), seconds=0.5)
        self.play_s(LaggedStart(*[GrowArrow(a) for a in side_arrows], lag_ratio=0.12), seconds=1.2)
        self.play_s(Write(eq_line), seconds=1.35)
        self.play_s(FadeIn(line_caption), seconds=0.55)
        self.until(20.0)
        self.clear_stage(header2, cyl, center_line, pluses, side_arrows,
                         eq_line, line_caption, seconds=0.65)

        # -----------------------------------------
        # 20–30s: final invitation to the channel
        # -----------------------------------------
        upper_rule = Line(LEFT * 4.65, RIGHT * 4.65, color=CYAN, stroke_width=1.8)
        upper_rule.move_to(UP * 2.30)
        lower_rule = Line(LEFT * 4.65, RIGHT * 4.65, color=CYAN, stroke_width=1.8)
        lower_rule.move_to(DOWN * 2.48)
        invitation = self.ar("للمزيد من الشرح", 31)
        invitation.move_to(UP * 1.30)
        visit = self.ar("زوروا القناة", 37, CYAN).move_to(UP * 0.40)
        channel = Text("The Physics Symphony", font_size=56,
                       color=GOLD, weight=BOLD).move_to(DOWN * 0.75)
        url = Text("youtube.com/@PhysicsSymphony_R", font_size=25,
                   color=WHITEISH).move_to(DOWN * 1.68)
        if channel.width > 11.8:
            channel.scale_to_fit_width(11.8)
        if invitation.width > 11.8:
            invitation.scale_to_fit_width(11.8)
        self.play_s(Create(upper_rule), Create(lower_rule), seconds=0.7)
        self.play_s(FadeIn(invitation, shift=UP * 0.12), seconds=1.0)
        self.play_s(FadeIn(visit), seconds=0.7)
        self.play_s(AddTextLetterByLetter(channel, time_per_char=0.065), seconds=2.4)
        self.play_s(FadeIn(url), seconds=0.65)
        # Keep the invitation legible for a substantial final hold.
        self.until(29.5)
        self.play_s(FadeOut(Group(*list(self.mobjects))), seconds=0.5)
        assert abs(self.clock - 30.0) < 0.04, self.clock


if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "manim", "-p", "-qh", "-r", "1920,1080",
        "--fps", "30", str(Path(__file__).resolve()), "GaussLawTrailer",
    ], check=True)
