from common import *


class Scene12EnergyVsPower(Lesson):
    def construct(self):
        self.begin(12,'الطاقة والقدرة: الكمية والمعدل','هل القدرة الأكبر تعني دائما طاقة كلية أكبر؟')
        axes=Axes(x_range=[0,6,1],y_range=[0,60,20],x_length=7.5,y_length=3.3,
                  axis_config={'include_tip':False,'color':EDGE}).move_to([-1,.25,0])
        labels=VGroup(eq('t (s)',24).next_to(axes.x_axis,DOWN),eq('E (J)',24,ENERGY).next_to(axes.y_axis,UP),
                      *[eq(str(v),18,MUTED).next_to(axes.c2p(v,0),DOWN,buff=.12) for v in [2,4,6]],
                      *[eq(str(v),18,MUTED).next_to(axes.c2p(0,v),LEFT,buff=.12) for v in [20,40,60]])
        slow=axes.plot(lambda t:10*t,x_range=[0,6],color=CURRENT)
        fast=axes.plot(lambda t:30*t,x_range=[0,2],color=RESIST)
        self.show(axes,labels)
        self.play(Create(slow),run_time=3)
        self.show(eq('10 W × 6 s',27,CURRENT).move_to([4.3,.3,0]))
        self.play(Create(fast),run_time=1)
        self.show(eq('30 W × 2 s',27,RESIST).move_to([4.3,1.1,0]))
        target=DashedLine(axes.c2p(0,60),axes.c2p(6,60),color=ENERGY)
        self.show(target)
        self.say('الجهازان يحولان 60 جول، لكن خلال زمنين مختلفين',5)
        self.formula('E = Pt = 60 J',ENERGY,y=-2.15)
        self.say('ميل الرسم يمثل القدرة والقيمة النهائية تمثل الطاقة',5)
        self.clear_stage()
        self.show(label_pair('مثال استهلاك','1000 W × 1 h',ENERGY).move_to([0,1.2,0]))
        self.formula('1 kWh = 3 600 000 J',ENERGY,y=-.4)
        self.say('الكيلوواط ساعة وحدة طاقة، وليست وحدة قدرة',5)
        self.finish('لمعرفة الطاقة نحتاج القدرة والزمن معا','E = Pt',ENERGY)


if __name__=='__main__': render_scene(Scene12EnergyVsPower)
