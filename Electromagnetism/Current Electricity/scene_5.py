from common import *


class Scene05FromVoltageToCurrent(Lesson):
    def construct(self):
        self.begin(5,'من فرق الجهد إلى التيار','ما الذي يتغير عند إغلاق المفتاح؟')
        b=battery(np.array([-4,0,0])); lamp=bulb(np.array([4,0,0]))
        wires=VGroup(path([[-4,.65,0],[-4,1.65,0],[-.7,1.65,0]]),
                     path([[.7,1.65,0],[4,1.65,0],[4,.4,0]]),
                     path([[4,-.4,0],[4,-1.65,0],[-4,-1.65,0],[-4,-.65,0]]))
        lever=wire([-.7,1.65,0],[.55,2.2,0]); contacts=VGroup(Dot([-.7,1.65,0]),Dot([.7,1.65,0]))
        self.show(b,wires,lamp,lever,contacts)
        electrons=VGroup(*[charge('−',.11).move_to([x,-1.65,0]) for x in np.linspace(-3.3,3.3,11)])
        self.show(electrons)
        self.say('الموصل يحتوي أصلًا على إلكترونات حرة',4)
        self.say('الدائرة المفتوحة لا تسمح بتيار مستمر حول المسار',4)
        self.play(Transform(lever,wire([-.7,1.65,0],[.7,1.65,0])),run_time=.8)
        glow=Circle(.64,stroke_width=0,fill_color=ENERGY,fill_opacity=.16).move_to(lamp)
        self.show(glow)
        self.say('بعد الإغلاق ينشأ انجراف منظم بفعل المجال الكهربائي',4)
        self.play(FadeOut(electrons))
        route=[[-4,0,0],[-4,1.65,0],[4,1.65,0],[4,-1.65,0],[-4,-1.65,0],[-4,0,0]]
        direction=VGroup(Arrow([-1.5,.7,0],[1.5,.7,0],color=CURRENT),ar('التيار الاصطلاحي',25,CURRENT).move_to([0,.2,0]))
        self.show(direction)
        self.say('خارج البطارية: التيار الاصطلاحي من الموجب إلى السالب',3,color=CURRENT)
        self.flow(route,seconds=5)
        self.play(FadeOut(direction))
        self.show(Arrow([1.5,.7,0],[-1.5,.7,0],color=NEGATIVE),ar('انجراف الإلكترونات',25,NEGATIVE).move_to([0,.2,0]))
        self.say('في السلك المعدني تنجرف الإلكترونات عكس التيار الاصطلاحي',4)
        # Show drift only in metal wire; do not imply electrons cross electrolyte.
        es=VGroup(*[charge('−',.1).move_to([x,-1.65,0]) for x in np.linspace(-3,2.5,10)])
        self.show(es); self.play(es.animate.shift(RIGHT*.7),run_time=3,rate_func=linear)
        self.say('إغلاق الدائرة يجعل حركتها أكثر تنظيما',3)
        self.finish('الشحنة تدور في الدائرة والطاقة تتحول في المصباح')


if __name__=='__main__': render_scene(Scene05FromVoltageToCurrent)
