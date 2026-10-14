from common import *


class Scene02FieldVsPotential(Lesson):
    def construct(self):
        self.begin(2,'المجال الكهربائي والجهد','هل الجهد والمجال هما الشيء نفسه؟')
        axes=Axes(x_range=[0,6,1],y_range=[0,7,1],x_length=7,y_length=3.3,
                  axis_config={'include_tip':False,'color':EDGE}).move_to([-1,.3,0])
        line=axes.plot(lambda x:6-x,x_range=[0,6],color=VOLT)
        levels=VGroup(*[DashedLine(axes.c2p(0,v),axes.c2p(6-v,v),color=EDGE) for v in [2,4,6]])
        labels=VGroup(eq('V',25,VOLT).next_to(axes.y_axis,UP),eq('x',25).next_to(axes.x_axis,RIGHT),
                      *[eq(str(v),21,VOLT).next_to(axes.c2p(0,v),LEFT,buff=.15) for v in [2,4,6]])
        self.show(axes,levels,labels); self.play(Create(line))
        self.say('الرسم يبين كيف يتغير الجهد مع الموضع',4)
        field=Arrow([3.4,.65,0],[5.6,.65,0],buff=0,color=CURRENT)
        field_label=ar('اتجاه المجال',24,CURRENT,width=3).move_to([4.5,1.25,0])
        self.show(field,field_label)
        self.formula('Eₓ = −ΔV / Δx',CURRENT)
        self.say('في مجال منتظم: المجال يتجه نحو تناقص الجهد',5)
        positive=charge().move_to([3.5,-.2,0]); negative=charge('−').move_to([5.5,-.9,0])
        self.show(positive,negative)
        self.play(positive.animate.shift(RIGHT*1.7),negative.animate.shift(LEFT*1.7),run_time=2)
        self.say('القوة مع المجال للشحنة الموجبة، وعكسه للسالبة',5)
        self.finish('الجهد كمية قياسية؛ والمجال له مقدار واتجاه','F = qE',CURRENT)


if __name__=='__main__': render_scene(Scene02FieldVsPotential)
