"""Scene 6 — oval athletics track. Run directly with PyCharm's Run button.
Only ManimCE and NumPy are required. SVG artwork is generated automatically.
Set SCENE06_FAST=1 in PyCharm environment variables for a quick render.
"""
from pathlib import Path
import math
import os
import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'scene06_assets'
BG, FG, AMBER, BLUE, GREEN = '#0D1117', '#E6EDF3', '#F2B84B', '#58A6FF', '#3FBF91'
FONT = 'Arial'  # Windows font; replace with DejaVu Sans if preferred.
FAST = os.getenv('SCENE06_FAST') == '1'


def stadium(r):
    """Closed stadium SVG path, centered at (450,300), straight half-length 190."""
    return (f'M {640+r} 300 A {r} {r} 0 0 0 640 {300-r} '
            f'H 260 A {r} {r} 0 0 0 {260-r} 300 '
            f'A {r} {r} 0 0 0 260 {300+r} H 640 '
            f'A {r} {r} 0 0 0 {640+r} 300 Z')


def make_assets():
    """Overwrite generated assets, so previous scene versions cannot leave stale SVGs."""
    ASSETS.mkdir(exist_ok=True)
    lanes = '\n'.join(
        f'<path d="{stadium(r)}" fill="none" stroke="#F4D7C0" '
        f'stroke-width="2.3" opacity="0.90"/>'
        for r in (194, 179, 164, 149)
    )
    squares = '\n'.join(
        f'<rect x="{776+i*12}" y="296" width="12" height="8" '
        f'fill="{("#F8FAFC" if i % 2 == 0 else "#172033")}"/>'
        for i in range(6)
    )
    track = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
      <path d="{stadium(209)}" fill="#B45347" stroke="#E5A98D" stroke-width="3"/>
      {lanes}
      <path d="{stadium(134)}" fill="#285C4B" stroke="#E9CCAE" stroke-width="3"/>
      <path d="M325 300 H575 M450 175 V425" stroke="#6BA48C" stroke-width="2" opacity="0.5"/>
      <circle cx="450" cy="300" r="45" stroke="#6BA48C" stroke-width="2" fill="none" opacity="0.5"/>
      <path d="M 776 300 H 849" stroke="#F8FAFC" stroke-width="7"/>
      {squares}
    </svg>'''
    runner = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 185">
      <circle cx="78" cy="29" r="17" fill="#F4CBA3" stroke="#182330" stroke-width="3"/>
      <path d="M66 22 Q70 6 90 16 L99 26 81 23 Z" fill="#29364B"/>
      <path d="M72 50 L106 75 88 113 52 83 Z" fill="#FF7655" stroke="#182330" stroke-width="4"/>
      <path d="M75 63 L40 73 28 48 M101 76 L115 98 133 80" fill="none" stroke="#F4CBA3" stroke-width="10" stroke-linecap="round"/>
      <path d="M73 108 L100 135 123 155 M66 108 L41 139 16 133" fill="none" stroke="#D5E8FF" stroke-width="13" stroke-linecap="round"/>
      <path d="M121 153 L136 157 M17 133 L5 146" fill="none" stroke="#F2B84B" stroke-width="10" stroke-linecap="round"/>
    </svg>'''
    (ASSETS / 'track.svg').write_text(track, encoding='utf-8')
    (ASSETS / 'runner.svg').write_text(runner, encoding='utf-8')


def lap_point(laps, center, scale):
    """Exact distance-parameterized stadium, aligned to the SVG middle lane."""
    h, r = 190 * scale, 171.5 * scale
    distance = (laps % 1.0) * (4*h + 2*math.pi*r)
    q = math.pi*r/2
    if distance < q:
        t = distance/r
        x, y = h+r*math.cos(t), r*math.sin(t)
    elif distance < q+2*h:
        x, y = h-(distance-q), r
    elif distance < 3*q+2*h:
        t = math.pi/2 + (distance-q-2*h)/r
        x, y = -h+r*math.cos(t), r*math.sin(t)
    elif distance < 3*q+4*h:
        x, y = -h+(distance-3*q-2*h), -r
    else:
        t = 3*math.pi/2+(distance-3*q-4*h)/r
        x, y = h+r*math.cos(t), r*math.sin(t)
    return center + np.array([x, y, 0])


class Scene06(MovingCameraScene):
    def arabic(self, s, size=28, color=FG):
        obj = Text('\u200e'+s, font=FONT, font_size=size, color=color)
        if not obj.width or not obj.height:
            raise RuntimeError(f'Arabic text has no geometry: {s!r}')
        return obj

    def construct(self):
        self.camera.background_color = BG
        make_assets()
        track = SVGMobject(str(ASSETS / 'track.svg')).set_width(7.5)
        track.move_to([-3.06, -0.33, 0])
        center = track.get_center().copy()
        # SVG visible outside bounds ≈798px, including a small stroke margin.
        scale = track.width / 802
        at = lambda p: lap_point(p, center, scale)
        start = at(0)
        marker = Dot(start, radius=0.085, color=GREEN)
        ring = Circle(radius=0.18, color=GREEN, stroke_width=3).move_to(start)
        runner = SVGMobject(str(ASSETS / 'runner.svg')).set_height(0.55)
        progress = ValueTracker(0)
        runner.add_updater(lambda m: m.move_to(at(progress.get_value()) + UP*0.24))

        # Stroke-only route: no area fill, even on a partially completed lap.
        trail = VMobject(stroke_color=AMBER, stroke_width=5, fill_opacity=0)
        def update_trail(m):
            p = progress.get_value()
            fraction = p - math.floor(p)
            if p > 0 and abs(fraction) < 1e-6:
                fraction = 1.0
            if fraction < 0.002:
                m.set_stroke(opacity=0)
                return
            samples = max(3, int(110*fraction))
            m.set_points_as_corners([at(fraction*i/samples) for i in range(samples+1)])
            m.set_fill(opacity=0)
            m.set_stroke(color=AMBER, width=5, opacity=1)
        trail.add_updater(update_trail)

        heading = self.arabic('مثال آخر: الجري على مضمار', 34).to_edge(UP, buff=0.28)
        start_label = self.arabic('البداية والنهاية', 21, GREEN)
        start_label.next_to(marker, UP+RIGHT, buff=0.23)
        lap_length = VGroup(self.arabic('طول المضمار', 24), Text('400 m', font=FONT,
                            font_size=32, color=AMBER)).arrange(DOWN, buff=0.10)
        lap_length.move_to(center + UP*0.18)

        panel = RoundedRectangle(corner_radius=0.19, width=4.25, height=4.85,
                                 stroke_color='#475569', stroke_width=1.4,
                                 fill_color='#121C2A', fill_opacity=0.98)
        panel.move_to([4.27, -0.37, 0])
        phase = self.arabic('دورة واحدة', 30).move_to([4.27, 1.55, 0])
        laps_title = self.arabic('عدد الدورات', 25).move_to([4.95, 0.77, 0])
        laps_num = Integer(0, font_size=34, color=FG).move_to([3.08, 0.77, 0])
        laps_num.add_updater(lambda m: m.set_value(min(5, int(progress.get_value()+1e-5))))
        distance_title = self.arabic('المسافة', 29, AMBER).move_to([4.95, -0.16, 0])
        distance_num = Integer(0, font_size=35, color=AMBER).move_to([3.12, -0.16, 0])
        distance_num.add_updater(lambda m: m.set_value(round(400*progress.get_value())))
        disp_title = self.arabic('الإزاحة', 29, BLUE).move_to([4.95, -1.12, 0])
        disp_num = Text('0 m', font=FONT, font_size=36, color=BLUE).move_to([3.16, -1.12, 0])
        explanation = self.arabic('النهاية هي نقطة البداية', 21, GREEN).move_to([4.27, -2.10, 0])

        # A small opening camera reveal, followed by an unmoving teaching layout.
        camera_frame = self.camera.frame
        camera_frame.save_state()
        camera_frame.set(width=10.8).move_to([-2.7, -0.3, 0])
        self.play(FadeIn(track), FadeIn(marker), Create(ring), run_time=1.1)
        self.play(Restore(camera_frame), FadeIn(heading), FadeIn(panel),
                  FadeIn(phase), FadeIn(laps_title), FadeIn(distance_title),
                  FadeIn(disp_title), run_time=1.4)
        self.play(FadeIn(start_label), FadeIn(lap_length), FadeIn(runner), run_time=0.9)
        self.add(trail, laps_num, distance_num)
        self.play(progress.animate.set_value(1), run_time=7 if not FAST else 3.5, rate_func=linear)
        self.play(FadeIn(disp_num), FadeIn(explanation), Indicate(ring, color=GREEN), run_time=1)
        self.wait(1.0)
        second = self.arabic('خمس دورات', 30).move_to(phase)
        self.play(ReplacementTransform(phase, second), FadeOut(disp_num),
                  FadeOut(explanation), run_time=0.75)
        self.play(progress.animate.set_value(5), run_time=13 if not FAST else 5, rate_func=linear)
        self.play(FadeIn(disp_num), FadeIn(explanation), Indicate(distance_num, color=AMBER),
                  Indicate(ring, color=GREEN), run_time=1)
        self.wait(2)
        runner.clear_updaters()
        trail.clear_updaters()
        laps_num.clear_updaters()
        distance_num.clear_updaters()
        self.play(*[FadeOut(obj) for obj in list(self.mobjects) if obj is not camera_frame], run_time=0.9)

if __name__ == "__main__":
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60
    config.output_file = "scene_06"
    config.preview = True
    config.quality = "high_quality"

    Scene06().render()



















""" 

if __name__ == '__main__':
    print(f'[SCENE06] Running: {Path(__file__).resolve()}', flush=True)
    with tempconfig({
        'pixel_width': 960 if FAST else 1920,
        'pixel_height': 540 if FAST else 1080,
        'frame_rate': 20 if FAST else 60,
        'media_dir': str(ROOT / 'scene06_media'),
        'output_file': 'scene06_REBUILT_PREVIEW' if FAST else 'scene06_REBUILT_FINAL',
        'preview': True,
    }):
        scene = Scene06()
        scene.render()
        print(f'[SCENE06] Video: {scene.renderer.file_writer.movie_file_path}', flush=True)
"""