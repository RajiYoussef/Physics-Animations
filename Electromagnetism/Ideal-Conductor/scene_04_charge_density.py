import numpy as np
from manim import *
from settings import BACKGROUND, CYAN, GOLD, WHITE, render
from support import ar, caption_panel
from tools import emphasize
from math_type import tex
from raji_sci.physics.field_visuals import polyline


class ChargeDensityInsideConductor(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        title = ar("الشحنة داخل الموصل", size=34).move_to([0, 3.45, 0])
        panel, first = caption_panel("ماذا نستنتج عن الشحنة داخل مادة الموصل؟")
        _, second = caption_panel("المجال الكهربائي يساوي صفرًا على السطح الغاوسي داخل الموصل.")
        _, third = caption_panel("التدفق يساوي صفرًا، والشحنة الصافية المحصورة تساوي صفرًا.")
        _, fourth = caption_panel("كثافة الشحنة الحجمية الصافية تساوي صفرًا داخل الموصل.")
        _, fifth = caption_panel("توجد الشحنة الزائدة على سطح الموصل عند الاتزان.")
        self.add(title,panel)
        self.play(FadeIn(first),run_time=.7)

        # Cutaway geometry keeps the Gaussian volume visibly inside the material.
        conductor=Circle(radius=2.2, stroke_color="#718d9e", stroke_width=2.5,
                         fill_color="#071520", fill_opacity=.82).move_to([-2.8,0,0])
        rings=VGroup(*[Circle(radius=r, color=CYAN, stroke_opacity=.1, stroke_width=1).move_to(conductor)
                       for r in [1.75,1.35,.95]])
        surface=VGroup(*[Text("+",font="Arial",font_size=23,color=GOLD).move_to(conductor.get_center()+2.17*np.array([np.cos(a),np.sin(a),0]))
                         for a in np.linspace(-PI/2,PI/2,9)],
                       *[Text("−",font="Arial",font_size=23,color=CYAN).move_to(conductor.get_center()+2.17*np.array([np.cos(a),np.sin(a),0]))
                         for a in np.linspace(PI/2,3*PI/2,9)[1:-1]])
        self.play(GrowFromCenter(conductor),Create(rings),LaggedStart(*[FadeIn(q,scale=.5) for q in surface],lag_ratio=.025),run_time=2)
        probes=VGroup(*[Dot(conductor.get_center()+np.array([x,y,0]),radius=.04,color=CYAN)
                        for x,y in [(-.9,.3),(-.4,-.9),(.0,.9),(.65,.1),(.9,-.7),(-1.1,-.55)]])
        self.play(LaggedStart(*[FadeIn(p,scale=2) for p in probes],lag_ratio=.2),run_time=1.8)
        region=VGroup(Ellipse(width=1.3,height=.54,color=CYAN,stroke_width=2.2),
                      Ellipse(width=1.3,height=1.03,color=CYAN,stroke_width=2.2),
                      Line([-.65,0,0],[.65,0,0],color=CYAN,stroke_opacity=.25))
        region.move_to(conductor.get_center()+[.25,.1,0])
        cursor=Circle(radius=.78,color=CYAN,stroke_opacity=.3,stroke_width=7).move_to(region)
        self.play(Create(region),Create(cursor),FadeOut(first),FadeIn(second),run_time=1.7)
        self.play(FadeOut(cursor),region.animate.shift(LEFT*.55+UP*.4),run_time=1.6)
        self.play(region.animate.shift(RIGHT*.9+DOWN*.8),run_time=1.8)
        label=ar("سطح غاوسي",size=24,color=CYAN).move_to([2.7,1.7,0])
        pointer=polyline(np.array([[1.4,1.5],[-.3,1],[-1.9,-.2]]),color=CYAN,stroke_width=2,smooth=False)
        self.play(FadeIn(label),Create(pointer),run_time=1)

        # Build the equation from the physical quantity being examined.
        law=tex(r'\oint\;\mathbf{E}\cdot d\mathbf{A}=\frac{Q_{\rm enc}}{\varepsilon_0}',size=49,color=WHITE,width=5.5).move_to([2.4,.45,0])
        zero_e=tex(r'\mathbf{E}=0',size=48,color=CYAN).move_to([2.4,-.75,0])
        self.play(Write(law),run_time=2.2)
        self.play(FadeIn(zero_e,shift=UP*.1),Indicate(region,color=CYAN),run_time=1.2)
        self.play(FadeOut(second),FadeIn(third),run_time=.7)
        enclosed=tex(r'Q_{\rm enc}=0',size=48,color=GOLD).move_to([2.4,-1.75,0])
        self.play(TransformFromCopy(law,enclosed),run_time=1.8)
        emphasize(self,enclosed,color=GOLD,run_time=.8)
        self.play(FadeOut(pointer),FadeOut(label),FadeOut(probes),FadeOut(zero_e),run_time=.8)

        # Sample different small volumes to show that the conclusion is local.
        small=VGroup(*[Circle(radius=.22, color=CYAN, stroke_width=2).move_to(conductor.get_center()+np.array([x,y,0]))
                       for x,y in [(-.85,.65),(.0,.85),(.85,.55),(-.9,-.5),(.15,-.4),(.85,-.65)]])
        self.play(FadeOut(region),LaggedStart(*[Create(s) for s in small],lag_ratio=.16),run_time=2.2)
        self.play(LaggedStart(*[Indicate(s,color=CYAN,scale_factor=1.25) for s in small],lag_ratio=.12),run_time=2)
        self.play(FadeOut(law),FadeOut(enclosed),FadeOut(third),FadeIn(fourth),run_time=.8)
        differential=tex(r'\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}',size=48,color=WHITE,width=5.5).move_to([2.5,.9,0])
        substitute=tex(r'0=\frac{\rho}{\varepsilon_0}',size=46,color=CYAN).move_to([2.5,-.15,0])
        answer=tex(r'\rho=0',size=57,color=GOLD).move_to([2.5,-1.3,0])
        self.play(Write(differential),run_time=2)
        self.play(TransformFromCopy(differential,substitute),run_time=1.4)
        self.play(TransformFromCopy(substitute,answer),run_time=1.4)
        self.play(Circumscribe(answer,color=GOLD,stroke_width=3,fade_out=True),run_time=1.2)

        # Positive and negative microscopic charges can remain while the net density is zero.
        self.play(FadeOut(differential),FadeOut(substitute),FadeOut(answer),FadeOut(small),run_time=1)
        neutral=VGroup(*[VGroup(Text("+",font="Arial",font_size=23,color=GOLD),Text("−",font="Arial",font_size=23,color=CYAN)).arrange(RIGHT,buff=.1).move_to(conductor.get_center()+[x,y,0])
                         for x,y in [(-.9,.75),(.1,.65),(.85,.3),(-.7,-.4),(.35,-.55)]])
        self.play(LaggedStart(*[FadeIn(pair) for pair in neutral],lag_ratio=.15),run_time=1.4)
        hint=ar("الشحنة الصافية داخل المادة",size=24,color=WHITE).move_to([2.5,.8,0])
        rho=tex(r'\rho=0',size=55,color=GOLD).move_to([2.5,-.3,0])
        self.play(FadeIn(hint),Write(rho),run_time=1.3)
        self.play(LaggedStart(*[Indicate(pair,color=WHITE,scale_factor=1.1) for pair in neutral],lag_ratio=.2),run_time=2)

        self.play(FadeOut(neutral),FadeOut(hint),FadeOut(rho),FadeOut(fourth),FadeIn(fifth),
                  FadeOut(surface),FadeOut(rings),conductor.animate.move_to(ORIGIN),run_time=1.4)
        exterior=VGroup(*[Text("−",font="Arial",font_size=27,color=CYAN).move_to(2.18*np.array([np.cos(a),np.sin(a),0])) for a in np.linspace(0,TAU,18,endpoint=False)])
        self.play(LaggedStart(*[FadeIn(q,scale=.45) for q in exterior],lag_ratio=.04),run_time=2)
        self.play(Indicate(exterior,color=CYAN,scale_factor=1.03),run_time=1.1)
        target1=Dot([-.8,0,0],color=GOLD,radius=.07);target2=Dot([.8,0,0],color=GOLD,radius=.07)
        path=polyline(np.array([[-.8,0],[-.35,.55],[.3,.55],[.8,0]]),color=WHITE,stroke_width=2)
        marker=Dot(target1.get_center(),color=WHITE,radius=.06)
        self.play(FadeIn(target1),FadeIn(target2),Create(path),FadeIn(marker),run_time=1)
        self.play(MoveAlongPath(marker,path),run_time=1.8)
        self.wait(.7)


if __name__ == "__main__":
    render(ChargeDensityInsideConductor, filename="scene_04_charge_density", preview=True)

