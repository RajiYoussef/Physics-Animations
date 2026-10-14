from common import *


class Scene04BatteryVoltage(Lesson):
    def construct(self):
        self.begin(4,'ماذا تعني بطارية بجهد محدد؟','هل جهد البطارية يخبرنا بكل طاقتها؟')
        source=battery(np.array([-4,.4,0]),'1.5 V').scale(1.5)
        self.show(source)
        low=Line([-1.5,-.8,0],[4.7,-.8,0],color=EDGE)
        high=Line([-1.5,1.35,0],[4.7,1.35,0],color=ENERGY)
        self.show(low,high,eq('0 J',27,MUTED).next_to(low,RIGHT),eq('+1.5 J',27,ENERGY).next_to(high,RIGHT))
        q=charge().move_to([.3,-.8,0]); qlabel=eq('q = 1 C',27,CURRENT).move_to([2.8,-1.4,0])
        self.show(q,qlabel)
        self.say('نموذج بطارية مثالية: ترفع طاقة الشحنة الموجبة',4)
        self.play(q.animate.move_to([.3,1.35,0]),run_time=2)
        self.formula('ΔU = qΔV = 1 C × 1.5 V = 1.5 J',ENERGY)
        self.say('التفاعلات الكيميائية تزود الدائرة بالطاقة',4)
        self.clear_stage()
        self.show(label_pair('شحنة أكبر','q = 2 C',CURRENT).move_to([-3,.7,0]),
                  label_pair('عند فرق الجهد نفسه','ΔV = 1.5 V',VOLT).move_to([3,.7,0]))
        self.say('ما مقدار الطاقة عند نقل كولومين؟',5)
        self.formula('ΔU = 2 × 1.5 = 3 J',ENERGY,y=-1)
        self.say('تتضاعف الطاقة المنقولة، ويبقى فرق الجهد نفسه',4)
        self.finish('جهد البطارية لا يحدد وحده طاقتها الكلية','ΔU = qΔV',VOLT)


if __name__=='__main__': render_scene(Scene04BatteryVoltage)
