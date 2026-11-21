from manim import *
import numpy as np
from pathlib import Path

BACKGROUND = "#0D1117"
TEXT_COLOR = "#E6EDF3"
MUTED = "#9CA3AF"
AMBER = "#F2B84B"
BLUE = "#58A6FF"
GREEN = "#3FBF91"
HOUSE_FILL = "#1F6FEB"
HOUSE_FILL_2 = "#2EA043"
STORE_FILL = "#8B5CF6"
CARD_BG = "#111827"
CARD_STROKE = "#334155"
FONT = "Arial"

# Approximate narration duration, including the ending fade.
# Change this to the duration of your eventual voice recording.
NARRATION_SECONDS = 75.0


class Scene05HouseShopNeighborSophisticated(Scene):
    def hold_until(self, cue):
        """Hold the current picture until a narration cue (75-second baseline)."""
        target = cue * NARRATION_SECONDS / 75.0
        remaining = target - self.time
        if remaining > 0:
            self.wait(remaining)

    def ar(self, text, size=30, color=TEXT_COLOR, weight=NORMAL):
        # A leading LRM prevents this Windows Pango build from emitting an
        # empty SVG for an Arabic-only line. Arabic shaping remains intact.
        rendered = Text("\u200e" + text, font=FONT, font_size=size,
                        color=color, weight=weight)
        if text.strip() and (rendered.width == 0 or rendered.height == 0):
            raise RuntimeError(f"Text rendered without glyphs: {text!r}")
        return rendered

    def make_house(self, body_color=HOUSE_FILL, scale_factor=1.0):
        body = RoundedRectangle(
            corner_radius=0.08,
            width=1.05,
            height=0.72,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=body_color,
            fill_opacity=1,
        )
        roof = Polygon(
            [-0.62, 0.0, 0],
            [0.0, 0.55, 0],
            [0.62, 0.0, 0],
            stroke_color=WHITE,
            stroke_width=2,
            fill_color="#EF4444",
            fill_opacity=1,
        )
        roof.move_to(body.get_top() + UP * 0.01)

        door = RoundedRectangle(
            corner_radius=0.04,
            width=0.18,
            height=0.34,
            stroke_color=WHITE,
            stroke_width=1.5,
            fill_color="#8B5A2B",
            fill_opacity=1,
        ).move_to(body.get_bottom() + UP * 0.17)

        win1 = Square(0.14, stroke_color=WHITE, stroke_width=1.2, fill_color="#93C5FD", fill_opacity=1)
        win2 = win1.copy()
        win1.move_to(body.get_center() + LEFT * 0.24 + UP * 0.12)
        win2.move_to(body.get_center() + RIGHT * 0.24 + UP * 0.12)

        return VGroup(body, roof, door, win1, win2).scale(scale_factor)

    def make_store(self, scale_factor=1.0):
        base = RoundedRectangle(
            corner_radius=0.06,
            width=1.55,
            height=0.82,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=STORE_FILL,
            fill_opacity=1,
        )
        awning_top = Rectangle(width=1.60, height=0.12, stroke_width=0, fill_color="#F8FAFC", fill_opacity=1)
        awning_top.move_to(base.get_top() + DOWN * 0.06)

        stripes = VGroup()
        colors = ["#F8FAFC", "#FB7185"] * 4
        x0 = -0.68
        for i in range(7):
            rect = Rectangle(width=0.20, height=0.20, stroke_width=0, fill_color=colors[i], fill_opacity=1)
            rect.move_to(base.get_top() + DOWN * 0.22 + RIGHT * (x0 + 0.22 * i))
            stripes.add(rect)

        door = RoundedRectangle(
            corner_radius=0.03,
            width=0.22,
            height=0.34,
            stroke_color=WHITE,
            stroke_width=1.4,
            fill_color="#0F172A",
            fill_opacity=1,
        ).move_to(base.get_bottom() + UP * 0.19 + RIGHT * 0.35)

        window = RoundedRectangle(
            corner_radius=0.03,
            width=0.42,
            height=0.24,
            stroke_color=WHITE,
            stroke_width=1.4,
            fill_color="#C4B5FD",
            fill_opacity=1,
        ).move_to(base.get_bottom() + UP * 0.25 + LEFT * 0.32)

        sign = RoundedRectangle(
            corner_radius=0.04,
            width=0.75,
            height=0.18,
            stroke_color=WHITE,
            stroke_width=1.0,
            fill_color="#111827",
            fill_opacity=1,
        ).move_to(base.get_top() + UP * 0.18)
        sign_text = self.ar("STORE", size=16, color=WHITE, weight=BOLD).move_to(sign.get_center())

        return VGroup(base, awning_top, stripes, door, window, sign, sign_text).scale(scale_factor)

    def make_person(self, scale_factor=1.0):
        head = Circle(radius=0.10, stroke_color=WHITE, stroke_width=2, fill_color="#FDE68A", fill_opacity=1)
        body = Line(ORIGIN + UP * 0.02, ORIGIN + DOWN * 0.22, color=WHITE, stroke_width=2)
        left_arm = Line(ORIGIN + DOWN * 0.03, ORIGIN + LEFT * 0.16 + DOWN * 0.12, color=WHITE, stroke_width=2)
        right_arm = Line(ORIGIN + DOWN * 0.03, ORIGIN + RIGHT * 0.16 + DOWN * 0.12, color=WHITE, stroke_width=2)
        left_leg = Line(ORIGIN + DOWN * 0.22, ORIGIN + LEFT * 0.14 + DOWN * 0.42, color=WHITE, stroke_width=2)
        right_leg = Line(ORIGIN + DOWN * 0.22, ORIGIN + RIGHT * 0.14 + DOWN * 0.42, color=WHITE, stroke_width=2)
        torso = VGroup(body, left_arm, right_arm, left_leg, right_leg)
        torso.shift(DOWN * 0.10)
        return VGroup(head, torso).scale(scale_factor)

    def construct(self):
        self.camera.background_color = BACKGROUND

        title = self.ar("مثال: المنزل والمتجر ومنزل الجار", size=34, weight=BOLD)
        title.to_edge(UP, buff=0.25)
        title.set_z_index(30)

        # Spread the two houses farther apart to use the available width better.
        home_pos = np.array([-5.4, -2.45, 0])
        neighbor_pos = np.array([-1.9, -2.45, 0])
        store_pos = np.array([1.9, 1.65, 0])

        home_icon = self.make_house(HOUSE_FILL, 0.92).move_to(home_pos + UP * 0.55)
        neighbor_icon = self.make_house(HOUSE_FILL_2, 0.92).move_to(neighbor_pos + UP * 0.55)
        store_icon = self.make_store(0.95).move_to(store_pos + DOWN * 0.10)

        home_door = home_icon[2].get_center()
        neighbor_door = neighbor_icon[2].get_center()
        store_anchor = store_icon[0].get_bottom() + DOWN * 0.04

        home_label = self.ar("منزلك", size=26, color=GREEN)
        home_label.next_to(home_icon, UP, buff=0.16)
        home_label.shift(LEFT * 0.10)
        home_label.set_z_index(20)

        neighbor_label = self.ar("منزل الجار", size=26, color=GREEN)
        neighbor_label.next_to(neighbor_icon, UP, buff=0.16)
        neighbor_label.shift(RIGHT * 0.18)
        neighbor_label.set_z_index(20)

        store_label = self.ar("المتجر", size=28, color=GREEN)
        store_label.next_to(store_icon, UP, buff=0.18)
        store_label.set_z_index(20)

        ground_left = Line(home_pos + LEFT * 1.2 + DOWN * 0.05, neighbor_pos + RIGHT * 1.2 + DOWN * 0.05, color="#475569", stroke_width=3)
        ground_right = Line(np.array([0.8, 1.0, 0]), np.array([3.0, 1.0, 0]), color="#475569", stroke_width=3)
        ground_left.set_z_index(1)
        ground_right.set_z_index(1)

        separation_line = Line(home_door + DOWN * 0.22, neighbor_door + DOWN * 0.22, color=MUTED, stroke_width=2)
        separation_ticks = VGroup(
            Line(separation_line.get_start() + UP * 0.12, separation_line.get_start() + DOWN * 0.12, color=MUTED, stroke_width=2),
            Line(separation_line.get_end() + UP * 0.12, separation_line.get_end() + DOWN * 0.12, color=MUTED, stroke_width=2),
        )
        separation_label = self.ar("10 m", size=24, color=MUTED)
        separation_label.next_to(separation_line, DOWN, buff=0.10)
        separation_label.set_z_index(18)

        path1 = Line(home_door, store_anchor, color=AMBER, stroke_width=7)
        path2 = Line(store_anchor, neighbor_door, color=AMBER, stroke_width=7)
        path1_bg = path1.copy().set_color("#3F3F46").set_stroke(width=9, opacity=0.5)
        path2_bg = path2.copy().set_color("#3F3F46").set_stroke(width=9, opacity=0.5)
        path1_bg.set_z_index(2)
        path2_bg.set_z_index(2)
        path1.set_z_index(5)
        path2.set_z_index(5)

        length1 = self.ar("100 m", size=28, color=AMBER)
        length1.move_to(path1.get_center() + LEFT * 0.88 + UP * 0.15)
        length1.set_z_index(20)

        length2 = self.ar("95 m", size=28, color=AMBER)
        length2.move_to(path2.get_center() + RIGHT * 0.80 + UP * 0.10)
        length2.set_z_index(20)

        person = self.make_person(0.95).move_to(home_door + UP * 0.28)
        person.set_z_index(25)

        distance_card = RoundedRectangle(
            corner_radius=0.16,
            width=3.75,
            height=1.55,
            stroke_color=CARD_STROKE,
            stroke_width=2,
            fill_color=CARD_BG,
            fill_opacity=0.90,
        )
        distance_card.move_to(np.array([4.25, -1.20, 0]))
        distance_title = self.ar("المسافة", size=32, color=AMBER, weight=BOLD)
        distance_eq = self.ar("100 + 95 = 195 m", size=28, color=AMBER)
        distance_group = VGroup(distance_title, distance_eq).arrange(DOWN, buff=0.10).move_to(distance_card.get_center())
        distance_box = VGroup(distance_card, distance_group)
        distance_box.set_z_index(22)

        displacement_card = RoundedRectangle(
            corner_radius=0.16,
            width=4.15,
            height=1.55,
            stroke_color=CARD_STROKE,
            stroke_width=2,
            fill_color=CARD_BG,
            fill_opacity=0.90,
        )
        displacement_card.move_to(np.array([4.25, -2.95, 0]))
        displacement_title = self.ar("الإزاحة", size=32, color=BLUE, weight=BOLD)
        displacement_eq = self.ar("10 m", size=28, color=BLUE)
        displacement_group = VGroup(displacement_title, displacement_eq).arrange(DOWN, buff=0.10).move_to(displacement_card.get_center())
        displacement_box = VGroup(displacement_card, displacement_group)
        displacement_box.set_z_index(22)

        displacement_arrow = Arrow(
            start=home_door + DOWN * 0.22,
            end=neighbor_door + DOWN * 0.22,
            buff=0,
            color=BLUE,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.12,
        )
        displacement_arrow.set_z_index(10)

        displacement_label = self.ar("الإزاحة", size=28, color=BLUE, weight=BOLD)
        displacement_label.next_to(displacement_arrow, UP, buff=0.16)
        displacement_label.set_z_index(18)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1.0)
        self.hold_until(4)  # Introduction

        self.play(
            FadeIn(ground_left), FadeIn(ground_right),
            FadeIn(home_icon), FadeIn(neighbor_icon), FadeIn(store_icon),
            FadeIn(home_label), FadeIn(neighbor_label), FadeIn(store_label),
            run_time=1.8,
        )
        self.wait(0.8)

        self.play(
            Create(separation_line), FadeIn(separation_ticks), FadeIn(separation_label),
            run_time=1.0,
        )
        self.hold_until(12)  # Doors are 10 metres apart

        self.add(person)
        self.play(FadeIn(path1_bg), FadeIn(path2_bg), run_time=0.4)
        self.play(
            Create(path1),
            MoveAlongPath(person, path1),
            run_time=4.2,
            rate_func=linear,
        )
        self.play(FadeIn(length1), run_time=0.6)
        self.hold_until(24)  # Arrival at shop and time to buy groceries

        self.play(
            Create(path2),
            MoveAlongPath(person, path2),
            run_time=4.0,
            rate_func=linear,
        )
        self.play(FadeIn(length2), run_time=0.6)
        self.hold_until(32)  # Arrival at the neighbour

        self.play(
            Indicate(path1, color=AMBER, scale_factor=1.02),
            Indicate(path2, color=AMBER, scale_factor=1.02),
            run_time=1.2,
        )
        self.play(FadeIn(distance_box), run_time=1.0)
        self.hold_until(42)  # Distance: 100 + 95 = 195 m

        self.play(
            path1.animate.set_stroke(opacity=0.35),
            path2.animate.set_stroke(opacity=0.35),
            FadeOut(separation_line), FadeOut(separation_ticks),
            FadeOut(person),
            run_time=0.9,
        )
        self.hold_until(50)  # Displacement does not depend on the whole route
        self.play(Indicate(home_icon, color=BLUE), run_time=1.0)
        self.hold_until(54)  # Where did you start?
        self.play(Indicate(neighbor_icon, color=BLUE), run_time=1.0)
        self.hold_until(60)  # Where did you end?
        self.play(GrowArrow(displacement_arrow), run_time=1.1)
        self.play(FadeIn(displacement_label), FadeIn(displacement_box), run_time=1.0)
        self.hold_until(73)  # 10 m, directed from home to the neighbour

        final_group = VGroup(
            title,
            ground_left, ground_right,
            home_icon, neighbor_icon, store_icon,
            home_label, neighbor_label, store_label,
            separation_label,
            path1_bg, path2_bg, path1, path2, length1, length2,
            distance_box,
            displacement_arrow, displacement_label, displacement_box,
        )
        self.play(FadeOut(final_group), run_time=1.2)
        self.hold_until(75)


if __name__ == "__main__":
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60
    config.output_file = "scene_05"
    config.preview = True
    config.quality = "high_quality"

    Scene05HouseShopNeighborSophisticated().render()
