"""GaussScene11 — uniformly charged solid sphere: external field.

Run this file using PyCharm's Run button. Optional audio beside the script:
  S11_ar.wav (complete narration), OR S11_B01_ar.wav ... S11_B03_ar.wav.
All Arabic prose uses MarkupText (Pango shaping). All algebra uses MathTex.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import contextlib
import wave
import subprocess
import sys
import numpy as np
from manim import *

BG = '#101820'
FG = '#F5F5F5'
CYAN = '#58C4DD'
GOLD = '#F6C85F'
RED = '#FF6B6B'
VIOLET = '#C792EA'
ARABIC_FONT = 'Arial'
FADE_OUT = True


def wav_duration(path):
    if not path.is_file():
        return 0.0
    try:
        with contextlib.closing(wave.open(str(path), 'rb')) as f:
            return f.getnframes() / f.getframerate()
    except (OSError, wave.Error, ZeroDivisionError):
        return 0.0


class GaussScene11(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0
        folder = Path(__file__).resolve().parent
        beats = [folder / f'S11_B0{i}_ar.wav' for i in (1, 2, 3)]
        whole = folder / 'S11_ar.wav'
        self.mode = 'silent'
        self.lengths = [19., 17., 22.]
        if whole.is_file():
            self.mode = 'whole'
            # Complete narration begins at second 1; don't cut the tail.
            self.lengths[-1] += max(0., wav_duration(whole) + 1.0 + 4.0 - 59.0)
        elif all(p.is_file() for p in beats):
            self.mode = 'beats'
            self.lengths = [max(s, wav_duration(p)) + h for (s, h), p in zip(((16,3),(14,3),(18,4)), beats)]
        self.beat_files = beats
        self.make_objects()
        self.run(FadeIn(self.title), 0.8)
        self.hold(0.2)
        if self.mode == 'whole':
            self.add_sound(str(whole))
        self.beat_1()
        self.beat_2()
        self.beat_3()
        expected = 1 + sum(self.lengths)
        assert abs(self.t - expected) < .07, (self.t, expected)
        print(f'S11 video duration: {expected:.2f} s; audio mode: {self.mode}')

    def ar(self, message, size=28, color=FG):
        return MarkupText(escape(message), font=ARABIC_FONT, font_size=size, color=color)

    def fit(self, mob, max_width):
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        return mob

    def run(self, animation, duration):
        self.play(animation, run_time=duration)
        self.t += duration

    def hold(self, seconds):
        if seconds > 1e-6:
            self.wait(seconds)
            self.t += seconds

    def start_beat(self, idx):
        if self.mode == 'beats':
            self.add_sound(str(self.beat_files[idx]))
        self.end_time = self.t + self.lengths[idx]

    def end_beat(self, final=False):
        remaining = self.end_time - self.t
        if remaining < -.05:
            raise RuntimeError(f'S11 beat exceeded time allowance by {-remaining:.2f} seconds')
        if final and FADE_OUT and remaining >= .5:
            self.hold(remaining-.5)
            self.run(FadeOut(Group(*list(self.mobjects))), .5)
        else:
            self.hold(max(0, remaining))

    def make_objects(self):
        # Safe frame: 14.22 x 8.0; main content above y=-2.8.
        self.title = self.fit(self.ar('كرة صلبة مشحونة بانتظام: المجال خارجها', 38), 11.8)
        self.title.move_to([0, 3.30, 0])
        self.c = np.array([-3.55, .20, 0.])
        a, r = 1.25, 1.92
        self.disk = Circle(a, color=CYAN, stroke_width=2.8, fill_color=CYAN, fill_opacity=.23).move_to(self.c)
        self.equator = Ellipse(width=2.2, height=.43, color=CYAN, stroke_width=1.5).move_to(self.c).set_opacity(.55)
        self.outer = DashedVMobject(Circle(r, color=CYAN, stroke_width=2.8).move_to(self.c), num_dashes=38)
        positions = [(-.48,.52),(.34,.62),(-.65,-.18),(.55,-.36),(.10,-.52)]
        self.plus = VGroup(*[MathTex('+', color=RED, font_size=24).move_to(self.c + [dx,dy,0]) for dx,dy in positions])
        self.total_q = MathTex('Q', color=RED, font_size=32).move_to(self.c + [.05,.07,0])
        self.a_line = Line(self.c, self.c + [a,0,0], color=FG, stroke_width=2.5)
        self.a_text = MathTex('a',color=FG,font_size=30).move_to(self.c + [.64,.24,0])
        angle = 35 * DEGREES
        self.r_line = Line(self.c, self.c + r*np.array([np.cos(angle),np.sin(angle),0]), color=FG, stroke_width=2.5)
        self.r_text = MathTex('r',color=FG,font_size=30).move_to(self.c + [1.39,.85,0])
        self.arrows = VGroup()
        for deg in (15,65,110,165,205,250,300,340):
            u = np.array([np.cos(deg*DEGREES), np.sin(deg*DEGREES), 0])
            p = self.c + r*u
            self.arrows.add(Arrow(p,p+.37*u,buff=0,color=GOLD,stroke_width=3.5,max_tip_length_to_length_ratio=.24))

        # ONE active label at a time, always in the same bounded strip.
        self.caption_pos = np.array([-3.55,-2.34,0])
        self.caption = None
        self.captions = [
            'مقطع في كرة صلبة مشحونة',
            'نصف قطر توزيع الشحنة الثابت',
            'كثافة شحنة حجمية منتظمة',
            'منطقة خارجية خالية من الشحنة',
            'نصف قطر سطح غاوس',
            'الشحنة كلها محصورة',
            'مقارنة بشحنة نقطية',
        ]

        # Equations occupy two fixed, nonoverlapping slots on the right.
        self.top_slot = np.array([3.55, .90, 0])
        self.bottom_slot = np.array([3.55,-.65,0])
        self.eq_top = None
        self.eq_bottom = None
        self.equations = [
            r'\rho_v=\frac{Q}{(4/3)\pi a^3}\quad(r<a)',
            r'\rho_v=0\quad(r>a)',
            r'Q_{\mathrm{in}}=Q\quad(r>a)',
            r'E_r(r)4\pi r^2=\frac{Q}{\epsilon_0}',
            r'\mathbf E=\frac{Q}{4\pi\epsilon_0 r^2}\hat{\mathbf r}\quad(r>a)',
        ]
        self.eq_width = 5.75
        # A comparison icon to the left of the final equation is intentionally
        # omitted: the original overlay in this region was unreadable.

    def set_caption(self, text, duration=.55):
        new = self.fit(self.ar(text, 25), 5.9)
        new.move_to(self.caption_pos)
        if self.caption is None:
            self.run(FadeIn(new), duration)
        else:
            self.run(FadeOut(self.caption), duration/2)
            self.run(FadeIn(new), duration/2)
        self.caption = new

    def show_eq(self, tex, slot, duration=1.2):
        obj = MathTex(tex, color=FG, font_size=36)
        self.fit(obj,self.eq_width)
        obj.move_to(self.top_slot if slot=='top' else self.bottom_slot)
        prior = self.eq_top if slot=='top' else self.eq_bottom
        if prior is not None:
            self.run(FadeOut(prior), .35)
        self.run(Write(obj), duration)
        if slot=='top': self.eq_top=obj
        else: self.eq_bottom=obj
        return obj

    def beat_1(self):
        self.start_beat(0)
        self.run(FadeIn(self.disk),.8)
        self.run(FadeIn(self.equator),.3)
        self.run(FadeIn(self.plus),.6)
        self.run(FadeIn(self.total_q),.4)
        self.set_caption(self.captions[0])
        self.run(Create(self.a_line),.5)
        self.run(FadeIn(self.a_text),.3)
        self.set_caption(self.captions[1])
        first=self.show_eq(self.equations[0],'top',1.3)
        self.set_caption(self.captions[2])
        self.run(Indicate(first,color=FG,scale_factor=1.03),.8)
        second=self.show_eq(self.equations[1],'bottom',1.1)
        self.set_caption(self.captions[3])
        self.run(Indicate(second,color=CYAN,scale_factor=1.03),.8)
        self.end_beat()

    def beat_2(self):
        self.start_beat(1)
        self.run(Create(self.outer),1.0)
        self.run(Create(self.r_line),.5)
        self.run(FadeIn(self.r_text),.3)
        self.set_caption(self.captions[4])
        self.run(LaggedStart(*[GrowArrow(a) for a in self.arrows],lag_ratio=.10),1.6)
        qin=self.show_eq(self.equations[2],'bottom',1.15)
        self.set_caption(self.captions[5])
        self.run(Circumscribe(self.disk,color=CYAN),1.0)
        self.run(Indicate(qin,color=FG,scale_factor=1.03),.8)
        self.end_beat()

    def beat_3(self):
        self.start_beat(2)
        flux=self.show_eq(self.equations[3],'top',1.35)
        self.run(Indicate(flux,color=GOLD,scale_factor=1.03),.85)
        result=self.show_eq(self.equations[4],'bottom',1.6)
        self.set_caption(self.captions[6])
        # Compare physically: a point Q at the same centre, without replacing
        # the volume charge distribution or obscuring the final equation.
        comparison=Dot(self.c,radius=.075,color=RED)
        self.run(FadeIn(comparison),.35)
        self.run(Indicate(result,color=FG,scale_factor=1.03),1.0)
        self.run(FadeOut(comparison),.3)
        self.end_beat(final=True)


# ===============================================================
# RENDER — CLICK RUN IN PYCHARM; OPEN VIDEO AUTOMATICALLY
# ===============================================================
if __name__ == '__main__':
    subprocess.run([
        sys.executable, '-m', 'manim', '-p', '-qh',
        '-r', '1920,1080', '--fps', '30',
        str(Path(__file__).resolve()), 'GaussScene11',
    ], check=True)
