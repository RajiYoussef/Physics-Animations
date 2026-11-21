"""Shared Arabic typography and layout for all lesson scenes."""
from manim import RoundedRectangle
from settings import ARABIC_FONT, BACKGROUND, WHITE
from tools import arabic_label, fit_inside, frame_violations


def ar(text, size=29, color=WHITE, max_width=11.65):
    return arabic_label(text, size=size, color=color, font=ARABIC_FONT, max_width=max_width)


def caption_panel(text, center=(0, -3.2, 0)):
    panel = RoundedRectangle(width=12.4, height=.84, corner_radius=.16,
                             fill_color=BACKGROUND, fill_opacity=.94,
                             stroke_color="#294556", stroke_opacity=.7, stroke_width=1).move_to(center)
    label = ar(text).move_to(panel)
    fit_inside(label, 11.65, .65, padding=.02)
    if frame_violations([panel, label], margin=.1):
        raise ValueError("Arabic caption extends beyond the safe frame")
    return panel, label
