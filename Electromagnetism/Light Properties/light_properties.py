from manim import *
import numpy as np


# =========================================================
# GLOBAL SETTINGS
# =========================================================

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = "#0B1020"


# =========================================================
# SCENE 1 — ELECTROMAGNETIC SPECTRUM
# =========================================================

class EMSpectrum(Scene):
    def construct(self):

        title = Text(
            "Electromagnetic Spectrum",
            font_size=52
        ).to_edge(UP)

        self.play(Write(title))

        names = [
            "Radio",
            "Microwave",
            "Infrared",
            "Visible",
            "Ultraviolet",
            "X-rays",
            "Gamma"
        ]

        colors = [
            PURPLE_E,
            PURPLE_C,
            RED_D,
            GREEN,
            BLUE,
            BLUE_D,
            PURPLE
        ]

        spectrum = VGroup()

        for name, color in zip(names, colors):

            box = Rectangle(
                width=1.65,
                height=1.3,
                fill_color=color,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )

            label = Text(
                name,
                font_size=22
            )

            label.move_to(box)

            section = VGroup(box, label)
            spectrum.add(section)

        spectrum.arrange(RIGHT, buff=0)
        spectrum.move_to(ORIGIN)

        self.play(
            LaggedStart(
                *[
                    FadeIn(section, shift=UP * 0.3)
                    for section in spectrum
                ],
                lag_ratio=0.15
            ),
            run_time=3
        )

        arrow = Arrow(
            spectrum.get_left(),
            spectrum.get_right(),
            buff=0,
            color=WHITE
        )

        arrow.next_to(
            spectrum,
            DOWN,
            buff=0.7
        )

        long_text = Text(
            "Long wavelength",
            font_size=25
        ).next_to(
            arrow,
            LEFT,
            buff=0.2
        )

        short_text = Text(
            "Short wavelength",
            font_size=25
        ).next_to(
            arrow,
            RIGHT,
            buff=0.2
        )

        self.play(
            GrowArrow(arrow),
            FadeIn(long_text),
            FadeIn(short_text)
        )

        self.wait(1)

        visible = spectrum[3]

        highlight = SurroundingRectangle(
            visible,
            color=YELLOW,
            stroke_width=6,
            buff=0.08
        )

        visible_text = Text(
            "Visible Light",
            color=YELLOW,
            font_size=34
        ).next_to(
            highlight,
            UP,
            buff=0.35
        )

        self.play(
            Create(highlight),
            Write(visible_text),
            run_time=1.5
        )

        self.wait(1)

        rainbow_colors = [
            RED,
            ORANGE,
            YELLOW,
            GREEN,
            BLUE,
            PURPLE
        ]

        rainbow = VGroup()

        for color in rainbow_colors:

            bar = Rectangle(
                width=0.65,
                height=0.55,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            )

            rainbow.add(bar)

        rainbow.arrange(RIGHT, buff=0)

        rainbow.next_to(
            spectrum,
            DOWN,
            buff=1.5
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(bar)
                    for bar in rainbow
                ],
                lag_ratio=0.12
            )
        )

        wavelength = MathTex(
            r"\approx 380\text{ nm} \;-\; 700\text{ nm}",
            font_size=36
        )

        wavelength.next_to(
            rainbow,
            DOWN
        )

        self.play(
            Write(wavelength)
        )

        self.wait(3)

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "EMSpectrum"
    }):
        EMSpectrum().render()
# =========================================================
# SCENE 2 — REFLECTION
# =========================================================

class Reflection(Scene):
    def construct(self):

        title = Text(
            "Reflection of Light",
            font_size=50
        ).to_edge(UP)

        self.play(
            Write(title)
        )

        # Mirror
        mirror = Line(
            LEFT * 5,
            RIGHT * 5,
            color=GREY_B,
            stroke_width=6
        ).shift(DOWN * 1.5)

        mirror_label = Text(
            "Mirror",
            font_size=26,
            color=GREY_A
        ).next_to(
            mirror,
            DOWN,
            buff=0.25
        )

        self.play(
            Create(mirror),
            FadeIn(mirror_label)
        )

        incidence_point = mirror.get_center()

        # Normal
        normal = DashedLine(
            incidence_point + DOWN * 0.1,
            incidence_point + UP * 4,
            color=WHITE,
            stroke_width=3
        )

        normal_label = Text(
            "Normal",
            font_size=24
        ).next_to(
            normal.get_end(),
            RIGHT,
            buff=0.2
        )

        self.play(
            Create(normal),
            FadeIn(normal_label)
        )

        # Incident ray
        incident_start = LEFT * 4 + UP * 2.5

        incident_ray = Arrow(
            incident_start,
            incidence_point,
            buff=0,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        incident_label = Text(
            "Incident ray",
            font_size=26,
            color=YELLOW
        ).next_to(
            incident_ray,
            LEFT,
            buff=0.2
        )

        self.play(
            GrowArrow(incident_ray),
            FadeIn(incident_label)
        )

        # Reflected ray
        reflected_end = RIGHT * 4 + UP * 2.5

        reflected_ray = Arrow(
            incidence_point,
            reflected_end,
            buff=0,
            color=BLUE_C,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        reflected_label = Text(
            "Reflected ray",
            font_size=26,
            color=BLUE_C
        ).next_to(
            reflected_ray,
            RIGHT,
            buff=0.2
        )

        self.play(
            GrowArrow(reflected_ray),
            FadeIn(reflected_label)
        )

        # Angles
        incident_angle = Angle(
            normal,
            incident_ray,
            radius=0.8,
            other_angle=True,
            color=YELLOW
        )

        reflected_angle = Angle(
            reflected_ray,
            normal,
            radius=0.8,
            other_angle=True,
            color=BLUE_C
        )

        theta_i = MathTex(
            r"\theta_i",
            color=YELLOW
        ).next_to(
            incident_angle,
            LEFT,
            buff=0.1
        )

        theta_r = MathTex(
            r"\theta_r",
            color=BLUE_C
        ).next_to(
            reflected_angle,
            RIGHT,
            buff=0.1
        )

        self.play(
            Create(incident_angle),
            Create(reflected_angle),
            Write(theta_i),
            Write(theta_r)
        )

        law = MathTex(
            r"\theta_i = \theta_r",
            font_size=48
        ).to_edge(DOWN)

        self.play(
            Write(law)
        )

        self.wait(2)

        self.play(
            FadeOut(
                incident_label,
                reflected_label,
                theta_i,
                theta_r,
                incident_angle,
                reflected_angle,
                law,
                normal_label
            )
        )

        # Move reflection diagram upward
        reflection_group = VGroup(
            mirror,
            mirror_label,
            normal,
            incident_ray,
            reflected_ray
        )

        self.play(
            reflection_group.animate.shift(UP * 0.7)
        )

        # -------------------------------------------------
        # Smooth vs rough reflection
        # -------------------------------------------------

        smooth_title = Text(
            "Smooth surface",
            font_size=30,
            color=GREEN_C
        ).shift(
            LEFT * 3 + DOWN * 1.9
        )

        rough_title = Text(
            "Rough surface",
            font_size=30,
            color=RED_C
        ).shift(
            RIGHT * 3 + DOWN * 1.9
        )

        self.play(
            FadeIn(smooth_title),
            FadeIn(rough_title)
        )

        # Smooth surface
        smooth_surface = Line(
            LEFT * 5.2,
            LEFT * 0.8,
            color=GREY_B,
            stroke_width=5
        ).shift(DOWN * 2.8)

        self.play(
            Create(smooth_surface)
        )

        smooth_incoming = VGroup()
        smooth_reflected = VGroup()

        for x in [-4.7, -3.7, -2.7, -1.7]:

            incoming = Arrow(
                [x - 0.5, -1.9, 0],
                [x, -2.8, 0],
                buff=0,
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )

            outgoing = Arrow(
                [x, -2.8, 0],
                [x + 0.5, -1.9, 0],
                buff=0,
                color=BLUE_C,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )

            smooth_incoming.add(incoming)
            smooth_reflected.add(outgoing)

        self.play(
            LaggedStart(
                *[
                    GrowArrow(ray)
                    for ray in smooth_incoming
                ],
                lag_ratio=0.15
            )
        )

        self.play(
            LaggedStart(
                *[
                    GrowArrow(ray)
                    for ray in smooth_reflected
                ],
                lag_ratio=0.15
            )
        )

        # Rough surface
        rough_points = [
            [1.0, -2.8, 0],
            [1.6, -2.55, 0],
            [2.2, -2.9, 0],
            [2.8, -2.6, 0],
            [3.4, -2.85, 0],
            [4.0, -2.6, 0],
            [4.6, -2.8, 0]
        ]

        rough_surface = VMobject()
        rough_surface.set_points_as_corners(
            rough_points
        )

        rough_surface.set_stroke(
            color=GREY_B,
            width=5
        )

        self.play(
            Create(rough_surface)
        )

        rough_incoming = VGroup()
        rough_reflected = VGroup()

        x_positions = [
            1.4,
            2.3,
            3.2,
            4.1
        ]

        directions = [
            LEFT * 0.4 + UP * 1.0,
            RIGHT * 0.7 + UP * 1.0,
            LEFT * 0.8 + UP * 1.0,
            RIGHT * 0.3 + UP * 1.0
        ]

        for x, direction in zip(
            x_positions,
            directions
        ):

            incoming = Arrow(
                [x - 0.4, -1.8, 0],
                [x, -2.7, 0],
                buff=0,
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )

            outgoing = Arrow(
                [x, -2.7, 0],
                np.array([x, -2.7, 0]) + direction,
                buff=0,
                color=BLUE_C,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )

            rough_incoming.add(incoming)
            rough_reflected.add(outgoing)

        self.play(
            LaggedStart(
                *[
                    GrowArrow(ray)
                    for ray in rough_incoming
                ],
                lag_ratio=0.15
            )
        )

        self.play(
            LaggedStart(
                *[
                    GrowArrow(ray)
                    for ray in rough_reflected
                ],
                lag_ratio=0.15
            )
        )

        specular_text = Text(
            "Regular reflection",
            font_size=24,
            color=GREEN_C
        ).next_to(
            smooth_surface,
            DOWN,
            buff=0.4
        )

        diffuse_text = Text(
            "Diffuse reflection",
            font_size=24,
            color=RED_C
        ).next_to(
            rough_surface,
            DOWN,
            buff=0.4
        )

        self.play(
            FadeIn(specular_text),
            FadeIn(diffuse_text)
        )

        self.wait(3)

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "Reflection"
    }):
        Reflection().render()
# =========================================================
# scene 3 refraction
# =========================================================

# =========================================================
# SCENE 3 — REFRACTION
# =========================================================

class Refraction(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Refraction of Light",
            font_size=50
        ).to_edge(UP)

        self.play(Write(title))

        # -------------------------------------------------
        # Interface between air and water
        # -------------------------------------------------

        boundary = Line(
            LEFT * 6,
            RIGHT * 6,
            color=WHITE,
            stroke_width=4
        )

        water = Rectangle(
            width=12,
            height=3.5,
            fill_color=BLUE_E,
            fill_opacity=0.35,
            stroke_width=0
        ).next_to(
            boundary,
            DOWN,
            buff=0
        )

        air_label = Text(
            "Air",
            font_size=30
        ).move_to(
            UP * 2.2 + LEFT * 5
        )

        water_label = Text(
            "Water",
            font_size=30,
            color=BLUE_B
        ).move_to(
            DOWN * 2.2 + LEFT * 5
        )

        self.play(
            FadeIn(water),
            Create(boundary),
            FadeIn(air_label),
            FadeIn(water_label)
        )

        # -------------------------------------------------
        # Point of incidence and normal
        # -------------------------------------------------

        incidence_point = ORIGIN

        normal = DashedLine(
            DOWN * 3,
            UP * 3,
            color=GREY_B,
            stroke_width=3
        )

        normal_label = Text(
            "Normal",
            font_size=24,
            color=GREY_A
        ).next_to(
            normal.get_top(),
            RIGHT,
            buff=0.2
        )

        self.play(
            Create(normal),
            FadeIn(normal_label)
        )

        # -------------------------------------------------
        # Incident ray
        # -------------------------------------------------

        incident_start = LEFT * 4 + UP * 2.7

        incident_ray = Arrow(
            incident_start,
            incidence_point,
            buff=0,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.08
        )

        incident_label = Text(
            "Incident ray",
            font_size=26,
            color=YELLOW
        ).next_to(
            incident_ray,
            LEFT,
            buff=0.2
        )

        self.play(
            GrowArrow(incident_ray),
            FadeIn(incident_label)
        )

        # -------------------------------------------------
        # Refracted ray
        # Bends toward the normal in water
        # -------------------------------------------------

        refracted_end = RIGHT * 1.8 + DOWN * 3

        refracted_ray = Arrow(
            incidence_point,
            refracted_end,
            buff=0,
            color=BLUE_C,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.08
        )

        refracted_label = Text(
            "Refracted ray",
            font_size=26,
            color=BLUE_C
        ).next_to(
            refracted_ray,
            RIGHT,
            buff=0.25
        )

        self.play(
            GrowArrow(refracted_ray),
            FadeIn(refracted_label)
        )

        # -------------------------------------------------
        # Angle labels
        # -------------------------------------------------

        theta_1 = MathTex(
            r"\theta_1",
            color=YELLOW,
            font_size=38
        ).move_to(
            LEFT * 0.7 + UP * 0.8
        )

        theta_2 = MathTex(
            r"\theta_2",
            color=BLUE_C,
            font_size=38
        ).move_to(
            RIGHT * 0.45 + DOWN * 0.9
        )

        self.play(
            Write(theta_1),
            Write(theta_2)
        )

        self.wait(1)

        # -------------------------------------------------
        # Show bending toward normal
        # -------------------------------------------------

        toward_normal = Text(
            "Light bends toward the normal",
            font_size=32,
            color=BLUE_B
        ).to_edge(DOWN)

        self.play(
            FadeIn(toward_normal)
        )

        self.wait(2)

        self.play(
            FadeOut(toward_normal)
        )

        # -------------------------------------------------
        # Refractive index
        # -------------------------------------------------

        refractive_index = MathTex(
            r"n=\frac{c}{v}",
            font_size=52
        ).to_corner(
            DR,
            buff=0.6
        )

        self.play(
            Write(refractive_index)
        )

        self.wait(2)

        # -------------------------------------------------
        # Snell's law
        # -------------------------------------------------

        snell = MathTex(
            r"n_1\sin\theta_1"
            r"="
            r"n_2\sin\theta_2",
            font_size=46
        ).to_corner(
            DL,
            buff=0.6
        )

        self.play(
            Write(snell)
        )

        self.wait(2)

        # -------------------------------------------------
        # Frequency / speed / wavelength
        # -------------------------------------------------

        self.play(
            FadeOut(
                incident_label,
                refracted_label,
                theta_1,
                theta_2,
                normal_label,
                refractive_index,
                snell
            )
        )

        physics_box = RoundedRectangle(
            width=6.6,
            height=2.2,
            corner_radius=0.2,
            color=GREY_B
        ).shift(RIGHT * 3 + UP * 1.8)

        frequency = MathTex(
            r"f=\text{constant}",
            font_size=38,
            color=GREEN_C
        )

        speed = MathTex(
            r"v\ \text{changes}",
            font_size=38,
            color=YELLOW
        )

        wavelength = MathTex(
            r"\lambda\ \text{changes}",
            font_size=38,
            color=BLUE_C
        )

        quantities = VGroup(
            frequency,
            speed,
            wavelength
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.25
        )

        quantities.move_to(physics_box)

        self.play(
            Create(physics_box)
        )

        self.play(
            LaggedStart(
                Write(frequency),
                Write(speed),
                Write(wavelength),
                lag_ratio=0.4
            )
        )

        self.wait(3)




if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "Refraction"
    }):
        Refraction().render()


# =========================================================
# SCENE 4 — FISH UNDER WATER / APPARENT DEPTH
# =========================================================

class FishRefraction(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Why Does a Fish Look Closer to the Surface?",
            font_size=46
        ).to_edge(UP)

        self.play(Write(title))

        # -------------------------------------------------
        # Water surface
        # -------------------------------------------------

        surface_y = 0.4

        surface = Line(
            LEFT * 6,
            RIGHT * 6,
            color=WHITE,
            stroke_width=4
        ).move_to([0, surface_y, 0])

        water = Rectangle(
            width=12,
            height=3.7,
            fill_color=BLUE_E,
            fill_opacity=0.32,
            stroke_width=0
        )

        water.next_to(
            surface,
            DOWN,
            buff=0
        )

        air_label = Text(
            "Air",
            font_size=28
        ).move_to(
            LEFT * 5 + UP * 2
        )

        water_label = Text(
            "Water",
            font_size=28,
            color=BLUE_B
        ).move_to(
            LEFT * 5 + DOWN * 2
        )

        self.play(
            FadeIn(water),
            Create(surface),
            FadeIn(air_label),
            FadeIn(water_label)
        )

        # -------------------------------------------------
        # Real fish
        # -------------------------------------------------

        fish_body = Ellipse(
            width=1.5,
            height=0.75,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        )

        fish_tail = Polygon(
            [-0.75, 0, 0],
            [-1.35, 0.5, 0],
            [-1.35, -0.5, 0],
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_color=WHITE
        )

        fish_eye = Dot(
            radius=0.06,
            color=BLACK
        ).move_to(
            [0.45, 0.12, 0]
        )

        real_fish = VGroup(
            fish_body,
            fish_tail,
            fish_eye
        )

        real_fish.scale(0.75)
        real_fish.move_to(
            LEFT * 2.8 + DOWN * 2.2
        )

        real_label = Text(
            "Real position",
            font_size=25,
            color=ORANGE
        ).next_to(
            real_fish,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(real_fish),
            FadeIn(real_label)
        )

        # -------------------------------------------------
        # Observer / eye
        # -------------------------------------------------

        eye_center = np.array([4.2, 2.3, 0])

        eye_outline = Ellipse(
            width=1.1,
            height=0.55,
            color=WHITE,
            stroke_width=3
        ).move_to(eye_center)

        pupil = Dot(
            eye_center,
            radius=0.11,
            color=BLUE_C
        )

        eye = VGroup(
            eye_outline,
            pupil
        )

        observer_label = Text(
            "Observer",
            font_size=25
        ).next_to(
            eye,
            UP,
            buff=0.2
        )

        self.play(
            FadeIn(eye),
            FadeIn(observer_label)
        )

        # -------------------------------------------------
        # Two points where rays leave the water
        # -------------------------------------------------

        point1 = np.array([0.1, surface_y, 0])
        point2 = np.array([1.3, surface_y, 0])

        # -------------------------------------------------
        # Rays inside water
        # -------------------------------------------------

        fish_source = real_fish.get_center() + RIGHT * 0.45

        water_ray_1 = Line(
            fish_source,
            point1,
            color=YELLOW,
            stroke_width=5
        )

        water_ray_2 = Line(
            fish_source,
            point2,
            color=YELLOW,
            stroke_width=5
        )

        self.play(
            Create(water_ray_1),
            Create(water_ray_2)
        )

        # -------------------------------------------------
        # Refracted rays in air
        # -------------------------------------------------

        air_ray_1 = Arrow(
            point1,
            eye_center,
            buff=0.15,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        air_ray_2 = Arrow(
            point2,
            eye_center,
            buff=0.15,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        self.play(
            GrowArrow(air_ray_1),
            GrowArrow(air_ray_2)
        )

        # -------------------------------------------------
        # Normals
        # -------------------------------------------------

        normal1 = DashedLine(
            point1 + DOWN * 0.9,
            point1 + UP * 0.9,
            color=GREY_B,
            stroke_width=2
        )

        normal2 = DashedLine(
            point2 + DOWN * 0.9,
            point2 + UP * 0.9,
            color=GREY_B,
            stroke_width=2
        )

        self.play(
            Create(normal1),
            Create(normal2)
        )

        self.wait(1)

        # -------------------------------------------------
        # Backward extensions
        # These show where the eye thinks the rays came from
        # -------------------------------------------------

        apparent_point = np.array(
            [-1.2, -1.05, 0]
        )

        extension1 = DashedLine(
            point1,
            apparent_point,
            color=BLUE_C,
            stroke_width=3
        )

        extension2 = DashedLine(
            point2,
            apparent_point,
            color=BLUE_C,
            stroke_width=3
        )

        self.play(
            Create(extension1),
            Create(extension2)
        )

        # -------------------------------------------------
        # Apparent fish
        # -------------------------------------------------

        apparent_fish = real_fish.copy()

        apparent_fish.scale(0.82)

        apparent_fish.move_to(
            apparent_point + LEFT * 0.5
        )

        apparent_fish.set_opacity(0.45)

        apparent_label = Text(
            "Apparent position",
            font_size=25,
            color=BLUE_C
        ).next_to(
            apparent_fish,
            UP,
            buff=0.2
        )

        self.play(
            FadeIn(apparent_fish),
            FadeIn(apparent_label)
        )

        self.wait(2)

        # -------------------------------------------------
        # Explanation
        # -------------------------------------------------

        explanation = Text(
            "The fish appears shallower than it really is",
            font_size=32,
            color=BLUE_B
        ).to_edge(DOWN)

        self.play(
            Write(explanation)
        )

        self.wait(3)

        # -------------------------------------------------
        # Depth comparison
        # -------------------------------------------------

        real_depth_line = DoubleArrow(
            [-4.5, surface_y, 0],
            [-4.5, real_fish.get_center()[1], 0],
            color=ORANGE,
            stroke_width=3
        )

        apparent_depth_line = DoubleArrow(
            [-3.8, surface_y, 0],
            [-3.8, apparent_fish.get_center()[1], 0],
            color=BLUE_C,
            stroke_width=3
        )

        real_depth_text = Text(
            "Real depth",
            font_size=22,
            color=ORANGE
        ).next_to(
            real_depth_line,
            LEFT,
            buff=0.15
        )

        apparent_depth_text = Text(
            "Apparent depth",
            font_size=22,
            color=BLUE_C
        ).next_to(
            apparent_depth_line,
            RIGHT,
            buff=0.15
        )

        self.play(
            GrowFromCenter(real_depth_line),
            GrowFromCenter(apparent_depth_line),
            FadeIn(real_depth_text),
            FadeIn(apparent_depth_text)
        )

        self.wait(3)


# =========================================================
# RENDER SCENE 4
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "FishRefraction"
    }):
        FishRefraction().render()


# =========================================================
# SCENE 5 — TOTAL INTERNAL REFLECTION
# =========================================================

class TotalInternalReflection(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Total Internal Reflection",
            font_size=50
        ).to_edge(UP)

        self.play(Write(title))

        # -------------------------------------------------
        # Boundary between water and air
        # -------------------------------------------------

        boundary = Line(
            LEFT * 6,
            RIGHT * 6,
            color=WHITE,
            stroke_width=4
        )

        water = Rectangle(
            width=12,
            height=3.5,
            fill_color=BLUE_E,
            fill_opacity=0.35,
            stroke_width=0
        ).next_to(
            boundary,
            DOWN,
            buff=0
        )

        air_label = Text(
            "Air",
            font_size=28
        ).move_to(
            LEFT * 5 + UP * 2
        )

        water_label = Text(
            "Water",
            font_size=28,
            color=BLUE_B
        ).move_to(
            LEFT * 5 + DOWN * 2
        )

        self.play(
            FadeIn(water),
            Create(boundary),
            FadeIn(air_label),
            FadeIn(water_label)
        )

        # -------------------------------------------------
        # Normal
        # -------------------------------------------------

        incidence_point = ORIGIN

        normal = DashedLine(
            DOWN * 3,
            UP * 3,
            color=GREY_B,
            stroke_width=3
        )

        self.play(Create(normal))

        # -------------------------------------------------
        # CASE 1 — Small incident angle
        # -------------------------------------------------

        case1_text = Text(
            "1. Small incident angle",
            font_size=30,
            color=GREEN_C
        ).to_corner(UL, buff=0.7)

        self.play(FadeIn(case1_text))

        ray1_start = LEFT * 2.2 + DOWN * 2.7

        ray1_incident = Arrow(
            ray1_start,
            incidence_point,
            buff=0,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        ray1_refracted = Arrow(
            incidence_point,
            RIGHT * 3.3 + UP * 2.4,
            buff=0,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        self.play(
            GrowArrow(ray1_incident)
        )

        self.play(
            GrowArrow(ray1_refracted)
        )

        refraction_label = Text(
            "Light exits the water",
            font_size=28,
            color=GREEN_C
        ).to_edge(DOWN)

        self.play(FadeIn(refraction_label))
        self.wait(2)

        self.play(
            FadeOut(
                ray1_incident,
                ray1_refracted,
                refraction_label,
                case1_text
            )
        )

        # -------------------------------------------------
        # CASE 2 — Critical angle
        # -------------------------------------------------

        case2_text = Text(
            "2. Critical angle",
            font_size=30,
            color=YELLOW
        ).to_corner(UL, buff=0.7)

        self.play(FadeIn(case2_text))

        ray2_start = LEFT * 4.2 + DOWN * 2.3

        ray2_incident = Arrow(
            ray2_start,
            incidence_point,
            buff=0,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        # At the critical angle, refracted ray travels along the boundary
        critical_ray = Arrow(
            incidence_point,
            RIGHT * 5,
            buff=0,
            color=ORANGE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        self.play(
            GrowArrow(ray2_incident)
        )

        self.play(
            GrowArrow(critical_ray)
        )

        critical_label = MathTex(
            r"\theta_i = \theta_c",
            font_size=42,
            color=ORANGE
        ).move_to(
            RIGHT * 3 + UP * 0.7
        )

        along_surface = Text(
            "The refracted ray travels along the surface",
            font_size=28,
            color=ORANGE
        ).to_edge(DOWN)

        self.play(
            Write(critical_label),
            FadeIn(along_surface)
        )

        self.wait(2)

        self.play(
            FadeOut(
                ray2_incident,
                critical_ray,
                critical_label,
                along_surface,
                case2_text
            )
        )

        # -------------------------------------------------
        # CASE 3 — Beyond critical angle
        # -------------------------------------------------

        case3_text = Text(
            "3. Incident angle greater than the critical angle",
            font_size=30,
            color=RED_C
        ).to_corner(UL, buff=0.7)

        self.play(FadeIn(case3_text))

        ray3_start = LEFT * 4.8 + DOWN * 1.7

        ray3_incident = Arrow(
            ray3_start,
            incidence_point,
            buff=0,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        reflected_end = RIGHT * 4.8 + DOWN * 1.7

        reflected_ray = Arrow(
            incidence_point,
            reflected_end,
            buff=0,
            color=BLUE_C,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        self.play(
            GrowArrow(ray3_incident)
        )

        self.play(
            GrowArrow(reflected_ray)
        )

        tir_label = Text(
            "Total Internal Reflection",
            font_size=34,
            color=BLUE_C
        ).to_edge(DOWN)

        self.play(
            Write(tir_label)
        )

        self.wait(2)

        # -------------------------------------------------
        # Critical angle equation
        # -------------------------------------------------

        critical_equation = MathTex(
            r"\sin\theta_c = \frac{n_2}{n_1}",
            font_size=48
        ).to_corner(DR, buff=0.6)

        condition = MathTex(
            r"n_1 > n_2",
            font_size=40,
            color=YELLOW
        ).next_to(
            critical_equation,
            UP,
            buff=0.3
        )

        self.play(
            Write(condition),
            Write(critical_equation)
        )

        self.wait(3)

        # -------------------------------------------------
        # Optical fiber illustration
        # -------------------------------------------------

        self.play(
            FadeOut(
                boundary,
                water,
                air_label,
                water_label,
                normal,
                ray3_incident,
                reflected_ray,
                tir_label,
                critical_equation,
                condition,
                case3_text
            )
        )

        fiber_title = Text(
            "Application: Optical Fiber",
            font_size=42
        ).to_edge(UP)

        self.play(
            Transform(title, fiber_title)
        )

        # Fiber body
        fiber_top = Line(
            LEFT * 5,
            RIGHT * 5,
            color=BLUE_B,
            stroke_width=6
        ).shift(UP * 1.2)

        fiber_bottom = Line(
            LEFT * 5,
            RIGHT * 5,
            color=BLUE_B,
            stroke_width=6
        ).shift(DOWN * 1.2)

        self.play(
            Create(fiber_top),
            Create(fiber_bottom)
        )

        # Zig-zag light path
        points = [
            [-5, 0, 0],
            [-3.5, 1.2, 0],
            [-2.0, -1.2, 0],
            [-0.5, 1.2, 0],
            [1.0, -1.2, 0],
            [2.5, 1.2, 0],
            [4.0, -1.2, 0],
            [5.0, -0.3, 0]
        ]

        light_path = VMobject()
        light_path.set_points_as_corners(points)
        light_path.set_stroke(
            color=YELLOW,
            width=6
        )

        self.play(
            Create(light_path),
            run_time=4
        )

        fiber_text = Text(
            "Light remains trapped inside by repeated total internal reflection",
            font_size=29,
            color=YELLOW
        ).to_edge(DOWN)

        self.play(
            FadeIn(fiber_text)
        )

        self.wait(3)


# =========================================================
# RENDER SCENE 5
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "TotalInternalReflection"
    }):
        TotalInternalReflection().render()


# =========================================================
# SCENE 6 — PRISM AND DISPERSION
# =========================================================

class PrismDispersion(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Dispersion of White Light",
            font_size=50
        ).to_edge(UP)

        self.play(Write(title))

        # -------------------------------------------------
        # Prism
        # -------------------------------------------------

        prism = Polygon(
            LEFT * 1.8 + DOWN * 2.2,
            RIGHT * 1.8 + DOWN * 2.2,
            UP * 2.3,
            stroke_color=BLUE_B,
            stroke_width=4,
            fill_color=BLUE_E,
            fill_opacity=0.22
        ).shift(RIGHT * 0.4)

        self.play(
            Create(prism),
            run_time=1.5
        )

        prism_label = Text(
            "Glass prism",
            font_size=26,
            color=BLUE_B
        ).next_to(
            prism,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(prism_label)
        )

        # -------------------------------------------------
        # Incoming white light
        # -------------------------------------------------

        incoming_start = LEFT * 6 + UP * 0.5
        prism_entry = LEFT * 1.4 + UP * 0.2

        white_ray = Arrow(
            incoming_start,
            prism_entry,
            buff=0,
            color=WHITE,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.06
        )

        white_label = Text(
            "White light",
            font_size=28,
            color=WHITE
        ).next_to(
            white_ray,
            UP,
            buff=0.25
        )

        self.play(
            GrowArrow(white_ray),
            FadeIn(white_label)
        )

        self.wait(1)

        # -------------------------------------------------
        # Internal ray through prism
        # -------------------------------------------------

        internal_start = prism_entry
        internal_end = RIGHT * 1.0 + DOWN * 0.2

        internal_ray = Line(
            internal_start,
            internal_end,
            color=WHITE,
            stroke_width=6
        )

        self.play(
            Create(internal_ray)
        )

        self.wait(1)

        # -------------------------------------------------
        # Emerging colors
        # -------------------------------------------------

        exit_point = internal_end

        ray_data = [
            (RED,     RIGHT * 5 + UP * 1.0),
            (ORANGE,  RIGHT * 5 + UP * 0.6),
            (YELLOW,  RIGHT * 5 + UP * 0.2),
            (GREEN,   RIGHT * 5 + DOWN * 0.2),
            (BLUE,    RIGHT * 5 + DOWN * 0.7),
            (PURPLE,  RIGHT * 5 + DOWN * 1.2)
        ]

        color_rays = VGroup()

        for color, end_point in ray_data:
            ray = Line(
                exit_point,
                end_point,
                color=color,
                stroke_width=6
            )
            color_rays.add(ray)

        self.play(
            LaggedStart(
                *[
                    Create(ray)
                    for ray in color_rays
                ],
                lag_ratio=0.15
            ),
            run_time=2.5
        )

        # -------------------------------------------------
        # Labels
        # -------------------------------------------------

        red_label = Text(
            "Red",
            font_size=24,
            color=RED
        ).next_to(
            color_rays[0].get_end(),
            RIGHT,
            buff=0.15
        )

        violet_label = Text(
            "Violet",
            font_size=24,
            color=PURPLE
        ).next_to(
            color_rays[-1].get_end(),
            RIGHT,
            buff=0.15
        )

        self.play(
            FadeIn(red_label),
            FadeIn(violet_label)
        )

        # -------------------------------------------------
        # Explanation arrows
        # -------------------------------------------------

        red_note = Text(
            "Longer wavelength\nsmaller deviation",
            font_size=24,
            color=RED
        ).move_to(
            RIGHT * 3.2 + UP * 2.3
        )

        violet_note = Text(
            "Shorter wavelength\nlarger deviation",
            font_size=24,
            color=PURPLE
        ).move_to(
            RIGHT * 3.2 + DOWN * 2.4
        )

        self.play(
            FadeIn(red_note),
            FadeIn(violet_note)
        )

        self.wait(2)

        # -------------------------------------------------
        # Dispersion label
        # -------------------------------------------------

        dispersion = Text(
            "Different wavelengths refract by different amounts",
            font_size=30,
            color=YELLOW
        ).to_edge(DOWN)

        self.play(
            Write(dispersion)
        )

        self.wait(3)

        # -------------------------------------------------
        # Optional rainbow connection
        # -------------------------------------------------

        self.play(
            FadeOut(
                white_label,
                red_note,
                violet_note,
                dispersion,
                red_label,
                violet_label
            )
        )

        rainbow_title = Text(
            "The same principle contributes to rainbow formation",
            font_size=34,
            color=WHITE
        ).to_edge(DOWN)

        self.play(
            FadeIn(rainbow_title)
        )

        self.wait(3)


# =========================================================
# RENDER SCENE 6
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "PrismDispersion"
    }):
        PrismDispersion().render()



# =========================================================
# SCENE 7 — POLARIZATION
# =========================================================

class Polarization(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Polarization of Light",
            font_size=50
        ).to_edge(UP)

        self.play(Write(title))

        # -------------------------------------------------
        # Incoming light representation
        # -------------------------------------------------

        beam_axis = Line(
            LEFT * 5,
            RIGHT * 5,
            color=GREY_B,
            stroke_width=2
        )

        self.play(Create(beam_axis))

        source_label = Text(
            "Unpolarized light",
            font_size=28
        ).move_to(LEFT * 4 + UP * 2.2)

        self.play(FadeIn(source_label))

        # Several oscillation directions
        directions = [
            UP,
            DOWN,
            UP + RIGHT,
            UP + LEFT,
            DOWN + RIGHT,
            DOWN + LEFT
        ]

        waves = VGroup()

        x_positions = [-4.2, -3.6, -3.0]

        for x in x_positions:
            for direction in directions:
                line = Line(
                    [x, 0, 0],
                    [x, 0, 0] + direction * 0.45,
                    color=YELLOW,
                    stroke_width=3
                )
                waves.add(line)

        self.play(
            LaggedStart(
                *[Create(w) for w in waves],
                lag_ratio=0.03
            )
        )

        # -------------------------------------------------
        # Polarizer
        # -------------------------------------------------

        polarizer = Rectangle(
            width=0.7,
            height=4.5,
            stroke_color=BLUE_B,
            stroke_width=4,
            fill_color=BLUE_E,
            fill_opacity=0.22
        ).move_to(ORIGIN)

        polarizer_label = Text(
            "Polarizing filter",
            font_size=28,
            color=BLUE_B
        ).next_to(
            polarizer,
            DOWN,
            buff=0.3
        )

        self.play(
            Create(polarizer),
            FadeIn(polarizer_label)
        )

        # Transmission axis
        axis = DoubleArrow(
            DOWN * 1.6,
            UP * 1.6,
            buff=0,
            color=GREEN_C,
            stroke_width=4
        ).move_to(ORIGIN)

        axis_label = Text(
            "Transmission axis",
            font_size=24,
            color=GREEN_C
        ).next_to(
            polarizer,
            UP,
            buff=0.25
        )

        self.play(
            GrowFromCenter(axis),
            FadeIn(axis_label)
        )

        # -------------------------------------------------
        # Polarized light after filter
        # -------------------------------------------------

        polarized_label = Text(
            "Polarized light",
            font_size=28,
            color=GREEN_C
        ).move_to(RIGHT * 3.7 + UP * 2.2)

        self.play(FadeIn(polarized_label))

        vertical_oscillations = VGroup()

        for x in [1.2, 2.2, 3.2, 4.2]:
            line = Line(
                [x, -0.7, 0],
                [x, 0.7, 0],
                color=GREEN_C,
                stroke_width=5
            )
            vertical_oscillations.add(line)

        self.play(
            LaggedStart(
                *[
                    GrowFromCenter(line)
                    for line in vertical_oscillations
                ],
                lag_ratio=0.2
            )
        )

        self.wait(2)

        # -------------------------------------------------
        # Second polarizer at 45 degrees
        # -------------------------------------------------

        self.play(
            FadeOut(
                waves,
                source_label
            )
        )

        second_filter = Rectangle(
            width=0.7,
            height=4.2,
            stroke_color=PURPLE_B,
            stroke_width=4,
            fill_color=PURPLE_E,
            fill_opacity=0.22
        ).move_to(RIGHT * 2.2)

        second_axis = DoubleArrow(
            DOWN * 1.5,
            UP * 1.5,
            buff=0,
            color=PURPLE_B,
            stroke_width=4
        ).rotate(
            45 * DEGREES
        ).move_to(
            RIGHT * 2.2
        )

        second_label = Text(
            "Second polarizer: 45°",
            font_size=26,
            color=PURPLE_B
        ).next_to(
            second_filter,
            DOWN,
            buff=0.3
        )

        self.play(
            Create(second_filter),
            GrowFromCenter(second_axis),
            FadeIn(second_label)
        )

        malus = MathTex(
            r"I = I_0 \cos^2\theta",
            font_size=48
        ).to_corner(
            DR,
            buff=0.6
        )

        self.play(
            Write(malus)
        )

        reduced_text = Text(
            "Only part of the intensity is transmitted",
            font_size=30,
            color=YELLOW
        ).to_edge(DOWN)

        self.play(
            FadeIn(reduced_text)
        )

        self.wait(3)

        # -------------------------------------------------
        # Crossed polarizers
        # -------------------------------------------------

        self.play(
            FadeOut(
                second_label,
                reduced_text,
                malus
            )
        )

        self.play(
            second_axis.animate.rotate(45 * DEGREES)
        )

        blocked_label = Text(
            "At 90° the transmitted intensity ideally becomes zero",
            font_size=29,
            color=RED_C
        ).to_edge(DOWN)

        zero_equation = MathTex(
            r"I = I_0 \cos^2 90^\circ = 0",
            font_size=44,
            color=RED_C
        ).to_corner(
            DR,
            buff=0.6
        )

        self.play(
            FadeIn(blocked_label),
            Write(zero_equation)
        )

        self.wait(3)

        # -------------------------------------------------
        # Everyday application
        # -------------------------------------------------

        self.play(
            FadeOut(
                second_filter,
                second_axis,
                zero_equation,
                blocked_label,
                vertical_oscillations,
                polarized_label,
                polarizer_label,
                axis_label,
                axis,
                polarizer,
                beam_axis
            )
        )

        application = Text(
            "Application: Polarized Sunglasses",
            font_size=42
        ).move_to(ORIGIN)

        glare = Text(
            "They reduce glare from reflected light",
            font_size=30,
            color=BLUE_B
        ).next_to(
            application,
            DOWN,
            buff=0.5
        )

        self.play(
            Write(application),
            FadeIn(glare)
        )

        self.wait(3)


# =========================================================
# RENDER SCENE 7
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "Polarization"
    }):
        Polarization().render()





# =========================================================
# SCENE 8 — DIFFRACTION
# =========================================================

class Diffraction(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Diffraction of Light",
            font_size=50
        ).to_edge(UP)

        self.play(Write(title))

        # -------------------------------------------------
        # Incoming wavefronts
        # -------------------------------------------------

        incoming_waves = VGroup()

        for x in [-5.5, -4.7, -3.9, -3.1]:
            wavefront = Line(
                [x, -2.3, 0],
                [x, 2.3, 0],
                color=YELLOW,
                stroke_width=4
            )
            incoming_waves.add(wavefront)

        self.play(
            LaggedStart(
                *[
                    Create(wave)
                    for wave in incoming_waves
                ],
                lag_ratio=0.15
            )
        )

        incoming_label = Text(
            "Incoming light",
            font_size=28,
            color=YELLOW
        ).move_to(
            LEFT * 4.4 + UP * 2.8
        )

        self.play(
            FadeIn(incoming_label)
        )

        # -------------------------------------------------
        # Barrier with narrow slit
        # -------------------------------------------------

        upper_barrier = Rectangle(
            width=0.45,
            height=2.7,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_color=GREY_A
        ).move_to(
            [0, 2.1, 0]
        )

        lower_barrier = Rectangle(
            width=0.45,
            height=2.7,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_color=GREY_A
        ).move_to(
            [0, -2.1, 0]
        )

        self.play(
            FadeIn(upper_barrier),
            FadeIn(lower_barrier)
        )

        slit_label = Text(
            "Narrow slit",
            font_size=26
        ).move_to(
            [0.9, 0, 0]
        )

        self.play(
            FadeIn(slit_label)
        )

        # -------------------------------------------------
        # Diffracted wavefronts
        # -------------------------------------------------

        center = np.array([0.25, 0, 0])

        arcs = VGroup()

        for radius in [0.8, 1.5, 2.2, 2.9, 3.6]:

            arc = Arc(
                radius=radius,
                start_angle=-PI / 2,
                angle=PI,
                arc_center=center,
                color=BLUE_C,
                stroke_width=4
            )

            arcs.add(arc)

        self.play(
            LaggedStart(
                *[
                    Create(arc)
                    for arc in arcs
                ],
                lag_ratio=0.15
            ),
            run_time=3
        )

        diffraction_label = Text(
            "The wave spreads after passing through the slit",
            font_size=31,
            color=BLUE_C
        ).to_edge(DOWN)

        self.play(
            FadeIn(diffraction_label)
        )

        self.wait(3)

        # -------------------------------------------------
        # Compare wide slit and narrow slit
        # -------------------------------------------------

        self.play(
            FadeOut(
                incoming_waves,
                incoming_label,
                upper_barrier,
                lower_barrier,
                slit_label,
                arcs,
                diffraction_label
            )
        )

        comparison_title = Text(
            "Diffraction Depends on Slit Width",
            font_size=42
        ).to_edge(UP)

        self.play(
            Transform(title, comparison_title)
        )

        # -------------------------------------------------
        # Left side — wide slit
        # -------------------------------------------------

        wide_label = Text(
            "Wide slit",
            font_size=30,
            color=GREEN_C
        ).move_to(
            LEFT * 3.3 + UP * 2.4
        )

        wide_top = Rectangle(
            width=0.35,
            height=1.7,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0
        ).move_to(
            LEFT * 3.2 + UP * 1.8
        )

        wide_bottom = Rectangle(
            width=0.35,
            height=1.7,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0
        ).move_to(
            LEFT * 3.2 + DOWN * 1.8
        )

        self.play(
            FadeIn(wide_label),
            FadeIn(wide_top),
            FadeIn(wide_bottom)
        )

        wide_center = np.array([-3.0, 0, 0])

        wide_rays = VGroup(
            Line(
                wide_center,
                wide_center + RIGHT * 3 + UP * 0.5,
                color=GREEN_C,
                stroke_width=4
            ),
            Line(
                wide_center,
                wide_center + RIGHT * 3,
                color=GREEN_C,
                stroke_width=4
            ),
            Line(
                wide_center,
                wide_center + RIGHT * 3 + DOWN * 0.5,
                color=GREEN_C,
                stroke_width=4
            )
        )

        self.play(
            LaggedStart(
                *[
                    Create(ray)
                    for ray in wide_rays
                ],
                lag_ratio=0.15
            )
        )

        small_diffraction = Text(
            "Small spreading",
            font_size=25,
            color=GREEN_C
        ).move_to(
            LEFT * 2.5 + DOWN * 3
        )

        self.play(
            FadeIn(small_diffraction)
        )

        # -------------------------------------------------
        # Right side — narrow slit
        # -------------------------------------------------

        narrow_label = Text(
            "Narrow slit",
            font_size=30,
            color=RED_C
        ).move_to(
            RIGHT * 3.3 + UP * 2.4
        )

        narrow_top = Rectangle(
            width=0.35,
            height=2.5,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0
        ).move_to(
            RIGHT * 3.2 + UP * 2.2
        )

        narrow_bottom = Rectangle(
            width=0.35,
            height=2.5,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0
        ).move_to(
            RIGHT * 3.2 + DOWN * 2.2
        )

        self.play(
            FadeIn(narrow_label),
            FadeIn(narrow_top),
            FadeIn(narrow_bottom)
        )

        narrow_center = np.array([3.4, 0, 0])

        narrow_arcs = VGroup()

        for radius in [0.7, 1.3, 1.9, 2.5]:

            arc = Arc(
                radius=radius,
                start_angle=-PI / 2,
                angle=PI,
                arc_center=narrow_center,
                color=RED_C,
                stroke_width=4
            )

            narrow_arcs.add(arc)

        self.play(
            LaggedStart(
                *[
                    Create(arc)
                    for arc in narrow_arcs
                ],
                lag_ratio=0.15
            )
        )

        strong_diffraction = Text(
            "Large spreading",
            font_size=25,
            color=RED_C
        ).move_to(
            RIGHT * 3.2 + DOWN * 3
        )

        self.play(
            FadeIn(strong_diffraction)
        )

        self.wait(3)

        # -------------------------------------------------
        # Wavelength relationship
        # -------------------------------------------------

        relation = MathTex(
            r"\text{Diffraction becomes important when } a \sim \lambda",
            font_size=40
        ).to_edge(DOWN)

        self.play(
            FadeOut(
                small_diffraction,
                strong_diffraction
            )
        )

        self.play(
            Write(relation)
        )

        self.wait(3)

        # -------------------------------------------------
        # Radio wave example
        # -------------------------------------------------

        self.play(
            FadeOut(
                wide_label,
                wide_top,
                wide_bottom,
                wide_rays,
                narrow_label,
                narrow_top,
                narrow_bottom,
                narrow_arcs,
                relation
            )
        )

        radio_title = Text(
            "Why Do Radio Waves Diffract More Easily?",
            font_size=39
        ).move_to(
            UP * 1.2
        )

        radio_text = Text(
            "Radio waves have much longer wavelengths than visible light",
            font_size=30,
            color=BLUE_B
        ).next_to(
            radio_title,
            DOWN,
            buff=0.6
        )

        building = Rectangle(
            width=2,
            height=3,
            fill_color=GREY_B,
            fill_opacity=0.8
        ).shift(DOWN * 1.5)

        radio_path = Arc(
            radius=3.3,
            start_angle=PI,
            angle=-PI / 2,
            color=YELLOW,
            stroke_width=6
        ).shift(
            LEFT * 0.3 + DOWN * 0.1
        )

        self.play(
            Write(radio_title),
            FadeIn(radio_text)
        )

        self.play(
            FadeIn(building),
            Create(radio_path),
            run_time=2
        )

        around_text = Text(
            "Longer wavelengths can bend around obstacles more noticeably",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN)

        self.play(
            FadeIn(around_text)
        )

        self.wait(3)


# =========================================================
# RENDER SCENE 8
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "Diffraction"
    }):
        Diffraction().render()


# =========================================================
# SCENE 9 — INTERFERENCE
# =========================================================

class Interference(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Interference of Light",
            font_size=50
        ).to_edge(UP)

        self.play(Write(title))

        # -------------------------------------------------
        # Intro text
        # -------------------------------------------------

        intro = Text(
            "When two waves overlap, their displacements add together",
            font_size=30
        ).shift(UP * 2.2)

        self.play(FadeIn(intro))

        # -------------------------------------------------
        # Axes for first demonstration
        # -------------------------------------------------

        axes1 = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-2.2, 2.2, 1],
            x_length=10,
            y_length=2.4,
            tips=False,
            axis_config={
                "stroke_color": GREY_B,
                "stroke_width": 2
            }
        ).shift(UP * 0.7)

        self.play(Create(axes1))

        # -------------------------------------------------
        # Constructive interference
        # -------------------------------------------------

        constructive_label = Text(
            "Constructive Interference",
            font_size=34,
            color=GREEN_C
        ).to_corner(UL, buff=0.6)

        self.play(FadeIn(constructive_label))

        wave1 = axes1.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=YELLOW,
            stroke_width=4
        )

        wave2 = axes1.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=BLUE_C,
            stroke_width=4
        )

        result = axes1.plot(
            lambda x: 2 * np.sin(x),
            x_range=[0, 2 * PI],
            color=GREEN_C,
            stroke_width=6
        )

        wave1.shift(UP * 0.15)
        wave2.shift(DOWN * 0.15)

        wave1_label = Text(
            "Wave 1",
            font_size=24,
            color=YELLOW
        ).move_to(LEFT * 4.5 + UP * 0.4)

        wave2_label = Text(
            "Wave 2",
            font_size=24,
            color=BLUE_C
        ).move_to(LEFT * 4.5 + DOWN * 0.4)

        self.play(
            Create(wave1),
            FadeIn(wave1_label)
        )

        self.play(
            Create(wave2),
            FadeIn(wave2_label)
        )

        self.wait(1)

        plus_sign = MathTex(
            "+",
            font_size=46
        ).move_to(LEFT * 5.4)

        self.play(Write(plus_sign))

        self.play(
            Transform(
                VGroup(wave1, wave2),
                result
            ),
            FadeOut(
                wave1_label,
                wave2_label,
                plus_sign
            ),
            run_time=2
        )

        constructive_text = Text(
            "Crest + Crest  →  Larger amplitude",
            font_size=30,
            color=GREEN_C
        ).to_edge(DOWN)

        self.play(FadeIn(constructive_text))

        self.wait(3)

        # -------------------------------------------------
        # Clear constructive section
        # -------------------------------------------------

        self.play(
            FadeOut(
                axes1,
                result,
                constructive_label,
                constructive_text,
                intro
            )
        )

        # -------------------------------------------------
        # Destructive interference
        # -------------------------------------------------

        destructive_label = Text(
            "Destructive Interference",
            font_size=34,
            color=RED_C
        ).to_corner(UL, buff=0.6)

        self.play(FadeIn(destructive_label))

        axes2 = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.6, 1.6, 0.5],
            x_length=10,
            y_length=2.4,
            tips=False,
            axis_config={
                "stroke_color": GREY_B,
                "stroke_width": 2
            }
        ).shift(UP * 0.7)

        self.play(Create(axes2))

        wave3 = axes2.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=YELLOW,
            stroke_width=4
        )

        wave4 = axes2.plot(
            lambda x: -np.sin(x),
            x_range=[0, 2 * PI],
            color=BLUE_C,
            stroke_width=4
        )

        zero_line = axes2.plot(
            lambda x: 0,
            x_range=[0, 2 * PI],
            color=RED_C,
            stroke_width=6
        )

        self.play(
            Create(wave3)
        )

        self.play(
            Create(wave4)
        )

        self.wait(1)

        self.play(
            Transform(
                VGroup(wave3, wave4),
                zero_line
            ),
            run_time=2
        )

        destructive_text = Text(
            "Crest + Trough  →  Cancellation",
            font_size=30,
            color=RED_C
        ).to_edge(DOWN)

        self.play(
            FadeIn(destructive_text)
        )

        self.wait(3)

        # -------------------------------------------------
        # Bright and dark regions
        # -------------------------------------------------

        self.play(
            FadeOut(
                axes2,
                zero_line,
                destructive_label,
                destructive_text
            )
        )

        pattern_title = Text(
            "Interference Produces Bright and Dark Regions",
            font_size=40
        ).to_edge(UP)

        self.play(
            Transform(title, pattern_title)
        )

        # Bright region
        bright = Rectangle(
            width=2.4,
            height=2.2,
            fill_color=YELLOW,
            fill_opacity=0.9,
            stroke_color=WHITE
        ).shift(LEFT * 3)

        bright_label = Text(
            "Constructive",
            font_size=28,
            color=GREEN_C
        ).next_to(
            bright,
            DOWN,
            buff=0.3
        )

        bright_equation = MathTex(
            r"\Delta \phi = 2\pi m",
            font_size=40,
            color=GREEN_C
        ).next_to(
            bright,
            UP,
            buff=0.3
        )

        # Dark region
        dark = Rectangle(
            width=2.4,
            height=2.2,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=WHITE
        ).shift(RIGHT * 3)

        dark_label = Text(
            "Destructive",
            font_size=28,
            color=RED_C
        ).next_to(
            dark,
            DOWN,
            buff=0.3
        )

        dark_equation = MathTex(
            r"\Delta \phi = (2m+1)\pi",
            font_size=40,
            color=RED_C
        ).next_to(
            dark,
            UP,
            buff=0.3
        )

        self.play(
            FadeIn(bright),
            FadeIn(dark)
        )

        self.play(
            FadeIn(bright_label),
            FadeIn(dark_label),
            Write(bright_equation),
            Write(dark_equation)
        )

        self.wait(3)

        # -------------------------------------------------
        # Final transition toward double slit
        # -------------------------------------------------

        next_text = Text(
            "This is the principle behind Young's double-slit experiment",
            font_size=31,
            color=BLUE_B
        ).to_edge(DOWN)

        self.play(
            FadeOut(
                bright_label,
                dark_label,
                bright_equation,
                dark_equation
            )
        )

        self.play(
            Write(next_text)
        )

        self.wait(3)


# =========================================================
# RENDER SCENE 9
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "Interference"
    }):
        Interference().render()


# =========================================================
# SCENE 10 — YOUNG'S DOUBLE-SLIT EXPERIMENT
# =========================================================

class DoubleSlit(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Young's Double-Slit Experiment",
            font_size=48
        ).to_edge(UP)

        self.play(Write(title))

        # -------------------------------------------------
        # Light source
        # -------------------------------------------------

        source = Dot(
            point=LEFT * 5.5,
            radius=0.13,
            color=YELLOW
        )

        source_glow = Circle(
            radius=0.35,
            color=YELLOW,
            stroke_opacity=0.4
        ).move_to(source)

        source_label = Text(
            "Light source",
            font_size=25,
            color=YELLOW
        ).next_to(
            source,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(source_glow),
            FadeIn(source),
            FadeIn(source_label)
        )

        # -------------------------------------------------
        # Incoming beam
        # -------------------------------------------------

        beam = Arrow(
            source.get_center(),
            LEFT * 1.7,
            buff=0.15,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.06
        )

        self.play(
            GrowArrow(beam)
        )

        # -------------------------------------------------
        # Double-slit barrier
        # -------------------------------------------------

        barrier_x = -1.4

        upper_barrier = Rectangle(
            width=0.35,
            height=2.15,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0
        ).move_to(
            [barrier_x, 2.15, 0]
        )

        middle_barrier = Rectangle(
            width=0.35,
            height=0.65,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0
        ).move_to(
            [barrier_x, 0, 0]
        )

        lower_barrier = Rectangle(
            width=0.35,
            height=2.15,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0
        ).move_to(
            [barrier_x, -2.15, 0]
        )

        slit1 = np.array([barrier_x, 0.72, 0])
        slit2 = np.array([barrier_x, -0.72, 0])

        slit1_label = MathTex(
            r"S_1",
            font_size=32,
            color=BLUE_C
        ).next_to(
            slit1,
            RIGHT,
            buff=0.25
        )

        slit2_label = MathTex(
            r"S_2",
            font_size=32,
            color=BLUE_C
        ).next_to(
            slit2,
            RIGHT,
            buff=0.25
        )

        self.play(
            FadeIn(upper_barrier),
            FadeIn(middle_barrier),
            FadeIn(lower_barrier)
        )

        self.play(
            Write(slit1_label),
            Write(slit2_label)
        )

        # -------------------------------------------------
        # Screen
        # -------------------------------------------------

        screen = Line(
            RIGHT * 5 + DOWN * 3,
            RIGHT * 5 + UP * 3,
            color=WHITE,
            stroke_width=7
        )

        screen_label = Text(
            "Screen",
            font_size=26
        ).next_to(
            screen,
            RIGHT,
            buff=0.2
        )

        self.play(
            Create(screen),
            FadeIn(screen_label)
        )

        # -------------------------------------------------
        # Waves spreading from slit 1
        # -------------------------------------------------

        wavefronts_1 = VGroup()

        for radius in [0.8, 1.5, 2.2, 2.9, 3.6, 4.3, 5.0, 5.7]:
            arc = Arc(
                radius=radius,
                start_angle=-PI / 2,
                angle=PI,
                arc_center=slit1,
                color=BLUE_C,
                stroke_width=2.5,
                stroke_opacity=0.65
            )

            wavefronts_1.add(arc)

        # -------------------------------------------------
        # Waves spreading from slit 2
        # -------------------------------------------------

        wavefronts_2 = VGroup()

        for radius in [0.8, 1.5, 2.2, 2.9, 3.6, 4.3, 5.0, 5.7]:
            arc = Arc(
                radius=radius,
                start_angle=-PI / 2,
                angle=PI,
                arc_center=slit2,
                color=GREEN_C,
                stroke_width=2.5,
                stroke_opacity=0.65
            )

            wavefronts_2.add(arc)

        self.play(
            LaggedStart(
                *[
                    Create(wave)
                    for wave in wavefronts_1
                ],
                lag_ratio=0.08
            ),
            run_time=2.5
        )

        self.play(
            LaggedStart(
                *[
                    Create(wave)
                    for wave in wavefronts_2
                ],
                lag_ratio=0.08
            ),
            run_time=2.5
        )

        # -------------------------------------------------
        # Interference regions
        # -------------------------------------------------

        interference_text = Text(
            "Waves from the two slits overlap and interfere",
            font_size=30,
            color=YELLOW
        ).to_edge(DOWN)

        self.play(
            FadeIn(interference_text)
        )

        self.wait(2)

        # -------------------------------------------------
        # Replace wavefronts with representative rays
        # -------------------------------------------------

        self.play(
            FadeOut(
                wavefronts_1,
                wavefronts_2,
                interference_text
            )
        )

        center_screen = np.array([5, 0, 0])

        upper_screen = np.array([5, 1.4, 0])
        lower_screen = np.array([5, -1.4, 0])

        center_ray_1 = Line(
            slit1,
            center_screen,
            color=BLUE_C,
            stroke_width=4
        )

        center_ray_2 = Line(
            slit2,
            center_screen,
            color=GREEN_C,
            stroke_width=4
        )

        upper_ray_1 = Line(
            slit1,
            upper_screen,
            color=BLUE_C,
            stroke_width=3
        )

        upper_ray_2 = Line(
            slit2,
            upper_screen,
            color=GREEN_C,
            stroke_width=3
        )

        lower_ray_1 = Line(
            slit1,
            lower_screen,
            color=BLUE_C,
            stroke_width=3
        )

        lower_ray_2 = Line(
            slit2,
            lower_screen,
            color=GREEN_C,
            stroke_width=3
        )

        self.play(
            Create(center_ray_1),
            Create(center_ray_2)
        )

        center_label = Text(
            "Constructive interference",
            font_size=25,
            color=YELLOW
        ).move_to(
            RIGHT * 2.6 + DOWN * 0.6
        )

        self.play(
            FadeIn(center_label)
        )

        self.wait(1)

        self.play(
            Create(upper_ray_1),
            Create(upper_ray_2),
            Create(lower_ray_1),
            Create(lower_ray_2)
        )

        # -------------------------------------------------
        # Interference pattern
        # -------------------------------------------------

        self.play(
            FadeOut(
                center_ray_1,
                center_ray_2,
                upper_ray_1,
                upper_ray_2,
                lower_ray_1,
                lower_ray_2,
                center_label
            )
        )

        # Bright and dark fringes positioned next to screen
        fringes = VGroup()

        fringe_positions = [
            (-2.5, 0.25),
            (-2.0, 0.55),
            (-1.5, 0.85),
            (-1.0, 1.15),
            (-0.5, 1.5),
            (0.0, 1.9),
            (0.5, 1.5),
            (1.0, 1.15),
            (1.5, 0.85),
            (2.0, 0.55),
            (2.5, 0.25)
        ]

        for y, opacity in fringe_positions:

            fringe = Rectangle(
                width=0.42,
                height=0.32,
                fill_color=YELLOW,
                fill_opacity=opacity,
                stroke_width=0
            )

            fringe.move_to(
                [4.7, y, 0]
            )

            fringes.add(fringe)

        self.play(
            LaggedStart(
                *[
                    FadeIn(fringe)
                    for fringe in fringes
                ],
                lag_ratio=0.08
            )
        )

        pattern_label = Text(
            "Interference pattern",
            font_size=29,
            color=YELLOW
        ).move_to(
            RIGHT * 2.7 + UP * 2.8
        )

        self.play(
            FadeIn(pattern_label)
        )

        # -------------------------------------------------
        # Bright and dark labels
        # -------------------------------------------------

        bright_arrow = Arrow(
            RIGHT * 3.3 + UP * 0.2,
            RIGHT * 4.5,
            buff=0.1,
            color=GREEN_C
        )

        bright_text = Text(
            "Bright fringe",
            font_size=25,
            color=GREEN_C
        ).next_to(
            bright_arrow,
            LEFT,
            buff=0.15
        )

        dark_arrow = Arrow(
            RIGHT * 3.3 + UP * 1,
            RIGHT * 4.5 + UP * 0.75,
            buff=0.1,
            color=RED_C
        )

        dark_text = Text(
            "Dark fringe",
            font_size=25,
            color=RED_C
        ).next_to(
            dark_arrow,
            LEFT,
            buff=0.15
        )

        self.play(
            GrowArrow(bright_arrow),
            FadeIn(bright_text)
        )

        self.play(
            GrowArrow(dark_arrow),
            FadeIn(dark_text)
        )

        self.wait(2)

        # -------------------------------------------------
        # Path difference equations
        # -------------------------------------------------

        constructive = MathTex(
            r"\Delta L = m\lambda",
            font_size=42,
            color=GREEN_C
        ).move_to(
            LEFT * 3.7 + DOWN * 2
        )

        destructive = MathTex(
            r"\Delta L = \left(m+\frac{1}{2}\right)\lambda",
            font_size=42,
            color=RED_C
        ).next_to(
            constructive,
            DOWN,
            buff=0.4
        )

        self.play(
            Write(constructive),
            Write(destructive)
        )

        self.wait(3)

        # -------------------------------------------------
        # Fringe spacing
        # -------------------------------------------------

        self.play(
            FadeOut(
                bright_arrow,
                bright_text,
                dark_arrow,
                dark_text,
                constructive,
                destructive
            )
        )

        spacing_equation = MathTex(
            r"\Delta y = \frac{\lambda L}{d}",
            font_size=52,
            color=BLUE_B
        ).move_to(
            LEFT * 3.4 + DOWN * 2.1
        )

        spacing_label = Text(
            "Fringe spacing",
            font_size=27,
            color=BLUE_B
        ).next_to(
            spacing_equation,
            UP,
            buff=0.25
        )

        self.play(
            FadeIn(spacing_label),
            Write(spacing_equation)
        )

        self.wait(3)

        # -------------------------------------------------
        # Conclusion
        # -------------------------------------------------

        conclusion = Text(
            "The interference pattern is evidence of the wave behavior of light",
            font_size=29,
            color=YELLOW
        ).to_edge(DOWN)

        self.play(
            FadeOut(
                spacing_label,
                spacing_equation
            )
        )

        self.play(
            Write(conclusion)
        )

        self.wait(3)


# =========================================================
# RENDER SCENE 10
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "DoubleSlit"
    }):
        DoubleSlit().render()


# =========================================================
# SCENE 11 — LIGHT INTERACTING WITH MATERIALS
# =========================================================

class LightMaterials(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "How Light Interacts with Materials",
            font_size=48
        ).to_edge(UP)

        self.play(Write(title))

        # -------------------------------------------------
        # Main idea: one incoming beam
        # -------------------------------------------------

        source = Dot(
            point=LEFT * 5.5,
            radius=0.12,
            color=YELLOW
        )

        source_label = Text(
            "Incoming light",
            font_size=26,
            color=YELLOW
        ).next_to(
            source,
            UP,
            buff=0.25
        )

        beam = Arrow(
            source.get_center(),
            LEFT * 1.5,
            buff=0.1,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.07
        )

        self.play(
            FadeIn(source),
            FadeIn(source_label),
            GrowArrow(beam)
        )

        # -------------------------------------------------
        # Material block
        # -------------------------------------------------

        material = Rectangle(
            width=1.5,
            height=3.5,
            fill_color=GREY_B,
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=3
        ).move_to(ORIGIN)

        material_label = Text(
            "Material",
            font_size=28
        ).next_to(
            material,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(material),
            FadeIn(material_label)
        )

        # -------------------------------------------------
        # Reflection
        # -------------------------------------------------

        reflected = Arrow(
            LEFT * 1.5,
            LEFT * 4 + UP * 2,
            buff=0,
            color=BLUE_C,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        reflected_label = Text(
            "Reflected",
            font_size=26,
            color=BLUE_C
        ).next_to(
            reflected,
            UP,
            buff=0.2
        )

        self.play(
            GrowArrow(reflected),
            FadeIn(reflected_label)
        )

        # -------------------------------------------------
        # Transmission
        # -------------------------------------------------

        transmitted = Arrow(
            RIGHT * 0.75,
            RIGHT * 4.8,
            buff=0,
            color=GREEN_C,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        transmitted_label = Text(
            "Transmitted",
            font_size=26,
            color=GREEN_C
        ).next_to(
            transmitted,
            UP,
            buff=0.2
        )

        self.play(
            GrowArrow(transmitted),
            FadeIn(transmitted_label)
        )

        # -------------------------------------------------
        # Absorption
        # -------------------------------------------------

        absorbed = Circle(
            radius=0.22,
            fill_color=RED_C,
            fill_opacity=1,
            stroke_width=0
        ).move_to(material.get_center())

        absorbed_label = Text(
            "Absorbed",
            font_size=26,
            color=RED_C
        ).next_to(
            material,
            UP,
            buff=0.3
        )

        self.play(
            FadeIn(absorbed),
            FadeIn(absorbed_label)
        )

        summary = Text(
            "Light can be reflected, transmitted, or absorbed",
            font_size=30,
            color=WHITE
        ).to_edge(DOWN)

        self.play(
            Write(summary)
        )

        self.wait(3)

        # -------------------------------------------------
        # Clear first diagram
        # -------------------------------------------------

        self.play(
            FadeOut(
                source,
                source_label,
                beam,
                material,
                material_label,
                reflected,
                reflected_label,
                transmitted,
                transmitted_label,
                absorbed,
                absorbed_label,
                summary
            )
        )

        # =================================================
        # EXAMPLE 1 — RED CLOTH
        # =================================================

        cloth_title = Text(
            "Example 1: Red Cloth",
            font_size=40,
            color=RED_C
        ).to_edge(UP)

        self.play(
            Transform(title, cloth_title)
        )

        cloth = Rectangle(
            width=3,
            height=2.4,
            fill_color=RED_D,
            fill_opacity=0.85,
            stroke_color=WHITE,
            stroke_width=3
        ).move_to(ORIGIN)

        self.play(
            FadeIn(cloth)
        )

        white_beam = Arrow(
            LEFT * 5,
            LEFT * 1.5,
            buff=0,
            color=WHITE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.07
        )

        white_label = Text(
            "White light",
            font_size=26
        ).next_to(
            white_beam,
            UP,
            buff=0.2
        )

        self.play(
            GrowArrow(white_beam),
            FadeIn(white_label)
        )

        # Reflected red light
        red_reflected = Arrow(
            LEFT * 1.5,
            LEFT * 4 + UP * 2,
            buff=0,
            color=RED,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.08
        )

        red_label = Text(
            "More red light reflected",
            font_size=26,
            color=RED
        ).next_to(
            red_reflected,
            UP,
            buff=0.2
        )

        self.play(
            GrowArrow(red_reflected),
            FadeIn(red_label)
        )

        absorbed_colors = Text(
            "Much of the other visible light is absorbed",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN)

        self.play(
            FadeIn(absorbed_colors)
        )

        self.wait(3)

        # -------------------------------------------------
        # Clear red cloth example
        # -------------------------------------------------

        self.play(
            FadeOut(
                cloth,
                white_beam,
                white_label,
                red_reflected,
                red_label,
                absorbed_colors
            )
        )

        # =================================================
        # EXAMPLE 2 — TRANSPARENT GLASS
        # =================================================

        glass_title = Text(
            "Example 2: Transparent Glass",
            font_size=40,
            color=BLUE_B
        ).to_edge(UP)

        self.play(
            Transform(title, glass_title)
        )

        glass = Rectangle(
            width=2.4,
            height=3,
            fill_color=BLUE_E,
            fill_opacity=0.20,
            stroke_color=BLUE_B,
            stroke_width=4
        ).move_to(ORIGIN)

        self.play(
            FadeIn(glass)
        )

        beam_in = Arrow(
            LEFT * 5,
            LEFT * 1.2,
            buff=0,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.07
        )

        self.play(
            GrowArrow(beam_in)
        )

        beam_through = Arrow(
            RIGHT * 1.2,
            RIGHT * 5,
            buff=0,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.07
        )

        self.play(
            GrowArrow(beam_through)
        )

        glass_text = Text(
            "A large fraction of the light is transmitted",
            font_size=30,
            color=GREEN_C
        ).to_edge(DOWN)

        self.play(
            FadeIn(glass_text)
        )

        self.wait(3)

        # -------------------------------------------------
        # Clear glass example
        # -------------------------------------------------

        self.play(
            FadeOut(
                glass,
                beam_in,
                beam_through,
                glass_text
            )
        )

        # =================================================
        # EXAMPLE 3 — OPAQUE METAL
        # =================================================

        metal_title = Text(
            "Example 3: Opaque Metal",
            font_size=40,
            color=GREY_A
        ).to_edge(UP)

        self.play(
            Transform(title, metal_title)
        )

        metal = Rectangle(
            width=2.5,
            height=3.2,
            fill_color=GREY_D,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=3
        ).move_to(ORIGIN)

        self.play(
            FadeIn(metal)
        )

        incoming_metal = Arrow(
            LEFT * 5,
            LEFT * 1.3,
            buff=0,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.07
        )

        self.play(
            GrowArrow(incoming_metal)
        )

        metal_reflection = Arrow(
            LEFT * 1.3,
            LEFT * 4 + UP * 2,
            buff=0,
            color=BLUE_C,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.08
        )

        self.play(
            GrowArrow(metal_reflection)
        )

        no_transmission = Text(
            "No visible transmission through the material",
            font_size=29,
            color=RED_C
        ).to_edge(DOWN)

        self.play(
            FadeIn(no_transmission)
        )

        self.wait(3)

        # -------------------------------------------------
        # Final comparison
        # -------------------------------------------------

        self.play(
            FadeOut(
                metal,
                incoming_metal,
                metal_reflection,
                no_transmission
            )
        )

        final_title = Text(
            "Different Materials Interact with Light Differently",
            font_size=38
        ).move_to(UP * 1.6)

        final_summary = VGroup(
            Text("Red cloth → selective reflection", font_size=28, color=RED_C),
            Text("Glass → strong transmission", font_size=28, color=GREEN_C),
            Text("Opaque metal → no transmission", font_size=28, color=GREY_A)
        ).arrange(
            DOWN,
            buff=0.5,
            aligned_edge=LEFT
        )

        final_summary.move_to(DOWN * 0.4)

        self.play(
            Transform(title, final_title)
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(item)
                    for item in final_summary
                ],
                lag_ratio=0.3
            )
        )

        self.wait(3)


# =========================================================
# RENDER SCENE 11
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "LightMaterials"
    }):
        LightMaterials().render()


# =========================================================
# SCENE 12 — FLUORESCENCE AND PHOSPHORESCENCE
# =========================================================

class FluorescencePhosphorescence(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Fluorescence and Phosphorescence",
            font_size=48
        ).to_edge(UP)

        self.play(Write(title))

        # =================================================
        # PART 1 — FLUORESCENCE
        # =================================================

        fluorescence_title = Text(
            "Fluorescence",
            font_size=38,
            color=GREEN_C
        ).move_to(UP * 2.2)

        self.play(
            FadeIn(fluorescence_title)
        )

        # -------------------------------------------------
        # Fluorescent material
        # -------------------------------------------------

        material = RoundedRectangle(
            width=3.0,
            height=2.0,
            corner_radius=0.2,
            fill_color=GREEN_E,
            fill_opacity=0.30,
            stroke_color=GREEN_C,
            stroke_width=4
        ).move_to(ORIGIN)

        material_label = Text(
            "Fluorescent material",
            font_size=27,
            color=GREEN_C
        ).next_to(
            material,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(material),
            FadeIn(material_label)
        )

        # -------------------------------------------------
        # Incoming UV light
        # -------------------------------------------------

        uv_source = Dot(
            point=LEFT * 5,
            radius=0.12,
            color=PURPLE
        )

        uv_label = Text(
            "Ultraviolet light",
            font_size=27,
            color=PURPLE
        ).next_to(
            uv_source,
            UP,
            buff=0.25
        )

        uv_ray = Arrow(
            uv_source.get_center(),
            LEFT * 1.5,
            buff=0.1,
            color=PURPLE,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.07
        )

        self.play(
            FadeIn(uv_source),
            FadeIn(uv_label),
            GrowArrow(uv_ray)
        )

        # -------------------------------------------------
        # Absorption
        # -------------------------------------------------

        absorption = Circle(
            radius=0.22,
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_width=0
        ).move_to(
            material.get_center()
        )

        absorbed_text = Text(
            "Energy absorbed",
            font_size=26,
            color=PURPLE
        ).next_to(
            material,
            UP,
            buff=0.25
        )

        self.play(
            FadeIn(absorption),
            FadeIn(absorbed_text)
        )

        self.wait(1)

        # -------------------------------------------------
        # Visible light emitted
        # -------------------------------------------------

        emitted_rays = VGroup()

        directions = [
            UP,
            DOWN,
            RIGHT,
            UP + RIGHT,
            DOWN + RIGHT
        ]

        for direction in directions:

            direction = direction / np.linalg.norm(direction)

            ray = Arrow(
                material.get_center(),
                material.get_center() + direction * 2.0,
                buff=0.4,
                color=GREEN_C,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.12
            )

            emitted_rays.add(ray)

        self.play(
            LaggedStart(
                *[
                    GrowArrow(ray)
                    for ray in emitted_rays
                ],
                lag_ratio=0.12
            )
        )

        emitted_label = Text(
            "Visible light emitted",
            font_size=29,
            color=GREEN_C
        ).move_to(
            RIGHT * 3.8 + UP * 1.8
        )

        self.play(
            FadeIn(emitted_label)
        )

        # -------------------------------------------------
        # Energy representation
        # -------------------------------------------------

        energy_relation = VGroup(

            Text(
                "Higher-energy light",
                font_size=25,
                color=PURPLE
            ),

            MathTex(
                r"\longrightarrow",
                font_size=40
            ),

            Text(
                "Lower-energy light",
                font_size=25,
                color=GREEN_C
            )

        ).arrange(
            RIGHT,
            buff=0.3
        ).to_edge(DOWN)

        self.play(
            FadeIn(energy_relation)
        )

        self.wait(3)

        # -------------------------------------------------
        # Key fluorescence point
        # -------------------------------------------------

        self.play(
            FadeOut(
                energy_relation,
                emitted_label,
                emitted_rays,
                absorbed_text,
                absorption
            )
        )

        fluorescence_message = Text(
            "Emission stops almost immediately when the excitation stops",
            font_size=29,
            color=GREEN_C
        ).to_edge(DOWN)

        self.play(
            Write(fluorescence_message)
        )

        # Remove incoming UV
        self.play(
            FadeOut(
                uv_ray,
                uv_source,
                uv_label
            )
        )

        # Material stops glowing
        self.play(
            material.animate.set_fill(
                GREEN_E,
                opacity=0.08
            ),
            run_time=1.5
        )

        self.wait(2)

        # =================================================
        # PART 2 — PHOSPHORESCENCE
        # =================================================

        self.play(
            FadeOut(
                fluorescence_title,
                fluorescence_message,
                material_label,
                material
            )
        )

        phosphorescence_title = Text(
            "Phosphorescence",
            font_size=38,
            color=YELLOW
        ).move_to(
            UP * 2.2
        )

        self.play(
            FadeIn(phosphorescence_title)
        )

        # -------------------------------------------------
        # Glow-in-the-dark material
        # -------------------------------------------------

        glow_material = RoundedRectangle(
            width=3.0,
            height=2.0,
            corner_radius=0.2,
            fill_color=YELLOW,
            fill_opacity=0.18,
            stroke_color=YELLOW,
            stroke_width=4
        ).move_to(ORIGIN)

        glow_label = Text(
            "Phosphorescent material",
            font_size=27,
            color=YELLOW
        ).next_to(
            glow_material,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(glow_material),
            FadeIn(glow_label)
        )

        # -------------------------------------------------
        # Excitation
        # -------------------------------------------------

        excitation_source = Dot(
            LEFT * 5,
            radius=0.12,
            color=PURPLE
        )

        excitation_ray = Arrow(
            excitation_source.get_center(),
            LEFT * 1.5,
            buff=0.1,
            color=PURPLE,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.07
        )

        excitation_label = Text(
            "Excitation light",
            font_size=27,
            color=PURPLE
        ).next_to(
            excitation_source,
            UP,
            buff=0.25
        )

        self.play(
            FadeIn(excitation_source),
            FadeIn(excitation_label),
            GrowArrow(excitation_ray)
        )

        # Material becomes brighter
        self.play(
            glow_material.animate.set_fill(
                YELLOW,
                opacity=0.65
            ),
            run_time=1.5
        )

        stored_energy = Text(
            "Some energy is stored temporarily",
            font_size=29,
            color=YELLOW
        ).to_edge(DOWN)

        self.play(
            FadeIn(stored_energy)
        )

        self.wait(2)

        # -------------------------------------------------
        # Remove the excitation source
        # -------------------------------------------------

        self.play(
            FadeOut(
                excitation_source,
                excitation_ray,
                excitation_label,
                stored_energy
            )
        )

        source_off = Text(
            "Light source OFF",
            font_size=29,
            color=RED_C
        ).move_to(
            LEFT * 4 + UP * 1.8
        )

        self.play(
            FadeIn(source_off)
        )

        # -------------------------------------------------
        # Delayed glow
        # -------------------------------------------------

        delayed_rays = VGroup()

        for direction in directions:

            direction = direction / np.linalg.norm(direction)

            ray = Arrow(
                glow_material.get_center(),
                glow_material.get_center() + direction * 1.8,
                buff=0.4,
                color=YELLOW,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.12
            )

            delayed_rays.add(ray)

        self.play(
            LaggedStart(
                *[
                    GrowArrow(ray)
                    for ray in delayed_rays
                ],
                lag_ratio=0.12
            )
        )

        continues_glowing = Text(
            "The material continues emitting light",
            font_size=30,
            color=YELLOW
        ).to_edge(DOWN)

        self.play(
            Write(continues_glowing)
        )

        self.wait(2)

        # Gradual fading
        self.play(
            delayed_rays.animate.set_opacity(0.35),
            glow_material.animate.set_fill(
                YELLOW,
                opacity=0.30
            ),
            run_time=2
        )

        self.play(
            delayed_rays.animate.set_opacity(0.10),
            glow_material.animate.set_fill(
                YELLOW,
                opacity=0.12
            ),
            run_time=2
        )

        self.wait(1)

        # =================================================
        # FINAL COMPARISON
        # =================================================

        self.play(
            FadeOut(
                delayed_rays,
                glow_material,
                glow_label,
                source_off,
                continues_glowing,
                phosphorescence_title
            )
        )

        comparison_title = Text(
            "Fluorescence vs Phosphorescence",
            font_size=43
        ).to_edge(UP)

        self.play(
            Transform(title, comparison_title)
        )

        # -------------------------------------------------
        # Fluorescence side
        # -------------------------------------------------

        fluorescence_box = RoundedRectangle(
            width=5.2,
            height=3.2,
            corner_radius=0.25,
            stroke_color=GREEN_C,
            stroke_width=4
        ).shift(
            LEFT * 3
        )

        f_title = Text(
            "Fluorescence",
            font_size=32,
            color=GREEN_C
        ).next_to(
            fluorescence_box,
            UP,
            buff=-0.5
        )

        f_text = VGroup(
            Text(
                "Absorbs light",
                font_size=25
            ),
            Text(
                "Re-emits quickly",
                font_size=25
            ),
            Text(
                "Stops almost immediately",
                font_size=25,
                color=GREEN_C
            )
        ).arrange(
            DOWN,
            buff=0.35
        ).move_to(
            fluorescence_box
        )

        # -------------------------------------------------
        # Phosphorescence side
        # -------------------------------------------------

        phosphorescence_box = RoundedRectangle(
            width=5.2,
            height=3.2,
            corner_radius=0.25,
            stroke_color=YELLOW,
            stroke_width=4
        ).shift(
            RIGHT * 3
        )

        p_title = Text(
            "Phosphorescence",
            font_size=32,
            color=YELLOW
        ).next_to(
            phosphorescence_box,
            UP,
            buff=-0.5
        )

        p_text = VGroup(
            Text(
                "Absorbs light",
                font_size=25
            ),
            Text(
                "Stores energy temporarily",
                font_size=25
            ),
            Text(
                "Continues glowing afterward",
                font_size=25,
                color=YELLOW
            )
        ).arrange(
            DOWN,
            buff=0.35
        ).move_to(
            phosphorescence_box
        )

        self.play(
            Create(fluorescence_box),
            Create(phosphorescence_box)
        )

        self.play(
            FadeIn(f_title),
            FadeIn(p_title)
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(item)
                    for item in f_text
                ],
                lag_ratio=0.25
            ),

            LaggedStart(
                *[
                    FadeIn(item)
                    for item in p_text
                ],
                lag_ratio=0.25
            )
        )

        self.wait(4)


# =========================================================
# RENDER SCENE 12
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "FluorescencePhosphorescence"
    }):
        FluorescencePhosphorescence().render()


# =========================================================
# SCENE 13 — MICROSCOPES AND RESOLUTION
# =========================================================

class MicroscopesResolution(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Microscopes and Resolution",
            font_size=48
        ).to_edge(UP)

        self.play(Write(title))

        # =================================================
        # PART 1 — LENSES AND MAGNIFICATION
        # =================================================

        lens_title = Text(
            "Lenses use refraction to form magnified images",
            font_size=32,
            color=BLUE_B
        ).move_to(UP * 2.4)

        self.play(FadeIn(lens_title))

        # Object
        object_arrow = Arrow(
            DOWN * 1.3,
            UP * 0.5,
            buff=0,
            color=YELLOW,
            stroke_width=6
        ).shift(LEFT * 4)

        object_label = Text(
            "Object",
            font_size=25,
            color=YELLOW
        ).next_to(
            object_arrow,
            DOWN,
            buff=0.25
        )

        # Convex lens
        lens = Ellipse(
            width=0.8,
            height=4.0,
            stroke_color=BLUE_C,
            stroke_width=5,
            fill_color=BLUE_E,
            fill_opacity=0.18
        )

        lens_label = Text(
            "Lens",
            font_size=25,
            color=BLUE_C
        ).next_to(
            lens,
            DOWN,
            buff=0.25
        )

        # Image
        image_arrow = Arrow(
            UP * 1.2,
            DOWN * 1.7,
            buff=0,
            color=GREEN_C,
            stroke_width=6
        ).shift(RIGHT * 4)

        image_label = Text(
            "Inverted image",
            font_size=25,
            color=GREEN_C
        ).next_to(
            image_arrow,
            DOWN,
            buff=0.25
        )

        self.play(
            GrowArrow(object_arrow),
            FadeIn(object_label),
            FadeIn(lens),
            FadeIn(lens_label)
        )

        # Light rays
        ray1 = Line(
            object_arrow.get_end(),
            lens.get_center() + UP * 0.6,
            color=YELLOW,
            stroke_width=4
        )

        ray2 = Line(
            object_arrow.get_end(),
            lens.get_center() + DOWN * 0.5,
            color=YELLOW,
            stroke_width=4
        )

        ray3 = Line(
            lens.get_center() + UP * 0.6,
            image_arrow.get_end(),
            color=GREEN_C,
            stroke_width=4
        )

        ray4 = Line(
            lens.get_center() + DOWN * 0.5,
            image_arrow.get_end(),
            color=GREEN_C,
            stroke_width=4
        )

        self.play(
            Create(ray1),
            Create(ray2)
        )

        self.play(
            Create(ray3),
            Create(ray4),
            GrowArrow(image_arrow),
            FadeIn(image_label)
        )

        self.wait(2)

        # -------------------------------------------------
        # Important distinction
        # -------------------------------------------------

        magnification_note = Text(
            "Magnification does not automatically mean more detail",
            font_size=31,
            color=ORANGE
        ).to_edge(DOWN)

        self.play(
            Write(magnification_note)
        )

        self.wait(3)

        # =================================================
        # PART 2 — RESOLUTION
        # =================================================

        self.play(
            FadeOut(
                lens_title,
                object_arrow,
                object_label,
                lens,
                lens_label,
                image_arrow,
                image_label,
                ray1,
                ray2,
                ray3,
                ray4,
                magnification_note
            )
        )

        resolution_title = Text(
            "Resolution",
            font_size=42,
            color=GREEN_C
        ).move_to(UP * 2.5)

        resolution_definition = Text(
            "Can two nearby points be seen as separate?",
            font_size=31
        ).next_to(
            resolution_title,
            DOWN,
            buff=0.4
        )

        self.play(
            FadeIn(resolution_title),
            FadeIn(resolution_definition)
        )

        # -------------------------------------------------
        # Poor resolution
        # -------------------------------------------------

        poor_label = Text(
            "Poor resolution",
            font_size=28,
            color=RED_C
        ).move_to(
            LEFT * 3.2 + UP * 0.6
        )

        poor_blob = Ellipse(
            width=2.0,
            height=1.0,
            fill_color=RED_C,
            fill_opacity=0.6,
            stroke_width=0
        ).move_to(
            LEFT * 3.2 + DOWN * 0.7
        )

        # -------------------------------------------------
        # Good resolution
        # -------------------------------------------------

        good_label = Text(
            "Good resolution",
            font_size=28,
            color=GREEN_C
        ).move_to(
            RIGHT * 3.2 + UP * 0.6
        )

        dot1 = Dot(
            point=RIGHT * 3.55 + DOWN * 0.7,
            radius=0.23,
            color=GREEN_C
        )

        dot2 = Dot(
            point=RIGHT * 2.85 + DOWN * 0.7,
            radius=0.23,
            color=GREEN_C
        )

        self.play(
            FadeIn(poor_label),
            FadeIn(good_label)
        )

        self.play(
            FadeIn(poor_blob),
            FadeIn(dot1),
            FadeIn(dot2)
        )

        self.wait(3)

        # =================================================
        # PART 3 — WAVELENGTH AND RESOLUTION
        # =================================================

        self.play(
            FadeOut(
                poor_label,
                good_label,
                poor_blob,
                dot1,
                dot2,
                resolution_definition
            )
        )

        wavelength_title = Text(
            "Shorter Wavelength → Better Resolution",
            font_size=38,
            color=BLUE_B
        ).move_to(UP * 1.7)

        self.play(
            FadeIn(wavelength_title)
        )

        # Long wavelength
        long_axes = Axes(
            x_range=[0, 2 * PI, PI],
            y_range=[-1.2, 1.2, 1],
            x_length=5,
            y_length=1.7,
            tips=False,
            axis_config={
                "stroke_color": GREY_B,
                "stroke_width": 2
            }
        ).shift(
            LEFT * 3 + DOWN * 0.2
        )

        long_wave = long_axes.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=RED_C,
            stroke_width=5
        )

        long_label = Text(
            "Long wavelength",
            font_size=26,
            color=RED_C
        ).next_to(
            long_axes,
            DOWN,
            buff=0.25
        )

        # Short wavelength
        short_axes = Axes(
            x_range=[0, 4 * PI, 2 * PI],
            y_range=[-1.2, 1.2, 1],
            x_length=5,
            y_length=1.7,
            tips=False,
            axis_config={
                "stroke_color": GREY_B,
                "stroke_width": 2
            }
        ).shift(
            RIGHT * 3 + DOWN * 0.2
        )

        short_wave = short_axes.plot(
            lambda x: np.sin(x),
            x_range=[0, 4 * PI],
            color=BLUE_C,
            stroke_width=5
        )

        short_label = Text(
            "Short wavelength",
            font_size=26,
            color=BLUE_C
        ).next_to(
            short_axes,
            DOWN,
            buff=0.25
        )

        self.play(
            Create(long_axes),
            Create(short_axes)
        )

        self.play(
            Create(long_wave),
            Create(short_wave),
            FadeIn(long_label),
            FadeIn(short_label)
        )

        better_detail = Text(
            "Shorter wavelengths can reveal smaller details",
            font_size=31,
            color=GREEN_C
        ).to_edge(DOWN)

        self.play(
            FadeIn(better_detail)
        )

        self.wait(3)

        # =================================================
        # PART 4 — LIGHT VS ELECTRON MICROSCOPE
        # =================================================

        self.play(
            FadeOut(
                long_axes,
                long_wave,
                long_label,
                short_axes,
                short_wave,
                short_label,
                better_detail,
                wavelength_title
            )
        )

        microscope_title = Text(
            "Light Microscope vs Electron Microscope",
            font_size=40
        ).move_to(UP * 2.2)

        self.play(
            FadeIn(microscope_title)
        )

        # Light microscope
        light_box = RoundedRectangle(
            width=5,
            height=3,
            corner_radius=0.2,
            stroke_color=BLUE_C,
            stroke_width=4
        ).shift(LEFT * 3)

        light_title = Text(
            "Light Microscope",
            font_size=30,
            color=BLUE_C
        ).next_to(
            light_box,
            UP,
            buff=-0.5
        )

        light_text = VGroup(
            Text(
                "Uses visible light",
                font_size=25
            ),
            Text(
                "Longer wavelength",
                font_size=25
            ),
            Text(
                "Lower resolving power",
                font_size=25,
                color=BLUE_C
            )
        ).arrange(
            DOWN,
            buff=0.35
        ).move_to(
            light_box
        )

        # Electron microscope
        electron_box = RoundedRectangle(
            width=5,
            height=3,
            corner_radius=0.2,
            stroke_color=PURPLE_C,
            stroke_width=4
        ).shift(RIGHT * 3)

        electron_title = Text(
            "Electron Microscope",
            font_size=30,
            color=PURPLE_C
        ).next_to(
            electron_box,
            UP,
            buff=-0.5
        )

        electron_text = VGroup(
            Text(
                "Uses electrons",
                font_size=25
            ),
            Text(
                "Much shorter wavelength",
                font_size=25
            ),
            Text(
                "Higher resolving power",
                font_size=25,
                color=GREEN_C
            )
        ).arrange(
            DOWN,
            buff=0.35
        ).move_to(
            electron_box
        )

        self.play(
            Create(light_box),
            Create(electron_box)
        )

        self.play(
            FadeIn(light_title),
            FadeIn(electron_title)
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(item)
                    for item in light_text
                ],
                lag_ratio=0.2
            ),
            LaggedStart(
                *[
                    FadeIn(item)
                    for item in electron_text
                ],
                lag_ratio=0.2
            )
        )

        self.wait(3)

        # =================================================
        # PART 5 — CONTRAST AND STAINING
        # =================================================

        self.play(
            FadeOut(
                light_box,
                light_title,
                light_text,
                electron_box,
                electron_title,
                electron_text,
                microscope_title
            )
        )

        contrast_title = Text(
            "Contrast Also Matters",
            font_size=42,
            color=YELLOW
        ).move_to(UP * 2)

        self.play(
            FadeIn(contrast_title)
        )

        # Transparent cell
        cell1 = Circle(
            radius=1.2,
            stroke_color=GREY_B,
            stroke_width=3,
            fill_color=GREY_E,
            fill_opacity=0.08
        ).shift(LEFT * 3)

        nucleus1 = Circle(
            radius=0.4,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_opacity=0
        ).shift(LEFT * 3)

        low_contrast = Text(
            "Low contrast",
            font_size=28,
            color=GREY_B
        ).next_to(
            cell1,
            DOWN,
            buff=0.3
        )

        # Stained cell
        cell2 = Circle(
            radius=1.2,
            stroke_color=BLUE_C,
            stroke_width=4,
            fill_color=BLUE_E,
            fill_opacity=0.25
        ).shift(RIGHT * 3)

        nucleus2 = Circle(
            radius=0.4,
            stroke_color=PURPLE_C,
            stroke_width=3,
            fill_color=PURPLE_C,
            fill_opacity=0.65
        ).shift(RIGHT * 3)

        high_contrast = Text(
            "Higher contrast after staining",
            font_size=28,
            color=GREEN_C
        ).next_to(
            cell2,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(cell1),
            FadeIn(nucleus1),
            FadeIn(cell2),
            FadeIn(nucleus2)
        )

        self.play(
            FadeIn(low_contrast),
            FadeIn(high_contrast)
        )

        final_message = Text(
            "Magnification, resolution, and contrast are different concepts",
            font_size=30,
            color=WHITE
        ).to_edge(DOWN)

        self.play(
            Write(final_message)
        )

        self.wait(4)


# =========================================================
# RENDER SCENE 13
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "MicroscopesResolution"
    }):
        MicroscopesResolution().render()


# =========================================================
# SCENE 14 — FINAL RECAP
# =========================================================

class FinalRecap(Scene):
    def construct(self):

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = Text(
            "Light: A Wave Interacting with the World",
            font_size=46
        ).to_edge(UP)

        self.play(Write(title))

        # -------------------------------------------------
        # Central light wave
        # -------------------------------------------------

        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.2, 1.2, 1],
            x_length=7,
            y_length=2.2,
            tips=False,
            axis_config={
                "stroke_color": GREY_B,
                "stroke_width": 2
            }
        ).shift(UP * 1.2)

        wave = axes.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=YELLOW,
            stroke_width=5
        )

        self.play(
            Create(axes),
            Create(wave)
        )

        light_label = Text(
            "Light",
            font_size=34,
            color=YELLOW
        ).next_to(
            axes,
            UP,
            buff=0.2
        )

        self.play(FadeIn(light_label))

        # -------------------------------------------------
        # Property labels
        # -------------------------------------------------

        labels = VGroup(
            Text("Reflection", font_size=30, color=BLUE_C),
            Text("Refraction", font_size=30, color=GREEN_C),
            Text("Dispersion", font_size=30, color=PURPLE_C),
            Text("Polarization", font_size=30, color=ORANGE),
            Text("Diffraction", font_size=30, color=RED_C),
            Text("Interference", font_size=30, color=YELLOW),
            Text("Absorption / Transmission", font_size=30, color=GREY_A)
        )

        labels.arrange(
            DOWN,
            buff=0.28,
            aligned_edge=LEFT
        )

        labels.scale(0.9)

        labels.shift(
            LEFT * 3.7 + DOWN * 1.1
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(label, shift=RIGHT * 0.2)
                    for label in labels
                ],
                lag_ratio=0.12
            ),
            run_time=2.5
        )

        # -------------------------------------------------
        # Everyday examples on the right
        # -------------------------------------------------

        examples = VGroup(
            Text("Mirror", font_size=27),
            Text("Fish under water", font_size=27),
            Text("Prism", font_size=27),
            Text("Sunglasses", font_size=27),
            Text("Narrow slit", font_size=27),
            Text("Double slit", font_size=27),
            Text("Glass / cloth / metal", font_size=27)
        )

        examples.arrange(
            DOWN,
            buff=0.33,
            aligned_edge=LEFT
        )

        examples.shift(
            RIGHT * 3.4 + DOWN * 1.1
        )

        arrows = VGroup()

        for left_item, right_item in zip(labels, examples):

            arrow = Arrow(
                left_item.get_right(),
                right_item.get_left(),
                buff=0.2,
                color=GREY_B,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.12
            )

            arrows.add(arrow)

        self.play(
            LaggedStart(
                *[
                    GrowArrow(arrow)
                    for arrow in arrows
                ],
                lag_ratio=0.08
            )
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(example)
                    for example in examples
                ],
                lag_ratio=0.12
            )
        )

        self.wait(2)

        # -------------------------------------------------
        # Final message
        # -------------------------------------------------

        self.play(
            FadeOut(
                axes,
                wave,
                light_label,
                labels,
                examples,
                arrows
            )
        )

        final_text = Text(
            "Many everyday phenomena come from the same underlying physics",
            font_size=38
        ).move_to(UP * 0.5)

        final_subtext = Text(
            "Light behaves as a wave and interacts with matter in different ways",
            font_size=30,
            color=BLUE_B
        ).next_to(
            final_text,
            DOWN,
            buff=0.6
        )

        self.play(
            Write(final_text)
        )

        self.play(
            FadeIn(final_subtext)
        )

        self.wait(4)


# =========================================================
# RENDER SCENE 14
# =========================================================

if __name__ == "__main__":
    with tempconfig({
        "write_to_movie": True,
        "disable_caching": True,
        "output_file": "FinalRecap"
    }):
        FinalRecap().render()


