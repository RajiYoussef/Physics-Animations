from common import *


class Scene09OhmsLaw(Lesson):
    def construct(self):
        self.begin(9,'قانون أوم','كيف تتغير شدة التيار عندما نغير الجهد؟')
        axes=Axes(x_range=[0,12,3],y_range=[0,4,1],x_length=6.3,y_length=3.5,
                  axis_config={'color':EDGE,'include_tip':False}).move_to([-2,.3,0])
        labels=VGroup(eq('V (V)',24,VOLT).next_to(axes.x_axis,DOWN),eq('I (A)',24,CURRENT).next_to(axes.y_axis,UP))
        ticks=VGroup(*[eq(str(v),18,MUTED).next_to(axes.c2p(v,0),DOWN,buff=.12) for v in [3,6,9,12]],
                     *[eq(str(i),18,MUTED).next_to(axes.c2p(0,i),LEFT,buff=.12) for i in [1,2,3,4]])
        line=axes.plot(lambda v:v/3,x_range=[0,12],color=CURRENT)
        self.show(axes,labels,ticks);self.play(Create(line))
        self.show(eq('R = 3 Ω',34,RESIST).move_to([3.65,1.7,0]))
        v=ValueTracker(3)
        dot=always_redraw(lambda:Dot(axes.c2p(v.get_value(),v.get_value()/3),color=ENERGY,radius=.09))
        guide=always_redraw(lambda:DashedLine(axes.c2p(v.get_value(),0),axes.c2p(v.get_value(),v.get_value()/3),color=VOLT))
        readout=always_redraw(lambda:VGroup(eq(f'V = {v.get_value():.0f} V',31,VOLT),eq(f'I = {v.get_value()/3:.0f} A',31,CURRENT)).arrange(DOWN,buff=.3).move_to([3.65,.2,0]))
        self.add(dot,guide,readout)
        self.say('لمقاومة أومية ثابتة: العلاقة خط مستقيم يمر بنقطة الأصل',4)
        self.play(v.animate.set_value(6),run_time=2,rate_func=linear)
        self.say('ضاعفنا الجهد, فتضاعف التيار',4)
        self.play(v.animate.set_value(12),run_time=2,rate_func=linear)
        self.formula('V = IR',VOLT,y=-2.25)
        self.say('يبقى ذلك صحيحا ما دامت المقاومة ثابتة',5)
        for mob in [dot,guide,readout]:mob.clear_updaters()
        self.clear_stage()
        self.show(label_pair('الجهد ثابت','V = 12 V',VOLT).move_to([0,1.7,0]),
                  label_pair('قبل زيادة المقاومة','R = 3 Ω    →    I = 4 A',CURRENT).move_to([-3.2,-.1,0]),
                  label_pair('بعد زيادة المقاومة','R = 6 Ω    →    I = 2 A',RESIST).move_to([3.2,-.1,0]))
        self.say('عند الجهد نفسه: مضاعفة المقاومة تخفض التيار إلى النصف',5)
        self.finish('قانون أوم يصف العناصر الأومية في ظروف ثابتة','V = IR',VOLT)


if __name__=='__main__': render_scene(Scene09OhmsLaw)
