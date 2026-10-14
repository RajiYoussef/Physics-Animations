
from common import *


class Scene18FinalSummary(Lesson):
    def construct(self):
        self.begin(18,'باختصار','')
        data=[('فرق الجهد','ΔV = ΔU / q',VOLT),('التيار','I = ΔQ / Δt',CURRENT),
              ('المقاومة الأومية','V = IR',RESIST),('القدرة','P = VI',ENERGY),
              ('الطاقة عند قدرة ثابتة','E = Pt',ENERGY),('السعة','C = Q / V',VOLT)]
        for i,(title,formula,color) in enumerate(data):
            x=[-4.15,0,4.15][i%3];y=1.4 if i<3 else -.75
            self.show(panel(3.8,1.8,[x,y,0]),ar(title,23,color,width=3.4).move_to([x,y+.45,0]),eq(formula,29,color,width=3.4).move_to([x,y-.25,0]))
            self.wait(1)

        self.say('كل علاقة تجيب عن سؤال مختلف عن الشحنة والطاقة',5)
        self.clear_stage()
        self.show(ar('اختبار',34,ENERGY).move_to([0,2,0]),
                  eq('V = 12 V    •    R = 6 Ω    •    t = 10 s',34).move_to([0,1.1,0]),
                  ar('احسب التيار والقدرة والطاقة',30).move_to([0,.3,0]))
        self.say('أوقف الفيديو للحظة، ثم تابع لمقارنة إجابتك',7)

        answers=VGroup(eq('I = V / R = 2 A',35,CURRENT),eq('P = VI = 24 W',35,ENERGY),eq('E = Pt = 240 J',35,ENERGY)).arrange(DOWN,buff=.35).move_to([0,-1.15,0])
        for answer in answers:
            self.show(answer)
            self.wait(2)

        self.say('الشحنة محفوظة والطاقة تنتقل وتتحول في عناصر الدائرة',5)
        self.finish('افهم ما تقيسه الكمية، ثم اختر العلاقة المناسبة','V    •    I    •    R    •    P    •    C')

        # FINAL OUTRO
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

        NAME_COLOR = ENERGY
        TEXT_MAIN = INK

        outro_name = Text("Raji Youssef", font="DejaVu Sans", font_size=52, weight=BOLD, color=NAME_COLOR)
        outro_greeting = ar("مع أطيب التحيات", 32, NAME_COLOR)
        outro_message_ar = ar("اشترك في القناة", 31, TEXT_MAIN)
        channel_name = Text("The Physics Symphony", font="DejaVu Sans", font_size=34, weight=BOLD, color=CURRENT)
        separator = Line(LEFT * 1.5, RIGHT * 1.5, stroke_width=2.5, color=NAME_COLOR)

        outro = VGroup(outro_name, outro_greeting, separator, outro_message_ar, channel_name).arrange(DOWN, buff=.3).move_to(ORIGIN)

        separator.save_state()
        separator.scale(0.001)

        self.play(AddTextLetterByLetter(outro_name, time_per_char=.10), run_time=1.5)
        self.play(FadeIn(outro_greeting, shift=UP*.15), run_time=.8)
        self.play(Restore(separator), run_time=.9, rate_func=smooth)
        self.play(FadeIn(outro_message_ar, shift=UP*.15), FadeIn(channel_name, shift=UP*.15), run_time=1.2)
        self.wait(4)
        self.play(FadeOut(outro, shift=UP*.2), run_time=1.5)


if __name__=='__main__': render_scene(Scene18FinalSummary)
