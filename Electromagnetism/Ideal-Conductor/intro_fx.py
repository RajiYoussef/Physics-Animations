"""Visual building blocks for the ideal-conductor introduction.

Everything here is driven by one scene clock (``CLOCK``), so objects keep moving
while the narration plays — a ``wait`` never shows a frozen frame as long as any
living object (``live_*`` helpers, ambient dust, flowing charges) is on stage.

Libraries used:
  * raji_sci  – Arabic labels, narration timing, scalar-field images, contours,
                field-line tracing, saturating field arrows
  * manim_toolkit – glow dots, glowing paths, charged particles, crystal lattice,
                flow particles, field-line bundles, wireframe sphere, the exact
                image-charge model of a neutral conducting sphere, equation effects
  * Ideas adapted (not copied) from the 3Blue1Brown videos repository:
      influence rings of a moving charge   (_2023/optics_puzzles/e_field.py)
      jiggling ions / thermal motion       (_2018/div_curl.py, JigglingSubmobjects)
      conductor bending a field around it  (_2018/div_curl.py, show_moving_charges)
"""
from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import numpy as np
from manim import *  # noqa: F401,F403 — Manim Community namespace

from settings import ARABIC_FONT, BACKGROUND, CYAN, GOLD, WHITE
from support import ar
import tools as _project_tools  # noqa: F401 — puts the Raji archive on sys.path
from math_type import tex as _math_tex
from raji_sci.em.field_lines import trace_field_line
from raji_sci.physics.electrostatics_logic import contour_paths
from raji_sci.physics.field_visuals import ScalarFieldImage, field_arrows, polyline

# ----------------------------------------------------------------------------
# Manim toolkit (loaded under a private package name: the lesson already has a
# tools.py, and the toolkit's techniques.py would otherwise import the wrong one)
# ----------------------------------------------------------------------------
TOOLKIT_ROOT = Path(os.environ.get(
    "CONDUCTOR_TOOLKIT_DIR",
    r"C:\Users\Bruker\Desktop\Creative softwares\YouTube\Libraries\manim_toolkit"))
if not TOOLKIT_ROOT.is_dir():
    raise FileNotFoundError(f"Manim toolkit folder not found: {TOOLKIT_ROOT}")

_PKG = "ideal_conductor_manim_toolkit"
if _PKG not in sys.modules:
    _package = ModuleType(_PKG)
    _package.__path__ = [str(TOOLKIT_ROOT)]
    sys.modules[_PKG] = _package
_tk_tools = importlib.import_module(f"{_PKG}.tools")
_tk_lib = importlib.import_module(f"{_PKG}.useful_libraries")
_saved_tools = sys.modules.get("tools")
sys.modules["tools"] = _tk_tools
try:
    _tk_tech = importlib.import_module(f"{_PKG}.techniques")
finally:
    sys.modules["tools"] = _saved_tools

tk = SimpleNamespace(
    glow_dot=_tk_tools.glow_dot,
    glowing_path=_tk_tools.glowing_path,
    ChargedParticle=_tk_tools.ChargedParticle,
    CrystalLattice=_tk_tools.CrystalLattice,
    FlowParticles=_tk_tools.FlowParticles,
    FieldLineBundle=_tk_tools.FieldLineBundle,
    conductor_track=_tk_tools.conductor_track,
    wireframe_sphere=_tk_tools.wireframe_sphere,
    NeutralConductingSphere=_tk_lib.NeutralConductingSphere,
    equation_impact=_tk_tech.equation_impact,
    travelling_pulse=_tk_tech.travelling_pulse,
    spotlight=_tk_tech.spotlight,
)

# ----------------------------------------------------------------------------
# Palette
# ----------------------------------------------------------------------------
RED = "#ff5d66"
ORANGE = "#ff9847"
METAL = "#9bb2bd"
DEEP = "#061a25"
ICE = "#c7fbff"
VIOLET = "#a98bff"
GREEN = "#79f7c2"
DIM = "#294556"
NUM_FONT = ARABIC_FONT  # Latin digits are fine in the Arabic font

# ----------------------------------------------------------------------------
# Scene clock and living updaters
# ----------------------------------------------------------------------------
CLOCK = ValueTracker(0.0)


def now() -> float:
    return CLOCK.get_value()


def install_clock(scene):
    """Add the clock to the scene. Its dt-updater makes every wait render real frames."""
    CLOCK.set_value(0.0)
    CLOCK.clear_updaters()
    CLOCK.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(CLOCK)


def live_spin(mob, rate, about=None, axis=OUT):
    """Rotate continuously (rad/s). ``about`` may be a point or a mobject to follow."""
    def upd(m, dt):
        centre = about.get_center() if isinstance(about, Mobject) else (
            about if about is not None else m.get_center())
        m.rotate(rate * dt, axis=axis, about_point=centre)
    mob.add_updater(upd)
    return mob


def live_bob(mob, amplitude=0.06, freq=0.5, phase=0.0, direction=UP):
    """Gentle floating motion that never drifts away."""
    state = {"last": 0.0}

    def upd(m, dt):
        value = amplitude * np.sin(TAU * freq * now() + phase)
        m.shift((value - state["last"]) * direction)
        state["last"] = value
    mob.add_updater(upd)
    return mob


def live_breathe(mob, low=0.35, high=1.0, freq=0.4, phase=0.0, stroke=True, fill=True):
    """Opacity breathing for glows and halos."""
    def upd(m):
        k = low + (high - low) * (0.5 + 0.5 * np.sin(TAU * freq * now() + phase))
        if stroke:
            m.set_stroke(opacity=k)
        if fill:
            m.set_fill(opacity=k * m._breathe_fill)
    mob._breathe_fill = max(mob.get_fill_opacity(), 1e-3) if fill else 0
    mob.add_updater(upd)
    return mob


def drive(scene, tracker, end, duration, rate=smooth, delay=0.0, start=None):
    """Animate a ValueTracker on the scene clock, independent of play() calls, so
    several motions can overlap freely across cues."""
    if tracker not in scene.mobjects:
        scene.add(tracker)
    t0 = now() + delay
    box = {"a": start}

    def upd(m, dt):
        u = (now() - t0) / max(duration, 1e-6)
        if u < 0:
            return
        if box["a"] is None:
            box["a"] = m.get_value()
        if u >= 1:
            m.set_value(end)
            m.remove_updater(upd)
            return
        m.set_value(box["a"] + (end - box["a"]) * rate(u))
    tracker.add_updater(upd)
    return tracker


def tracker(scene, value=0.0):
    t = ValueTracker(value)
    scene.add(t)
    return t


def freeze(*mobs):
    for m in mobs:
        m.clear_updaters(recursive=True)


# ----------------------------------------------------------------------------
# Text and equations
# ----------------------------------------------------------------------------
def eq(latex, size=44, color=WHITE, width=None):
    """Formula through the project's math_type (standard notation stays LTR)."""
    if width is None:
        return _math_tex(latex, size=size, color=color)
    return _math_tex(latex, size=size, color=color, width=width)


def eq_row(*parts, buff=0.14):
    """Equation built from separately animatable pieces: (latex, color[, size])."""
    pieces = []
    for p in parts:
        latex, color = p[0], p[1]
        size = p[2] if len(p) > 2 else 44
        pieces.append(eq(latex, size=size, color=color))
    return VGroup(*pieces).arrange(RIGHT, buff=buff)


def num_text(s, size=30, color=WHITE):
    return Text(s, font=NUM_FONT, font_size=size, color=color)


def rtl_reveal(text_mob, run_time=1.2, lag=0.55, shift=0.12):
    """Reveal Arabic glyphs right-to-left (reading order), each sliding in from the right."""
    glyphs = sorted(text_mob.submobjects, key=lambda g: -g.get_center()[0]) or [text_mob]
    return LaggedStart(*[FadeIn(g, shift=LEFT * shift) for g in glyphs],
                       lag_ratio=lag / max(len(glyphs), 1) * 8, run_time=run_time)


def glow_text(text_mob, color=CYAN, layers=3, opacity=0.16):
    """Soft halo behind a Text: wide translucent strokes around the same glyphs."""
    halo = VGroup()
    for i in range(1, layers + 1):
        c = text_mob.copy().set_fill(opacity=0)
        c.set_stroke(color, width=5 * i, opacity=opacity / i)
        halo.add(c)
    halo.set_z_index(-1)
    return halo


def heading(text, size=38, color=WHITE, y=3.3, accent=CYAN):
    label = ar(text, size=size, color=color, max_width=11.8).move_to([0, y, 0])
    line = Line(label.get_corner(DL) + DOWN * 0.12, label.get_corner(DR) + DOWN * 0.12,
                color=accent, stroke_width=1.6, stroke_opacity=0.7)
    return VGroup(label, line)


class LiveNumber(VGroup):
    """Number shown with Pango Text (no LaTeX), refreshed only when its string changes."""

    def __init__(self, getter, fmt="{:.2f}", size=30, color=WHITE, align=LEFT, at=ORIGIN):
        super().__init__()
        self.getter, self.fmt, self.size, self.color_, self.align = getter, fmt, size, color, align
        self.anchor = Dot(radius=0.001, fill_opacity=0, stroke_width=0).move_to(at)
        self.add(self.anchor)
        self._shown = None
        self._cache = {}
        self.refresh()
        self.add_updater(lambda m: m.refresh())

    def _format(self, v):
        return self.fmt(v) if callable(self.fmt) else self.fmt.format(v)

    def refresh(self):
        s = self._format(self.getter())
        if s == self._shown:
            return self
        if s not in self._cache:
            self._cache[s] = num_text(s, self.size, self.color_)
        t = self._cache[s].copy()
        t.next_to(self.anchor.get_center(), -self.align, buff=0) if not np.allclose(self.align, ORIGIN) \
            else t.move_to(self.anchor)
        t.set_opacity(self._opacity if hasattr(self, "_opacity") else 1)
        self.submobjects = [self.anchor, t]
        self._shown = s
        return self

    def place(self, point):
        """Move the anchor and redraw the number there."""
        self.anchor.move_to(point)
        self._shown = None
        return self.refresh()

    def set_number_opacity(self, value):
        self._opacity = value
        self._shown = None
        return self.refresh()


# ----------------------------------------------------------------------------
# Particles, glows, ambient life
# ----------------------------------------------------------------------------
def glow(color=CYAN, radius=0.06, n=4, opacity=0.2):
    return tk.glow_dot(color=color, radius=radius, n_glow=n, glow_opacity=opacity)


def ambient_dust(count=70, seed=11, color=CYAN, area=(7.0, 3.9)):
    """Slowly drifting, twinkling dust: keeps the stage alive in every frame."""
    rng = np.random.default_rng(seed)
    dust = VGroup()
    data = []
    for _ in range(count):
        d = Dot(radius=rng.uniform(0.006, 0.02), color=color)
        base = np.array([rng.uniform(-area[0], area[0]), rng.uniform(-area[1], area[1]), 0])
        vel = np.array([rng.uniform(-0.05, 0.05), rng.uniform(0.01, 0.06), 0])
        data.append((base, vel, rng.uniform(0, TAU), rng.uniform(0.05, 0.3)))
        d.move_to(base)
        dust.add(d)

    def upd(group):
        t = now()
        for d, (base, vel, ph, op) in zip(group, data):
            p = base + vel * t
            p[0] = (p[0] + area[0]) % (2 * area[0]) - area[0]
            p[1] = (p[1] + area[1]) % (2 * area[1]) - area[1]
            d.move_to(p)
            d.set_opacity(op * (0.55 + 0.45 * np.sin(1.3 * t + ph)) * group.level.get_value())
    dust.level = ValueTracker(1.0)
    dust.add_updater(upd)
    return dust


def starfield(count=220, seed=4, depth_speed=0.22):
    """Warp-style starfield (sci-fi look): stars stream outward from the centre."""
    rng = np.random.default_rng(seed)
    stars = VGroup()
    params = []
    for _ in range(count):
        ang = rng.uniform(0, TAU)
        r0 = rng.uniform(0.05, 1.0)
        speed = rng.uniform(0.4, 1.0) * depth_speed
        s = Dot(radius=0.012, color=rng.choice([WHITE, ICE, CYAN, VIOLET]))
        params.append((ang, r0, speed))
        stars.add(s)
    stars.level = ValueTracker(0.0)

    def upd(group):
        t = now()
        for s, (ang, r0, sp) in zip(group, params):
            r = ((r0 + sp * t) % 1.0)
            rr = 0.2 + 8.0 * r ** 2.2
            s.move_to([rr * np.cos(ang), 0.62 * rr * np.sin(ang), 0])
            s.set(width=0.016 + 0.07 * r)
            s.set_opacity(min(1, 3 * r) * (1 - r) * 1.6 * group.level.get_value())
    stars.add_updater(upd)
    return stars


def influence_rings(source, color=RED, period=0.55, speed=2.6, max_r=9.0):
    """Expanding rings sent out by a charge (field news travels outward)."""
    rings = VGroup()
    rings.state = {"t": 0.0, "active": True}

    def upd(group, dt):
        st = group.state
        st["t"] += dt
        if st["active"] and st["t"] >= period:
            st["t"] = 0.0
            ring = Circle(radius=1.0, color=color, stroke_width=3)
            ring.r = 0.05
            ring.c = source.get_center().copy()
            group.add(ring)
        for ring in list(group.submobjects):
            ring.r += speed * dt
            if ring.r >= max_r:
                group.remove(ring)
                continue
            fade = 1 - ring.r / max_r
            ring.set(width=2 * ring.r).move_to(ring.c)
            ring.set_stroke(width=max(0.4, 3.0 * fade), opacity=0.75 * fade ** 1.4 * group.level.get_value())
    rings.level = ValueTracker(1.0)
    rings.add_updater(upd)
    return rings


def floating_marks(symbol="؟", count=7, center=ORIGIN, spread=3.2, color=GOLD, seed=2, size=40):
    """Question marks that rise, sway and fade in a loop."""
    rng = np.random.default_rng(seed)
    marks = VGroup()
    data = []
    for i in range(count):
        m = ar(symbol, size=size * rng.uniform(0.6, 1.2), color=color)
        data.append((rng.uniform(-spread, spread), rng.uniform(0, 1), rng.uniform(0.12, 0.22),
                     rng.uniform(0, TAU)))
        marks.add(m)
    marks.level = ValueTracker(0.0)

    def upd(group):
        t = now()
        for m, (x0, ph, sp, sw) in zip(group, data):
            u = (ph + sp * t) % 1.0
            m.move_to(np.array(center) + np.array([x0 + 0.25 * np.sin(2 * t + sw), -1.2 + 3.0 * u, 0]))
            m.set_opacity(group.level.get_value() * np.sin(PI * u) ** 1.5)
    marks.add_updater(upd)
    return marks


# ----------------------------------------------------------------------------
# Conductors and instruments
# ----------------------------------------------------------------------------
def metal_sphere(radius=1.5, center=ORIGIN, tint="#6f8792", rim=CYAN, layers=26):
    """Shaded metallic sphere: offset radial gradient, specular, rim light, equator."""
    center = np.array(center, dtype=float)
    body = VGroup()
    light = np.array([-0.38, 0.42, 0]) * radius
    for i in range(layers):
        k = i / (layers - 1)
        shade = interpolate_color(ManimColor("#03090d"), ManimColor(tint), k ** 1.3)
        c = Circle(radius=radius * (1 - 0.93 * k), stroke_width=0, fill_color=shade, fill_opacity=1)
        body.add(c.move_to(center + light * k))
    outline = Circle(radius=radius, stroke_color="#b8d1dc", stroke_width=2.2).move_to(center)
    rim_arc = Arc(radius=radius * 0.985, start_angle=-PI * 0.42, angle=PI * 0.62,
                  stroke_color=rim, stroke_width=4, stroke_opacity=0.7).move_arc_center_to(center)
    rim_glow = rim_arc.copy().set_stroke(width=14, opacity=0.12)
    spec = VGroup(
        Ellipse(width=0.62 * radius, height=0.36 * radius, stroke_width=0,
                fill_color=WHITE, fill_opacity=0.10),
        Ellipse(width=0.34 * radius, height=0.18 * radius, stroke_width=0,
                fill_color=WHITE, fill_opacity=0.35),
    ).rotate(PI / 7).move_to(center + light * 0.95)
    equator = Ellipse(width=2 * radius, height=0.42 * radius, color=CYAN,
                      stroke_width=1.1, stroke_opacity=0.35).move_to(center)
    sphere = VGroup(body, equator, outline, rim_glow, rim_arc, spec)
    sphere.radius = radius
    sphere.rim = VGroup(rim_glow, rim_arc)
    return sphere


def spinning_rim(sphere, rate=0.6):
    """Make the rim light orbit the sphere — the metal looks alive."""
    live_spin(sphere.rim, rate, about=sphere[2])
    return sphere


def globe(radius=1.6, center=ORIGIN, color=CYAN, tilt=0.42, rate=0.35, opacity=0.5):
    """Toolkit 3D wireframe sphere, tilted and spinning; the 2D camera projects it."""
    g = tk.wireframe_sphere(radius=radius, latitude_count=8, longitude_count=14,
                            color=color, opacity=opacity)
    g.rotate(PI / 2 - tilt, axis=RIGHT, about_point=ORIGIN)
    axis = rotate_vector(OUT, -(PI / 2 - tilt), axis=RIGHT)
    g.move_to(center)
    g.spin_axis = axis
    live_spin(g, rate, axis=axis)
    return g


def thermometer(height=3.0, level=0.8, color=ORANGE):
    """Thermometer whose mercury follows ``thermo.level`` (a ValueTracker)."""
    tracker = ValueTracker(level)
    tube = RoundedRectangle(width=0.34, height=height, corner_radius=0.17,
                            stroke_color=METAL, stroke_width=2, fill_color="#0a1218", fill_opacity=0.9)
    bulb = Circle(radius=0.32, stroke_color=METAL, stroke_width=2, fill_color=color,
                  fill_opacity=1).next_to(tube, DOWN, buff=-0.12)
    ticks = VGroup(*[Line(LEFT * 0.09, RIGHT * 0.09, stroke_width=1.2, color=METAL)
                     .move_to(tube.get_left() + RIGHT * 0.04 + UP * (y - height / 2 + 0.25))
                     for y in np.linspace(0.3, height - 0.4, 9)])

    def mercury():
        h = max(0.05, (height - 0.4) * tracker.get_value())
        col = interpolate_color(ManimColor(CYAN), ManimColor(color), tracker.get_value())
        r = RoundedRectangle(width=0.16, height=h, corner_radius=0.08, stroke_width=0,
                             fill_color=col, fill_opacity=1)
        r.move_to(tube.get_bottom() + UP * (0.18 + h / 2))
        bulb.set_fill(col)
        return r
    merc = always_redraw(mercury)
    group = VGroup(tube, ticks, merc, bulb)
    group.level = tracker
    return group


def zigzag(start, end, amplitude, teeth=6, color=ORANGE, width=4):
    """Resistor zig-zag whose amplitude can shrink to a straight wire."""
    start, end = np.array(start, float), np.array(end, float)
    direction = end - start
    normal = rotate_vector(direction / np.linalg.norm(direction), PI / 2)
    pts = [start, start + 0.18 * direction]
    for i in range(teeth * 2):
        u = 0.18 + 0.64 * (i + 0.5) / (teeth * 2)
        pts.append(start + u * direction + normal * amplitude * (1 if i % 2 == 0 else -1))
    pts += [start + 0.82 * direction, end]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)


def dial(radius=1.25, label=r"\sigma", color=CYAN, value=0.0):
    """Analogue gauge: 0 at the left, ∞ at the right. ``dial.value`` in [0, 1]."""
    tracker = ValueTracker(value)
    arc = Arc(radius=radius, start_angle=PI, angle=-PI, stroke_color=METAL, stroke_width=3)
    hub = VGroup(Circle(radius=0.11, fill_color=METAL, fill_opacity=1, stroke_width=0),
                 Circle(radius=0.05, fill_color=WHITE, fill_opacity=1, stroke_width=0))
    glow_arc = always_redraw(lambda: Arc(radius=radius, start_angle=PI,
                                         angle=-PI * max(tracker.get_value(), 1e-3),
                                         stroke_color=color, stroke_width=9, stroke_opacity=0.55,
                                         arc_center=hub.get_center()))
    ticks = VGroup()
    for i in range(21):
        a = PI - PI * i / 20
        inner = radius * (0.84 if i % 5 == 0 else 0.9)
        ticks.add(Line(inner * np.array([np.cos(a), np.sin(a), 0]),
                       radius * np.array([np.cos(a), np.sin(a), 0]),
                       stroke_width=2 if i % 5 == 0 else 1, color=METAL))
    zero = num_text("0", 24, METAL).move_to(radius * 1.18 * LEFT + DOWN * 0.05)
    inf = num_text("∞", 34, color).move_to(radius * 1.2 * RIGHT + DOWN * 0.02)

    def needle():
        a = PI - PI * tracker.get_value()
        tip = 0.92 * radius * np.array([np.cos(a), np.sin(a), 0])
        c = hub.get_center()
        return Line(c, c + tip, color=color, stroke_width=4)
    needle_m = always_redraw(needle)
    sym = eq(label, size=40, color=color).move_to(DOWN * 0.45)
    g = VGroup(arc, glow_arc, ticks, zero, inf, needle_m, hub, sym)
    g.value = tracker
    return g


def warning_sign(size=1.3, color=GOLD):
    tri = Triangle(stroke_color=color, stroke_width=6, fill_color="#2a1d05", fill_opacity=0.9)
    tri.scale_to_fit_height(size)
    bang = num_text("!", int(size * 46), color).move_to(tri.get_center() + DOWN * size * 0.1)
    return VGroup(tri, bang)


def stamp(text, color=RED, size=36, angle=0.14):
    label = ar(text, size=size, color=color)
    box = SurroundingRectangle(label, buff=0.22, corner_radius=0.08, stroke_color=color, stroke_width=5)
    inner = SurroundingRectangle(label, buff=0.12, corner_radius=0.06, stroke_color=color,
                                 stroke_width=1.5, stroke_opacity=0.7)
    return VGroup(box, inner, label).rotate(angle)


def crack_lines(center, radius, seed=5, count=5, color=WHITE):
    """Branching fracture lines spreading from an impact point on a sphere."""
    rng = np.random.default_rng(seed)
    cracks = VGroup()
    origin = np.array(center) + radius * 0.25 * np.array([0.5, 0.6, 0])
    for i in range(count):
        ang = TAU * i / count + rng.uniform(-0.3, 0.3)
        pts = [origin]
        p = origin.copy()
        for _ in range(7):
            ang += rng.uniform(-0.5, 0.5)
            p = p + rng.uniform(0.12, 0.26) * radius * np.array([np.cos(ang), np.sin(ang), 0])
            if np.linalg.norm(p - center) > radius * 0.97:
                break
            pts.append(p.copy())
        if len(pts) > 1:
            cracks.add(VMobject(stroke_color=color, stroke_width=2.2).set_points_as_corners(pts))
    return cracks


def hud_brackets(width=12.6, height=6.8, color=CYAN, arm=0.6):
    w, h = width / 2, height / 2
    corners = VGroup()
    for sx, sy in [(-1, 1), (1, 1), (1, -1), (-1, -1)]:
        c = np.array([sx * w, sy * h, 0])
        corners.add(VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
            [c + np.array([0, -sy * arm, 0]), c, c + np.array([-sx * arm, 0, 0])]))
    return corners


def scan_lines(width=14.4, height=8.2, count=46, color=CYAN):
    """Moving hologram scan lines."""
    lines = VGroup(*[Line(LEFT * width / 2, RIGHT * width / 2, stroke_width=1, color=color)
                     for _ in range(count)])
    lines.level = ValueTracker(0.0)

    def upd(group):
        t = now()
        for i, l in enumerate(group):
            y = ((i / count + 0.06 * t) % 1.0) * height - height / 2
            l.move_to([0, y, 0])
            l.set_stroke(opacity=group.level.get_value() * (0.05 + 0.05 * np.sin(9 * y + 4 * t)))
    lines.add_updater(upd)
    return lines


# ----------------------------------------------------------------------------
# Physics helpers
# ----------------------------------------------------------------------------
def sphere_in_uniform_field(R):
    """Exact field outside a conducting sphere (radius R) in a uniform field E0 = x̂ (slice z=0)."""
    def field(p):
        x, y = float(p[0]), float(p[1])
        r2 = x * x + y * y
        if r2 <= R * R:
            return np.zeros(2)
        r = np.sqrt(r2)
        a = R ** 3
        return np.array([1 - a / r ** 3 + 3 * a * x * x / r ** 5, 3 * a * x * y / r ** 5])
    return field


def resample(points, n=90):
    pts = np.asarray(points, float)
    if pts.shape[1] == 2:
        pts = np.column_stack([pts, np.zeros(len(pts))])
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    if s[-1] <= 0:
        return np.repeat(pts[:1], n, axis=0)
    u = np.linspace(0, s[-1], n)
    return np.column_stack([np.interp(u, s, pts[:, k]) for k in range(3)])


def expelled_field_lines(R, seeds_y, x_start=-6.6, n=90):
    """Left halves of field lines before (straight, through the metal) and after
    (bent, ending perpendicularly on the surface). Mirror gives the right halves."""
    field = sphere_in_uniform_field(R)
    before, after = [], []
    for y in seeds_y:
        line = trace_field_line(field, [x_start, y], step=0.03, steps=600,
                                bounds=[[x_start - 0.1, 0.0], [-4.2, 4.2]])
        line = np.asarray(line)
        r = np.linalg.norm(line[:, :2], axis=1)
        inside = np.where(r <= R * 1.003)[0]
        if len(inside):
            line = line[:inside[0] + 1]
        before.append(resample(np.array([[x_start, y], [0.0, y]]), n))
        after.append(resample(line, n))
    return before, after


def star_radius(theta, R=1.45):
    """Egg-like conductor with a pointed nose toward +x (star-shaped about the origin)."""
    wrapped = (theta + PI) % TAU - PI
    return R * (1 + 0.42 * np.exp(-(wrapped / 0.42) ** 2) + 0.08 * np.cos(2 * theta))


def simulate_surface_migration(n=64, steps=240, seed=7, R=1.45):
    """Excess electrons repel (2D Coulomb, overdamped) inside the conductor and
    end up on its surface, denser at the pointed end. Returns (steps+1, n, 2)."""
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, TAU, n)
    rr = np.sqrt(rng.uniform(0.0, 1.0, n)) * 0.7
    pos = np.column_stack([rr * star_radius(th, R) * np.cos(th), rr * star_radius(th, R) * np.sin(th)])
    frames = [pos.copy()]
    for k in range(steps):
        d = pos[:, None, :] - pos[None, :, :]
        r2 = (d ** 2).sum(-1) + 1e-3
        np.fill_diagonal(r2, np.inf)
        force = (d / r2[..., None]).sum(1)
        step = 0.0035 * force
        mag = np.linalg.norm(step, axis=1, keepdims=True)
        step = np.where(mag > 0.06, step * 0.06 / mag, step)
        pos = pos + step
        ang = np.arctan2(pos[:, 1], pos[:, 0])
        lim = star_radius(ang, R) * 0.985
        rad = np.linalg.norm(pos, axis=1)
        over = rad > lim
        pos[over] *= (lim[over] / rad[over])[:, None]
        frames.append(pos.copy())
    return np.array(frames)


# ----------------------------------------------------------------------------
# Beat timing on top of raji_sci narration plans
# ----------------------------------------------------------------------------
class Beat:
    """One narration segment. Cue times are relative to when the beat starts, so an
    overrun shifts later beats instead of clipping animations; drift is reported."""

    report = []

    def __init__(self, scene, seg):
        self.scene, self.seg = scene, seg
        self.t0 = float(scene.time)

    def _rel(self, t_abs):
        return self.t0 + (t_abs - self.seg.start)

    def cue(self, phrase, offset=0.0):
        return self._rel(self.seg.phrases[phrase].start) + offset

    @property
    def end(self):
        return self._rel(self.seg.window_end)

    def remaining(self):
        return self.end - float(self.scene.time)

    def wait_until(self, t):
        dt = t - float(self.scene.time)
        if dt > 1.0 / 60:
            self.scene.wait(dt)

    def at(self, phrase, offset=0.0):
        target = self.cue(phrase, offset)
        late = float(self.scene.time) - target
        if late > 0.25:
            Beat.report.append(f"segment {self.seg.index}: phrase {phrase} reached {late:.2f}s late")
        self.wait_until(target)

    def finish(self):
        late = float(self.scene.time) - self.end
        if late > 0.05:
            Beat.report.append(f"segment {self.seg.index}: overran its window by {late:.2f}s")
        self.wait_until(self.end)
