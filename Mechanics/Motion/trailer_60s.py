"""One-minute trailer. Press PyCharm Run; uses the neighbouring film helpers.

On-screen Arabic is taken from the user's edited scenes. Original scenes are
not modified. QUALITY and BACKGROUND follow settings.py. Optional soundtrack:
audio/trailer_60s.wav (record approximately 60 seconds; no automatic time stretch).
"""
from film_core import *


class MotionTrailer(Scene):
    def caption(self, text):
        self.add(ar(text, 29, width=12.4).move_to([0, -3.25, 0]))

    def end_beat(self, deadline, name):
        remaining = deadline - float(self.time)
        if remaining > 1 / config.frame_rate:
            self.wait(remaining)
        review = ROOT / 'review' / 'trailer'
        review.mkdir(parents=True, exist_ok=True)
        self.renderer.static_image = None
        self.renderer.update_frame(self)
        from PIL import Image
        Image.fromarray(self.renderer.get_frame()).save(review / (name + '.png'))
        for mob in self.mobjects:
            mob.clear_updaters(recursive=True)
        self.clear()

    def construct(self):
        soundtrack = ROOT / 'audio' / 'trailer_60s.wav'
        if settings.USE_AUDIO and soundtrack.exists():
            self.add_sound(str(soundtrack))

        # 0–7: the question, with a vector rotating behind it.
        question = VGroup(ar('هل يمكن لجسم ما أن يتسارع', 40),
                          ar('دون زيادة في سرعته؟', 40, color=VELOCITY))
        question.arrange(DOWN, buff=.25).shift(UP * 1.1)
        angle = ValueTracker(0)
        arrow = always_redraw(lambda: vector([0, -1.5, 0], radial(angle.get_value()), 1.5))
        self.play(FadeIn(question, shift=UP*.15), run_time=1)
        self.add(arrow)
        self.play(angle.animate.set_value(PI*.65), run_time=4, rate_func=smooth)
        self.end_beat(7, '01_question')

        # 7–17: identical readouts, different directions.
        self.add(ar('السرعة والسرعة المتجهة', 36).move_to([0, 2.8, 0]))
        self.caption('تتطابق السرعتان، لكن السيارتين تتجهان في اتجاهين مختلفين.')
        right = Car(length=1).move_to([-4, -.2, 0])
        left = Car(length=1).pose([4, -.2, 0], PI)
        arrows = VGroup(vector([-4, .6, 0], RIGHT, 1.4), vector([4, .6, 0], LEFT, 1.4))
        numbers = VGroup(*[math_label('50 km/h', 36, VELOCITY).move_to([x, 1.6, 0]) for x in (-3.5, 3.5)])
        self.add(right, left, arrows, numbers)
        self.play(right.animate.shift(RIGHT*1.5), left.animate.shift(LEFT*1.5),
                  arrows[0].animate.shift(RIGHT*1.5), arrows[1].animate.shift(LEFT*1.5),
                  run_time=6, rate_func=linear)
        self.play(FadeIn(ar('العداد لا يخبرنا بالاتجاه', 30).move_to([0,-1.7,0])), run_time=1)
        self.end_beat(17, '02_direction')

        # 17–27: braking, with speed and position linked by x(t).
        self.add(ar('التسارع لا يعني دائماً زيادة السرعة', 34).move_to([0,2.8,0]))
        self.caption('عندما نضغط على المكابح')
        t = ValueTracker(0)
        def pos():
            u=t.get_value()
            return np.array([-4 + .9*u - .025*u*u, -.5, 0])
        car = Car(length=.9)
        car.add_updater(lambda m:m.pose(pos(),0))
        speed = always_redraw(lambda:vector(pos()+UP*.55, RIGHT, 1.7-.08*t.get_value()))
        acceleration = always_redraw(lambda:vector(pos()+UP*1.2, LEFT, .8, ACCELERATION))
        self.add(Line([-5,-.5,0],[5,-.5,0],color=GHOST),car,speed,acceleration)
        self.play(t.animate.set_value(8),run_time=8,rate_func=linear)
        self.end_beat(27, '03_braking')

        # 27–40: constant speed around a bend.
        self.add(ar('يتغيّر الاتجاه، ويبقى المقدار ثابتاً',34).move_to([0,2.8,0]))
        self.caption('ما يحدث هو أن الاتجاه يتغير.')
        center=np.array([-2.5,.1,0]); theta=ValueTracker(-PI/2)
        def position():return center+1.8*radial(theta.get_value())
        car=Car(length=.75)
        car.add_updater(lambda m:m.pose(position(),theta.get_value()+PI/2))
        velocity=always_redraw(lambda:vector(position(),tangent(theta.get_value()),1.1))
        acceleration=always_redraw(lambda:vector(position(),-radial(theta.get_value()),.8,ACCELERATION))
        gauge=SpeedGauge(lambda:50).move_to([3.6,.8,0])
        self.add(arc_road(center,1.8,-PI/2,PI*1.4),car,velocity,gauge)
        self.play(theta.animate.set_value(.1*PI),run_time=5,rate_func=linear)
        self.add(acceleration,ar('هذه أيضا حالة تسارع',29,color=ACCELERATION).move_to([3.6,-1,0]))
        self.play(theta.animate.set_value(.7*PI),run_time=5,rate_func=linear)
        self.end_beat(40, '04_turn')

        # 40–51: the same idea, now in orbit.
        self.add(ar('الحركة الدائرية المنتظمة',36).move_to([0,2.8,0]))
        self.caption('حتى مع ثبات المقدار، يظلّ الاتجاه يتغيّر')
        center=np.array([-2.7,0,0]); theta=ValueTracker(-PI/3)
        earth=Earth(.7).move_to(center)
        satellite=Satellite()
        def orbital_position():return center+1.8*radial(theta.get_value())
        satellite.add_updater(lambda m:m.move_to(orbital_position()))
        arrows=always_redraw(lambda:orbit_arrows(orbital_position(),theta.get_value(),1,.7))
        self.add(earth,Circle(radius=1.8,color=GHOST).move_to(center),satellite,arrows)
        self.add(ar('مقدار السرعة ثابت، لا يتغير',28,width=5).move_to([3.4,.9,0]))
        self.add(tex(r'a=\frac{v^2}{r}',48,ACCELERATION).move_to([3.4,-.7,0]))
        self.play(theta.animate.increment_value(PI*1.5),run_time=9,rate_func=linear)
        self.end_beat(51, '05_orbit')

        # 51–60: leave a question for the full lesson.
        self.play(FadeIn(ar('ماذا يحدث لو ضاعفنا السرعة؟',40).move_to([0,1.6,0])),run_time=1)
        expression=tex(r'v\ \longrightarrow\ 2v',52,VELOCITY).move_to([0,.1,0])
        self.play(Write(expression),run_time=2)
        self.play(FadeIn(ar('من تغيّر الاتجاه إلى مقدار التسارع',32).move_to([0,-1.6,0])),run_time=1)
        self.wait(4)
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=1)


if __name__ == '__main__':
    quality=os.environ.get('PHYSICS_QUALITY',settings.QUALITY)
    w,h,fps={'preview':(854,480,15),'draft':(1280,720,30),'final':(1920,1080,60)}[quality]
    folder=ROOT/'videos'; folder.mkdir(exist_ok=True)
    with tempconfig({'pixel_width':w,'pixel_height':h,'frame_rate':fps,
                     'frame_width':128/9,'frame_height':8,'background_color':settings.BACKGROUND,
                     'media_dir':str(ROOT/'_render_cache'),'video_dir':str(folder),
                     'output_file':'trailer_60s','disable_caching':True,'preview':False}):
        scene=MotionTrailer(); scene.render()
        output=Path(scene.renderer.file_writer.movie_file_path)
    print(output)
    if settings.OPEN_AFTER_RENDER and os.environ.get('PHYSICS_BATCH')!='1':
        os.startfile(str(output))
