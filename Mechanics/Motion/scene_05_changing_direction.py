"""Chapter 5: constant speed, rotating velocity, and an inward change."""
from film_core import *


class Scene05ChangingDirection(FilmScene):
    chapter_id=5

    def construct(self):
        self.opening("يتغيّر الاتجاه، ويبقى المقدار ثابتاً","TURNING / CONSTANT SPEED")
        center=np.array([-2.75,.05,0]);radius=2
        theta=ValueTracker(-PI*.72)
        angular_rate=1.22*PI/(.8*self.shot_info(0)[0]+.76*self.shot_info(1)[0])
        def location():return center+radius*radial(theta.get_value())
        car=Car(length=.7)
        car.add_updater(lambda m:m.pose(location(),theta.get_value()+PI/2))
        velocity=always_redraw(lambda:vector(location(),tangent(theta.get_value()),1.15))
        inward=always_redraw(lambda:vector(location(),-radial(theta.get_value()),.88,ACCELERATION))
        road=arc_road(center,radius,-PI*.8,PI*1.4)
        gauge=SpeedGauge(lambda:50).move_to([4,1.55,0])
        self.add(road,car,velocity,gauge)
        with self.shot(0) as d:
            self.caption_ar("يظل مقدار السرعة ثابتاً، دون تغيير.ورغم ذلك فإن السيارة سيكون لها تسارع")
            self.play(theta.animate.increment_value(angular_rate*d*.8),run_time=d*.8,rate_func=linear)
            self.play(Indicate(gauge.frame,color=VELOCITY),run_time=d*.08)
        with self.shot(1) as d:
            self.caption_ar("يتبع متجه السرعة (السهم الأزرق) المسار، بينما يتجه التسارع (السهم الأصفر) نحو الداخل.")
            self.add(inward)
            normal=always_redraw(lambda:right_angle_at(location(),theta.get_value()))
            self.add(normal)
            tangent_note=ar("مماس للمسار",25,color=VELOCITY).move_to([4,-.15,0])
            normal_note=ar("نحو إلى مركز المسار المنحنيء",25,color=ACCELERATION).move_to([4,-.85,0])
            self.play(FadeIn(tangent_note),FadeIn(normal_note),run_time=d*.06)
            self.play(theta.animate.increment_value(angular_rate*d*.76),run_time=d*.76,rate_func=linear)
            self.checkpoint("perpendicular_vectors_on_turn")
        car.clear_updaters();velocity.clear_updaters();inward.clear_updaters();gauge.clear_updaters();normal.clear_updaters()
        self.clear_stage()
        with self.shot(2) as d:
            self.caption_ar("مقدار السرعة هو نفسه في كلتا الحالتين، لكن الحركة الدائرية تؤدي إلى وجود تسارع.")
            left_origin=np.array([-3.4,-.2,0]);right_origin=np.array([3.2,-.2,0])
            separation=Line([0,-2.6,0],[0,2.6,0],color=GHOST,stroke_width=1)
            line=Line([-5.5,-.2,0],[-1.3,-.2,0],color=GHOST,stroke_width=2)
            circle=Circle(radius=1.4,color=GHOST,stroke_width=2).move_to(right_origin)
            clock=ValueTracker(0)
            leftcar=Car(length=.65)
            leftcar.add_updater(lambda m:m.pose(left_origin+[-1.4+clock.get_value()*.7,0,0],0))
            rightcar=Car(length=.65)
            rightcar.add_updater(lambda m:m.pose(right_origin+1.4*radial(clock.get_value()*.5-PI/2),clock.get_value()*.5))
            leftv=always_redraw(lambda:vector(leftcar.get_center(),RIGHT,.85))
            rightv=always_redraw(lambda:vector(rightcar.get_center(),tangent(clock.get_value()*.5-PI/2),.85))
            righta=always_redraw(lambda:vector(rightcar.get_center(),-radial(clock.get_value()*.5-PI/2),.6,ACCELERATION))
            labels=VGroup(ar("خط مستقيم",28).move_to([-3.4,2,0]),
                          ar("مسار منحني",28).move_to([3.2,2,0]),
                          math_label("50 km/h",28,VELOCITY).move_to([-3.4,1.3,0]),
                          math_label("50 km/h",28,VELOCITY).move_to([3.2,1.3,0]),
                          math_label("a = 0",28,ACCELERATION).move_to([-3.4,-2.2,0]),
                          math_label("a > 0",28,ACCELERATION).move_to([3.2,-2.2,0]))
            self.add(separation,line,circle,labels,leftcar,rightcar,leftv,rightv,righta)
            # Equal scene speed: .7 on the line, r*omega = 1.4*.5 on the circle.
            self.play(clock.animate.set_value(4),run_time=d*.78,rate_func=linear)
            for mob in (leftcar,rightcar,leftv,rightv,righta):mob.clear_updaters()
            self.checkpoint("equal_speed_different_acceleration")
        self.finish()


if __name__=="__main__":
    render_chapter(Scene05ChangingDirection)
