from explainer_tools import *

class InitializeNetwork(Explainer):
    chapter=3
    def construct(self):
        p=self.data['weights'][0];n=(len(p)-1)//4
        with self.beat(0):
            self.heading('من إحداثيين إلى قيمة للجهد')
            net=network().scale(1.65).move_to([-2.4,0,0]);self.play(Create(net),run_time=2)
            self.reveal(ar('خمس خلايا معروضة من أصل مئة',23,width=6).move_to([-2.5,-2.6,0]))
            self.cue('إكس وواي يحددان النقطة التي نحسب الجهد عندها')
            read=None
            for x,y in [(.3,.4),(1.2,.4),(1.2,2),(2.7,2.5)]:
                h=np.tanh(x*p[:n]+y*p[2*n:3*n]+p[n:2*n]);value=float(evaluate(p,np.array(x),np.array(y)))
                new=VGroup(formula(fr'x={x:.1f},\ y={y:.1f}',27),formula(fr'V_\theta={value:.3f}',32,GREEN)).arrange(DOWN,buff=.7).move_to([3.8,.3,0])
                if read is None:self.reveal(new)
                else:self.play(ReplacementTransform(read,new),run_time=.5)
                read=new
                self.play(*[ShowPassingFlash(e.copy().set_color(AMBER),time_width=.4) for e in net[0][:10]],run_time=.9)
                self.play(*[c.animate.set_fill(CYAN if val>=0 else PURPLE,opacity=abs(float(val))) for c,val in zip(net[2],h[:5])],run_time=.8)
                self.play(*[ShowPassingFlash(e.copy().set_color(GREEN),time_width=.4) for e in net[0][10:]],run_time=.8)
            self.cue('اللون يميز إشارة خرج الخلية، وشدته تمثل مقدار هذا الخرج')
            self.wait(2)
        self.reset()
        with self.beat(1):
            self.heading('هذه الأعداد هي معاملات الشبكة')
            colors=[CYAN,AMBER,PURPLE,GREEN];names=['w_x','b','w_y','u'];cells=VGroup()
            for j,(name,color) in enumerate(zip(names,colors)):
                xx=-4.8+j*3.15
                group=VGroup(*[RoundedRectangle(width=1.8,height=.48,corner_radius=.05,color=color,fill_color=color,fill_opacity=.12).move_to([xx,1.2-i*.65,0]) for i in range(4)])
                texts=VGroup(*[formula(f'{p[j*n+i]:.3f}',23,color).move_to(c) for i,c in enumerate(group)])
                self.reveal(group,texts,formula(name,28,color).move_to([xx,2.25,0]));cells.add(group,texts)
                self.wait(1)
            self.reveal(ar('أول أربعة أعداد من كل مجموعة',22,width=9).move_to([0,-1.6,0]))
            eq=formula('100+100+100+100+1=401',33).move_to([0,-2.5,0]);self.reveal(eq)
            self.cue('لكل خلية وزنان وانحياز ووزن للخرج، ثم انحياز أخير للجهد')
            emphasize(self,eq,run_time=1.2);self.wait(2)
            self.code_flash('initialize',2)
        self.reset()
        with self.beat(2):
            self.heading('الكود ينفّذ الحساب نفسه')
            code=code_panel('model',8).move_to([-2.3,.7,0]);self.reveal(code)
            point=formula(r'x=1,\quad y=1',26).move_to([4,2,0]);self.reveal(point)
            z=float(p[0]+p[2*n]+p[n]);h=float(np.tanh(z));contrib=float(h*p[3*n])
            equations=[(2,fr'z_1={z:.3f}'),(3,fr'h_1=\tanh(z_1)={h:.3f}'),(4,fr'u_1h_1={contrib:.3f}')]
            for j,(line,source) in enumerate(equations):
                self.highlight(code,line)
                self.reveal(formula(source,26,width=4.5).move_to([3.9,.9-j*1,0]));self.wait(1.5)
            self.reveal(formula(fr'V_\theta(1,1)=\sum_{{i=1}}^{{100}}u_ih_i+b_{{out}}={float(evaluate(p,np.array(1.),np.array(1.))):.3f}',28,width=12).move_to([0,-2.3,0]))
            self.cue('هذه قيم الشبكة قبل التدريب؛ لا نتوقع منها حلاً صحيحاً بعد')
            self.wait(2)

if __name__=='__main__':run_independent(InitializeNetwork)
