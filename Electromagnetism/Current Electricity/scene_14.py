from common import *


class Scene14ParallelCircuit(Lesson):
    def construct(self):
        self.begin(14,'التوصيل على التوازي','كيف يتوزع التيار بين فرعين؟')
        b=battery(np.array([-4.8,0,0]),'6 V')
        supply=VGroup(path([[-4.8,.65,0],[-4.8,1.8,0],[-2.8,1.8,0],[-2.8,-.7,0]]),
                      path([[3.4,1.2,0],[3.4,-1.7,0],[-4.8,-1.7,0],[-4.8,-.65,0]]))
        branches=VGroup()
        for y,r in [(1.2,'3 Ω'),(-.7,'6 Ω')]:
            branches.add(VGroup(wire([-2.8,y,0],[-1.8,y,0]),wire([-1.1,y,0],[-.675,y,0]),
                                resistor(np.array([0,y,0]),label=r),wire([.675,y,0],[3.4,y,0])))
        switches=VGroup(wire([-1.8,1.2,0],[-1.1,1.2,0]),wire([-1.8,-.7,0],[-1.1,-.7,0]))
        nodes=VGroup(*[Dot([x,y,0],color=CURRENT,radius=.065) for x in [-2.8,3.4] for y in [1.2,-.7]])
        self.show(b,supply,branches,switches,nodes)
        top=eq('I₁ = 2 A',29,CURRENT).move_to([1.9,1.65,0]);bottom=eq('I₂ = 1 A',29,CURRENT).move_to([1.9,-.2,0])
        lower_voltage=eq('6 V',26,VOLT).move_to([0,-1.25,0])
        self.show(top,bottom,eq('6 V',26,VOLT).move_to([0,.6,0]),lower_voltage)
        self.say('الفرعان متصلان بين العقدتين نفسيهما لذا جهدهما متساو',5)
        formula=self.formula('I = I₁ + I₂ = 2 + 1 = 3 A',CURRENT)
        self.say('التيار الأكبر يمر في المقاومة الأصغر',4)
        # Individual packets each follow a complete physical loop. Interleaved
        # 2:1 scheduling conserves packet count at every split and merge.
        loops=[]
        for y in [1.2,1.2,-.7]:
            pts=[[-4.8,0,0],[-4.8,1.8,0],[-2.8,1.8,0],[-2.8,y,0],[3.4,y,0],[3.4,-1.7,0],[-4.8,-1.7,0],[-4.8,0,0]]
            loops.append(path(pts))
        dots=VGroup(*[Dot([-4.8,0,0],radius=.065,color=CURRENT) for _ in range(9)])
        self.add(dots)
        self.play(LaggedStart(*[MoveAlongPath(d,loops[i%3],rate_func=linear) for i,d in enumerate(dots)],lag_ratio=.12),run_time=6)
        self.remove(dots,*dots)
        self.say(' ماذا يحدث عند فتح مفتاح الفرع السفلي؟',5)
        self.play(Transform(switches[1],wire([-1.8,-.7,0],[-1.2,-.25,0])),
                  Transform(bottom,eq('I₂ = 0 A',29,MUTED).move_to(bottom)),
                  Transform(lower_voltage,eq('0 V',26,MUTED).move_to(lower_voltage)),
                  Transform(formula,eq('I = 2 + 0 = 2 A',36,CURRENT).move_to(formula)))
        self.say('يبقى تيار الفرع العلوي كما هو مع مصدر جهد مثالي',5)
        self.show(eq('6 V',24,VOLT).move_to([-1.55,-1.25,0]))
        self.say('الجهد كله عبر المفتاح المفتوح والجهد على مقاومة الفرع يساوي صفرا',5)
        self.flow([[-4.8,0,0],[-4.8,1.8,0],[-2.8,1.8,0],[-2.8,1.2,0],[3.4,1.2,0],[3.4,-1.7,0],[-4.8,-1.7,0],[-4.8,0,0]],seconds=4,count=12)
        self.finish('التوازي: جهد واحد وتيارات فروع تتجمع','V₁ = V₂    •    I = I₁ + I₂',VOLT)


if __name__=='__main__': render_scene(Scene14ParallelCircuit)
