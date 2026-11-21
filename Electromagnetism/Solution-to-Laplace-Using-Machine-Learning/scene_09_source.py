from visual_helpers import *

class SourceBook(Lesson):
    chapter=9
    def construct(self):
        self.heading('المصدر :')
        title=Text('Elementary Electromagnetism',font_size=34)
        subtitle=Text('Using Python',font_size=30,color=CYAN)
        author=Text('Anders Malthe-Sørenssen',font_size=28)
        section=Text('Section 5.9 | Numerical solutions: Machine learning methods',font_size=21)
        date=Text('22 October 2022',font_size=22,color=MUTED)
        group=VGroup(title,subtitle,author,section,date).arrange(DOWN,buff=.4)
        if group.width>12:group.scale_to_fit_width(12)
        with self.beat(0):
            self.play(LaggedStart(*[FadeIn(m) for m in group],lag_ratio=.2),run_time=1.5)
            self.caption('يستند هذا الشرح إلى القسم 5.9 من الكتاب')

if __name__=='__main__':
    run_independent(SourceBook)
