"""Scene 6: self-contained PyCharm script; SVG assets created automatically."""
from pathlib import Path
import math
import os
import numpy as np
from manim import *

BASE = Path(__file__).resolve().parent
ASSETS = BASE / 'scene06_assets'
BG = '#0D1117'
FG = '#E6EDF3'
AMBER = '#F2B84B'
BLUE = '#58A6FF'
GREEN = '#3FBF91'
FONT = 'Arial'
FAST = os.environ.get('SCENE06_FAST', '0') == '1'

TRACK_SVG = '<?xml version="1.0" encoding="utf-8" ?>\n<svg baseProfile="full" height="600px" version="1.1" viewBox="0 0 900 600" width="900px" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><rect fill="#0D1117" height="600" width="900" x="0" y="0" /><path d="M 849 300 A 209 209 0 0 0 640 91 H 260 A 209 209 0 0 0 51 300 A 209 209 0 0 0 260 509 H 640 A 209 209 0 0 0 849 300 Z" fill="#963A36" stroke="#DAA27A" stroke-width="3" /><path d="M 836 300 A 196 196 0 0 0 640 104 H 260 A 196 196 0 0 0 64 300 A 196 196 0 0 0 260 496 H 640 A 196 196 0 0 0 836 300 Z" fill="none" opacity="0.8" stroke="#F7D7B9" stroke-width="2.7" /><path d="M 820 300 A 180 180 0 0 0 640 120 H 260 A 180 180 0 0 0 80 300 A 180 180 0 0 0 260 480 H 640 A 180 180 0 0 0 820 300 Z" fill="none" opacity="0.8" stroke="#F7D7B9" stroke-width="2.7" /><path d="M 804 300 A 164 164 0 0 0 640 136 H 260 A 164 164 0 0 0 96 300 A 164 164 0 0 0 260 464 H 640 A 164 164 0 0 0 804 300 Z" fill="none" opacity="0.8" stroke="#F7D7B9" stroke-width="2.7" /><path d="M 788 300 A 148 148 0 0 0 640 152 H 260 A 148 148 0 0 0 112 300 A 148 148 0 0 0 260 448 H 640 A 148 148 0 0 0 788 300 Z" fill="none" opacity="0.8" stroke="#F7D7B9" stroke-width="2.7" /><path d="M 776 300 A 136 136 0 0 0 640 164 H 260 A 136 136 0 0 0 124 300 A 136 136 0 0 0 260 436 H 640 A 136 136 0 0 0 776 300 Z" fill="#245844" stroke="#F7D7B9" stroke-width="3" /><line opacity="0.45" stroke="#367159" stroke-width="4" x1="315" x2="585" y1="220" y2="220" /><line opacity="0.45" stroke="#367159" stroke-width="4" x1="315" x2="585" y1="265" y2="265" /><line opacity="0.45" stroke="#367159" stroke-width="4" x1="315" x2="585" y1="310" y2="310" /><line opacity="0.45" stroke="#367159" stroke-width="4" x1="315" x2="585" y1="355" y2="355" /><line opacity="0.5" stroke="#57927A" stroke-width="2" x1="450" x2="450" y1="173" y2="427" /><circle cx="450" cy="300" fill="none" opacity="0.5" r="42" stroke="#57927A" stroke-width="2" /><line stroke="#0B1520" stroke-width="11" x1="777" x2="858" y1="300" y2="300" /><line stroke="#FFFFFF" stroke-width="7" x1="777" x2="858" y1="300" y2="300" /><rect fill="#FFFFFF" height="8.4" width="13" x="777" y="295.8" /><rect fill="#151923" height="8.4" width="13" x="790" y="295.8" /><rect fill="#FFFFFF" height="8.4" width="13" x="803" y="295.8" /><rect fill="#151923" height="8.4" width="13" x="816" y="295.8" /><rect fill="#FFFFFF" height="8.4" width="13" x="829" y="295.8" /><rect fill="#151923" height="8.4" width="13" x="842" y="295.8" /></svg>'

RUNNER_SVG = '<?xml version="1.0" encoding="utf-8" ?>\n<svg baseProfile="full" height="185px" version="1.1" viewBox="0 0 140 185" width="140px" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><circle cx="78" cy="29" fill="#F4CBA3" r="17" stroke="#0A1422" stroke-width="3" /><path d="M 66 22 Q 70 6 90 16 L 99 26 L 81 23 Z" fill="#2C394D" /><path d="M 72 50 L 106 75 L 88 113 L 52 83 Z" fill="#FF6B4A" stroke="#182330" stroke-width="4" /><path d="M 75 63 L 40 73 L 28 48" fill="none" stroke="#F4CBA3" stroke-linecap="round" stroke-linejoin="round" stroke-width="11" /><path d="M 101 76 L 115 98 L 133 80" fill="none" stroke="#F4CBA3" stroke-linecap="round" stroke-linejoin="round" stroke-width="10" /><path d="M 73 108 L 100 135 L 123 155" fill="none" stroke="#D5E8FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="13" /><path d="M 66 108 L 41 139 L 16 133" fill="none" stroke="#D5E8FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="13" /><path d="M 121 153 L 136 157" fill="none" stroke="#F5B84B" stroke-linecap="round" stroke-width="11" /><path d="M 17 133 L 5 146" fill="none" stroke="#F5B84B" stroke-linecap="round" stroke-width="11" /></svg>'


def ensure_assets():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for filename, contents in (
        ('athletics_track.svg', TRACK_SVG),
        ('runner.svg', RUNNER_SVG),
    ):
        target = ASSETS / filename
        if not target.is_file() or target.stat().st_size == 0:
            target.write_text(contents, encoding='utf-8')
            print(f'[SCENE06] Created: {target.resolve()}', flush=True)


def track_point(progress, center, straight=1.60, radius=1.43):
    """One lap on the oval's middle lane; equal progress means equal distance."""
    perimeter = 4 * straight + 2 * math.pi * radius
    s = (progress % 1.0) * perimeter
    quarter = math.pi * radius / 2

    if s < quarter:
        angle = s / radius
        xy = (straight + radius * math.cos(angle), radius * math.sin(angle))
    elif s < quarter + 2 * straight:
        xy = (straight - (s - quarter), radius)
    elif s < 3 * quarter + 2 * straight:
        angle = math.pi / 2 + (s - quarter - 2 * straight) / radius
        xy = (-straight + radius * math.cos(angle), radius * math.sin(angle))
    elif s < 3 * quarter + 4 * straight:
        xy = (-straight + (s - 3 * quarter - 2 * straight), -radius)
    else:
        angle = 3 * math.pi / 2 + (s - 3 * quarter - 4 * straight) / radius
        xy = (straight + radius * math.cos(angle), radius * math.sin(angle))

    return center + np.array([xy[0], xy[1], 0])


class Scene06OvalRaceTrack(Scene):
    def arabic(self, value, size=29, color=FG):
        result = Text('\u200e' + value, font=FONT, font_size=size, color=color)
        if result.width <= 0 or result.height <= 0:
            raise RuntimeError(f'Arabic glyph rendering failed: {value}')
        return result

    def construct(self):
        self.camera.background_color = BG
        ensure_assets()

        heading = self.arabic('مثال: الجري على مضمار', 34).to_edge(UP, buff=0.25)

        track = SVGMobject(str(ASSETS / 'athletics_track.svg'))
        track.set_width(7.60).move_to([-2.78, -0.27, 0])

        center = np.array([-2.78, -0.27, 0.0])
        start = track_point(0, center)

        athlete = SVGMobject(str(ASSETS / 'runner.svg')).set_height(0.53)
        athlete.move_to(start + UP * 0.23)

        progress = ValueTracker(0.0)
        athlete.add_updater(
            lambda m: m.move_to(
                track_point(progress.get_value(), center) + UP * 0.23
            )
        )

        mark = Dot(start, radius=0.065, color=GREEN)
        start_name = self.arabic('البداية والنهاية', 22, GREEN)
        start_name.move_to([0.28, -1.55, 0])

        length_tag = self.arabic('طول المضمار', 23)
        length_tag.move_to([-3.5, 0.35, 0])

        length_num = Text('400 m', font=FONT, font_size=34, color=AMBER)
        length_num.next_to(length_tag, DOWN, buff=0.17)

        # Draw only the stroke. Never fill the enclosed area.
        highlight = VMobject(
            stroke_color=AMBER,
            stroke_width=5,
            fill_opacity=0,
        )
        highlight.set_fill(opacity=0)

        def draw_highlight(m):
            frac = min(1.0, max(0.0, progress.get_value()))

            if frac <= 0.001:
                m.set_opacity(0)
                return

            m.set_opacity(1)

            pts = [
                track_point(frac * j / 180, center)
                for j in range(181)
            ]

            m.set_points_as_corners(pts)

            # Critical: prevent the open route from being filled.
            m.set_fill(opacity=0)

        highlight.add_updater(draw_highlight)

        panel = RoundedRectangle(
            corner_radius=0.18,
            width=4.15,
            height=4.95,
            stroke_color='#334155',
            fill_color='#111827',
            fill_opacity=0.98,
            stroke_width=1.5,
        )
        panel.move_to([4.02, -0.33, 0])

        phase = self.arabic('دورة واحدة', 30)
        phase.move_to([4.02, 1.53, 0])

        lap_title = self.arabic('الدورات', 25)
        lap_title.move_to([4.77, 0.74, 0])

        lap_count = Integer(0, font_size=37, color=FG)
        lap_count.move_to([2.90, 0.74, 0])
        lap_count.add_updater(
            lambda m: m.set_value(
                min(5, int(progress.get_value() + 1e-5))
            )
        )

        distance_title = self.arabic('المسافة', 29, AMBER)
        distance_title.move_to([4.80, -0.25, 0])

        distance_value = Integer(0, font_size=37, color=AMBER)
        distance_value.move_to([3.18, -0.25, 0])
        distance_value.add_updater(
            lambda m: m.set_value(
                round(400 * progress.get_value())
            )
        )

        displacement_title = self.arabic('الإزاحة', 29, BLUE)
        displacement_title.move_to([4.8, -1.30, 0])

        displacement_value = Text('0 m', font=FONT, font_size=38, color=BLUE)
        displacement_value.move_to([3.10, -1.30, 0])

        explanation = self.arabic('نقطة النهاية = نقطة البداية', 19, GREEN)
        explanation.move_to([4.02, -2.08, 0])

        self.play(
            FadeIn(heading),
            FadeIn(track),
            run_time=1.3,
        )

        self.play(
            FadeIn(mark),
            FadeIn(start_name),
            FadeIn(length_tag),
            FadeIn(length_num),
            FadeIn(athlete),
            run_time=0.9,
        )

        self.play(
            FadeIn(panel),
            FadeIn(phase),
            FadeIn(lap_title),
            FadeIn(distance_title),
            FadeIn(displacement_title),
            run_time=1.0,
        )

        self.add(highlight, lap_count, distance_value)

        self.play(
            progress.animate.set_value(1),
            rate_func=linear,
            run_time=6.0 if FAST else 8.0,
        )

        self.play(
            FadeIn(displacement_value),
            FadeIn(explanation),
            Indicate(mark, color=GREEN),
            run_time=1.0,
        )
        self.wait(0.7)

        five = self.arabic('خمس دورات', 30).move_to(phase)

        self.play(
            ReplacementTransform(phase, five),
            FadeOut(displacement_value),
            FadeOut(explanation),
            run_time=0.7,
        )

        self.play(
            progress.animate.set_value(5),
            rate_func=linear,
            run_time=8.0 if FAST else 14.0,
        )

        self.play(
            FadeIn(displacement_value),
            FadeIn(explanation),
            Indicate(distance_value, color=AMBER),
            run_time=1.0,
        )

        self.wait(2.0)

        athlete.clear_updaters()
        highlight.clear_updaters()
        lap_count.clear_updaters()
        distance_value.clear_updaters()

        self.play(
            *[FadeOut(m) for m in list(self.mobjects)],
            run_time=1.0,
        )


if __name__ == '__main__':
    source = Path(__file__).resolve()
    print(f'[SCENE06] Script: {source}', flush=True)

    with tempconfig({
        'pixel_width': 960 if FAST else 1920,
        'pixel_height': 540 if FAST else 1080,
        'frame_rate': 20 if FAST else 60,
        'media_dir': str(BASE / 'scene06_media'),
        'output_file': 'scene06_SVG_preview' if FAST else 'scene06_SVG_final',
        'preview': True,
    }):
        scene = Scene06OvalRaceTrack()
        scene.render()

        print(
            f'[SCENE06] Video: {scene.renderer.file_writer.movie_file_path}',
            flush=True,
        )