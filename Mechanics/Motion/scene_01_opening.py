"""Chapter 1: a visual question. Press PyCharm Run."""
from film_core import *
from motion_models import bend_by_distance


class Scene01Opening(FilmScene):
    chapter_id=1

    def construct(self):
        self.opening("هل يمكن لجسم ما أن يتسارع دون زيادة في سرعته؟","MOTION / A QUESTION")
        distance=ValueTracker(0)
        active_time=.83*self.shot_info(0)[0]+.8*self.shot_info(1)[0]
        visual_speed=6.1/active_time
        def state():return bend_by_distance(distance.get_value())
        def location():return state()[0]
        roadway=VGroup(
            Line([-5.8,-1.3,0],[-2,-1.3,0],color="#23394A",stroke_width=30),
            DashedLine([-5.8,-1.3,0],[-2,-1.3,0],color=GHOST,stroke_width=1),
            arc_road([-2,.9,0],2.2,-PI/2,1.6))
        car=Car(length=.8)
        car.add_updater(lambda m:m.pose(location(),np.arctan2(state()[1][1],state()[1][0])))
        vel=always_redraw(lambda:vector(location(),state()[1],1.2))
        gauge=SpeedGauge(lambda:50).move_to([4.1,1.3,0])
        scalar_note=ar("يخبرنا عداد السرعة بمدى سرعتنا.",25,width=3.8).move_to([4.1,-.05,0])
        self.add(roadway,car,vel,gauge)
        with self.shot(0) as d:
            self.caption_ar("تظل السرعة ثابتة... فما الذي يحدث للمتجه؟؟")
            self.play(FadeIn(scalar_note),run_time=d*.07)
            self.play(distance.animate.set_value(visual_speed*d*.83),run_time=d*.83,rate_func=linear)
            self.checkpoint("straight_equal_speed")
        with self.shot(1) as d:
            self.caption_ar("ما يحدث هو أن الاتجاه يتغير.")
            start_copy=vel.copy().clear_updaters().set_opacity(.25)
            self.add(start_copy)
            self.play(distance.animate.increment_value(visual_speed*d*.4),run_time=d*.4,rate_func=linear)
            middle_copy=vel.copy().clear_updaters().set_opacity(.3)
            self.add(middle_copy)
            self.play(distance.animate.set_value(6.1),run_time=d*.4,rate_func=linear)
            self.play(Indicate(gauge.frame,color=VELOCITY,scale_factor=1.04),run_time=d*.1)
            self.checkpoint("same_number_new_heading")
        with self.shot(2) as d:
            self.caption_ar(" هذه أيضا حالة تسارع",ACCELERATION)
            position=location()
            inward=vector(position,-radial((6.1-3)/2.2-PI/2),1.05,ACCELERATION)
            answer=VGroup(ar("تغيّر الاتجاه",29,color=VELOCITY),
                          ar("وهذا يعني أن السرعة المتجهة تتغير",26,width=4.5,color=ACCELERATION)).arrange(DOWN,buff=.35).move_to([3.8,-1.6,0])
            self.play(GrowArrow(inward),FadeOut(scalar_note),run_time=d*.16)
            self.play(FadeIn(answer,shift=UP*.12),run_time=d*.12)
            self.play(Circumscribe(answer,color=ACCELERATION),run_time=d*.2)
        car.clear_updaters();vel.clear_updaters();gauge.clear_updaters()
        self.finish()


if __name__=="__main__":
    render_chapter(Scene01Opening)
