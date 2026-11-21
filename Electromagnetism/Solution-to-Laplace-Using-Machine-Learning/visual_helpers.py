from pathlib import Path
from contextlib import contextmanager
import json, os, re
import numpy as np
import av
from manim import *
from science_anim.style import label
from math_type import tex
import settings

ROOT=Path(__file__).resolve().parent
CYAN='#58D5E8'; AMBER='#FFB65C'; GREEN='#79DCA5'; PURPLE='#BA9AF2'; MUTED='#7C8DA5'
SCRIPT=json.loads((ROOT/'narration.json').read_text(encoding='utf-8'))

def ar(text,size=29,width=12,color=WHITE):
    return label(text,size,color=color,font=settings.ARABIC_FONT,max_width=width)

def formula(text,size=32,color=CYAN,width=12):
    return tex(text,size,color,width)

def code_panel(name,width=7.2):
    source=(ROOT/('plot_data.py' if name=='grid' else 'model.py')).read_text(encoding='utf-8')
    snippet=source.split('# snippet:'+name+'\n')[1].split('# end:'+name)[0].strip()
    panel=Code(code_string=snippet,language='python',add_line_numbers=False,
               background='rectangle',background_config={'fill_color':'#10141C','fill_opacity':1,'stroke_width':1,'stroke_color':MUTED},
               paragraph_config={'font':settings.CODE_FONT,'font_size':23,'line_spacing':.65})
    if panel.width>width:panel.scale_to_fit_width(width)
    if panel.height>4.6:panel.scale_to_fit_height(4.6)
    return panel

def plane(width=4.3):
    axes=Axes(x_range=[0,PI,PI/2],y_range=[0,PI,PI/2],x_length=width,y_length=width,
              axis_config={'include_tip':False,'stroke_color':MUTED,'stroke_width':1})
    box=Polygon(axes.c2p(0,0),axes.c2p(PI,0),axes.c2p(PI,PI),axes.c2p(0,PI),color=MUTED,stroke_width=1)
    grid=VGroup(*[Line(axes.c2p(t,0),axes.c2p(t,PI),stroke_width=.5,color=MUTED,stroke_opacity=.25) for t in np.linspace(0,PI,9)],*[Line(axes.c2p(0,t),axes.c2p(PI,t),stroke_width=.5,color=MUTED,stroke_opacity=.25) for t in np.linspace(0,PI,9)])
    labels=VGroup(formula('x',22).next_to(axes.c2p(PI,0),RIGHT,buff=.12),formula('y',22).next_to(axes.c2p(0,PI),UP,buff=.12),formula('0',18).next_to(axes.c2p(0,0),DL,buff=.1))
    return VGroup(axes,box,grid,labels)

def curve_axes(width=5,height=2.8):
    return Axes(x_range=[0,PI,PI/2],y_range=[-1.5,1.5,1],x_length=width,y_length=height,
                axis_config={'include_tip':False,'stroke_color':MUTED})

def heatmap(values,size=3.8,lo=0,hi=1):
    from matplotlib import colormaps
    rgba=colormaps['viridis'](np.clip((values-lo)/max(hi-lo,1e-12),0,1))
    image=ImageMobject((np.flipud(rgba)*255).astype(np.uint8)).set_height(size)
    image.set_resampling_algorithm(RESAMPLING_ALGORITHMS['nearest'])
    return image

def network():
    inputs=VGroup(*[Circle(.22,color=CYAN).move_to([-1.6,y,0]) for y in [.65,-.65]])
    hidden=VGroup(*[Circle(.16,color=PURPLE).move_to([0,y,0]) for y in np.linspace(-1.1,1.1,5)])
    output=Circle(.23,color=GREEN).move_to([1.5,0,0])
    edges=VGroup(*[Line(a.get_right(),b.get_left(),stroke_width=1,color=MUTED) for a in inputs for b in hidden],
                 *[Line(b.get_right(),output.get_left(),stroke_width=1,color=MUTED) for b in hidden])
    labels=VGroup(formula('x',23).move_to(inputs[0]),formula('y',23).move_to(inputs[1]),
                  formula('V',23,GREEN).move_to(output))
    return VGroup(edges,inputs,hidden,output,labels)

class Lesson(ThreeDScene):
    chapter=1
    def setup(self):
        self.camera.background_color=settings.BACKGROUND
        self.timeline=[]; self.scale_time=float(os.environ.get('ML_TIME_SCALE','1'))
        self.data=np.load(ROOT/'data/training.npz')
    def heading(self,text):
        obj=ar(text,33).move_to([0,3.45,0]);self.add_fixed_in_frame_mobjects(obj)
    def caption(self,text):
        if getattr(self,'current_caption',None) is not None:
            self.remove_fixed_in_frame_mobjects(self.current_caption)
            self.remove(self.current_caption)
        obj=ar(text,26,width=12.5).move_to([0,-3.45,0]);self.add_fixed_in_frame_mobjects(obj)
        self.current_caption=obj
    def reveal(self,*objects):
        self.play(*[FadeIn(o,shift=UP*.08) for o in objects],run_time=settings.CODE_REVEAL_SECONDS)
    def highlight(self,panel,line=0):
        target=panel.code_lines[line]
        self.play(Indicate(target,color=AMBER,scale_factor=1.03),run_time=.7)
    def reset(self):
        for m in list(self.mobjects):
            m.clear_updaters(recursive=True)
            self.remove_fixed_in_frame_mobjects(m)
        self.clear()
    @contextmanager
    def beat(self,index):
        entry=SCRIPT[self.chapter-1]['blocks'][index]
        start=float(self.time); duration=entry['seconds']*self.scale_time
        audio=ROOT/'audio'/f'scene_{self.chapter:02d}_{index+1:02d}.wav'
        if settings.USE_AUDIO and self.scale_time==1 and audio.exists():
            with av.open(str(audio)) as c:duration=float(c.duration)/1e6
            self.add_sound(str(audio))
        self.timeline.append({'start':start,'text':entry['text'],'duration':duration})
        yield duration
        remainder=start+duration-float(self.time)
        if remainder<-.3:raise RuntimeError(f'Chapter {self.chapter} block {index+1} overruns by {-remainder:.2f}s')
        if remainder>1/config.frame_rate:self.wait(remainder)
        dest=ROOT/'review'/f'scene_{self.chapter:02d}';dest.mkdir(parents=True,exist_ok=True)
        self.renderer.static_image=None;self.renderer.update_frame(self)
        self.camera.get_image().save(dest/f'block_{index+1}.png')
        (dest/'timing.json').write_text(json.dumps(self.timeline,ensure_ascii=False,indent=2),encoding='utf-8')

def render_scene(cls):
    quality=os.environ.get('ML_QUALITY',settings.QUALITY)
    w,h,fps={'preview':(854,480,15),'draft':(1280,720,30),'final':(1920,1080,60)}[quality]
    video=ROOT/'videos';video.mkdir(exist_ok=True)
    with tempconfig({'pixel_width':w,'pixel_height':h,'frame_rate':fps,
          'frame_width':128/9,'frame_height':8,'background_color':settings.BACKGROUND,
          'media_dir':str(ROOT/'_cache'),'partial_movie_dir':str(ROOT/'_cache'/'partial_movie_files'/'{scene_name}'),'video_dir':str(video),'output_file':f'scene_{cls.chapter:02d}',
          'disable_caching':True,'preview':False}):
        scene=cls();scene.render()
        return Path(scene.renderer.file_writer.movie_file_path)


def run_independent(cls):
    from prepare_data import prepare
    prepare()
    path=render_scene(cls)
    print('Saved video:',path)
    if settings.OPEN_AFTER_RENDER and os.environ.get('ML_BATCH')!='1':os.startfile(str(path))
