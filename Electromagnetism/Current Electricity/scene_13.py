from common import *


class Scene13SeriesCircuit(Lesson):
    def construct(self):
        self.begin(13,'التوصيل على التوالي','ماذا يبقى متساويا في مسار واحد؟')
        b=battery(np.array([-4.6,.15,0]),'12 V')
        # Wires stop at component terminals: there is no hidden short circuit.
        wires=VGroup(path([[-4.6,.8,0],[-4.6,1.65,0],[-2.675,1.65,0]]),
                     wire([-1.325,1.65,0],[.325,1.65,0]),
                     path([[1.675,1.65,0],[4.6,1.65,0],[4.6,-1.35,0],[-4.6,-1.35,0],[-4.6,-.5,0]]))
        r1=resistor(np.array([-2,1.65,0]),label='2 Ω');r2=resistor(np.array([1,1.65,0]),label='4 Ω')
        self.show(b,wires,r1,r2)
        self.show(eq('I = 2 A',31,CURRENT).move_to([.2,-.8,0]))
        self.say('المقاومة الكلية 6 أوم والتيار 2أمبير',4)
        route=[[-4.6,.15,0],[-4.6,1.65,0],[4.6,1.65,0],[4.6,-1.35,0],[-4.6,-1.35,0],[-4.6,.15,0]]
        self.flow(route,seconds=5,count=16)
        self.say('في الحالة المستقرة: التيار نفسه يمر في كل عنصر',5)
        self.show(eq('V₁ = 4 V',28,VOLT).move_to([-2,.75,0]),eq('V₂ = 8 V',28,VOLT).move_to([1,.75,0]))
        self.formula('12 V = 4 V + 8 V',VOLT)
        self.say('يتوزع فرق الجهد بنسبة المقاومات وليس بالتساوي دائما',5)
        self.clear_stage()
        self.show(eq('Rₛ = R₁ + R₂ = 2 + 4 = 6 Ω',37,RESIST).move_to([0,1.1,0]),
                  eq('I = 12 / 6 = 2 A',37,CURRENT).move_to([0,.1,0]),
                  eq('V₁ = IR₁ = 4 V    •    V₂ = IR₂ = 8 V',33,VOLT).move_to([0,-.9,0]))
        self.say('إذا انقطع هذا المسار، ينقطع التيار عن جميع العناصر',5)
        self.finish('التوالي: تيار واحد وفروق جهد تتجمع','I₁ = I₂    •    V = V₁ + V₂',CURRENT)


if __name__=='__main__': render_scene(Scene13SeriesCircuit)
