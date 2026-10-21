"""Independent, editable two-page Manim closing credits.

Page 1: source credit shown for exactly 3 seconds.
Page 2: greeting and subscribe message with a typing-style reveal.

Run this file directly in PyCharm to render and open the video.
The Arabic letters are laid out FIRST with MarkupText and revealed from the
finished glyphs; this preserves contextual Arabic shaping.
"""

from html import escape
from pathlib import Path
import subprocess
import sys

from manim import *

# ---------------------------- EASY TO EDIT ----------------------------
BACKGROUND = "#101820"
WHITEISH = "#F5F5F5"
GOLD = "#F6C85F"
CYAN = "#58C4DD"
ARABIC_FONT = "Arial"
ENGLISH_FONT = "DejaVu Sans"

SOURCE_PAGE_SECONDS = 3.0  # Requested: 2–3 seconds
GREETING_PAGE_SECONDS = 11.0
FADE_SECONDS = 0.35

AR_SOURCE = "المصدر: الفصل الثالث من كتاب الكهرومغناطيسية الأولية باستخدام بايثون،"
AR_AUTHOR = "Anders Malthe-Sørenssen، 2022."
EN_TITLE = "Elementary Electromagnetism"
EN_SUBTITLE = "Using Python"
EN_AUTHOR = "Anders Malthe-Sørenssen, 2022"

AR_GREETING = "مع تحيات"
YOUR_NAME = "Raji Youssef"
YOUR_NICKNAME = "The Fifth Dimension"
AR_SUBSCRIBE = "اشتركوا في قناة"
CHANNEL_NAME = "The Physics Symphony"
CHANNEL_URL = "www.youtube.com/@PhysicsSymphony_R"
# ----------------------------------------------------------------------


class GaussOutroTyping(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        self.source_page()
        self.greeting_page()

    def ar(self, content, font_size=30, color=WHITEISH):
        return MarkupText(escape(content), font=ARABIC_FONT,
                          font_size=font_size, color=color)

    def en(self, content, font_size=30, color=WHITEISH):
        return Text(content, font=ENGLISH_FONT,
                    font_size=font_size, color=color)

    def sized(self, obj, max_width):
        if obj.width > max_width:
            obj.scale_to_fit_width(max_width)
        return obj

    def type_reveal(self, obj, seconds):
        """Reveal already-shaped glyphs; do not construct partial Arabic words."""
        self.play(ShowIncreasingSubsets(obj, rate_func=linear), run_time=seconds)

    def source_page(self):
        # All positions are within the safe area of the 16:9 frame.
        heading = self.ar("المصدر", 46, GOLD).move_to(UP * 2.65)
        rule = Line(LEFT * 1.35, RIGHT * 1.35,
                    stroke_color=GOLD, stroke_width=2).next_to(heading, DOWN, buff=0.22)

        arabic = self.sized(self.ar(AR_SOURCE, 29), 11.7).move_to(UP * 1.12)
        author_ar = self.en(AR_AUTHOR, 27, CYAN).move_to(UP * 0.48)
        title = self.en(EN_TITLE, 37, WHITEISH).move_to(DOWN * 0.52)
        subtitle = self.en(EN_SUBTITLE, 37, WHITEISH).move_to(DOWN * 1.17)
        author_en = self.en(EN_AUTHOR, 27, CYAN).move_to(DOWN * 2.07)

        # Exactly 3.0 seconds total for this source page, including exit.
        self.play(FadeIn(heading), Create(rule), run_time=0.25)
        self.type_reveal(arabic, 0.49)
        self.type_reveal(author_ar, 0.32)
        self.type_reveal(title, 0.35)
        self.type_reveal(subtitle, 0.25)
        self.type_reveal(author_en, 0.34)
        self.wait(0.65)
        self.play(FadeOut(Group(*list(self.mobjects))), run_time=0.35)
        # 0.25 + .49 + .32 + .35 + .25 + .34 + .65 + .35 = 3.00

    def greeting_page(self):
        greeting = self.ar(AR_GREETING, 37, WHITEISH).move_to(UP * 2.60)
        name = self.en(YOUR_NAME, 56, GOLD).move_to(UP * 1.78)
        nickname = self.en(YOUR_NICKNAME, 32, CYAN).move_to(UP * 0.92)
        separator = Line(LEFT * 2.15, RIGHT * 2.15,
                         color=WHITEISH, stroke_opacity=0.4, stroke_width=1.5)
        separator.move_to(UP * 0.20)
        invitation = self.ar(AR_SUBSCRIBE, 35, WHITEISH).move_to(DOWN * 0.65)
        channel = self.en(CHANNEL_NAME, 46, GOLD).move_to(DOWN * 1.50)
        url = self.en(CHANNEL_URL, 26, CYAN).move_to(DOWN * 2.38)
        self.sized(url, 11.6)

        self.type_reveal(greeting, 0.65)
        self.type_reveal(name, 1.10)
        self.type_reveal(nickname, 0.90)
        self.play(Create(separator), run_time=0.35)
        self.type_reveal(invitation, 0.75)
        self.type_reveal(channel, 1.45)
        self.type_reveal(url, 1.45)
        self.wait(3.65)
        self.play(FadeOut(Group(*list(self.mobjects))), run_time=0.70)
        # .65 + 1.10 + .90 + .35 + .75 + 1.45 + 1.45 + 3.65 + .70 = 11.00


if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "manim", "-p", "-qh", "-r", "1920,1080",
        "--fps", "30", str(Path(__file__).resolve()), "GaussOutroTyping",
    ], check=True)
