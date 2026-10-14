from common import *


class Scene10ElectricalPower(Lesson):
    def construct(self):
        self.begin(10,'القدرة الكهربائية','أي جهاز يحول طاقة أكثر في الثانية؟')
        self.show(panel(5.7,3.9,[-3.1,.4,0]),panel(5.7,3.9,[3.1,.4,0]))
        self.show(label_pair('الجهاز الأول','P = 10 W',ENERGY).move_to([-3.1,1.3,0]),
                  label_pair('الجهاز الثاني','P = 30 W',ENERGY).move_to([3.1,1.3,0]))
        t=ValueTracker(0)
        bars=[]
        for x,power in [(-3.1,10),(3.1,30)]:
            outline=Rectangle(width=4.5,height=.38,color=EDGE).move_to([x,-.25,0]);self.show(outline)
            bar=always_redraw(lambda x=x,p=power:Rectangle(width=max(.005,4.5*p*t.get_value()/90),height=.36,
                               fill_color=ENERGY,fill_opacity=1,stroke_width=0).move_to([x-2.25+max(.005,4.5*p*t.get_value()/90)/2,-.25,0]))
            reading=always_redraw(lambda x=x,p=power:eq(f'E = {p*t.get_value():.0f} J',30,ENERGY).move_to([x,-1,0]))
            self.add(bar,reading);bars.extend([bar,reading])
        timer=always_redraw(lambda:eq(f't = {t.get_value():.1f} s',29).move_to([0,-2,0]));self.add(timer)
        self.say('نقارن الطاقة المحولة خلال الزمن نفسه',4)
        self.play(t.animate.set_value(1),run_time=2,rate_func=linear)
        self.say('بعد ثانية: 10 جول مقابل 30 جول',4)
        self.play(t.animate.set_value(3),run_time=3,rate_func=linear)
        self.say('الطاقة تتراكم مع الزمن والقدرة هنا ثابتة',4)
        for mob in bars+[timer]:mob.clear_updaters()
        self.finish('القدرة هي معدل انتقال الطاقة أو تحولها','P = ΔE / Δt    •    1 W = 1 J/s',ENERGY)


if __name__=='__main__': render_scene(Scene10ElectricalPower)
