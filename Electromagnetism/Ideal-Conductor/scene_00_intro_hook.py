from dataclasses import dataclass
import importlib
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import numpy as np
from manim import *

from settings import BACKGROUND, CYAN, GOLD, WHITE
from support import ar
from tools import emphasize, field_arrows
from math_type import tex
from raji_sci.em.field_lines import trace_field_line
from raji_sci.physics.electrostatics_logic import contour_paths
from raji_sci.physics.field_visuals import ScalarFieldImage, polyline


# Load the supplied toolkit under a private package name. The lesson project
# already has its own tools.py, so adding the toolkit directory to sys.path
# would silently import the wrong module from techniques.py.
TOOLKIT_ROOT = Path(
    r"C:\Users\Bruker\Desktop\Creative softwares\YouTube\Libraries\manim_toolkit"
)
if not TOOLKIT_ROOT.is_dir():
    raise FileNotFoundError(f"Manim toolkit folder not found: {TOOLKIT_ROOT}")

_TOOLKIT_PACKAGE = "ideal_conductor_manim_toolkit"
if _TOOLKIT_PACKAGE not in sys.modules:
    _package = ModuleType(_TOOLKIT_PACKAGE)
    _package.__path__ = [str(TOOLKIT_ROOT)]
    sys.modules[_TOOLKIT_PACKAGE] = _package

_toolkit_tools = importlib.import_module(f"{_TOOLKIT_PACKAGE}.tools")
_toolkit_library = importlib.import_module(f"{_TOOLKIT_PACKAGE}.useful_libraries")
_project_tools = sys.modules.get("tools")
if _project_tools is None:
    raise ImportError("The lesson project's shared tools.py must load before the toolkit")
sys.modules["tools"] = _toolkit_tools
try:
    _toolkit_techniques = importlib.import_module(f"{_TOOLKIT_PACKAGE}.techniques")
finally:
    sys.modules["tools"] = _project_tools

toolkit = SimpleNamespace(
    ChargedParticle=_toolkit_tools.ChargedParticle,
    CrystalLattice=_toolkit_tools.CrystalLattice,
    FlowParticles=_toolkit_tools.FlowParticles,
    conductor_track=_toolkit_tools.conductor_track,
    FieldLineBundle=_toolkit_tools.FieldLineBundle,
    VectorArrowGrid=_toolkit_tools.VectorArrowGrid,
    EquipotentialContours=_toolkit_tools.EquipotentialContours,
    potential_aurora=_toolkit_tools.potential_aurora,
    scalar_grid=_toolkit_library.scalar_grid,
    NeutralConductingSphere=_toolkit_library.NeutralConductingSphere,
    equation_impact=_toolkit_techniques.equation_impact,
    travelling_pulse=_toolkit_techniques.travelling_pulse,
    live_trajectory=_toolkit_techniques.live_trajectory,
    staggered_reveal=_toolkit_techniques.staggered_reveal,
)


ROOT = Path(__file__).resolve().parent
SEGMENTS = json.loads((ROOT / "intro_hook_segments.json").read_text(encoding="utf-8"))
RED = "#ff5d66"
ORANGE = "#ff9847"
METAL = "#9bb2bd"
DEEP_BLUE = "#061a25"


@dataclass(frozen=True)
class HookTiming:
    seconds: tuple[float, ...]

    @classmethod
    def from_json(cls, rows):
        return cls(tuple(float(row["estimated_seconds"]) for row in rows))


TIMING = HookTiming.from_json(SEGMENTS)


def glow_dot(color=CYAN, radius=0.055, opacity=1.0):
    return VGroup(
        Circle(radius=radius * 4.3, stroke_width=0, fill_color=color, fill_opacity=.028 * opacity),
        Circle(radius=radius * 2.5, stroke_width=0, fill_color=color, fill_opacity=.08 * opacity),
        Circle(radius=radius * 1.55, stroke_width=0, fill_color=color, fill_opacity=.18 * opacity),
        Dot(radius=radius, color=color, fill_opacity=opacity),
    )


def metallic_ring(radius=1.7, center=ORIGIN):
    ring = VGroup(
        Circle(radius=radius + .16, stroke_color=CYAN, stroke_width=12, stroke_opacity=.055),
        Circle(radius=radius + .08, stroke_color="#355564", stroke_width=18, stroke_opacity=.75),
        Circle(radius=radius, stroke_color="#b9d3dd", stroke_width=7, stroke_opacity=.9),
        Circle(radius=radius - .06, stroke_color="#304957", stroke_width=4, stroke_opacity=.9),
        Circle(radius=radius - .12, stroke_color=CYAN, stroke_width=2, stroke_opacity=.35),
    )
    return ring.move_to(center)


def metallic_sphere(radius=1.45, center=ORIGIN, wireframe=False):
    body = VGroup()
    if not wireframe:
        for index in range(22):
            shade = interpolate_color(ManimColor("#041016"), ManimColor("#6f8792"), index / 27)
            body.add(Circle(radius=radius * (1 - index / 27), stroke_width=0,
                            fill_color=shade, fill_opacity=.23).move_to(
                                center + np.array([-.021 * index, .018 * index, 0])))
    body.add(Circle(radius=radius, stroke_color="#b8d1dc", stroke_width=2.4).move_to(center))
    body.add(Ellipse(width=2 * radius, height=.48 * radius, color=CYAN,
                     stroke_width=1.1, stroke_opacity=.42).move_to(center))
    body.add(Ellipse(width=.55 * radius, height=2 * radius, color=CYAN,
                     stroke_width=1.1, stroke_opacity=.38).move_to(center))
    body.add(Ellipse(width=1.3 * radius, height=2 * radius, color=CYAN,
                     stroke_width=.8, stroke_opacity=.22).move_to(center))
    return body


def lattice_wire(y, color, ideal=False):
    body = RoundedRectangle(width=10.7, height=1.15, corner_radius=.38,
                            fill_color="#07131a", fill_opacity=.96,
                            stroke_color=color, stroke_width=2.2).move_to([0, y, 0])
    rails = VGroup(
        Line([-5.0, y + .39, 0], [5.0, y + .39, 0], color=color, stroke_width=1.1, stroke_opacity=.5),
        Line([-5.0, y - .39, 0], [5.0, y - .39, 0], color=color, stroke_width=1.1, stroke_opacity=.5),
    )
    ions = VGroup()
    for x in np.linspace(-4.65, 4.65, 15):
        ion = VGroup(Circle(radius=.13, stroke_color=GOLD, stroke_width=1,
                            fill_color="#6a3918", fill_opacity=.32),
                     Text("+", font="Arial", font_size=14, color=GOLD)).move_to([x, y, 0])
        ions.add(ion)
    if ideal:
        ions.set_opacity(.34)
    return VGroup(body, rails, ions)


def arrow_field(points, vectors, color=GOLD, max_length=.55, reference=.35):
    return field_arrows(np.asarray(points, dtype=float), np.asarray(vectors, dtype=float),
                        max_length=max_length, color=color, reference=reference,
                        stroke_width=2.2)


def conductor_sphere_field(point):
    x, y = float(point[0]), float(point[1])
    radius_squared = x * x + y * y
    if radius_squared <= 1.0:
        return np.zeros(2)
    radius = np.sqrt(radius_squared)
    return np.array([1 - 1 / radius**3 + 3 * x * x / radius**5,
                     3 * x * y / radius**5])


def potential_of_conducting_cylinder(points):
    points = np.asarray(points, dtype=float)
    x = points[..., 0]
    y = points[..., 1]
    radius_squared = x * x + y * y
    safe = np.maximum(radius_squared, 1e-9)
    # Potential of a neutral conducting sphere in a uniform +x field.
    # Its gradient matches conductor_sphere_field below.
    value = -x * (1 - 1 / safe**1.5)
    return np.where(radius_squared <= 1.0, 0.0, value)


def surface_signs(center, radius, negative_side="left", count=26):
    signs = VGroup()
    for angle in np.linspace(0, TAU, count, endpoint=False):
        cosine = np.cos(angle)
        is_negative = cosine < 0 if negative_side == "left" else cosine > 0
        color = CYAN if is_negative else RED
        sign = "−" if is_negative else "+"
        marker = Text(sign, font="Arial", font_size=21, color=color)
        marker.move_to(center + radius * np.array([np.cos(angle), np.sin(angle), 0]))
        marker.set_opacity(.42 + .58 * abs(cosine))
        signs.add(marker)
    return signs


class IdealConductorHook(MovingCameraScene):
    def hold_to_segment_end(self, segment_index, started_at, trackers=()):
        remaining = max(0.0, TIMING.seconds[segment_index] - (self.time - started_at))
        if remaining <= 0:
            return
        self.wait(remaining)

    def arabic_heading(self, text, size=38, color=WHITE, y=3.23):
        heading = ar(text, size=size, color=color, max_width=11.5).move_to([0, y, 0])
        underline = Line([heading.get_left()[0], y - .34, 0],
                         [heading.get_right()[0], y - .34, 0],
                         color=color, stroke_width=1.4, stroke_opacity=.55)
        return VGroup(heading, underline)

    def ambient_particles(self):
        particles = VGroup()
        for index in range(36):
            rng = np.random.default_rng(3100 + index)
            dot = Dot([rng.uniform(-7.0, 7.0), rng.uniform(-3.85, 3.85), 0],
                      radius=rng.uniform(.007, .019), color=CYAN)
            dot.set_opacity(rng.uniform(.08, .28))
            particles.add(dot)
        return particles

    def construct(self):
        self.camera.background_color = BACKGROUND
        self.camera.frame.save_state()
        ambient = self.ambient_particles()
        self.add(ambient)
        flow_clock = ValueTracker(0)
        flow_clock.add_updater(lambda tracker, dt: tracker.increment_value(dt))
        self.add(flow_clock)

        self.forever_current(flow_clock)
        self.no_resistance(flow_clock)
        self.science_fiction_ring(flow_clock)
        self.introduce_ideal_conductor(flow_clock)
        self.theoretical_model(flow_clock)
        self.why_study_it(flow_clock)
        self.surface_redistribution(flow_clock)
        self.zero_internal_field(flow_clock)
        self.induction_without_contact(flow_clock)
        self.final_reveal(flow_clock, ambient)

    def forever_current(self, clock):
        started = self.time
        path = Arc(radius=1.72, start_angle=PI, angle=-TAU * .76)
        electron = glow_dot(radius=.085).move_to(path.get_start())
        trail = TracedPath(electron.get_center, stroke_color=CYAN,
                           stroke_width=3.2, dissipating_time=1.15)
        self.add(trail, electron)
        self.wait(.35)
        self.play(MoveAlongPath(electron, path),
                  self.camera.frame.animate.scale(1.12), run_time=2.1, rate_func=rush_into)
        current_path = Circle(radius=1.72, stroke_width=0).set_stroke(opacity=0)
        ring = toolkit.conductor_track(current_path, color=METAL,
                                       inner_color=CYAN, width=11)
        orbiters = toolkit.FlowParticles(current_path, count=20, radius=.035,
                                         color=CYAN)
        orbiters.phase.add_updater(
            lambda phase, dt: phase.set_value(clock.get_value() * 1.8)
        )
        energy_title = ar("الطاقة محفوظة", size=29, color=WHITE,
                          max_width=3.3).move_to([4.25, .72, 0])
        energy_value = tex(r"100\%", size=52, color=CYAN).move_to([4.25, -.05, 0])
        gauge_shell = RoundedRectangle(width=2.45, height=.36, corner_radius=.14,
                                       color=METAL, stroke_width=1.2).move_to([4.25, -.82, 0])
        gauge_fill = RoundedRectangle(width=2.32, height=.23, corner_radius=.1,
                                      stroke_width=0, fill_color=CYAN,
                                      fill_opacity=.9).move_to(gauge_shell)
        currents = VGroup(*[Arc(radius=2.1 + .17 * i, start_angle=.2,
                                angle=TAU * .78, color=CYAN, stroke_width=1.1,
                                stroke_opacity=.18) for i in range(3)])
        self.play(FadeOut(electron), FadeOut(trail), FadeIn(ring), FadeIn(orbiters),
                  LaggedStart(*[Create(arc) for arc in currents], lag_ratio=.12), run_time=1.35)
        self.play(FadeIn(energy_title, shift=UP * .12), Write(energy_value),
                  FadeIn(gauge_shell), GrowFromEdge(gauge_fill, LEFT), run_time=1.15)
        self.play(
                  *[ShowPassingFlash(arc.copy().set_stroke(width=3), time_width=.18)
                    for arc in currents], run_time=2, rate_func=linear)
        self.hold_to_segment_end(0, started, (clock,))
        self._current_group = VGroup(ring, orbiters, currents, energy_title,
                                     energy_value, gauge_shell, gauge_fill)

    def no_resistance(self, clock):
        started = self.time
        hot_wire = lattice_wire(1.35, ORANGE, ideal=False)
        ideal_wire = lattice_wire(-1.15, CYAN, ideal=True)
        labels = VGroup(
            ar("موصل ذو مقاومة", size=25, color=ORANGE, max_width=3.2).move_to([3.85, 2.28, 0]),
            ar("موصل مثالي", size=27, color=CYAN, max_width=3.0).move_to([4.25, -.22, 0]))
        self.play(FadeOut(self._current_group), self.camera.frame.animate.restore(),
                  FadeIn(hot_wire, shift=RIGHT * .35),
                  FadeIn(ideal_wire, shift=LEFT * .35), FadeIn(labels), run_time=1.2)
        hot_electrons = VGroup()
        ideal_electrons = VGroup()
        hot_paths = VGroup()
        for index in range(8):
            x0 = -4.7 + index * 1.15
            points = np.array([[x0, 1.35], [x0 + .38, 1.55],
                               [x0 + .72, 1.12], [x0 + 1.05, 1.35]])
            hot_paths.add(polyline(points, color=ORANGE, stroke_width=1.5, smooth=False))
            hot_electrons.add(glow_dot(CYAN, .036).move_to([x0, 1.35, 0]))
        for index in range(11):
            phase = index / 11
            electron = glow_dot(CYAN, .037)
            electron.add_updater(lambda mob, phase=phase: mob.move_to([
                -4.75 + 9.5 * ((phase + .105 * clock.get_value()) % 1), -1.15, 0]))
            ideal_electrons.add(electron)
        heat = VGroup(*[AnnularSector(inner_radius=.16, outer_radius=.3 + .05 * (i % 3),
                                      angle=PI * .72, start_angle=PI * .14,
                                      fill_color=ORANGE, fill_opacity=.28,
                                      stroke_width=0).move_to([-3.8 + i * 1.27, 1.35, 0])
                        for i in range(7)])
        self.play(FadeIn(hot_electrons), FadeIn(ideal_electrons),
                  LaggedStart(*[Create(path) for path in hot_paths], lag_ratio=.06), run_time=1.0)
        self.play(*[MoveAlongPath(dot, path, rate_func=linear)
                    for dot, path in zip(hot_electrons, hot_paths)],
                  FadeIn(heat, scale=.55),
                  run_time=2.4, rate_func=linear)
        power = tex(r"P=I^2R", size=39, color=ORANGE).move_to([-3.95, 2.35, 0])
        ideal_eq = tex(r"R=0\quad\Longrightarrow\quad P=0", size=40,
                       color=CYAN, width=5.0).move_to([0, -2.62, 0])
        self.play(Write(power), Write(ideal_eq), heat.animate.set_opacity(.12), run_time=1.25)
        emphasize(self, ideal_eq, color=CYAN, run_time=.8)
        self.hold_to_segment_end(1, started, (clock,))
        self._wire_group = VGroup(hot_wire, ideal_wire, labels, hot_electrons,
                                  ideal_electrons, hot_paths, heat, power, ideal_eq)

    def science_fiction_ring(self, clock):
        started = self.time
        ring = metallic_ring(1.85)
        halo = VGroup(*[Circle(radius=2.2 + .22 * i, color=CYAN,
                              stroke_width=1.1, stroke_opacity=.18 / (i + 1))
                        for i in range(4)])
        sparks = VGroup(*[glow_dot(CYAN, .022).move_to(
            (2.45 + .16 * np.sin(i * 2.1)) * np.array([
                np.cos(TAU * i / 24), np.sin(TAU * i / 24), 0])) for i in range(24)])
        question = self.arabic_heading("هل يبدو هذا خيالًا علميًا؟",
                                       size=35, color=WHITE, y=-2.75)
        self.play(FadeOut(self._wire_group), FadeIn(ring, scale=.72), FadeIn(halo),
                  LaggedStart(*[FadeIn(s, scale=.2) for s in sparks], lag_ratio=.025),
                  run_time=1.35)
        self.play(Rotate(ring, angle=PI / 4), Rotate(halo, angle=-PI / 5),
                  self.camera.frame.animate.scale(.86), run_time=1.4)
        self.play(FadeIn(question, shift=UP * .14),
                  *[ShowPassingFlash(c.copy().set_stroke(width=3), time_width=.16)
                    for c in halo], run_time=1.0)
        self.hold_to_segment_end(2, started, (clock,))
        self._fiction_group = VGroup(ring, halo, sparks, question)

    def introduce_ideal_conductor(self, clock):
        started = self.time
        sphere = metallic_sphere(1.55)
        title = self.arabic_heading("الموصل المثالي", size=50, color=WHITE, y=2.95)
        sigma = tex(r"\sigma\rightarrow\infty", size=53, color=CYAN).move_to([-4.2, .65, 0])
        resistance = tex(r"R=0", size=55, color=GOLD).move_to([4.2, .65, 0])
        arrows = VGroup(Arrow([-5.0, -.8, 0], [-2.15, -.8, 0], color=CYAN,
                              stroke_width=3, buff=0),
                        Arrow([2.15, -.8, 0], [5.0, -.8, 0], color=CYAN,
                              stroke_width=3, buff=0))
        carriers = VGroup()
        for index in range(18):
            angle = TAU * index / 18
            carrier = glow_dot(CYAN, .029)
            carrier.add_updater(lambda mob, angle=angle: mob.move_to(
                1.55 * np.array([np.cos(angle - .55 * clock.get_value()),
                                 np.sin(angle - .55 * clock.get_value()), 0])))
            carriers.add(carrier)
        self.play(ReplacementTransform(self._fiction_group[0], sphere),
                  FadeOut(VGroup(*self._fiction_group[1:])),
                  self.camera.frame.animate.restore(), run_time=1.55)
        self.play(LaggedStart(FadeIn(title), Write(sigma), Write(resistance), lag_ratio=.17),
                  run_time=2.1)
        self.play(FadeIn(carriers), GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  run_time=2.5, rate_func=linear)
        equation_arc = ArcBetweenPoints(sigma.get_right(), resistance.get_left(),
                                        angle=-PI / 2, color=CYAN, stroke_width=2)
        self.play(Create(equation_arc), Circumscribe(sphere, color=CYAN, fade_out=True),
                  run_time=1.2)
        toolkit.equation_impact(self, resistance, color=GOLD, run_time=.8)
        self.play(ShowPassingFlash(equation_arc.copy().set_stroke(width=6), time_width=.22),
                  run_time=2.4, rate_func=linear)
        zero_loss = ar("تتحرك الشحنات دون فقدٍ للطاقة", size=29, color=WHITE,
                       max_width=6.4).move_to([0, -2.73, 0])
        self.play(FadeIn(zero_loss, shift=UP * .12), arrows.animate.set_color(GOLD),
                  run_time=1.15)
        self.hold_to_segment_end(3, started, (clock,))
        self._ideal_group = VGroup(sphere, title, sigma, resistance, arrows,
                                   carriers, equation_arc, zero_loss)

    def theoretical_model(self, clock):
        started = self.time
        wireframe = metallic_sphere(1.55, wireframe=True)
        axes = VGroup(DashedLine([-3.1, 0, 0], [3.1, 0, 0], dash_length=.14,
                                 color=GOLD, stroke_opacity=.5),
                      DashedLine([0, -2.35, 0], [0, 2.35, 0], dash_length=.14,
                                 color=GOLD, stroke_opacity=.5))
        rings = VGroup(*[Circle(radius=r, color=CYAN, stroke_width=.9,
                               stroke_opacity=.22) for r in [1.9, 2.3, 2.7]])
        model_text = self.arabic_heading("نموذجٌ نظري", size=42, color=GOLD, y=2.9)
        ideal_eq = tex(r"\rho=0\qquad \mathbf{E}=0",
                       size=43, color=WHITE, width=7.4).move_to([0, -2.85, 0])
        self.play(FadeOut(VGroup(*self._ideal_group[1:])),
                  Transform(self._ideal_group[0], wireframe), FadeIn(axes), FadeIn(rings),
                  run_time=1.75)
        sphere = self._ideal_group[0]
        self.play(FadeIn(model_text, shift=DOWN * .12), Write(ideal_eq),
                  Rotate(rings, angle=PI / 7), run_time=1.55)
        scan = Line([-1.6, 1.6, 0], [1.6, 1.6, 0], color=CYAN,
                    stroke_width=3, stroke_opacity=.7)
        self.play(scan.animate.shift(DOWN * 3.2), Rotate(sphere, angle=PI / 6),
                  run_time=2.2, rate_func=linear)
        self.play(FadeOut(scan), Indicate(model_text, color=GOLD),
                  *[ShowPassingFlash(r.copy().set_stroke(width=3), time_width=.2)
                    for r in rings], run_time=1.35)
        self.hold_to_segment_end(4, started, (clock,))
        self._model_group = VGroup(sphere, axes, rings, model_text, ideal_eq)

    def why_study_it(self, clock):
        started = self.time
        self.play(FadeOut(self._model_group), run_time=.7)
        question = ar("لماذا ندرس نموذجًا مثاليًا؟", size=44, color=WHITE,
                      max_width=8.5).move_to([0, 2.95, 0])
        question_line = Underline(question, color=CYAN, stroke_width=1.5)
        real_body = RoundedRectangle(width=4.75, height=3.65, corner_radius=.7,
                                     fill_color="#111519", fill_opacity=.96,
                                     stroke_color=ORANGE, stroke_width=2).move_to([-3.35, -.05, 0])
        ideal_body = Circle(radius=1.78, fill_color=DEEP_BLUE, fill_opacity=.78,
                            stroke_color=CYAN, stroke_width=2.4).move_to([3.35, -.05, 0])
        real_label = ar("التفاصيل المعقّدة", size=25, color=ORANGE,
                        max_width=3.8).move_to([-3.35, -2.35, 0])
        ideal_label = ar("القانون الواضح", size=27, color=CYAN,
                         max_width=3.8).move_to([3.35, -2.35, 0])
        lattice = toolkit.CrystalLattice(
            rows=6, cols=9, spacing=.42, stagger=True,
            bond_opacity=.25, ion_radius=.065, color=GOLD,
        ).move_to([-3.35, -.05, 0])
        collisions = VGroup(*[polyline(
            np.array([[-4.9 + .65 * i, .2], [-4.55 + .65 * i, .5],
                      [-4.15 + .65 * i, -.07]]), color=ORANGE,
            stroke_width=1.5, smooth=False) for i in range(5)])
        self.play(FadeIn(question, shift=DOWN * .12), Create(question_line), run_time=1.0)
        self.play(FadeIn(real_body),
                  LaggedStart(*[FadeIn(ion, scale=.2) for ion in lattice], lag_ratio=.018),
                  FadeIn(collisions), FadeIn(real_label), run_time=1.7)
        self.play(FadeIn(ideal_body, scale=.7), FadeIn(ideal_label), run_time=1.1)
        points = np.array([[x, y] for x in np.linspace(1.45, 5.25, 7)
                           for y in np.linspace(-1.35, 1.25, 5)])
        local = (points - np.array([3.35, -.05])) / 1.78
        mask = np.linalg.norm(local, axis=1) > 1.05
        field = arrow_field(points[mask], np.tile([1.0, 0.0], (mask.sum(), 1)),
                            color=GOLD, max_length=.34, reference=.5)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in field], lag_ratio=.02),
                  run_time=1.25)
        simplify_arrows = VGroup(*[Arrow([-1.0, y, 0], [1.0, y, 0], color=WHITE,
                                         stroke_width=2,
                                         max_tip_length_to_length_ratio=.13)
                                    for y in [-.85, -.05, .75]])
        self.play(lattice.animate.set_opacity(.08), collisions.animate.set_opacity(.08),
                  LaggedStart(*[GrowArrow(arrow) for arrow in simplify_arrows], lag_ratio=.1),
                  run_time=1.4)
        self.play(FadeOut(VGroup(real_body, lattice, collisions, real_label,
                                 simplify_arrows)),
                  ideal_body.animate.move_to(ORIGIN).scale(1.08),
                  ideal_label.animate.move_to([0, -2.5, 0]),
                  field.animate.shift(LEFT * 3.35), run_time=1.6)
        self.play(FadeOut(question), FadeOut(question_line), FadeOut(ideal_label),
                  FadeOut(field), run_time=.65)
        x = np.linspace(-3.15, 3.15, 121)
        y = np.linspace(-2.05, 2.05, 81)
        X, Y = np.meshgrid(x, y)
        field_model = toolkit.NeutralConductingSphere(
            center=(0.0, 0.0, 0.0), radius=1.0,
            external_position=(-4.0, 0.0, 0.0), external_charge=4.0,
        )
        values = np.array([[field_model.potential(np.array([xx, yy, 0.0]))
                            for xx in x] for yy in y])
        heatmap = ScalarFieldImage(values, width=6.3, height=4.1, center=(0, 0, 0),
                                   vmax=3.0, positive="#df8448", negative="#176b9b",
                                   zero="#02070a", opacity=.72)
        heatmap.set_z_index(-2)
        self.play(FadeIn(heatmap), ideal_body.animate.set_fill(opacity=.34),
                  self.camera.frame.animate.scale(.82), run_time=1.4)
        masked = values.copy()
        masked[X * X + Y * Y <= 1.0] = np.nan
        contours = VGroup()
        for level in [-2.2, -1.55, -.95, -.45, .45, .95, 1.55, 2.2]:
            for path in contour_paths(X, Y, masked, level):
                contours.add(polyline(path, color=CYAN if level < 0 else GOLD,
                                      stroke_width=1.45, smooth=False))
        self.play(LaggedStart(*[Create(contour) for contour in contours], lag_ratio=.035),
                  run_time=2.2)
        # A second, denser vector layer makes the field legible between contours.
        vector_grid = toolkit.VectorArrowGrid(
            field_model.field, x_range=(-5.7, 5.7), y_range=(-2.0, 2.0),
            shape=(21, 9), color=GOLD, length=.25,
            reference_magnitude=.75,
            mask=lambda p: np.linalg.norm(p[:2]) < 1.12,
        )
        vector_grid.set_opacity(.56)
        self.play(FadeIn(vector_grid), run_time=.65)
        rays = VGroup()
        for seed_y in [-1.45, -1.05, -.65, .65, 1.05, 1.45]:
            line_points = trace_field_line(
                lambda p: field_model.field(np.array([p[0], p[1], 0.0]))[:2],
                [-5.65, seed_y],
                                           step=.035, steps=190,
                                           bounds=[[-5.8, 5.8], [-2.0, 2.0]])
            if len(line_points) > 2:
                rays.add(polyline(line_points, color=WHITE, stroke_width=1.25,
                                  smooth=False))
        self.play(LaggedStart(*[Create(ray) for ray in rays], lag_ratio=.08), run_time=2.0)
        # A moving sample follows an equipotential; its live readout stays tied
        # to the same numerical potential model that generated the map.
        probe = glow_dot(CYAN, .045)
        probe_angle = ValueTracker(0.35)
        probe.add_updater(lambda mob: mob.move_to(
            2.15 * np.array([np.cos(probe_angle.get_value()),
                             np.sin(probe_angle.get_value()), 0])))
        probe_value = Text("0.00", font="Arial", font_size=25,
                           color=CYAN).move_to([4.65, .35, 0])
        probe_value.add_updater(lambda mob: mob.become(
            Text(f"{field_model.potential(probe.get_center()):+.2f}",
                 font="Arial", font_size=25, color=CYAN).move_to([4.65, .35, 0])))
        probe_label = ar("قراءة الجهد", size=22, color=WHITE,
                         max_width=2.2).move_to([4.65, .78, 0])
        self.add(probe, probe_value)
        self.play(FadeIn(probe_label),
                  probe_angle.animate.increment_value(TAU), run_time=3.8,
                  rate_func=linear)
        law = tex(r"\nabla^2V=0", size=48, color=WHITE).move_to([-4.55, 2.5, 0])
        relation = tex(r"\mathbf{E}=-\nabla V", size=43, color=CYAN).move_to([4.45, 2.5, 0])
        simple_world = ar("نزيل التعقيد لنرى القانون", size=32, color=WHITE,
                          max_width=6.5).move_to([0, -2.75, 0])
        self.play(Write(law), Write(relation), FadeIn(simple_world, shift=UP * .12),
                  run_time=1.8)
        self.play(*[ShowPassingFlash(ray.copy().set_stroke(width=4), time_width=.18)
                    for ray in rays],
                  Circumscribe(ideal_body, color=CYAN, fade_out=True), run_time=2.1)
        self.play(self.camera.frame.animate.scale(.9),
                  contours.animate.rotate(PI / 40), run_time=1.1)
        self.play(self.camera.frame.animate.restore(), Indicate(law, color=GOLD),
                  Indicate(relation, color=CYAN), run_time=1.1)
        self.hold_to_segment_end(5, started, (clock,))
        self._why_group = Group(ideal_body, heatmap, contours, vector_grid,
                                rays, probe, probe_value, probe_label,
                                law, relation, simple_world)

    def surface_redistribution(self, clock):
        started = self.time
        self.play(FadeOut(self._why_group), run_time=.8)
        heading = self.arabic_heading("كيف تعيد الشحنات توزيع نفسها؟",
                                      size=37, color=WHITE)
        body = RoundedRectangle(width=6.0, height=3.25, corner_radius=1.05,
                                fill_color="#0a1b23", fill_opacity=.92,
                                stroke_color=METAL, stroke_width=2.4).move_to([0, -.15, 0])
        inner_grid = VGroup(*[Dot([x, y, 0], radius=.022, color=METAL,
                                 fill_opacity=.28) for x in np.linspace(-2.35, 2.35, 10)
                             for y in np.linspace(-1.1, .8, 5)])
        electrons = VGroup()
        starts, targets = [], []
        rng = np.random.default_rng(42)
        for index in range(24):
            start = np.array([rng.uniform(-2.25, 2.25), rng.uniform(-1.0, .75), 0])
            angle = TAU * index / 24
            target = np.array([2.83 * np.cos(angle),
                               -.15 + 1.48 * np.sin(angle), 0])
            electrons.add(toolkit.ChargedParticle(
                charge=-1, radius=.035, color=CYAN, show_sign=False,
            ).move_to(start))
            starts.append(start)
            targets.append(target)
        density_axis = Axes(x_range=[-PI, PI, PI], y_range=[0, 1, .5],
                            x_length=3.0, y_length=1.45, tips=False,
                            axis_config={"stroke_opacity": .4,
                                         "stroke_width": 1}).move_to([4.7, -.2, 0])
        density_curve = density_axis.plot(lambda x: .35 + .55 * np.cos(x) ** 2,
                                          color=CYAN, stroke_width=2)
        density_label = tex(r"\rho_s(\theta)", size=35,
                            color=CYAN).move_to([4.7, 1.0, 0])
        self.play(FadeIn(heading), GrowFromCenter(body), FadeIn(inner_grid),
                  LaggedStart(*[FadeIn(e, scale=.2) for e in electrons], lag_ratio=.025),
                  run_time=1.5)
        paths = []
        for start, target in zip(starts, targets):
            mid = .5 * (start + target) + np.array([0, .18 * np.sign(target[1] - start[1]), 0])
            paths.append(polyline(np.array([start[:2], mid[:2], target[:2]]),
                                  color=CYAN, stroke_width=.8, smooth=True))
        self.play(*[MoveAlongPath(electron, path)
                    for electron, path in zip(electrons, paths)],
                  run_time=2.5, rate_func=smooth)
        self.play(FadeIn(density_axis), Create(density_curve), FadeIn(density_label),
                  body.animate.set_stroke(color=CYAN, width=3.0), run_time=1.5)
        tangential = VGroup(*[CurvedArrow(
            3.05 * np.array([np.cos(angle), np.sin(angle), 0]) + DOWN * .15,
            3.05 * np.array([np.cos(angle + .35), np.sin(angle + .35), 0]) + DOWN * .15,
            angle=.3, color=CYAN, stroke_width=2)
            for angle in np.linspace(.25, TAU - .6, 8)])
        self.play(LaggedStart(*[Create(a) for a in tangential], lag_ratio=.08),
                  run_time=1.3)
        self.play(*[ShowPassingFlash(path.copy().set_stroke(width=3), time_width=.2)
                    for path in paths[::3]], run_time=1.4)
        self.hold_to_segment_end(6, started, (clock,))
        self._redistribution_group = VGroup(heading, body, inner_grid, electrons,
                                            density_axis, density_curve,
                                            density_label, tangential)

    def zero_internal_field(self, clock):
        started = self.time
        heading = self.arabic_heading("لماذا ينعدم المجال داخل الموصل؟",
                                      size=37, color=WHITE)
        sphere = metallic_sphere(1.55)
        exterior_points = np.array([[x, y] for x in np.linspace(-5.8, 5.8, 13)
                                    for y in np.linspace(-1.65, 1.45, 5)])
        outside = exterior_points[np.linalg.norm(exterior_points, axis=1) > 1.85]
        outside_arrows = arrow_field(outside,
                                     np.tile([1.0, 0.0], (len(outside), 1)),
                                     color=GOLD, max_length=.48, reference=.45)
        inside_points = np.array([[x, y] for x in [-.95, -.48, 0, .48, .95]
                                  for y in [-.7, 0, .7]
                                  if x * x + y * y < 1.45**2])
        inside_arrows = arrow_field(inside_points,
                                    np.tile([1.0, 0.0], (len(inside_points), 1)),
                                    color=GOLD, max_length=.46, reference=.45)
        signs = surface_signs(ORIGIN, 1.55, negative_side="left", count=28)
        self.play(FadeOut(self._redistribution_group), FadeIn(heading), GrowFromCenter(sphere),
                  LaggedStart(*[GrowArrow(a) for a in outside_arrows], lag_ratio=.012),
                  FadeIn(inside_arrows), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(sign, scale=.35) for sign in signs],
                              lag_ratio=.025),
                  inside_arrows.animate.scale(.03).set_opacity(0), run_time=1.55)
        zero = tex(r"\mathbf{E}=0", size=55,
                   color=CYAN).move_to([3.95, -2.45, 0])
        self.play(Write(zero), Circumscribe(sphere, color=CYAN, fade_out=True),
                  run_time=1.0)
        self.hold_to_segment_end(7, started, (clock,))
        self._zero_group = VGroup(heading, sphere, outside_arrows,
                                  inside_arrows, signs, zero)

    def induction_without_contact(self, clock):
        started = self.time
        self.play(FadeOut(self._zero_group), run_time=.75)
        heading = self.arabic_heading("استقطابٌ من دون تلامس", size=39, color=WHITE)
        center = np.array([2.15, -.05, 0])
        sphere = metallic_sphere(1.65, center=center)
        source = toolkit.ChargedParticle(
            charge=1, radius=.24, color=RED, show_sign=True,
        ).move_to([-5.3, -.05, 0])
        neutral_pairs = VGroup()
        for angle in np.linspace(0, TAU, 16, endpoint=False):
            position = center + 1.64 * np.array([np.cos(angle), np.sin(angle), 0])
            neutral_pairs.add(VGroup(Text("−", font="Arial", font_size=18, color=CYAN),
                                     Text("+", font="Arial", font_size=18, color=RED))
                              .arrange(RIGHT, buff=.03).move_to(position))
        self.play(FadeIn(heading), GrowFromCenter(sphere), FadeIn(neutral_pairs),
                  FadeIn(source), run_time=1.4)
        self.play(source.animate.shift(RIGHT * 1.85), run_time=1.55,
                  rate_func=smooth)
        field_model = toolkit.NeutralConductingSphere(
            center=tuple(center), radius=1.65,
            external_position=(-3.45, -.05, 0), external_charge=1.0,
        )
        polarized = VGroup()
        for angle in np.linspace(0, TAU, 30, endpoint=False):
            position = center + 1.65 * np.array([np.cos(angle), np.sin(angle), 0])
            density = field_model.surface_induced_charge_density(position)
            sign = "−" if density < 0 else "+"
            color = CYAN if density < 0 else RED
            marker = Text(sign, font="Arial", font_size=18, color=color)
            marker.move_to(position)
            marker.set_opacity(.38 + .62 * min(1.0, abs(density) * 1.8))
            polarized.add(marker)
        self.play(ReplacementTransform(neutral_pairs, polarized), run_time=1.5)
        seeds = [np.array([-3.45 + .30 * np.cos(angle),
                           -.05 + .30 * np.sin(angle), 0])
                 for angle in np.linspace(0, TAU, 12, endpoint=False)]
        field_lines = toolkit.FieldLineBundle(
            field_model.field, seeds, color=GOLD, line_width=1.55,
            step=.055, max_steps=300,
            bounds=(-5.8, 5.8, -3.3, 3.3),
        )
        self.play(LaggedStart(*[Create(line) for line in field_lines.curves], lag_ratio=.08),
                  FadeIn(field_lines.arrows),
                  run_time=1.8)
        if len(field_lines.curves):
            toolkit.travelling_pulse(self, field_lines.curves[0], color=CYAN,
                                      width=4.2, run_time=1.1)
        balance = VGroup(tex(r"Q_{-}", size=40, color=CYAN),
                         tex(r"+", size=35, color=WHITE),
                         tex(r"Q_{+}", size=40, color=RED),
                         tex(r"=0", size=43, color=WHITE)).arrange(
                             RIGHT, buff=.16).move_to([2.15, -2.55, 0])
        net_text = ar("الشحنة الكلية تبقى صفرًا", size=27, color=WHITE,
                      max_width=4.7).move_to([2.15, -3.15, 0])
        self.play(LaggedStart(*[Write(part) for part in balance], lag_ratio=.16),
                  FadeIn(net_text, shift=UP * .12), run_time=1.5)
        self.play(*[ShowPassingFlash(line.copy().set_stroke(width=4), time_width=.2)
                    for line in field_lines.curves[::2]],
                  Indicate(balance, color=GOLD), run_time=1.65)
        self.hold_to_segment_end(8, started, (clock,))
        self._induction_group = VGroup(heading, sphere, source,
                                       polarized, field_lines, balance, net_text)

    def final_reveal(self, clock, ambient):
        started = self.time
        self.play(FadeOut(self._induction_group), run_time=.8)
        core = metallic_sphere(.78)
        symmetry = VGroup(*[Circle(radius=radius, color=CYAN, stroke_width=1.25,
                                  stroke_opacity=.18 + .08 * index)
                            for index, radius in enumerate([1.18, 1.65, 2.15, 2.72])])
        rays = VGroup(*[Line(1.0 * np.array([np.cos(angle), np.sin(angle), 0]),
                             2.85 * np.array([np.cos(angle), np.sin(angle), 0]),
                             color=GOLD, stroke_width=1.2, stroke_opacity=.5)
                        for angle in np.linspace(0, TAU, 24, endpoint=False)])
        charges = VGroup(*[glow_dot(CYAN if index % 2 == 0 else RED, .025).move_to(
            2.72 * np.array([np.cos(TAU * index / 32),
                             np.sin(TAU * index / 32), 0])) for index in range(32)])
        equations = VGroup(tex(r"R=0", size=38, color=CYAN).move_to([-4.4, 1.7, 0]),
                           tex(r"\mathbf{E}=0", size=38, color=GOLD).move_to([4.4, 1.7, 0]),
                           tex(r"\rho=0", size=38, color=GOLD).move_to([-4.4, -1.55, 0]),
                           tex(r"V=\mathrm{const.}", size=36, color=CYAN).move_to([4.4, -1.55, 0]))
        world_text = ar("لفهم العالم الحقيقي، نبدأ بعالمٍ مثالي", size=34,
                        color=WHITE, max_width=8.7).move_to([0, 3.22, 0])
        self.play(GrowFromCenter(core),
                  LaggedStart(*[Create(circle) for circle in symmetry], lag_ratio=.1),
                  LaggedStart(*[Create(ray) for ray in rays], lag_ratio=.025), run_time=1.7)
        self.play(LaggedStart(*[FadeIn(charge, scale=.2) for charge in charges],
                              lag_ratio=.02),
                  LaggedStart(*[Write(eq) for eq in equations], lag_ratio=.14),
                  FadeIn(world_text, shift=DOWN * .12), run_time=1.9)
        self.play(Rotate(symmetry, angle=PI / 8), Rotate(rays, angle=-PI / 12),
                  Rotate(charges, angle=PI / 5),
                  self.camera.frame.animate.scale(1.08), run_time=2.2)
        self.play(*[ShowPassingFlash(circle.copy().set_stroke(width=4), time_width=.18)
                    for circle in symmetry], run_time=1.4)
        composition = VGroup(core, symmetry, rays, charges, equations, world_text)
        title = ar("الموصلات المثالية", size=59, color=WHITE,
                   max_width=9.2).move_to([0, .35, 0])
        title_glow = title.copy().set_color(CYAN).set_opacity(.22).scale(1.025)
        subtitle = ar("فهم الكهرباء من خلال نموذجٍ مثالي", size=30,
                      color=CYAN, max_width=8.5).move_to([0, -.75, 0])
        rule = Line([-3.7, -1.25, 0], [3.7, -1.25, 0], color=GOLD,
                    stroke_width=1.2, stroke_opacity=.7)
        self.play(FadeOut(composition, scale=1.16), FadeIn(title_glow, scale=.82),
                  Write(title), run_time=1.7)
        self.play(Create(rule), FadeIn(subtitle, shift=UP * .12),
                  self.camera.frame.animate.restore(), run_time=1.25)
        emphasize(self, title, color=CYAN, run_time=.9)
        bridge = glow_dot(CYAN, .06).move_to([-5.5, -2.55, 0])
        bridge_path = CubicBezier([-5.5, -2.55, 0], [-2.0, -1.85, 0],
                                  [2.2, -2.9, 0], [5.6, -2.35, 0])
        bridge_trail = TracedPath(bridge.get_center, stroke_color=CYAN,
                                  stroke_width=2.5, dissipating_time=1.1)
        self.add(bridge_trail, bridge)
        self.play(MoveAlongPath(bridge, bridge_path), run_time=2.2, rate_func=linear)
        self.hold_to_segment_end(9, started, (clock,))
        self.play(FadeOut(VGroup(title_glow, title, subtitle, rule, bridge,
                                 bridge_trail, ambient)), run_time=1.0)


if __name__ == "__main__":
    from manim import tempconfig

    with tempconfig({
        "pixel_width": 1920,
        "pixel_height": 1080,
        "frame_rate": 60,
        "frame_width": 128 / 9,
        "frame_height": 8,
        "background_color": "#000000",
        "media_dir": str(ROOT / "media" / "scene_00_intro_hook"),
        "output_file": "scene_00_intro_hook",
        "preview": True,
        "disable_caching": True,
    }):
        IdealConductorHook().render()
