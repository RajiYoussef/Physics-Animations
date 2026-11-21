import numpy as np
from manim import *
from settings import BACKGROUND, CYAN, GOLD, WHITE, render
from support import ar, caption_panel
from tools import emphasize
from math_type import tex
from raji_sci.physics.field_visuals import ScalarFieldImage, polyline
from raji_sci.presentation.layout import fit_inside, frame_violations


class ConductorEquipotential(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        title = ar("الجهد الكهربائي داخل الموصل", size=35).move_to([0, 3.42, 0])
        panel, c1 = caption_panel("نختار نقطتين داخل الموصل ونبحث عن فرق الجهد بينهما.")
        _, c2 = caption_panel("فرق الجهد يرتبط بالمجال الكهربائي على المسار بين النقطتين.")
        _, c3 = caption_panel("بما أن المجال داخل الموصل صفر، فإن فرق الجهد يساوي صفرًا.")
        _, c4 = caption_panel("النقاط داخل الموصل وعلى سطحه تقع عند الجهد نفسه.")
        _, c5 = caption_panel("سطح الموصل سطح متساوي الجهد.")
        for m in [title,panel,c1,c2,c3,c4,c5]:
            if frame_violations([m],margin=.08):
                raise ValueError("Text outside the frame")
        self.add(title,panel)
        self.play(FadeIn(c1), run_time=.6)

        # Cutaway of the charged conductor, with two connected interior points.
        centre=np.array([-3.35,.05,0]); radius=2.05
        body=Circle(radius=radius, stroke_color="#9ab9c6",stroke_width=2.5,
                    fill_color="#0a1b25",fill_opacity=.9).move_to(centre)
        rings=VGroup(*[Circle(radius=r,stroke_color=CYAN,stroke_opacity=.12,stroke_width=1).move_to(centre) for r in [.55,1.0,1.45,1.78]])
        charges=VGroup(*[Text("+",font="Arial",font_size=20,color=GOLD).move_to(centre+radius*np.array([np.cos(a),np.sin(a),0])) for a in np.linspace(-PI/2,PI/2,10)],
                       *[Text("−",font="Arial",font_size=20,color=CYAN).move_to(centre+radius*np.array([np.cos(a),np.sin(a),0])) for a in np.linspace(PI/2,3*PI/2,10)[1:-1]])
        self.play(FadeIn(body,scale=.85),Create(rings),LaggedStart(*[FadeIn(x,scale=.4) for x in charges],lag_ratio=.025),run_time=2)
        A=centre+[-1.12,-.56,0]; B=centre+[1.05,.6,0]
        dot_a=Dot(A,radius=.095,color=GOLD);dot_b=Dot(B,radius=.095,color=CYAN)
        la=tex('A',size=34,color=GOLD).next_to(dot_a,DOWN,buff=.12)
        lb=tex('B',size=34,color=CYAN).next_to(dot_b,UP,buff=.12)
        self.play(GrowFromCenter(dot_a),Write(la),GrowFromCenter(dot_b),Write(lb),run_time=1.3)
        p1=polyline(np.array([A[:2],[-3.7,-.55],[-3.2,-.1],[-2.8,.35],B[:2]]),color=WHITE,stroke_width=3)
        p2=polyline(np.array([A[:2],[-4.1,.6],[-3.5,1.2],[-2.8,1.15],B[:2]]),color="#688ea3",stroke_width=2.2)
        marker=Dot(A,radius=.085,color=WHITE)
        trail=TracedPath(marker.get_center,stroke_color=WHITE,stroke_width=3,dissipating_time=1.1)
        self.play(Create(p1),FadeIn(marker),run_time=1.2)
        self.add(trail)
        self.play(MoveAlongPath(marker,p1),run_time=3,rate_func=linear)
        self.play(FadeOut(trail),FadeOut(marker),Create(p2),run_time=1.2)
        marker2=Dot(A,radius=.07,color=CYAN)
        self.add(marker2)
        self.play(MoveAlongPath(marker2,p2),run_time=2.6,rate_func=linear)
        self.play(FadeOut(marker2),FadeOut(c1),FadeIn(c2),run_time=.8)

        # Build the source's signed potential difference step by step.
        difference=tex(r'V_A-V_B',size=49,color=GOLD,width=4.8).move_to([2.75,2.05,0])
        law=tex(r'V_A-V_B=\int_A^B\mathbf{E}\cdot d\mathbf{l}',size=47,color=WHITE,width=5.8).move_to([2.7,.45,0])
        zero=tex(r'\mathbf{E}=0',size=43,color=CYAN).move_to([2.7,-.65,0])
        self.play(Write(difference),run_time=1.2)
        self.play(FadeIn(law, shift=UP*.1),run_time=1.8)
        self.play(FadeIn(zero,shift=UP*.15),Indicate(p1,color=CYAN),run_time=1.3)
        integral=tex(r'V_A-V_B=\int_A^B 0\cdot d\mathbf{l}=0',size=41,color=WHITE,width=6).move_to([2.7,-1.55,0])
        self.play(FadeOut(c2),FadeIn(c3),FadeIn(integral, shift=UP*.1),run_time=1.7)
        emphasize(self,integral,color=GOLD,run_time=.9)
        self.play(FadeOut(difference),FadeOut(law),FadeOut(zero),FadeOut(integral),FadeOut(p1),FadeOut(p2),run_time=1)

        # Equal potential is a constant scalar field. Every sampled value is the same.
        equal=tex(r'V_A=V_B',size=53,color=GOLD).move_to([2.7,1.65,0])
        self.play(FadeIn(equal,scale=.7),FadeOut(c3),FadeIn(c4),run_time=1.1)
        heat=ScalarFieldImage(np.ones((50,70))*.65,width=5.6,height=2.5,center=(2.8,-.15,0),
                              vmax=1.0,positive="#53b6cf",zero="#08161e",opacity=.65)
        heatborder=RoundedRectangle(width=5.65,height=2.55,corner_radius=.12,stroke_color=CYAN,stroke_opacity=.55,stroke_width=1.4).move_to([2.8,-.15,0])
        heatlabel=ar("قيمة الجهد داخل الموصل",size=22,color=WHITE).move_to([2.8,.78,0])
        self.play(FadeIn(heat),Create(heatborder),FadeIn(heatlabel),run_time=1.5)
        probe=Dot([.8,-.5,0],radius=.08,color=WHITE)
        read=tex(r'V=V_0',size=34,color=WHITE).move_to([2.8,-1.85,0])
        route=polyline(np.array([[.8,-.5],[1.6,.5],[2.7,-.8],[3.8,.5],[4.8,-.4]]),color=WHITE,stroke_width=2)
        self.play(FadeIn(probe),FadeIn(read),run_time=.7)
        self.play(MoveAlongPath(probe,route),run_time=4,rate_func=linear)
        self.play(FadeOut(heat),FadeOut(heatborder),FadeOut(heatlabel),FadeOut(probe),FadeOut(read),FadeOut(equal),run_time=1)

        # A tilted constant-height plane connects potential to a geometric representation.
        self.play(FadeOut(body),FadeOut(rings),FadeOut(charges),FadeOut(dot_a),FadeOut(dot_b),FadeOut(la),FadeOut(lb),run_time=1)
        corners=[[-4.6,-1.25,0],[1.3,-1.25,0],[4.1,.55,0],[-1.8,.55,0]]
        plane=Polygon(*corners,stroke_color=CYAN,stroke_width=2,fill_color="#20758a",fill_opacity=.32)
        grid=VGroup()
        for t in np.linspace(.1,.9,9):
            a=(1-t)*np.array(corners[0])+t*np.array(corners[3]);b=(1-t)*np.array(corners[1])+t*np.array(corners[2])
            grid.add(Line(a,b,color=CYAN,stroke_opacity=.38,stroke_width=1))
            a=(1-t)*np.array(corners[0])+t*np.array(corners[1]);b=(1-t)*np.array(corners[3])+t*np.array(corners[2])
            grid.add(Line(a,b,color=CYAN,stroke_opacity=.38,stroke_width=1))
        formula=tex(r'V=\mathrm{constant}',size=45,color=WHITE).move_to([3.8,1.75,0])
        path_a=np.array([-3.0,-.9,0]);path_b=np.array([2.0,.25,0]);travel=Line(path_a,path_b,color=GOLD,stroke_width=3)
        bead=Dot(path_a,radius=.1,color=GOLD)
        self.play(FadeOut(c4),FadeIn(c5),DrawBorderThenFill(plane),LaggedStart(*[Create(line) for line in grid],lag_ratio=.025),Write(formula),run_time=2.5)
        self.play(Create(travel),FadeIn(bead),run_time=.9)
        self.play(MoveAlongPath(bead,travel),run_time=3,rate_func=linear)
        self.play(Circumscribe(formula,color=CYAN,fade_out=True),run_time=1)
        self.wait(.8)


if __name__ == "__main__":
    render(ConductorEquipotential, filename="scene_05_equipotential", preview=True)


