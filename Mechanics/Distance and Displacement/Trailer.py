"""40-second trailer for Distance vs Displacement — run directly in PyCharm.
Requires: manim, numpy. Artwork is generated as an SVG automatically.
Optional: put trailer_music.mp3 or trailer_music.wav next to this script.
Set TRAILER_FAST=1 in PyCharm environment variables for a quick preview.
"""
from html import escape
from pathlib import Path
import math
import os
import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent
BG, WHITEISH = '#0D1117', '#E6EDF3'
GOLD, CYAN, GREEN, MUTED = '#F4B85A', '#46D9FF', '#3FBF91', '#9CA3AF'
ARABIC_FONT, ENGLISH_FONT = 'Arial', 'DejaVu Sans'
FAST = os.getenv('TRAILER_FAST', '0') == '1'


def track_svg():
    """Generate a four-lane stadium track, with a clear finish line."""
    destination = ROOT / 'trailer_assets' / 'running_track.svg'
    destination.parent.mkdir(parents=True, exist_ok=True)

    def oval(r):
        return (f'M {725+r} 300 A {r} {r} 0 0 0 725 {300-r} '
                f'H 275 A {r} {r} 0 0 0 {275-r} 300 '
                f'A {r} {r} 0 0 0 275 {300+r} H 725 '
                f'A {r} {r} 0 0 0 {725+r} 300 Z')

    boundaries = '\n'.join(
        f'<path d="{oval(r)}" fill="none" stroke="#FFE8D6" '
        f'stroke-width="2.7" opacity="0.82"/>'
        for r in (151, 140, 129, 118)
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600">
      <path d="{oval(162)}" fill="#B34E48" stroke="#E2A88D" stroke-width="4"/>
      {boundaries}
      <path d="{oval(108)}" fill="#225746" stroke="#F7D6B6" stroke-width="3"/>
      <path d="M 540 300 H 710 M 625 205 V 395" stroke="#6CA48C"
            stroke-width="2" opacity="0.45" fill="none"/>
      <path d="M 843 300 H 890" stroke="#FFFFFF" stroke-width="8"/>
      <path d="M 849 296 H 862 V 304 H 849 Z M 875 296 H 888 V 304 H 875 Z"
            fill="#131C28"/>
    </svg>'''

    destination.write_text(svg, encoding='utf-8')
    return destination


def stadium_point(laps, center, scale, half_straight=225, radius=134.5):
    """Distance-linearized path along one lane of the SVG stadium."""
    h, r = half_straight * scale, radius * scale
    length = 4 * h + TAU * r
    s = (laps % 1.0) * length
    quarter = PI * r / 2

    if s < quarter:
        t = s / r
        xy = (h + r * np.cos(t), r * np.sin(t))
    elif s < quarter + 2 * h:
        xy = (h - (s - quarter), r)
    elif s < 3 * quarter + 2 * h:
        t = PI / 2 + (s - quarter - 2 * h) / r
        xy = (-h + r * np.cos(t), r * np.sin(t))
    elif s < 3 * quarter + 4 * h:
        xy = (-h + (s - 3 * quarter - 2 * h), -r)
    else:
        t = 3 * PI / 2 + (s - 3 * quarter - 4 * h) / r
        xy = (h + r * np.cos(t), r * np.sin(t))

    return center + np.array([xy[0], xy[1], 0.0])


class PhysicsTrailer40s(MovingCameraScene):
    def ar(self, message, size=34, color=WHITEISH):
        glyphs = MarkupText(
            escape(message),
            font=ARABIC_FONT,
            font_size=size,
            color=color,
        )
        if not glyphs.width or not glyphs.height:
            raise RuntimeError(f'Arabic glyphs are missing: {message!r}')
        return glyphs

    @staticmethod
    def fit(obj, width=11.8):
        if obj.width > width:
            obj.scale(width / obj.width)
        return obj

    def wipe(self, duration=0.4):
        contents = list(self.mobjects)
        if contents:
            self.play(
                *[FadeOut(obj) for obj in contents],
                run_time=duration,
            )
        else:
            self.wait(duration)

    def hook(self):
        # Section 1: 6.00 seconds
        eyebrow = Text(
            'THE PHYSICS SYMPHONY',
            font=ENGLISH_FONT,
            font_size=25,
            color=CYAN,
            weight=BOLD,
        ).to_edge(UP, buff=0.5)

        question = self.fit(
            self.ar('هل المسافة هي الإزاحة؟', 58, WHITEISH)
        )
        question.move_to(UP * 0.55)

        underline = Line(
            LEFT * 3.4,
            RIGHT * 3.4,
            stroke_color=GOLD,
            stroke_width=5,
        ).next_to(question, DOWN, buff=0.35)

        subtitle = Text(
            'DISTANCE  ≠  DISPLACEMENT',
            font=ENGLISH_FONT,
            font_size=35,
            color=CYAN,
            weight=BOLD,
        ).move_to(DOWN * 1.3)

        self.play(
            FadeIn(eyebrow, shift=UP * 0.2),
            run_time=0.7,
        )
        self.play(
            FadeIn(question, scale=0.87),
            run_time=1.2,
        )
        self.play(Create(underline), run_time=0.6)
        self.play(
            FadeIn(subtitle, shift=UP * 0.3),
            run_time=0.9,
        )
        self.play(
            Indicate(question, color=GOLD, scale_factor=1.025),
            run_time=1.0,
        )
        self.wait(1.2)
        self.wipe(0.4)

    def contrast(self):
        # Section 2: 9.00 seconds
        a = np.array([-4.4, -1.2, 0])
        b = np.array([3.15, -1.2, 0])

        heading = self.ar(
            ' ما هي الإزاحة؟ الطريق الذي تسلكه... أم مكان انتهائك؟',
            38,
        )
        self.fit(heading).to_edge(UP, buff=0.44)

        first = Dot(a, color=GREEN, radius=0.115)
        last = Dot(b, color=GREEN, radius=0.115)

        first_title = self.ar('البداية', 24, GREEN)
        first_title.next_to(first, DOWN, buff=0.28)

        last_title = self.ar('النهاية', 24, GREEN)
        last_title.next_to(last, DOWN, buff=0.28)

        route = ParametricFunction(
            lambda t: interpolate(a, b, t)
            + UP * (
                2.5
                * math.sin(PI * t)
                * (1 + .18 * math.sin(4 * PI * t))
            ),
            t_range=[0, 1],
            color=GOLD,
            stroke_width=8,
        ).set_fill(opacity=0)

        tracer = Dot(a, color=GOLD, radius=0.09)

        length = self.ar('المسافة', 32, GOLD)
        length.move_to([-2.0, 1.25, 0])

        arrow = Arrow(
            a + UP * .10,
            b + UP * .10,
            buff=0.14,
            color=CYAN,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.10,
        )

        vector_label = self.ar('الإزاحة', 32, CYAN)
        vector_label.move_to([0.0, -2.25, 0])

        self.play(
            FadeIn(heading),
            FadeIn(first),
            FadeIn(last),
            FadeIn(first_title),
            FadeIn(last_title),
            run_time=1.2,
        )

        self.add(tracer)

        self.play(
            Create(route),
            MoveAlongPath(tracer, route),
            run_time=3.0,
            rate_func=linear,
        )

        self.play(
            FadeIn(length, shift=UP * .2),
            run_time=.7,
        )

        self.play(
            route.animate.set_stroke(opacity=.33),
            GrowArrow(arrow),
            run_time=1.3,
        )

        self.play(
            FadeIn(vector_label),
            Indicate(arrow, color=CYAN),
            run_time=1.0,
        )

        self.wait(1.4)
        self.wipe(.4)

    def circuit(self):
        # Section 3: 11.00 seconds
        svg = track_svg()
        track = SVGMobject(str(svg))
        track.set_width(7.5)
        track.move_to([-2.65, -0.26, 0])

        center = track.get_center().copy()
        scale = track.width / 774

        progress = ValueTracker(0)

        def point(p):
            return stadium_point(p, center, scale)

        runner = Dot(
            point(0),
            radius=.13,
            color=GOLD,
        )

        runner.add_updater(
            lambda m: m.move_to(point(progress.get_value()))
        )

        finish = Dot(
            point(0),
            radius=.085,
            color=GREEN,
        )

        title = self.ar(
            'دورة كاملة... ثم خمس دورات',
            38,
        )
        self.fit(title).to_edge(UP, buff=.35)

        box = RoundedRectangle(
            width=4.35,
            height=4.7,
            corner_radius=.18,
            fill_color='#121D2B',
            fill_opacity=.98,
            stroke_color='#344256',
            stroke_width=2,
        )
        box.move_to([4.25, -.25, 0])

        lap_label = self.ar(
            'عدد الدورات',
            24,
            WHITEISH,
        ).move_to([4.5, 1.2, 0])

        lap_value = Integer(
            0,
            font_size=37,
            color=WHITEISH,
        ).move_to([2.9, 1.2, 0])

        lap_value.add_updater(
            lambda m: m.set_value(
                min(
                    5,
                    math.floor(progress.get_value() + 1e-5),
                )
            )
        )

        distance = self.ar(
            'المسافة',
            30,
            GOLD,
        ).move_to([4.82, .05, 0])

        length = Integer(
            0,
            font_size=38,
            color=GOLD,
        ).move_to([3.18, .05, 0])

        length.add_updater(
            lambda m: m.set_value(
                int(round(progress.get_value() * 400))
            )
        )

        displacement = self.ar(
            'الإزاحة',
            30,
            CYAN,
        ).move_to([4.77, -1.13, 0])

        zero = Text(
            '0 m',
            font=ENGLISH_FONT,
            font_size=36,
            color=CYAN,
        ).move_to([3.18, -1.13, 0])

        self.play(
            FadeIn(title),
            FadeIn(track),
            FadeIn(finish),
            FadeIn(box),
            run_time=1.3,
        )

        self.play(
            FadeIn(lap_label),
            FadeIn(distance),
            FadeIn(displacement),
            FadeIn(runner),
            run_time=.7,
        )

        self.add(lap_value, length)

        self.play(
            progress.animate.set_value(1),
            run_time=3.0,
            rate_func=linear,
        )

        self.play(
            FadeIn(zero),
            Indicate(finish, color=GREEN),
            run_time=.7,
        )

        self.play(
            progress.animate.set_value(5),
            run_time=3.7,
            rate_func=linear,
        )

        self.play(
            Indicate(length, color=GOLD),
            Indicate(zero, color=CYAN),
            run_time=.9,
        )

        self.wait(.3)

        runner.clear_updaters()
        lap_value.clear_updaters()
        length.clear_updaters()

        self.wipe(.4)

    def curved_space(self):
        # Section 4: 9.00 seconds
        heading = self.ar(
            'لكن... ماذا لو كان الفضاء منحنياً؟',
            38,
        )
        self.fit(heading).to_edge(UP, buff=.48)

        center = np.array([0, -.22, 0])
        depth = ValueTracker(0.0)

        def warp(x, y, amount):
            rr = (x / 3.4)**2 + (y / 2.15)**2
            factor = amount * math.exp(-1.9 * rr)

            return center + np.array([
                x * (1 - .16 * factor),
                y + .78 * factor * (1 - .16 * (x / 3.4)**2),
                0,
            ])

        lines = VGroup()

        for x in np.linspace(-5.0, 5.0, 15):
            stroke = VMobject(
                stroke_color=CYAN,
                stroke_width=1.5,
                fill_opacity=0,
            )
            stroke.base_axis = ('x', x)
            lines.add(stroke)

        for y in np.linspace(-2.1, 2.1, 9):
            stroke = VMobject(
                stroke_color=CYAN,
                stroke_width=1.5,
                fill_opacity=0,
            )
            stroke.base_axis = ('y', y)
            lines.add(stroke)

        def redraw(m):
            axis, value = m.base_axis

            if axis == 'x':
                pts = [
                    warp(value, t, depth.get_value())
                    for t in np.linspace(-2.1, 2.1, 55)
                ]
            else:
                pts = [
                    warp(t, value, depth.get_value())
                    for t in np.linspace(-5, 5, 75)
                ]

            m.set_points_as_corners(pts)
            m.set_fill(opacity=0)

        for line in lines:
            line.add_updater(redraw)
            redraw(line)

        question = self.ar(
            'هل تبقى أقصر مسافة بهذه البساطة؟',
            33,
            GOLD,
        )
        self.fit(question).to_edge(DOWN, buff=.5)

        frame = self.camera.frame
        frame.save_state()

        self.play(
            FadeIn(heading),
            FadeIn(lines),
            run_time=1.6,
        )

        self.play(
            depth.animate.set_value(1),
            frame.animate.scale(.92),
            run_time=3.1,
        )

        self.play(
            FadeIn(question, shift=UP * .12),
            run_time=1.0,
        )

        self.wait(2.5)

        self.play(
            Restore(frame),
            run_time=.4,
        )

        for line in lines:
            line.clear_updaters()

        self.wipe(.4)

    def end_card(self):
        # Section 5: 5.00 seconds
        signature = Text(
            'THE PHYSICS SYMPHONY',
            font=ENGLISH_FONT,
            font_size=26,
            color=CYAN,
            weight=BOLD,
        ).to_edge(UP, buff=.62)

        name = self.ar(
            'المسافة والإزاحة',
            53,
            GOLD,
        ).move_to(UP * .8)

        translation = Text(
            'DISTANCE vs DISPLACEMENT',
            font=ENGLISH_FONT,
            font_size=34,
            color=WHITEISH,
        ).move_to(DOWN * .14)

        line = Line(
            LEFT * 2.0,
            RIGHT * 2.0,
            color=CYAN,
            stroke_width=3,
        ).move_to(DOWN * .75)

        invitation = self.ar(
            'شاهد الحلقة كاملة',
            32,
            WHITEISH,
        ).move_to(DOWN * 1.55)

        self.play(
            FadeIn(signature),
            run_time=.6,
        )

        self.play(
            FadeIn(name, scale=.9),
            run_time=.9,
        )

        self.play(
            FadeIn(translation),
            Create(line),
            run_time=.9,
        )

        self.play(
            FadeIn(invitation, shift=UP * .2),
            run_time=.7,
        )

        self.wait(1.5)
        self.wipe(.4)

    def construct(self):
        self.camera.background_color = BG

        for filename in (
            'trailer_music.mp3',
            'trailer_music.wav',
        ):
            soundtrack = ROOT / filename

            if soundtrack.is_file():
                self.add_sound(str(soundtrack))
                print(
                    f'[TRAILER] Soundtrack: {soundtrack}',
                    flush=True,
                )
                break

        self.hook()
        self.contrast()
        self.circuit()
        self.curved_space()
        self.end_card()

        print(
            f'[TRAILER] Scene duration: {self.time:.2f}s',
            flush=True,
        )

if __name__ == "__main__":
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60
    config.output_file = "Trailer"
    config.preview = True
    config.quality = "high_quality"

    PhysicsTrailer40s().render()












"""
if __name__ == '__main__':
    source = Path(__file__).resolve()
    print(f'[TRAILER] Script: {source}', flush=True)

    with tempconfig({
        'pixel_width': 960 if FAST else 1920,
        'pixel_height': 540 if FAST else 1080,
        'frame_rate': 20 if FAST else 60,
        'media_dir': str(ROOT / 'trailer_media'),
        'output_file': (
            'Distance_Displacement_Trailer_40s_PREVIEW'
            if FAST else
            'Distance_Displacement_Trailer_40s'
        ),
        'preview': True,
        'disable_caching': True,
    }):
        scene = PhysicsTrailer40s()
        scene.render()

        print(
            f'[TRAILER] Movie: '
            f'{scene.renderer.file_writer.movie_file_path}',
            flush=True,
        )
"""