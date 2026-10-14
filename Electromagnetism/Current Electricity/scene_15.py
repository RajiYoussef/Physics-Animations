from common import *


class Scene15CapacitorConcept(Lesson):
    def construct(self):
        self.begin(15,'المكثف: فصل الشحنة وتخزين الطاقة','أين تختزن الطاقة في المكثف؟')
        cap=capacitor(np.array([0,.3,0]),height=2.7,gap=2,n=7)
        self.show(cap[0],cap[1])
        self.show(ar('موصل',26).move_to([-2.2,1.3,0]),ar('موصل',26).move_to([2.2,1.3,0]),
                  ar('عازل',26,VOLT).move_to([0,-1.5,0]))
        self.say('موصلان يفصل بينهما عازل فلا تعبره شحنات التوصيل',5)
        self.show(cap[2])
        self.show(eq('+Q',33,POSITIVE).move_to([-2.2,.25,0]),eq('−Q',33,NEGATIVE).move_to([2.2,.25,0]))
        self.say('مصدر الجهد يفصل شحنتين متساويتين في المقدار ومتعاكستين',5)
        self.play(LaggedStart(*[GrowArrow(a) for a in cap[3]],lag_ratio=.15),run_time=1.5)
        self.say('المجال بين اللوحين يتجه من الموجب إلى السالب',4)
        self.play(cap[0].animate.set_fill(opacity=.22),run_time=1.5)
        self.formula('U = ½CV²',ENERGY)
        self.say('الطاقة المخزنة ترتبط بالمجال الكهربائي',5)
        self.say('بعد فصل المصدر يحتفظ المكثف المثالي بشحنته ',5)
        self.finish('المكثف يخزن طاقة بفصل شحنتين متعاكستين','Q + (−Q) = 0',VOLT)


if __name__=='__main__': render_scene(Scene15CapacitorConcept)
