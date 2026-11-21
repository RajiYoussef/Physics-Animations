import numpy as np
from manim import *
from settings import BACKGROUND,CYAN,GOLD,WHITE,render
from support import ar,caption_panel
from tools import emphasize
from math_type import tex
from hbar_character import hbar_character
from raji_sci.physics.field_visuals import polyline
from raji_sci.em.geometry import GaussianContour
from raji_sci.presentation.layout import frame_violations

class ConductorQuestions(MovingCameraScene):
    def construct(self):
        self.camera.background_color=BACKGROUND
        title=ar('اختبر فهمك',size=36).move_to([0,3.45,0])
        panel,c1=caption_panel('أين يكون جهد الكرة الموصلة الموجبة أكبر ما يمكن؟')
        _,c2=caption_panel('الجهد ثابت داخل الكرة ويساوي جهد سطحها.')
        _,c3=caption_panel('ما الشحنة على السطح الخارجي للكرة النحاسية المتعادلة؟')
        _,c4=caption_panel('تظهر شحنة مستحثة سالبة على السطح الداخلي وموجبة على الخارجي.')
        _,c5=caption_panel('كرتان معزولتان تحملان الشحنة نفسها: أيهما جهدها أعلى؟')
        _,c6=caption_panel('عند تساوي الشحنتين، يكون جهد الكرة الأصغر أعلى.')
        if frame_violations([title,panel,c1,c2,c3,c4,c5,c6],margin=.08):raise ValueError('text outside frame')
        self.add(title,panel)
        mascot=hbar_character(.8).move_to([5.9,2.55,0])
        self.play(FadeIn(c1),FadeIn(mascot,shift=LEFT*.2),run_time=.8)

        # Question A: constant inside, decreasing outside.
        center=np.array([-3.35,-.1,0]);radius=1.65
        ball=Circle(radius=radius,stroke_color=GOLD,stroke_width=2,fill_color='#263b43',fill_opacity=.8).move_to(center)
        charges=VGroup(*[Text('+',font='Arial',font_size=18,color=GOLD).move_to(center+radius*np.array([np.cos(a),np.sin(a),0])) for a in np.linspace(0,TAU,16,endpoint=False)])
        qlabel=tex('Q>0',size=35,color=GOLD).move_to(center)
        self.play(GrowFromCenter(ball),LaggedStart(*[FadeIn(q,scale=.4) for q in charges],lag_ratio=.025),FadeIn(qlabel),run_time=2)
        point=Dot(center+[-1.05,0,0],color=WHITE,radius=.08)
        probe_path=polyline(np.array([[center[0]-1.05,center[1]],[center[0],center[1]+.65],[center[0]+1.05,center[1]]]),color=CYAN,stroke_width=3)
        self.play(FadeIn(point),Create(probe_path),run_time=1)
        self.play(MoveAlongPath(point,probe_path),run_time=2.5,rate_func=linear)
        axes=Axes(x_range=[0,4.2,1],y_range=[0,1.4,.5],x_length=4.3,y_length=2.4,tips=False,axis_config={'color':'#7893a2','stroke_width':1.5}).move_to([3,-.05,0])
        xlab=tex('r',size=26,color=WHITE).next_to(axes.x_axis,RIGHT,buff=.1)
        ylab=tex('V',size=26,color=WHITE).next_to(axes.y_axis,UP,buff=.1)
        plot=axes.plot(lambda r:1 if r<=1.4 else 1.4/r,x_range=[0,4],color=CYAN,stroke_width=4,use_smoothing=False)
        cutoff=DashedLine(axes.c2p(1.4,0),axes.c2p(1.4,1),color=GOLD,stroke_width=2)
        edge=tex('R',size=25,color=GOLD).next_to(axes.c2p(1.4,0),DOWN,buff=.12)
        self.play(Create(axes),FadeIn(xlab),FadeIn(ylab),Create(plot),Create(cutoff),FadeIn(edge),Succession(FadeOut(c1),FadeIn(c2)),run_time=2.2)
        emphasize(self,plot,color=CYAN,run_time=.8)
        self.play(*[FadeOut(m) for m in [ball,charges,qlabel,point,probe_path,axes,xlab,ylab,plot,cutoff,edge]],Succession(FadeOut(c2),FadeIn(c3)),run_time=1)

        # Question B: charge at the center of a cavity in an initially neutral conductor.
        center=np.array([-3.2,-.15,0]);outer=Circle(radius=1.95,stroke_color=GOLD,stroke_width=3,fill_color='#173749',fill_opacity=.9).move_to(center)
        cavity=Circle(radius=.78,stroke_color=CYAN,stroke_width=2,fill_color=BACKGROUND,fill_opacity=1).move_to(center)
        central=Dot(center,radius=.17,color=GOLD)
        plus=Text('+',font='Arial',font_size=20,color=BACKGROUND).move_to(center)
        q=tex('+Q',size=33,color=GOLD).next_to(central,UP,buff=.18)
        self.play(Create(outer),FadeIn(cavity),GrowFromCenter(central),FadeIn(plus),FadeIn(q),run_time=2)
        gaussian=GaussianContour(radius=1.34,normals=0).move_to(center)
        self.play(Create(gaussian),run_time=1)
        inside_minus=VGroup(*[Text('−',font='Arial',font_size=18,color=CYAN).move_to(center+.78*np.array([np.cos(a),np.sin(a),0])) for a in np.linspace(0,TAU,12,endpoint=False)])
        outside_plus=VGroup(*[Text('+',font='Arial',font_size=18,color=GOLD).move_to(center+1.95*np.array([np.cos(a),np.sin(a),0])) for a in np.linspace(0,TAU,16,endpoint=False)])
        self.play(LaggedStart(*[FadeIn(a,scale=.4) for a in inside_minus],lag_ratio=.035),run_time=1.5)
        qinner=tex(r'Q_{\rm inner}=-Q',size=38,color=CYAN,width=5).move_to([3,1.2,0])
        total=tex(r'Q_{\rm conductor}=0',size=36,color=WHITE,width=5).move_to([3,.15,0])
        qout=tex(r'Q_{\rm outer}=+Q',size=38,color=GOLD,width=5).move_to([3,-.95,0])
        self.play(Write(qinner),FadeIn(total),run_time=1.6)
        self.play(LaggedStart(*[FadeIn(a,scale=.4) for a in outside_plus],lag_ratio=.025),FadeIn(qout),Succession(FadeOut(c3),FadeIn(c4)),run_time=1.7)
        self.play(Circumscribe(qout,color=GOLD,fade_out=True),run_time=.9)
        self.play(*[FadeOut(m) for m in [outer,cavity,central,plus,q,gaussian,inside_minus,outside_plus,qinner,total,qout]],Succession(FadeOut(c4),FadeIn(c5)),run_time=1)

        # Question C: the spheres represent independent isolated systems.
        ca=np.array([-3.4,.15,0]);cb=np.array([2.4,.15,0]);ra=1.55;rb=.9
        a=Circle(radius=ra,stroke_color=CYAN,stroke_width=2.5,fill_color='#123648',fill_opacity=.85).move_to(ca)
        b=Circle(radius=rb,stroke_color=GOLD,stroke_width=2.5,fill_color='#56371a',fill_opacity=.85).move_to(cb)
        al=tex('A',size=40,color=CYAN).move_to(ca);bl=tex('B',size=40,color=GOLD).move_to(cb)
        qa=tex('+Q',size=34,color=CYAN).next_to(a,DOWN,buff=.28);qb=tex('+Q',size=34,color=GOLD).next_to(b,DOWN,buff=.28)
        self.play(GrowFromCenter(a),GrowFromCenter(b),FadeIn(al),FadeIn(bl),FadeIn(qa),FadeIn(qb),run_time=1.8)
        formula=tex(r'V=\frac{Q}{4\pi\varepsilon_0 R}',size=43,color=WHITE,width=5).move_to([0,2.15,0])
        self.play(Write(formula),run_time=1.5)
        # Height of each bar follows the relative potential 1/R.
        bars=VGroup(Rectangle(width=.4,height=1.0,color=CYAN,fill_color=CYAN,fill_opacity=.7).move_to([-1.0,-.35,0]),Rectangle(width=.4,height=ra/rb,color=GOLD,fill_color=GOLD,fill_opacity=.7).move_to([.1,.01,0]))
        cmp=tex(r'V_B>V_A',size=46,color=GOLD).move_to([0,-1.95,0])
        self.play(LaggedStart(*[GrowFromEdge(x,DOWN) for x in bars],lag_ratio=.3),FadeIn(cmp),Succession(FadeOut(c5),FadeIn(c6)),run_time=1.8)
        self.play(Circumscribe(cmp,color=GOLD,fade_out=True),mascot.animate.shift(LEFT*.25),run_time=1)
        self.wait(1)

if __name__ == '__main__':
    render(ConductorQuestions,filename='scene_08_conductor_questions',preview=True)

