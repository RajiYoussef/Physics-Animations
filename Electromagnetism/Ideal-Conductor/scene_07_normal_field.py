import numpy as np
from manim import *
from settings import BACKGROUND,CYAN,GOLD,WHITE,render
from support import ar,caption_panel
from tools import field_arrows,emphasize
from math_type import tex
from hbar_character import hbar_character
from raji_sci.presentation.layout import frame_violations
from raji_sci.physics.field_visuals import polyline
from raji_sci.em.geometry import FluxPatch

class NormalBoundary(MovingCameraScene):
    def construct(self):
        self.camera.background_color=BACKGROUND
        title=ar('المجال العمودي والشحنة السطحية',size=34).move_to([0,3.43,0])
        box,c1=caption_panel('كيف نحسب المجال الكهربائي خارج سطح الموصل؟')
        _,c2=caption_panel('نختار سطحًا غاوسيًا صغيرًا يقطع سطح الموصل.')
        _,c3=caption_panel('المجال داخل الموصل صفر، فيبقى التدفق عبر الوجه الخارجي.')
        _,c4=caption_panel('كثافة الشحنة السطحية تحدد المركبة العمودية للمجال.')
        _,c5=caption_panel('في الفراغ نستخدم سماحية الفراغ، وفي وسط عازل نستخدم سماحيته.')
        if frame_violations([title,box,c1,c2,c3,c4,c5],margin=.08):raise ValueError('Text outside frame')
        self.add(title,box)
        guide=hbar_character(.75).move_to([5.95,2.65,0])
        self.play(FadeIn(c1),FadeIn(guide,shift=LEFT*.15),run_time=.8)

        # Surface patch: the field changes with surface charge density.
        surface=Line([-5.8,-.35,0],[-.2,-.35,0],color=GOLD,stroke_width=4)
        material=Polygon([-5.8,-.35,0],[-.2,-.35,0],[-.2,-2,0],[-5.8,-2,0],stroke_width=0,fill_color='#15384b',fill_opacity=.8)
        stripes=VGroup(*[Line([x,-1.9,0],[x+.75,-.45,0],color='#5d95a9',stroke_opacity=.16,stroke_width=1) for x in np.linspace(-5.65,-1.05,10)])
        density=ValueTracker(.55)
        points=np.array([[x,.28] for x in np.linspace(-5.3,-.65,8)])
        arrows=always_redraw(lambda:field_arrows(points,np.tile([0.,density.get_value()],(len(points),1)),max_length=1.55,color=CYAN,reference=.35,stroke_width=3.1))
        charge_marks=VGroup(*[Text('+',font='Arial',font_size=21,color=GOLD).move_to([x,-.35,0]) for x in np.linspace(-5.5,-.5,12)])
        slabel=tex(r'\rho_s',size=36,color=GOLD).move_to([-4.9,.17,0])
        inlabel=ar('داخل الموصل',size=22).move_to([-4.75,-1.5,0])
        outlabel=ar('الوسط الخارجي',size=22).move_to([-4.5,2.12,0])
        self.play(FadeIn(material),Create(stripes),Create(surface),LaggedStart(*[FadeIn(q,scale=.4) for q in charge_marks],lag_ratio=.04),FadeIn(slabel),FadeIn(inlabel),FadeIn(outlabel),run_time=2)
        self.play(FadeIn(arrows),density.animate.set_value(1),run_time=2)

        # Thin cylindrical Gaussian pillbox shown as two ellipses and sidewalls.
        top=Ellipse(width=2.3,height=.55,color=WHITE,stroke_width=2.4).move_to([-2.8,.65,0])
        bottom=Ellipse(width=2.3,height=.55,color=WHITE,stroke_width=2.4).move_to([-2.8,-1.03,0])
        sides=VGroup(Line(top.get_left(),bottom.get_left(),color=WHITE,stroke_width=2),Line(top.get_right(),bottom.get_right(),color=WHITE,stroke_width=2))
        pill=VGroup(top,bottom,sides)
        patch=FluxPatch(width=1.5,height=.38,normal=(0,1,0)).scale(.75).move_to([-2.8,.67,0])
        patch.set_opacity(.5)
        area=tex(r'A',size=33,color=WHITE).move_to([-2.8,.9,0])
        self.play(Succession(FadeOut(c1),FadeIn(c2)),Create(top),Create(bottom),Create(sides),run_time=1.6)
        self.play(FadeIn(patch),FadeIn(area),run_time=.8)
        self.play(pill.animate.stretch(.65,1,about_point=[-2.8,-.35,0]),FadeOut(patch),FadeOut(area),run_time=1.5)
        self.play(Succession(FadeOut(c2),FadeIn(c3)),run_time=.7)

        # Charge on the enclosed patch and the displacement-flux boundary law.
        qeq=tex(r'Q_{\rm enc}=\rho_s A',size=37,color=GOLD,width=4.3).move_to([3.15,1.6,0])
        flux=tex(r'D_{2n}A-D_{1n}A=\rho_s A',size=36,color=WHITE,width=5.2).move_to([3.1,.6,0])
        boundary=tex(r'D_{2n}-D_{1n}=\rho_s',size=39,color=WHITE,width=5).move_to([3.1,-.35,0])
        inside=tex(r'D_{1n}=0',size=36,color=CYAN).move_to([3.1,-1.28,0])
        self.play(Write(qeq),run_time=1.5)
        self.play(FadeIn(flux,shift=UP*.12),run_time=1.5)
        self.play(FadeIn(boundary,shift=UP*.1),run_time=1.3)
        self.play(Circumscribe(boundary,color=GOLD,fade_out=True),FadeIn(inside),run_time=1.2)
        self.play(FadeOut(qeq),FadeOut(flux),FadeOut(boundary),FadeOut(inside),Succession(FadeOut(c3),FadeIn(c4)),run_time=1)

        # The equality remains signed: reversing rho reverses the normal field.
        d_eq=tex(r'D_{2n}=\rho_s',size=43,color=WHITE).move_to([3.15,1.45,0])
        e_eq=tex(r'\varepsilon E_n=\rho_s',size=42,color=CYAN).move_to([3.15,.35,0])
        result=tex(r'E_n=\frac{\rho_s}{\varepsilon}',size=50,color=GOLD).move_to([3.15,-.95,0])
        self.play(FadeIn(d_eq,shift=UP*.1),run_time=1)
        self.play(FadeIn(e_eq,shift=UP*.1),run_time=1)
        self.play(FadeIn(result,shift=UP*.1),run_time=1)
        emphasize(self,result,color=GOLD,run_time=.8)
        self.play(density.animate.set_value(.25),run_time=1.5)
        self.play(density.animate.set_value(1.0),run_time=1.8)
        self.play(FadeOut(d_eq),FadeOut(e_eq),FadeOut(result),Succession(FadeOut(c4),FadeIn(c5)),run_time=1)
        vacuum=tex(r'E_n=\frac{\rho_s}{\varepsilon_0}',size=44,color=CYAN,width=4.3).move_to([3.15,.95,0])
        medium=tex(r'E_n=\frac{\rho_s}{\varepsilon}',size=44,color=GOLD,width=4.3).move_to([3.15,-.85,0])
        vacuum_label=ar('في الفراغ',size=23,color=CYAN).move_to([3.15,1.95,0])
        medium_label=ar('في وسط عازل',size=23,color=GOLD).move_to([3.15,.1,0])
        self.play(FadeIn(vacuum_label),Write(vacuum),run_time=1.3)
        self.play(FadeIn(medium_label),Write(medium),run_time=1.3)
        self.play(Indicate(vacuum,color=CYAN),Indicate(medium,color=GOLD),run_time=1)
        self.wait(1)

if __name__ == '__main__':
    render(NormalBoundary,filename='scene_07_normal_field',preview=True)
