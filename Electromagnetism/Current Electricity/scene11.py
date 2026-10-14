from common import *


class Scene11PowerVoltageCurrent(Lesson):
    def construct(self):
        self.begin(11,'الجهد والتيار يحددان القدرة','كيف نجمع طاقة كل كولوم مع عدد الكولومات؟')
        self.show(panel(5.7,3.4,[-3.1,.65,0]),panel(5.7,3.4,[3.1,.65,0]))
        self.show(label_pair('طاقة لكل وحدة شحنة','V = 6 J/C',VOLT).move_to([-3.1,.8,0]),
                  label_pair('شحنة تمر في كل ثانية','I = 2 C/s',CURRENT).move_to([3.1,.8,0]))
        self.say('فرق الجهد يحدد الطاقة المنتقلة لكل كولوم',4,color=VOLT)
        self.say('والتيار يحدد عدد الكولومات التي تمر في الثانية',4,color=CURRENT)
        formula=self.formula('P = (6 J/C) × (2 C/s) = 12 J/s',ENERGY,y=-1.9)
        self.say('بضربهما نحصل على جول في الثانية: أي واط',4)
        self.play(Transform(formula,eq('P = VI = 6 × 2 = 12 W',39,ENERGY).move_to(formula)))
        self.wait(3)
        self.clear_stage()
        steps=VGroup(eq('P = ΔE / Δt',40,ENERGY),eq('ΔE = VΔQ',36,VOLT),eq('P = V × (ΔQ / Δt) = VI',40,ENERGY)).arrange(DOWN,buff=.55)
        for step in steps:self.show(step);self.wait(2)
        self.say('نستخدم هنا مقادير ثابتة في دائرة تيار مستمر',4)
        self.finish('القدرة تساوي فرق الجهد مضروًا في التيار','P = VI',ENERGY)


if __name__=='__main__': render_scene(Scene11PowerVoltageCurrent)
