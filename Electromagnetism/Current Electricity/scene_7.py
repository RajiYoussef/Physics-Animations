from common import *


class Scene07WaterAnalogy(Lesson):
    def construct(self):
        self.begin(7,'تشبيه يساعد على الفهم','كيف يشبه التيار تدفق الماء؟')
        self.show(panel(5.8,4,[-3.15,.3,0]),panel(5.8,4,[3.15,.3,0]))
        self.show(ar('الماء',30,NEGATIVE).move_to([-3.15,1.8,0]),ar('الكهرباء',30,CURRENT).move_to([3.15,1.8,0]))
        for y,left,right in [(1,'فرق الضغط','فرق الجهد'),(0,'حجم الماء في الثانية','الشحنة في الثانية'),(-1,'مضخة في مسار مغلق','بطارية في دائرة مغلقة')]:
            self.show(ar(left,26,width=5).move_to([-3.15,y,0]),ar(right,26,width=5).move_to([3.15,y,0]))
            self.wait(2)
        self.say('نستخدم التشبيه لفهم المعدل والمسار المغلق',4)
        self.clear_stage()
        for y,color,title in [(1.1,NEGATIVE,'ماء يعبر مقطع الأنبوب'),(-.8,CURRENT,'شحنة تعبر مقطع السلك')]:
            self.show(ar(title,27,color).move_to([0,y+.65,0]),
                      Line([-5,y-.25,0],[5,y-.25,0],color=EDGE),Line([-5,y+.25,0],[5,y+.25,0],color=EDGE),
                      DashedLine([0,y-.4,0],[0,y+.4,0],color=ENERGY))
        packets=VGroup(*[Dot([x,y,0],radius=.07,color=color) for y,color in [(1.1,NEGATIVE),(-.8,CURRENT)] for x in np.linspace(-4,3,15)])
        self.show(packets); self.play(packets.animate.shift(RIGHT*1.4),run_time=3,rate_func=linear)
        self.say('معدل أكبر يعني كمية أكبر تعبر خلال الزمن نفسه',4)
        #self.say('حدود التشبيه: الشحنة ليست ماءً، والإلكترون لا يُستهلك في المصباح',5,color=ENERGY)
        #self.finish('التشبيه يوضح الفكرة والقوانين تصف الكهرباء','I = ΔQ / Δt',CURRENT)


if __name__=='__main__': render_scene(Scene07WaterAnalogy)
