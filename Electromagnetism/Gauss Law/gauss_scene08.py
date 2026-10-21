"""S08 — A repeatable method. Run directly in PyCharm.

Optional narration beside this file:
    S08_ar.wav (whole scene), OR all of:
    S08_B01_ar.wav, S08_B02_ar.wav, S08_B03_ar.wav

An unsegmented recording starts at t=1s. Its paragraph transition times
must match the planned 16s and 36s cues for precise synchronization.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import contextlib
import subprocess
import sys
import wave
import numpy as np
from manim import *

DARK = '#101820'
WHITEISH = '#F5F5F5'
GOLD = '#F6C85F'
CYAN = '#58C4DD'
VIOLET = '#C792EA'
RED = '#FF6B6B'
BLUE = '#64B5F6'
ARABIC_FONT = 'Arial'  # Change only if this font lacks Arabic glyphs on your machine.
FADE_LAST_HALF_SECOND = True


def wav_seconds(path: Path) -> float:
    if not path.is_file():
        return 0.0
    try:
        with contextlib.closing(wave.open(str(path), 'rb')) as f:
            return f.getnframes() / f.getframerate()
    except (OSError, wave.Error, ZeroDivisionError):
        return 0.0


class GaussScene08(Scene):
    def ar(self, value: str, size=27, color=WHITEISH):
        # Pango-backed Arabic shaping: reliable alternative to Text for this setup.
        return MarkupText(escape(value), font=ARABIC_FONT,
                          font_size=size, color=color)

    def fit(self, mob, max_width):
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        return mob

    def construct(self):
        self.camera.background_color = DARK
        self.elapsed = 0.0
        directory = Path(__file__).resolve().parent
        planned = [(12., 3.), (17., 3.), (15., 4.)]
        self.lengths = [sum(x) for x in planned]  # 15+20+19, plus 1s setup = 55s
        whole = directory / 'S08_ar.wav'
        clips = [directory / f'S08_B0{i}_ar.wav' for i in (1, 2, 3)]
        self.mode = 'silent'
        if whole.is_file():
            self.mode = 'whole'
            self.whole_path = whole
            # The last speech window ends at 51s; retain the 4s final hold.
            self.lengths[-1] += max(0., wav_seconds(whole) - 50.)
            print('S08: whole-file paragraph cues assume t=16s and t=36s.')
        elif all(p.is_file() for p in clips):
            self.mode = 'beats'
            self.clips = clips
            self.lengths = [max(s, wav_seconds(p)) + h
                            for p, (s, h) in zip(clips, planned)]
        else:
            print('S08: audio unavailable; rendering silent preview.')
        self.expected = 1.0 + sum(self.lengths)
        print(f'S08 scene length: {self.expected:.3f}s')

        self.make_layout()
        self.play_for(FadeIn(self.title, shift=DOWN * .1), .8)
        self.pause(.2)
        if self.mode == 'whole':
            self.add_sound(str(self.whole_path))
        self.beat1()
        self.beat2()
        self.beat3()
        assert abs(self.elapsed - self.expected) < .06, (self.elapsed, self.expected)

    def make_layout(self):
        self.title = self.ar('طريقة يمكن استخدامها بشكل متكرر', 42).move_to([0, 3.23, 0])

        # Cards stay inside the left half; only the active card is bright.
        self.cards = VGroup()
        self.card_texts = []
        self.card_icons = []
        self.revealed_cards = set()
        labels = [
            'استخدم التناظر',
            'اختر سطحًا مغلقًا',
            'احسب التدفق\nوالشحنة المحصورة',
            'طبّق قانون غاوس ثم حل',
        ]
        self.card_centers_y = [1.97, .67, -.63, -1.93]
        for i, (label, y) in enumerate(zip(labels, self.card_centers_y)):
            panel = RoundedRectangle(corner_radius=.14, width=5.85, height=1.03,
                                      stroke_color=CYAN, stroke_width=1.8,
                                      fill_color='#182932', fill_opacity=.65)
            panel.move_to([-3.39, y, 0])
            number = MathTex(str(i+1), font_size=28, color=GOLD).move_to([-.94, y, 0])
            text_label = self.fit(self.ar(label, 27), 4.35)
            text_label.move_to([-3.6, y, 0])
            text_label.align_to(np.array([-1.48, y, 0.]), RIGHT)
            card = VGroup(panel, number, text_label)
            # Keep text readable; activation changes each component separately.
            self.cards.add(card)
            self.card_texts.append(text_label)
            self.card_icons.append(number)

        # Large geometry examples occupy the right panel only during beat 1.
        self.sphere_icon = VGroup(
            Circle(radius=.67, color=CYAN, stroke_width=3),
            Ellipse(width=1.34, height=.38, color=CYAN, stroke_width=2),
        ).move_to([1.75, .80, 0])
        self.cylinder_icon = self.cylinder_geometry(
            center=[4.6, .80, 0], rx=.62, ry=.20, h=1.25)
        self.sphere_caption = self.ar('سطح كروي', 25).move_to([1.75, -.40, 0])
        self.cylinder_caption = self.ar('سطح أسطواني مغلق', 25).move_to([4.6, -.40, 0])
        self.sphere_example = VGroup(self.sphere_icon, self.sphere_caption)
        self.cylinder_example = VGroup(self.cylinder_icon, self.cylinder_caption)

        self.eq_parts = MathTex(
            r'\Phi_E=', r'\sum_j', r'\int_{S_j}',
            r'\mathbf E\cdot\hat{\mathbf n}', r'\,dS',
            font_size=34, color=WHITEISH,
        ).move_to([3.25, 1.85, 0])
        self.fit(self.eq_parts, 5.60)
        self.eq_final = MathTex(
            r'\Phi_E=\frac{Q_{\mathrm{in}}}{\epsilon_0}',
            font_size=42, color=WHITEISH,
        ).move_to([3.17, -.05, 0])

        # Schematic cylinder: curved side + both caps; no two-dimensional loop integral.
        self.cyl_center = np.array([3.17, -.84, 0.])
        cx, cy = self.cyl_center[:2]
        rx, ry, h = .96, .25, 1.25
        top_y, bot_y = cy + h/2, cy - h/2
        # A curved projected side, without the rectangle's false horizontal edges.
        self.side = VMobject(stroke_color=CYAN, stroke_width=2,
                             fill_color=CYAN, fill_opacity=.12)
        self.side.start_new_path(np.array([cx-rx, top_y, 0]))
        self.side.add_line_to(np.array([cx-rx, bot_y, 0]))
        self.side.add_cubic_bezier_curve_to(
            np.array([cx-rx, bot_y-4*ry/3, 0]),
            np.array([cx+rx, bot_y-4*ry/3, 0]),
            np.array([cx+rx, bot_y, 0]))
        self.side.add_line_to(np.array([cx+rx, top_y, 0]))
        self.side.add_cubic_bezier_curve_to(
            np.array([cx+rx, top_y-4*ry/3, 0]),
            np.array([cx-rx, top_y-4*ry/3, 0]),
            np.array([cx-rx, top_y, 0]))
        self.side.close_path()
        self.top_cap = Ellipse(width=2*rx, height=2*ry, color=VIOLET,
                               stroke_width=2.6, fill_color=VIOLET, fill_opacity=.16).move_to([cx,top_y,0])
        self.bottom_cap = Ellipse(width=2*rx, height=2*ry, color=VIOLET,
                                  stroke_width=2.6, fill_color=VIOLET, fill_opacity=.16).move_to([cx,bot_y,0])
        self.cylinder = VGroup(self.side, self.bottom_cap, self.top_cap)
        self.side_name = self.fit(self.ar('السطح الجانبي المنحني', 23, CYAN), 4.8)
        self.side_name.move_to([3.17, -2.09, 0])
        self.caps_name = self.ar('القاعدتان', 23, VIOLET).move_to([3.17, -2.52, 0])

        # Closing reminder remains within top/bottom safe frame.
        self.symmetry_reminder = self.ar('استخدم التناظر', 27, GOLD).move_to([3.16, .82, 0])

        self.check_layout()

    def cylinder_geometry(self, center, rx, ry, h):
        x, y, _ = center
        return VGroup(
            Line([x-rx, y+h/2, 0], [x-rx, y-h/2, 0], color=CYAN, stroke_width=2),
            Line([x+rx, y+h/2, 0], [x+rx, y-h/2, 0], color=CYAN, stroke_width=2),
            Ellipse(width=2*rx, height=2*ry, color=CYAN, stroke_width=2).move_to([x,y+h/2,0]),
            Ellipse(width=2*rx, height=2*ry, color=CYAN, stroke_width=2).move_to([x,y-h/2,0]),
        )

    def check_layout(self):
        # Detect off-screen prose in code, before expensive rendering.
        for item in [self.title, *self.card_texts, self.side_name, self.sphere_caption, self.cylinder_caption,
                     self.caps_name, self.symmetry_reminder, self.eq_parts, self.eq_final]:
            if (item.get_left()[0] < -6.70 or item.get_right()[0] > 6.70 or
                item.get_top()[1] > 3.70 or item.get_bottom()[1] < -2.90):
                raise ValueError(f'Object outside safe screen area: {item}')

    def beat_start(self, index):
        if self.mode == 'beats':
            self.add_sound(str(self.clips[index]))
        self.beat_end = self.elapsed + self.lengths[index]

    def play_for(self, animation, seconds):
        self.play(animation, run_time=seconds)
        self.elapsed += seconds

    def pause(self, seconds):
        if seconds > 1.e-5:
            self.wait(seconds)
            self.elapsed += seconds

    def finish_beat(self, final=False):
        left = self.beat_end - self.elapsed
        if left < -.05:
            raise RuntimeError(f'S08 beat exceeded schedule by {-left:.2f}s')
        if final and FADE_LAST_HALF_SECOND and left >= .5:
            self.pause(left-.5)
            self.play_for(FadeOut(Group(*list(self.mobjects))), .5)
        else:
            self.pause(max(0., left))

    def reveal_card(self, i, duration=.6):
        self.revealed_cards.add(i)
        self.play_for(FadeIn(self.cards[i]), duration)

    def activate(self, i, duration=.6):
        # Never animate unrevealed cards: Manim would add them to the scene.
        anims = []
        for j in sorted(self.revealed_cards):
            panel, number, text = self.cards[j]
            active = j == i
            anims.extend([
                panel.animate.set_stroke(GOLD if active else CYAN,
                                        width=2.5 if active else 1.4,
                                        opacity=1 if active else .55)
                             .set_fill('#223943' if active else '#182932', opacity=.8),
                number.animate.set_opacity(1 if active else .7),
                text.animate.set_opacity(1 if active else .72),
            ])
        self.play_for(AnimationGroup(*anims, lag_ratio=0), duration)

    def beat1(self):
        self.beat_start(0)
        self.reveal_card(0, .7)
        self.activate(0, .6)
        self.play_for(FadeIn(self.sphere_example), .8)
        self.play_for(Indicate(self.sphere_icon, color=CYAN), 1.1)
        self.reveal_card(1, .7)
        self.activate(1, .6)
        self.play_for(FadeIn(self.cylinder_example), .8)
        self.play_for(Indicate(self.cylinder_icon, color=CYAN), .9)
        self.finish_beat()

    def beat2(self):
        self.beat_start(1)
        self.play_for(FadeOut(self.sphere_example, self.cylinder_example), .5)
        self.reveal_card(2, .6)
        self.activate(2, .55)
        self.play_for(FadeIn(self.cylinder), 1.1)
        self.play_for(Indicate(self.side, color=CYAN, scale_factor=1.035), 1.1)
        self.play_for(FadeIn(self.side_name), .6)
        self.play_for(Indicate(VGroup(self.top_cap, self.bottom_cap), color=VIOLET), 1.1)
        self.play_for(FadeIn(self.caps_name), .6)
        # Build the surface decomposition from the equation's actual terms.
        for term, duration in zip(self.eq_parts, [.5, .6, .65, .8, .5]):
            self.play_for(Write(term), duration)
        self.play_for(Indicate(self.eq_parts[2], color=CYAN), .9)
        self.finish_beat()

    def beat3(self):
        self.beat_start(2)
        self.reveal_card(3, .6)
        self.activate(3, .6)
        self.play_for(FadeOut(self.cylinder, self.side_name, self.caps_name), .8)
        self.play_for(self.eq_parts.animate.set_opacity(.55), .55)
        self.play_for(Write(self.eq_final), 1.6)
        self.play_for(Circumscribe(self.eq_final, color=GOLD), 1.1)
        self.activate(0, .7)
        self.play_for(FadeIn(self.symmetry_reminder), .65)
        self.play_for(Indicate(self.cards[0], color=CYAN), .85)
        self.finish_beat(final=True)


# =============================================================
# PYCHARM: CLICK RUN — RENDER AND OPEN THE VIDEO AUTOMATICALLY
# =============================================================
if __name__ == '__main__':
    subprocess.run([
        sys.executable, '-m', 'manim', '-p', '-qh',
        '-r', '1920,1080', '--fps', '30',
        str(Path(__file__).resolve()), 'GaussScene08',
    ], check=True)
