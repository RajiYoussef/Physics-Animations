from common import *


class Scene06CurrentDefinition(Lesson):
    def construct(self):
        self.begin(6,'كيف نقيس التيار؟','نعد الشحنة التي تعبر مقطعًا خلال زمن معلوم')
        tube=VGroup(Line([-5,.35,0],[5,.35,0],color=EDGE),Line([-5,1.35,0],[5,1.35,0],color=EDGE))
        gate=DashedLine([0,0,0],[0,1.7,0],color=ENERGY)
        self.show(tube,gate,ar('مقطع القياس',25,ENERGY).move_to([0,2.1,0]))
        note=ar('كل علامة تمثل حزمة شحنة مقدارها كولوم واحد',24,MUTED).move_to([0,-.35,0]); self.show(note)
        clock=ValueTracker(0)
        time_value=DecimalNumber(0,num_decimal_places=1,font_size=33,color=INK,mob_class=Text).move_to([-3,-1.3,0])
        count_value=Integer(0,font_size=33,color=CURRENT,mob_class=Text).move_to([3,-1.3,0])
        time_value.add_updater(lambda m:m.set_value(clock.get_value()))
        count_value.add_updater(lambda m:m.set_value(sum(clock.get_value()>=t for t in [.25,.75,1.25,1.75])))
        self.show(eq('t (s)',25).move_to([-3,-.8,0]),eq('Q (C)',25,CURRENT).move_to([3,-.8,0]),time_value,count_value)
        dots=VGroup(*[Dot(radius=.11,color=CURRENT) for _ in range(4)])
        for i,d in enumerate(dots):
            d.add_updater(lambda m,i=i:m.move_to([(clock.get_value()-(.25+.5*i))*2,.85,0]))
            d.update()
        self.add(dots)
        self.say('نبدأ القياس راقب عدد الحزم التي تعبر الخط',3)
        self.play(clock.animate.set_value(2),run_time=4,rate_func=linear)
        time_value.clear_updaters();count_value.clear_updaters();dots.clear_updaters()
        self.say('عبر 4 كولوم خلال ثانيتين',4)
        self.formula('I = ΔQ / Δt = 4 C / 2 s = 2 A',CURRENT,y=-2.2)
        self.say('هذه قيمة التيار المتوسط خلال فترة القياس',4)
        self.finish('الأمبير هو كولوم واحد في كل ثانية','1 A = 1 C/s',CURRENT)


if __name__=='__main__': render_scene(Scene06CurrentDefinition)
