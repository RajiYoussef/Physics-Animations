from dataclasses import dataclass
import numpy as np
from manim import *
from settings import BACKGROUND,CYAN,GOLD,WHITE,render
from support import ar,caption_panel
from tools import field_arrows,emphasize
from math_type import tex
from hbar_character import hbar_character
from raji_sci.physics.field_visuals import ScalarFieldImage,polyline
from raji_sci.physics.electrostatics_logic import contour_paths
from raji_sci.em.field_lines import trace_field_line
from raji_sci.presentation.layout import frame_violations


@dataclass(frozen=True)
class ConductingCylinder:
    radius: float=1.0
    applied_field: float=1.0

    def potential(self,points):
        p=np.asarray(points,dtype=float)
        x,y=p[...,0],p[...,1]
        r2=x*x+y*y
        safe=np.maximum(r2,1e-14)
        v=-self.applied_field*x*(1-self.radius**2/safe)
        return np.where(r2<=self.radius**2,0.0,v)

    def field(self,points):
        p=np.asarray(points,dtype=float)
        x,y=p[...,0],p[...,1]
        r2=x*x+y*y
        den=np.maximum(r2*r2,1e-14)
        ex=self.applied_field*(1+self.radius**2*(x*x-y*y)/den)
        ey=self.applied_field*(2*self.radius**2*x*y/den)
        return np.where((r2<=self.radius**2)[...,None],0.0,np.stack((ex,ey),axis=-1))


def validate_model(model):
    assert np.allclose(model.field([[0,0],[.2,.3]]),0)
    for angle in np.linspace(0,TAU,20,endpoint=False):
        n=np.array([np.cos(angle),np.sin(angle)])
        t=np.array([-n[1],n[0]])
        assert abs(model.potential(n*model.radius))<1e-12
        E=model.field(n*model.radius*(1+1e-6))
        assert abs(E@t)<1e-5
        assert np.isclose(E@n,2*model.applied_field*np.cos(angle),atol=1e-5)
    for p in (np.array([1.4,.6]),np.array([-1.6,.8]),np.array([.3,-1.8])):
        d=1e-5
        grad=np.array([(model.potential(p+np.eye(2)[k]*d)-model.potential(p-np.eye(2)[k]*d))/(2*d) for k in range(2)])
        assert np.allclose(model.field(p),-grad,atol=1e-8)


def switch(old,new):
    return Succession(FadeOut(old,run_time=.25),FadeIn(new,run_time=.25))


def conductor(center,radius):
    body=VGroup()
    for i in range(14):
        shade=interpolate_color(ManimColor('#061724'),ManimColor('#1c566a'),i/21)
        body.add(Circle(radius=radius*(1-i/22),stroke_width=0,fill_color=shade,fill_opacity=.32).move_to(center+[-.025*i,.019*i,0]))
    body.add(Circle(radius=radius,stroke_color='#a8dce8',stroke_width=2.4).move_to(center))
    return body


class ChapterSummary(MovingCameraScene):
    def construct(self):
        model=ConductingCylinder();validate_model(model)
        self.camera.background_color=BACKGROUND
        title=ar('الموصل المثالي في الاتزان',size=35).move_to([0,3.43,0])
        panel,c1=caption_panel('يعيد الموصل الأسطواني توزيع شحناته عند تطبيق مجال خارجي.')
        _,c2=caption_panel('عند الاتزان، ينعدم المجال والشحنة الحجمية الصافية داخل الموصل.')
        _,c3=caption_panel('سطح الموصل متساوي الجهد، والمجال خارجه عمودي عليه.')
        _,c4=caption_panel('ترتبط المركبة العمودية بكثافة الشحنة السطحية وسماحية الوسط.')
        _,c5=caption_panel('يستخدم جهد الموصل شرطًا حدّيًا لإيجاد الجهد والمجال حوله.')
        if frame_violations([title,panel,c1,c2,c3,c4,c5],margin=.08):
            raise ValueError('Caption exceeds frame')
        self.add(title,panel)
        guide=hbar_character(.72).move_to([5.95,2.6,0])
        self.play(FadeIn(c1),FadeIn(guide,shift=LEFT*.15),run_time=.8)
        center=np.array([-2.55,0,0]);scale=1.35
        to_world=lambda p:center+np.array([p[0]*scale,p[1]*scale,0])
        sphere=conductor(center,scale)
        self.play(GrowFromCenter(sphere),run_time=1.7)

        # Begin with the applied field and show mobile electrons moving against it.
        uniform_points=np.array([[x,y] for x in [-5.8,-4.9,-.1,.8] for y in [-1.5,-.6,.3,1.2]])
        uniform=field_arrows(uniform_points,np.tile([1.,0.],(len(uniform_points),1)),max_length=.72,color=CYAN,reference=.3)
        ext=tex(r'\mathbf{E}_{\rm ext}',size=33,color=CYAN).move_to([3.3,1.8,0])
        self.play(LaggedStart(*[GrowArrow(a) for a in uniform],lag_ratio=.025),FadeIn(ext),run_time=1.7)
        electrons=VGroup(*[Dot(center+np.array([x,y,0]),radius=.055,color=CYAN) for x,y in [(.45,-.55),(.3,.48),(.7,.0),(.1,-.15),(.65,.75)]])
        self.play(FadeIn(electrons),run_time=.5)
        self.play(electrons.animate.shift(LEFT*.8),run_time=1.8,rate_func=smooth)
        signs=VGroup()
        for angle in np.linspace(0,TAU,28,endpoint=False):
            component=np.cos(angle)
            if abs(component)<.16:continue
            pos=to_world([np.cos(angle),np.sin(angle)])
            col=GOLD if component>0 else CYAN
            symbol='+' if component>0 else '−'
            q=Text(symbol,font='Arial',font_size=22,color=col).move_to(pos)
            q.set_opacity(.5+.5*abs(component))
            signs.add(q)
        self.play(FadeOut(electrons),LaggedStart(*[FadeIn(q,scale=.4) for q in signs],lag_ratio=.035),run_time=2)

        # Raji RK4 traces the field of the conductor-plus-applied-field solution.
        rays=VGroup()
        for y in [-1.45,-1.05,-.68,-.37,.37,.68,1.05,1.45]:
            pts=trace_field_line(model.field,[-2.55,y],step=.035,steps=170,
                                 bounds=[[-2.58,2.58],[-1.63,1.63]])
            if len(pts)>2:
                rays.add(polyline(np.array([to_world(p)[:2] for p in pts]),color=CYAN,stroke_width=1.8,smooth=False))
        for angle in np.linspace(-1.28,1.28,7):
            seed=np.array([1.025*np.cos(angle),1.025*np.sin(angle)])
            pts=trace_field_line(model.field,seed,step=.035,steps=170,
                                 bounds=[[-2.58,2.58],[-1.63,1.63]])
            if len(pts)>2:
                rays.add(polyline(np.array([to_world(p)[:2] for p in pts]),color=CYAN,stroke_width=1.8,smooth=False))
        sample=np.array([[x,y] for x in np.linspace(-2.4,2.4,10) for y in [-1.35,-.8,-.25,.25,.8,1.35]])
        sample=sample[np.linalg.norm(sample,axis=1)>1.15]
        world=np.array([to_world(p)[:2] for p in sample])
        vectors=field_arrows(world,model.field(sample),max_length=.39,color=CYAN,reference=.7,stroke_width=1.8)
        self.play(FadeOut(uniform),LaggedStart(*[Create(ray) for ray in rays],lag_ratio=.09),
                  LaggedStart(*[GrowArrow(a) for a in vectors],lag_ratio=.008),run_time=2.8)
        self.play(*[ShowPassingFlash(ray.copy().set_stroke(width=3.3),time_width=.22) for ray in rays],run_time=1.8)

        # A probe crosses the interior as the internal conditions appear.
        self.play(FadeOut(ext),switch(c1,c2),run_time=.7)
        probe=Dot(center+LEFT*.95,radius=.08,color=WHITE)
        route=polyline(np.array([[center[0]-.95,0],[center[0]-.25,.25],[center[0]+.45,-.15],[center[0]+.95,0]]),color=WHITE,stroke_width=2)
        trail=TracedPath(probe.get_center,stroke_color=WHITE,stroke_width=2.5,dissipating_time=1.2)
        zeroe=tex(r'\mathbf{E}=0',size=49,color=CYAN).move_to([3.3,1.1,0])
        zerorho=tex(r'\rho=0',size=45,color=GOLD).move_to([3.3,-.05,0])
        self.add(trail,probe)
        self.play(MoveAlongPath(probe,route),FadeIn(zeroe),run_time=3.0,rate_func=linear)
        self.play(FadeIn(zerorho,shift=UP*.1),run_time=1)
        self.play(Circumscribe(zeroe,color=CYAN,fade_out=True),Indicate(zerorho,color=GOLD),run_time=1)
        self.play(FadeOut(probe),FadeOut(trail),FadeOut(zeroe),FadeOut(zerorho),switch(c2,c3),run_time=.9)

        # Field direction at a surface point: the tangential component vanishes.
        point=to_world([1,0]);normal=Arrow(point,point+RIGHT*.82,buff=0,color=WHITE,stroke_width=4)
        tangent=DashedLine(point+UP*.65,point+DOWN*.65,color=GOLD,stroke_width=2,dash_length=.11)
        nlabel=tex(r'\hat{\mathbf{n}}',size=30,color=WHITE).next_to(normal,UP,buff=.1)
        et=tex(r'E_t=0',size=44,color=GOLD).move_to([3.35,1.3,0])
        equip=tex(r'V=\mathrm{constant}',size=41,color=WHITE,width=4.8).move_to([3.35,.15,0])
        self.play(GrowArrow(normal),Create(tangent),FadeIn(nlabel),Write(et),run_time=1.5)
        self.play(Write(equip),run_time=1.2)
        self.play(Indicate(tangent,color=GOLD),Indicate(sphere,color=CYAN,scale_factor=1.01),run_time=.8)
        self.play(FadeOut(equip),switch(c3,c4),run_time=.7)
        en=tex(r'E_n=\frac{\rho_s}{\varepsilon}',size=46,color=GOLD).move_to([3.35,-.1,0])
        self.play(FadeIn(en,shift=UP*.1),run_time=1.1)
        emphasize(self,en,color=GOLD,run_time=.8)

        # A potential map and calculated contours lead into the boundary-value method.
        self.play(FadeOut(et),FadeOut(en),FadeOut(normal),FadeOut(tangent),FadeOut(nlabel),
                  FadeOut(rays),FadeOut(vectors),switch(c4,c5),run_time=1)
        x=np.linspace(-2.6,2.6,145);y=np.linspace(-1.63,1.63,91)
        X,Y=np.meshgrid(x,y);points=np.stack((X,Y),axis=-1)
        V=model.potential(points)
        heat=ScalarFieldImage(V,width=(x[-1]-x[0])*scale,height=(y[-1]-y[0])*scale,
                              center=tuple(center),vmax=2.6,positive='#e9a35c',negative='#247cba',zero='#050a11',opacity=.72)
        heat.set_z_index(-2)
        self.play(FadeIn(heat),run_time=1.4)
        masked=V.copy();masked[X*X+Y*Y<=model.radius**2]=np.nan
        contours=VGroup()
        for level in [-2.0,-1.4,-.8,-.35,.35,.8,1.4,2.0]:
            for path in contour_paths(X,Y,masked,level):
                contours.add(polyline(np.array([to_world(p)[:2] for p in path]),
                                      color=CYAN if level<0 else GOLD,stroke_width=1.5,smooth=False))
        self.play(LaggedStart(*[Create(c) for c in contours],lag_ratio=.04),run_time=2.4)
        laplace=tex(r'\nabla^2V=0',size=44,color=CYAN).move_to([3.35,1.35,0])
        surface=tex(r'V\vert_S=0',size=43,color=GOLD).move_to([3.35,.2,0])
        relation=tex(r'\mathbf{E}=-\nabla V',size=40,color=WHITE,width=4.8).move_to([3.35,-.95,0])
        self.play(Write(laplace),FadeIn(surface,shift=UP*.1),run_time=1.7)
        self.play(FadeIn(relation,shift=UP*.1),run_time=1.2)
        self.play(Circumscribe(relation,color=CYAN,fade_out=True),guide.animate.shift(LEFT*.15),run_time=1)
        self.wait(1.2)


if __name__ == '__main__':
    render(ChapterSummary,filename='scene_13_chapter_summary',preview=True)
