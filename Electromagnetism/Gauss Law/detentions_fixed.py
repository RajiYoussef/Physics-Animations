"""DETENTIONS — symbol-introduction interlude after GaussScene01.

This intentionally DOES NOT explain E dot dS. It introduces each vector separately.
Optional narration in the same directory: detentions_ar.wav, OR
  detentions_B01_ar.wav + detentions_B02_ar.wav + detentions_B03_ar.wav.
Silent duration: 91 seconds (1 s setup + 26 + 34 + 30 s).
Recommended: eight detentions_N01_ar.wav ... detentions_N08_ar.wav clips.
These synchronize each definition separately and extend holds automatically.
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

BG = '#101820'
FG = '#F5F5F5'
CYAN = '#58C4DD'
GOLD = '#F6C85F'
VIOLET = '#C792EA'
RED = '#FF6B6B'
BLUE = '#64B5F6'
FONT = 'Arial'
# Cue keys are (zero-based beat, seconds within the planned beat).
NARRATION_CUES = {(0, 0.0): 1, (0, 6.0): 2, (0, 14.0): 3,
                  (1, 1.0): 4, (1, 20.0): 5,
                  (2, 1.0): 6, (2, 10.0): 7, (2, 18.0): 8}
# Do not erase a definition while its narration is still playing.
AUDIO_GUARDS = set(NARRATION_CUES) | {(1, 19.0), (1, 29.5)}
FADE_AT_END = True


def sound_duration(path):
    try:
        with contextlib.closing(wave.open(str(path), 'rb')) as w:
            return w.getnframes() / w.getframerate()
    except (OSError, wave.Error, ZeroDivisionError, EOFError) as exc:
        raise ValueError(f'Cannot read narration WAV: {path}') from exc


class Detentions(Scene):
    def arabic(self, s, size=29, color=FG):
        return MarkupText(escape(s), font=FONT, font_size=size, color=color)

    def run_anim(self, anim, secs):
        self.play(anim, run_time=secs)
        self.clock += secs

    def rest(self, secs):
        if secs > 0:
            self.wait(secs)
            self.clock += secs

    def cue(self, local_seconds, beat_start):
        """Wait until a narration cue measured from the start of this beat."""
        key = (self.beat_index, local_seconds)
        target = beat_start + local_seconds + self.cue_shift
        if self.audio_mode == 'segments' and key in AUDIO_GUARDS:
            delay = max(0.0, self.speech_end + .45 - target)
            self.cue_shift += delay
            self.end_beat_at += delay
            self.beat_lengths[self.beat_index] += delay
            target += delay
        if self.clock > target + 0.04:
            raise RuntimeError(f'Cue missed by {self.clock-target:.2f}s')
        self.rest(max(0.0, target - self.clock))
        if self.audio_mode == 'segments' and key in NARRATION_CUES:
            path = self.segments[NARRATION_CUES[key]-1]
            self.add_sound(str(path))
            self.speech_end = self.clock + sound_duration(path)

    def open_beat(self, n):
        self.beat_index = n
        self.cue_shift = 0.0
        self.speech_end = self.clock - .45
        self.beat_start_at = self.clock
        self.end_beat_at = self.clock + self.beat_lengths[n]
        if self.audio_mode == 'clips':
            self.add_sound(str(self.clips[n]))
        self.cue(0.0, self.beat_start_at)

    def close_beat(self, last=False):
        if self.audio_mode == 'segments':
            extra = max(0.0, self.speech_end + (2.0 if last else 1.0) - self.end_beat_at)
            self.end_beat_at += extra
            self.beat_lengths[self.beat_index] += extra
        left = self.end_beat_at - self.clock
        if left < -0.06:
            raise RuntimeError(f'Beat ran {abs(left):.2f}s too long')
        if last and FADE_AT_END and left >= 0.5:
            self.rest(left - 0.5)
            self.run_anim(FadeOut(Group(*list(self.mobjects))), 0.5)
        else:
            self.rest(max(0, left))

    def show_definition(self, symbol, description, secs=1.1):
        """Replace the previous definition; NEVER stack labels on top of it."""
        symbol.move_to([3.1, 1.16, 0])
        description.move_to([3.1, .10, 0])
        if symbol.width > 5.0:
            symbol.scale_to_fit_width(5.0)
        if symbol.height > 1.10:
            symbol.scale_to_fit_height(1.10)
        if description.width > 5.0:
            description.scale_to_fit_width(5.0)
        if self.active_definition is not None:
            self.run_anim(FadeOut(self.active_definition), .4)
        self.active_definition = VGroup(symbol, description)
        self.run_anim(FadeIn(self.active_definition, shift=UP * .13), secs)

    def construct(self):
        self.camera.background_color = BG
        self.clock = 0.0
        root = Path(__file__).resolve().parent
        self.clips = [root / f'detentions_B0{i}_ar.wav' for i in (1, 2, 3)]
        whole = root / 'detentions_ar.wav'
        # Planned beat windows include reading and transition pauses.
        self.beat_lengths = [26.0, 34.0, 30.0]
        self.audio_mode = 'silent'
        self.segments = [root / f'detentions_N{i:02d}_ar.wav' for i in range(1, 9)]
        if any(p.exists() for p in self.segments):
            if not all(p.exists() for p in self.segments):
                raise ValueError('Provide all eight detentions_N01_ar.wav through N08 clips.')
            for path in self.segments:
                if sound_duration(path) <= 0:
                    raise ValueError(f'Empty narration: {path}')
            self.audio_mode = 'segments'
        elif whole.exists():
            self.audio_mode = 'whole'
            # Starts at t=1s. Extend last hold to prevent truncation.
            self.beat_lengths[2] += max(0.0, sound_duration(whole) + 2.0 - 90.0)
        elif all(p.exists() for p in self.clips):
            self.audio_mode = 'clips'
            # Preserve a 3/3/4-second reading hold after each recording.
            self.beat_lengths = [max(n, sound_duration(p) + h)
                                 for n, p, h in zip(self.beat_lengths, self.clips, (3, 3, 4))]
        if self.audio_mode in ('whole', 'clips'):
            print('Legacy audio: internal sentence cues must match the narration timing sheet. Use N01-N08 for automatic per-definition timing.')
        print(f'Detentions: audio={self.audio_mode}, duration={1 + sum(self.beat_lengths):.2f}s')

        self.title = self.arabic('كيف نقرأ رموز قانون غاوس؟', 39)
        self.title.move_to([0, 3.20, 0])

        # Simple 2D SECTION of a closed 3D Gaussian surface, not a loop-integral.
        c = np.array([-3.45, -.15, 0])
        radius = 1.46
        sphere = Circle(radius=radius, stroke_color=CYAN, stroke_width=4,
                        fill_color=CYAN, fill_opacity=.075).move_to(c)
        dashed_equator = DashedVMobject(Ellipse(width=2.75, height=.60, color=CYAN,
                                                stroke_width=1.4).move_to(c), num_dashes=25)
        source = Dot(c, color=RED, radius=.105)
        source_sign = MathTex('+', font_size=28, color=FG).move_to(c)
        q_label = MathTex(r'Q_{\mathrm{in}}', font_size=35, color=RED).move_to(c + DOWN * .55)
        surf_name = MathTex('S', color=CYAN, font_size=38).move_to(c + LEFT * 1.89 + UP * .6)
        section_note = self.arabic('مقطع تخطيطي لسطح مغلق', 22).move_to([-3.40, -2.17, 0])

        theta = 38 * DEGREES
        u = np.array([np.cos(theta), np.sin(theta), 0])
        rim = c + radius * u
        patch = Arc(radius=radius, start_angle=theta - 11*DEGREES,
                    angle=22*DEGREES, arc_center=c,
                    stroke_color=VIOLET, stroke_width=11)
        surface_normal = Arrow(rim, rim + .87*u, buff=0, color=VIOLET,
                               stroke_width=5, max_tip_length_to_length_ratio=.22)
        ds_symbol = MathTex(r'd\mathbf S', color=VIOLET, font_size=34).move_to(rim + .69*u + UP*.30)
        # Distinct electric field vector at the highlighted surface patch.  No angle,
        # projection or dot-product explanation is supplied in this interlude.
        electric_field = Arrow(rim, rim + .94*u,
                               buff=0, color=GOLD, stroke_width=5,
                               max_tip_length_to_length_ratio=.22)
        e_symbol = MathTex(r'\mathbf E', color=GOLD, font_size=34).move_to([-1.86, 1.67, 0])

        # Dedicated right-hand definition zone; one definition is visible at a time.
        divider = Line([-0.45, 2.60, 0], [-0.45, -2.45, 0], color='#45616B', stroke_width=1.5)
        right_heading = self.arabic('الرمز ومعناه', 26, CYAN).move_to([3.1, 2.28, 0])
        base_line = Line([.45,-.77,0], [5.72,-.77,0], color='#45616B', stroke_width=1.5)
        law = MathTex(r'\oint_S\mathbf E\cdot d\mathbf S=\frac{Q_{\mathrm{in}}}{\epsilon_0}',
                      font_size=38, color=FG)
        law.move_to([3.14, -1.56, 0])
        law_box = SurroundingRectangle(law, color=CYAN, buff=.20, corner_radius=.10, stroke_width=1.7)
        self.active_definition = None

        # Initial silent second.
        self.run_anim(FadeIn(self.title), .75)
        self.rest(.25)
        if self.audio_mode == 'whole':
            self.add_sound(str(whole))

        # Cue times (in seconds FROM EACH BEAT START).
        # Adjust these numbers after listening to your finished recordings.
        # B01 narration: intro -> S -> Q_in.
        self.open_beat(0)
        b = self.beat_start_at
        self.run_anim(Create(divider), .5)
        self.run_anim(FadeIn(right_heading), .5)
        self.cue(3.2, b)
        self.run_anim(Create(sphere), 1.2)
        self.run_anim(FadeIn(dashed_equator, section_note, surf_name), .8)
        self.cue(6.0, b)
        self.show_definition(MathTex('S', color=CYAN, font_size=72),
                             self.arabic('سطح غاوسي مغلق', 32), .8)
        self.cue(14.0, b)
        self.run_anim(FadeIn(source, source_sign), .6)
        self.run_anim(FadeIn(q_label), .5)
        self.cue(15.5, b)
        self.show_definition(MathTex(r'Q_{\mathrm{in}}', color=RED, font_size=62),
                             self.arabic('الشحنة الصافية داخل السطح', 31), .8)
        self.cue(22.0, b)
        self.run_anim(Indicate(source, color=RED), .8)
        self.close_beat()

        # B02 narration: surface patch / dS first; E much later.
        # Clear all dS geometry AND its definition before introducing E.
        self.open_beat(1)
        b = self.beat_start_at
        self.cue(1.0, b)
        self.run_anim(Create(patch), .6)
        self.cue(3.0, b)
        self.run_anim(GrowArrow(surface_normal), .9)
        self.run_anim(FadeIn(ds_symbol), .4)
        self.cue(4.5, b)
        self.show_definition(MathTex(r'd\mathbf S', color=VIOLET, font_size=65),
                             self.arabic('متجه عنصر المساحة\nمقداره مساحة العنصر واتجاهه عمودي إلى الخارج', 25), .9)
        self.cue(19.0, b)
        self.run_anim(FadeOut(VGroup(patch, surface_normal, ds_symbol,
                                     self.active_definition)), .65)
        self.active_definition = None
        self.cue(20.0, b)
        self.run_anim(GrowArrow(electric_field), .85)
        self.run_anim(FadeIn(e_symbol), .35)
        self.cue(21.5, b)
        self.show_definition(MathTex(r'\mathbf E', color=GOLD, font_size=70),
                             self.arabic('متجه المجال الكهربائي عند النقطة', 28), .9)
        self.cue(29.5, b)
        self.run_anim(FadeOut(VGroup(electric_field, e_symbol,
                                     self.active_definition)), .65)
        self.active_definition = None
        self.close_beat()

        # B03 narration: closed integral -> epsilon_0 -> final equation.
        self.open_beat(2)
        b = self.beat_start_at
        self.cue(1.0, b)
        self.show_definition(MathTex(r'\oint_S', color=CYAN, font_size=70),
                             self.arabic('تكامل على السطح المغلق كله', 30), .9)
        self.cue(4.6, b)
        self.run_anim(Indicate(sphere, color=CYAN, scale_factor=1.015), 1.1)
        self.cue(10.0, b)
        self.show_definition(MathTex(r'\epsilon_0', color=FG, font_size=72),
                             self.arabic('سماحية الفراغ', 34), .9)
        self.cue(18.0, b)
        self.run_anim(Create(base_line), .45)
        self.run_anim(Write(law), 1.5)
        self.run_anim(Create(law_box), .65)
        self.cue(25.0, b)
        self.show_definition(self.arabic('والآن... تأمل الرموز معًا', 34, GOLD),
                             self.arabic('سنستخدم هذه المعادلة في المشاهد التالية', 25), .9)
        # E dot dS is NEVER explained or separately highlighted.
        self.close_beat(last=True)
        assert abs(self.clock - (1 + sum(self.beat_lengths))) <= 1/30 + .01


if __name__ == '__main__':
    subprocess.run([
        sys.executable, '-m', 'manim', '-p', '-qh', '-r', '1920,1080',
        '--fps', '30', str(Path(__file__).resolve()), 'Detentions',
    ], check=True)

