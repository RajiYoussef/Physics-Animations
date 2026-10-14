from common import *


class Scene03VoltageMeaning(Lesson):
    def construct(self):
        self.begin(3,'معنى فرق الجهد','كم تتغير الطاقة لكل كولوم؟')
        cards=VGroup(panel(5.6,3.5,[-3.05,.5,0]),panel(5.6,3.5,[3.05,.5,0]))
        left=label_pair('تغير طاقة الوضع','ΔU = 12 J',ENERGY).move_to(cards[0])
        right=label_pair('الشحنة الموجبة المنقولة','q = 2 C',CURRENT).move_to(cards[1])
        self.show(*cards,left,right)
        self.say('ننقل شحنة موجبة بين نقطتين في مجال كهربائي',4)
        expression=VGroup(eq('ΔV =',40,VOLT),frac('ΔU','q',VOLT)).arrange(RIGHT,buff=.25).move_to([0,-2,0])
        self.show(expression)
        self.say('فرق الجهد هو تغير طاقة الوضع مقسومًا على الشحنة',5)
        result=eq('ΔV = 12 J / 2 C = 6 V',37,VOLT).move_to(expression)
        self.play(ReplacementTransform(expression,result))
        self.say('كل كولوم يقابل تغيرا في الطاقة مقداره ستة جول',4)
        self.clear_stage()
        self.show(label_pair('نقطة البداية','A: 0 V',VOLT).move_to([-3,1,0]),
                  label_pair('نقطة النهاية','B: 6 V',VOLT).move_to([3,1,0]),
                  Arrow([-1.7,1,0],[1.7,1,0],color=VOLT))
        self.formula('ΔV = Vᴮ − Vᴬ',VOLT,y=-.8)
        self.say('نحدد نقطة مرجعية للجهد؛ والفرق بين نقطتين هو ما يهم هنا',5)
        self.finish('الفولت هو جول لكل كولوم','1 V = 1 J/C',VOLT)


if __name__=='__main__': render_scene(Scene03VoltageMeaning)
