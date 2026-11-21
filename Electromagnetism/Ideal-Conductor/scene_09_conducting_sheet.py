"""Charged conducting sheet: source Chapter 7, pages 5-6."""
from dataclasses import dataclass
import numpy as np
from manim import *
from settings import BACKGROUND, CYAN, GOLD, WHITE, render
from support import ar, caption_panel
from tools import field_arrows, emphasize
from math_type import tex
from hbar_character import hbar_character
from raji_sci.physics.field_visuals import polyline
from raji_sci.em.field_lines import trace_field_line
from raji_sci.presentation.layout import frame_violations


@dataclass(frozen=True)
class SheetCase:
    field: float
    total_charge: float = 2.0
    epsilon_area: float = 1.0

    @property
    def upper(self):
        return self.total_charge / 2 + self.epsilon_area * self.field

    @property
    def lower(self):
        return self.total_charge / 2 - self.epsilon_area * self.field

    @property
    def net_field(self):
        return self.field + (self.lower - self.upper) / (2 * self.epsilon_area)


def validate_cases():
    for case in (SheetCase(0), SheetCase(1), SheetCase(.55), SheetCase(1.45)):
        assert np.isclose(case.upper + case.lower, case.total_charge)
        assert np.isclose(case.net_field, 0)
    assert SheetCase(1).lower == 0
    assert SheetCase(.55).lower > 0
    assert SheetCase(1.45).lower < 0


def caption_transition(old, new):
    return Succession(FadeOut(old, run_time=.25), FadeIn(new, run_time=.25))


def plate_charges(y, n=11, color=GOLD, sign='+', x_min=-5.6, x_max=.35):
    return VGroup(*[Text(sign, font='Arial', font_size=23, color=color).move_to([x,y,0])
                    for x in np.linspace(x_min,x_max,n)])


def surface_plate():
    return VGroup(
        Polygon([-5.9,.15,0],[.65,.15,0],[.65,-.55,0],[-5.9,-.55,0],
                stroke_color='#92d1dd',stroke_width=2,fill_color='#123a4c',fill_opacity=.92),
        Line([-5.9,.15,0],[.65,.15,0],color=CYAN,stroke_width=4),
        Line([-5.9,-.55,0],[.65,-.55,0],color='#367e94',stroke_width=3),
        *[Line([x,-.5,0],[x+.36,.1,0],color='#8fd6e1',stroke_opacity=.14,stroke_width=1)
          for x in np.linspace(-5.7,.1,15)])


def field_line(x, y0, y1, color):
    direction=1 if y1>y0 else -1
    points=trace_field_line(lambda p: np.array([0.,1.]),[x,y0],step=.08,
                            steps=int(abs(y1-y0)/.08),direction=direction)
    return polyline(points,color=color,stroke_width=1.3,smooth=False)


class ConductingSheet(MovingCameraScene):
    def construct(self):
        validate_cases()
        self.camera.background_color=BACKGROUND
        title=ar('صفيحة موصلة في مجال كهربائي',size=34).move_to([0,3.45,0])
        box,c1=caption_panel('صفيحة موصلة رقيقة تحمل شحنة كلية موجبة.')
        _,c2=caption_panel('في غياب المجال الخارجي، تتوزع الشحنة بالتساوي على الوجهين.')
        _,c3=caption_panel('المجالان الناتجان عن الوجهين يتلاشيان داخل الصفيحة.')
        _,c4=caption_panel('نطبّق الآن مجالًا كهربائيًا خارجيًا إلى أعلى.')
        _,c5=caption_panel('نقارن المجال المطبق بالمجال الناتج عن الشحنة على الوجه العلوي.')
        _,c6=caption_panel('إذا تساوى المجالان، يكون النظام في حالة اتزان.')
        _,c7=caption_panel('إذا كان المجال المطبق أضعف، تظهر شحنة موجبة على الوجه السفلي.')
        _,c8=caption_panel('إذا كان المجال المطبق أقوى، تصبح الشحنة على الوجه السفلي سالبة.')
        _,c9=caption_panel('في كل الحالات يبقى مجموع شحنتي الوجهين ثابتًا.')
        if frame_violations([title,box,c1,c2,c3,c4,c5,c6,c7,c8,c9],margin=.08):
            raise ValueError('A caption extends outside the frame')
        self.add(title,box)
        guide=hbar_character(.73).move_to([5.95,2.63,0])
        self.play(FadeIn(c1),FadeIn(guide,shift=LEFT*.15),run_time=.9)

        # Isometric solid: large face, thin front and side, and moving charge.
        top=Polygon([-5.8,.65,0],[-1.2,.65,0],[.55,1.55,0],[-4.05,1.55,0],
                    stroke_color='#9be3ee',stroke_width=2,fill_color='#1c7787',fill_opacity=.72)
        front=Polygon([-5.8,.65,0],[-1.2,.65,0],[-1.2,.35,0],[-5.8,.35,0],
                      stroke_color='#5c9daa',stroke_width=1.5,fill_color='#174052',fill_opacity=.95)
        side=Polygon([-1.2,.65,0],[.55,1.55,0],[.55,1.25,0],[-1.2,.35,0],
                     stroke_color='#8ab9c5',stroke_width=1.5,fill_color='#246078',fill_opacity=.9)
        grid=VGroup()
        for t in np.linspace(.16,.84,6):
            a=(1-t)*np.array([-5.8,.65,0])+t*np.array([-4.05,1.55,0])
            b=(1-t)*np.array([-1.2,.65,0])+t*np.array([.55,1.55,0])
            grid.add(Line(a,b,color='#b7e8ef',stroke_opacity=.22,stroke_width=1))
        geom=VGroup(front,side,top,grid)
        dimension=VGroup(tex(r'A=a^2',size=42,color=WHITE),tex(r'a\gg h',size=36,color=CYAN),tex(r'Q>0',size=40,color=GOLD)).arrange(DOWN,buff=.35).move_to([3.4,.55,0])
        for item in dimension:
            if frame_violations([item],margin=.1):raise ValueError('Formula outside frame')
        self.play(FadeIn(geom,scale=.9),LaggedStart(*[Write(x) for x in dimension],lag_ratio=.35),run_time=2.5)
        trace=Line([-5.4,.8,0],[-1.4,.8,0],color=WHITE,stroke_width=3)
        self.play(ShowPassingFlash(trace,time_width=.3),run_time=1.6)
        self.play(geom.animate.shift(DOWN*.4),run_time=1.1)

        # Cut to a cross-section; +Q/2 is placed on each face.
        plate=surface_plate()
        self.play(FadeOut(geom),FadeOut(dimension),FadeIn(plate),caption_transition(c1,c2),run_time=1.3)
        upper=plate_charges(.30);lower=plate_charges(-.70)
        symbols=VGroup(*[Text('+',font='Arial',font_size=22,color=GOLD).move_to([x,-.2,0]) for x in np.linspace(-5.5,.25,11)])
        self.play(LaggedStart(*[FadeIn(q,scale=.5) for q in symbols],lag_ratio=.04),run_time=1)
        self.play(FadeOut(symbols),LaggedStart(*[FadeIn(q,shift=UP*.2) for q in upper],lag_ratio=.025),
                  LaggedStart(*[FadeIn(q,shift=DOWN*.2) for q in lower],lag_ratio=.025),run_time=2)
        qtop=tex(r'Q/2',size=39,color=GOLD).move_to([2.45,.8,0])
        qbot=tex(r'Q/2',size=39,color=GOLD).move_to([2.45,-1,0])
        self.play(Write(qtop),Write(qbot),run_time=1.2)
        # Counter-directed fields at the same internal points.
        xpts=np.array([[x,-.19] for x in np.linspace(-5.3,-.2,8)])
        e_top=field_arrows(xpts+[-.09,0],np.tile([0.,-1.],(len(xpts),1)),max_length=.39,color=GOLD,reference=.3)
        e_bot=field_arrows(xpts+[.09,0],np.tile([0.,1.],(len(xpts),1)),max_length=.39,color=CYAN,reference=.3)
        cancel=tex(r'\mathbf{E}_{\rm inside}=0',size=37,color=WHITE,width=4.2).move_to([3.05,-.05,0])
        self.play(LaggedStart(*[GrowArrow(a) for a in e_top],lag_ratio=.025),
                  LaggedStart(*[GrowArrow(a) for a in e_bot],lag_ratio=.025),
                  FadeIn(cancel),caption_transition(c2,c3),run_time=2)
        self.play(Indicate(e_top,color=GOLD),Indicate(e_bot,color=CYAN),run_time=1.1)

        # External field built with traced field lines and arrows from the actual uniform field.
        self.play(FadeOut(e_top),FadeOut(e_bot),FadeOut(cancel),FadeOut(qtop),FadeOut(qbot),
                  caption_transition(c3,c4),run_time=.8)
        seeds=np.array([[x,-2.25] for x in np.linspace(-5.3,-.2,7)])
        field_arrows_up=field_arrows(seeds,np.tile([0.,1.],(len(seeds),1)),max_length=1.3,color=CYAN,reference=.3)
        stream=VGroup(*[field_line(x,-2.25,-1.05,CYAN) for x in np.linspace(-5.3,-.2,7)])
        field_label=tex(r'\mathbf{E}_{\rm ext}=E_0\hat{\mathbf{z}}',size=38,color=CYAN,width=4.2).move_to([3.1,1.05,0])
        self.play(LaggedStart(*[Create(s) for s in stream],lag_ratio=.045),
                  LaggedStart(*[GrowArrow(a) for a in field_arrows_up],lag_ratio=.045),Write(field_label),run_time=2.4)
        self.play(*[ShowPassingFlash(s.copy().set_stroke(width=3),time_width=.25) for s in stream],run_time=1.6)

        # The source tests a state with Q on the upper face and compares its opposing field.
        self.play(FadeOut(lower),FadeOut(upper),FadeIn(plate_charges(.30,n=15)),FadeOut(stream),FadeOut(field_arrows_up),FadeOut(field_label),
                  caption_transition(c4,c5),run_time=1.1)
        top_only=tex(r'Q_{\rm top}=Q',size=34,color=GOLD).move_to([3.05,1.65,0])
        threshold=tex(r'E_c=\frac{Q}{2\varepsilon_0 A}',size=41,color=WHITE,width=4.8).move_to([3.05,.55,0])
        # Longer opposing arrows are constructed by the Raji helper from a downward field.
        down=field_arrows(xpts,np.tile([0.,-1.],(len(xpts),1)),max_length=.5,color=GOLD,reference=.25)
        self.play(Write(top_only),Write(threshold),LaggedStart(*[GrowArrow(a) for a in down],lag_ratio=.04),run_time=2)
        self.play(Indicate(threshold,color=GOLD),run_time=.8)

        # Three source cases.  Each panel is a separate equilibrium for the same Q and A.
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in [title,box,c5,guide]],run_time=1)
        self.play(caption_transition(c5,c6),run_time=.7)
        headings=[tex(r'E_0=E_c',size=34,color=WHITE),tex(r'E_0<E_c',size=34,color=WHITE),tex(r'E_0>E_c',size=34,color=WHITE)]
        tops=[tex('Q',size=35,color=GOLD),tex('Q-q',size=35,color=GOLD),tex('Q+q',size=35,color=GOLD)]
        bottoms=[tex('0',size=35,color=WHITE),tex('+q',size=35,color=GOLD),tex('-q',size=35,color=CYAN)]
        frames=VGroup()
        for i,x in enumerate([-4.2,0,4.2]):
            slab=RoundedRectangle(width=3.35,height=.52,corner_radius=.08,stroke_color=CYAN,stroke_width=2,
                                  fill_color='#174052',fill_opacity=.9).move_to([x,-.1,0])
            headings[i].move_to([x,1.65,0]);tops[i].move_to([x,.65,0]);bottoms[i].move_to([x,-.9,0])
            upper_marks=VGroup(*[Text('+',font='Arial',font_size=16,color=GOLD).move_to([x+dx,.18,0])
                                 for dx in np.linspace(-1.25,1.25,6)])
            lower_marks=VGroup()
            if i:
                sign='+' if i==1 else '−'
                color=GOLD if i==1 else CYAN
                lower_marks=VGroup(*[Text(sign,font='Arial',font_size=16,color=color).move_to([x+dx,-.38,0])
                                     for dx in np.linspace(-1.25,1.25,6)])
            field_pair=VGroup(
                Arrow([x-.45,-.26,0],[x-.45,.06,0],buff=0,color=CYAN,stroke_width=2.2,
                      max_tip_length_to_length_ratio=.35),
                Arrow([x+.45,.06,0],[x+.45,-.26,0],buff=0,color=GOLD,stroke_width=2.2,
                      max_tip_length_to_length_ratio=.35))
            unit=VGroup(slab,headings[i],tops[i],bottoms[i],upper_marks,lower_marks,field_pair)
            frames.add(unit)
        self.play(FadeIn(frames[0],shift=UP*.1),run_time=1.2)
        eq0=tex(r'E_{\rm inside}=0',size=34,color=CYAN).move_to([-4.2,-1.7,0])
        self.play(FadeIn(eq0),run_time=.6)
        self.play(caption_transition(c6,c7),FadeIn(frames[1],shift=UP*.1),run_time=1.3)
        eq1=tex(r'E_{\rm inside}=0',size=34,color=CYAN).move_to([0,-1.7,0])
        self.play(FadeIn(eq1),run_time=.6)
        self.play(caption_transition(c7,c8),FadeIn(frames[2],shift=UP*.1),run_time=1.3)
        eq2=tex(r'E_{\rm inside}=0',size=34,color=CYAN).move_to([4.2,-1.7,0])
        self.play(FadeIn(eq2),run_time=.6)
        self.play(Indicate(bottoms[0],color=WHITE),Indicate(bottoms[1],color=GOLD),Indicate(bottoms[2],color=CYAN),run_time=1.4)
        self.play(caption_transition(c8,c9),run_time=.7)
        total=tex(r'Q_{\rm top}+Q_{\rm bottom}=Q',size=33,color=WHITE,width=6.8).move_to([0,2.55,0])
        self.play(Write(total),run_time=1.5)
        self.play(Circumscribe(total,color=CYAN,fade_out=True),run_time=1)
        self.wait(1)


if __name__ == '__main__':
    render(ConductingSheet,filename='scene_09_conducting_sheet',preview=True)
