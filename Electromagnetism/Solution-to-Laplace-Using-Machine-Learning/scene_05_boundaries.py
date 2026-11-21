from explainer_tools import *

class BoundaryConditions(Explainer):
    chapter=5
    def construct(self):
        with self.beat(0):
            self.heading('نحدد الجهد على حواف المنطقة')
            a,l=domain();tiles=cell_map(a,trial);self.add(tiles,a,l,colour_key())
            self.reveal(ar('تخمين يطابق قيم الحدود',23,width=5).move_to([-3.7,2.7,0]))
            b,bl=graph([0,PI,PI/2],[0,1.15,.5],5,3,[3.3,0,0],'x','V',[(0,'0'),(PI/2,r'\pi/2'),(PI,r'\pi')],[(0,'0'),(1,'1')]);self.add(b,bl)
            xs=np.linspace(0,PI,121);curve=sampled(b,xs,np.sin(xs),GREEN);self.play(Create(curve),run_time=1.5)
            edge=Line(a.c2p(0,0),a.c2p(PI,0),color=GREEN,stroke_width=5);self.play(Create(edge),run_time=1)
            eq=formula(r'V(x,0)=\sin x',30,GREEN).move_to([3.3,2.45,0]);self.reveal(eq)
            x=ValueTracker(0)
            probes=always_redraw(lambda:VGroup(Dot(a.c2p(x.get_value(),0),color=AMBER,radius=.08),Dot(b.c2p(x.get_value(),np.sin(x.get_value())),color=AMBER,radius=.08)))
            self.add(probes);self.cue('نقرأ الإحداثيات من المحور ونحدد قيمة الجهد على الرسم البياني.')
            self.play(x.animate.set_value(PI),run_time=5,rate_func=linear)
            self.remove(probes)
            edges=[((0,0),(0,PI),r'V(0,y)=0','y'),((PI,0),(PI,PI),r'V(\pi,y)=0','y'),((0,PI),(PI,PI),r'V(x,\pi)=0','x')]
            for start,end,source,symbol in edges:
                self.play(Transform(edge,Line(a.c2p(*start),a.c2p(*end),color=PURPLE,stroke_width=5)),Transform(curve,sampled(b,xs,np.zeros_like(xs),PURPLE)),run_time=1.2)
                eq=self.change(eq,formula(source,30,PURPLE))
                next_label=formula(symbol,24).move_to(bl[0])
                self.play(ReplacementTransform(bl[0],next_label),run_time=.3)
                bl.submobjects[0]=next_label
                # Replace the stored label reference as well as its display.
                self.cue('على هذه الحافة، الجهد المطلوب يساوي صفر');self.wait(.8)
            self.wait(1)
        self.reset()
        with self.beat(1):
            self.heading('من شرط مكتوب إلى قيم نحسبها')
            a,l=graph([0,PI,PI/2],[0,1.15,.5],7,3.4,[-2,0,0],'x','V(x,0)',[(0,'0'),(PI/2,r'\pi/2'),(PI,r'\pi')],[(0,'0'),(1,'1')]);self.add(a,l)
            xs=np.linspace(0,PI,121);self.play(Create(sampled(a,xs,np.sin(xs),GREEN)),run_time=1.5)
            nodes=VGroup(*[Dot(a.c2p(x,np.sin(x)),radius=.04,color=GREEN) for x in np.linspace(0,PI,31)])
            self.play(LaggedStart(*[FadeIn(p) for p in nodes],lag_ratio=.08),run_time=2.5)
            info=None
            for i,(x,name) in enumerate([(0,'0'),(PI/6,r'\pi/6'),(PI/2,r'\pi/2'),(PI,r'\pi')]):
                new=VGroup(formula('x='+name,27),formula(fr'\sin({name})={np.sin(x):.2f}',29,GREEN)).arrange(DOWN,buff=.5).move_to([4.1,.6,0])
                if info is None:self.reveal(new)
                else:
                    self.play(FadeOut(info),run_time=.2)
                    self.play(FadeIn(new),run_time=.4)
                info=new
                self.play(Indicate(nodes[int(round(x/PI*30))],scale_factor=2,color=AMBER),run_time=1);self.wait(.7)
            self.cue('القيم المطلوبة هي 31 نقطة على كل حافة.')
            self.wait(2)
            self.code_flash('boundary', 2)

if __name__=='__main__':run_independent(BoundaryConditions)
