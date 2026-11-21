"""Reference card (~5 s): the textbook chapter this lesson draws on.

Render: Run button in PyCharm (uses settings.render), or
        manim -qh scene_00b_reference.py ReferenceCard
"""
from __future__ import annotations

import numpy as np
from manim import *  # noqa: F401,F403

from settings import CYAN, GOLD, WHITE
from support import ar
from intro_fx import (DEEP, ICE, METAL, ambient_dust, drive, expelled_field_lines, glow_text, heading,
                      install_clock, live_breathe, now, rtl_reveal, tk)

# ---- edit these to match your copy of the book ------------------------------
BOOK_TITLE = ("Elementary Electromagnetism", "Using Python")
AUTHOR = "Anders Malthe-Sørenssen"
AFFILIATION = "University of Oslo"
CHAPTER_NUMBER = 7
CHAPTER_TITLE_EN = "Conductors"
CHAPTER_TITLE_AR = "الموصلات"
SERIF = "Times New Roman"   # Latin text of the book title (kept in its original language)
# -----------------------------------------------------------------------------

NAVY = "#0b1f33"
PAPER = "#e9e4d8"
INK = "#1b2733"


def latin(text, size=24, color=WHITE, slant=NORMAL, weight=NORMAL):
    return Text(text, font=SERIF, font_size=size, color=color, slant=slant, weight=weight)


class ReferenceCard(MovingCameraScene):
    def construct(self):
        install_clock(self)
        self.add(ambient_dust(count=50))

        # ---------------------------------------------------------- the book
        W, H = 2.7, 3.7
        spine_x, cy = -3.55, -0.2
        thickness = VGroup(*[Rectangle(width=W, height=H, stroke_color="#b9b2a2", stroke_width=0.8,
                                       fill_color=PAPER, fill_opacity=1)
                             .move_to([spine_x + W / 2 + 0.035 * k, cy - 0.035 * k, 0]) for k in range(4, 0, -1)])
        page = Rectangle(width=W, height=H, stroke_color="#b9b2a2", stroke_width=1, fill_color=PAPER,
                         fill_opacity=1).move_to([spine_x + W / 2, cy, 0])
        # chapter page: number, English title, a small conductor-in-a-field figure
        ch_word = latin("Chapter", 22, INK, slant=ITALIC)
        ch_num = latin(str(CHAPTER_NUMBER), 64, INK, weight=BOLD)
        ch_title = latin(CHAPTER_TITLE_EN, 26, INK, weight=BOLD)
        ch_head = VGroup(ch_word, ch_num, ch_title).arrange(DOWN, buff=0.12).move_to(page.get_top() + DOWN * 1.05)
        fig_c, R = page.get_center() + DOWN * 0.95, 0.42
        _, after = expelled_field_lines(R, np.linspace(-0.62, 0.62, 7), x_start=-1.15, n=40)
        lines = VGroup()
        for pts in after:
            for side in (1, -1):
                q = pts.copy()
                q[:, 0] *= side
                if side < 0:
                    q = q[::-1]
                lines.add(VMobject(stroke_color="#8a6a2a", stroke_width=1.4).set_points_as_corners(q + fig_c))
        disk = Circle(radius=R, stroke_color=INK, stroke_width=1.6, fill_color="#c9d6dd", fill_opacity=1).move_to(fig_c)
        flow = VGroup(*[Dot(radius=0.028, color="#b0482c") for _ in lines])
        flow.add_updater(lambda g: [d.move_to(l.point_from_proportion((0.45 * now() + 0.37 * k) % 1.0))
                                    for k, (d, l) in enumerate(zip(g, lines))])
        page_content = VGroup(ch_head, lines, disk, flow)

        cover = Rectangle(width=W, height=H, stroke_color=GOLD, stroke_width=2, fill_color=NAVY,
                          fill_opacity=1).move_to(page)
        frame_line = Rectangle(width=W - 0.3, height=H - 0.3, stroke_color=GOLD, stroke_width=1, stroke_opacity=0.6
                               ).move_to(cover)
        c_title = VGroup(*[latin(t, 21, WHITE, weight=BOLD) for t in BOOK_TITLE]).arrange(DOWN, buff=0.08)
        c_title.set(width=min(c_title.width, W - 0.55)).move_to(cover.get_top() + DOWN * 0.95)
        c_rule = Line(LEFT * 0.9, RIGHT * 0.9, stroke_color=GOLD, stroke_width=1.5).next_to(c_title, DOWN, buff=0.25)
        c_author = latin(AUTHOR, 15, ICE).next_to(c_rule, DOWN, buff=0.3)
        c_author.set(width=min(c_author.width, W - 0.5))
        cover_text = VGroup(frame_line, c_title, c_rule, c_author)
        spine = Rectangle(width=0.12, height=H, stroke_width=0, fill_color="#06121e", fill_opacity=1
                          ).move_to([spine_x - 0.06, cy, 0])
        book = VGroup(thickness, page, page_content, cover, cover_text, spine)
        book_glow = RoundedRectangle(width=W + 0.5, height=H + 0.5, corner_radius=0.2, stroke_color=CYAN,
                                     stroke_width=10, stroke_opacity=0.08, fill_opacity=0).move_to(page)
        live_breathe(book_glow, 0.03, 0.14, freq=0.6, fill=False)

        # ------------------------------------------------- Arabic text column
        top = heading("المرجع", 40, GOLD, y=3.25, accent=GOLD)
        x_col = 3.15
        book_name = VGroup(*[latin(t, 30, WHITE, slant=ITALIC) for t in BOOK_TITLE]).arrange(DOWN, buff=0.1)
        book_name.move_to([x_col, 1.55, 0])
        author = latin(AUTHOR, 24, ICE).move_to([x_col, 0.55, 0])
        uni = latin(AFFILIATION, 20, METAL).move_to([x_col, 0.1, 0])
        chapter = ar(f"الفصل {CHAPTER_NUMBER}: {CHAPTER_TITLE_AR}", 36, CYAN).move_to([x_col, -0.95, 0])
        chapter_halo = glow_text(chapter, CYAN, layers=3, opacity=0.18)
        rule = Line([x_col - 2.6, -0.42, 0], [x_col + 2.6, -0.42, 0], stroke_color=GOLD, stroke_width=1.2,
                    stroke_opacity=0.7)

        # ---------------------------------------------------------- timeline (5 s)
        self.add(thickness, page, cover, cover_text, spine)
        closed = VGroup(thickness, page, cover, cover_text, spine)
        closed.shift(DOWN * 0.4).set_opacity(0)
        self.play(closed.animate.shift(UP * 0.4).set_opacity(1), FadeIn(book_glow), FadeIn(top[0], shift=DOWN * 0.1),
                  Create(top[1]), run_time=0.7)
        # the cover swings open about the spine; the chapter page appears underneath
        self.play(FadeOut(cover_text, run_time=0.25), FadeIn(page_content, run_time=0.9),
                  cover.animate.stretch(-1, 0, about_point=[spine_x, cy, 0]).set_fill("#10283f"),
                  self.camera.frame.animate.scale(0.97).shift(LEFT * 0.1),
                  FadeIn(book_name, shift=LEFT * 0.15), FadeIn(author, shift=LEFT * 0.15),
                  FadeIn(uni, shift=LEFT * 0.15), run_time=0.9, rate_func=rate_functions.ease_in_out_sine)
        ribbon = Polygon([0, 0, 0], [0.26, 0, 0], [0.26, -0.75, 0], [0.13, -0.6, 0], [0, -0.75, 0],
                         stroke_width=0, fill_color="#c0392b", fill_opacity=1)
        ribbon.move_to(page.get_corner(UR) + LEFT * 0.45 + DOWN * 0.3)
        self.play(Create(rule), rtl_reveal(chapter, run_time=0.7), GrowFromEdge(ribbon, UP), run_time=0.7)
        self.add(chapter_halo)
        self.play(Indicate(ch_num, color="#b0482c", scale_factor=1.15), Circumscribe(disk, Circle, color=GOLD,
                                                                                       fade_out=True), run_time=0.8)
        self.wait(1.1)
        stage = VGroup(book, ribbon, book_glow, top, book_name, author, uni, rule, chapter, chapter_halo)
        for m in stage.get_family():
            m.clear_updaters()
        self.play(FadeOut(stage, shift=UP * 0.15), Restore(self.camera.frame) if hasattr(self.camera.frame, "saved_state")
                  else Wait(0), run_time=0.8)


if __name__ == "__main__":
    from settings import render

    render(ReferenceCard, "scene_00b_reference")
