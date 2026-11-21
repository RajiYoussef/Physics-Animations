"""Chapter 3: construct velocity change by moving actual snapshots."""
from film_core import *
from motion_models import velocity_difference


class Scene03AccelerationDefinition(FilmScene):
    chapter_id=3

    def construct(self):
        self.opening("ما الذي تغيّر في متجه السرعة؟","COMPARE / SUBTRACT / DIVIDE BY TIME")
        center=np.array([-2.8,.7,0]);radius=2.3
        angles=(-PI*.42,-PI*.08)
        theta=ValueTracker(angles[0])
        def position():return center+radius*radial(theta.get_value())
        car=Car(length=.7)
        car.add_updater(lambda m:m.pose(position(),theta.get_value()+PI/2))
        velocity=always_redraw(lambda:vector(position(),tangent(theta.get_value()),1.45))
        road=arc_road(center,radius,-PI*.53,PI*.59)
        gauge=SpeedGauge(lambda:50).move_to([4.1,1,0])
        self.add(road,car,velocity,gauge)
        with self.shot(0) as d:
            self.caption_ar("لنقارن السرعة المتجهة قبل المنعطف وبعده")
            first=vector(center+radius*radial(angles[0]),tangent(angles[0]),1.45).set_opacity(.6)
            ghost=car.copy().clear_updaters().set_opacity(.25)
            self.add(first,ghost)
            self.play(theta.animate.set_value(angles[1]),run_time=d*.55,rate_func=linear)
            second=vector(position(),tangent(angles[1]),1.45)
            self.add(second)
            first_label=math_label("v1",24,VELOCITY).next_to(first,DOWN,buff=.12)
            second_label=math_label("v2",24,VELOCITY).next_to(second,RIGHT,buff=.12)
            self.play(FadeIn(first_label),FadeIn(second_label),run_time=d*.08)
            self.checkpoint("velocity_snapshots")
        car.clear_updaters();velocity.clear_updaters();gauge.clear_updaters()
        with self.shot(1) as d:
            self.caption_ar("نضع المتجهين عند نقطة بداية مشتركة لنرى الفرق.")
            origin=np.array([-4,-.65,0]);v1=1.45*tangent(angles[0]);v2=1.45*tangent(angles[1])
            target1=vector(origin,v1,np.linalg.norm(v1));target2=vector(origin,v2,np.linalg.norm(v2))
            # Copies visibly retain their direction while moving to a common tail.
            self.play(FadeOut(road),FadeOut(car),FadeOut(velocity),FadeOut(ghost),FadeOut(gauge),
                      FadeOut(first_label),FadeOut(second_label),
                      Transform(first,target1),Transform(second,target2),run_time=d*.12)
            self.add(Dot(origin,radius=.05,color=MUTED))
            names=VGroup(math_label("v1",22,VELOCITY).move_to(origin+v1+[.05,-.3,0]),
                         math_label("v2",22,VELOCITY).move_to(origin+v2+[-.35,.05,0]))
            self.add(names)
            delta=Arrow(origin+v1,origin+v2,buff=0,color=ACCELERATION,stroke_width=5)
            delta_name=math_label("Δv",27,ACCELERATION).next_to(delta,RIGHT,buff=.15)
            expression=equation(math_label("Δv",36,ACCELERATION),"=",math_label("v2",36,VELOCITY),"-",math_label("v1",36,VELOCITY)).move_to([3.1,1,0])
            self.play(GrowArrow(delta),FadeIn(delta_name),FadeIn(expression),run_time=d*.12)
            self.checkpoint("head_to_head_difference")
            formula=tex(r"\vec a_{\mathrm{avg}}=\frac{\Delta\vec v}{\Delta t}",36,ACCELERATION).move_to([3.1,-.6,0])
            average=ar("التسارع المتوسط",27,color=ACCELERATION).move_to([3.1,-1.8,0])
            self.play(FadeIn(formula,shift=UP*.15),FadeIn(average),run_time=d*.12)
            translated=delta.copy()
            self.play(translated.animate.shift(origin-(origin+v1)),run_time=d*.1)
            direction_note=ar("اتجاه التسارع",21,color=ACCELERATION).move_to([-4.9,-1.35,0])
            self.add(direction_note)
            self.play(Indicate(translated,color=ACCELERATION),run_time=d*.08)
            self.check_layout(expression,formula,average)
        self.clear_stage()
        with self.shot(2) as d:
            self.caption_ar("يمكن أن يتغير مقدار المتجه أو اتجاهه... أو كلاهما.")
            clock=ValueTracker(0)
            centers=[np.array([x,0,0]) for x in (-4.3,0,4.3)]
            labels=VGroup(*[ar(text,28,width=3.8).move_to(c+[0,1.65,0]) for text,c in zip(
                ["المقدار","الاتجاه","المقدار والاتجاه"],centers)])
            arrows=VGroup(
                always_redraw(lambda:vector(centers[0]+[-1,0,0],RIGHT,.7+1.2*clock.get_value())),
                always_redraw(lambda:vector(centers[1],radial(clock.get_value()*PI*.65),1.4)),
                always_redraw(lambda:vector(centers[2],radial(clock.get_value()*PI*.65),.7+.7*clock.get_value())))
            self.add(labels,arrows)
            self.play(clock.animate.set_value(1),run_time=d*.42,rate_func=linear)
            self.checkpoint("three_changes")
            arrows.clear_updaters(recursive=True)
            result=ar("في كل حالة تتغير فيها السرعة، نحصل على تسارع.",33,color=ACCELERATION).move_to([0,-1.6,0])
            self.play(FadeIn(result),run_time=d*.09)
        self.finish()


if __name__=="__main__":
    render_chapter(Scene03AccelerationDefinition)
