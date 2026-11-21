
from manim import *
import numpy as np

BACKGROUND = "#0D1117"
TEXT_COLOR = "#E6EDF3"
SUBTLE = "#9CAABD"
AMBER = "#F2B84B"
GREEN = "#3FBF91"
ROAD = "#364151"
FONT = "Arial"


class Scene02WhatIsDistance(Scene):

    def make_route(self):
        """Build a continuous, length-parameterized route."""

        a = np.array([-4.90, -0.80, 0.0])
        b = np.array([-2.55, -0.80, 0.0])
        c = np.array([1.65, 0.15, 0.0])
        d = np.array([4.85, 0.15, 0.0])

        components = [
            Line(a, b),
            CubicBezier(
                b,
                [-1.60, 1.15, 0],
                [0.05, -1.10, 0],
                c
            ),
            Line(c, d),
        ]

        cloud = []

        for index, part in enumerate(components):
            values = np.linspace(0, 1, 600)

            if index:
                values = values[1:]

            cloud.extend(
                part.point_from_proportion(float(t))
                for t in values
            )

        cloud = np.array(cloud)

        segment_lengths = np.linalg.norm(
            np.diff(cloud, axis=0),
            axis=1
        )

        cumulative = np.r_[
            0,
            np.cumsum(segment_lengths)
        ]

        distances = np.linspace(
            0,
            cumulative[-1],
            1800
        )

        even_points = np.stack([
            np.interp(
                distances,
                cumulative,
                cloud[:, axis]
            )
            for axis in range(3)
        ], axis=1)

        route = VMobject()
        route.set_points_as_corners(even_points)

        return route, a, d

    def construct(self):

        self.camera.background_color = BACKGROUND

        # Title
        heading = Text(
            "المسافة",
            font=FONT,
            font_size=48,
            color=TEXT_COLOR,
            weight=BOLD
        )

        heading.to_edge(UP, buff=0.55)

        self.play(
            FadeIn(heading, shift=0.15 * DOWN),
            run_time=1.2
        )

        self.wait(1.6)

        # Draw the route
        route, start, end = self.make_route()

        base = route.copy().set_stroke(
            ROAD,
            width=10,
            opacity=0.95
        )

        base.set_z_index(1)

        self.play(
            Create(base),
            run_time=2.5
        )

        start_dot = Dot(
            start,
            radius=0.105,
            color=GREEN
        ).set_z_index(6)

        end_dot = Dot(
            end,
            radius=0.105,
            color=GREEN
        ).set_z_index(6)

        start_text = Text(
            "البداية",
            font=FONT,
            font_size=24,
            color=GREEN
        )

        end_text = Text(
            "النهاية",
            font=FONT,
            font_size=24,
            color=GREEN
        )

        start_text.next_to(
            start_dot,
            DOWN,
            buff=0.30
        )

        end_text.next_to(
            end_dot,
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(start_dot),
            FadeIn(end_dot),
            FadeIn(start_text),
            FadeIn(end_text),
            run_time=1.3
        )

        self.wait(1.2)

        # Moving object and traveled path
        progress = ValueTracker(0)

        trace = route.copy().set_stroke(
            AMBER,
            width=10,
            opacity=1
        )

        trace.pointwise_become_partial(
            route, 0, 0.000001
        )

        trace.set_z_index(3)

        marker = VGroup(
            Circle(
                radius=0.19,
                stroke_color=TEXT_COLOR,
                stroke_width=2,
                fill_opacity=0
            ),
            Dot(
                radius=0.09,
                color=TEXT_COLOR
            )
        )

        marker.move_to(start)
        marker.set_z_index(8)

        def update_trace(mob):
            fraction = np.clip(
                progress.get_value(),
                0.0,
                1.0
            )

            mob.pointwise_become_partial(
                route,
                0,
                max(0.000001, fraction)
            )

            mob.set_stroke(
                AMBER,
                width=10,
                opacity=1
            )

        trace.add_updater(update_trace)

        marker.add_updater(
            lambda mob: mob.move_to(
                route.point_from_proportion(
                    np.clip(
                        progress.get_value(),
                        0.0,
                        1.0
                    )
                )
            )
        )

        self.add(trace, marker)

        # First section of the journey
        self.play(
            progress.animate.set_value(0.36),
            run_time=4.4,
            rate_func=linear
        )

        self.wait(0.7)

        # Curved section
        self.play(
            progress.animate.set_value(0.70),
            run_time=4.2,
            rate_func=linear
        )

        self.wait(0.7)

        # Final section
        self.play(
            progress.animate.set_value(1.0),
            run_time=3.7,
            rate_func=linear
        )

        trace.clear_updaters()
        marker.clear_updaters()

        self.wait(1.2)

        # Emphasize the complete traveled route
        self.play(
            FadeOut(marker),
            Indicate(
                trace,
                color=AMBER,
                scale_factor=1.012
            ),
            run_time=1.5
        )

        self.wait(0.9)

        idea = Text(
            "طول الطريق الذي قُطِع فعلًا",
            font=FONT,
            font_size=31,
            color=TEXT_COLOR
        )

        idea.to_edge(DOWN, buff=0.56)

        underline = Underline(
            idea,
            color=AMBER,
            buff=0.14,
            stroke_width=3
        )

        self.play(
            FadeIn(idea, shift=0.14 * UP),
            Create(underline),
            run_time=1.4
        )

        self.wait(3.6)

        # Clean ending for the continuous video
        self.play(
            FadeOut(
                VGroup(
                    heading,
                    idea,
                    underline,
                    base,
                    trace,
                    start_dot,
                    end_dot,
                    start_text,
                    end_text
                )
            ),
            run_time=1.4
        )

        self.wait(0.5)


if __name__ == "__main__":
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60
    config.output_file = "scene_02"
    config.preview = True
    config.quality = "high_quality"

    Scene02WhatIsDistance().render()
