"""Chapter 2: magnitude, direction, distance and displacement."""
from film_core import *
from science_anim.presentation.layout import Comparison


class Scene02SpeedVelocity(FilmScene):
    chapter_id=2

    def construct(self):
        self.opening("السرعة والسرعة المتجهة","MAGNITUDE / DIRECTION")
        car=Car(length=1.2).move_to([-2,0,0])
        gauge=SpeedGauge(lambda:50).move_to([3.8,.7,0])
        possibilities=VGroup(*[vector([-2,0,0],direction,1.7,color=GHOST)
                              for direction in (RIGHT,UP,LEFT,DOWN)])
        unknown=ar("أي اتجاه؟",36,color=PURPLE).move_to([-2,2.35,0])
        with self.shot(0) as d:
            self.caption_ar("نعرف كم تسرع السيارة، لكن أي اتجاه؟")
            self.add(car,gauge)
            self.play(FadeIn(unknown),LaggedStart(*[GrowArrow(a) for a in possibilities],lag_ratio=.15),run_time=d*.14)
            self.play(Indicate(gauge.frame,color=VELOCITY),run_time=d*.08)
            one_number=ar("العداد لا يخبرنا بالاتجاه",28,width=4.5).move_to([3.8,-1.1,0])
            self.play(FadeIn(one_number),run_time=d*.08)
        self.clear_stage()
        with self.shot(1) as d:
            self.caption_ar("تتطابق السرعتان، لكن السيارتين تتجهان في اتجاهين مختلفين.")
            east=Car(length=1).move_to([-3.4,-.1,0])
            west=Car(length=1).pose([3.4,-.1,0],PI)
            east_arrow=vector([-4.4,-1.1,0],RIGHT,2)
            west_arrow=vector([4.4,-1.1,0],LEFT,2)
            east_info=VGroup(ar("إلى اليمين",30),math_label("50 km/h",34,VELOCITY)).arrange(DOWN,buff=.35).move_to([-3.4,1.6,0])
            west_info=VGroup(ar("إلى اليسار",30),math_label("50 km/h",34,VELOCITY)).arrange(DOWN,buff=.35).move_to([3.4,1.6,0])
            self.add(Line([0,-2.4,0],[0,2.5,0],stroke_width=1,color=GHOST))
            self.play(FadeIn(east_info),FadeIn(west_info),FadeIn(east),FadeIn(west),run_time=d*.08)
            self.play(GrowArrow(east_arrow),GrowArrow(west_arrow),run_time=d*.08)
            self.play(east.animate.shift(RIGHT*.85),west.animate.shift(LEFT*.85),run_time=d*.25,rate_func=linear)
            same=ar("السرعة نفسها على العداد",26,color=VELOCITY).move_to([0,-2.15,0])
            self.play(FadeIn(same),run_time=d*.06)
            self.play(Indicate(east_arrow),Indicate(west_arrow),run_time=d*.08)
            self.checkpoint("opposite_velocities")
        self.clear_stage()
        with self.shot(2) as d:
            self.caption_ar("كم قطعنا؟ وأين انتهينا بالنسبة إلى البداية؟")
            start=np.array([-4.8,1.1,0]);turn=np.array([3.2,1.1,0]);end=np.array([-1.6,1.1,0])
            route=Line(start,turn,color=GHOST)
            traveler=Dot(start,color=INK,radius=.07)
            outward=Arrow(start+[0,.22,0],turn+[0,.22,0],buff=0,color=PURPLE,stroke_width=4)
            back=Arrow(turn+[0,-.22,0],end+[0,-.22,0],buff=0,color=PURPLE,stroke_width=4)
            labels=VGroup(math_label("A",23).next_to(start,LEFT),math_label("B",23).move_to(end+[0,-.95,0]),
                          math_label("100 m",23,PURPLE).move_to([-1,1.95,0]),
                          math_label("60 m",23,PURPLE).move_to([.8,.25,0]),
                          math_label("20 s",30).move_to([5,1.1,0]))
            self.add(route,traveler,labels)
            self.play(GrowArrow(outward),traveler.animate.move_to(turn),run_time=d*.17,rate_func=linear)
            self.play(GrowArrow(back),traveler.animate.move_to(end),run_time=d*.13,rate_func=linear)
            displacement=Arrow(start+[0,-.65,0],end+[0,-.65,0],buff=0,color=DISPLACEMENT,stroke_width=4)
            self.play(GrowArrow(displacement),run_time=d*.07)
            left=VGroup(ar("السرعة القياسية المتوسطة",25,width=5.4),
                        tex(r"\frac{100+60}{20}=8\,\mathrm{m/s}",34,PURPLE)).arrange(DOWN,buff=.25).move_to([-3.3,-1.7,0])
            right=VGroup(ar("السرعة المتجهة المتوسطة",25,width=5.4),
                         tex(r"\frac{40}{20}=2\,\mathrm{m/s}",34,DISPLACEMENT),
                         ar("نحو اليمين",22,color=DISPLACEMENT)).arrange(DOWN,buff=.18).move_to([3.1,-1.75,0])
            self.play(FadeIn(left),FadeIn(right),run_time=d*.13)
            self.check_layout(left,right)
            self.checkpoint("distance_vs_displacement")
        self.finish()


if __name__=="__main__":
    render_chapter(Scene02SpeedVelocity)
