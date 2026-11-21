
from manim import *
import numpy as np

BACKGROUND = "#0D1117"
TEXT_COLOR = "#E6EDF3"
MUTED = "#9CAABD"
AMBER = "#F2B84B"
BLUE = "#58A6FF"
GREEN = "#3FBF91"
ROAD = "#364151"
FONT = "Arial"



class Scene04Displacement(Scene):
    def arabic(self, string, size=30, color=TEXT_COLOR, weight=NORMAL):
        return Text(string, font=FONT, font_size=size, color=color, weight=weight)

    def make_path_one(self):
        points = [
            np.array([-5.2, -1.0, 0]),
            np.array([-4.2,  1.8, 0]),
            np.array([-2.4,  1.2, 0]),
            np.array([-0.6, -0.9, 0]),
            np.array([ 1.4, -1.5, 0]),
            np.array([ 3.8, -0.2, 0]),
            np.array([ 5.0,  1.2, 0]),
        ]
        path = VMobject()
        path.set_points_smoothly(points)
        path.set_fill(opacity=0)
        return path

    def construct(self):
        self.camera.background_color = BACKGROUND

        # ------------------------- Core geometry -------------------------
        start_point = np.array([-5.2, -1.0, 0])
        end_point = np.array([5.0, 1.2, 0])

        path1 = self.make_path_one()

        base_path = path1.copy().set_fill(opacity=0).set_stroke(ROAD, width=8, opacity=0.95)
        base_path.set_z_index(1)

        traveled_path = path1.copy().set_fill(opacity=0).set_stroke(AMBER, width=8, opacity=1)
        traveled_path.pointwise_become_partial(path1, 0, 0.00001)
        traveled_path.set_z_index(3)

        start_dot = Dot(start_point, radius=0.11, color=GREEN).set_z_index(8)
        end_dot = Dot(end_point, radius=0.11, color=GREEN).set_z_index(8)

        start_label = self.arabic("الموقع الابتدائي", size=26, color=GREEN)
        start_label.next_to(start_dot, DOWN, buff=0.48)
        start_label.set_z_index(10)

        end_label = self.arabic("الموقع النهائي", size=26, color=GREEN)
        end_label.next_to(end_dot, UP, buff=0.45)
        end_label.set_z_index(10)

        traveler = VGroup(
            Circle(radius=0.19, stroke_color=TEXT_COLOR, stroke_width=2, fill_opacity=0),
            Dot(radius=0.085, color=TEXT_COLOR),
        )
        traveler.move_to(start_point)
        traveler.set_z_index(9)

        path_label = self.arabic("المسار الفعلي", size=28, color=AMBER)
        path_label.move_to(np.array([-2.0, 2.35, 0]))
        path_label.set_z_index(12)

        progress = ValueTracker(0.0)

        def update_traveled(mob):
            p = np.clip(progress.get_value(), 0, 1)
            mob.pointwise_become_partial(path1, 0, max(0.00001, p))
            mob.set_fill(opacity=0)
            mob.set_stroke(AMBER, width=8, opacity=1)

        traveled_path.add_updater(update_traveled)
        traveler.add_updater(lambda m: m.move_to(path1.point_from_proportion(np.clip(progress.get_value(), 0, 1))))

        title = self.arabic("الإزاحة", size=44, color=TEXT_COLOR, weight=BOLD)
        title.to_edge(UP, buff=0.45)

        # ------------------------- Intro -------------------------
        self.play(FadeIn(title, shift=0.15 * DOWN), run_time=1.1)
        self.wait(0.8)

        self.play(Create(base_path), run_time=1.8)
        self.play(
            FadeIn(start_dot), FadeIn(end_dot),
            FadeIn(start_label), FadeIn(end_label),
            FadeIn(path_label, shift=0.1 * DOWN),
            run_time=1.5,
        )
        self.wait(1.0)

        self.add(traveled_path, traveler)
        self.play(progress.animate.set_value(1.0), run_time=4.8, rate_func=linear)
        traveled_path.clear_updaters()
        traveler.clear_updaters()
        self.wait(0.8)

        # ------------------------- Displacement vector -------------------------
        displacement_arrow = Arrow(
            start=start_point,
            end=end_point,
            buff=0,
            stroke_width=6,
            color=BLUE,
            max_tip_length_to_length_ratio=0.08,
        )
        displacement_arrow.set_z_index(6)

        disp_label = self.arabic("الإزاحة", size=30, color=BLUE)
        disp_label.move_to(np.array([2.25, 1.22, 0]))
        disp_label.set_z_index(11)

        self.play(
            base_path.animate.set_stroke(opacity=0.30),
            path_label.animate.set_opacity(0.55),
            run_time=0.8
        )
        self.play(GrowArrow(displacement_arrow), FadeIn(disp_label, shift=0.08 * DOWN), run_time=1.6)
        self.wait(1.2)

        # ------------------------- Magnitude and direction -------------------------
        magnitude_text = self.arabic("المقدار", size=24, color=BLUE)
        magnitude_text.move_to(np.array([-0.45, -1.05, 0]))
        magnitude_text.set_z_index(11)

        direction_text = self.arabic("الاتجاه", size=24, color=BLUE)
        direction_text.next_to(end_dot, DOWN, buff=0.32)
        direction_text.set_z_index(11)

        self.play(FadeIn(magnitude_text), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(direction_text), run_time=1.0)
        self.wait(1.2)

        # Maintain the exact same original curve and displacement arrow.
        self.play(FadeOut(traveler), run_time=0.4)
        self.wait(0.8)

        # ------------------------- The two questions -------------------------
        # Each question explicitly names the concept asking it.
        # Show them one at a time BELOW the diagram, never over the curve.
        distance_question = self.arabic(
            "المسافة تسأل: كم قطعت؟", size=28, color=AMBER
        )
        distance_question.move_to(np.array([0.0, -2.95, 0]))
        distance_question.set_z_index(15)

        displacement_question = self.arabic(
            "الإزاحة تسأل: أين انتهيت بالنسبة إلى المكان الذي بدأت منه؟",
            size=24, color=BLUE
        )
        displacement_question.move_to(np.array([0.0, -2.95, 0]))
        displacement_question.scale_to_fit_width(
            min(displacement_question.width, 11.7)
        )
        displacement_question.set_z_index(15)

        self.play(FadeIn(distance_question, shift=UP * 0.10), run_time=0.9)
        self.wait(2.0)
        self.play(
            FadeOut(distance_question),
            FadeIn(displacement_question, shift=UP * 0.10),
            run_time=0.9
        )
        self.wait(3.2)

        # ------------------------- Clean ending -------------------------
        final_group = VGroup(
            title,
            base_path,
            traveled_path,
            start_dot,
            end_dot,
            start_label,
            end_label,
            path_label,
            displacement_arrow,
            disp_label,
            magnitude_text,
            direction_text,
            displacement_question,
        )

        self.play(FadeOut(final_group), run_time=1.2)
        self.wait(0.4)


if __name__ == "__main__":
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60
    config.output_file = "scene_04"
    config.preview = True
    config.quality = "high_quality"

    Scene04Displacement().render()
