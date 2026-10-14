from common import *


class Scene08Resistance(Lesson):
    def construct(self):
        self.begin(8,'المقاومة الكهربائية','عند الجهد نفسه: أي مقاومة تسمح بتيار أكبر؟')
        for x,r,i in [(-3.2,3,2),(3.2,6,1)]:
            self.show(panel(5.8,3.8,[x,.3,0]),eq('V = 6 V',30,VOLT).move_to([x,1.65,0]),
                      resistor(np.array([x,.65,0]),2,f'{r} Ω'),
                      eq(f'I = {i} A',35,CURRENT).move_to([x,-.4,0]))
            bar=Rectangle(width=i*1.5,height=.18,fill_color=CURRENT,fill_opacity=1,stroke_width=0).move_to([x,-1,0]);self.show(bar)
        self.say('ضاعفنا المقاومة مع ثبات فرق الجهد فانخفض التيار إلى النصف',5)
        self.formula('I = V / R',CURRENT)
        self.say('المقاومة تقاس بالأوم',3)
        self.clear_stage()
        r=resistor(ORIGIN,3,'R'); self.show(r)
        self.show(Arrow([-4,0,0],[-1.6,0,0],color=CURRENT),Arrow([1.6,0,0],[4,0,0],color=CURRENT),
                  eq('I',32,CURRENT).move_to([-3,.55,0]),eq('I',32,CURRENT).move_to([3,.55,0]))
        heat=VGroup(*[Arrow([x,.4,0],[x,1.6,0],color=ENERGY,stroke_width=2) for x in [-.9,0,.9]])
        self.show(heat,ar('طاقة حرارية',28,ENERGY).move_to([0,2,0]))
        self.say('الشحنة محفوظة والمقاومة تحول طاقة كهربائية إلى حرارة',5)
        self.finish('مقاومة أكبر تعني تيارا أقل عند الجهد نفسه','R = V / I    •    Ω',RESIST)


if __name__=='__main__': render_scene(Scene08Resistance)
