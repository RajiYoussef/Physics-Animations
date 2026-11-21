import numpy as np
from manim import *
from settings import BACKGROUND,CYAN,GOLD,WHITE,render
from support import ar,caption_panel
from tools import field_arrows,emphasize
from math_type import tex
from hbar_character import hbar_character
from raji_sci.physics.electrostatics_logic import point_charge_field
from raji_sci.presentation.layout import frame_violations

class TangentialBoundary(MovingCameraScene):
    def construct(self):
        self.camera.background_color=BACKGROUND
        title=ar("المجال الكهربائي عند سطح الموصل",size=34).move_to([0,3.45,0])
        panel,c1=caption_panel("ما اتجاه المجال الكهربائي خارج سطح الموصل؟")
        _,c2=caption_panel("نحلّل المجال إلى مركبتين: مماسية وعمودية على السطح.")
        _,c3=caption_panel("المركبة المماسية للمجال متصلة عبر الحد الفاصل.")
        _,c4=caption_panel("المجال داخل الموصل صفر، لذلك تنعدم المركبة المماسية خارجه.")
        _,c5=caption_panel("عند الاتزان، يكون المجال خارج سطح الموصل عموديًا عليه.")
        if frame_violations([title,panel,c1,c2,c3,c4,c5],margin=.08):
            raise ValueError('caption outside safe frame')
        self.add(title,panel)
        mascot=hbar_character(.85).move_to([5.9,2.55,0])
        self.play(FadeIn(c1),FadeIn(mascot,shift=LEFT*.2),run_time=.8)
        center=np.array([-2.3,.05,0]);radius=1.8
        disk=Circle(radius=radius,stroke_color='#96b7c7',stroke_width=2.2,fill_color='#0a1b25',fill_opacity=.9).move_to(center)
        angles=np.linspace(0,TAU,18,endpoint=False)
        charges=VGroup(*[Text('+',font='Arial',font_size=19,color=GOLD).move_to(center+radius*np.array([np.cos(a),np.sin(a),0])) for a in angles])
        points=np.array([[center[0]+2.4*np.cos(a),center[1]+2.4*np.sin(a)] for a in angles])
        vectors=point_charge_field(np.array([[center[0],center[1],1.]]),points)
        arrows=field_arrows(points,vectors,max_length=.8,color=CYAN,reference=.08)
        self.play(GrowFromCenter(disk),LaggedStart(*[FadeIn(q,scale=.4) for q in charges],lag_ratio=.03),run_time=2)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.03),run_time=2)
        spot=Circle(radius=.3,color=WHITE,stroke_width=2).move_to(center+RIGHT*radius)
        self.play(Create(spot),mascot.animate.shift(LEFT*.3),run_time=1)
        self.play(Indicate(spot,color=CYAN),run_time=.7)
        self.play(FadeOut(disk),FadeOut(charges),FadeOut(arrows),FadeOut(spot),Succession(FadeOut(c1),FadeIn(c2)),run_time=1)

        region=Polygon([-5.5,-1.9,0],[2.5,-1.9,0],[2.5,-.3,0],[-5.5,-.3,0],fill_color='#13394a',fill_opacity=.7,stroke_width=0)
        surface=Line([-5.5,-.3,0],[2.5,-.3,0],color=GOLD,stroke_width=4)
        stripes=VGroup(*[Line([x,-1.8,0],[x+.8,-.4,0],color='#71b0c2',stroke_opacity=.13,stroke_width=1) for x in np.linspace(-5.2,1.5,12)])
        lab1=ar('داخل الموصل',size=23).move_to([-4.0,-1.2,0]);lab2=ar('خارج الموصل',size=23).move_to([-4.1,1.8,0])
        point=np.array([-1.8,-.3,0]);dot=Dot(point,color=WHITE,radius=.07)
        self.play(FadeIn(region),Create(surface),Create(stripes),FadeIn(lab1),FadeIn(lab2),FadeIn(dot),run_time=1.5)
        normal=DashedLine(point,point+UP*2,color='#97acb6',stroke_width=1.5)
        tangent=DashedLine(point+LEFT*2,point+RIGHT*2,color='#97acb6',stroke_width=1.5)
        vec=Arrow(point,point+[1.6,1.4,0],buff=0,color=WHITE,stroke_width=5)
        vn=Arrow(point,point+UP*1.4,buff=0,color=CYAN,stroke_width=5)
        vt=Arrow(point,point+RIGHT*1.6,buff=0,color=GOLD,stroke_width=5)
        nl=tex(r'E_n',size=31,color=CYAN).next_to(vn,LEFT,buff=.1)
        tl=tex(r'E_t',size=31,color=GOLD).next_to(vt,DOWN,buff=.12)
        self.play(Create(normal),Create(tangent),GrowArrow(vec),run_time=1.3)
        self.play(GrowArrow(vn),GrowArrow(vt),FadeIn(nl),FadeIn(tl),run_time=1.6)
        self.play(Indicate(vt,color=GOLD),run_time=.8)
        self.play(FadeOut(vec),Succession(FadeOut(c2),FadeIn(c3)),run_time=.7)
        one=tex('1',size=26,color=WHITE).move_to([1.95,-1,0]);two=tex('2',size=26,color=WHITE).move_to([1.95,.45,0])
        relation=tex(r'E_{2t}=E_{1t}',size=47,color=WHITE,width=3.7).move_to([4.35,1.25,0])
        inzero=tex(r'E_{1t}=0',size=39,color=CYAN).move_to([4.35,.2,0])
        outzero=tex(r'E_{2t}=0',size=42,color=GOLD).move_to([4.35,-.8,0])
        self.play(FadeIn(one),FadeIn(two),Write(relation),run_time=1.5)
        self.play(Circumscribe(relation,color=GOLD,fade_out=True),run_time=.8)
        self.play(Succession(FadeOut(c3),FadeIn(c4)),FadeIn(inzero,shift=UP*.1),run_time=1)
        self.play(FadeIn(outzero,shift=UP*.1),vt.animate.scale(.001,about_point=point),FadeOut(tl),run_time=1.8)
        emphasize(self,outzero,color=GOLD,run_time=.8)
        self.play(*[FadeOut(m) for m in [region,surface,stripes,lab1,lab2,dot,normal,tangent,vn,vt,nl,one,two,relation,inzero,outzero]],Succession(FadeOut(c4),FadeIn(c5)),run_time=1)
        center=np.array([-.8,0,0]);disk.move_to(center);charges=VGroup(*[Text('+',font='Arial',font_size=19,color=GOLD).move_to(center+radius*np.array([np.cos(a),np.sin(a),0])) for a in angles])
        points=np.array([[center[0]+2.4*np.cos(a),center[1]+2.4*np.sin(a)] for a in angles])
        vectors=point_charge_field(np.array([[center[0],center[1],1.]]),points)
        arrows=field_arrows(points,vectors,max_length=.8,color=CYAN,reference=.08)
        eq=tex(r'E_t=0',size=46,color=GOLD).move_to([4.25,1.05,0])
        final=tex(r'\mathbf{E}=E_n\hat{\mathbf{n}}',size=38,color=WHITE,width=4).move_to([4.25,-.15,0])
        self.play(Create(disk),FadeIn(charges),LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.03),run_time=2)
        self.play(Write(eq),FadeIn(final,shift=UP*.1),mascot.animate.move_to([5.9,2.55,0]),run_time=1.5)
        self.play(Circumscribe(eq,color=GOLD,fade_out=True),run_time=.9)
        self.wait(1)

if __name__ == '__main__':
    render(TangentialBoundary,filename='scene_06_tangential_field',preview=True)

