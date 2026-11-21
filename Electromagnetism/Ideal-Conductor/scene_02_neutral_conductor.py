import numpy as np
from manim import *
from settings import BACKGROUND, CYAN, GOLD, WHITE, render
from support import ar, caption_panel
from tools import field_arrows, emphasize
from raji_sci.physics.electrostatics_logic import point_charge_field
from raji_sci.physics.field_visuals import polyline


class NeutralConductor(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        title = ar("التعادل وإعادة توزيع الشحنات", size=34).move_to([0, 3.45, 0])
        panel, cap1 = caption_panel("قد يحتوي الموصل المتعادل على شحنات موجبة وسالبة.")
        _, cap2 = caption_panel("تتساوى الشحنة الموجبة الكلية مع الشحنة السالبة الكلية.")
        _, cap3 = caption_panel("يمكن للإلكترونات الحركة مع بقاء الشحنة الكلية صفرًا.")
        _, cap4 = caption_panel("يحرك المجال الخارجي الإلكترونات نحو أحد جانبي الموصل.")
        _, cap5 = caption_panel("يتغير توزيع الشحنة، بينما تبقى الشحنة الكلية للموصل صفرًا.")
        self.add(title, panel)
        self.play(FadeIn(cap1), run_time=.7)

        ions = VGroup()
        for row, y in enumerate(np.linspace(-1.3, 1.3, 3)):
            for x in np.linspace(-4.1, 4.1, 7):
                p = np.array([x+(row % 2)*.18, y, 0])
                ions.add(VGroup(Circle(radius=.30, color=GOLD, stroke_opacity=.25, fill_color=GOLD, fill_opacity=.08),
                                Dot(radius=.12, color=GOLD), Text("+", font="Arial", font_size=18, color=BLACK)).move_to(p))
        cloud = VGroup(*[Circle(radius=.52, stroke_width=0, fill_color=CYAN, fill_opacity=.045).move_to([x,y,0])
                         for x in np.linspace(-4,4,9) for y in np.linspace(-1.3,1.3,4)])
        t = ValueTracker(0)
        shift = ValueTracker(0)
        rng = np.random.default_rng(22)
        electrons = VGroup()
        for _ in range(21):
            x,y,phase = rng.uniform(-4,4),rng.uniform(-1.35,1.35),rng.uniform(0,TAU)
            mob = VGroup(Circle(radius=.15, stroke_width=0, fill_color=CYAN, fill_opacity=.12), Dot(radius=.055, color=CYAN))
            def update(m, x=x, y=y, phase=phase):
                v = t.get_value()
                m.move_to([x + .28*np.sin(.7*v+phase) - shift.get_value(), y + .18*np.cos(.9*v+phase),0])
            mob.add_updater(update)
            electrons.add(mob)
        self.play(LaggedStart(*[FadeIn(i, scale=.4) for i in ions], lag_ratio=.025), FadeIn(cloud), FadeIn(electrons), run_time=2.2)
        self.play(t.animate.set_value(4), run_time=4, rate_func=linear)

        pos = ar("الشحنة الموجبة الكلية", size=25, color=GOLD).move_to([-3.5, 2.3, 0])
        neg = ar("الشحنة السالبة الكلية", size=25, color=CYAN).move_to([3.5, 2.3, 0])
        balance = Text("+Q  +  (−Q)  =  0", font="Arial", font_size=42, color=WHITE).move_to([0, -.05, 0])
        veil = RoundedRectangle(width=5.7, height=1.1, corner_radius=.2, stroke_color="#4b5967", fill_color=BLACK, fill_opacity=.90).move_to(balance)
        self.play(FadeOut(cap1), FadeIn(cap2), FadeIn(pos), FadeIn(neg), FadeIn(veil), FadeIn(balance), t.animate.set_value(6), run_time=2)
        emphasize(self, balance, color=WHITE, run_time=1.2)
        self.play(t.animate.set_value(9), run_time=3, rate_func=linear)
        self.play(FadeOut(veil), FadeOut(balance), FadeOut(pos), FadeOut(neg), FadeOut(cap2), FadeIn(cap3), run_time=1.3)

        trace_dot = Dot(color=WHITE, radius=.08).move_to([-3.8,-.3,0])
        points = np.array([[-3.8,-.3],[-2.2,.6],[-.8,-.5],[.9,.55],[2.4,-.45],[3.6,.3]])
        path = polyline(points, color=WHITE, stroke_width=2.3)
        tracing = TracedPath(trace_dot.get_center, stroke_color=WHITE, dissipating_time=1.1, stroke_width=2)
        self.add(tracing, trace_dot)
        self.play(MoveAlongPath(trace_dot, path), t.animate.set_value(14), run_time=5, rate_func=linear)
        self.play(FadeOut(trace_dot), FadeOut(tracing), FadeOut(cap3), FadeIn(cap4), run_time=1)

        arrow_points=np.array([[x,y] for x in [-5.7,-3.9,-2.0,0,2.0,3.9,5.7] for y in [-2.1,2.05]])
        applied=field_arrows(arrow_points, np.tile([1.,0.],(len(arrow_points),1)), max_length=1.1, color=CYAN, reference=.3)
        field_label=ar("المجال الخارجي", size=23, color=CYAN).move_to([0,2.58,0])
        body=RoundedRectangle(width=9.7,height=3.7,corner_radius=.3,stroke_color="#526475",stroke_width=1.5)
        self.play(Create(body), LaggedStart(*[GrowArrow(a) for a in applied],lag_ratio=.02), FadeIn(field_label), run_time=2)
        self.play(t.animate.set_value(21), shift.animate.set_value(.7), run_time=6, rate_func=linear)
        minus=VGroup(*[Text("−", font="Arial", font_size=29, color=CYAN).move_to([-4.6,y,0]) for y in np.linspace(-1.25,1.25,5)])
        plus=VGroup(*[Text("+", font="Arial", font_size=29, color=GOLD).move_to([4.6,y,0]) for y in np.linspace(-1.25,1.25,5)])
        zero=Text("Q = 0", font="Arial", font_size=30, color=WHITE).move_to([5.7,0,0])
        self.play(FadeIn(minus), FadeIn(plus), FadeIn(zero), FadeOut(cap4), FadeIn(cap5), t.animate.set_value(23), run_time=2)
        self.play(t.animate.set_value(26),run_time=3,rate_func=linear)

        # The final arrows are calculated from two representative separated charges.
        charges=np.array([[-4.6,0,-1.0],[4.6,0,1.0]])
        points=np.array([[x,y] for x in [-3.,-1.5,0,1.5,3.] for y in [-.85,0,.85]])
        vectors=point_charge_field(charges,points,softening=.35)
        induced=field_arrows(points,vectors,max_length=.85,color=GOLD,reference=.04)
        induced_label=ar("المجال الناتج عن الشحنات السطحية",size=22,color=GOLD).move_to([0,-2.5,0])
        self.play(LaggedStart(*[GrowArrow(a) for a in induced],lag_ratio=.025), FadeIn(induced_label), t.animate.set_value(29), run_time=3)
        self.wait(.8)


if __name__ == "__main__":
    render(NeutralConductor, filename="scene_02_neutral_conductor", preview=True)

