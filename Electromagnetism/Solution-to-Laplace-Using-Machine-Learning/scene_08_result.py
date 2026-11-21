from explainer_tools import *

class FinalResult(Explainer):
    chapter=8
    def construct(self):
        with self.beat(0):
            self.heading('يمثل هذا الرسم البياني الحل الذي حسبته الشبكة العصبية')
            self.cue('ارتفاع السطح يمثل قيمة الجهد')
            p=self.data['weights'][-1];axis=self.data['axis'];field=self.data['fields'][-1]
            a=ThreeDAxes(x_range=[0,PI,PI/2],y_range=[0,PI,PI/2],z_range=[0,1,.5],x_length=5,y_length=5,z_length=2.7)
            self.set_camera_orientation(phi=62*DEGREES,theta=-65*DEGREES)
            self.add(a);lines=VGroup()
            for j in range(0,len(axis),2):
                row=VMobject(color=CYAN,stroke_width=1.4).set_points_as_corners([a.c2p(x,axis[j],field[j,i]) for i,x in enumerate(axis)])
                col=VMobject(color=CYAN,stroke_width=1.1).set_points_as_corners([a.c2p(axis[j],y,field[i,j]) for i,y in enumerate(axis)])
                lines.add(row,col)
            self.play(LaggedStart(*[Create(m) for m in lines],lag_ratio=.04),run_time=4)
            labels=VGroup(formula('x',26).move_to(a.c2p(PI+.3,0,0)),formula('y',26).move_to(a.c2p(0,PI+.3,0)),formula('V',26).move_to(a.c2p(0,0,1.2)));self.add_fixed_orientation_mobjects(*labels)
            bottom=VMobject(color=GREEN,stroke_width=4).set_points_as_corners([a.c2p(x,0,field[0,i]) for i,x in enumerate(axis)])
            self.play(Create(bottom),run_time=2);self.move_camera(theta=-110*DEGREES,run_time=7)
            self.cue('الحافة السفلى تتبع دالة الجيب والجهد يقترب من الصفر على الحواف الأخرى')
            self.move_camera(theta=-75*DEGREES,run_time=4)
        self.reset();self.set_camera_orientation(phi=0,theta=-PI/2)
        with self.beat(1):
            self.heading('نقارن بين الحلين عند الإحداثيات نفسها')
            p=self.data['weights'][-1];a,l=domain();self.add(a,l,cell_map(a,lambda x,y:evaluate(p,x,y)),colour_key())
            b,bl=graph([0,PI,PI/2],[0,1.05,.5],5,3.2,[3.3,0,0],'x','V(x,y)',[(0,'0'),(PI,r'\pi')],[(0,'0'),(1,'1')]);self.add(b,bl)
            y=ValueTracker(0);xs=np.linspace(0,PI,150)
            predicted=always_redraw(lambda:sampled(b,xs,evaluate(p,xs,np.full_like(xs,y.get_value())),CYAN))
            reference=always_redraw(lambda:DashedVMobject(sampled(b,xs,exact(xs,y.get_value()),GREEN),num_dashes=35))
            cut=always_redraw(lambda:Line(a.c2p(0,y.get_value()),a.c2p(PI,y.get_value()),color=AMBER,stroke_width=3));self.add(predicted,reference,cut)
            self.reveal(ar('يمثل اللون الأزرق حل الشبكة، بينما يمثل الخط الأخضر المتقطع الحل التحليلي.',22,width=11).move_to([0,2.7,0]))
            self.cue('الحل التحليلي لم يدخل في التدريب')
            for target in [PI/4,PI/2,3*PI/4,PI]:self.play(y.animate.set_value(target),run_time=3,rate_func=linear)
            self.reveal(formula(r'V(x,y)=\sin x\,\frac{\sinh(\pi-y)}{\sinh\pi}',29).move_to([3.3,-2.5,0]))
            self.wait(2)
        self.reset()
        with self.beat(2):
            self.heading('لا يكفي الحصول على رسمين بيانيين متشابهين, إذ نحتاج إلى رصد الاختلافات الطفيفة')
            p=self.data['weights'][-1];a,l=graph([0,PI,PI/2],[-.012,.012,.006],6,3.5,[-3,0,0],'x',r'V_\theta-V',[(0,'0'),(PI,r'\pi')],[(-.01,'-0.01'),(0,'0'),(.01,'0.01')]);self.add(a,l)
            xs=np.linspace(0,PI,160);y=ValueTracker(0)
            error=always_redraw(lambda:sampled(a,xs,evaluate(p,xs,np.full_like(xs,y.get_value()))-exact(xs,y.get_value()),AMBER));self.add(error,meter('y',y,[3.5,1.9,0]))
            self.cue('نكبِر الأخطاء لنرى الفروق بوضوح')
            for target in [PI/4,PI/2,3*PI/4,PI]:self.play(y.animate.set_value(target),run_time=2.5)
            metrics=json.loads((ROOT/'data/metadata.json').read_text())['metrics']
            info=VGroup(ar('خطأ نسبي على نقاط جديدة',23,width=5),formula(fr'{metrics["relative_L2"]*100:.3f}\%',31,AMBER),ar('أكبر خطأ مقاس على الحدود',23,width=5),formula(f'{metrics["boundary_max_abs"]:.4f}',29,GREEN)).arrange(DOWN,buff=.3).move_to([3.5,-.3,0]);self.reveal(info)
            self.cue('هذه نتيجة تقريبية اختبرناها عدديًا؛ وهي ليست حلا تحليليا دقيقا.ً')
            self.wait(2)

if __name__=='__main__':run_independent(FinalResult)
