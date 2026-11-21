import numpy as np
from manim import *
from settings import BACKGROUND, CYAN, GOLD, WHITE, render
from support import ar, caption_panel
from tools import field_arrows, emphasize
from raji_sci.physics.electrostatics_logic import point_charge_field
from raji_sci.physics.field_visuals import polyline


class ConductorEquilibrium(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        title = ar("الموصل في المجال الكهربائي", size=35).move_to([0,3.45,0])
        panel, cap1 = caption_panel("تولّد الشحنات المتجمعة على سطح الموصل مجالًا كهربائيًا.")
        _, cap2 = caption_panel("يعاكس المجال الناتج عن الشحنات المجال الخارجي داخل الموصل.")
        _, cap3 = caption_panel("تستمر إعادة التوزيع ما دام المجال المحصل داخل الموصل غير صفري.")
        _, cap4 = caption_panel("عند الاتزان تنعدم محصلة المجال الكهربائي داخل الموصل.")
        self.add(title,panel)
        self.play(FadeIn(cap1),run_time=.6)

        disk=Circle(radius=1.85, color="#839eae", stroke_width=2, fill_color="#101d24", fill_opacity=.45).move_to([-2.8,.0,0])
        surface_neg=VGroup(*[Text("−",font="Arial",font_size=28,color=CYAN).move_to([-2.8-1.8*np.cos(a),1.8*np.sin(a),0]) for a in np.linspace(-1.15,1.15,7)])
        surface_pos=VGroup(*[Text("+",font="Arial",font_size=25,color=GOLD).move_to([-2.8+1.8*np.cos(a),1.8*np.sin(a),0]) for a in np.linspace(-1.15,1.15,7)])
        self.play(Create(disk),LaggedStart(*[FadeIn(x,scale=.5) for x in surface_neg],lag_ratio=.08),LaggedStart(*[FadeIn(x,scale=.5) for x in surface_pos],lag_ratio=.08),run_time=2.3)
        charge_sources=np.array([[-4.6,y,-1.] for y in [-1.05,0,1.05]]+[[ -1.0,y,1.] for y in [-1.05,0,1.05]])
        pts=np.array([[x,y] for x in np.linspace(-4.0,-1.6,5) for y in [-.7,0,.7]])
        vec=point_charge_field(charge_sources,pts,softening=.35)
        induced=field_arrows(pts,vec,max_length=.7,color=GOLD,reference=.3,stroke_width=2.2)
        legend=ar("مجال الشحنات السطحية",size=24,color=GOLD).move_to([2.7,2.0,0])
        self.play(LaggedStart(*[GrowArrow(a) for a in induced],lag_ratio=.04),FadeIn(legend),run_time=2.3)
        self.wait(.6)

        # Move from the conductor to a vector addition at one interior point.
        self.play(FadeOut(cap1),FadeIn(cap2),disk.animate.scale(.78).move_to([-4.1,0,0]),
                  surface_neg.animate.scale(.78).move_to([-5.5,0,0]),surface_pos.animate.scale(.78).move_to([-2.7,0,0]),
                  FadeOut(induced),FadeOut(legend),run_time=1.5)
        probe=Dot([-4.1,0,0],radius=.085,color=WHITE)
        connector=polyline(np.array([[-4.1,0],[-2.5,-.5],[-1.2,-.5]]),color="#879baa",stroke_width=2,smooth=False)
        self.play(FadeIn(probe),Create(connector),run_time=1)
        ext_label=ar("المجال الخارجي",size=24,color=CYAN).move_to([2.1,1.55,0])
        induced_label=ar("مجال الشحنات",size=24,color=GOLD).move_to([2.1,.3,0])
        ext=Arrow([-.8,1.05,0],[3.3,1.05,0],buff=0,color=CYAN,stroke_width=6)
        induced_arrow=Arrow([3.3,-.2,0],[-.8,-.2,0],buff=0,color=GOLD,stroke_width=6)
        self.play(FadeIn(ext_label),GrowArrow(ext),run_time=1.5)
        self.play(FadeIn(induced_label),GrowArrow(induced_arrow),run_time=1.5)
        self.play(Indicate(probe,color=WHITE),run_time=.7)

        # Progressive cancellation, shown as a head-to-tail vector sum.
        self.play(FadeOut(cap2),FadeIn(cap3),FadeOut(connector),FadeOut(disk),FadeOut(surface_neg),FadeOut(surface_pos),FadeOut(probe),
                  FadeOut(ext_label),FadeOut(induced_label),FadeOut(ext),FadeOut(induced_arrow),run_time=1.2)
        base=np.array([-3.6,.65,0]); end=np.array([2.7,.65,0])
        external=Arrow(base,end,buff=0,color=CYAN,stroke_width=6)
        a=ValueTracker(.12)
        opposite=always_redraw(lambda: Arrow(end,end+LEFT*6.3*a.get_value(),buff=0,color=GOLD,stroke_width=6))
        result=always_redraw(lambda: Arrow(base,base+RIGHT*max(.025,6.3*(1-a.get_value())),buff=0,color=WHITE,stroke_width=5))
        row1=ar("المجال الخارجي",size=25,color=CYAN).move_to([0,1.35,0])
        row2=ar("مجال الشحنات السطحية",size=25,color=GOLD).move_to([0,.05,0])
        row3=ar("المجال المحصل داخل الموصل",size=25,color=WHITE).move_to([0,-1.65,0])
        result.move_to([0,-1.0,0])
        # Position the resultant independently of its changing length.
        result=always_redraw(lambda: Arrow([-3.6,-1,0],[-3.6+max(.025,6.3*(1-a.get_value())),-1,0],buff=0,color=WHITE,stroke_width=5))
        self.play(FadeIn(row1),GrowArrow(external),FadeIn(row2),FadeIn(opposite),FadeIn(row3),FadeIn(result),run_time=2)
        self.play(a.animate.set_value(1),run_time=6,rate_func=linear)
        self.play(FadeOut(cap3),FadeIn(cap4),run_time=1)
        zero=Text("E = 0",font="Arial",font_size=48,color=WHITE).move_to([0,-1.03,0])
        self.play(FadeOut(result),FadeIn(zero,scale=.7),run_time=1.2)
        emphasize(self,zero,color=CYAN,run_time=.8)

        # Return to the entire conductor while retaining the conclusion.
        self.play(FadeOut(external),FadeOut(opposite),FadeOut(row1),FadeOut(row2),FadeOut(row3),
                  zero.animate.scale(.8).move_to([0,2.1,0]),run_time=1.2)
        final=Circle(radius=1.7,stroke_color="#839eae",stroke_width=2,fill_color="#10202a",fill_opacity=.4)
        left=VGroup(*[Text("−",font="Arial",font_size=27,color=CYAN).move_to([-1.65*np.cos(a),1.65*np.sin(a),0]) for a in np.linspace(-1.2,1.2,7)])
        right=VGroup(*[Text("+",font="Arial",font_size=25,color=GOLD).move_to([1.65*np.cos(a),1.65*np.sin(a),0]) for a in np.linspace(-1.2,1.2,7)])
        outer_points=np.array([[x,y] for x in [-5,-3,-2,2,3,5] for y in [-.9,0,.9]])
        x, y = outer_points[:, 0], outer_points[:, 1]
        r2 = x*x + y*y
        outer_vectors = np.column_stack((1 - 1.7**2*(x*x-y*y)/r2**2, -2*1.7**2*x*y/r2**2))
        outer=field_arrows(outer_points,outer_vectors,max_length=.8,color=CYAN,reference=.3)
        self.play(Create(final),FadeIn(left),FadeIn(right),LaggedStart(*[GrowArrow(x) for x in outer],lag_ratio=.02),run_time=2)
        self.wait(1)


if __name__ == "__main__":
    render(ConductorEquilibrium, filename="scene_03_conductor_equilibrium", preview=True)

