"""Animated introduction to Poisson's equation.

The narration is copied from the user's 1.txt. The seven visual beats are
timed to leave room for a recorded voice track; this scene renders from PyCharm.
"""

from manim import *
import numpy as np
import os
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap

os.environ.setdefault("POISSON_QUALITY", "final")

from math_type import tex
from settings34 import BLUE, GREEN, GREY, RED, WHITE, YELLOW, run
from support34 import ar


BG = "#000000"
TARGET_SECONDS = 180.0
FIELD_CMAP = LinearSegmentedColormap.from_list(
    "poisson_field", ["#244B8A", "#111925", "#F0B94D", "#E85E50"]
)


def point_charge(charge, position, radius=0.14):
    """Return one signed charge marker at a scene-space position."""
    position = np.array(position, dtype=float)
    if position.size == 2:
        position = np.append(position, 0.0)
    color = RED if charge > 0 else BLUE
    disc = Circle(radius=radius, stroke_width=1.6, color=color,
                  fill_color=color, fill_opacity=0.96)
    sign = Text("+" if charge > 0 else "−", font="Arial", font_size=20,
                color=BG).move_to(disc)
    return VGroup(disc, sign).move_to(position)


def field_image(values, width, height, centre, vmin, vmax):
    """Rasterize a scalar field; values are indexed [y, x]."""
    values = np.asarray(values, dtype=float)
    scaled = np.clip((values - vmin) / max(vmax - vmin, 1e-12), 0, 1)
    rgba = FIELD_CMAP(scaled, bytes=True)
    rgba[..., 3] = 240
    pixel_width = 640
    pixel_height = round(pixel_width * height / width)
    pixels = Image.fromarray(np.flipud(rgba)).resize(
        (pixel_width, pixel_height), Image.Resampling.BICUBIC
    )
    mob = ImageMobject(np.asarray(pixels))
    mob.scale_to_fit_width(width).move_to(centre)
    return mob


def poisson_example(nx=45, ny=45, iterations=2400, boundary_value=0.4):
    """Solve ΔV=-rho on a square grid with prescribed boundary value V_b.

    Arrays use [y, x] indexing so np.gradient returns (d/dy, d/dx).
    """
    x = np.linspace(-2, 2, nx)
    y = np.linspace(-2, 2, ny)
    h = x[1] - x[0]
    X, Y = np.meshgrid(x, y)
    rho = 1.4 * np.exp(-(X**2 + Y**2) / 0.34)
    potential = np.full_like(rho, boundary_value)
    for _ in range(iterations):
        updated = potential.copy()
        updated[1:-1, 1:-1] = 0.25 * (
            potential[1:-1, :-2] + potential[1:-1, 2:]
            + potential[:-2, 1:-1] + potential[2:, 1:-1]
            + h * h * rho[1:-1, 1:-1]
        )
        potential = updated
    return x, y, rho, potential, boundary_value


def hill_projection(x, y, height, centre):
    """Project a scalar-potential hill into a clean 2.5D scene drawing."""
    return np.array([
        centre[0] + 0.48 * (x - y),
        centre[1] + 0.24 * (x + y) + 1.55 * height,
        0.0,
    ])


def potential_hill(centre=(-3.45, -0.25, 0.0)):
    """A wireframe height map: vertical height encodes V, not physical space."""
    mesh = VGroup()
    samples = np.linspace(-1.8, 1.8, 13)

    def v(x, y):
        return 1.18 * np.exp(-0.72 * (x*x + y*y))

    for fixed, horizontal in [(q, True) for q in samples] + [(q, False) for q in samples]:
        coords = np.linspace(-1.8, 1.8, 65)
        points = []
        for q in coords:
            x, y = (q, fixed) if horizontal else (fixed, q)
            points.append(hill_projection(x, y, v(x, y), centre))
        curve = VMobject().set_points_smoothly(points)
        level = v(fixed, 0.0) / 1.18
        curve.set_stroke(interpolate_color(ManimColor(BLUE), ManimColor(YELLOW), level),
                         width=1.35, opacity=0.78)
        mesh.add(curve)

    contours = VGroup()
    for radius, color in [(0.52, YELLOW), (0.95, BLUE), (1.38, BLUE)]:
        points = []
        for theta in np.linspace(0, TAU, 120):
            x, y = radius*np.cos(theta), radius*np.sin(theta)
            points.append(hill_projection(x, y, v(x, y), centre))
        contour = VMobject().set_points_smoothly(points).set_stroke(color, width=2.1)
        contours.add(contour)
    return mesh, contours, v


class PoissonIntroduction(MovingCameraScene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.electrostatic_routes()
        self.integral_difficulty()
        self.local_laws()
        self.potential_and_poisson()
        self.curl_identity()
        self.boundary_and_close()
        if self.time < TARGET_SECONDS:
            self.wait(TARGET_SECONDS - self.time)
        print(f"[scene_00] duration: {self.time:.2f} s; voice target: {TARGET_SECONDS:.0f} s")

    def hold_to(self, end_time):
        remaining = end_time - self.time
        if remaining > 0:
            self.wait(remaining)

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=0.55)

    def heading(self, text):
        title = ar(text, 30, WHITE).to_edge(UP, buff=0.3)
        rule = Line([-6.7, 3.02, 0], [6.7, 3.02, 0], color=GREY,
                    stroke_width=1).set_stroke(opacity=0.48)
        self.play(FadeIn(title, shift=DOWN*0.12), Create(rule), run_time=0.65)
        return VGroup(title, rule)

    def opening(self):
        start = self.time
        title = ar("معادلة بواسون", 43, YELLOW).move_to([0, 2.75, 0])
        equation = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 51, WHITE).move_to([0, 1.85, 0])
        domain = RoundedRectangle(width=5.3, height=3.25, corner_radius=0.12,
                                  color=GREEN, stroke_width=2.0).move_to([-3.25, -0.62, 0])
        rng = np.random.default_rng(12)
        charge_dots = VGroup(*[
            Dot([-3.25 + rng.normal(0, 0.67), -0.62 + rng.normal(0, 0.5), 0],
                radius=0.035 + 0.012*(i % 3),
                color=RED if i % 4 == 0 else YELLOW)
            for i in range(35)
        ])
        source_tag = tex(r"\rho", 25, RED).move_to([-5.55, 1.0, 0])
        boundary_tag = tex(r"V_b", 24, GREEN).move_to([-3.25, 1.25, 0])
        contours = VGroup(*[
            Ellipse(width=w, height=h, color=color, stroke_width=1.6)
            .move_to([-3.25, -0.62, 0])
            for w, h, color in [(0.8, 0.58, YELLOW), (1.55, 1.08, BLUE), (2.3, 1.65, BLUE)]
        ])
        potential_tag = tex(r"V", 20, YELLOW).move_to([-2.52, -0.16, 0])
        unique = ar("تتحقق وحدانية الحل عندما تتوفر شروط حدية ملائمة.", 22, GREEN).move_to([3.1, -0.15, 0])
        application = ar("نمذجة الأنظمة الكهروستاتيكية", 22, BLUE).move_to([3.1, -1.05, 0])
        question = tex(r"\rho\;\longrightarrow\;V", 33, YELLOW).move_to([3.05, -2.0, 0])

        self.play(FadeIn(title, shift=UP*0.18), run_time=0.8)
        self.play(Write(equation), run_time=1.5)
        self.play(Create(domain), FadeIn(source_tag), FadeIn(boundary_tag), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in charge_dots], lag_ratio=0.025), run_time=2.0)
        self.play(LaggedStart(*[Create(c) for c in contours], lag_ratio=0.28), run_time=1.8)
        self.play(FadeIn(potential_tag), LaggedStart(*[Indicate(d, color=RED) for d in charge_dots[::7]],
                                                       lag_ratio=0.12), run_time=1.4)
        self.play(FadeIn(unique, shift=LEFT*0.18), FadeIn(application, shift=LEFT*0.18),
                  Write(question), run_time=1.4)
        self.play(Indicate(equation, color=YELLOW), Indicate(domain, color=GREEN), run_time=1.0)
        self.play(self.camera.frame.animate.scale(0.96).move_to([-1.3, 0.0, 0]), run_time=1.2)
        self.play(self.camera.frame.animate.scale(1/0.96).move_to(ORIGIN), run_time=1.2)
        self.hold_to(start + 22)
        self.clear_scene()

    def electrostatic_routes(self):
        start = self.time
        self.heading("إيجاد المجال من التوزيع المكاني للشحنات")
        source_xy = [(-5.3, 0.95), (-5.0, 0.0), (-5.3, -0.95)]
        charges = VGroup(*[point_charge(1, p, 0.13) for p in source_xy])
        probe = Dot([-2.0, -0.05, 0], radius=0.09, color=WHITE)
        probe_label = ar("نقطة الرصد", 18, WHITE).next_to(probe, DOWN, buff=0.2)
        contributions = VGroup(
            Arrow(probe.get_center(), probe.get_center()+[1.0, 0.48, 0], buff=0.02,
                  color=RED, stroke_width=3.5),
            Arrow(probe.get_center(), probe.get_center()+[1.25, 0.0, 0], buff=0.02,
                  color=BLUE, stroke_width=3.5),
            Arrow(probe.get_center(), probe.get_center()+[1.0, -0.48, 0], buff=0.02,
                  color=GREEN, stroke_width=3.5),
        )
        sum_formula = tex(r"\mathbf{E}(\mathbf{r})=\sum_i\mathbf{E}_i(\mathbf{r})", 30).move_to([3.45, 1.9, 0])
        resultant = Arrow([-1.9, -0.05, 0], [0.0, -0.05, 0], buff=0.03,
                          color=YELLOW, stroke_width=5)
        total = tex(r"\mathbf{E}=\mathbf{E}_1+\mathbf{E}_2+\mathbf{E}_3", 26, YELLOW).move_to([3.45, 0.95, 0])
        continuous = tex(r"\sum_i\;\longrightarrow\;\int", 32, WHITE).move_to([3.4, -0.08, 0])

        self.play(LaggedStart(*[GrowFromCenter(q) for q in charges], lag_ratio=0.2), run_time=1.2)
        self.play(FadeIn(probe), FadeIn(probe_label), run_time=0.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in contributions], lag_ratio=0.2), run_time=1.7)
        self.play(Write(sum_formula), run_time=1.0)
        self.play(FadeOut(contributions), GrowArrow(resultant), Write(total), run_time=1.3)
        self.play(ReplacementTransform(total, continuous), run_time=1.3)

        # The Gaussian surface is a new view: a cross-section enclosing charge,
        # with arrows normal to its boundary, rather than another dipole plot.
        surface = Ellipse(width=2.2, height=1.6, color=GREEN, stroke_width=2.5).move_to([-4.0, -1.3, 0])
        enclosed = VGroup(*[point_charge(1, [-4.0 + dx, -1.3 + dy], 0.09)
                            for dx, dy in [(-0.28, 0), (0.22, 0.18), (0.18, -0.2)]])
        normals = VGroup()
        for angle in np.linspace(0, TAU, 10, endpoint=False):
            origin = np.array([-4.0 + 1.0*np.cos(angle), -1.3 + 0.72*np.sin(angle), 0])
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            normals.add(Arrow(origin, origin + 0.36*direction, buff=0,
                              color=BLUE, stroke_width=2.2,
                              max_tip_length_to_length_ratio=0.3))
        gauss_label = ar("سطح غاوسي", 19, GREEN).next_to(surface, DOWN, buff=0.13)
        gauss = tex(r"\oint_S\mathbf{E}\cdot d\mathbf{A}=\frac{q_{\mathrm{enc}}}{\varepsilon_0}", 25, BLUE).move_to([3.45, -1.1, 0])
        symmetry = ar("في ظل وجود تناظر ملائم", 18, GREY).move_to([3.45, -1.75, 0])
        self.play(FadeOut(charges), FadeOut(probe), FadeOut(probe_label), FadeOut(resultant),
                  FadeOut(total), FadeOut(continuous), run_time=0.7)
        self.play(Create(surface), FadeIn(enclosed), LaggedStart(*[GrowArrow(a) for a in normals], lag_ratio=0.07),
                  FadeIn(gauss_label), Write(gauss), FadeIn(symmetry), run_time=2.0)
        flux_markers = VGroup(*[
            Dot(surface.get_center()+0.28*np.array([np.cos(a), np.sin(a), 0]),
                radius=0.04, color=WHITE)
            for a in (-0.9, -0.3, 0.35, 0.95, 2.2)
        ])
        self.add(flux_markers)
        self.play(*[
            marker.animate.shift(0.62*np.array([np.cos(a), np.sin(a), 0]))
            for marker, a in zip(flux_markers, (-0.9, -0.3, 0.35, 0.95, 2.2))
        ], run_time=2.2)
        self.hold_to(start + 32)
        self.clear_scene()

    def integral_difficulty(self):
        start = self.time
        self.heading("قد تصبح عملية حساب التكاملات صعبة من الناحية العملية في بعض الحالات")
        # A distributed line charge creates a distinct source-to-observation
        # geometry. Rays here represent the kernel directions r-r', not E-lines.
        rail = Line([-5.5, -0.65, 0], [-1.3, -0.65, 0], color=GREY, stroke_width=2)
        qs = VGroup(*[Dot([-5.35 + i*0.2, -0.65 + 0.11*np.sin(i*0.7), 0],
                          radius=0.045, color=YELLOW if i % 3 else RED)
                      for i in range(21)])
        probe = Dot([1.65, 0.65, 0], radius=0.09, color=WHITE)
        rays = always_redraw(lambda: VGroup(*[
            Line(q.get_center(), probe.get_center(), color=BLUE,
                 stroke_width=0.8).set_stroke(opacity=0.62) for q in qs
        ]))
        ray_label = tex(r"\hat{\mathbf{r}}", 21, BLUE).move_to([-0.95, 0.1, 0])
        integral = tex(r"\mathbf{E}(\mathbf{r})=\frac{1}{4\pi\varepsilon_0}\int\frac{\rho(\mathbf{r}')\,\hat{\mathbf{r}}}{r^2}\,d\tau'", 27).move_to([3.5, 2.0, 0])
        difficulty = ar("حتى مع معرفة توزيع الشحنات", 21, WHITE).move_to([3.45, 0.85, 0])
        rename = ar("لذلك، نعيد صياغة المسألة,باستخدام المعادلات التفاضلية", 21, GREEN).move_to([3.45, -0.05, 0])
        differential = ar("مما قد يجعل إجراء الحسابات أسهل", 23, GREEN).move_to([3.45, -1.1, 0])
        self.play(Create(rail), LaggedStart(*[FadeIn(q, scale=1.7) for q in qs], lag_ratio=0.03), run_time=2.0)
        self.play(FadeIn(probe), LaggedStart(*[Create(ray) for ray in rays], lag_ratio=0.015), run_time=2.3)
        self.play(Write(integral), FadeIn(difficulty), FadeIn(ray_label), run_time=1.2)
        self.play(probe.animate.move_to([0.55, 1.7, 0]), run_time=1.2)
        self.play(probe.animate.move_to([1.9, -0.2, 0]), run_time=1.2)
        self.play(probe.animate.move_to([0.75, -1.45, 0]), run_time=1.2)
        self.play(FadeOut(rays), FadeIn(rename), FadeIn(differential, shift=UP*0.15), run_time=1.0)
        self.hold_to(start + 18)
        self.clear_scene()

    def local_laws(self):
        start = self.time
        self.heading("نستخدم معادلتين تفاضليتين لهذا الغرض : قانون غاوس في الصيغة التفاضلية وانعدام دوران المجال الكهربائي")

        # LEFT: Gauss's law. Flux leaves the enclosed positive charge.
        source = Dot([-4.05, -0.25, 0], radius=0.13, color=RED)
        gauss_surface = Circle(radius=0.8, color=BLUE, stroke_width=2.2).move_to(source)
        outward = VGroup()
        for angle in np.linspace(0, TAU, 10, endpoint=False):
            p = source.get_center() + 0.79 * np.array([
                np.cos(angle), np.sin(angle), 0
            ])
            d = np.array([np.cos(angle), np.sin(angle), 0])
            outward.add(Arrow(
                p, p + 0.38 * d, buff=0, color=BLUE, stroke_width=2.5,
                max_tip_length_to_length_ratio=0.3,
            ))
        gauss = tex(
            r"\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}",
            31, BLUE,
        ).move_to([-3.75, 1.95, 0])
        source_caption = ar(
            "الشحنة المحصورة داخل سطح غاوسي", 18, BLUE,
        ).move_to([-3.75, -1.65, 0])

        # RIGHT: A uniform electrostatic field E = E0 * x-hat has zero curl.
        # Equivalently, E = -grad(V), with V = -E0*x.
        # The GREEN arrows show the field; none points around the loop.
        uniform = VGroup(*[
            Arrow([x, y, 0], [x + 0.48, y, 0], buff=0,
                  color=GREEN, stroke_width=2.2,
                  max_tip_length_to_length_ratio=0.28)
            for x in np.linspace(1.1, 4.5, 6)
            for y in (-0.85, -0.15, 0.55)
        ])

        # The YELLOW circle is a chosen CLOSED INTEGRATION PATH C, NOT
        # a circular field line or a picture of the curl vector.
        loop = Circle(radius=0.84, color=YELLOW, stroke_width=2.8)
        loop.move_to([2.85, -0.15, 0])
        loop_label = tex(r"C", 21, YELLOW).move_to([3.91, -0.15, 0])
        loop_marker = Dot(loop.point_from_proportion(0), radius=0.065, color=WHITE)

        curl = tex(r"\nabla\times\mathbf{E}=0", 32, GREEN).move_to([3.0, 1.95, 0])
        curl_caption = ar(
            "انعدام دوران المجال الكهربائي", 17, GREEN,
        ).move_to([3.0, -1.35, 0])
        # For constant E, integral_C E.dl = E.(r_final-r_initial) = 0.
        circulation = tex(
            r"\oint_C \mathbf{E}\cdot d\boldsymbol{\ell}=0",
            25, YELLOW,
        ).move_to([3.0, -2.08, 0])

        self.play(
            FadeIn(source), Create(gauss_surface),
            LaggedStart(*[GrowArrow(a) for a in outward], lag_ratio=0.08),
            Write(gauss), FadeIn(source_caption), run_time=2.4,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in uniform], lag_ratio=0.018),
            run_time=1.7,
        )
        self.play(
            Create(loop), FadeIn(loop_label),
            Write(curl), FadeIn(curl_caption), run_time=1.6,
        )
        # The white dot traces the *chosen path*, not fluid/field rotation.
        # The green field arrows remain fixed throughout the traversal.
        self.add(loop_marker)
        self.play(
            MoveAlongPath(loop_marker, loop.copy()),
            run_time=2.4, rate_func=linear,
        )
        self.play(Write(circulation), run_time=1.1)
        self.play(
            Indicate(gauss, color=BLUE), Indicate(curl, color=GREEN),
            run_time=1.1,
        )
        self.hold_to(start + 25)
        self.clear_scene()

    def potential_and_poisson(self):
        start = self.time
        self.heading("يُتيح لنا الجهد الكهربائي إيجاد المجال الكهربائي")
        mesh, contours, potential = potential_hill()
        # The projected mesh is a graph of V(x,y); its height is a scalar value.
        height_label = ar("الجهد الكهربائي", 19, YELLOW).move_to([-3.5, 2.15, 0])
        v_symbol = tex(r"V", 25, YELLOW).move_to([-3.45, 1.72, 0])
        x_axis = Line([-5.2, -1.55, 0], [-1.7, -1.55, 0], color=GREY, stroke_width=1.2)
        y_axis = Line([-5.2, -1.55, 0], [-4.0, -2.15, 0], color=GREY, stroke_width=1.2)
        x_tag, y_tag = tex("x", 20, GREY).next_to(x_axis, RIGHT, buff=0.05), tex("y", 20, GREY).next_to(y_axis, DOWN, buff=0.02)
        ball_path = VMobject().set_points_smoothly([
            hill_projection(x, 0, potential(x, 0), (-3.45, -0.25, 0))
            for x in np.linspace(0.0, 1.55, 60)
        ]).set_stroke(YELLOW, width=2.3)
        bead = Dot(ball_path.get_start(), radius=0.07, color=WHITE)
        pos = hill_projection(0.78, 0, potential(0.78, 0), (-3.45, -0.25, 0))
        end = hill_projection(1.28, 0, potential(1.28, 0), (-3.45, -0.25, 0))
        electric_arrow = Arrow(pos, end, buff=0, color=BLUE, stroke_width=4)
        relation = tex(r"\mathbf{E}=-\nabla V", 39, YELLOW).move_to([3.65, 1.75, 0])
        relation_words = ar("يمكن إيجاد المجال الكهربائي عن طريق حساب تدرج الجهد.", 19, WHITE).move_to([3.65, 1.0, 0])
        self.play(LaggedStart(*[Create(line) for line in mesh], lag_ratio=0.035), run_time=3.3)
        self.play(LaggedStart(*[Create(c) for c in contours], lag_ratio=0.2),
                  FadeIn(height_label), FadeIn(v_symbol), Create(x_axis), Create(y_axis), FadeIn(x_tag), FadeIn(y_tag), run_time=1.6)
        self.play(Create(ball_path), FadeIn(bead), MoveAlongPath(bead, ball_path), run_time=3.0)
        self.play(GrowArrow(electric_arrow), Write(relation), FadeIn(relation_words), run_time=1.5)
        self.wait(1.0)
        self.clear_scene()

        self.heading("يمكننا الانتقال من قانون غاوس إلى معادلة بواسون.")
        law = tex(r"\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}", 39, BLUE).move_to([0, 1.7, 0])
        potential_relation = tex(r"\mathbf{E}=-\nabla V", 37, YELLOW).move_to([0, 0.8, 0])
        substitution = tex(r"\nabla\cdot(-\nabla V)=\frac{\rho}{\varepsilon_0}", 34, WHITE).move_to([0, -0.2, 0])
        laplacian = tex(r"-\nabla^2V=\frac{\rho}{\varepsilon_0}", 37, WHITE).move_to([0, -1.05, 0])
        result = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 44, YELLOW).move_to([0, -2.15, 0])
        result_box = SurroundingRectangle(result, color=YELLOW, buff=0.14, stroke_width=2)
        self.play(Write(law), run_time=1.2)
        self.play(Write(potential_relation), run_time=1.1)
        self.play(Write(substitution), run_time=1.4)
        self.play(TransformMatchingShapes(substitution, laplacian), run_time=1.4)
        self.play(Write(result), Create(result_box), run_time=1.4)
        self.play(Indicate(result, color=YELLOW), run_time=0.9)
        self.hold_to(start + 40)
        self.clear_scene()

    def curl_identity(self):
        """Show zero curl using a genuine gradient and a CLOSED test path.

        The blue arrows are the gradient of V(x,y) = 1/2 [x^2 + (y/b)^2]
        in coordinates relative to the diagram's centre.  Its equipotentials
        are ellipses, so every arrow is exactly normal to its local contour.

        The yellow circle is a chosen integration path C, NOT a streamline or
        a representation of the curl.  The yellow tangent is d-ell, whereas
        the moving blue arrow is grad(V) sampled at the white marker.
        """
        start = self.time
        self.heading("انعدام دوران المجال الكهربائي")

        center = np.array([-3.50, -0.28, 0.0])
        aspect = 0.625

        def gradient_at(point):
            """grad V for V = (dx^2 + (dy/aspect)^2)/2."""
            relative = np.asarray(point, dtype=float) - center
            return np.array([relative[0], relative[1] / aspect**2, 0.0])

        # Genuine equipotentials: V = r^2/2 (ellipses with aspect b/a).
        levels = VGroup()
        for radius, color in [
            (0.45, YELLOW), (0.80, BLUE), (1.15, BLUE),
            (1.50, BLUE), (1.85, BLUE),
        ]:
            levels.add(
                Ellipse(width=2 * radius, height=2 * aspect * radius,
                        color=color, stroke_width=1.7).move_to(center)
            )

        # The blue field arrows point in the analytically correct grad(V)
        # direction, perpendicular to the elliptical equipotential lines.
        gradient_arrows = VGroup()
        for radius, count in [(0.78, 12), (1.36, 16)]:
            for theta in np.linspace(0, TAU, count, endpoint=False):
                p = center + np.array([
                    radius * np.cos(theta),
                    aspect * radius * np.sin(theta),
                    0.0,
                ])
                g = gradient_at(p)
                unit_g = g / np.linalg.norm(g)
                gradient_arrows.add(
                    Arrow(p, p + 0.30 * unit_g,
                          buff=0, color=BLUE, stroke_width=2.4,
                          max_tip_length_to_length_ratio=0.29)
                )

        # C is deliberately offset from the potential minimum, so the
        # potential changes along C even though the TOTAL circulation is zero.
        loop_center = center + np.array([0.40, -0.09, 0.0])
        loop_radius = 0.73
        loop = Circle(radius=loop_radius, color=YELLOW,
                      stroke_width=3.1).move_to(loop_center)
        loop_label = tex(r"C", 21, YELLOW).move_to(
            loop_center + np.array([loop_radius + 0.15, -0.08, 0.0])
        )
        path_caption = ar("مسار تكامل مغلق", 17, YELLOW).move_to([-3.5, -2.05, 0])
        level_label = tex(r"V=c", 23, YELLOW).move_to([-5.20, 1.45, 0])
        gradient_label = tex(r"\nabla V", 22, BLUE).move_to([-1.77, 1.45, 0])

        # White marker traverses C.  The moving BLUE arrow samples grad(V),
        # and the YELLOW tangent shows d-ell for the line integral.  They are
        # independent: the yellow tangent is not the direction of the field.
        angle = ValueTracker(0.0)

        def point_on_loop():
            t = angle.get_value()
            return loop_center + loop_radius * np.array([
                np.cos(t), np.sin(t), 0.0,
            ])

        moving_point = always_redraw(
            lambda: Dot(point_on_loop(), radius=0.063, color=WHITE)
        )

        def local_gradient_arrow():
            p = point_on_loop()
            g = gradient_at(p)
            return Arrow(
                p, p + 0.32 * g / np.linalg.norm(g),
                buff=0, color=BLUE, stroke_width=3.6,
                max_tip_length_to_length_ratio=0.30,
            )

        moving_field = always_redraw(local_gradient_arrow)

        def local_path_tangent():
            t = angle.get_value()
            p = point_on_loop()
            tangent = np.array([-np.sin(t), np.cos(t), 0.0])
            return Arrow(
                p, p + 0.28 * tangent,
                buff=0, color=YELLOW, stroke_width=3.0,
                max_tip_length_to_length_ratio=0.34,
            )

        moving_tangent = always_redraw(local_path_tangent)

        relation = tex(r"\nabla\times(-\nabla V)=0", 33, WHITE).move_to([3.55, 1.55, 0])
        circulation = tex(
            r"\oint_C\nabla V\cdot d\boldsymbol{\ell}=0",
            29, GREEN,
        ).move_to([3.55, 0.50, 0])
        identity = tex(r"\nabla\times(\nabla V)=0", 34, YELLOW).move_to([3.55, -0.55, 0])
        statement = ar("انعدام الدوران المحلي لتدرج الجهد", 19, GREY).move_to([3.55, -1.60, 0])

        self.play(LaggedStart(*[Create(level) for level in levels], lag_ratio=0.18),
                  run_time=1.75)
        self.play(LaggedStart(*[GrowArrow(a) for a in gradient_arrows], lag_ratio=0.022),
                  run_time=1.80)
        self.play(FadeIn(level_label), FadeIn(gradient_label),
                  Create(loop), FadeIn(loop_label), FadeIn(path_caption),
                  run_time=1.15)
        self.add(moving_field, moving_tangent, moving_point)
        self.play(angle.animate.set_value(TAU), run_time=3.4, rate_func=linear)
        self.play(Write(relation), Write(circulation), run_time=1.65)
        self.play(Write(identity), FadeIn(statement), run_time=1.30)
        self.play(Circumscribe(identity, color=YELLOW), run_time=0.85)
        self.hold_to(start + 18)
        self.clear_scene()

    def boundary_and_close(self):
        start = self.time
        self.heading("حل الجهد ثم استخراج المجال")
        x, y, rho, potential, boundary_value = poisson_example()
        axes = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=4.25, y_length=4.25,
                    tips=False, axis_config={"color": GREY, "stroke_width": 1,
                                             "include_ticks": False, "include_numbers": False})\
                    .move_to([-3.3, -0.05, 0])
        frame = Rectangle(width=4.25, height=4.25, color=GREEN, stroke_width=2.2).move_to(axes)
        image = field_image(potential, 4.25, 4.25, axes.get_center(),
                            boundary_value, float(potential.max()))
        boundary_dots = VGroup(*[
            Dot(axes.c2p(px, py), radius=0.031, color=GREEN)
            for px, py in [*((float(v), -2.0) for v in x[::4]),
                           *((float(v), 2.0) for v in x[::4]),
                           *((-2.0, float(v)) for v in y[1:-1:4]),
                           *((2.0, float(v)) for v in y[1:-1:4])]
        ])
        source = Dot(axes.c2p(0, 0), radius=0.09, color=RED)
        boundary_label = ar("الشروط الحدية المناسبة", 18, GREEN).move_to([-3.3, 2.28, 0])
        # potential is [y, x]; np.gradient returns (dV/dy, dV/dx).
        dVdy, dVdx = np.gradient(potential, y[1]-y[0], x[1]-x[0])
        arrows = VGroup()
        for j in range(4, len(y)-4, 6):
            for i in range(4, len(x)-4, 6):
                vector = np.array([-dVdx[j, i], -dVdy[j, i]])
                magnitude = np.linalg.norm(vector)
                if magnitude < 1e-8:
                    continue
                p = np.array([x[i], y[j]])
                q = p + 0.2*vector/magnitude
                arrows.add(Arrow(axes.c2p(*p), axes.c2p(*q), buff=0,
                                 color=BLUE, stroke_width=1.8,
                                 max_tip_length_to_length_ratio=0.3))
        pde = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 33, YELLOW).move_to([3.45, 1.6, 0])
        boundary = tex(r"V_{\partial\Omega}=V_b", 29, GREEN).move_to([3.45, 0.65, 0])
        result = tex(r"\mathbf{E}=-\nabla V", 38, BLUE).move_to([3.45, -0.35, 0])
        equivalent = ar("طريقة مكافئة للتكامل المباشر", 19, WHITE).move_to([3.45, -1.2, 0])
        math_tools = ar("وتفتح المجال أمام أدوات رياضية وعددية", 18, GREY).move_to([3.45, -1.95, 0])
        routes = VGroup(
            tex(r"\int \rho\,d\tau'", 24, YELLOW).move_to([2.15, -2.8, 0]),
            tex(r"\nabla^2V", 24, BLUE).move_to([4.45, -2.8, 0]),
            Arrow([2.85, -2.8, 0], [3.75, -2.8, 0], buff=0, color=WHITE, stroke_width=2.0),
        )
        self.play(Create(frame), FadeIn(axes), FadeIn(boundary_label), run_time=1.0)
        self.play(FadeIn(image), LaggedStart(*[FadeIn(d) for d in boundary_dots], lag_ratio=0.009), run_time=1.8)
        self.play(FadeIn(source), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.012), run_time=1.8)
        self.play(Write(pde), Write(boundary), run_time=1.2)
        self.play(Write(result), FadeIn(equivalent), FadeIn(math_tools), run_time=1.3)
        self.play(FadeIn(routes), Indicate(boundary, color=GREEN), run_time=1.2)
        self.hold_to(start + 28)
        self.clear_scene()


if __name__ == "__main__":
    run(PoissonIntroduction)
