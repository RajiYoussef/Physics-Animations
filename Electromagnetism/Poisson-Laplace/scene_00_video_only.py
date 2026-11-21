"""Scene 00 - introduction to Poisson's equation.

Content follows the lesson text (1.txt). The video is exactly 180 seconds long, with the
same section lengths as the project's original scene_00 (25, 32, 15, 27, 38, 17,
22 s, then a hold). No audio is generated or attached, and no text file is read:
the start time of every visual beat is written below in CUES (seconds from the
start of its section).

Physics shown on screen is computed, not drawn by hand: Coulomb superposition,
point-charge potential and equipotentials, the SOR solution of Poisson's equation
with Dirichlet boundaries, -grad V, circulation and flux integrals
(raji_sci.physics.electrostatics_logic). Maths is typeset by math_type.tex
(no LaTeX installation needed).
"""

from manim import *  # noqa: F403 - Manim colours are overridden by the project palette below
import numpy as np

from settings34 import ARABIC_FONT, BLUE, GREEN, GREY, RED, ROOT, WHITE, YELLOW, run
from math_type import tex
from model import Slab

from raji_sci.core.labels import arabic_label
from raji_sci.physics.electrostatics_logic import (
    circulation,
    contour_paths,
    field_contributions,
    grid,
    negative_gradient,
    point_charge_field,
    point_charge_potential,
    poisson_sor,
)
from raji_sci.physics.field_visuals import ScalarFieldImage, field_arrows, polyline
from raji_sci.presentation.narration import Director, NarrationPlan, TimedPhrase, TimedSegment

REVIEW = ROOT / "review"

# Video length and section timing, taken from the project's 180-second scene_00:
# opening 25 s, routes 32 s, integral 15 s, laws 27 s, potential 38 s, curl 17 s,
# boundary 22 s, then a hold to 180 s. No audio is generated or attached.
SECTION_SECONDS = (25.0, 32.0, 15.0, 27.0, 38.0, 17.0, 22.0)
TARGET_SECONDS = 180.0
GAP = 0.8  # pause at the end of each section, used for clearing the stage


# Beat start times inside each section (seconds from the section start); the last
# number of each row is where the section's content ends and its clearing pause begins.
CUES = (
    (0.0, 1.99, 7.575, 11.875, 17.524, 24.2),
    (0.0, 0.799, 5.669, 7.686, 9.284, 10.654, 12.29, 14.344, 16.361, 22.449, 25.036, 31.2),
    (0.0, 1.552, 5.83, 8.652, 14.2),
    (0.0, 2.37, 7.751, 12.62, 20.435, 26.2),
    (0.0, 3.846, 6.869, 9.836, 14.122, 16.704, 22.474, 27.529, 34.562, 37.2),
    (0.0, 3.082, 8.243, 10.609, 16.2),
    (0.0, 0.66, 3.339, 8.115, 10.833, 15.609, 21.2),
)


def fixed_plan() -> NarrationPlan:
    """Timeline from SECTION_SECONDS and CUES; the last section holds until TARGET_SECONDS."""
    segments = []
    t = 0.0
    for k, (slot, cues) in enumerate(zip(SECTION_SECONDS, CUES)):
        beats = [TimedPhrase(f"beat {i}", t + a, t + b) for i, (a, b) in enumerate(zip(cues[:-1], cues[1:]))]
        last = k == len(SECTION_SECONDS) - 1
        window_end = TARGET_SECONDS if last else t + slot
        segments.append(TimedSegment(k + 1, f"section {k + 1}", t, t + cues[-1], window_end, beats))
        t += slot
    return NarrationPlan(segments, TARGET_SECONDS, "fixed", "", 0.0, GAP, TARGET_SECONDS - (t - GAP),
                         notes=["fixed section lengths, no audio, no text file"])


BLACK_BG = "#000000"


# ---------------------------------------------------------------------------
# Small builders
# ---------------------------------------------------------------------------

def ar(text, size=28, color=WHITE):
    """Arabic prose. Pango shapes it; never pre-reshape (see raji_sci.core.labels)."""
    return arabic_label(text, size=size, color=color, font=ARABIC_FONT, max_width=12.6)


def frac(num, den, size=40, color=WHITE):
    """Fraction from separate pieces so numerator and denominator can be highlighted."""
    n, d = tex(num, size, color), tex(den, size, color)
    bar = Line(LEFT, RIGHT, color=color, stroke_width=max(1.5, size / 22))
    bar.set_width(max(n.width, d.width) + 0.14)
    g = VGroup(n, bar, d).arrange(DOWN, buff=0.07)
    g.num, g.bar, g.den = n, bar, d
    return g


def row(*parts, buff=0.17):
    return VGroup(*parts).arrange(RIGHT, buff=buff)


def underline(mob, color, buff=0.08):
    return Line(mob.get_corner(DL) + DOWN * buff, mob.get_corner(DR) + DOWN * buff,
                color=color, stroke_width=3)


def charge_mob(x, y, q, base=0.15):
    col = RED if q > 0 else BLUE
    r = base * (0.85 + 0.35 * min(abs(q), 1.0))
    disc = Circle(radius=r, color=col, fill_color=col, fill_opacity=0.95, stroke_width=0)
    bar = Line(LEFT * r * 0.55, RIGHT * r * 0.55, color=BLACK_BG, stroke_width=3)
    sign = VGroup(bar) if q < 0 else VGroup(bar, bar.copy().rotate(PI / 2))
    return VGroup(disc, sign).move_to([x, y, 0])


def chapter(title):
    return ar(title, 21, GREY).to_corner(UR, buff=0.32)


def clear(scene):
    return lambda: [FadeOut(m) for m in list(scene.mobjects)]


def at_frac(seg, phrase, fraction, *anims, run_time=None):
    """Anchor inside a phrase: ``fraction`` of the way through its spoken duration."""
    start, end = seg.window(phrase)
    return seg.at(phrase, *anims, run_time=run_time, offset=fraction * (end - start))


def number_text(value, size=24, color=WHITE, fmt="{:.3f}"):
    return Text(fmt.format(value), font_size=size, color=color)


# ---------------------------------------------------------------------------
# Computed physics used by several segments
# ---------------------------------------------------------------------------

CHARGES = np.array([
    [-5.3, 1.3, 1.0], [-4.4, -1.6, -1.0], [-3.4, 1.5, 0.8],
    [-1.6, -1.5, 1.0], [-1.0, 1.1, -0.9], [-5.6, -0.4, 0.6],
])
REGION = {"x": (-6.7, 0.3), "y": (-2.9, 2.5)}
PROBE = np.array([-2.9, -0.1])


def coulomb_arrows(opacity=1.0):
    xs = np.arange(REGION["x"][0] + 0.3, REGION["x"][1], 0.5)
    ys = np.arange(REGION["y"][0] + 0.3, REGION["y"][1], 0.5)
    pts = np.array([[x, y] for x in xs for y in ys])
    keep = np.min(np.hypot(pts[:, None, 0] - CHARGES[None, :, 0], pts[:, None, 1] - CHARGES[None, :, 1]), axis=1) > 0.42
    pts = pts[keep]
    E = point_charge_field(CHARGES, pts, softening=0.15)
    arrows = field_arrows(pts, E, max_length=0.42, color=BLUE, stroke_width=2.2)
    if opacity < 1:
        for a in arrows:
            a.set_opacity(a.get_stroke_opacity() * opacity)
    return arrows


def potential_view():
    nx, ny = 141, 109
    X, Y, _ = grid(REGION["x"], REGION["y"], nx, ny)
    V = point_charge_potential(CHARGES, np.column_stack([X.ravel(), Y.ravel()]), softening=0.12).reshape(X.shape)
    w = REGION["x"][1] - REGION["x"][0]
    h = REGION["y"][1] - REGION["y"][0]
    centre = ((REGION["x"][0] + REGION["x"][1]) / 2, (REGION["y"][0] + REGION["y"][1]) / 2, 0)
    # p95 of |V| is about 2.4 here; vmax=3 keeps the gradient visible instead of flat blobs
    image = ScalarFieldImage(V, w, h, centre, vmax=3.0, gamma=0.75, opacity=0.8,
                             negative=BLUE, zero=BLACK_BG, positive=RED).set_z_index(-2)
    lines = VGroup()
    for level in (-1.0, -0.5, -0.25, 0.25, 0.5, 1.0):
        for path in contour_paths(X, Y, V, level):
            if len(path) > 12:
                lines.add(polyline(path, color=RED if level > 0 else BLUE, stroke_width=1.8).set_stroke(opacity=0.9))
    lines.set_z_index(-1)
    return image, lines


class ElectrostaticSystem:
    """Grounded box with two electrodes and a charge cloud, solved with SOR.

    Local coordinates: x in [-3.3, 3.3], y in [-2.0, 2.0], spacing 0.1.
    """

    W, H, STEP = 6.6, 4.0, 0.1

    def __init__(self):
        X, Y, (h, _) = grid((-3.3, 3.3), (-2.0, 2.0), 67, 41)
        self.X, self.Y, self.h = X, Y, h
        fixed = np.zeros_like(X, bool)
        fixed[0, :] = fixed[-1, :] = fixed[:, 0] = fixed[:, -1] = True
        self.plate = (np.abs(Y - 1.0) <= 0.08) & (X >= -2.3) & (X <= -0.5)
        self.block = (np.abs(X - 1.9) <= 0.26) & (np.abs(Y + 0.9) <= 0.26)
        fixed |= self.plate | self.block
        values = np.where(self.plate, 1.0, np.where(self.block, -0.6, 0.0))
        self.rho = 9.0 * np.exp(-((X - 0.4) ** 2 + (Y - 0.6) ** 2) / (2 * 0.32 ** 2))
        self.V, info = poisson_sor(self.rho, h, fixed, values, omega=1.72, tol=1e-6, snapshot_every=2)
        self.snapshots = [v for _, v in info["snapshots"]] + [self.V]
        self.iterations = info["iterations"]
        self.fixed = fixed
        Ex, Ey = negative_gradient(self.V, h, h)
        self.Ex, self.Ey = Ex, Ey

    def to_scene(self, centre, width):
        s = width / self.W
        c = np.asarray(centre, float)
        return lambda lx, ly: np.array([c[0] + s * lx, c[1] + s * ly, 0.0])

    def build(self, centre, width, arrows=True):
        """Group(image, outlines, labels, arrows) at ``centre`` with the given width."""
        s = width / self.W
        P = self.to_scene(centre, width)
        # V spans [-0.6, 1.73] (electrodes at +1 and -0.6, charge cloud peaks higher)
        image = ScalarFieldImage(self.V, width, self.H * s, P(0, 0), vmax=1.8, gamma=1.0, opacity=0.85,
                                 negative=BLUE, zero=BLACK_BG, positive=RED)
        frame = Rectangle(width=width, height=self.H * s, color=GREY, stroke_width=2).move_to(P(0, 0))
        plate = Rectangle(width=1.8 * s, height=0.16 * s, color=WHITE, fill_color="#C0392B",
                          fill_opacity=1, stroke_width=2.5).move_to(P(-1.4, 1.0))
        block = Square(side_length=0.52 * s, color=WHITE, fill_color="#1F6F96", fill_opacity=1,
                       stroke_width=2.5).move_to(P(1.9, -0.9))
        size = 22 * max(s, 0.75)
        labels = VGroup(
            tex(r"V=0", size, GREY).move_to(P(2.55, 1.65)),
            tex(r"V_0", size, WHITE).next_to(plate, UP, buff=0.08),
            tex(r"V_1", size, WHITE).next_to(block, DOWN, buff=0.08),
            tex(r"\rho", size * 1.1, YELLOW).move_to(P(0.4, 0.05)),
        )
        group = Group(image, frame, plate, block, labels)
        if arrows:
            group.add(self.arrows(centre, width))
        group.image, group.frame, group.labels = image, frame, labels
        return group

    def arrows(self, centre, width, every=5):
        P = self.to_scene(centre, width)
        s = width / self.W
        pts, vec = [], []
        for j in range(3, self.X.shape[0] - 3, every):
            for i in range(3, self.X.shape[1] - 3, every):
                if self.fixed[j, i]:
                    continue
                pts.append(P(self.X[j, i], self.Y[j, i])[:2])
                vec.append([self.Ex[j, i], self.Ey[j, i]])
        return field_arrows(np.array(pts), np.array(vec), max_length=0.34 * s, color=WHITE, stroke_width=1.8)


# ---------------------------------------------------------------------------
# The scene
# ---------------------------------------------------------------------------

class PoissonIntroduction(Scene):
    def add_sound(self, *args, **kwargs):
        """Video only: this scene never adds audio, whatever calls it."""
        return None

    def construct(self):
        self.plan = fixed_plan()
        d = Director(self, self.plan, attach_audio=False)  # video only: no sound is ever added
        self.system = ElectrostaticSystem()

        self.segment_1(d)
        self.segment_2(d)
        self.segment_3(d)
        self.segment_4(d)
        self.segment_5(d)
        self.segment_6(d)
        self.segment_7(d)

        REVIEW.mkdir(exist_ok=True)
        drift = d.finish(REVIEW / "scene_00_timing.json")
        print(f"[scene_00] duration {self.time:.3f} s (target {TARGET_SECONDS:.0f} s, drift {drift * 1000:.1f} ms)")

    # -- 1. topic: solving, properties (uniqueness), applications -------------
    def segment_1(self, d):
        with d.segment(1) as s:
            title = ar("معادلة بواسون", 42, YELLOW).move_to([0, 3.15, 0])
            s.at(0, FadeIn(title, shift=DOWN * 0.15), run_time=1.0)

            poisson = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 50, WHITE).move_to([0, 2.0, 0])
            solve = ar("حل المسائل", 24, GREY).next_to(poisson, RIGHT, buff=0.6)
            s.at(1, Write(poisson), run_time=2.0)
            s.then(FadeIn(solve, shift=LEFT * 0.2), run_time=0.8)

            # properties panel: uniqueness under boundary conditions (model.Slab, Vc = -6, rho = 4)
            slab = Slab()
            left = RoundedRectangle(corner_radius=0.15, width=6.5, height=3.95, color=GREY,
                                    stroke_width=1.5).move_to([-3.5, -1.3, 0]).set_stroke(opacity=0.6)
            axes = Axes(x_range=[0, slab.H, 1], y_range=[-7, 3, 2], x_length=3.3, y_length=2.9,
                        tips=False, axis_config={"color": GREY, "stroke_width": 1.6, "include_ticks": False}
                        ).move_to([-3.35, -1.45, 0])
            ax_labels = VGroup(tex("y", 22, GREY).next_to(axes.x_axis, RIGHT, buff=0.1),
                               tex("V", 22, GREY).next_to(axes.y_axis, UP, buff=0.08))
            props = ar("الخصائص الرياضية", 25, WHITE).move_to([-3.5, 0.98, 0])
            s.at(2, FadeIn(left), Create(axes), FadeIn(ax_labels), FadeIn(props), run_time=1.4)

            def true_v(y):
                return slab.potential(y, Vc=-6.0, rho=4.0)

            shapes = [(2.6, 1), (-2.4, 1), (1.6, 2), (-1.4, 2), (3.2, 3)]
            amp = ValueTracker(1.0)
            colors = [BLUE, GREEN, RED, GREY, BLUE]
            candidates = VGroup(*[
                always_redraw(lambda a=a, k=k, c=c: axes.plot(
                    lambda y: true_v(y) + amp.get_value() * a * np.sin(k * np.pi * y / slab.H),
                    x_range=[0, slab.H], color=c, stroke_width=2).set_stroke(opacity=0.75))
                for (a, k), c in zip(shapes, colors)
            ])
            ends = VGroup(Dot(axes.c2p(0, true_v(0)), radius=0.07, color=GREEN),
                          Dot(axes.c2p(slab.H, true_v(slab.H)), radius=0.07, color=GREEN))
            end_labels = VGroup(tex(r"V(0)=V_0", 20, GREEN).next_to(ends[0], LEFT, buff=0.15),
                                tex(r"V(H)=V_1", 20, GREEN).next_to(ends[1], DOWN, buff=0.12).shift(LEFT * 0.35))
            unique = ar("وحيدية الحل عند توفر شروط حدّية مناسبة", 23, GREEN).move_to([-3.5, 0.98, 0])
            s.at(3, FadeIn(candidates), GrowFromCenter(ends), FadeIn(end_labels),
                 ReplacementTransform(props, unique), run_time=1.4)
            solution = axes.plot(true_v, x_range=[0, slab.H], color=YELLOW, stroke_width=4)
            at_frac(s, 3, 0.35, amp.animate.set_value(0.0), run_time=2.6)
            s.then(FadeIn(solution), FadeOut(candidates), Flash(ends[1], color=GREEN), run_time=1.0)

            # applications panel: a computed electrostatic system
            right = left.copy().move_to([3.5, -1.3, 0])
            system = self.system.build(centre=(3.5, -1.5), width=5.6)
            apps = ar("تطبيقات: نمذجة الأنظمة الكهروستاتيكية", 23, BLUE).move_to([3.5, 0.98, 0])
            s.at(4, FadeIn(right), FadeIn(apps), FadeIn(system), run_time=1.6)
            s.outro(clear(self))

    # -- 2. from charges to the field: sum, integral, potential, Gauss -------
    def segment_2(self, d):
        with d.segment(2) as s:
            head = chapter("من الشحنات إلى المجال")
            charges = VGroup(*[charge_mob(x, y, q) for x, y, q in CHARGES])
            s.at(0, FadeIn(head), LaggedStart(*[GrowFromCenter(c) for c in charges], lag_ratio=0.15), run_time=1.1)

            arrows = coulomb_arrows()
            rho_to_e = tex(r"\rho(\mathbf{r})\;\longrightarrow\;\mathbf{E}(\mathbf{r})", 34, WHITE).move_to([3.8, 2.75, 0])
            s.at(1, LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.01), run_time=2.6)
            s.then(Write(rho_to_e), run_time=1.0)

            # (a) sum of contributions at a probe point, then tip to tail
            probe = Dot([*PROBE, 0], radius=0.07, color=WHITE)
            contrib = field_contributions(CHARGES, PROBE, softening=0.0)
            scale = 1.5 / np.max(np.linalg.norm(contrib, axis=1))
            vecs = contrib * scale
            pieces = VGroup(*[
                Arrow([*PROBE, 0], [*(PROBE + v), 0], buff=0, stroke_width=3,
                      color=RED if q > 0 else BLUE, max_tip_length_to_length_ratio=0.18)
                for v, q in zip(vecs, CHARGES[:, 2])
            ])
            label_sum = ar("جمع المساهمات", 22, GREY).move_to([3.8, 1.95, 0])
            f_sum = tex(r"\mathbf{E}=\sum_i\,\frac{q_i}{4\pi\varepsilon_0}\,\frac{\hat{\mathbf{r}}_i}{r_i^2}", 30).move_to([3.8, 1.2, 0])
            s.at(2, lambda: [arrows.animate.set_opacity(0.18), FadeIn(probe),
                             LaggedStart(*[GrowArrow(p) for p in pieces], lag_ratio=0.12),
                             FadeIn(label_sum), Write(f_sum)], run_time=1.6)
            chain = []
            tip = PROBE.copy()
            for p, v in zip(pieces, vecs):
                chain.append(p.animate.shift([*(tip - PROBE), 0]))
                tip = tip + v
            resultant = Arrow([*PROBE, 0], [*tip, 0], buff=0, color=YELLOW, stroke_width=5,
                              max_tip_length_to_length_ratio=0.15)
            s.then(*chain, run_time=1.0)
            s.then(GrowArrow(resultant), run_time=0.5)

            # (b) direct integration over a continuous distribution
            label_int = ar("أو التكامل المباشر", 22, GREY).move_to([3.8, 0.35, 0])
            f_int = tex(r"\mathbf{E}(\mathbf{r})=\frac{1}{4\pi\varepsilon_0}\int\;\frac{\rho(\mathbf{r}^{\prime})\,"
                        r"\hat{\mathbf{r}}}{r^2}\,d\tau^{\prime}", 28).move_to([3.8, -0.4, 0])
            s.at(3, FadeOut(pieces), FadeOut(resultant), FadeIn(label_int), Write(f_int), run_time=1.4)

            # (c) another route: potential, then E from its gradient
            image, contours = potential_view()
            label_v = ar("طريق آخر: الجهد الكهربائي", 22, GREEN).move_to([3.8, -1.25, 0])
            s.at(4, FadeIn(label_v), FadeOut(probe), run_time=0.8)
            f_v = tex(r"V\;\longrightarrow\;\mathbf{E}=-\nabla V", 32, GREEN).move_to([3.8, -1.95, 0])
            s.at(5, FadeIn(image), Create(contours), FadeOut(arrows), run_time=1.8)
            downhill = coulomb_arrows()  # E is perpendicular to the equipotentials, pointing downhill
            s.at(6, Write(f_v), LaggedStart(*[GrowArrow(a) for a in downhill], lag_ratio=0.01), run_time=1.6)

            # (d) high symmetry: Gauss's law, integral form
            column = VGroup(rho_to_e, label_sum, f_sum, label_int, f_int, label_v, f_v)
            s.at(7, FadeOut(image), FadeOut(contours), FadeOut(downhill), FadeOut(charges),
                 FadeOut(column), run_time=1.0)
            centre = np.array([-3.2, -0.3, 0])
            ball = Circle(radius=0.75, color=RED, fill_color=RED, fill_opacity=0.35, stroke_width=2).move_to(centre)
            q_label = tex(r"Q_{\mathrm{enc}}", 26, YELLOW).move_to(centre)
            radial = VGroup(*[
                Arrow(centre + 2.15 * np.array([np.cos(t), np.sin(t), 0]),
                      centre + 2.75 * np.array([np.cos(t), np.sin(t), 0]), buff=0, color=BLUE, stroke_width=3)
                for t in np.linspace(0, TAU, 16, endpoint=False)
            ])
            s.then(GrowFromCenter(ball), FadeIn(q_label), LaggedStart(*[GrowArrow(a) for a in radial], lag_ratio=0.04),
                   run_time=1.5)

            surface = DashedVMobject(Circle(radius=1.55, color=GREEN, stroke_width=3).move_to(centre), num_dashes=40)
            normals = VGroup(*[
                Arrow(centre + 1.55 * np.array([np.cos(t), np.sin(t), 0]),
                      centre + 2.05 * np.array([np.cos(t), np.sin(t), 0]), buff=0, color=GREEN, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.3)
                for t in np.linspace(0, TAU, 12, endpoint=False)
            ])
            s_label = tex("S", 26, GREEN).move_to(centre + np.array([1.2, 1.25, 0]))
            gauss_title = ar("قانون غاوس بصيغته التكاملية", 25, GREEN).move_to([3.4, 1.5, 0])
            lhs = tex(r"\oint_S\;\;\mathbf{E}\cdot d\mathbf{A}", 42, WHITE)
            eq = tex("=", 42, WHITE)
            rhs = frac(r"Q_{\mathrm{enc}}", r"\varepsilon_0", 42, WHITE)
            gauss = row(lhs, eq, rhs, buff=0.2).move_to([3.4, 0.1, 0])
            s.at(8, Create(surface), FadeIn(s_label), FadeIn(gauss_title), run_time=1.5)
            at_frac(s, 8, 0.25, LaggedStart(*[GrowArrow(n) for n in normals], lag_ratio=0.05), Write(gauss), run_time=2.2)
            at_frac(s, 8, 0.75, Indicate(q_label, color=YELLOW, scale_factor=1.3), run_time=1.2)

            # the formula, read aloud piece by piece
            s.at(9, Circumscribe(gauss, color=WHITE, buff=0.15), run_time=1.6)
            u1, u2, u3 = underline(lhs, BLUE), underline(rhs.num, YELLOW, 0.04), underline(rhs.den, GREEN, 0.04)
            s.at(10, lhs.animate.set_color(BLUE), Create(u1), run_time=1.0)
            at_frac(s, 10, 0.38, rhs.num.animate.set_color(YELLOW), Create(u2), Indicate(q_label, color=YELLOW), run_time=1.0)
            at_frac(s, 10, 0.78, rhs.den.animate.set_color(GREEN), Create(u3), run_time=1.0)
            s.outro(clear(self))

    # -- 3. why reformulate -------------------------------------------------
    def segment_3(self, d):
        with d.segment(3) as s:
            head = chapter("لماذا نعيد صياغة المسألة؟")
            icons = VGroup(tex(r"\sum", 58), tex(r"\int", 58), tex(r"\oint", 58)).arrange(RIGHT, buff=1.6).move_to([0, 1.9, 0])
            checks = VGroup(*[tex(r"\checkmark", 34, GREEN).next_to(i, RIGHT, buff=0.15) for i in icons])
            s.at(0, FadeIn(head), LaggedStart(*[FadeIn(i, shift=UP * 0.2) for i in icons], lag_ratio=0.2), run_time=1.2)
            s.then(LaggedStart(*[GrowFromCenter(c) for c in checks], lag_ratio=0.2), run_time=0.8)

            integral = tex(r"\mathbf{E}(\mathbf{r})=\frac{1}{4\pi\varepsilon_0}\int\;\frac{\rho(\mathbf{r}^{\prime})\,"
                           r"\hat{\mathbf{r}}}{r^2}\,d\tau^{\prime}", 40).move_to([0, 0.95, 0])
            hard = ar("قد يصبح صعباً عملياً", 26, RED).move_to([0, -0.35, 0])
            sources = np.array([[x, y] for x in np.linspace(-5.6, 1.6, 15) for y in np.linspace(-3.35, -1.35, 5)])
            target = np.array([4.7, -2.3, 0])
            probe = Dot(target, radius=0.08, color=WHITE)
            r_label = tex(r"\mathbf{r}", 26).next_to(probe, UP, buff=0.12)
            lines = VGroup(*[Line([x, y, 0], target, stroke_width=0.8, color=GREY).set_stroke(opacity=0.45)
                             for x, y in sources])
            s.at(1, lambda: [VGroup(icons, checks).animate.scale(0.6).move_to([0, 2.85, 0]), Write(integral)], run_time=1.6)
            at_frac(s, 1, 0.35, FadeIn(probe), FadeIn(r_label),
                    LaggedStart(*[Create(l) for l in lines], lag_ratio=0.01), run_time=2.2)
            at_frac(s, 1, 0.75, FadeIn(hard, shift=UP * 0.1), Wiggle(integral, scale_value=1.04), run_time=1.3)

            X, Y, _ = grid((-6.0, 2.0), (-3.7, -1.0), 120, 40)
            rho = (np.exp(-((X + 4.0) ** 2 + (Y + 2.4) ** 2) / 0.6) + 0.8 * np.exp(-((X + 1.0) ** 2 + (Y + 2.0) ** 2) / 0.9)
                   + 0.5 * np.exp(-((X - 1.0) ** 2 + (Y + 3.0) ** 2) / 0.3))
            density = ScalarFieldImage(rho, 8.0, 2.7, (-2.0, -2.35, 0), vmax=1.0, negative=BLUE, zero=BLACK_BG,
                                       positive=YELLOW, opacity=0.9)
            known = row(tex(r"\rho(x,y)", 28, YELLOW), tex(r"\checkmark", 28, GREEN), buff=0.15).move_to([-6.0, -0.6, 0])
            density.set_z_index(-1)  # behind the lines; z_index orders without adding anything to the scene
            s.at(2, FadeIn(density), FadeIn(known), run_time=1.4)

            nabla = tex(r"\nabla", 120, GREEN).move_to([0, 0.5, 0])
            diff = ar("المعادلات التفاضلية", 30, GREEN).next_to(nabla, DOWN, buff=0.45)
            s.at(3, lambda: [FadeOut(density), FadeOut(lines), FadeOut(probe), FadeOut(r_label), FadeOut(known),
                             FadeOut(hard), FadeOut(icons), FadeOut(checks)], run_time=0.9)
            s.then(ReplacementTransform(integral, nabla), run_time=1.6)
            s.then(FadeIn(diff, shift=UP * 0.15), run_time=0.9)
            s.outro(clear(self))

    # -- 4. two field equations -------------------------------------------
    def segment_4(self, d):
        with d.segment(4) as s:
            head = chapter("معادلتان للمجال")
            heading = ar("في الكهروستاتيكا", 34).move_to([0, 3.05, 0])
            s.at(0, FadeIn(head), FadeIn(heading, shift=DOWN * 0.1), run_time=1.0)

            slot1 = RoundedRectangle(corner_radius=0.15, width=6.2, height=2.3, color=GREEN, stroke_width=1.5).move_to([3.3, 0.8, 0])
            slot2 = RoundedRectangle(corner_radius=0.15, width=6.2, height=2.3, color=BLUE, stroke_width=1.5).move_to([3.3, -1.95, 0])
            two = ar("معادلتان أساسيتان للمجال الكهربائي", 24, GREY).move_to([3.3, 2.35, 0])
            s.at(1, FadeIn(two), Create(slot1), Create(slot2), run_time=1.4)

            name1 = ar("قانون غاوس بصيغته التفاضلية", 23, GREEN).move_to([3.3, 1.6, 0])
            s.at(2, FadeIn(name1, shift=DOWN * 0.1), run_time=1.0)
            div = tex(r"\nabla\cdot\mathbf{E}", 44)
            rhs = frac(r"\rho", r"\varepsilon_0", 44)
            eq1 = row(div, tex("=", 44), rhs).move_to([3.3, 0.55, 0])

            # divergence picture: a positive charge is a source of field lines
            c1 = np.array([-3.6, 0.8, 0])
            source = charge_mob(*c1[:2], 1.0, base=0.2)
            out = VGroup(*[Arrow(c1 + 0.35 * np.array([np.cos(t), np.sin(t), 0]),
                                 c1 + 1.15 * np.array([np.cos(t), np.sin(t), 0]), buff=0, color=BLUE, stroke_width=3)
                           for t in np.linspace(0, TAU, 10, endpoint=False)])
            box = DashedVMobject(Square(1.3, color=GREEN, stroke_width=2).move_to(c1), num_dashes=24)
            s.at(3, Write(eq1), GrowFromCenter(source), run_time=1.4)
            at_frac(s, 3, 0.15, div.animate.set_color(BLUE), LaggedStart(*[GrowArrow(a) for a in out], lag_ratio=0.05),
                    Create(box), run_time=1.4)
            at_frac(s, 3, 0.55, rhs.num.animate.set_color(YELLOW), Indicate(source, color=YELLOW), run_time=1.0)
            at_frac(s, 3, 0.8, rhs.den.animate.set_color(GREEN), run_time=0.8)

            name2 = ar("انعدام دوران المجال الكهربائي", 23, BLUE).move_to([3.3, -1.15, 0])
            curl = tex(r"\nabla\times\mathbf{E}", 44, BLUE)
            eq2 = row(curl, tex("=", 44), tex("0", 44)).move_to([3.3, -2.2, 0])
            # curl-free picture: circulation of a Coulomb field around a loop is computed, and is zero
            q2 = np.array([-5.2, -2.0])
            loop_c = np.array([-3.3, -2.0])
            loop = DashedVMobject(Circle(radius=0.6, color=GREEN, stroke_width=3).move_to([*loop_c, 0]), num_dashes=24)
            spin = CurvedArrow([loop_c[0] + 0.6, loop_c[1] + 0.05, 0], [loop_c[0] - 0.05, loop_c[1] + 0.6, 0],
                               color=GREEN, stroke_width=3)
            charge2 = charge_mob(*q2, 1.0, base=0.2)
            pts = np.array([[x, y] for x in np.linspace(-4.6, -2.3, 5) for y in np.linspace(-2.9, -1.1, 4)])
            field2 = field_arrows(pts, point_charge_field([[*q2, 1.0]], pts), max_length=0.35, color=BLUE)
            value = circulation(lambda p: point_charge_field([[*q2, 1.0]], p), loop_c, 0.6)
            readout = row(tex(r"\oint\;\;\mathbf{E}\cdot d\mathbf{l}=", 26), number_text(abs(value), 24), buff=0.12
                          ).move_to([-3.6, -3.35, 0])
            s.at(4, FadeIn(name2, shift=DOWN * 0.1), Write(eq2), FadeIn(charge2), FadeIn(field2), run_time=1.6)
            s.then(Create(loop), Create(spin), FadeIn(readout), run_time=1.4)
            s.outro(clear(self))

    # -- 5. the potential, substitution, Poisson's equation ---------------
    def segment_5(self, d):
        with d.segment(5) as s:
            head = chapter("إدخال الجهد الكهربائي")
            small = VGroup(tex(r"\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}", 30),
                           tex(r"\nabla\times\mathbf{E}=0", 30)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-4.6, 2.3, 0])
            components = tex(r"\mathbf{E}=(E_x,\,E_y,\,E_z)", 28, BLUE).move_to([-4.6, 0.95, 0])
            three = ar("ثلاث مركبات مجهولة", 21, GREY).next_to(components, DOWN, buff=0.2)
            complex_ = ar("حلّهما مباشرةً قد يكون معقّداً", 23, RED).move_to([-4.6, -0.55, 0])
            s.at(0, FadeIn(head), FadeIn(small), run_time=1.0)
            s.then(FadeIn(components), FadeIn(three), FadeIn(complex_), Indicate(small, color=RED), run_time=1.5)

            v_big = tex("V", 76, GREEN).move_to([2.4, 2.25, 0])
            scalar = ar("الجهد الكهربائي: دالة قياسية واحدة", 23, GREEN).next_to(v_big, DOWN, buff=0.25)
            s.at(1, FadeIn(v_big, scale=1.4), FadeIn(scalar), run_time=1.3)

            e_sym = tex(r"\mathbf{E}", 46, BLUE)
            grad = tex(r"-\nabla V", 46, GREEN)
            relation = row(e_sym, tex("=", 46), grad).move_to([2.4, 0.55, 0])
            s.at(2, lambda: [FadeOut(scalar), v_big.animate.scale(0.55).move_to([5.8, 2.3, 0]), Write(relation)], run_time=1.5)
            s.at(3, Indicate(grad, color=GREEN), Circumscribe(relation, color=YELLOW, buff=0.12), run_time=1.6)

            # substitution chain from 1.txt: div E = -lap V = rho/eps0
            a = tex(r"\nabla\cdot\mathbf{E}", 42)
            e1 = tex("=", 42)
            c = frac(r"\rho", r"\varepsilon_0", 42)
            gauss_row = row(a, e1, c).move_to([0.8, -1.0, 0])
            s.at(4, lambda: [FadeOut(components), FadeOut(three), FadeOut(complex_),
                             small.animate.set_opacity(0.35), Write(gauss_row)], run_time=1.2)
            mid = tex(r"\nabla\cdot(-\nabla V)", 42, GREEN)
            e2 = tex("=", 42)
            target = row(a.copy(), e1.copy(), mid, e2, c.copy()).move_to([0.8, -1.0, 0])
            s.then(lambda: [a.animate.move_to(target[0]), e1.animate.move_to(target[1]), c.animate.move_to(target[4]),
                            TransformFromCopy(grad, mid), FadeIn(e2)], run_time=1.3)

            lap = tex(r"-\nabla^2V", 42, GREEN)
            final = row(a.copy(), e1.copy(), lap, e2.copy(), c.copy()).move_to([0.8, -1.0, 0])
            note = tex(r"\nabla\cdot\nabla=\nabla^2", 26, GREY).move_to([0.8, -2.05, 0])
            s.at(5, lambda: [a.animate.move_to(final[0]), e1.animate.move_to(final[1]),
                             ReplacementTransform(mid, lap), e2.animate.move_to(final[3]), c.animate.move_to(final[4]),
                             FadeIn(note, shift=UP * 0.1)], run_time=1.8)
            s.then(Indicate(lap, color=GREEN), run_time=1.0)
            s.at(6, c.animate.set_color(YELLOW), Create(underline(final[4], YELLOW)), run_time=1.2)

            poisson = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 54, YELLOW).move_to([0.8, -2.75, 0])
            boxed = SurroundingRectangle(poisson, color=YELLOW, buff=0.2, stroke_width=3)
            s.at(7, FadeOut(note), TransformFromCopy(VGroup(lap, e2, c), poisson), run_time=2.0)
            s.then(Create(boxed), run_time=0.9)
            name = ar("معادلة بواسون", 30, YELLOW).next_to(boxed, LEFT, buff=0.5)
            s.at(8, FadeIn(name, shift=LEFT * 0.2), Circumscribe(boxed, color=WHITE, buff=0.05), run_time=1.6)
            s.outro(clear(self))

    # -- 6. the second equation is automatic -------------------------------
    def segment_6(self, d):
        with d.segment(6) as s:
            head = chapter("ماذا يحدث للمعادلة الثانية؟")
            second = ar("المعادلة الثانية", 24, GREY).move_to([3.2, 2.95, 0])
            curl_e = tex(r"\nabla\times\mathbf{E}=0", 46, BLUE).move_to([3.2, 2.1, 0])
            s.at(0, FadeIn(head), FadeIn(second), Write(curl_e), run_time=1.4)

            sub = tex(r"\mathbf{E}=-\nabla V", 26, GREY).move_to([5.6, 1.25, 0])
            curl_grad = tex(r"\nabla\times(\nabla V\,)=0", 46, GREEN).move_to([3.2, 0.6, 0])
            s.at(1, FadeIn(sub), TransformFromCopy(curl_e, curl_grad), run_time=1.8)

            ok = tex(r"\checkmark", 44, GREEN).next_to(curl_grad, RIGHT, buff=0.3)
            always = ar("متحققة دائماً", 26, GREEN).next_to(curl_grad, DOWN, buff=0.35)
            s.at(2, GrowFromCenter(ok), FadeIn(always), run_time=1.0)

            # any scalar function f: circulation of grad f around a moving loop, computed live
            c0 = np.array([-3.4, -0.9])

            def f(u, v):
                return np.sin(1.3 * u) * np.cos(1.1 * v) + 0.25 * u

            def grad_f(p):
                u, v = p[:, 0] - c0[0], p[:, 1] - c0[1]
                return np.column_stack([1.3 * np.cos(1.3 * u) * np.cos(1.1 * v) + 0.25,
                                        -1.1 * np.sin(1.3 * u) * np.sin(1.1 * v)])

            X, Y, _ = grid((-3.0, 3.0), (-2.0, 2.0), 121, 81)
            heat = ScalarFieldImage(f(X, Y), 6.0, 4.0, (*c0, 0), vmax=1.6, negative=BLUE, zero=BLACK_BG, positive=GREEN)
            pts = np.array([[x, y] for x in np.linspace(c0[0] - 2.7, c0[0] + 2.7, 10)
                            for y in np.linspace(c0[1] - 1.7, c0[1] + 1.7, 7)])
            grad_arrows = field_arrows(pts, grad_f(pts), max_length=0.38, color=WHITE, stroke_width=2)
            f_label = tex(r"f(x,y)", 26, GREEN).move_to([c0[0] - 2.4, c0[1] + 2.35, 0])
            t = ValueTracker(0.0)

            def loop_centre():
                a = t.get_value()
                return c0 + np.array([1.6 * np.cos(a), 0.9 * np.sin(2 * a)])

            loop = always_redraw(lambda: DashedVMobject(
                Circle(radius=0.55, color=YELLOW, stroke_width=3).move_to([*loop_centre(), 0]), num_dashes=22))
            readout = always_redraw(lambda: row(
                tex(r"\oint\;\;\nabla f\cdot d\mathbf{l}=", 26),
                number_text(abs(circulation(grad_f, loop_centre(), 0.55)), 24, YELLOW), buff=0.12
            ).move_to([c0[0], c0[1] - 2.45, 0]))
            identity = ar("دوران تدرّج أي دالة قياسية يساوي صفراً", 24).move_to([3.2, -1.2, 0])
            ident_eq = tex(r"\nabla\times\nabla f=0", 38, GREEN).move_to([3.2, -2.1, 0])
            s.at(3, FadeIn(heat), FadeIn(grad_arrows), FadeIn(f_label), FadeIn(identity), run_time=1.0)
            s.then(Write(ident_eq), Create(loop), FadeIn(readout), run_time=1.0)
            s.then(t.animate.set_value(TAU), run_time=3.0, rate_func=linear)
            s.outro(clear(self))

    # -- 7. one equation instead of two; equivalence; numerical tools ------
    def segment_7(self, d):
        sysm = self.system
        with d.segment(7) as s:
            head = chapter("لماذا نحل معادلة بواسون؟")
            s.at(0, FadeIn(head), run_time=0.8)

            two = VGroup(tex(r"\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}", 36),
                         tex(r"\nabla\times\mathbf{E}=0", 36)).arrange(DOWN, buff=0.35).move_to([-3.2, 1.0, 0])
            two_label = ar("معادلتان للمجال الكهربائي", 24, GREY).next_to(two, UP, buff=0.35)
            s.at(1, FadeIn(two_label), Write(two), run_time=1.6)

            poisson = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 40, YELLOW).move_to([3.8, 2.45, 0])
            one = ar("معادلة واحدة للجهد", 24, YELLOW).next_to(poisson, LEFT, buff=0.4)
            centre, width = (-3.1, -0.85), 6.6
            system = sysm.build(centre, width, arrows=False)
            bc = ar("مع الشروط الحدّية المناسبة", 23, GREEN).move_to([-3.1, -3.3, 0])
            s.at(2, FadeOut(two_label), ReplacementTransform(two, poisson), FadeIn(one), run_time=1.6)
            at_frac(s, 2, 0.3, FadeIn(system.frame), FadeIn(system[2]), FadeIn(system[3]), FadeIn(system.labels),
                    run_time=1.4)
            at_frac(s, 2, 0.65, FadeIn(bc), Indicate(system.frame, color=GREEN), Indicate(system.labels[:3], color=GREEN),
                    run_time=1.6)

            arrows = sysm.arrows(centre, width)
            e_rel = tex(r"\mathbf{E}=-\nabla V", 36, BLUE).move_to([3.8, 1.35, 0])
            system.image.set_z_index(-1)
            s.at(3, FadeIn(system.image), Write(e_rel), run_time=1.5)
            s.then(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.005), run_time=1.5)

            equiv = ar("طريقة مكافئة للتكامل المباشر", 23, YELLOW).move_to([3.8, 0.35, 0])
            integral = tex(r"\frac{1}{4\pi\varepsilon_0}\int\;\frac{\rho(\mathbf{r}^{\prime})\,\hat{\mathbf{r}}}{r^2}\,d\tau^{\prime}",
                           28).move_to([3.8, -0.45, 0])
            iff = tex(r"\Longleftrightarrow", 34, YELLOW).rotate(PI / 2).move_to([3.8, -1.25, 0])
            local = tex(r"\nabla^2V=-\frac{\rho}{\varepsilon_0}", 30, YELLOW).move_to([3.8, -2.0, 0])
            s.at(4, FadeIn(equiv), Write(integral), run_time=1.6)
            s.then(GrowFromCenter(iff), TransformFromCopy(poisson, local), run_time=1.4)

            # numerical tools: watch SOR relax the potential from zero to the solution
            tools = ar("أدوات رياضية وعددية", 25, GREEN).move_to([3.8, 0.35, 0])
            k = ValueTracker(0)
            snaps = sysm.snapshots
            counter = always_redraw(lambda: row(
                ar("التكرار", 22, GREY),
                Text(str(min(2 * int(round(k.get_value())), sysm.iterations)), font_size=24, color=WHITE),
                buff=0.2).move_to([3.8, -0.5, 0]))
            complex_sys = ar("لدراسة الأنظمة الكهروستاتيكية المعقدة", 23, WHITE).move_to([3.8, -1.45, 0])
            s.at(5, FadeOut(equiv), FadeOut(integral), FadeOut(iff), FadeOut(local), FadeOut(arrows), run_time=0.8)
            system.image.update_values(snaps[0])
            s.then(FadeIn(tools), FadeIn(counter), FadeIn(complex_sys), run_time=0.6)
            system.image.add_updater(lambda m: m.update_values(snaps[min(int(round(k.get_value())), len(snaps) - 1)]))
            s.then(k.animate.set_value(len(snaps) - 1), run_time=4.2, rate_func=linear)
            system.image.clear_updaters()
            s.then(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.005),
                   Circumscribe(poisson, color=YELLOW), run_time=1.4)
            # last segment: no outro clear, the final frame holds through the tail


if __name__ == "__main__":
    run(PoissonIntroduction)
