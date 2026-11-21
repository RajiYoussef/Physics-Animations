"""Chapter 6: position-space orbit and velocity-space circle."""
from film_core import *


class Scene06UniformCircularMotion(FilmScene):
    chapter_id=6

    def construct(self):
        self.opening("الحركة الدائرية المنتظمة","POSITION SPACE / VELOCITY SPACE")
        center=np.array([-3.35,-.1,0]);radius=2.05
        theta=ValueTracker(-PI/3)
        angular_rate=3*PI/(.72*self.shot_info(0)[0]+.73*self.shot_info(1)[0])
        arc_step=angular_rate*.18*self.shot_info(0)[0]
        def position():return center+radius*radial(theta.get_value())
        orbit=Circle(radius=radius,color=GHOST,stroke_width=2).move_to(center)
        earth=Earth(.72).move_to(center)
        satellite=Satellite().scale(.65)
        satellite.add_updater(lambda m:m.move_to(position()))
        v=always_redraw(lambda:vector(position(),tangent(theta.get_value()),1.05))
        a=always_redraw(lambda:vector(position(),-radial(theta.get_value()),.8,ACCELERATION))
        self.add(earth,orbit,satellite)
        with self.shot(0) as d:
            self.caption_ar("يقطع القمر الصناعي مسافة متساوية في كل فترة زمنية متساوية.")
            title=ar("مقدار السرعة ثابت، لا يتغير",30,color=VELOCITY).move_to([3.4,1.3,0])
            equal=VGroup(*[Arc(radius=radius,start_angle=-PI/3+j*arc_step,angle=arc_step-.06,
                               arc_center=center,color=VELOCITY,stroke_width=4)
                          for j in range(4)])
            markers=VGroup(*[Dot(center+radius*radial(-PI/3+j*arc_step),radius=.05,color=INK)
                            for j in range(5)])
            self.play(FadeIn(title),run_time=d*.04)
            for j in range(4):
                self.play(theta.animate.set_value(-PI/3+(j+1)*arc_step),
                          Create(equal[j]),FadeIn(markers[j]),run_time=d*.18,rate_func=linear)
            self.add(markers[-1])
            label_time=math_label("Δt   Δt   Δt   Δt",24,MUTED).move_to([3.4,.45,0])
            self.play(FadeIn(label_time),run_time=d*.05)
            self.checkpoint("equal_arcs")
        with self.shot(1) as d:
            self.caption_ar("يشير متجه السرعة دائما في اتجاه الحركة، بينما يشير متجه التسارع نحو الداخل.")
            self.play(FadeOut(title),FadeOut(label_time),run_time=d*.03)
            self.add(v,a)
            angle_mark=always_redraw(lambda:right_angle_at(position(),theta.get_value()))
            self.add(angle_mark)
            velocity_origin=np.array([3.35,-.1,0]);velocity_radius=1.35
            velocity_circle=Circle(radius=velocity_radius,color=GHOST,stroke_width=1).move_to(velocity_origin)
            speed_vector=always_redraw(lambda:vector(velocity_origin,tangent(theta.get_value()),velocity_radius))
            head=always_redraw(lambda:Dot(velocity_origin+velocity_radius*tangent(theta.get_value()),radius=.055,color=VELOCITY))
            chart_title=ar("نرسم السرعة من نقطة ثابتة",26,width=5).move_to([3.35,2.2,0])
            chart_note=ar("مقدار متجه السرعة ثابت، أما ما يتغير فهو اتجاهه.",24,width=5,color=VELOCITY).move_to([3.35,-2.1,0])
            self.play(Create(velocity_circle),FadeIn(chart_title),FadeIn(chart_note),run_time=d*.06)
            self.add(speed_vector,head)
            self.play(theta.animate.increment_value(angular_rate*d*.73),run_time=d*.73,rate_func=linear)
            self.checkpoint("velocity_space_circle")
        satellite.clear_updaters();v.clear_updaters();a.clear_updaters()
        angle_mark.clear_updaters();speed_vector.clear_updaters();head.clear_updaters()
        with self.shot(2) as d:
            self.caption_ar("حتى مع ثبات المقدار، يظلّ الاتجاه يتغيّر")
            base=float(theta.get_value())
            p=velocity_origin
            first=vector(p,tangent(base),velocity_radius)
            second=vector(p,tangent(base+PI/4),velocity_radius)
            delta=Arrow(p+velocity_radius*tangent(base),p+velocity_radius*tangent(base+PI/4),
                        buff=0,color=ACCELERATION,stroke_width=4)
            self.play(FadeOut(speed_vector),FadeOut(head),GrowArrow(first),run_time=d*.07)
            self.play(TransformFromCopy(first,second),run_time=d*.1)
            self.play(GrowArrow(delta),run_time=d*.08)
            text=equation(math_label("Δv",34,ACCELERATION),"=",math_label("v2",34,VELOCITY),"-",math_label("v1",34,VELOCITY)).move_to([3.35,-2.35,0])
            self.play(FadeOut(chart_note),FadeIn(text),run_time=d*.05)
            ninety=math_label("90°",23,INK).move_to(position()+.55*(tangent(base)-radial(base)))
            self.play(FadeIn(ninety),Indicate(a,color=ACCELERATION),run_time=d*.09)
            self.checkpoint("constant_speed_nonzero_delta_v")
        self.finish()


if __name__=="__main__":
    render_chapter(Scene06UniformCircularMotion)
