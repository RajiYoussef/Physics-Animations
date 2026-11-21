from dataclasses import dataclass
import numpy as np
from manim import *
from settings import BACKGROUND, CYAN, GOLD, WHITE, render
from support import ar, caption_panel
from tools import field_arrows, emphasize
from math_type import tex
from hbar_character import hbar_character
from raji_sci.physics.electrostatics_logic import point_charge_field, point_charge_potential
from raji_sci.physics.field_visuals import ScalarFieldImage, polyline
from raji_sci.em.field_lines import trace_field_line
from raji_sci.presentation.layout import frame_violations


@dataclass(frozen=True)
class SphereModel:
    radius: float = 1.2
    kq: float = 1.0

    def potential(self, r):
        return self.kq / max(abs(float(r)), self.radius)

    def field(self, r):
        r = abs(float(r))
        return 0.0 if r < self.radius else self.kq / r**2

    def field_points(self, points):
        p = np.asarray(points, dtype=float)
        values = point_charge_field([[0, 0, self.kq]], p, k=1)
        values[np.linalg.norm(p, axis=1) <= self.radius] = 0
        return values


def validate_physics(model):
    a=model.radius
    assert model.field(a*.5)==0
    assert np.isclose(model.potential(a*.5),model.potential(a))
    assert np.isclose(model.potential(a),model.potential(a*(1+1e-8)),rtol=1e-7)
    for r in (a*1.01,a*2,a*3):
        assert np.isclose(model.field(r),model.kq/r**2)
        assert np.isclose(model.potential(r),model.kq/r)
    sample=np.array([[a*.5,0],[a*2,0]])
    assert np.allclose(model.field_points(sample),[[0,0],[model.field(a*2),0]])


def switch(old,new):
    return Succession(FadeOut(old,run_time=.25),FadeIn(new,run_time=.25))


def charged_sphere(center, radius):
    layers=VGroup()
    for i in range(16):
        r=radius*(1-i/19)
        shade=interpolate_color(ManimColor('#071923'),ManimColor('#194c60'),i/22)
        layer=Circle(radius=r,stroke_width=0,fill_color=shade,fill_opacity=.30).move_to(center+np.array([-.025*i,.020*i,0]))
        layers.add(layer)
    outline=Circle(radius=radius,stroke_color='#a4d9e5',stroke_width=2.2).move_to(center)
    ellipse1=Ellipse(width=radius*1.85,height=radius*.6,color=CYAN,stroke_width=1,stroke_opacity=.26).move_to(center)
    ellipse2=Ellipse(width=radius*.58,height=radius*1.95,color=CYAN,stroke_width=1,stroke_opacity=.20).move_to(center)
    sites=VGroup(*[Text('+',font='Arial',font_size=19,color=GOLD).move_to(center+radius*np.array([np.cos(t),np.sin(t),0])) for t in np.linspace(0,TAU,20,endpoint=False)])
    return VGroup(layers,ellipse1,ellipse2,outline,sites)


class ConductingSphere(MovingCameraScene):
    def construct(self):
        model=SphereModel();validate_physics(model)
        self.camera.background_color=BACKGROUND
        title=ar('مثال: موصل كروي مشحون',size=35).move_to([0,3.43,0])
        box,c1=caption_panel('كرة موصلة نصف قطرها معلوم وتحمل شحنة كلية على سطحها.')
        _,c2=caption_panel('نحدد المجال باستخدام التناظر الكروي وقانون غاوس.')
        _,c3=caption_panel('داخل الموصل ينعدم المجال، وخارجه يتناقص مع مربع المسافة.')
        _,c4=caption_panel('خارج الكرة، الجهد هو جهد شحنة نقطية في المركز.')
        _,c5=caption_panel('يبقى الجهد ثابتًا داخل الموصل ويساوي جهد سطحه.')
        _,c6=caption_panel('يمكن أيضًا حل معادلة لابلاس باستخدام جهد السطح شرطًا حدّيًا.')
        if frame_violations([title,box,c1,c2,c3,c4,c5,c6],margin=.08):
            raise ValueError('Text outside the safe frame')
        self.add(title,box)
        mascot=hbar_character(.72).move_to([5.95,2.58,0])
        self.play(FadeIn(c1),FadeIn(mascot,shift=LEFT*.2),run_time=.7)
        center=np.array([-3.45,.05,0]);R=1.45
        sphere=charged_sphere(center,R)
        radius_line=Arrow(center,center+np.array([R*.86,-R*.51,0]),buff=0,color=WHITE,stroke_width=2.5)
        a_label=tex('a',size=32,color=WHITE).next_to(radius_line,DOWN,buff=.1)
        q_label=tex('q>0',size=36,color=GOLD).move_to(center+UP*.15)
        self.play(GrowFromCenter(sphere),GrowArrow(radius_line),FadeIn(a_label),Write(q_label),run_time=2.1)
        scan=Circle(radius=R*.92,color=CYAN,stroke_width=3,stroke_opacity=.7).move_to(center)
        self.play(Create(scan),scan.animate.scale(1.11).set_opacity(0),run_time=1.3)

        # Two Gaussian radii demonstrate the enclosed-charge cases.
        rtracker=ValueTracker(.65)
        gaussian=always_redraw(lambda: DashedVMobject(Circle(radius=R*rtracker.get_value()/model.radius,color=WHITE,stroke_width=2).move_to(center),num_dashes=48))
        marker=always_redraw(lambda: Dot(center+RIGHT*(R*rtracker.get_value()/model.radius),radius=.07,color=WHITE))
        rlabel=tex('r',size=30,color=WHITE).move_to([-1.0,1.8,0])
        inside=tex(r'Q_{\rm enc}=0',size=42,color=CYAN,width=4.5).move_to([3.0,1.4,0])
        e0=tex(r'\mathbf{E}=0\quad(r<a)',size=41,color=CYAN,width=4.9).move_to([3.0,.15,0])
        self.play(FadeOut(radius_line),FadeOut(a_label),FadeOut(q_label),FadeIn(gaussian),FadeIn(marker),FadeIn(rlabel),switch(c1,c2),run_time=1.1)
        self.play(Write(inside),FadeIn(e0,shift=UP*.1),run_time=1.5)
        self.play(rtracker.animate.set_value(.95),run_time=1.5)
        self.play(FadeOut(inside),FadeOut(e0),rtracker.animate.set_value(1.65),run_time=1.5)
        outside=tex(r'Q_{\rm enc}=q',size=42,color=GOLD,width=4.8).move_to([3.0,1.45,0])
        gauss=tex(r'E_r(4\pi r^2)=\frac{q}{\varepsilon_0}',size=39,color=WHITE,width=5.2).move_to([3.0,.3,0])
        self.play(FadeIn(outside),Write(gauss),run_time=1.8)
        rpts=np.array([[r*np.cos(t),r*np.sin(t)] for r in [1.35,2.0,2.7] for t in np.linspace(0,TAU,16,endpoint=False)])
        # Field points are in physical coordinates and are mapped to the diagram.
        # Discard arrows that would intrude into the equation panel or title.
        world=np.array([[center[0]+p[0]*R/model.radius,center[1]+p[1]*R/model.radius] for p in rpts])
        keep=(world[:,0]<-.4)&(world[:,0]>-6.8)&(world[:,1]>-2.5)&(world[:,1]<2.5)
        arrows=field_arrows(world[keep],model.field_points(rpts[keep]),max_length=.46,color=CYAN,reference=.12,stroke_width=2.5)
        rays=VGroup()
        for theta in np.linspace(PI/2,3*PI/2,9):
            seed=np.array([1.32*np.cos(theta),1.32*np.sin(theta)])
            ray=trace_field_line(lambda p: point_charge_field([[0,0,model.kq]],np.asarray([p]),k=1)[0],
                                 seed,step=.055,steps=13,direction=1)
            world_ray=np.column_stack((center[0]+ray[:,0]*R/model.radius,center[1]+ray[:,1]*R/model.radius))
            rays.add(polyline(world_ray,color=CYAN,stroke_width=1.8,smooth=False))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.018),
                  LaggedStart(*[Create(ray) for ray in rays],lag_ratio=.04),run_time=2)
        self.play(*[ShowPassingFlash(ray.copy().set_stroke(width=3),time_width=.35) for ray in rays],run_time=1.2)
        er=tex(r'\mathbf{E}=E_r\hat{\mathbf{r}},\quad E_r=\frac{q}{4\pi\varepsilon_0r^2}',size=37,color=GOLD,width=5.3).move_to([3.0,-1.2,0])
        self.play(FadeIn(er,shift=UP*.1),switch(c2,c3),run_time=1.2)
        emphasize(self,er,color=GOLD,run_time=.8)

        # A moving probe links physical position and the field graph.
        self.play(FadeOut(outside),FadeOut(gauss),FadeOut(er),FadeOut(gaussian),FadeOut(marker),FadeOut(rlabel),FadeOut(arrows),FadeOut(rays),run_time=.9)
        axes=Axes(x_range=[0,3.6,1],y_range=[0,1.0,.5],x_length=4.7,y_length=2.5,tips=False,
                  axis_config={'color':'#8aa5b4','stroke_width':1.4,'include_ticks':False}).move_to([3.0,-.15,0])
        xlabel=tex('r',size=27,color=WHITE).next_to(axes.x_axis,RIGHT,buff=.1)
        ylabel=tex('E_r',size=27,color=CYAN).next_to(axes.y_axis,UP,buff=.1)
        a=model.radius
        ein=Line(axes.c2p(0,0),axes.c2p(a,0),color=CYAN,stroke_width=4)
        eout=axes.plot(lambda x:model.field(x),x_range=[a,3.5],color=CYAN,stroke_width=4,use_smoothing=False)
        jump=DashedLine(axes.c2p(a,0),axes.c2p(a,model.kq/a**2),color=GOLD,stroke_width=2)
        alabel=tex('a',size=27,color=GOLD).next_to(axes.c2p(a,0),DOWN,buff=.13)
        probe_r=ValueTracker(.15)
        visual_probe=always_redraw(lambda:Dot(center+RIGHT*R*probe_r.get_value()/a,radius=.085,color=GOLD))
        graph_probe=always_redraw(lambda:Dot(axes.c2p(probe_r.get_value(),model.field(probe_r.get_value())),radius=.075,color=GOLD))
        self.play(Create(axes),FadeIn(xlabel),FadeIn(ylabel),Create(ein),Create(jump),Create(eout),FadeIn(alabel),FadeIn(visual_probe),FadeIn(graph_probe),run_time=2.1)
        self.play(probe_r.animate.set_value(3.05),run_time=4.5,rate_func=linear)
        self.play(Indicate(eout,color=CYAN,scale_factor=1.02),run_time=.7)

        # Potential map uses the same piecewise model, continuous across the boundary.
        self.play(FadeOut(axes),FadeOut(xlabel),FadeOut(ylabel),FadeOut(ein),FadeOut(jump),FadeOut(eout),FadeOut(alabel),FadeOut(visual_probe),FadeOut(graph_probe),switch(c3,c4),run_time=1)
        xs=np.linspace(-2.8,2.8,120)*model.radius/R
        ys=np.linspace(-2.2,2.2,96)*model.radius/R
        X,Y=np.meshgrid(xs,ys)
        rr=np.sqrt(X*X+Y*Y)
        values=model.kq/np.maximum(rr,model.radius)
        # Verify the outside potential against the supplied library's point-charge solver.
        sample=np.array([[2.0,0],[0,2.4]])
        assert np.allclose(point_charge_potential([[0,0,model.kq]],sample,k=1),[model.potential(2),model.potential(2.4)])
        heat=ScalarFieldImage(values,width=5.6,height=4.4,center=(-3.45,0,0),vmax=1.1,positive='#227b9d',zero='#03080e',opacity=.75)
        heat_outline=Circle(radius=R,color=GOLD,stroke_width=2).move_to(center)
        self.play(FadeOut(sphere),FadeIn(heat),Create(heat_outline),run_time=1.8)
        veq=tex(r'V(r)=\frac{q}{4\pi\varepsilon_0r}',size=43,color=WHITE,width=5.2).move_to([3.05,1.35,0])
        cond=tex(r'r\geq a',size=30,color=CYAN).move_to([3.05,.45,0])
        self.play(Write(veq),FadeIn(cond),run_time=1.8)
        self.play(FadeOut(veq),FadeOut(cond),switch(c4,c5),run_time=.8)
        vinside=tex(r'V(r)=\frac{q}{4\pi\varepsilon_0a}',size=43,color=GOLD,width=5.4).move_to([3.05,1.35,0])
        insidecond=tex(r'r\leq a',size=30,color=CYAN).move_to([3.05,.45,0])
        self.play(Write(vinside),FadeIn(insidecond),run_time=1.7)
        vaxes=Axes(x_range=[0,3.6,1],y_range=[0,1.05,.5],x_length=4.5,y_length=1.55,tips=False,
                   axis_config={'color':'#8aa5b4','stroke_width':1.2,'include_ticks':False}).move_to([3,-1.15,0])
        vleft=Line(vaxes.c2p(0,model.potential(0)),vaxes.c2p(a,model.potential(a)),color=GOLD,stroke_width=3)
        vright=vaxes.plot(lambda r:model.potential(r),x_range=[a,3.5],color=GOLD,stroke_width=3,use_smoothing=False)
        vr=tex('r',size=22,color=WHITE).next_to(vaxes.x_axis,RIGHT,buff=.08)
        vv=tex('V',size=22,color=GOLD).next_to(vaxes.y_axis,UP,buff=.08)
        self.play(Create(vaxes),Create(vleft),Create(vright),FadeIn(vr),FadeIn(vv),run_time=1.6)
        self.play(Circumscribe(vinside,color=GOLD,fade_out=True),run_time=.9)

        # Close with the alternative boundary-value method mentioned in the source.
        self.play(FadeOut(heat),FadeOut(heat_outline),FadeOut(vinside),FadeOut(insidecond),FadeOut(vaxes),FadeOut(vleft),FadeOut(vright),FadeOut(vr),FadeOut(vv),switch(c5,c6),run_time=1)
        self.play(FadeIn(sphere),run_time=1)
        laplace=tex(r'\nabla^2 V=0',size=45,color=CYAN).move_to([3.0,1.45,0])
        boundary=tex(r'V(a)=\frac{q}{4\pi\varepsilon_0a}',size=40,color=GOLD,width=5).move_to([3.0,.3,0])
        infinity=tex(r'V(\infty)=0',size=38,color=WHITE).move_to([3.0,-.8,0])
        self.play(Write(laplace),run_time=1.1)
        self.play(FadeIn(boundary,shift=UP*.1),FadeIn(infinity,shift=UP*.1),run_time=1.3)
        emphasize(self,boundary,color=GOLD,run_time=.8)
        self.wait(1)


if __name__ == '__main__':
    render(ConductingSphere,filename='scene_10_conducting_sphere',preview=True)
