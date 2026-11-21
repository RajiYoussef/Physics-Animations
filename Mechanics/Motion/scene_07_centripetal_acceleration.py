"""Chapter 7: derive a=v²/r, then show both parameter comparisons."""
from film_core import *


def comparison_orbit(center,radius,speed,clock,acceleration_scale=.7):
    """Same time tracker and common arrow scale make the comparison quantitative."""
    center=np.asarray(center,float)
    def angle():return speed*clock.get_value()/radius-PI/2
    def point():return center+radius*radial(angle())
    circle=Circle(radius=radius,color=GHOST,stroke_width=1.7).move_to(center)
    ball=always_redraw(lambda:Dot(point(),radius=.065,color=INK))
    vel=always_redraw(lambda:vector(point(),tangent(angle()),speed*.45))
    acc=always_redraw(lambda:vector(point(),-radial(angle()),acceleration_scale*speed*speed/radius,ACCELERATION))
    return VGroup(circle,ball,vel,acc)


class Scene07CentripetalAcceleration(FilmScene):
    chapter_id=7

    def construct(self):
        self.opening("من تغيّر الاتجاه إلى مقدار التسارع","GEOMETRY / PREDICTION")
        with self.shot(0) as d:
            self.caption_ar("لاحظ الزاوية: هي نفسها في المثلثين")
            left=np.array([-3.9,-.1,0]);right=np.array([.6,-.1,0])
            angle=ValueTracker(.65);r=1.7;v=1.35
            def radius_triangle():
                a,b=-angle.get_value()/2,angle.get_value()/2
                return VGroup(Line(left,left+r*radial(a),color=GHOST),
                              Line(left,left+r*radial(b),color=GHOST),
                              Line(left+r*radial(a),left+r*radial(b),color=DISPLACEMENT,stroke_width=4))
            def velocity_triangle():
                a,b=-angle.get_value()/2,angle.get_value()/2
                return VGroup(vector(right,tangent(a),v),vector(right,tangent(b),v),
                              Arrow(right+v*tangent(a),right+v*tangent(b),buff=0,color=ACCELERATION,stroke_width=4))
            rtri=always_redraw(radius_triangle);vtri=always_redraw(velocity_triangle)
            arc=always_redraw(lambda:Arc(radius=r,start_angle=-angle.get_value()/2,
                                         angle=angle.get_value(),arc_center=left,color=DISPLACEMENT,stroke_width=3))
            angle_marks=always_redraw(lambda:VGroup(
                Arc(radius=.4,start_angle=-angle.get_value()/2,angle=angle.get_value(),
                    arc_center=left,color=PURPLE,stroke_width=3),
                Arc(radius=.4,start_angle=PI/2-angle.get_value()/2,angle=angle.get_value(),
                    arc_center=right,color=PURPLE,stroke_width=3)))
            top=VGroup(ar("الموضع",27,color=DISPLACEMENT).move_to([-3.3,2.25,0]),
                       ar("السرعة",27,color=VELOCITY).move_to([.6,2.25,0]))
            exact=tex(r"\frac{|\Delta\vec v|}{v}=\frac{|\Delta\vec r|}{r}",32).move_to([-1.1,-1.45,0])
            limit_note=ar(" في اللحظة ذاتها",24,width=6).move_to([-1.1,-2.1,0])
            annotations=VGroup(math_label("r",26,MUTED).move_to([-3.1,-.5,0]),
                              math_label("v",26,VELOCITY).move_to([.9,.65,0]),
                              math_label("Δr",23,DISPLACEMENT).move_to([-1.8,-.1,0]),
                              math_label("Δθ",22,PURPLE).move_to(left+[.6,.4,0]),
                              math_label("Δθ",22,PURPLE).move_to(right+[-.5,.35,0]))
            self.add(rtri,vtri,arc,top,annotations,angle_marks)
            self.play(FadeIn(exact),run_time=d*.07)
            self.checkpoint("similar_triangles")
            self.play(angle.animate.set_value(.12),FadeIn(limit_note),run_time=d*.23)
            # The finite identity uses the chord; ds=v dt holds in the small-interval limit.
            steps=VGroup(tex(r"\frac{|\Delta\vec v|}{v}\approx\frac{v\,\Delta t}{r}",30),
                         tex(r"\lim_{\Delta t\to0}\frac{|\Delta\vec v|}{\Delta t}=\frac{v^2}{r}",28)).arrange(DOWN,buff=.4).move_to([4,1.1,0])
            self.play(FadeIn(steps),run_time=d*.08)
            formula=tex(r"a=\frac{v^2}{r}",48,ACCELERATION).move_to([4,-1.1,0])
            self.play(FadeIn(formula,shift=UP*.15),run_time=d*.08)
            self.check_layout(steps,formula)
            self.checkpoint("small_interval_derivation")
            rtri.clear_updaters();vtri.clear_updaters();arc.clear_updaters();angle_marks.clear_updaters()
        self.clear_stage()
        with self.shot(1) as d:
            self.caption_ar("ماذا يحدث لو ضاعفنا السرعة؟")
            clock=ValueTracker(0)
            # r=1.5 for both, speeds 1 and 2: a ratio exactly 4.
            first=comparison_orbit([-3.2,-.15,0],1.5,1,clock,.5)
            second=comparison_orbit([3.2,-.15,0],1.5,2,clock,.5)
            labels=VGroup(math_label("v",30,VELOCITY).move_to([-3.2,2.2,0]),
                          math_label("2v",30,VELOCITY).move_to([3.2,2.2,0]),
                          math_label("a",34,ACCELERATION).move_to([-3.2,-2.3,0]),
                          math_label("4a",34,ACCELERATION).move_to([3.2,-2.3,0]))
            self.add(first,second,labels)
            self.play(clock.animate.set_value(4),run_time=d*.38,rate_func=linear)
            self.checkpoint("double_speed_four_acceleration")
            first.clear_updaters(recursive=True);second.clear_updaters(recursive=True)
            self.clear_stage()
            self.caption_ar("عندما يكون نصف القطر أكبر")
            clock2=ValueTracker(0)
            small=comparison_orbit([-3.4,-.15,0],.95,1,clock2,.75)
            large=comparison_orbit([3,-.15,0],1.9,1,clock2,.75)
            notes=VGroup(math_label("r",30).move_to([-3.4,2.3,0]),
                         math_label("2r",30).move_to([3,2.3,0]),
                         math_label("a",32,ACCELERATION).move_to([-3.4,-2.5,0]),
                         math_label("a / 2",32,ACCELERATION).move_to([3,-2.5,0]),
                         ar("السرعة نفسها",23,color=VELOCITY).move_to([0,2.35,0]))
            self.add(small,large,notes)
            self.play(clock2.animate.set_value(4),run_time=d*.38,rate_func=linear)
            self.checkpoint("double_radius_half_acceleration")
            small.clear_updaters(recursive=True);large.clear_updaters(recursive=True)
        self.clear_stage()
        with self.shot(2) as d:
            self.caption_ar("عندما تتغير السرعة المتجهة، يحدث تسارع.",ACCELERATION)
            clock=ValueTracker(0)
            labels=VGroup(*[ar(text,28,width=3.8).move_to([x,2,0]) for text,x in
                             zip(["تزداد السرعة","تنخفض السرعة","يتغيّر الاتجاه"],[-4.3,0,4.3])])
            grow=always_redraw(lambda:vector([-5.3,.35,0],RIGHT,.7+clock.get_value()))
            shrink=always_redraw(lambda:vector([-1,.35,0],RIGHT,1.7-clock.get_value()))
            turn=always_redraw(lambda:vector([4.3,.35,0],radial(clock.get_value()*PI/2),1.3))
            acceleration=VGroup(vector([-5.3,-.7,0],RIGHT,.8,ACCELERATION),
                                vector([.8,-.7,0],LEFT,.8,ACCELERATION))
            normal=always_redraw(lambda:vector([4.3,-.7,0],tangent(clock.get_value()*PI/2),.8,ACCELERATION))
            self.add(labels,grow,shrink,turn,acceleration,normal)
            self.play(clock.animate.set_value(1),run_time=d*.35,rate_func=linear)
            for obj in (grow,shrink,turn,normal):obj.clear_updaters()
            final=tex(r"\vec a=\frac{d\vec v}{dt}",42,ACCELERATION).move_to([0,-2,0])
            self.play(FadeIn(final),run_time=d*.08)
            self.checkpoint("final_recap")
        self.finish()


if __name__=="__main__":
    render_chapter(Scene07CentripetalAcceleration)
