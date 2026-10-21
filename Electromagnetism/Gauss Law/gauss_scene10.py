"""S10: Infinite line charge — cylindrical Gaussian surface.
Run directly in PyCharm. Optional S10_ar.wav OR S10_B01_ar.wav etc.
For a single continuous recording, paragraph starts are estimates and may require editing.
"""
from __future__ import annotations
from pathlib import Path
from html import escape
import contextlib, wave, subprocess, sys
import numpy as np
from manim import *

BG='#101820'; WHITE='#F5F5F5'; GOLD='#F6C85F'; CYAN='#58C4DD'; VIOLET='#C792EA'; RED='#FF6B6B'
ARABIC_FONT='Arial'


def wav_duration(p):
    try:
        with contextlib.closing(wave.open(str(p),'rb')) as w:
            return w.getnframes()/w.getframerate()
    except (OSError, wave.Error, ZeroDivisionError): return 0.

class GaussScene10(Scene):
    def ar(self, s, size=25, color=WHITE):
        obj=MarkupText(escape(s),font=ARABIC_FONT,font_size=size,color=color)
        if obj.width > 5.6: obj.scale_to_fit_width(5.6)
        return obj

    def play_t(self, animation, seconds):
        self.play(animation,run_time=seconds); self.t+=seconds

    def wait_t(self, seconds):
        if seconds>1e-5: self.wait(seconds); self.t+=seconds

    def start_beat(self, i):
        if self.audio_mode=='beats': self.add_sound(str(self.clips[i]))
        self.beat_end=self.t+self.lengths[i]

    def finish_beat(self, final=False):
        remaining=self.beat_end-self.t
        if remaining<-.05: raise RuntimeError(f'Beat overrun: {-remaining:.2f}s')
        if final and remaining>=.5:
            self.wait_t(remaining-.5)
            self.play_t(FadeOut(Group(*list(self.mobjects))),.5)
        else: self.wait_t(max(0,remaining))

    def construct(self):
        self.camera.background_color=BG
        self.t=0.
        directory=Path(__file__).resolve().parent
        self.clips=[directory/f'S10_B0{i}_ar.wav' for i in (1,2,3)]
        whole=directory/'S10_ar.wav'
        self.lengths=[18.,19.,27.]
        self.audio_mode='silent'
        if whole.is_file():
            self.audio_mode='whole'
            self.lengths[-1]+=max(0.,wav_duration(whole)-60.)
            print('Continuous narration: cue changes use planned 00:19 and 00:38 starts; adjust after measuring actual paragraph transitions.')
        elif all(p.is_file() for p in self.clips):
            self.audio_mode='beats'
            self.lengths=[max(s,wav_duration(p))+h for p,s,h in zip(self.clips,(15,16,23),(3,3,4))]
        self.build_objects()
        self.play_t(FadeIn(self.title),.8); self.wait_t(.2)
        if self.audio_mode=='whole': self.add_sound(str(whole))
        self.beat1(); self.beat2(); self.beat3()
        print('S10 actual scheduled length:',self.t)
        assert abs(self.t-(1+sum(self.lengths)))<.07

    def build_objects(self):
        self.title=self.ar('خط الشحنة: حساب التدفق عبر الأسطوانة',39).move_to([0,3.29,0])
        # A projected closed cylinder, not a 2D loop integral.
        cx=-3.85; top=1.48; bot=-1.32; rx=1.47; ry=.43
        self.axis=DashedLine([cx,-2.22,0],[cx,2.24,0],color=RED,dash_length=.16,stroke_width=3)
        self.charges=VGroup(*[MathTex('+',color=RED,font_size=25).move_to([cx,y,0]) for y in np.linspace(-2.02,2.05,10)])
        self.top_ellipse=Ellipse(width=2*rx,height=2*ry,color=CYAN,stroke_width=2.5).move_to([cx,top,0])
        self.bottom_ellipse=Ellipse(width=2*rx,height=2*ry,color=CYAN,stroke_width=2.5).move_to([cx,bot,0])
        self.sides=VGroup(Line([cx-rx,top,0],[cx-rx,bot,0],color=CYAN,stroke_width=3),Line([cx+rx,top,0],[cx+rx,bot,0],color=CYAN,stroke_width=3))
        self.side_fill=Rectangle(width=rx*2,height=top-bot,stroke_opacity=0,fill_color=CYAN,fill_opacity=.065).move_to([cx,(top+bot)/2,0])
        self.top_fill=Ellipse(width=2*rx,height=2*ry,stroke_opacity=0,fill_color=CYAN,fill_opacity=.22).move_to([cx,top,0])
        self.bot_fill=Ellipse(width=2*rx,height=2*ry,stroke_opacity=0,fill_color=CYAN,fill_opacity=.22).move_to([cx,bot,0])
        self.top_normal=Arrow([cx+.6,top,0],[cx+.6,top+.7,0],buff=0,color=VIOLET,stroke_width=4)
        self.bot_normal=Arrow([cx+.6,bot,0],[cx+.6,bot-.7,0],buff=0,color=VIOLET,stroke_width=4)
        self.side_normal=Arrow([cx+rx,.07,0],[cx+rx+.67,.07,0],buff=0,color=VIOLET,stroke_width=4)
        self.side_field=Arrow([cx+rx-.6,-.42,0],[cx+rx+.48,-.42,0],buff=0,color=GOLD,stroke_width=5)
        self.length_marker=DoubleArrow([cx-rx-.30,bot,0],[cx-rx-.30,top,0],buff=0,tip_length=.11,color=WHITE,stroke_width=2)
        self.L=MathTex('L',font_size=31,color=WHITE).next_to(self.length_marker,LEFT,buff=.13)
        self.radius_marker=Line([cx,top,0],[cx+rx,top,0],color=WHITE,stroke_width=2)
        self.r=MathTex('r',font_size=31,color=WHITE).next_to(self.radius_marker,UP,buff=.13)
        self.cylinder_label=self.ar('سطح غاوس أسطواني مغلق',22).move_to([cx,-2.37,0])
        self.cap_top_label=self.ar('القاعدة العليا',23).move_to([cx+1.47,2.25,0])
        self.cap_bottom_label=self.ar('القاعدة السفلى',23).move_to([cx+1.45,-1.93,0])
        self.side_label=self.ar('السطح الجانبي المنحني',22).move_to([cx,-2.37,0])
        self.segment_label=self.ar('الجزء المحصور من خط الشحنة',21).move_to([cx,-2.37,0])
        self.segment=Line([cx,bot,0],[cx,top,0],color=RED,stroke_width=7)
        # Inset from above: field arrows lie in cap plane, orthogonal to axial normals.
        ic=np.array([-1.10,1.78,0]); self.inset_center=ic
        self.inset_circle=Circle(radius=.47,color=CYAN,stroke_width=2).move_to(ic)
        self.inset_charge=MathTex('+',color=RED,font_size=23).move_to(ic)
        self.inset_arrows=VGroup()
        for a in (0,PI/2,PI,3*PI/2):
            vec=np.array([np.cos(a),np.sin(a),0])
            self.inset_arrows.add(Arrow(ic+vec*.15,ic+vec*.42,buff=0,color=GOLD,stroke_width=3,tip_length=.12))
        self.inset_label=self.ar('منظر علوي',20).move_to([-1.13,1.09,0])
        # Right-side algebra: equations occupy separate, nonoverlapping rows.
        strings=[r'\Phi_{\mathrm{caps}}=0',r'\Phi_{\mathrm{side}}=E_r(r)\,2\pi rL',r'Q_{\mathrm{in}}=\rho_l L',r'E_r(r)\,2\pi rL=\frac{\rho_l L}{\epsilon_0}',r'\mathbf E=\frac{\rho_l}{2\pi\epsilon_0 r}\hat{\mathbf u}_r\quad(r>0)']
        self.eqs=[]
        for j,(s,y) in enumerate(zip(strings,(1.88,1.02,.16,-.78,-1.84))):
            mob=MathTex(s,color=WHITE,font_size=35, **({'substrings_to_isolate':['L']} if j == 3 else {})).move_to([3.36,y,0])
            if mob.width>6.0: mob.scale_to_fit_width(6.0)
            self.eqs.append(mob)
        self.zero_label=self.ar('تدفق القاعدتين يساوي صفرًا',24).move_to([3.25,2.55,0])
        self.side_eq_label=self.ar('السطح الجانبي المنحني',22).move_to([3.25,1.53,0])
        # Showing cancellation on a duplicate equation keeps original exact LaTeX intact.
        self.cancel_L=MathTex('L',color=GOLD,font_size=32).move_to([4.6,-.31,0])
        self.highlight=SurroundingRectangle(self.eqs[-1],buff=.12,color=GOLD,stroke_width=2)

    def beat1(self):
        self.start_beat(0)
        self.play_t(Create(self.axis),.7)
        self.play_t(FadeIn(self.charges),.6)
        self.play_t(Create(self.top_ellipse),.65)
        self.play_t(Create(self.bottom_ellipse),.65)
        self.play_t(Create(self.sides),.7)
        self.play_t(FadeIn(self.side_fill,self.cylinder_label),.5)
        self.play_t(GrowFromCenter(self.length_marker),.7)
        self.play_t(FadeIn(self.L),.3)
        self.play_t(Create(self.radius_marker),.45)
        self.play_t(FadeIn(self.r),.3)
        self.play_t(FadeIn(self.top_fill,self.bot_fill),.6)
        self.play_t(FadeIn(self.cap_top_label,self.cap_bottom_label),.7)
        self.play_t(GrowArrow(self.top_normal),.65)
        self.play_t(GrowArrow(self.bot_normal),.65)
        self.play_t(Create(self.inset_circle),.5)
        self.play_t(FadeIn(self.inset_charge,self.inset_label),.5)
        self.play_t(LaggedStart(*[GrowArrow(a) for a in self.inset_arrows],lag_ratio=.18),1.)
        self.play_t(Write(self.eqs[0]),1.1)
        self.play_t(FadeIn(self.zero_label),.55)
        self.finish_beat()

    def beat2(self):
        self.start_beat(1)
        self.play_t(FadeOut(self.zero_label,self.cap_top_label,self.cap_bottom_label,self.cylinder_label),.5)
        self.play_t(FadeOut(self.top_fill,self.bot_fill),.4)
        self.play_t(Indicate(self.side_fill,color=CYAN),1.0)
        self.play_t(FadeIn(self.side_label),.5)
        self.play_t(GrowArrow(self.side_field),.85)
        self.play_t(GrowArrow(self.side_normal),.85)
        self.play_t(Indicate(self.side_field,color=GOLD),.8)
        self.play_t(FadeIn(self.side_eq_label),.5)
        self.play_t(Write(self.eqs[1]),1.8)
        self.play_t(Indicate(self.eqs[1],color=GOLD),1.)
        self.finish_beat()

    def beat3(self):
        self.start_beat(2)
        self.play_t(FadeOut(self.side_label,self.side_eq_label),.5)
        self.play_t(Indicate(self.charges,color=RED),1.1)
        self.play_t(Indicate(self.segment,color=RED),1.) if self.segment in self.mobjects else self.play_t(Create(self.segment),.8)
        self.play_t(FadeIn(self.segment_label),.5)
        self.play_t(Write(self.eqs[2]),1.2)
        self.play_t(Write(self.eqs[3]),1.9)
        self.play_t(Circumscribe(self.eqs[3],color=GOLD),1.3)
        # The L factors were isolated when constructing this MathTex object.
        # Inspect direct parts instead of calling version-dependent get_parts_by_tex.
        L_terms = [part for part in self.eqs[3].submobjects
                   if getattr(part, "tex_string", "").strip() == "L"]
        if len(L_terms) == 2:
            self.play_t(AnimationGroup(*[
                Indicate(part, color=GOLD) for part in L_terms
            ]), .8)
            strokes = VGroup(*[
                Line(part.get_corner(DL), part.get_corner(UR),
                     color=RED, stroke_width=3.5) for part in L_terms
            ])
            self.play_t(Create(strokes), .65)
            self.play_t(FadeOut(strokes), .45)
        else:
            # Safe fallback if an installed Manim version groups MathTex
            # components differently: the algebra remains correct and visible.
            self.play_t(Indicate(self.eqs[3], color=GOLD), 1.9)
        self.play_t(Write(self.eqs[4]),2.2)
        self.play_t(Create(self.highlight),.65)
        self.play_t(Indicate(self.eqs[4],color=GOLD),1.0)
        self.finish_beat(final=True)


# =====================================================
# RUN DIRECTLY IN PYCHARM — OPEN RENDERED VIDEO
# =====================================================
if __name__=='__main__':
    subprocess.run([
        sys.executable,'-m','manim','-p','-qh',
        '-r','1920,1080','--fps','30',
        str(Path(__file__).resolve()),'GaussScene10'
    ],check=True)
