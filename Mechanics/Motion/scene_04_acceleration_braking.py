"""Chapter 4: one continuous trajectory and its velocity-time graph."""
from film_core import *
from motion_models import two_phase
from science_anim.visuals import SampledCurve


class Scene04AccelerationBraking(FilmScene):
    chapter_id=4

    def construct(self):
        self.opening("التسارع لا يعني دائماً زيادة السرعة","ONE CAR / ONE HISTORY")
        physical_time=ValueTracker(0)
        acceleration_sign=ValueTracker(1)
        motion_duration=min(self.shot_info(0)[0],self.shot_info(1)[0])*.83
        def state():return two_phase(physical_time.get_value())
        def car_position():return np.array([-5.2+float(state()[0])/272*9.6,0,0])
        car=Car(length=.72)
        car.add_updater(lambda m:m.pose(car_position(),0))
        road=Line([-6.1,0,0],[5.5,0,0],color="#23394A",stroke_width=29).set_z_index(-3)
        dashes=DashedLine([-6.1,0,0],[5.5,0,0],color=GHOST,stroke_width=1).set_z_index(-2)
        velocity=always_redraw(lambda:vector(car_position()+[0,.42,0],RIGHT,float(state()[1])*.065))
        acceleration=always_redraw(lambda:vector(car_position()+[0,1,0],RIGHT*acceleration_sign.get_value(),.85,ACCELERATION))
        gauge=SpeedGauge(lambda:float(state()[1]),unit="m/s",maximum=30).move_to([4.35,2.15,0])
        axes=Axes(x_range=[0,16,4],y_range=[0,28,10],x_length=10,y_length=2.05,tips=False,
                  axis_config={"stroke_color":GHOST,"stroke_width":1.5}).move_to([0,-1.65,0])
        axis_labels=VGroup(math_label("v (m/s)",19,VELOCITY).next_to(axes.y_axis,LEFT,buff=.15),
                           math_label("t (s)",19,MUTED).next_to(axes.x_axis,RIGHT,buff=.12))
        for value in [0,8,16]:
            axis_labels.add(math_label(str(value),17,MUTED).next_to(axes.c2p(value,0),DOWN,buff=.1))
        for value in [10,24]:
            axis_labels.add(math_label(str(value),17,MUTED).next_to(axes.c2p(0,value),LEFT,buff=.1))
        curve=VMobject(color=VELOCITY,stroke_width=3)
        def update_curve(m):
            t=max(physical_time.get_value(),.0001)
            samples=np.linspace(0,t,121)
            m.set_points_as_corners([axes.c2p(s,float(two_phase(s)[1])) for s in samples])
        curve.add_updater(update_curve)
        marker=always_redraw(lambda:Dot(axes.c2p(physical_time.get_value(),float(state()[1])),color=INK,radius=.055))
        phase=ar("تزداد السرعة",30,color=ACCELERATION).move_to([-2.3,2.35,0])
        acceleration_value=math_label("a = +1.75 m/s²",26,ACCELERATION).move_to([-2.3,1.65,0])
        self.add(road,dashes,car,velocity,acceleration,gauge,axes,axis_labels,curve,marker,phase,acceleration_value)
        with self.shot(0) as d:
            self.caption_ar("الجزء1 :التسارع يدفع السرعة إلى الزيادة. يشير متجه التسارع في الاتجاه نفسه")
            self.play(physical_time.animate.set_value(8),run_time=motion_duration,rate_func=linear)
            self.checkpoint("accelerating_same_car")
        with self.shot(1) as d:
            self.caption_ar("تتباطأ السرعة , متجه التسارع يشير إلى الاتجاه المعاكس")
            new_phase=ar("عندما نضغط على المكابح",30,color=ACCELERATION).move_to(phase)
            new_value=math_label("a = -1.75 m/s²",26,ACCELERATION).move_to(acceleration_value)
            self.play(Transform(phase,new_phase),Transform(acceleration_value,new_value),run_time=d*.05)
            acceleration_sign.set_value(-1)
            self.play(physical_time.animate.set_value(16),run_time=motion_duration,rate_func=linear)
            self.checkpoint("braking_same_car")
        car.clear_updaters();velocity.clear_updaters();acceleration.clear_updaters()
        gauge.clear_updaters();curve.clear_updaters();marker.clear_updaters()
        with self.shot(2) as d:
            self.caption_ar("يمكن تحديد التسارع من خلال ميل هذا المنحنى.في الجزء الأول يكون الميل موجب، بينما في الجزء الثاني يكون سالب.")
            # Same completed trace; do not substitute a second experiment.
            first_slope=Line(axes.c2p(2,13.5),axes.c2p(6,20.5),color=ACCELERATION,stroke_width=6)
            second_slope=Line(axes.c2p(10,20.5),axes.c2p(14,13.5),color=ACCELERATION,stroke_width=6)
            equation1=tex(r"a=\frac{\Delta v}{\Delta t}",34,ACCELERATION).move_to([-2.1,1.8,0])
            self.play(FadeOut(phase),FadeOut(acceleration_value),FadeIn(equation1),run_time=d*.08)
            self.play(Create(first_slope),run_time=d*.08)
            self.play(Indicate(first_slope,color=ACCELERATION),run_time=d*.1)
            self.play(Create(second_slope),run_time=d*.08)
            self.play(Indicate(second_slope,color=ACCELERATION),run_time=d*.1)
            self.checkpoint("slope_is_acceleration")
        self.finish()


if __name__=="__main__":
    render_chapter(Scene04AccelerationBraking)
