from common import *


class Scene01Intro(Lesson):
    def construct(self):
        self.begin(1,'الكهرباء: من الشحنة إلى الطاقة','ماذا تعني الأرقام على أجهزتنا؟')
        cards=VGroup(*[panel(3.7,3.7,[x,.35,0]) for x in [-4.15,0,4.15]])
        self.show(*cards)
        cell=VGroup(RoundedRectangle(width=.95,height=1.55,corner_radius=.12,color=VOLT),
                    Rectangle(width=.34,height=.14,color=VOLT).shift(UP*.84),eq('+',25,VOLT).shift(UP*.4)).move_to([-4.15,1,0])
        lamp=bulb(np.array([0,1,0])).scale(1.6)
        kettle=VGroup(RoundedRectangle(width=1.2,height=1.2,corner_radius=.2,color=RESIST),
                      Arc(radius=.4,start_angle=-PI/2,angle=PI,color=RESIST).shift(RIGHT*.6)).move_to([4.15,1,0])
        self.show(cell,lamp,kettle)
        names=VGroup(*[ar(t,26).move_to([x,-.1,0]) for x,t in [(-4.15,'بطارية'),(0,'مصباح'),(4.15,'غلاية')]])
        numbers=VGroup(*[eq(t,36,c).move_to([x,-.75,0]) for x,t,c in [(-4.15,'1.5 V',VOLT),(0,'10 W',ENERGY),(4.15,'2000 W',ENERGY)]])
        self.show(names,numbers)
        self.say('الفولت والواط يصفان كميتين مختلفتين',4)
        self.play(Indicate(numbers[0],color=VOLT),run_time=1)
        self.say('فرق الجهد: طاقة تنتقل لكل وحدة شحنة',4,color=VOLT)
        self.play(Indicate(VGroup(numbers[1],numbers[2]),color=ENERGY),run_time=1)
        self.say('القدرة: طاقة تتحول في كل ثانية',4,color=ENERGY)
        self.finish('سنربط الشحنة والجهد والتيار والطاقة','V    •    I    •    R    •    P    •    C')


if __name__=='__main__': render_scene(Scene01Intro)
