"""Linked numerical displays. Scientific state drives every graph and value."""
from visual_helpers import *
from science_anim.visuals import SampledCurve
from science_anim.fields import ScalarHeatmap
from science_anim.maths.calculus_visuals import TangentLine
from science_anim.presentation.choreography import emphasize
from plot_data import evaluate

def graph(xr,yr,width=5,height=3,center=(0,0,0),xlabel='x',ylabel='V',xticks=None,yticks=None):
    a=Axes(x_range=xr,y_range=yr,x_length=width,y_length=height,
        axis_config={'include_tip':False,'stroke_color':MUTED,'stroke_width':1.4}).move_to(center)
    labels=VGroup(formula(xlabel,24).next_to(a,DOWN,buff=.38),formula(ylabel,24).next_to(a,UP,buff=.18))
    for v,t in (xticks or []):labels.add(formula(t,18,WHITE).next_to(a.c2p(v,yr[0]),DOWN,buff=.1))
    for v,t in (yticks or []):labels.add(formula(t,18,WHITE).next_to(a.c2p(xr[0],v),LEFT,buff=.1))
    return a,labels

def number(value,size=26,color=WHITE,places=2):
    return DecimalNumber(value,num_decimal_places=places,mob_class=Text,font_size=size,color=color,group_with_commas=False)

def meter(symbol,tracker,position,color=AMBER,places=2):
    prefix=formula(symbol+'=',26,color)
    value=number(tracker.get_value(),26,color,places)
    row=VGroup(prefix,value).arrange(RIGHT,buff=.15).move_to(position)
    value.add_updater(lambda m:m.set_value(tracker.get_value()))
    return row

def scientific(value):
    mantissa,power=f'{value:.2e}'.split('e')
    return mantissa+r'\times10^{'+str(int(power))+'}'

def sampled(a,x,y,color=CYAN):return SampledCurve(a,np.asarray(x),np.asarray(y),color=color)

def cell_map(a,function,n=15,lo=0,hi=1):
    t=(np.arange(n)+.5)*PI/n;X,Y=np.meshgrid(t,t,indexing='xy')
    return ScalarHeatmap(a,function(X,Y),(0,PI),(0,PI),vmin=lo,vmax=hi).set_z_index(-1)

def colour_key(lo=0,hi=1,center=(-3.5,-2.75,0),width=3.5):
    tiles=VGroup(*[Rectangle(width=width/24,height=.14,stroke_width=0,fill_opacity=.85,
        fill_color=interpolate_color(BLUE,RED,k/23)).move_to([center[0]-width/2+(k+.5)*width/24,center[1],0]) for k in range(24)])
    labels=VGroup(formula(f'{lo:g}',18,WHITE).next_to(tiles,LEFT),formula(f'{hi:g}',18,WHITE).next_to(tiles,RIGHT))
    return VGroup(tiles,labels)

def domain(center=(-3.7,0,0),size=3.8):
    return graph([0,PI,PI/2],[0,PI,PI/2],size,size,center,'x','y',[(0,'0'),(PI,r'\pi')],[(PI,r'\pi')])

def trial(x,y):return np.sin(x)*(1-y/PI)
def exact(x,y):return np.sin(x)*np.sinh(PI-y)/np.sinh(PI)

def derivatives(p,x,y):
    n=(len(p)-1)//4;wx,b,wy,u=p[:n],p[n:2*n],p[2*n:3*n],p[3*n:4*n]
    h=np.tanh(np.asarray(x)[...,None]*wx+np.asarray(y)[...,None]*wy+b)
    common=-2*h*(1-h*h)*u
    return np.sum(common*wx**2,axis=-1),np.sum(common*wy**2,axis=-1)

class Explainer(Lesson):
    """Definitions belong beside the changing quantity, never on a separate slide."""
    def heading(self,text):
        old=getattr(self,'current_heading',None)
        if old is not None:self.remove_fixed_in_frame_mobjects(old);self.remove(old)
        self.current_heading=ar(text,31,width=12.4).move_to([0,3.45,0])
        self.add_fixed_in_frame_mobjects(self.current_heading)
    def change(self,old,new,seconds=.6):
        new.move_to(old)
        self.play(FadeOut(old),run_time=seconds/3)
        self.play(FadeIn(new),run_time=2*seconds/3)
        return new
    def cue(self,text):self.caption(text)
    def code_flash(self,name,seconds=3):
        self.reset();code=code_panel(name,11.5)
        self.reveal(code);self.highlight(code,min(2,len(code.code_lines)-1));self.wait(seconds)
    @contextmanager
    def beat(self,index):
        entry=SCRIPT[self.chapter-1]['blocks'][index]
        start=float(self.time);duration=entry['seconds']
        audio=ROOT/'audio'/f'scene_{self.chapter:02d}_{index+1:02d}.wav'
        if settings.USE_AUDIO and audio.exists():
            with av.open(str(audio)) as c:duration=float(c.duration)/1e6
            self.add_sound(str(audio))
        yield duration
        animation_end=float(self.time)
        # Never disguise a long missing visual sequence with a 20-second wait.
        remainder=max(0,start+duration-animation_end)
        if remainder>4.1:raise RuntimeError(f'Scene {self.chapter}, beat {index}: {remainder:.1f}s has no visual explanation')
        if remainder>1/config.frame_rate:self.wait(remainder)
        self.timeline.append({'start':start,'duration':float(self.time)-start,'text':entry['text'],'static_tail':remainder})
        dest=ROOT/'review'/f'scene_{self.chapter:02d}';dest.mkdir(parents=True,exist_ok=True)
        self.renderer.static_image=None;self.renderer.update_frame(self)
        self.camera.get_image().save(dest/f'block_{index+1}.png')
        (dest/'timing.json').write_text(json.dumps(self.timeline,ensure_ascii=False,indent=2),encoding='utf-8')

class NumericNeuron(VGroup):
    def __init__(self):
        self.inputs=VGroup(*[Circle(.4,color=CYAN,fill_opacity=.15).move_to([-5,y,0]) for y in [1.2,-1.2]])
        self.sum=Circle(.48,color=AMBER).move_to([-1.5,0,0])
        self.activation=RoundedRectangle(width=1.4,height=1,corner_radius=.12,color=PURPLE).move_to([1.3,0,0])
        self.output=Circle(.5,color=GREEN).move_to([4.7,0,0])
        self.links=VGroup(*[Arrow(c.get_right(),self.sum.get_left(),buff=.08,color=CYAN if i==0 else PURPLE,stroke_width=3) for i,c in enumerate(self.inputs)],
            Arrow(self.sum.get_right(),self.activation.get_left(),buff=.08),Arrow(self.activation.get_right(),self.output.get_left(),buff=.08,color=GREEN))
        super().__init__(self.links,self.inputs,self.sum,self.activation,self.output)

