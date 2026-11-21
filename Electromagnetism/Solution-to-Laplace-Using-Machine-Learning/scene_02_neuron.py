from explainer_tools import *

class NeuronExplained(Explainer):
    chapter=2
    def construct(self):
        with self.beat(0):
            self.heading('لنحسب ناتج خلية عصبية واحدة')
            net=NumericNeuron();self.play(Create(net),run_time=2)
            labels=VGroup(formula('0.5',25).move_to(net.inputs[0]),formula('1',25).move_to(net.inputs[1]),
                formula(r'\Sigma',32,AMBER).move_to(net.sum),formula(r'\tanh',25,PURPLE).move_to(net.activation))
            self.reveal(labels)
            self.reveal(formula('x=0.5',25).next_to(net.inputs[0],UP),formula('y=1',25).next_to(net.inputs[1],DOWN))
            weights=VGroup(formula('w_x=2',25,CYAN).move_to([-3.5,1.2,0]),formula('w_y=-0.5',25,PURPLE).move_to([-3.5,-1.2,0]))
            self.reveal(weights)
            self.cue('نضرب كلاً من الإحداثيين في وزنيهما، ثم نجمع الناتجين معاً.')
            for i,text in enumerate(['2(0.5)=1','-0.5(1)=-0.5']):
                pulse=Dot(net.inputs[i].get_right(),color=AMBER);self.add(pulse)
                self.play(MoveAlongPath(pulse,net.links[i]),run_time=1.6);self.remove(pulse)
                self.reveal(formula(text,27,AMBER).move_to([-2+4*i,-2.2,0]))
            bias=formula('b=0.2',26,GREEN).move_to([-1.5,1.6,0]);self.reveal(bias)
            self.play(GrowArrow(Arrow(bias.get_bottom(),net.sum.get_top(),buff=.1,color=GREEN)),run_time=.8)
            z=formula('z=1-0.5+0.2=0.7',29).move_to([1,2.5,0]);self.reveal(z)
            pulse=Dot(net.sum.get_right(),color=AMBER);self.add(pulse);self.play(MoveAlongPath(pulse,net.links[2]),run_time=1.5);self.remove(pulse)
            self.reveal(formula('0.604',22,GREEN).move_to(net.output))
            self.reveal(formula(r'h=\tanh(0.7)\approx0.604',29,GREEN).move_to([1,-2.9,0]))
            self.cue('تأخذ دالة التنشيط المجموع وتحوله إلى مخرجات الخلية.')
            self.wait(2)
            self.change(z,formula(r'h_i=\tanh(w_{x,i}x+w_{y,i}y+b_i)',29,PURPLE))
            self.wait(1)
        self.reset()
        with self.beat(1):
            self.heading('لماذا نمرر المجموع في دالة تنشيط؟')
            a,l=graph([-3,3,1],[-1.2,1.2,1],7,3.5,[-2,0,0],'z','h=\\tanh z',[(-3,'-3'),(0,'0'),(3,'3')],[(-1,'-1'),(0,'0'),(1,'1')]);self.add(a,l)
            xs=np.linspace(-3,3,160);curve=sampled(a,xs,np.tanh(xs),PURPLE);self.play(Create(curve),run_time=2)
            z=ValueTracker(.7);h=ValueTracker(float(np.tanh(.7)))
            dot=always_redraw(lambda:Dot(a.c2p(z.get_value(),np.tanh(z.get_value())),color=AMBER))
            guides=always_redraw(lambda:VGroup(DashedLine(a.c2p(z.get_value(),0),dot.get_center(),color=MUTED),DashedLine(dot.get_center(),a.c2p(0,np.tanh(z.get_value())),color=MUTED)))
            self.add(dot,guides,meter('z',z,[4.3,1,0]),meter('h',h,[4.3,0,0],GREEN))
            h.add_updater(lambda m:m.set_value(float(np.tanh(z.get_value()))));self.add(h)
            self.cue('المحور الأفقي هو المجموع والمحور العمودي هو نتيجة الخلية')
            for value in [-2,0,2,.7]:self.play(z.animate.set_value(value),run_time=2.5)
            self.reveal(ar('المخرجات تقع بين "-1" و"1"',24,width=4).move_to([4,-1.4,0]))
            self.cue('من دون هذه الخطوة  تبقى الشبكة مجرد دالة خطية مع ثابت')
            self.play(z.animate.set_value(-.3),run_time=2);self.wait(2)
        self.reset()
        with self.beat(2):
            self.heading('نجمع مساهمات الخلايا للحصول على الجهد')
            a,l=graph([-3,3,1],[-2,2,1],5,3.4,[-3.7,0,0],'x','u_i h_i',[(-3,'-3'),(0,'0'),(3,'3')],[(-1,'-1'),(1,'1')]);b,bl=graph([-3,3,1],[-2,2,1],5,3.4,[3.3,0,0],'x',r'V_\theta(x)',[(-3,'-3'),(0,'0'),(3,'3')],[(-1,'-1'),(1,'1')]);self.add(a,l,b,bl)
            xs=np.linspace(-3,3,150);parts=[np.tanh(xs+1),-.8*np.tanh(2*xs),.5*np.tanh(xs-1)]
            self.cue('مثال مصغر يتكون من ثلاث خلايا حيث نقوم بجمع القيم الموجودة عند الإحداثيات ذاتها.')
            info=formula(r'u=(1,-0.8,0.5),\quad b_{out}=0',27).move_to([0,2.65,0]);self.reveal(info)
            total=np.zeros_like(xs);out=sampled(b,xs,total,GREEN);self.add(out)
            for i,values in enumerate(parts):
                c=sampled(a,xs,values,[CYAN,PURPLE,AMBER][i]);self.play(Create(c),run_time=1.5)
                self.play(Transform(out,sampled(b,xs,total+values,GREEN)),run_time=2);total+=values
            probe=ValueTracker(-2.5)
            dots=always_redraw(lambda:VGroup(*[Dot(a.c2p(probe.get_value(),v),radius=.06,color=col) for v,col in zip([np.tanh(probe.get_value()+1),-.8*np.tanh(2*probe.get_value()),.5*np.tanh(probe.get_value()-1)],[CYAN,PURPLE,AMBER])],Dot(b.c2p(probe.get_value(),np.tanh(probe.get_value()+1)-.8*np.tanh(2*probe.get_value())+.5*np.tanh(probe.get_value()-1)),color=GREEN)))
            self.add(dots);self.play(probe.animate.set_value(2.5),run_time=5)
            self.change(info,formula(r'V_\theta=u_1h_1+u_2h_2+u_3h_3+b_{out}',29));self.wait(1)

if __name__=='__main__':run_independent(NeuronExplained)
