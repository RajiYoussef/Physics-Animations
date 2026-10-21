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
        # All main content is above y=-2.72; lower caption band stays free.
        self.title = self.fit(self.ar('كرة صلبة مشحونة بانتظام: المجال خارجها', 37), 11.7)
        self.title.move_to([0, 3.30, 0])
        self.c = np.array([-3.65, .12, 0.])
        self.a = 1.32
        self.r_out = 1.96
        self.disk = Circle(radius=self.a, color=CYAN, stroke_width=3,
                           fill_color=CYAN, fill_opacity=.26).move_to(self.c)
        pts = [(-.55,.54),(.38,.60),(-.70,-.15),(.52,-.35),(.02,-.60),(-.22,.03)]
        self.charges = VGroup(*[MathTex('+',color=RED,font_size=27).move_to(self.c+[x,y,0])
                                for x,y in pts])
        self.radius_a = Line(self.c,self.c+RIGHT*self.a,color=FG,stroke_width=2)
        self.a_text = MathTex('a',color=FG,font_size=30).move_to(self.c+[.72,.22,0])
        self.gaussian = DashedVMobject(Circle(radius=.79,color=CYAN,stroke_width=3).move_to(self.c),
                                       num_dashes=36)
        self.gauss_label = self.fit(self.ar('سطح غاوس',24,color=CYAN),2.4)
        self.gauss_label.move_to([-3.65,2.52,0])
        self.radius_r = Line(self.c,self.c+RIGHT*.79,color=VIOLET,stroke_width=2.5)
        self.r_text = MathTex('r',color=VIOLET,font_size=30).move_to(self.c+[.45,-.24,0])
        self.field_arrows = VGroup()
        for degree in (0,45,90,135,180,225,270,315):
            direction=np.array([np.cos(degree*DEGREES),np.sin(degree*DEGREES),0])
            start=self.c+self.r_out*direction
            self.field_arrows.add(Arrow(start,start+.28*direction,buff=0,
                    color=GOLD,stroke_width=3.1,max_tip_length_to_length_ratio=.34))
        self.label_slot = [-3.65,-2.38,0]
        self.label = None

        # Dedicated math area, no permanent pile-up of equations.
        self.math_center=np.array([3.36,.10,0])
        self.math_width=5.80
        self.math_current=None
        self.headline_center=np.array([3.37,2.03,0])
        self.headline=None
        self.boundary_label=self.fit(self.ar('عند الحد الفاصل',23),4.7)
        self.boundary_label.move_to(self.headline_center)

        # Two fixed, spatially separated tags. They appear only in the outside case.
        # These labels are positioned ABOVE the reserved subtitle area.
        self.core_tag = self.fit(self.ar('هنا توجد الشحنات', 23, RED), 2.8)
        self.core_tag.move_to([-5.0, 2.42, 0])
        self.empty_tag = self.fit(self.ar('هنا لا توجد شحنات', 23, GOLD), 3.1)
        self.empty_tag.move_to([-1.62, 1.90, 0])
        self.source_ring = Circle(radius=self.a, stroke_color=RED, stroke_width=5,
                                  fill_opacity=0).move_to(self.c)
        # Field arrows are anchored outside the material, i.e. in rho_v=0 space.
        # Their presence makes the difference between charge and field visible.
        self.outside_arrow = Arrow(self.c + RIGHT * (self.a + .14),
                                   self.c + RIGHT * (self.r_out + .46),
                                   buff=0, color=GOLD, stroke_width=6,
                                   max_tip_length_to_length_ratio=.22)

    def caption(self, words, duration=.5, color=FG):
        new=self.fit(self.ar(words,25,color),5.9)
        new.move_to(self.label_slot)
        if self.label is not None:
            self.run(FadeOut(self.label),duration*.5)
            self.run(FadeIn(new),duration*.5)
        else:
            self.run(FadeIn(new),duration)
        self.label=new

    def heading(self, words, duration=.45):
        new=self.fit(self.ar(words,25),5.7)
        new.move_to(self.headline_center)
        if self.headline is not None:
            self.run(FadeOut(self.headline),duration*.5)
            self.run(FadeIn(new),duration*.5)
        else:
            self.run(FadeIn(new),duration)
        self.headline=new

    def formula(self, tex, duration=1.0, size=37):
        new=MathTex(tex,color=FG,font_size=size)
        self.fit(new,self.math_width)
        new.move_to(self.math_center)
        if self.math_current is not None:
            self.run(FadeOut(self.math_current),.28)
        self.run(Write(new),duration)
        self.math_current=new
        return new

    def gaussian_radius(self, radius, duration=1.3):
        # A single concentric dashed Gaussian circle changes radius; charge disk stays fixed.
        new=DashedVMobject(Circle(radius=radius,color=CYAN,stroke_width=3).move_to(self.c),
                             num_dashes=36)
        new_line=Line(self.c,self.c+RIGHT*radius,color=VIOLET,stroke_width=2.5)
        new_r=MathTex('r',color=VIOLET,font_size=30).move_to(self.c+[radius*.61,-.24,0])
        self.run(AnimationGroup(Transform(self.gaussian,new),
                                Transform(self.radius_r,new_line),
                                Transform(self.r_text,new_r),lag_ratio=0),duration)

    def disk_partition(self, radius):
        """Charge actually enclosed: disk clipped at min(r,a), never the outer empty annulus."""
        return Circle(radius=min(radius,self.a),stroke_width=0,
                      fill_color=RED,fill_opacity=.16).move_to(self.c)

    def empty_annulus(self):
        """Ring a<distance<r: geometric area exists, but carries no charge."""
        return Annulus(inner_radius=self.a,outer_radius=self.r_out,
                       fill_color=GOLD,fill_opacity=.105,
                       stroke_width=0).move_to(self.c)

    def proof(self, first, second, duration1=1.2, duration2=1.3, fontsize=32):
        """Two explicit connected equations replacing one another in same reserved area."""
        self.formula(first,duration1,fontsize)
        self.formula(second,duration2,fontsize)

    def beat_1(self):
        # 00:01–00:20. Define source, then distinguish ρ=0 from E=0.
        self.start_beat(0)
        self.run(FadeIn(self.disk), .75)
        self.run(FadeIn(self.charges), .6)
        self.caption('الشحنة تملأ حجم الكرة، وليست على سطحها', .75)
        self.run(Create(self.radius_a), .5)
        self.run(FadeIn(self.a_text), .35)
        self.heading('a: نصف قطر الكرة المشحونة الثابت', .65)
        self.formula(r'\rho_v=\frac{Q}{(4/3)\pi a^3}\quad(r<a)', 1.4, 36)
        self.caption('الكثافة داخل الكرة ثابتة', .55)
        self.run(Indicate(self.charges,color=RED,scale_factor=1.12),.75)
        self.formula(r'\rho_v=0\quad(r>a)',1.1,41)
        self.heading('خارج الكرة: لا توجد شحنة محلية', .6)
        self.caption('صفر كثافة الشحنة لا يعني صفر المجال', .75, GOLD)
        self.end_beat()

    def beat_2(self):
        # 00:20–00:37. Make the distinction between radii *physically visible*.
        # A red overlay marks precisely the part of the charge the Gaussian surface contains.
        self.start_beat(1)
        self.run(FadeIn(self.gaussian), .5)
        self.run(Create(self.radius_r), .25)
        self.run(FadeIn(self.r_text), .2)
        self.run(FadeIn(self.gauss_label), .35)
        self.heading('r<a: سطح غاوس داخل المادة المشحونة', .45)
        self.caption('الجزء داخل سطح غاوس فقط هو المحصور', .55)
        self.enclosed=self.disk_partition(.79)
        self.run(FadeIn(self.enclosed), .4)
        self.proof(r'Q_{\mathrm{in}}=\rho_v\frac{4}{3}\pi r^3',
                   r'Q_{\mathrm{in}}=Q\frac{r^3}{a^3}\quad(r<a)',.8,.85,35)
        self.gaussian_radius(self.a, .85)
        self.run(Transform(self.enclosed,self.disk_partition(self.a)), .5)
        self.heading('r=a: سطح غاوس يضم الشحنة كلها', .45)
        self.caption('عند الحد: الشحنة المحصورة تساوي Q', .4)
        self.formula(r'Q_{\mathrm{in}}(a)=Q\frac{a^3}{a^3}=Q', .95, 34)
        # r>a: expand ONLY the imaginary Gaussian surface, never the charge disk.
        self.gaussian_radius(self.r_out,.85)
        self.empty_region=self.empty_annulus()
        self.run(FadeIn(self.empty_region), .55)
        self.run(Create(self.source_ring), .45)
        self.run(FadeIn(self.core_tag), .40)
        self.run(FadeIn(self.empty_tag), .40)
        self.heading('r>a: ازداد الحجم، لا الشحنة', .45)
        self.caption('الأحمر مشحون، والحلقة الذهبية فارغة', .45, GOLD)
        # The visible + signs stay the same while the outer boundary is larger.
        self.run(Indicate(self.charges, color=RED, scale_factor=1.07), .55)
        self.formula(r'Q_{\mathrm{in}}=Q+0=Q\quad(r>a)', .85, 34)
        self.end_beat()

    def beat_3(self):
        # 00:37–00:59. Explicitly integrate both regions, then show the field at and beyond the boundary.
        self.start_beat(2)
        # Explicit partition: charged core + empty outer shell.
        self.heading('الشحنة داخل a فقط؛ والمنطقة من a إلى r فارغة', .55)
        self.run(Indicate(self.source_ring, color=RED, scale_factor=1.03), .55)
        self.formula(r'Q_{\mathrm{in}}=\underbrace{\rho_v\frac43\pi a^3}_{Q}+\underbrace{0}_{\text{for }a<r}', 1.2, 33)
        self.caption('السطح الأكبر يضيف حجمًا فارغًا، لا شحنة إضافية', .55, GOLD)
        self.formula(r'Q_{\mathrm{in}}=Q+0=Q\quad(r>a)', 0.95, 37)

        # Zero density outside does not imply zero field there.
        self.heading('خارج المادة: ρ_v=0 لكن المجال يمتد إلى الخارج', .55)
        self.run(GrowArrow(self.outside_arrow), .55)
        self.run(LaggedStart(*[GrowArrow(arrow) for arrow in self.field_arrows], lag_ratio=.05), 0.95)
        self.formula(r'\rho_v=0\quad\not\Rightarrow\quad\mathbf E=0', 0.9, 36)
        self.caption('لا توجد شحنات في الحلقة الخارجية، لكن الأسهم الذهبية ما زالت موجودة', .55, GOLD)

        # Boundary r=a: the enclosed charge has already reached Q, and the field is continuous.
        self.gaussian_radius(self.a, 0.55)
        self.heading('عند r=a: السطح يلامس حد الشحنة', .45)
        self.formula(r'E_{\mathrm{inside}}(a)=\frac{Qa}{4\pi\epsilon_0 a^3}=\frac{Q}{4\pi\epsilon_0 a^2}', 0.95, 30)
        self.formula(r'E_{\mathrm{outside}}(a)=\frac{Q}{4\pi\epsilon_0 a^2}', 0.8, 31)
        self.caption('القيمتان متساويتان عند الحد؛ المجال متصل عند r=a', .5)

        # Expand back to the external Gaussian sphere and finish the outside derivation.
        self.gaussian_radius(self.r_out, 0.45)
        self.formula(r'E_r(r)4\pi r^2=\frac{Q}{\epsilon_0}', 0.85, 36)
        self.heading('خارج الكرة: نحسب المجال على سطح غاوس الخارجي', .5)
        self.formula(r'\mathbf E=\frac{Q}{4\pi\epsilon_0 r^2}\hat{\mathbf r}\quad(r>a)', 1.0, 33)
        self.formula(r'\mathbf E(r)=\begin{cases}'
                     r'\dfrac{Qr}{4\pi\epsilon_0 a^3}\hat{\mathbf r},&0<r\le a,\\[6pt]'
                     r'\dfrac{Q}{4\pi\epsilon_0 r^2}\hat{\mathbf r},&r\ge a.'
                     r'\end{cases}', 1.1, 30)
        self.caption('داخل الكرة يزداد المجال مع r، وخارجها يتناقص مع r^2', .55)
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
