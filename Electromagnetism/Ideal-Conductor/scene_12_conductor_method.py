from dataclasses import dataclass
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from manim import *
from settings import BACKGROUND,CYAN,GOLD,WHITE,render
from support import ar,caption_panel
from tools import field_arrows,emphasize
from math_type import tex
from hbar_character import hbar_character
from raji_sci.physics.electrostatics_logic import poisson_sor,negative_gradient,contour_paths
from raji_sci.physics.field_visuals import ScalarFieldImage,polyline
from raji_sci.em.field_lines import trace_field_line
from raji_sci.presentation.layout import frame_violations


@dataclass(frozen=True)
class ConductorProblem:
    n: int=65
    center_x: float=-.25
    radius: float=.28
    inner_voltage: float=1.0

    def solve(self):
        coords=np.linspace(-1,1,self.n)
        X,Y=np.meshgrid(coords,coords)
        h=coords[1]-coords[0]
        metal=(X-self.center_x)**2+Y**2<=self.radius**2
        fixed=metal.copy()
        fixed[[0,-1],:]=True
        fixed[:,[0,-1]]=True
        fixed_values=np.where(metal,self.inner_voltage,0.0)
        V,info=poisson_sor(np.zeros_like(X),h,fixed,fixed_values,omega=1.75,tol=1e-8,snapshot_every=10)
        if not info['converged']:
            raise RuntimeError('Laplace solver did not converge')
        residual=(V[2:,1:-1]+V[:-2,1:-1]+V[1:-1,2:]+V[1:-1,:-2]-4*V[1:-1,1:-1])/(h*h)
        if np.max(np.abs(residual[~fixed[1:-1,1:-1]])) > 1e-4:
            raise RuntimeError('Discrete Laplace residual exceeds tolerance')
        if not np.allclose(V[fixed],fixed_values[fixed]) or V.min() < -1e-7 or V.max() > self.inner_voltage+1e-7:
            raise RuntimeError('The potential violates the conductor boundary conditions')
        Ex,Ey=negative_gradient(V,h,h)
        fx=RegularGridInterpolator((coords,coords),Ex,bounds_error=False,fill_value=0)
        fy=RegularGridInterpolator((coords,coords),Ey,bounds_error=False,fill_value=0)
        return coords,X,Y,h,metal,V,info,fx,fy


def switch(old,new):
    return Succession(FadeOut(old,run_time=.25),FadeIn(new,run_time=.25))


class ConductorsSolutionMethod(MovingCameraScene):
    def construct(self):
        model=ConductorProblem()
        coords,X,Y,h,metal,V,info,fx,fy=model.solve()
        self.camera.background_color=BACKGROUND
        title=ar('طريقة حل مسائل الموصلات',size=35).move_to([0,3.43,0])
        panel,c1=caption_panel('نحدد الموصلات وجهودها، وهذه هي شروط الحدود.')
        _,c2=caption_panel('نحل معادلة لابلاس أو بواسون في المنطقة بين الموصلات.')
        _,c3=caption_panel('بعد إيجاد الجهد نحسب المجال الكهربائي من التدرج السالب.')
        _,c4=caption_panel('نحسب كثافة الشحنة السطحية من المركبة العمودية للمجال.')
        _,c5=caption_panel('هكذا نحصل على الجهد والمجال والشحنة من شروط المسألة.')
        if frame_violations([title,panel,c1,c2,c3,c4,c5],margin=.08):
            raise ValueError('Caption exceeds frame')
        self.add(title,panel)
        guide=hbar_character(.7).move_to([5.95,2.6,0])
        self.play(FadeIn(c1),FadeIn(guide,shift=LEFT*.15),run_time=.8)

        # Coordinate map from a two-dimensional cross-section into scene space.
        center=np.array([-3.25,-.05,0]);size=4.35;scale=size/2
        to_scene=lambda p: center+np.array([p[0]*scale,p[1]*scale,0])
        inner=to_scene([model.center_x,0]);rad=model.radius*scale
        back=Rectangle(width=size+.16,height=size+.16,stroke_color='#547a8b',stroke_width=5,
                       fill_color='#04101a',fill_opacity=1).move_to(center)
        back.set_z_index(-3)
        frame=Square(side_length=size,stroke_color=CYAN,stroke_width=4,fill_opacity=0).move_to(center)
        inset=Square(side_length=size-.11,stroke_color='#b8d9e0',stroke_width=1,stroke_opacity=.4).move_to(center)
        disc=Circle(radius=rad,stroke_color=GOLD,stroke_width=3,fill_color='#71451d',fill_opacity=1).move_to(inner)
        gleam=Arc(radius=rad*.78,start_angle=PI*.24,angle=PI*.42,color='#ffd994',stroke_width=2,stroke_opacity=.45).move_to(inner+[-.03,.03,0])
        ring=Circle(radius=rad*.77,stroke_color=GOLD,stroke_width=1,stroke_opacity=.3).move_to(inner)
        shape=VGroup(back,frame,inset,disc,gleam,ring)
        self.play(FadeIn(back,scale=.95),Create(frame),Create(inset),GrowFromCenter(disc),FadeIn(gleam),Create(ring),run_time=2.2)
        vinner=tex(r'V=V_c',size=38,color=GOLD).move_to([3,1.3,0])
        vouter=tex(r'V=0',size=38,color=CYAN).move_to([3,.2,0])
        connector1=polyline(np.array([vinner.get_left()[:2]+[-.15,0],[-.55,1.3],
                                      [inner[0]+rad*.707,inner[1]+rad*.707]]),color=GOLD,stroke_width=1.5,smooth=False)
        connector2=polyline(np.array([vouter.get_left()[:2]+[-.15,0],[-.55,.2],
                                      [center[0]+size/2,.2]]),color=CYAN,stroke_width=1.5,smooth=False)
        self.play(Write(vinner),Create(connector1),run_time=1.1)
        self.play(Write(vouter),Create(connector2),run_time=1.1)
        self.play(Indicate(disc,color=GOLD),Indicate(frame,color=CYAN),run_time=1)

        # Every displayed state is an actual solver iteration.
        self.play(FadeOut(connector1),FadeOut(connector2),FadeOut(vinner),FadeOut(vouter),switch(c1,c2),run_time=.8)
        snapshots=[a for _,a in info['snapshots']]
        if not np.array_equal(snapshots[-1],V): snapshots.append(V.copy())
        heat=ScalarFieldImage(snapshots[0],width=size,height=size,center=tuple(center),vmax=1,
                              positive='#b97d34',zero='#06111d',negative='#1b8ea5',opacity=.96)
        heat.set_z_index(-1)
        index=ValueTracker(0)
        def update_heat(m):
            idx=int(np.clip(round(index.get_value()),0,len(snapshots)-1))
            m.update_values(snapshots[idx])
        heat.add_updater(update_heat)
        self.play(FadeIn(heat),run_time=.9)
        laplace=tex(r'\nabla^2V=0',size=45,color=CYAN).move_to([3,1.55,0])
        poisson=tex(r'\nabla^2V=-\frac{\rho}{\varepsilon_0}',size=40,color=WHITE,width=5).move_to([3,.2,0])
        self.play(Write(laplace),FadeIn(poisson,shift=UP*.1),index.animate.set_value(len(snapshots)-1),run_time=4.6,rate_func=linear)
        heat.clear_updaters()
        heat.update_values(V)
        contours=VGroup()
        for level in [.15,.30,.45,.60,.75,.9]:
            for path in contour_paths(X,Y,V,level):
                pts=np.array([to_scene(p)[:2] for p in path])
                contours.add(polyline(pts,color='#e0c48e',stroke_width=1.5,smooth=False))
        self.play(LaggedStart(*[Create(c) for c in contours],lag_ratio=.12),run_time=2.1)
        self.play(Indicate(laplace,color=CYAN),run_time=.7)

        # Field samples and trajectories are derived from the calculated potential.
        self.play(FadeOut(laplace),FadeOut(poisson),switch(c2,c3),run_time=.8)
        candidates=np.array([[x,y] for x in np.linspace(-.9,.9,11) for y in np.linspace(-.9,.9,9)])
        keep=((candidates[:,0]-model.center_x)**2+candidates[:,1]**2>(model.radius+2*h)**2)
        sample=candidates[keep]
        lookup=np.column_stack((sample[:,1],sample[:,0]))
        vectors=np.column_stack((fx(lookup),fy(lookup)))
        world=np.array([to_scene(p)[:2] for p in sample])
        arrows=field_arrows(world,vectors,max_length=.30,color=CYAN,reference=1.7,stroke_width=2.0)
        eformula=tex(r'\mathbf{E}=-\nabla V',size=46,color=CYAN,width=5).move_to([3,1.2,0])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.012),Write(eformula),run_time=2.6)
        def field(p):
            return np.array([float(fx((p[1],p[0]))),float(fy((p[1],p[0])))])
        trails=VGroup()
        for theta in [0,.65,-.65,1.4,-1.4,2.25,3.2,4.15]:
            seed=np.array([model.center_x+(model.radius+2.2*h)*np.cos(theta),(model.radius+2.2*h)*np.sin(theta)])
            pts=trace_field_line(field,seed,step=.022,steps=150,bounds=[[-.98,.98],[-.98,.98]])
            if len(pts)>2:
                trails.add(polyline(np.array([to_scene(p)[:2] for p in pts]),color=CYAN,stroke_width=2,smooth=False))
        self.play(LaggedStart(*[Create(p) for p in trails],lag_ratio=.12),run_time=2)
        self.play(*[ShowPassingFlash(p.copy().set_stroke(width=3.2),time_width=.22) for p in trails],run_time=1.6)
        self.play(Indicate(eformula,color=CYAN),run_time=.7)

        # Evaluate normal field just outside the inner surface, then show its variation.
        self.play(FadeOut(eformula),FadeOut(arrows),FadeOut(trails),switch(c3,c4),run_time=1)
        theta=np.linspace(0,TAU,20,endpoint=False)
        sample_r=model.radius+2*h
        sxy=np.column_stack((model.center_x+sample_r*np.cos(theta),sample_r*np.sin(theta)))
        sample_yx=np.column_stack((sxy[:,1],sxy[:,0]))
        normal_values=fx(sample_yx)*np.cos(theta)+fy(sample_yx)*np.sin(theta)
        if not np.all(normal_values>0):
            raise RuntimeError('Unexpected normal-field sign at conductor surface')
        magnitudes=normal_values/normal_values.max()
        surface_marks=VGroup()
        for angle,mag in zip(theta,magnitudes):
            pos=inner+rad*np.array([np.cos(angle),np.sin(angle),0])
            glow=Dot(pos,radius=.075+.025*mag,color=GOLD,fill_opacity=.25+.55*mag)
            plus=Text('+',font='Arial',font_size=17,color=WHITE).move_to(pos)
            surface_marks.add(VGroup(glow,plus))
        self.play(LaggedStart(*[FadeIn(q,scale=.4) for q in surface_marks],lag_ratio=.04),run_time=2)
        angle=.65; pos=inner+rad*np.array([np.cos(angle),np.sin(angle),0]);nvec=np.array([np.cos(angle),np.sin(angle),0])
        normal=Arrow(pos,pos+nvec*.75,buff=0,color=WHITE,stroke_width=3)
        nlabel=tex(r'\hat{\mathbf{n}}',size=30,color=WHITE).next_to(normal,UR,buff=.08)
        self.play(GrowArrow(normal),FadeIn(nlabel),run_time=1)
        sigma=tex(r'\rho_s=\varepsilon_0\mathbf{E}\cdot\hat{\mathbf{n}}',size=43,color=GOLD,width=5.4).move_to([3,.9,0])
        vacuum=ar('في الفراغ',size=23,color=WHITE).move_to([3,-.05,0])
        self.play(Write(sigma),FadeIn(vacuum),run_time=1.8)
        self.play(Circumscribe(sigma,color=GOLD,fade_out=True),Indicate(surface_marks,color=GOLD,scale_factor=1.02),run_time=1.1)
        self.play(switch(c4,c5),run_time=.7)
        self.play(guide.animate.shift(LEFT*.16),run_time=.6)
        self.wait(1)


if __name__ == '__main__':
    render(ConductorsSolutionMethod,filename='scene_12_conductor_method',preview=True)
