from manim import *
import numpy as np


BG = "#0D1117"
WHITE_SOFT = "#E6EDF3"
MUTED = "#97A6BA"
AMBER = "#F2B84B"
BLUE = "#58A6FF"
GREEN = "#3FBF91"
ROAD = "#334155"
FONT = "Arial"


class Scene01DistanceDisplacement(Scene):
    """Scene 01: a 1000 m closed walk, ending with zero displacement."""

    def construct(self):
        self.camera.background_color = BG

        # ---------- Typography / title ----------
        title = Text("المسافة والإزاحة", font=FONT, font_size=45,
                     color=WHITE_SOFT, weight=BOLD).to_edge(UP, buff=0.40)
        subtitle = Text("هل يمكن أن تقطع مسافة وتعود إلى نقطة البداية؟",
                        font=FONT, font_size=25, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1.2)
        self.play(FadeIn(subtitle, shift=DOWN * 0.12), run_time=1.0)
        self.wait(1.1)

        # ---------- A metric-independent schematic route ----------
        # We sample a simple closed curve and resample it at equal arc-length
        # intervals. Consequently, a linear tracker gives uniform progress in
        # traversed distance, and the distance counter can read 1000*t meters.
        n_raw = 2500
        theta = np.linspace(np.pi, 3 * np.pi, n_raw)
        cx, cy = -0.18, -0.37
        rx, ry = 3.86, 1.75
        x = cx + rx * np.cos(theta)
        y = cy + ry * np.sin(theta) + 0.19 * np.sin(2 * theta)
        raw = np.column_stack((x, y, np.zeros_like(x)))
        seg = np.linalg.norm(np.diff(raw, axis=0), axis=1)
        cumulative = np.r_[0.0, np.cumsum(seg)]
        targets = np.linspace(0, cumulative[-1], 1100)
        samples = np.column_stack([
            np.interp(targets, cumulative, raw[:, k]) for k in range(3)
        ])
        samples[-1] = samples[0]

        route = VMobject()
        route.set_points_as_corners(samples)
        route.set_stroke(ROAD, width=11, opacity=0.85)

        start = samples[0]
        # House is attached to the start point on the far-left of the route.
        wall = RoundedRectangle(width=1.18, height=0.92, corner_radius=0.07,
                                stroke_color=WHITE_SOFT, stroke_width=2,
                                fill_color="#203040", fill_opacity=1)
        wall.move_to(start + LEFT * 0.59 + UP * 0.12)
        roof = Polygon(start + LEFT * 1.26 + UP * 0.58,
                       start + LEFT * 0.59 + UP * 1.15,
                       start + RIGHT * 0.08 + UP * 0.58,
                       color=WHITE_SOFT, stroke_width=2,
                       fill_color="#31536D", fill_opacity=1)
        door = Rectangle(width=0.22, height=0.43,
                         color=AMBER, stroke_width=1.5,
                         fill_color="#172431", fill_opacity=1)
        door.move_to(start + LEFT * 0.12 + DOWN * 0.12)
        home = VGroup(wall, roof, door)
        home_label = Text("المنزل", font=FONT, font_size=25,
                          color=WHITE_SOFT).next_to(home, LEFT, buff=0.25)

        start_ring = Circle(radius=0.16, color=GREEN, stroke_width=2.5)
        start_ring.move_to(start)
        start_marker = Dot(start, radius=0.07, color=GREEN)
        start_tag = Text("نقطة البداية", font=FONT, font_size=21,
                         color=GREEN).next_to(start_ring, DOWN, buff=0.25)

        self.play(DrawBorderThenFill(home), FadeIn(home_label), run_time=1.8)
        self.play(Create(route), run_time=2.0)
        self.play(Create(start_ring), FadeIn(start_marker), FadeIn(start_tag),
                  run_time=1.4)
        self.wait(1.3)

        # ---------- Motion and progress-linked distance ----------
        progress = ValueTracker(0)
        walked = route.copy().set_stroke(AMBER, width=12, opacity=1)
        walked.pointwise_become_partial(route, 0, 0.00001)
        walked.add_updater(lambda mob: mob.pointwise_become_partial(
            route, 0, max(0.00001, progress.get_value())))
        walked.set_z_index(2)

        # A small moving person icon made only with vector primitives.
        head = Circle(radius=0.095, stroke_width=0,
                      fill_color=WHITE_SOFT, fill_opacity=1).shift(UP * 0.16)
        body = Line(DOWN * 0.02, DOWN * 0.25, color=WHITE_SOFT,
                    stroke_width=3.2)
        arms = VGroup(
            Line(UP * 0.01, LEFT * 0.13 + DOWN * 0.11,
                 color=WHITE_SOFT, stroke_width=2.7),
            Line(UP * 0.01, RIGHT * 0.13 + DOWN * 0.10,
                 color=WHITE_SOFT, stroke_width=2.7)
        )
        legs = VGroup(
            Line(DOWN * 0.25, LEFT * 0.12 + DOWN * 0.38,
                 color=WHITE_SOFT, stroke_width=2.7),
            Line(DOWN * 0.25, RIGHT * 0.12 + DOWN * 0.37,
                 color=WHITE_SOFT, stroke_width=2.7)
        )
        person = VGroup(head, body, arms, legs)
        person.move_to(start + UP * 0.20)
        person.add_updater(lambda mob: mob.move_to(
            route.point_from_proportion(progress.get_value()) + UP * 0.20))
        person.set_z_index(5)

        dist_value = DecimalNumber(0, num_decimal_places=0, font_size=43,
                                   color=AMBER, group_with_commas=False)
        dist_unit = Text("m", font=FONT, font_size=26, color=AMBER)
        # Keep the changing number and its unit in ONE centered row.
        # DecimalNumber changes width (e.g. 99 -> 100 -> 1000), so the row
        # must be rearranged on every rendered frame to avoid overlap.
        dist_number = VGroup(dist_value, dist_unit).arrange(RIGHT, buff=0.18)
        dist_title = Text("المسافة المقطوعة", font=FONT,
                          font_size=24, color=MUTED)
        dist_panel = VGroup(dist_title, dist_number).arrange(DOWN, buff=0.15)
        dist_panel.move_to(DOWN * 3.13 + LEFT * 3.05)
        number_row_center = dist_number.get_center().copy()
        def update_distance_row(row):
            # Update the digits BEFORE arranging the unit, in the same frame.
            dist_value.set_value(1000 * progress.get_value())
            row.arrange(RIGHT, buff=0.18)
            row.move_to(number_row_center)

        dist_number.add_updater(update_distance_row)
        dist_box = RoundedRectangle(width=4.1, height=1.24,
                                    corner_radius=0.17, stroke_color=AMBER,
                                    stroke_opacity=0.45, stroke_width=1.4,
                                    fill_color="#121D29", fill_opacity=0.95)
        dist_box.move_to(dist_panel)

        self.play(FadeIn(dist_box), FadeIn(dist_title),
                  FadeIn(dist_number), FadeIn(person), run_time=1.3)
        self.add(walked)
        self.play(progress.animate.set_value(0.48),
                  run_time=5.5, rate_func=linear)
        self.wait(0.7)
        self.play(progress.animate.set_value(1.0),
                  run_time=6.0, rate_func=linear)
        # Freeze the distance and drawing at the final value.
        walked.clear_updaters()
        person.clear_updaters()
        dist_number.clear_updaters()
        dist_value.set_value(1000)
        dist_number.arrange(RIGHT, buff=0.18).move_to(number_row_center)
        self.wait(1.7)

        # ---------- Reveal that start and finish are the same ----------
        finish_ring = Circle(radius=0.28, color=BLUE, stroke_width=2.4)
        finish_ring.move_to(start)
        endpoint_text = Text("النهاية = البداية", font=FONT,
                             font_size=26, color=BLUE)
        endpoint_text.move_to(RIGHT * 2.7 + UP * 1.9)
        endpoint_line = Line(endpoint_text.get_left() + LEFT * 0.12,
                             start + RIGHT * 0.16 + UP * 0.12,
                             color=BLUE, stroke_width=1.8)
        endpoint_line.set_opacity(0.70)

        # Fade the previously traced path so the common endpoint is central.
        self.play(walked.animate.set_stroke(opacity=0.32),
                  route.animate.set_stroke(opacity=0.35),
                  Create(finish_ring), run_time=1.7)
        self.play(FadeIn(endpoint_text), Create(endpoint_line),
                  run_time=1.4)
        self.wait(1.6)

        displacement_title = Text("مقدار الإزاحة", font=FONT,
                                  font_size=24, color=MUTED)
        displacement_value = Text("0 m", font=FONT,
                                  font_size=43, color=BLUE)
        displacement_panel = VGroup(displacement_title,
                                    displacement_value).arrange(DOWN, buff=0.15)
        displacement_panel.move_to(DOWN * 3.13 + RIGHT * 3.05)
        displacement_box = RoundedRectangle(width=4.1, height=1.24,
                                           corner_radius=0.17,
                                           stroke_color=BLUE,
                                           stroke_opacity=0.5,
                                           stroke_width=1.4,
                                           fill_color="#121D29", fill_opacity=0.95)
        displacement_box.move_to(displacement_panel)
        self.play(FadeIn(displacement_box), FadeIn(displacement_panel,
                                                  shift=UP * 0.1),
                  run_time=1.5)
        self.wait(2.2)

        # ---------- Clean closing question, lead into scene 02 ----------
        closing = Text("لماذا تختلف المسافة عن الإزاحة؟", font=FONT,
                       font_size=29, color=WHITE_SOFT)
        closing.move_to(UP * 2.42)
        self.play(FadeOut(subtitle), FadeOut(endpoint_line),
                  FadeOut(endpoint_text), FadeIn(closing), run_time=1.3)
        self.wait(3.0)
        self.play(FadeOut(VGroup(title, closing, home, home_label, route,
                                 walked, person, start_ring, start_marker,
                                 start_tag, finish_ring, dist_box, dist_panel,
                                 displacement_box, displacement_panel)),
                  run_time=1.7)
        self.wait(0.8)


if __name__ == "__main__":
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60
    config.background_color = BG
    config.output_file = "scene_01"
    config.preview = True
    config.quality = "high_quality"

    Scene01DistanceDisplacement().render()
