"""Shared native diagram, with one physical state driving all visible quantities."""
import json
import numpy as np
from manim import *
from science_anim.style import label
from math_type import tex
from model import Slab
from settings import ROOT, WHITE, BLUE, YELLOW, GREY

def ar(text, size=29, color=WHITE):
    return label(text, size=size, font='Arial', color=color)

class OpeningScene(Scene):
    def setup(self):
        self.beats = []
        self.caption = None
        self.add(ar('.',18,GREY).move_to([4.8,-3.65,0]))

    def beat(self, name):
        self.beats.append({'name':name,'start':round(self.time,3)})

    def say(self, text):
        new = ar(text,29).move_to([0,3.35,0])
        if self.caption is None:
            self.play(FadeIn(new),run_time=.8)
        else:
            self.play(FadeOut(self.caption),FadeIn(new),run_time=.8)
        self.caption = new

    def finish(self):
        for i,b in enumerate(self.beats):
            b['end'] = self.beats[i+1]['start'] if i+1<len(self.beats) else round(self.time,3)
        (ROOT/'review').mkdir(exist_ok=True)
        self.renderer.camera.get_image().save(ROOT/'review'/f'{type(self).__name__}_end.png')
        (ROOT/'review'/f'{type(self).__name__}_timing.json').write_text(json.dumps(self.beats,ensure_ascii=False,indent=2),encoding='utf-8')

class SlabDiagram:
    def __init__(self):
        self.model=Slab()
        self.vc=ValueTracker(-3)
        self.rho=ValueTracker(0)
        self.probe=ValueTracker(.3)
        self.left=-5.6; self.right=-.9; self.bottom=-2.25
        self.height=4.1
        self.boundaries=VGroup(*[Line([self.left,self.Y(y),0],[self.right,self.Y(y),0],color=WHITE,stroke_width=3) for y in (0,3)])
        self.charges=VGroup(*[tex(sign,23,color=BLUE).move_to([x,self.Y(y)+dy,0]) for y,sign,dy in [(0,'+',-.24),(3,'-',.24)] for x in np.linspace(self.left+.25,self.right-.25,7)])
        self.boundary_labels=VGroup(tex('V_0=0',28).move_to([-6.1,self.Y(0)-.65,0]),tex('V_1',28).move_to([-6.1,self.Y(3),0]))
        self.vtop=DecimalNumber(-3,num_decimal_places=1,mob_class=Text,font_size=28,color=BLUE).move_to([-6.05,self.Y(3)-.45,0])
        self.vtop.add_updater(lambda m:m.set_value(self.vc.get_value()))
        self.levels=VGroup(*[Line([self.left+.1,self.Y(y),0],[self.right-.1,self.Y(y),0],stroke_width=1,color=BLUE,stroke_opacity=.5) for y in (.5,1,1.5,2,2.5)])
        self.height_axis=VGroup(Arrow([-.5,self.Y(0),0],[-.5,self.Y(3)+.2,0],buff=0,color=GREY,stroke_width=1.5),tex('y',23).move_to([-.2,self.Y(3)+.3,0]),tex('0',20).move_to([-.2,self.Y(0),0]),tex('H=3',22).move_to([-.1,self.Y(3)-.15,0]))
        self.level_values=VGroup()
        for y in (1.,2.):
            value=DecimalNumber(self.V(y),num_decimal_places=1,mob_class=Text,font_size=22,color=BLUE).move_to([self.left-.4,self.Y(y),0])
            value.add_updater(lambda m,y=y:m.set_value(self.V(y)))
            self.level_values.add(value)
        self.arrows=always_redraw(lambda:VGroup(*[Arrow([x,self.Y(y),0],[x,self.Y(y)+.30*self.E(y),0],buff=0,color=BLUE,stroke_width=3,max_tip_length_to_length_ratio=.24) for x in (-5.1,-3.8,-2.5,-1.3) for y in (.3,1.25,2.2)]))
        self.axes=Axes(x_range=[0,3,1],y_range=[-6,0,2],x_length=4.6,y_length=3.5,tips=False,axis_config={'color':GREY,'stroke_width':2},x_axis_config={'include_numbers':False},y_axis_config={'include_numbers':False}).move_to([3.5,-.1,0])
        self.axis_labels=VGroup(tex('y',27).next_to(self.axes.x_axis,RIGHT,buff=.15),tex('V',27).next_to(self.axes.y_axis,UP,buff=.24))
        self.ticks=VGroup(*[tex(str(y),21,color=GREY).next_to(self.axes.c2p(y,0),UP,buff=.12) for y in (1,2,3)],*[tex(str(v),21,color=GREY).next_to(self.axes.c2p(0,v),LEFT,buff=.13) for v in (-2,-4,-6)])
        self.curve=always_redraw(lambda:ParametricFunction(lambda y:self.axes.c2p(y,self.V(y)),t_range=[0,3,.025],color=BLUE,stroke_width=4))
        self.dot=always_redraw(lambda:Dot([-3.25,self.Y(self.probe.get_value()),0],radius=.075,color=YELLOW))
        self.graph_dot=always_redraw(lambda:Dot(self.axes.c2p(self.probe.get_value(),self.V(self.probe.get_value())),radius=.07,color=YELLOW))
        self.crosshair=always_redraw(lambda:DashedLine(self.axes.c2p(self.probe.get_value(),0),self.axes.c2p(self.probe.get_value(),self.V(self.probe.get_value())),color=YELLOW,stroke_width=1.3))
        self.readout=VGroup(tex('y=',26),DecimalNumber(.3,num_decimal_places=1,mob_class=Text,font_size=26),tex('V=',26),DecimalNumber(-.3,num_decimal_places=2,mob_class=Text,font_size=26)).arrange(RIGHT,buff=.30).move_to([3.4,-2.65,0])
        self.readout[1].add_updater(lambda m:m.set_value(self.probe.get_value()))
        self.readout[3].add_updater(lambda m:m.set_value(self.V(self.probe.get_value())))

    def Y(self,y): return self.bottom+self.height*y/3
    def V(self,y): return self.model.potential(y,self.vc.get_value(),self.rho.get_value())
    def E(self,y): return self.model.field(y,self.vc.get_value(),self.rho.get_value())
    def plot(self): return VGroup(self.axes,self.axis_labels,self.ticks,self.curve)
    def field(self): return VGroup(self.boundaries,self.charges,self.boundary_labels,self.vtop)

