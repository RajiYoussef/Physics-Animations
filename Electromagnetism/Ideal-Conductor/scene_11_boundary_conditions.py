from dataclasses import dataclass
import numpy as np
from manim import *
from settings import BACKGROUND,CYAN,GOLD,WHITE,render
from support import ar,caption_panel
from tools import field_arrows,emphasize
from math_type import tex
from hbar_character import hbar_character
from raji_sci.physics.electrostatics_logic import poisson_1d_dirichlet,negative_gradient
from raji_sci.physics.field_visuals import ScalarFieldImage,polyline
from raji_sci.em.field_lines import trace_field_line
from raji_sci.presentation.layout import frame_violations


@dataclass(frozen=True)
class PlateModel:
    length: float=4.0
    node_count: int=81

    def solve(self, voltage):
        rho=np.zeros(self.node_count)
        return poisson_1d_dirichlet(rho,self.length/(self.node_count-1),0.0,voltage)

    def field(self,voltage):
        v=np.tile(self.solve(voltage),(9,1))
        ex,ey=negative_gradient(v,self.length/(self.node_count-1),1.0)
        return ex,ey


def validate_model(model):
    for voltage in (0.0,4.0,6.0):
        v=model.solve(voltage)
        assert np.isclose(v[0],0.0) and np.isclose(v[-1],voltage)
        assert np.allclose(np.diff(v,2),0,atol=1e-12)
        ex,ey=model.field(voltage)
        assert np.allclose(ex,-voltage/model.length,atol=1e-12)
        assert np.allclose(ey,0,atol=1e-12)


def switch(old,new):
    return Succession(FadeOut(old,run_time=.25),FadeIn(new,run_time=.25))


class ConductorBoundaryConditions(MovingCameraScene):
    def construct(self):
        model=PlateModel();validate_model(model)
        self.camera.background_color=BACKGROUND
        title=ar('الموصلات والشروط الحدية',size=35).move_to([0,3.43,0])
        panel,c1=caption_panel('يمكن تثبيت فرق الجهد بين موصلين باستخدام بطارية.')
        _,c2=caption_panel('كل موصل متساوي الجهد، ويحدد جهد سطحه شرطًا حدّيًا.')
        _,c3=caption_panel('نحل معادلة لابلاس في المنطقة الخالية من الشحنات.')
        _,c4=caption_panel('تحدد قيم الجهد على الحدود حل الجهد داخل المنطقة.')
        _,c5=caption_panel('يتغير الجهد والمجال عندما نغير فرق الجهد بين الموصلين.')
        _,c6=caption_panel('إذا وُجدت شحنة حجمية في المنطقة، نستخدم معادلة بواسون.')
        _,c7=caption_panel('من الجهد والمجال يمكن حساب الشحنة السطحية على الموصل.')
        if frame_violations([title,panel,c1,c2,c3,c4,c5,c6,c7],margin=.08):
            raise ValueError('Caption outside safe frame')
        self.add(title,panel)
        guide=hbar_character(.7).move_to([5.95,2.6,0])
        self.play(FadeIn(c1),FadeIn(guide,shift=LEFT*.15),run_time=.8)

        # A battery maintains a voltage difference across two conducting plates.
        xl,xr=-5.3,-.9; mid=(xl+xr)/2
        left=Polygon([xl-.2,-1.45,0],[xl,-1.45,0],[xl,1.65,0],[xl-.2,1.65,0],
                     stroke_color=CYAN,stroke_width=2,fill_color='#12465c',fill_opacity=.95)
        right=Polygon([xr,-1.45,0],[xr+.2,-1.45,0],[xr+.2,1.65,0],[xr,1.65,0],
                      stroke_color=GOLD,stroke_width=2,fill_color='#7c4d26',fill_opacity=.95)
        depth=VGroup(
            Polygon([xl-.2,1.65,0],[xl,1.65,0],[xl+.18,1.83,0],[xl-.02,1.83,0],stroke_color=CYAN,stroke_width=1.2,fill_color='#357e92',fill_opacity=.9),
            Polygon([xl,1.65,0],[xl+.18,1.83,0],[xl+.18,-1.27,0],[xl,-1.45,0],stroke_color=CYAN,stroke_width=1.0,fill_color='#123d4d',fill_opacity=.8),
            Polygon([xr,1.65,0],[xr+.2,1.65,0],[xr+.38,1.83,0],[xr+.18,1.83,0],stroke_color=GOLD,stroke_width=1.2,fill_color='#cc9052',fill_opacity=.9),
            Polygon([xr+.2,1.65,0],[xr+.38,1.83,0],[xr+.38,-1.27,0],[xr+.2,-1.45,0],stroke_color=GOLD,stroke_width=1.0,fill_color='#644020',fill_opacity=.8))
        highlights=VGroup(*[Line([x,y,0],[x,y+.42,0],stroke_color=color,stroke_width=1.1,stroke_opacity=.55)
                            for x,color in [(xl-.1,CYAN),(xr+.1,GOLD)] for y in np.linspace(-1.15,1.2,5)])
        wires=VGroup(polyline(np.array([[xl,-1.45],[xl,-2.15],[mid-.30,-2.15]]),color=CYAN,stroke_width=3,smooth=False),
                     polyline(np.array([[mid+.30,-2.15],[xr,-2.15],[xr,-1.45]]),color=GOLD,stroke_width=3,smooth=False))
        battery=VGroup(Line([mid-.30,-2.38,0],[mid-.30,-1.92,0],color=WHITE,stroke_width=3),
                       Line([mid+.30,-2.5,0],[mid+.30,-1.8,0],color=WHITE,stroke_width=3),
                       Text('−',font='Arial',font_size=20,color=CYAN).move_to([mid-.62,-1.84,0]),
                       Text('+',font='Arial',font_size=20,color=GOLD).move_to([mid+.62,-1.84,0]))
        lpot=tex(r'V_L=0',size=32,color=CYAN).move_to([xl,2.1,0])
        rpot=tex(r'V_R=V_0',size=32,color=GOLD).move_to([xr,2.1,0])
        self.play(FadeIn(left,shift=LEFT*.15),FadeIn(right,shift=RIGHT*.15),FadeIn(depth),Create(highlights),run_time=1.8)
        self.play(Create(wires),Create(battery),Write(lpot),Write(rpot),run_time=2)
        self.play(*[ShowPassingFlash(w.copy().set_stroke(width=5),time_width=.3) for w in wires],run_time=1.3)
        fixed1=tex(r'V\vert_{S_1}=0',size=38,color=CYAN,width=4.7).move_to([3,1.25,0])
        fixed2=tex(r'V\vert_{S_2}=V_0',size=38,color=GOLD,width=4.7).move_to([3,.25,0])
        self.play(FadeIn(fixed1,shift=UP*.12),FadeIn(fixed2,shift=UP*.12),switch(c1,c2),run_time=1.5)
        self.play(Indicate(left,color=CYAN),Indicate(right,color=GOLD),run_time=1)

        # The 1D Dirichlet solution is extended uniformly along the plates.
        voltage=ValueTracker(4.0)
        basis=model.solve(1.0)
        values=np.tile(4.0*basis,(64,1))
        heat=ScalarFieldImage(values,width=xr-xl,height=2.8,center=(mid,.1,0),vmax=6,
                              zero='#07121d',positive='#e7a150',negative='#57bddd',opacity=.85)
        heat.set_z_index(-1)
        for x in [0,.2,.4,.6,.8,1]:
            assert np.isclose(np.interp(x,np.linspace(0,1,model.node_count),basis),x)
        lines=VGroup(*[Line([xl+(xr-xl)*u,-1.25,0],[xl+(xr-xl)*u,1.45,0],color=WHITE,stroke_opacity=.35,stroke_width=1.5)
                       for u in np.linspace(.2,.8,4)])
        surface_charges=VGroup(
            *[Text('−',font='Arial',font_size=18,color=CYAN).move_to([xl+.11,y,0]) for y in np.linspace(-1.13,1.35,8)],
            *[Text('+',font='Arial',font_size=18,color=GOLD).move_to([xr-.09,y,0]) for y in np.linspace(-1.13,1.35,8)])
        self.play(FadeIn(heat),LaggedStart(*[Create(x) for x in lines],lag_ratio=.18),
                  LaggedStart(*[FadeIn(q,scale=.5) for q in surface_charges],lag_ratio=.025),run_time=1.9)
        self.play(FadeOut(fixed1),FadeOut(fixed2),switch(c2,c3),run_time=.8)
        laplace=tex(r'\nabla^2V=0',size=51,color=CYAN).move_to([3,1.55,0])
        region=ar('في المنطقة بين الموصلين',size=22,color=WHITE).move_to([3,.55,0])
        boundary=tex(r'V(0)=0,\quad V(L)=V_0',size=36,color=WHITE,width=5.1).move_to([3,-.45,0])
        self.play(Write(laplace),FadeIn(region),run_time=1.5)
        self.play(FadeIn(boundary,shift=UP*.1),run_time=1.2)
        self.play(Circumscribe(boundary,color=GOLD,fade_out=True),run_time=1)

        # V(x) and the visual probe are both read from the same solved profile.
        self.play(FadeOut(laplace),FadeOut(region),FadeOut(boundary),switch(c3,c4),run_time=.9)
        axes=Axes(x_range=[0,model.length,1],y_range=[0,6.5,2],x_length=4.5,y_length=2.5,tips=False,
                  axis_config={'color':'#8aa6b4','stroke_width':1.4,'include_ticks':False}).move_to([3,-.1,0])
        xlab=tex('x',size=26,color=WHITE).next_to(axes.x_axis,RIGHT,buff=.30)
        ylab=tex('V',size=26,color=GOLD).next_to(axes.y_axis,UP,buff=.08)
        Llab=tex('L',size=24,color=WHITE).next_to(axes.c2p(model.length,0),DOWN,buff=.24).shift(LEFT*.12)
        curve=always_redraw(lambda:Line(axes.c2p(0,0),axes.c2p(model.length,voltage.get_value()),color=GOLD,stroke_width=4))
        tracker=ValueTracker(0.0)
        physical=always_redraw(lambda:Dot([xl+(xr-xl)*tracker.get_value()/model.length,.1,0],radius=.09,color=WHITE))
        plotted=always_redraw(lambda:Dot(axes.c2p(tracker.get_value(),voltage.get_value()*np.interp(tracker.get_value(),np.linspace(0,model.length,model.node_count),basis)),radius=.08,color=WHITE))
        numeric=DecimalNumber(4.0,num_decimal_places=1,mob_class=Text,font_size=32,color=GOLD)
        numeric.add_updater(lambda m:m.set_value(voltage.get_value()))
        readout=VGroup(tex(r'V_0=',size=32,color=GOLD),numeric,tex(r'\mathrm{V}',size=30,color=WHITE)).arrange(RIGHT,buff=.12).move_to([3,1.85,0])
        self.play(Create(axes),FadeIn(xlab),FadeIn(ylab),FadeIn(Llab),FadeIn(curve),FadeIn(physical),FadeIn(plotted),FadeIn(readout),run_time=1.6)
        self.play(tracker.animate.set_value(model.length),run_time=4,rate_func=linear)
        self.play(tracker.animate.set_value(model.length*.53),run_time=1.5,rate_func=linear)

        # Changing the boundary value updates the solver-derived map and graph together.
        self.play(switch(c4,c5),run_time=.6)
        heat.add_updater(lambda m:m.update_values(np.tile(voltage.get_value()*basis,(64,1))))
        sample=np.array([[x,y] for x in np.linspace(xl+.4,xr-.4,5) for y in [-.8,.1,1.0]])
        def vector_field():
            ex,_=model.field(voltage.get_value())
            return np.tile([ex[0,0],0.0],(len(sample),1))
        arrows=always_redraw(lambda:field_arrows(sample,vector_field(),max_length=.65,color=CYAN,reference=.5,stroke_width=2.2))
        self.play(FadeIn(arrows),run_time=1)
        traced=VGroup()
        for y in [-.8,.1,1.0]:
            ray=trace_field_line(lambda p: np.array([model.field(voltage.get_value())[0][0,0],0]),
                                 [xr-.15,y],step=.07,steps=54,direction=1)
            traced.add(polyline(ray,color=CYAN,stroke_width=2,smooth=False))
        self.play(*[ShowPassingFlash(line,time_width=.25) for line in traced],run_time=1.4)
        self.play(voltage.animate.set_value(6.0),run_time=4,rate_func=linear)
        heat.clear_updaters()
        self.play(Indicate(curve,color=GOLD,scale_factor=1.01),run_time=.8)
        self.play(FadeOut(axes),FadeOut(xlab),FadeOut(ylab),FadeOut(Llab),FadeOut(curve),FadeOut(physical),FadeOut(plotted),FadeOut(arrows),FadeOut(readout),switch(c5,c6),run_time=1)
        poisson=tex(r'\nabla^2V=-\frac{\rho}{\varepsilon}',size=48,color=WHITE,width=4.8).move_to([3,1.25,0])
        gauss=tex(r'\rho=0\ \Rightarrow\ \nabla^2V=0',size=36,color=CYAN,width=5.1).move_to([3,0,0])
        self.play(Write(poisson),run_time=1.8)
        self.play(FadeIn(gauss,shift=UP*.1),run_time=1.3)
        self.play(FadeOut(poisson),FadeOut(gauss),switch(c6,c7),run_time=.8)
        source=tex(r'V\quad\longrightarrow\quad\mathbf{E}',size=43,color=CYAN,width=4.8).move_to([3,1.0,0])
        charges=tex(r'\mathbf{E}\quad\longrightarrow\quad\rho_s',size=43,color=GOLD,width=4.8).move_to([3,-.2,0])
        self.play(Write(source),Write(charges),run_time=1.6)
        self.play(Circumscribe(charges,color=GOLD,fade_out=True),guide.animate.shift(LEFT*.15),run_time=.9)
        self.wait(1)


if __name__ == '__main__':
    render(ConductorBoundaryConditions,filename='scene_11_boundary_conditions',preview=True)
