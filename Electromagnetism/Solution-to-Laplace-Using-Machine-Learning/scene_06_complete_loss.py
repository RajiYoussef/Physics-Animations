from explainer_tools import *

class CompleteLoss(Explainer):
    chapter=6
    def construct(self):
        with self.beat(0):
            self.heading('نقيس الفارق بين التخمين والشرط الحدّي')
            a,l=graph([0,PI,PI/2],[-.1,1.3,.5],6,3.3,[-3,-.1,0],'x','V(x,0)',[(0,'0'),(PI/2,r'\pi/2'),(PI,r'\pi')],[(0,'0'),(1,'1')]);self.add(a,l)
            xs=np.linspace(0,PI,121);scale=ValueTracker(.65);offset=ValueTracker(.2)
            target=sampled(a,xs,np.sin(xs),GREEN);self.play(Create(target),run_time=1)
            line=always_redraw(lambda:sampled(a,xs,scale.get_value()*np.sin(xs)+offset.get_value(),CYAN));self.add(line)
            locations=np.linspace(.15,PI-.15,9)
            gaps=always_redraw(lambda:VGroup(*[Line(a.c2p(x,np.sin(x)),a.c2p(x,scale.get_value()*np.sin(x)+offset.get_value()),color=AMBER,stroke_width=3) for x in locations]));self.add(gaps)
            self.reveal(ar('الأخضر: المطلوب',23,width=3,color=GREEN).move_to([-4.4,2.55,0]),ar('الأزرق: تخمين توضيحي',23,width=3.5,color=CYAN).move_to([-1,2.55,0]))
            equation=VGroup(formula(r'x=\pi/2',29),formula('e=0.85-1=-0.15',29,AMBER),formula('e^2=0.0225',29,AMBER)).arrange(DOWN,buff=.6).move_to([3.7,.5,0]);self.reveal(equation)
            self.cue('تمثل الأجزاء الصفراء الفروق. نقوم بتربيع كل من هذه الفروق، ثم نحسب متوسطها.')
            self.wait(2);self.play(FadeOut(equation),run_time=.5)
            loss=ValueTracker(float(np.mean((.65*np.sin(locations)+.2-np.sin(locations))**2)))
            loss.add_updater(lambda m:m.set_value(float(np.mean((scale.get_value()*np.sin(locations)+offset.get_value()-np.sin(locations))**2))))
            self.add(loss,meter(r'\mathcal{L}_{bottom}',loss,[3.5,.5,0],places=4))
            self.cue('نُقرِّب المنحنيين من بعضهما البعض، فتتقلص الفروقات، وينخفض الخطأ تبعا لذلك، حتى يتطابقا تماما.')
            self.play(scale.animate.set_value(.9),offset.animate.set_value(.08),run_time=4)
            self.play(scale.animate.set_value(1),offset.animate.set_value(0),run_time=4)
            self.reveal(formula(r'\mathcal{L}_{bottom}=\frac{1}{M}\sum_j e_j^2',28,width=5).move_to([3.5,-1.2,0]));self.wait(2)
            self.code_flash('boundary_loss',2)
        self.reset()
        with self.beat(1):
            self.heading('نجمع الخطأ الموجود في الداخل والأخطاء عند الحواف الأربع.')
            vals=self.data['losses'][-1];names=[r'PDE','bottom','left','right','top'];arabic=['داخل المنطقة','الحافة السفلى','الحافة اليسرى','الحافة اليمنى','الحافة العليا']
            self.cue('مثال من نتائج الشبكة: كل حد في المجموع يأتي من اختبار مختلف')
            total=0;running=formula('0',34,AMBER).move_to([3.6,0,0]);self.add(running)
            for i,(name,value,meaning) in enumerate(zip(names,vals,arabic)):
                row=VGroup(ar(meaning,23,width=2.8),formula(fr'\mathcal{{L}}_{{{name}}}='+scientific(value),24,CYAN if i==0 else GREEN)).arrange(RIGHT,buff=.4).move_to([-2.5,2-i*.9,0])
                self.reveal(row);total+=float(value)
                updated=formula(f'{total:.5f}',34,AMBER).move_to(running)
                pulse=Dot(row[1].get_right()+RIGHT*.1,radius=.06,color=AMBER);self.add(pulse)
                self.play(pulse.animate.move_to([3.6,-1,0]),run_time=.7);self.remove(pulse)
                token=formula('+'+scientific(value),24,GREEN).move_to([3.6,-1,0])
                self.play(FadeIn(token),run_time=.2)
                self.play(FadeOut(token),FadeOut(running),run_time=.2)
                self.play(FadeIn(updated),run_time=.2);running=updated
                self.wait(.5)
            self.reveal(formula(r'\mathcal{L}=\mathcal{L}_{PDE}+\sum_{edges}\mathcal{L}_{edge}',29,width=5.2).move_to([3.5,1.7,0]))
            #self.cue('هذا هو العدد الذي نريد تقليله؛ له خمسة مصادر واضحة')
            #self.wait(1);self.code_flash('loss',2)

            self.cue('هذا هو الرقم الذي نسعى إلى تقليله. وله خمسة مصادر واضحة.')
            self.wait(2)
            self.code_flash('boundary', 4)


if __name__=='__main__':run_independent(CompleteLoss)
