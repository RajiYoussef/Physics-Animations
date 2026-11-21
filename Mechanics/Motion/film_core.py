"""Shared film design and narration-aware rendering; no LaTeX or optional plugin required."""
from pathlib import Path
from contextlib import contextmanager
import json
import os
import sys
import math
import numpy as np
import av
from manim import *
import settings
from science_anim.style import label,TeachingScene
from science_anim.presentation.layout import fit_inside,frame_violations
from science_anim.presentation.choreography import NarrationTimeline
from motion_models import radial,tangent
from math_type import tex, math_label

ROOT=Path(__file__).resolve().parent
SCRIPT=json.loads((ROOT/"script.json").read_text(encoding="utf-8"))
VELOCITY="#57D5E8"
ACCELERATION="#FFB65C"
DISPLACEMENT="#69D6A5"
INK="#EDF2FA"
MUTED="#91A4BA"
GHOST="#52718B"
PAPER="#172333"
PURPLE="#BF9CF5"


def ar(text,size=30,width=12,color=INK):
    return label(text,size,color=color,font="Arial",max_width=width)


def en(text,size=30,color=INK,width=None):
    return label(text,size,color=color,max_width=width)


def vector(start,direction,length=1,color=VELOCITY,width=4):
    d=np.asarray(direction,float); start=np.asarray(start,float)
    if np.linalg.norm(d)<1e-9 or length<1e-9:
        return Dot(start,radius=.015,color=color).set_opacity(0)
    return Arrow(start,start+d/np.linalg.norm(d)*length,buff=0,color=color,
                 stroke_width=width,max_tip_length_to_length_ratio=.18)


def vector_symbol(text="v",size=38,color=VELOCITY):
    return tex(r"\vec " + text,size,color)


def fraction(numerator,denominator,size=34,color=INK):
    a=math_label(numerator,size,color) if isinstance(numerator,str) else numerator
    b=math_label(denominator,size,color) if isinstance(denominator,str) else denominator
    bar=Line(LEFT*max(a.width,b.width)*.55,RIGHT*max(a.width,b.width)*.55,color=color,stroke_width=2)
    a.next_to(bar,UP,buff=.12);b.next_to(bar,DOWN,buff=.12)
    return VGroup(a,bar,b)


def equation(*parts,buff=.2):
    objects=[math_label(p,34) if isinstance(p,str) else p for p in parts]
    return VGroup(*objects).arrange(RIGHT,buff=buff)


def card(content,width=3.2,height=1.3,color=GHOST):
    border=RoundedRectangle(width=width,height=height,corner_radius=.12,
                            fill_color=PAPER,fill_opacity=.8,stroke_color=color,stroke_width=1)
    fit_inside(content,width-.2,height-.18,padding=.05)
    content.move_to(border)
    return VGroup(border,content)


class Car(VGroup):
    """Original vector top-view car, pointing +x; pose updates keep one object alive."""
    def __init__(self,color=VELOCITY,length=.8):
        body=RoundedRectangle(width=.95,height=.47,corner_radius=.12,
                              fill_color=color,fill_opacity=1,stroke_color=INK,stroke_width=1.2)
        windows=VGroup(
            Polygon([.12,.17,0],[.30,.13,0],[.30,-.13,0],[.12,-.17,0],
                    fill_color="#183C51",fill_opacity=1,stroke_width=0),
            RoundedRectangle(width=.23,height=.32,corner_radius=.04,
                             fill_color="#183C51",fill_opacity=1,stroke_width=0).shift(LEFT*.2))
        wheels=VGroup(*[RoundedRectangle(width=.18,height=.08,corner_radius=.02,
                                        fill_color="#02070D",fill_opacity=1,stroke_color=MUTED,stroke_width=.7)
                        .move_to([x,y,0]) for x in [-.3,.3] for y in [-.25,.25]])
        lights=VGroup(*[Line([.43,y-.04,0],[.43,y+.04,0],color="#FFF0BC",stroke_width=3)
                       for y in [-.14,.14]])
        super().__init__(wheels,body,windows,lights)
        self.scale_to_fit_width(length)
        self._heading=0.
        self.set_z_index(5)

    def pose(self,position,heading):
        self.rotate(heading-self._heading,about_point=self.get_center())
        self._heading=heading
        return self.move_to(position)


class SpeedGauge(VGroup):
    """Opaque, fixed-position numerals; no Tex and no opacity animation on an updater."""
    def __init__(self,get_value,unit="km/h",maximum=80,width=2.5):
        self.get_value=get_value;self.maximum=maximum
        self.frame=RoundedRectangle(width=width,height=1.65,corner_radius=.12,
                                    fill_color=PAPER,fill_opacity=1,stroke_color=GHOST,stroke_width=1)
        self.heading=ar("مقدار السرعة",22,width=width-.25).move_to([0,.54,0])
        self.digits=DecimalNumber(get_value(),num_decimal_places=0,mob_class=Text,
                                   font_size=40,color=INK).move_to([-.24,0,0])
        self.unit=math_label(unit,20,MUTED).move_to([.64,-.04,0])
        self.rail=Line([-.92,-.52,0],[.92,-.52,0],color=GHOST,stroke_width=4)
        self.fill=Line([-.92,-.52,0],[.92,-.52,0],color=VELOCITY,stroke_width=4)
        super().__init__(self.frame,self.heading,self.digits,self.unit,self.rail,self.fill)
        self.add_updater(lambda m:m.refresh())
        self.refresh()

    def refresh(self):
        center=self.frame.get_center()
        value=round(float(self.get_value()))
        if getattr(self,"_last_value",None)!=value:
            self.digits.set_value(value).set_opacity(1)
            self._last_value=value
        self.digits.move_to(center+[-.24,0,0])
        start,end=self.rail.get_start(),self.rail.get_end()
        f=np.clip(self.get_value()/self.maximum,1e-5,1)
        self.fill.put_start_and_end_on(start,start+f*(end-start))
        return self


class Earth(VGroup):
    """Quiet vector illustration; latitude lines explain the globe, not decoration."""
    def __init__(self,radius=.75):
        globe=Circle(radius=radius,fill_color="#153C54",fill_opacity=1,
                     stroke_color="#458AA6",stroke_width=1.5)
        super().__init__(globe)
        for w in [.55,1.3]:
            self.add(Ellipse(width=radius*w,height=2*radius,color="#448A9B",stroke_width=.8,stroke_opacity=.45))
        for y in [-.45,0,.45]:
            self.add(Ellipse(width=radius*2*np.sqrt(1-y*y),height=radius*.26,color="#448A9B",
                             stroke_width=.8,stroke_opacity=.4).shift(UP*y*radius))
        self.add(Arc(radius=radius*.96,start_angle=.1,angle=1.3,color="#6BC2C4",stroke_width=2))


class Satellite(VGroup):
    def __init__(self):
        super().__init__(
            Rectangle(width=.22,height=.25,fill_color=INK,fill_opacity=1,stroke_width=0),
            Rectangle(width=.29,height=.19,fill_color="#237EAB",fill_opacity=1,stroke_color=VELOCITY,stroke_width=1).shift(LEFT*.29),
            Rectangle(width=.29,height=.19,fill_color="#237EAB",fill_opacity=1,stroke_color=VELOCITY,stroke_width=1).shift(RIGHT*.29))
        self.set_z_index(6)


def arc_road(center,radius,start,angle):
    outer=Arc(radius=radius,arc_center=center,start_angle=start,angle=angle,
              stroke_color="#23394A",stroke_width=30)
    dashes=DashedVMobject(Arc(radius=radius,arc_center=center,start_angle=start,angle=angle,
                             stroke_color="#6B8296",stroke_width=1.3),num_dashes=22)
    return VGroup(outer,dashes).set_z_index(-3)


def orbit_arrows(position,theta,vlength=1,alength=.8):
    return VGroup(vector(position,tangent(theta),vlength,VELOCITY),
                  vector(position,-radial(theta),alength,ACCELERATION))


def right_angle_at(position,theta,size=.28):
    p=np.asarray(position);t=tangent(theta);n=-radial(theta)
    return VMobject(color=INK,stroke_width=1.7).set_points_as_corners(
        [p+size*t,p+size*(t+n),p+size*n]).set_z_index(8)


class FilmScene(TeachingScene):
    chapter_id=0

    def setup(self):
        super().setup()
        self.camera.background_color=settings.BACKGROUND
        self.scale_time=float(os.environ.get("PHYSICS_TIME_SCALE",settings.TIME_SCALE))
        if self.scale_time<=0:raise ValueError("TIME_SCALE must be positive")
        self.chapter=SCRIPT[self.chapter_id-1]
        self.timeline=[]
        self.recording=None
        self.hud=VGroup()
        self.stage=VGroup()
        self.note=None
        self.qa=[]

    def opening(self,title,kicker):
        title=ar(title,32,width=12).move_to([0,3.48,0])
        line=Line([-6.5,3.12,0],[6.5,3.12,0],stroke_width=1,color="#304052")
        self.hud.add(title,line)
        self.add(self.hud)

    def caption_ar(self,text,color=INK):
        new=ar(text,27,width=12.3,color=color).move_to([0,-3.35,0])
        if self.note is not None:
            self.remove(self.note)
        self.note=new
        self.add(new)
        self.check_layout(new)
        return new

    def check_layout(self,*objects):
        invalid=frame_violations(objects,margin=.12)
        if invalid:raise ValueError(f"Clipped label in chapter {self.chapter_id}: {invalid}")

    def clear_stage(self,*keep):
        """Remove active content cleanly, including updater ownership."""
        preserved=[self.hud,self.note,*keep]
        old=[m for m in self.mobjects if all(m is not x for x in preserved)]
        for obj in old:obj.clear_updaters(recursive=True)
        self.remove(*old)

    def checkpoint(self,name):
        """Saved inspection frame without affecting narration time."""
        if not hasattr(self.renderer,"update_frame"):return
        dest=ROOT/"review"/f"scene_{self.chapter_id:02d}"
        dest.mkdir(parents=True,exist_ok=True)
        self.renderer.static_image=None
        self.renderer.update_frame(self)
        self.camera.get_image().save(dest/f"{name}.png")
        self.qa.append({"name":name,"time":round(float(self.time),3)})

    @contextmanager
    def shot(self,index):
        text=self.chapter["narration"][index]
        start=float(self.time)
        duration,recording=self.shot_info(index)
        if recording:
            self.add_sound(str(recording))
        self.timeline.append({"start":start,"duration":duration,"text":text,
                              "audio":str(recording) if recording else None})
        yield duration
        remaining=start+duration-float(self.time)
        # Manim rounds each animation to frame boundaries. Permit accumulated frame error.
        if remaining<-.35:
            raise RuntimeError(f"Shot {index+1} overrun by {-remaining:.2f}s")
        if remaining>=1/config.frame_rate:self.wait(remaining)
        self.checkpoint(f"shot_{index+1:02d}")

    def shot_info(self,index):
        """Inspect duration without scheduling audio; also keeps playback rates consistent."""
        planned=self.chapter["seconds"][index]
        recording=next((ROOT/"audio"/f"scene_{self.chapter_id:02d}_{index+1:02d}.{extension}"
                        for extension in ("wav","mp3","m4a")
                        if (ROOT/"audio"/f"scene_{self.chapter_id:02d}_{index+1:02d}.{extension}").exists()),None)
        if recording and settings.USE_AUDIO and self.scale_time==1:
            with av.open(str(recording)) as container:
                planned=float(container.duration)/1e6
        else:
            recording=None
        return planned*self.scale_time,recording

    def finish(self):
        dest=ROOT/"review"/f"scene_{self.chapter_id:02d}"
        dest.mkdir(parents=True,exist_ok=True)
        (dest/"timing.json").write_text(json.dumps(self.timeline,ensure_ascii=False,indent=2),encoding="utf-8")
        (dest/"checkpoints.json").write_text(json.dumps(self.qa,indent=2))
        # Split captions at punctuation/short word groups rather than one long paragraph.
        cues=[]
        for block in self.timeline:
            words=block["text"].split()
            chunks=[" ".join(words[i:i+10]) for i in range(0,len(words),10)]
            for i,chunk in enumerate(chunks):
                cues.append((block["start"]+block["duration"]*i/len(chunks),chunk))
        NarrationTimeline(cues).write_srt(dest/"captions.srt",max(float(self.time),cues[-1][0]+.1))


def render_chapter(cls):
    quality=os.environ.get("PHYSICS_QUALITY",settings.QUALITY)
    w,h,fps={"preview":(854,480,15),"draft":(1280,720,30),"final":(1920,1080,60)}[quality]
    time_scale=float(os.environ.get("PHYSICS_TIME_SCALE",settings.TIME_SCALE))
    suffix="_quick" if time_scale!=1 else ""
    folder=ROOT/"videos";folder.mkdir(exist_ok=True)
    name=f"scene_{cls.chapter_id:02d}{suffix}"
    with tempconfig({"pixel_width":w,"pixel_height":h,"frame_rate":fps,
                     "frame_width":128/9,"frame_height":8,"background_color":settings.BACKGROUND,
                     "media_dir":str(ROOT/"_render_cache"),"video_dir":str(folder),
                     "output_file":name,"preview":False,"disable_caching":True}):
        scene=cls();scene.render()
        path=Path(scene.renderer.file_writer.movie_file_path)
    print(f"Rendered: {path}")
    if settings.OPEN_AFTER_RENDER and os.environ.get("PHYSICS_BATCH")!="1" and os.name=="nt":
        os.startfile(str(path))
    return path
