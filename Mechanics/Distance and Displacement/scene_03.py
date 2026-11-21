from manim import *
import numpy as np
import html

BG = "#0D1117"
WHITE = "#E6EDF3"
MUTED = "#9CAABD"
AMBER = "#F2B84B"
BLUE = "#58A6FF"
GREEN = "#3FBF91"
FONT = "Arial"



class Scene03DistanceUnitsZoom(MovingCameraScene):

    def arabic(self, string, size=30, color=WHITE):
        safe_string = html.escape(string)
        return MarkupText(f'<span font_family="{FONT}" lang="ar">{safe_string}</span>', font_size=size, color=color, disable_ligatures=False)

    def everyday(self):
        ruler = RoundedRectangle(width=5.6, height=0.65, corner_radius=0.08, stroke_color=MUTED, stroke_width=2, fill_color="#17202D", fill_opacity=1).shift(UP * 1.0)
        ticks = VGroup()

        for i in range(11):
            x = ruler.get_left()[0] + 0.25 + i * 0.51
            h = 0.30 if i in (0, 5, 10) else 0.16
            ticks.add(Line([x, 1.0 - h / 2, 0], [x, 1.0 + h / 2, 0], stroke_width=2, color=WHITE))

        meter = Text("1 m", font=FONT, font_size=34, color=AMBER)
        meter.next_to(ruler, UP, buff=0.25)

        road = RoundedRectangle(width=7.0, height=0.88, corner_radius=0.30, fill_color="#354253", fill_opacity=1, stroke_width=0).shift(DOWN * 1.0)
        stripe = DashedLine(road.get_left() + RIGHT * 0.45, road.get_right() + LEFT * 0.45, dash_length=0.22, color=WHITE, stroke_width=2)
        km = Text("1 km", font=FONT, font_size=34, color=AMBER)
        km.next_to(road, UP, buff=0.25)

        car_body = RoundedRectangle(width=0.40, height=0.18, corner_radius=0.05, stroke_width=0, fill_color=GREEN, fill_opacity=1)
        car_top = RoundedRectangle(width=0.22, height=0.10, corner_radius=0.03, stroke_width=0, fill_color="#52C7A3", fill_opacity=1).next_to(car_body, UP, buff=-0.03)
        wheel_left = Circle(radius=0.04, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        wheel_right = Circle(radius=0.04, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        wheel_left.move_to(car_body.get_bottom() + LEFT * 0.10 + DOWN * 0.01)
        wheel_right.move_to(car_body.get_bottom() + RIGHT * 0.10 + DOWN * 0.01)

        car = VGroup(car_body, car_top, wheel_left, wheel_right)
        car.move_to(road.get_left() + RIGHT * 0.65)

        road_set = VGroup(road, stripe, km, car)
        return VGroup(ruler, ticks, meter), road_set, car, road

    def astronomy(self):
        # Sun
        sun_halo = Circle(radius=1.38, stroke_width=0, fill_color="#FFA74D", fill_opacity=0.13)
        sun = Circle(radius=1.05, stroke_color="#FFBE62", stroke_width=3, fill_color="#FF7958", fill_opacity=1)
        sun_group = VGroup(sun_halo, sun).move_to([-4.2, 0.5, 0])
        sun_group.set_z_index(3)

        # Earth
        earth = Circle(radius=0.43, stroke_color=WHITE, stroke_width=2.5, fill_color="#2878E3", fill_opacity=1).move_to([3.9, 0.5, 0])
        patch1 = Ellipse(width=0.34, height=0.18, fill_color="#42B883", fill_opacity=1, stroke_width=0).rotate(0.5).move_to(earth.get_center() + LEFT * 0.09 + UP * 0.10)
        patch2 = Ellipse(width=0.17, height=0.23, fill_color="#42B883", fill_opacity=1, stroke_width=0).rotate(-0.5).move_to(earth.get_center() + RIGHT * 0.16 + DOWN * 0.11)

        earth_group = VGroup(earth, patch1, patch2)
        earth_group.set_z_index(5)

        # Arabic labels
        sun_name = self.arabic("الشمس", 32, WHITE)
        sun_name.next_to(sun_group, UP, buff=0.35)
        sun_name.set_z_index(10)

        earth_name = self.arabic("الأرض", 36, WHITE)
        earth_name.next_to(earth_group, UP, buff=0.35)
        earth_name.set_z_index(10)

        # Measurement arrow
        measure = DoubleArrow([-3.05, 0.5, 0], [3.35, 0.5, 0], buff=0, stroke_width=3.8, color=AMBER, tip_length=0.17)
        measure.set_z_index(1)

        unit = Text("1 AU", font=FONT, font_size=42, color=AMBER)
        unit.move_to([0.15, -0.25, 0])
        unit.set_z_index(10)

        return VGroup(sun_group, earth_group, sun_name, earth_name, measure, unit)

    def light_year(self):
        source = VGroup(Circle(radius=0.26, color=AMBER, stroke_width=3), Dot(radius=0.12, color=AMBER)).move_to([-4.9, 0.1, 0])
        target = VGroup(Circle(radius=0.28, color=BLUE, stroke_width=3), Dot(radius=0.08, color=BLUE)).move_to([4.9, 0.1, 0])

        labels = VGroup(self.arabic("مصدر ضوء", 28).move_to([-4.9, -0.70, 0]), self.arabic("نقطة وصول", 28).move_to([4.9, -0.70, 0]))

        x0 = -4.55
        x1 = 4.55
        y = 0.1

        baseline = DashedLine([x0, y, 0], [x1, y, 0], dash_length=0.16, color="#415164", stroke_width=2)
        clock_bg = RoundedRectangle(width=2.35, height=0.7, corner_radius=0.12, stroke_color=BLUE, stroke_width=2, fill_color="#111E2D", fill_opacity=1).move_to([0, 2.4, 0])

        progress = ValueTracker(0)
        clock_value = DecimalNumber(0, num_decimal_places=1, font_size=30, color=BLUE)
        clock_unit = Text("year", font=FONT, font_size=25, color=BLUE)
        clock_unit.move_to([0.67, 2.4, 0])

        def update_clock(obj):
            obj.set_value(progress.get_value())
            obj.move_to([-0.48, 2.4, 0])

        clock_value.add_updater(update_clock)
        clock_value.move_to([-0.48, 2.4, 0])

        wave = VMobject()
        wave.set_stroke(AMBER, width=4)

        def update_wave(obj):
            p = max(0, min(1, progress.get_value()))
            end_x = x0 + (x1 - x0) * p

            if p < 0.003:
                obj.set_points_as_corners([[x0, y, 0], [x0 + 0.001, y, 0]])
                return

            xs = np.linspace(x0, end_x, max(12, int(250 * p)))
            phase = 2 * np.pi * 7 * (xs - x0) / (x1 - x0) - 2 * np.pi * 7 * p
            envelope = np.minimum(1.0, (xs - x0) / 0.35)
            envelope *= np.minimum(1.0, (end_x - xs) / 0.35)
            yy = y + 0.21 * np.maximum(0, envelope) * np.sin(phase)

            obj.set_points_as_corners(np.column_stack((xs, yy, np.zeros(len(xs)))))
            obj.set_stroke(AMBER, width=4)

        wave.add_updater(update_wave)
        wave.update()

        tip = Dot(radius=0.085, color=AMBER)
        tip.add_updater(lambda m: m.move_to([x0 + (x1 - x0) * progress.get_value(), y, 0]))
        tip.update()

        length_line = Line([x0, -1.35, 0], [x1, -1.35, 0], color=AMBER, stroke_width=2.8)
        ticks = VGroup(Line([x0, -1.18, 0], [x0, -1.52, 0], color=AMBER), Line([x1, -1.18, 0], [x1, -1.52, 0], color=AMBER))
        length_label = self.arabic("سنة ضوئية", 35, AMBER)
        length_label.move_to([0, -2.0, 0])
        ruler = VGroup(length_line, ticks, length_label)

        static = VGroup(source, target, labels, baseline, clock_bg, clock_value, clock_unit)
        return static, wave, tip, ruler, progress, clock_value

    def atomic(self):
        main = Line([-4.2, 0.45, 0], [4.2, 0.45, 0], color=AMBER, stroke_width=6)
        caps = VGroup(Line([-4.2, 0.23, 0], [-4.2, 0.67, 0], color=AMBER), Line([4.2, 0.23, 0], [4.2, 0.67, 0], color=AMBER))
        nm = Text("1 nm", font=FONT, font_size=38, color=AMBER)
        nm.move_to([0, -0.30, 0])

        tenth = Line([-4.2, 0.45, 0], [-3.36, 0.45, 0], color=BLUE, stroke_width=9)
        tenth.set_z_index(4)
        short_ticks = VGroup(Line([-4.2, 0.09, 0], [-4.2, 0.79, 0], color=BLUE), Line([-3.36, 0.09, 0], [-3.36, 0.79, 0], color=BLUE))
        eq = Text("1 Å = 0.1 nm", font=FONT, font_size=36, color=BLUE)
        eq.move_to([0, 1.50, 0])

        return VGroup(main, caps, nm), VGroup(tenth, short_ticks, eq)

    def construct(self):
        self.camera.background_color = BG
        self.camera.frame.save_state()

        # Everyday scale
        ruler, road_group, marker, road = self.everyday()
        self.play(FadeIn(ruler), run_time=1.2)
        self.wait(1.4)
        self.play(FadeIn(road_group), run_time=1.2)

        path = Line(road.get_left() + RIGHT * 0.65, road.get_right() + LEFT * 0.65)
        self.play(MoveAlongPath(marker, path), run_time=2.2, rate_func=linear)
        self.wait(0.8)

        # Zoom out
        self.play(self.camera.frame.animate.scale(1.10), FadeOut(ruler, scale=0.75), FadeOut(road_group, scale=0.75), run_time=1.5)
        self.remove(ruler, road_group)

        # Astronomy
        astronomy = self.astronomy()
        self.play(FadeIn(astronomy[0]), FadeIn(astronomy[1], scale=0.6), run_time=1.5)
        self.play(FadeIn(astronomy[2]), FadeIn(astronomy[3]), run_time=0.9)
        self.wait(0.7)
        self.play(GrowFromCenter(astronomy[4]), FadeIn(astronomy[5]), run_time=1.5)
        self.wait(2.5)

        # Remove astronomy graphics
        self.play(FadeOut(astronomy), self.camera.frame.animate.scale(1.06), run_time=1.4)
        self.remove(astronomy)

        # Light-year
        ly_static, wave, tip, ly_ruler, progress, clock_value = self.light_year()
        self.play(FadeIn(ly_static), run_time=1.3)
        self.wait(0.7)
        self.add(wave, tip)
        self.play(progress.animate.set_value(1), run_time=5.0, rate_func=linear)

        wave.clear_updaters()
        tip.clear_updaters()
        clock_value.clear_updaters()

        self.wait(0.6)
        self.play(Create(ly_ruler[0]), FadeIn(ly_ruler[1]), FadeIn(ly_ruler[2]), run_time=1.4)
        self.wait(2.0)

        # Atomic scale
        self.play(FadeOut(ly_static), FadeOut(wave), FadeOut(tip), FadeOut(ly_ruler), self.camera.frame.animate.scale(0.85), run_time=1.5)
        self.remove(ly_static, wave, tip, ly_ruler)

        nm_group, angstrom_group = self.atomic()
        self.play(FadeIn(nm_group), run_time=1.4)
        self.wait(1.2)
        self.play(FadeIn(angstrom_group), run_time=1.4)
        self.wait(3.5)
        self.play(FadeOut(nm_group), FadeOut(angstrom_group), run_time=1.2)
        self.wait(0.5)


if __name__ == "__main__":
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60
    config.output_file = "scene_03"
    config.preview = True
    config.quality = "high_quality"

    Scene03DistanceUnitsZoom().render()