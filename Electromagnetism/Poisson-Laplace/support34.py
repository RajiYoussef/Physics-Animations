import json
from dataclasses import dataclass
import numpy as np
from manim import *
from science_anim.style import label
from math_type import tex
from settings34 import ROOT, WHITE, BLUE, YELLOW, GREY, GREEN, RED

def ar(text, size=29, color=WHITE):
    obj = label(text, size=size, font='Arial', color=color)
    if obj.width > 12.6:
        obj.scale_to_fit_width(12.6)
    return obj

def number(value, size=25, color=WHITE, decimals=1):
    return DecimalNumber(value, num_decimal_places=decimals, mob_class=Text,
                         font_size=size, color=color)

@dataclass(frozen=True)
class PlateModel:
    length: float = 3.0
    v0: float = 0.0

    def potential(self, x, v1):
        return self.v0 + (v1-self.v0)*x/self.length

    def field(self, v1):
        return -(v1-self.v0)/self.length

class LessonScene(Scene):
    def setup(self):
        self.beats = []
        self.caption = None

    def beat(self, name):
        self.beats.append({'name': name, 'start': round(self.time, 3)})

    def say(self, text):
        new = ar(text, 31).move_to([0, 3.42, 0])
        if self.caption is None:
            self.play(FadeIn(new, shift=DOWN*.12), run_time=.8)
        else:
            self.play(FadeOut(self.caption), FadeIn(new, shift=DOWN*.1), run_time=.8)
        self.caption = new

    def finish(self):
        for i, beat in enumerate(self.beats):
            beat['end'] = self.beats[i+1]['start'] if i+1<len(self.beats) else round(self.time, 3)
        review = ROOT/'review'
        review.mkdir(exist_ok=True)
        (review/f'{type(self).__name__}_timing.json').write_text(json.dumps(self.beats, ensure_ascii=False, indent=2), encoding='utf-8')
        self.renderer.camera.get_image().save(review/f'{type(self).__name__}_end.png')

def graph_axes(center, width=4.6, height=3.4, ymax=10, xlabel=r'x\;(\mathrm{m})', ylabel=r'V\;(\mathrm{V})'):
    axes = Axes(x_range=[0, 3.3, 1], y_range=[0, ymax, 2], x_length=width,
                y_length=height, tips=False,
                axis_config={'color': GREY, 'stroke_width': 1.7, 'include_ticks': False}).move_to(center)
    labels = VGroup(tex(xlabel, 25).next_to(axes.x_axis, DOWN, buff=.44),
                    tex(ylabel, 25).next_to(axes.y_axis, UP, buff=.18))
    ticks = VGroup()
    for x in (0, 1, 2, 3):
        p = axes.c2p(x, 0)
        ticks.add(Line(p+UP*.045, p+DOWN*.045, color=GREY), tex(str(x), 19, GREY).next_to(p, DOWN, buff=.12))
    for y in range(2, ymax, 2):
        p = axes.c2p(0, y)
        ticks.add(Line(p+LEFT*.045, p+RIGHT*.045, color=GREY), tex(str(y), 19, GREY).next_to(p, LEFT, buff=.12))
    grid = VGroup(*[Line(axes.c2p(0,y), axes.c2p(3,y), color=GREY, stroke_opacity=.15, stroke_width=1) for y in range(2,ymax,2)])
    return axes, VGroup(axes, labels, ticks, grid)

class PlatePlot:
    def __init__(self):
        self.model = PlateModel()
        self.v1 = ValueTracker(6)
        self.probe = ValueTracker(.3)
        self.axes, self.frame = graph_axes([3.65, .1, 0])
        self.plates = VGroup(*[Line([x,-1.75,0],[x,1.9,0],color=c,stroke_width=6) for x,c in [(-5.9,GREEN),(-1.1,BLUE)]])
        self.baseline = Arrow([-5.9,-2.1,0],[-.8,-2.1,0],buff=0,color=GREY,stroke_width=2)
        self.ends = VGroup(tex(r'x=0',23).move_to([-5.9,-2.48,0]),tex(r'x=L',23).move_to([-1.1,-2.48,0]),tex(r'L=3\;\mathrm{m}',25).move_to([-3.5,-2.6,0]))
        self.left_label = tex(r'V_0=0\;\mathrm{V}',27,GREEN).move_to([-5.5,2.35,0])
        self.right_label = VGroup(tex(r'V_1=',26,BLUE), number(6,26,BLUE), tex(r'\mathrm{V}',25,BLUE)).arrange(RIGHT,buff=.12).move_to([-1.65,2.35,0])
        self.right_label[1].add_updater(lambda m:m.set_value(self.v1.get_value()))
        self.curve = always_redraw(lambda:Line(self.axes.c2p(0,0),self.axes.c2p(3,self.v1.get_value()),color=BLUE,stroke_width=4))
        self.graph_dot = always_redraw(lambda:Dot(self.axes.c2p(self.probe.get_value(),self.V(self.probe.get_value())),radius=.08,color=YELLOW))
        self.physical_dot = always_redraw(lambda:Dot(self.P(self.probe.get_value()),radius=.1,color=YELLOW))
        self.projection = always_redraw(lambda:DashedLine(self.axes.c2p(self.probe.get_value(),0),self.axes.c2p(self.probe.get_value(),self.V(self.probe.get_value())),color=YELLOW,stroke_width=1.5))
        self.guide = always_redraw(lambda:DashedLine(self.P(self.probe.get_value())+DOWN*1.8,self.P(self.probe.get_value())+UP*1.6,color=YELLOW,stroke_width=1,stroke_opacity=.5))
        self.readout = VGroup(tex(r'x=',25,YELLOW),number(.3,25,YELLOW),tex(r'\mathrm{m}',23,YELLOW),tex(r'V=',25,YELLOW),number(.6,25,YELLOW),tex(r'\mathrm{V}',23,YELLOW)).arrange(RIGHT,buff=.13).move_to([3.7,-2.85,0])
        self.readout[1].add_updater(lambda m:m.set_value(self.probe.get_value()))
        self.readout[4].add_updater(lambda m:m.set_value(self.V(self.probe.get_value())))
        self.arrows = always_redraw(lambda:VGroup(*[Arrow(self.P(x)+UP*y,self.P(x)+UP*y+RIGHT*.34*self.model.field(self.v1.get_value()),buff=0,color=BLUE,stroke_width=3,max_tip_length_to_length_ratio=.22) for x in (.9,1.8,2.7) for y in (-1.1,0,1.1)]))

    def P(self,x):
        return np.array([-5.9+4.8*x/3,.1,0])

    def V(self,x):
        return self.model.potential(x,self.v1.get_value())

    def physical(self):
        return VGroup(self.plates,self.baseline,self.ends,self.left_label,self.right_label)

    def probes(self):
        return VGroup(self.graph_dot,self.physical_dot,self.projection,self.guide,self.readout)
