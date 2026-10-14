"""Shared visual language for the Arabic electricity course (Manim CE).

Arabic is shaped by Pango as complete strings. Never reverse/reshape it or
animate its individual glyphs. Equations use separate left-to-right objects.
All geometry is authored for a 16:9 frame; quantities are schematic, not scale.
"""
from manim import *
import manimpango
import numpy as np
import os
from pathlib import Path
from html import escape

BG = '#0B1426'
PANEL = '#13223A'
EDGE = '#2A405A'
INK = '#F0F5FF'
MUTED = '#A9BBD0'
VOLT = '#AE9BFF'
CURRENT = '#4EDFD0'
RESIST = '#FFAD78'
ENERGY = '#FFDA78'
NEGATIVE = '#70B9FF'
POSITIVE = '#FF929D'
ROOT = Path(__file__).resolve().parent
_fonts = set(manimpango.list_fonts())
AR_FONT = os.environ.get('ELECTRICITY_AR_FONT') or next(
    (f for f in ['Noto Sans Arabic', 'Tahoma', 'DejaVu Sans', 'Arial'] if f in _fonts), '')
LATIN_FONT = next((f for f in ['Segoe UI', 'DejaVu Sans', 'Arial'] if f in _fonts), '')


def fit(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def ar(text, size=30, color=INK, width=11.8, bold=False):
    """Whole-string shaping preserves Arabic joins and right-to-left order."""
    # Manim 0.21 Text drops some single-word RTL strings. MarkupText preserves
    # Pango's complete glyph output; escaping makes user text literal markup.
    return fit(MarkupText(escape(text), font=AR_FONT, font_size=size, color=color,
                          weight=BOLD if bold else NORMAL, disable_ligatures=False), width)


def eq(text, size=34, color=INK, width=11.8):
    """Unicode equations: no LaTeX installation or Arabic/Latin bidi mixing."""
    return fit(Text(text, font=LATIN_FONT, font_size=size, color=color), width)


def frac(numerator, denominator, color=INK):
    top, bottom = eq(numerator, 32, color), eq(denominator, 32, color)
    line = Line(LEFT * max(top.width, bottom.width) / 2,
                RIGHT * max(top.width, bottom.width) / 2, color=color)
    return VGroup(top, line, bottom).arrange(DOWN, buff=.14)


def panel(width=5.7, height=3.8, center=ORIGIN):
    return RoundedRectangle(width=width, height=height, corner_radius=.18,
                            stroke_color=EDGE, stroke_width=1.5,
                            fill_color=PANEL, fill_opacity=1).move_to(center)


def label_pair(arabic, latin, color=INK):
    return VGroup(ar(arabic, 25, width=4.8), eq(latin, 35, color, width=4.8)).arrange(DOWN, buff=.28)


def charge(sign='+', radius=.19):
    color = POSITIVE if sign == '+' else NEGATIVE
    return VGroup(Circle(radius=radius, color=color, fill_color=BG, fill_opacity=1,
                         stroke_width=2), eq(sign, 20 * radius / .19, color))


def path(points, color=MUTED, width=3):
    return VMobject(color=color, stroke_width=width).set_points_as_corners(points)


def wire(a, b, color=MUTED):
    return Line(a, b, color=color, stroke_width=3)


def resistor(center=ORIGIN, width=1.35, label='R'):
    box = Rectangle(width=width, height=.48, stroke_color=RESIST,
                    fill_color=PANEL, fill_opacity=1, stroke_width=2.5).move_to(center)
    return VGroup(box, eq(label, 23, RESIST, width=width-.16).move_to(box))


def battery(center=ORIGIN, label='6 V'):
    # Terminals are exactly center +/- 0.65 UP; long plate is positive.
    x, y, _ = center
    return VGroup(wire([x,y+.65,0],[x,y+.18,0]),
                  wire([x,y-.18,0],[x,y-.65,0]),
                  Line([x-.42,y+.18,0],[x+.42,y+.18,0],color=VOLT,stroke_width=5),
                  Line([x-.23,y-.18,0],[x+.23,y-.18,0],color=VOLT,stroke_width=5),
                  eq('+',20,POSITIVE).move_to([x-.7,y+.23,0]),
                  eq('−',20,NEGATIVE).move_to([x-.7,y-.23,0]),
                  eq(label,25,VOLT).move_to([x-1,y-.9,0]))


def bulb(center=ORIGIN):
    c = Circle(.4, color=ENERGY, stroke_width=2.5).move_to(center)
    return VGroup(c, Line(center+[-.24,.24,0],center+[.24,-.24,0],color=ENERGY),
                  Line(center+[-.24,-.24,0],center+[.24,.24,0],color=ENERGY))


def capacitor(center=ORIGIN, height=2.4, gap=1.5, n=6):
    """Equal/opposite charges, no moving dots across the dielectric."""
    x,y,_ = center
    dielectric = Rectangle(width=gap,height=height,stroke_width=0,fill_color=VOLT,fill_opacity=.08).move_to(center)
    plates = VGroup(*[Line([x+s*gap/2,y-height/2,0],[x+s*gap/2,y+height/2,0],
                          color=POSITIVE if s<0 else NEGATIVE,stroke_width=6) for s in [-1,1]])
    charges = VGroup(*[charge('+' if s<0 else '−',.12).move_to([x+s*(gap/2+.22),yy,0])
                       for s in [-1,1] for yy in np.linspace(y-height*.4,y+height*.4,n)])
    fields = VGroup(*[Arrow([x-gap/2+.15,yy,0],[x+gap/2-.15,yy,0],buff=0,color=VOLT,
                            stroke_width=2,max_tip_length_to_length_ratio=.14)
                      for yy in np.linspace(y-height*.33,y+height*.33,4)])
    return VGroup(dielectric,plates,charges,fields)


class Lesson(Scene):
    """Persistent chapter header; stable diagram, equation and caption zones."""
    def setup(self):
        self.camera.background_color = BG
        self.pace = float(os.environ.get('ELECTRICITY_PACE', '1'))
        if self.pace <= 0:
            raise ValueError('ELECTRICITY_PACE must be positive')
        self.header = VGroup()
        self.caption = None
        self.beat_index = 0

    def play(self, *animations, **kwargs):
        # Scene.wait calls self.play(Wait(run_time=...)); preserve that duration.
        # Otherwise a default of one second silently destroys reading pauses.
        duration=kwargs.get('run_time',max(
            [a.run_time for a in animations if isinstance(a,Animation)] or [1]))
        kwargs['run_time'] = max(1/config.frame_rate, duration*self.pace)
        return super().play(*animations, **kwargs)

    def wait(self, duration=1, **kwargs):
        # Scaling happens once, in play(), including internally created Waits.
        return super().wait(duration, **kwargs)

    def begin(self, number, title, question):
        title_mob = ar(title, 35, bold=True, width=10.8).move_to([0, 3.32, 0])

        self.header = VGroup(title_mob)
        self.add(self.header)

        q = ar(question, 36, bold=True).move_to([0, .35, 0])
        self.play(FadeIn(q, shift=UP * .12), run_time=.8)
        self.wait(3)
        self.play(FadeOut(q), run_time=.5)

    def say(self, text, hold=3, color=INK):
        new = VGroup(panel(12.7,.72,[0,-3.22,0]),ar(text,27,color,width=12.05).move_to([0,-3.22,0]))
        if self.caption is None:
            self.play(FadeIn(new),run_time=.45)
        else:
            self.play(ReplacementTransform(self.caption,new),run_time=.45)
        self.caption = new
        self.wait(hold)
        self.snapshot()

    def snapshot(self):
        """Optional contact-sheet source frames for visual regression review."""
        dest = os.environ.get('ELECTRICITY_QA_DIR')
        if dest:
            self.beat_index += 1
            folder=Path(dest); folder.mkdir(parents=True,exist_ok=True)
            self.renderer.update_frame(self)
            self.renderer.camera.get_image().save(folder/f'{type(self).__name__}_{self.beat_index:02d}.png')

    def show(self, *mobs):
        self.play(LaggedStart(*[FadeIn(m,shift=UP*.1) for m in mobs],lag_ratio=.12),run_time=1)

    def clear_stage(self):
        keep = [self.header,self.caption]
        items = [m for m in self.mobjects if all(m is not k for k in keep)]
        if items:
            self.play(*[FadeOut(m) for m in items],run_time=.6)

    def formula(self, text, color=INK, y=-2.15):
        obj=eq(text,36,color).move_to([0,y,0]); self.show(obj); return obj

    def finish(self, takeaway, formula=None, color=CURRENT):
        self.clear_stage()
        if self.caption is not None:
            self.play(FadeOut(self.caption),run_time=.4)
            self.caption=None
        card=panel(11.7,3.35,[0,.15,0])
        tag = Text("⭐", font_size=24).move_to([0, 1.3, 0])
        #tag = Star(n=5, outer_radius=0.2, color=ENERGY, fill_color=ENERGY, fill_opacity=1, stroke_width=0).move_to(
            #[0, 1.3, 0])
        message=ar(takeaway,35,width=10.7,bold=True).move_to([0,.35,0])
        self.show(card,tag,message)
        if formula:
            self.show(eq(formula,37,color).move_to([0,-.75,0]))
        self.wait(5)
        self.snapshot()

    def flow(self, points, seconds=4, count=12, color=CURRENT, cycles=1, reverse=False):
        """Constant arc-length speed; schematic conventional-current markers.

        Only use on a closed loop; this avoids teleporting over a circuit gap.
        """
        pts=np.array(points,dtype=float)
        lengths=np.linalg.norm(np.diff(pts,axis=0),axis=1)
        cumulative=np.r_[0,np.cumsum(lengths)]
        def point(u):
            distance=(u%1)*cumulative[-1]
            i=min(np.searchsorted(cumulative,distance,side='right')-1,len(lengths)-1)
            return pts[i]+(pts[i+1]-pts[i])*(distance-cumulative[i])/lengths[i]
        dots=VGroup(*[Dot(point(i/count),radius=.055,color=color) for i in range(count)])
        self.add(dots)
        def update(m,alpha):
            for i,dot in enumerate(m):
                dot.move_to(point(i/count+(-1 if reverse else 1)*alpha*cycles))
        self.play(UpdateFromAlphaFunc(dots,update),run_time=seconds,rate_func=linear)
        self.remove(dots)


def render_scene(scene):
    """Run a scene directly in PyCharm; CLI quality flags remain independent."""
    quality=os.environ.get('ELECTRICITY_QUALITY','high_quality')
    with tempconfig({'quality':quality,'frame_width':128/9,'frame_height':8,
                     'media_dir':str(ROOT/'media'),'preview':False}):
        scene().render()
