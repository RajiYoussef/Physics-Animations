from manim import VGroup, Dot, Circle, ArcBetweenPoints, WHITE, BLACK, RIGHT
from math_type import tex

def hbar_character(height=1.0):
    body=tex(r'\hbar',size=64,color='#37BDF0').scale_to_fit_height(.65)
    eye1=Circle(radius=.085,fill_color=WHITE,fill_opacity=1,stroke_width=0).move_to([-.12,.35,0])
    eye2=eye1.copy().move_to([.18,.35,0])
    pupils=VGroup(Dot(eye1.get_center()+RIGHT*.012,radius=.038,color=BLACK),Dot(eye2.get_center()+RIGHT*.012,radius=.038,color=BLACK))
    arms=VGroup(ArcBetweenPoints([-.1,.04,0],[-.55,.12,0],angle=-.7,color='#37BDF0',stroke_width=5),ArcBetweenPoints([.28,.04,0],[.72,.12,0],angle=.7,color='#37BDF0',stroke_width=5),Dot([-.55,.12,0],radius=.09,color='#37BDF0'),Dot([.72,.12,0],radius=.09,color='#37BDF0'))
    return VGroup(arms,body,eye1,eye2,pupils).scale_to_fit_height(height)
