from common import *


class Scene17CameraFlash(Lesson):
    def construct(self):
        self.begin(17,'تطبيق: فلاش الكاميرا','كيف نطلق طاقة مخزنة خلال زمن قصير؟')
        # Functional energy diagram, explicitly not a literal wiring schematic.
        blocks=VGroup(*[panel(3.3,2.9,[x,.5,0]) for x in [-4.3,0,4.3]])
        self.show(*blocks)
        self.show(ar('بطارية ودائرة شحن',25,width=3).move_to([-4.3,1.35,0]),
                  ar('مكثف',28).move_to([0,1.35,0]),ar('مصباح الفلاش',26).move_to([4.3,1.35,0]))
        cap=capacitor(np.array([0,.1,0]),height=1.15,gap=.7,n=3)
        lamp=bulb(np.array([4.3,.2,0]))
        self.show(cap[0],cap[1],lamp,eq('DC',34,VOLT).move_to([-4.3,.25,0]))
        charging=Arrow([-2.55,.45,0],[-1.75,.45,0],buff=0,color=VOLT)
        discharge=Arrow([1.75,.45,0],[2.55,.45,0],buff=0,color=ENERGY)
        self.show(ar('مخطط  مبسط',23,MUTED).move_to([0,-1.35,0]),charging)
        energy=ValueTracker(0)
        bar=always_redraw(lambda:Rectangle(width=max(.01,8*energy.get_value()/10),height=.22,stroke_width=0,
                         fill_color=ENERGY,fill_opacity=1).move_to([-4+max(.01,8*energy.get_value()/10)/2,-2,0]))
        self.show(Rectangle(width=8,height=.25,color=EDGE).move_to([0,-2,0]))
        reading=always_redraw(lambda:eq(f'U = {energy.get_value():.1f} J',27,ENERGY).move_to([0,-2.5,0]))
        self.add(bar,reading)
        self.say('دائرة الشحن ترفع الجهد وتجمع الطاقة في المكثف تدريجيا',4)
        self.play(energy.animate.set_value(10),FadeIn(cap[2]),FadeIn(cap[3]),run_time=5,rate_func=smooth)
        self.say('نفرض أن الطاقة المخزنة 10 جول',4)
        self.play(FadeOut(charging),FadeIn(discharge))
        self.say('عند التشغيل تنتقل الطاقة إلى مصباح الفلاش بسرعة',3)
        glow=Circle(.8,stroke_width=0,fill_color=ENERGY,fill_opacity=.45).move_to(lamp)
        self.add(glow)
        self.play(energy.animate.set_value(0),FadeOut(cap[2]),FadeOut(cap[3]),FadeOut(glow),run_time=.8,rate_func=linear)
        self.say('',5)
        bar.clear_updaters();reading.clear_updaters()
        self.clear_stage()
        self.show(eq('Δt = 0.01 s    •    ΔE = 10 J',35,ENERGY).move_to([0,1.2,0]))
        self.formula('Pₐᵥ = 10 / 0.01 = 1000 W',ENERGY,y=-.1)
        #self.say('هذه قدرة كهربائية متوسطة ليست كلها ضوءًا مفيدًا',5)
        self.finish('طاقة محدودة خلال زمن قصير تعطي قدرة كبيرة','Pₐᵥ = ΔE / Δt',ENERGY)


if __name__=='__main__': render_scene(Scene17CameraFlash)
