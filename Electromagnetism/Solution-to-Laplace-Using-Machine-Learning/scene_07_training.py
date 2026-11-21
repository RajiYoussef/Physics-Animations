from explainer_tools import *

class Training(Explainer):
    chapter=7
    def construct(self):
        with self.beat(0):
            self.heading('أي تعديل يجعل الخطأ أصغر؟')
            a,l=graph([-1.5,3.5,1],[0,10,2],6,3.5,[-3,0,0],'w','L(w)',[(-1,'-1'),(0,'0'),(2,'2')],[(0,'0'),(4,'4'),(9,'9')]);self.add(a,l)
            xs=np.linspace(-1,3.5,150);self.play(Create(sampled(a,xs,(xs-2)**2,AMBER)),run_time=1.5)
            self.reveal(formula('L(w)=(w-2)^2',31,AMBER).move_to([3.5,2,0]))
            self.cue('مثال مبسط بمعامل واحد: نتحرك في الاتجاه الذي يقلل الخطأ')
            w=ValueTracker(-1);dot=always_redraw(lambda:Dot(a.c2p(w.get_value(),(w.get_value()-2)**2),color=GREEN))
            tangent=always_redraw(lambda:TangentLine(a,lambda q:(q-2)**2,w.get_value(),derivative=lambda q:2*(q-2),span=.6,color=GREEN));self.add(dot,tangent)
            read=None
            for _ in range(3):
                old=w.get_value();g=2*(old-2);new_w=old-.2*g
                new=VGroup(formula(fr'L^\prime(w)={g:.3f}',29),formula(fr'w_{{new}}={old:.3f}-0.2({g:.3f})',25),formula(fr'w_{{new}}={new_w:.3f}',29,GREEN)).arrange(DOWN,buff=.5).move_to([3.4,-.1,0])
                if read is None:self.reveal(new)
                else:self.play(ReplacementTransform(read,new),run_time=.6)
                read=new;self.wait(1);self.play(w.animate.set_value(new_w),run_time=2.5)
            self.cue('في الشبكة العصبية، نطبِق هذا المفهوم على جميع الأوزان والانحيازات')
            self.wait(1)
        self.reset()
        with self.beat(1):
            self.heading('في التدريب الفعلي: تتغير الدالة ويقل الخطأ')
            epochs=self.data['epochs'];losses=self.data['losses'].sum(axis=1);weights=self.data['weights'];xs=np.linspace(0,PI,150)
            curves=[evaluate(p,xs,np.full_like(xs,PI/2)) for p in weights]
            low=float(np.floor(np.min(curves)));high=float(np.ceil(np.max(curves)))
            a,l=graph([0,PI,PI/2],[low,high,max(1,(high-low)/4)],5,3.6,[-3.6,0,0],'x',r'V_\theta(x,\pi/2)',[(0,'0'),(PI,r'\pi')],[(low,f'{low:g}'),(0,'0'),(high,f'{high:g}')])
            b,bl=graph([0,10000,5000],[-6,3,3],5,3.6,[3.3,0,0],r'k',r'\log_{10}\mathcal{L}',[(0,'0'),(5000,'5000'),(10000,'10000')],[(-6,'-6'),(-3,'-3'),(0,'0'),(3,'3')]);self.add(a,l,b,bl)
            line=sampled(a,xs,curves[0]);trace=VMobject(color=AMBER);self.add(line,trace)
            ref=sampled(a,xs,exact(xs,PI/2),GREEN).set_stroke(opacity=.6);self.add(ref)
            self.reveal(ar('الأخضر: الحل التحليلي للمقارنة',20,width=5,color=GREEN).move_to([-3.6,-2.8,0]))
            counter=Text('k = 0',font=settings.CODE_FONT,font_size=25).move_to([0,2.65,0]);self.add(counter)
            self.cue('هو رقم خطوة التدريب. هنا، كل لقطة لها أهميتها الفعلية "k"ً')
            positions=[]
            for i,k in enumerate(epochs):
                line.set_values(curves[i]);positions.append(b.c2p(float(k),float(np.log10(losses[i]))))
                if len(positions)>1:trace.set_points_as_corners(positions)
                self.remove(counter);counter=Text(f'k = {k}',font=settings.CODE_FONT,font_size=25).move_to([0,2.65,0]);self.add(counter)
                self.wait(.48)
            self.cue(' التغير يمثل تحسن التقريب')
            self.wait(1)
            self.cue('عند اكتمال التدريب، نقوم الآن بتوسيع نطاق المحور الرأسي لعرض الجزء النهائي.')
            self.play(FadeOut(line),FadeOut(ref),FadeOut(a),FadeOut(l),run_time=.5)
            zoom,zl=graph([0,PI,PI/2],[-.02,.24,.1],5,3.6,[-3.6,0,0],'x',r'V_\theta(x,\pi/2)',[(0,'0'),(PI,r'\pi')],[(0,'0'),(.1,'0.1'),(.2,'0.2')])
            self.add(zoom,zl)
            self.play(Create(sampled(zoom,xs,curves[-1],CYAN)),Create(DashedVMobject(sampled(zoom,xs,exact(xs,PI/2),GREEN),num_dashes=30)),run_time=2)
            self.wait(2)
        self.reset()
        with self.beat(2):
            self.heading('نستخدم ما يُسمى بالزخم.')
            equations=[r'\theta_{look}=\theta_k+\mu v_k',r'g_k=\nabla_\theta\mathcal{L}(\theta_{look})',r'v_{k+1}=\mu v_k-\eta g_k',r'\theta_{k+1}=\theta_k+v_{k+1}']
            labels=['نتقدم قليلاً في اتجاه الخطوة السابقة','نحسب التدرج في الموضع المتقدم','نجمع أثر الزخم مع التعديل الجديد','نحدّث معاملات الشبكة']
            for i,(source,text) in enumerate(zip(equations,labels)):
                row=VGroup(formula(source,30,AMBER if i==1 else CYAN),ar(text,23,width=5.5)).arrange(RIGHT,buff=.55).move_to([0,2-i*1.05,0]);self.reveal(row)
                self.wait(.8)
            self.cue('يُبقي الزخم  على تأثير الخطوة السابقة، بينما يعمل معدل التعلم  على تعديل مقدار التحديث')
            self.wait(1);self.code_flash('update',2)

if __name__=='__main__':run_independent(Training)
