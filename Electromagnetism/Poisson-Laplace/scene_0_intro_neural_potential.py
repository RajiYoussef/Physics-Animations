"""Scene 05 - from a finite-difference grid to a neural-network potential.

VIDEO ONLY: no audio is generated, read or attached. No text file is read.

Each section shows exactly what its Arabic passage says (the passage is copied
above each section as a comment). SECTION_SECONDS holds the length of each section;
every visual beat sits at a fraction of its section, so if your recording of a
passage is longer or shorter, change that one number and the beats follow.

All numbers on screen are computed (pinn_logic.py): the grid values come from a
finite-difference solution of Laplace's equation, the interpolation is real
bilinear interpolation, and the network is actually trained to satisfy Laplace's
equation and the boundary values; its outputs, activations and shrinking
mismatches are taken from that training.

Style follows 3Blue1Brown's "But what is a neural network?" (chapter 1): unit
brightness = activation, edge colour = sign of the weight, edge width = its size.
Written for Manim Community; no code is taken from 3Blue1Brown's repository.
"""

from manim import *  # noqa: F403 - Manim colours are overridden by the project palette below
import numpy as np

from settings34 import ARABIC_FONT, BLUE, GREEN, GREY, RED, ROOT, WHITE, YELLOW, run
from math_type import tex
import pinn_logic as P

from raji_sci.core.colormap import ramp
from raji_sci.core.labels import arabic_label
from raji_sci.physics.field_visuals import ScalarFieldImage

# Length of each section in seconds. Change a value to match your recorded passage.
SECTION_SECONDS = (13.0, 12.0, 13.0, 11.0, 14.0, 19.0, 13.0, 12.0, 18.0, 13.0, 19.0, 13.0)
CLEAR = 0.6  # seconds at the end of a section used to clear the stage
CACHE = ROOT / "media" / "scene_05_training.npz"
DARK = "#0B0F14"


# ---------------------------------------------------------------------------
# Timing: absolute section windows; beats at fractions of a section
# ---------------------------------------------------------------------------

class Timeline:
    def __init__(self, scene):
        self.scene = scene
        self.starts = np.concatenate([[0.0], np.cumsum(SECTION_SECONDS)])

    def start(self, k):
        return float(self.starts[k - 1])

    def end(self, k):
        return float(self.starts[k])

    def wait_until(self, t):
        dt = t - float(self.scene.time)
        if dt > 1e-9:
            self.scene.wait(dt)

    def _play(self, k, anims, run_time, **kw):
        room = self.end(k) - CLEAR - float(self.scene.time)
        rt = max(min(run_time, room), 1 / config.frame_rate)
        self.scene.play(*anims, run_time=rt, **kw)

    def at(self, k, frac, *anims, run_time=1.0, **kw):
        """Play when ``frac`` of section k has passed (clipped to the section)."""
        self.wait_until(self.start(k) + frac * SECTION_SECONDS[k - 1])
        self._play(k, anims, run_time, **kw)

    def then(self, k, *anims, run_time=1.0, **kw):
        self._play(k, anims, run_time, **kw)

    def close(self, k, keep=()):
        """Fade out everything except ``keep`` in the last CLEAR seconds of section k."""
        self.wait_until(self.end(k) - CLEAR)
        keep_ids = {id(f) for m in keep for f in m.get_family()}
        gone = []

        def expand(mobs):
            # a wrapper group (e.g. made by an animation) may hold kept and unkept parts:
            # unwrap it in place (same drawing order) so only the unkept parts fade
            out = []
            for m in mobs:
                if id(m) in keep_ids:
                    out.append(m)
                elif not any(id(f) in keep_ids for f in m.get_family()):
                    out.append(m)
                    gone.append(m)
                else:
                    out.extend(expand(m.submobjects))
            return out

        self.scene.mobjects = expand(self.scene.mobjects)
        if gone:
            self.scene.play(*[FadeOut(m) for m in gone], run_time=CLEAR * 0.9)
        self.wait_until(self.end(k))


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def ar(text, size=26, color=WHITE):
    return arabic_label(text, size=size, color=color, font=ARABIC_FONT, max_width=12.6)


def num(value, size=24, color=WHITE, fmt="{:.2f}"):
    return Text(fmt.format(value), font_size=size, color=color)


def potential_cmap(values, **_):
    """0 -> dark, 0.5 -> blue, 1 -> yellow (V lies in [0, 1] here)."""
    rgb = ramp(np.clip(values, 0, 1), [(0.0, DARK), (0.45, BLUE), (1.0, YELLOW)])
    return np.clip(rgb * 255 + 0.5, 0, 255).astype(np.uint8)


def potential_color(v):
    r, g, b = potential_cmap(np.array([[v]]))[0, 0]
    return ManimColor.from_rgb((int(r), int(g), int(b)))


class Region:
    """The unit square x, y in [0, 1], drawn with centre ``c`` and side ``s``."""

    def __init__(self, c, s):
        self.c, self.s = np.asarray(c, float), float(s)

    def p(self, x, y):
        return np.array([self.c[0] + self.s * (x - 0.5), self.c[1] + self.s * (y - 0.5), 0.0])

    def square(self, color=WHITE):
        return Square(self.s, color=color, stroke_width=3).move_to([*self.c, 0])


class Net:
    """Drawing of the trained network's architecture, P.LAYERS = (2, 6, 6, 1)."""

    def __init__(self, xs, cy=-0.3, dy=0.82, r=0.22):
        self.pos = [[np.array([x, cy + dy * ((n - 1) / 2 - i), 0.0]) for i in range(n)]
                    for x, n in zip(xs, P.LAYERS)]
        self.r = r

    def node(self, l, i):
        return self.pos[l][i]

    def edge_line(self, l, i, j):
        a, b = self.pos[l][i], self.pos[l + 1][j]
        d = (b - a) / np.linalg.norm(b - a)
        return Line(a + d * self.r, b - d * self.r)

    def nodes(self, acts=None, stroke=WHITE):
        g = VGroup()
        for l, layer in enumerate(self.pos):
            for i, p in enumerate(layer):
                fill, op = DARK, 1.0
                if acts is not None:
                    a = float(acts[l][i])
                    t = np.clip(abs(a), 0, 1)
                    fill = interpolate_color(ManimColor(DARK), ManimColor(YELLOW if a >= 0 else BLUE), t)
                g.add(Circle(self.r, color=stroke, stroke_width=2, fill_color=fill, fill_opacity=op).move_to(p))
        return g

    def edges(self, theta=None, width=1.2, color=GREY, opacity=0.6):
        """Neutral edges, or coloured by weight (sign -> colour, size -> width) when theta is given."""
        g = VGroup()
        params = P.unpack(theta) if theta is not None else None
        wmax = max(np.max(np.abs(W)) for W, _ in params) if params else 1.0
        for l in range(len(self.pos) - 1):
            for j in range(len(self.pos[l + 1])):
                for i in range(len(self.pos[l])):
                    line = self.edge_line(l, i, j)
                    if params is None:
                        line.set_stroke(color, width, opacity)
                    else:
                        w = float(params[l][0][j, i])
                        line.set_stroke(BLUE if w >= 0 else RED, 0.4 + 4.0 * abs(w) / wmax, 0.85)
                    g.add(line)
        return g

    def edges_between(self, group, l):
        """Slice of an ``edges`` group for layer l -> l + 1 (edges are built in order)."""
        sizes = [P.LAYERS[k] * P.LAYERS[k + 1] for k in range(len(P.LAYERS) - 1)]
        start = sum(sizes[:l])
        return VGroup(*group[start:start + sizes[l]])


def travel(dot, line, run_time=1.0):
    return MoveAlongPath(dot, line.copy(), run_time=run_time, rate_func=smooth)


def signal_dot(color=YELLOW, r=0.07):
    return Dot(radius=r, color=color)


# ---------------------------------------------------------------------------
# Computed data
# ---------------------------------------------------------------------------

def load_training():
    if CACHE.is_file():
        d = np.load(CACHE)
        return d["theta"], d["thetas"], d["interior"], d["boundary"]
    theta, history = P.train()
    thetas = np.array([h[0] for h in history])
    interior = np.array([h[1] for h in history])
    boundary = np.array([h[2] for h in history])
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez(CACHE, theta=theta, thetas=thetas, interior=interior, boundary=boundary)
    return theta, thetas, interior, boundary


# ---------------------------------------------------------------------------
# The scene
# ---------------------------------------------------------------------------

class NeuralPotential(Scene):
    def add_sound(self, *args, **kwargs):
        """Video only: this scene never adds audio."""
        return None

    def construct(self):
        self.camera.background_color = "#000000"
        self.T = Timeline(self)
        self.GX, self.GY, self.GV = P.grid_solution(6)
        self.theta, self.thetas, self.res_hist, self.bnd_hist = load_training()
        self.region = Region((-3.4, -0.35), 5.0)
        self.probe_xy = (0.47, 0.55)

        self.s1_grid()
        self.s2_question()
        self.s3_interpolation()
        self.s4_dimensions()
        self.s5_network()
        self.s6_signals()
        self.s7_weights()
        self.s8_bias_activation()
        self.s9_forward()
        self.s10_potential()
        self.s11_training()
        self.s12_continuous()
        self.T.wait_until(self.T.end(12))
        print(f"[scene_05] duration {self.time:.2f} s (planned {sum(SECTION_SECONDS):.0f} s)")

    # 1 ----------------------------------------------------------------------
    # توفر لنا طريقة الفروق المحدودة وسيلةً فعالةً لحل معادلة لابلاس؛
    # حيث نقوم بحساب الجهد عند نقاطٍ موزعةٍ على شبكة.
    def s1_grid(self):
        T, R = self.T, self.region
        n = self.GX.shape[0]
        method = ar("طريقة الفروق المحدودة", 30, YELLOW).move_to([3.7, 2.3, 0])
        laplace = tex(r"\nabla^2 V = 0", 46).move_to([3.7, 1.1, 0])
        laplace_name = ar("معادلة لابلاس", 24, GREY).next_to(laplace, DOWN, buff=0.25)
        square = R.square()
        T.at(1, 0.0, Create(square), FadeIn(method, shift=DOWN * 0.15), run_time=1.4)
        T.at(1, 0.22, Write(laplace), FadeIn(laplace_name), run_time=1.4)

        s = np.linspace(0, 1, n)
        hlines = VGroup(*[Line(R.p(0, v), R.p(1, v), color=GREY, stroke_width=1.5) for v in s[1:-1]])
        vlines = VGroup(*[Line(R.p(v, 0), R.p(v, 1), color=GREY, stroke_width=1.5) for v in s[1:-1]])
        T.at(1, 0.48, LaggedStart(*[Create(l) for l in hlines], lag_ratio=0.15),
             LaggedStart(*[Create(l) for l in vlines], lag_ratio=0.15), run_time=1.6)

        self.dots = VGroup(*[Dot(R.p(s[i], s[j]), radius=0.065, color=WHITE) for j in range(n) for i in range(n)])
        self.vlabels = VGroup(*[
            tex(rf"V_{{{i}{j}}}", 15, GREY).next_to(R.p(s[i], s[j]), UR, buff=0.04)
            for j in range(n) for i in range(n)
        ])
        points_note = ar("الجهد عند نقاط الشبكة", 24, BLUE).move_to([3.7, -0.6, 0])
        T.at(1, 0.66, LaggedStart(*[FadeIn(d, scale=2.5) for d in self.dots], lag_ratio=0.06), run_time=2.4)
        T.then(1, LaggedStart(*[FadeIn(v, shift=UP * 0.05) for v in self.vlabels], lag_ratio=0.03),
               FadeIn(points_note), run_time=1.8)
        self.s1_side = VGroup(method, laplace, laplace_name, points_note)
        self.square, self.gridlines = square, VGroup(hlines, vlines)
        T.close(1, keep=[square, hlines, vlines, self.dots, self.vlabels])

    # 2 ----------------------------------------------------------------------
    # ولكن، ماذا لو أردنا الحصول على دالةٍ تُمكّننا من معرفة قيمة الجهد
    # في أي موضعٍ داخل النطاق المطلوب؟
    def s2_question(self):
        T, R = self.T, self.region
        n = self.GX.shape[0]
        s = np.linspace(0, 1, n)
        start = R.p(s[2], s[2])
        target = R.p(*self.probe_xy)
        self.probe = Dot(start, radius=0.1, color=YELLOW)
        T.at(2, 0.05, GrowFromCenter(self.probe), run_time=0.8)
        T.at(2, 0.3, self.probe.animate.move_to(target), run_time=1.8)
        self.xy_label = tex(r"(x,y)", 22, YELLOW).next_to(target, DOWN + LEFT * 0.2, buff=0.12)
        self.qmark = tex(r"V=\,?", 26, YELLOW).next_to(target, UP + LEFT * 0.3, buff=0.12)
        question = tex(r"V(x,y)\;=\;?", 44, YELLOW).move_to([3.7, 1.2, 0])
        anywhere = ar("قيمة الجهد في أي موضع داخل النطاق", 24).move_to([3.7, 0.1, 0])
        T.at(2, 0.58, FadeIn(self.xy_label), FadeIn(self.qmark, scale=1.4), Write(question), run_time=1.4)
        T.then(2, FadeIn(anywhere), run_time=0.8)
        T.close(2, keep=[self.square, self.gridlines, self.dots, self.vlabels, self.probe, self.xy_label, self.qmark])

    # 3 ----------------------------------------------------------------------
    # عند الاعتماد على قيمٍ محددةٍ عند نقاط الشبكة، نحتاج إلى استخدام الاستكمال
    # لتقدير القيم بين تلك النقاط.
    def s3_interpolation(self):
        T = self.T
        n = self.GX.shape[0]
        _, weights = P.bilinear(self.GX, self.GY, self.GV, *self.probe_xy)
        corners = [(j, i) for (j, i) in weights]
        idx = [j * n + i for (j, i) in corners]
        rings = VGroup(*[Circle(0.16, color=GREEN, stroke_width=3).move_to(self.dots[k]) for k in idx])
        T.at(3, 0.02, LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2),
             *[self.vlabels[k].animate.set_color(GREEN) for k in idx], run_time=1.6)

        target = self.probe.get_center()
        flows = [self.vlabels[k].copy() for k in idx]
        estimate = tex(r"\tilde V", 22, GREEN).next_to(target, RIGHT, buff=0.18)
        T.at(3, 0.4, FadeOut(self.qmark), *[f.animate.move_to(target).scale(0.6).set_opacity(0.0) for f in flows],
             run_time=1.8)
        for f in flows:
            self.remove(f)
        name = ar("تقدير بالاستكمال", 26, GREEN).move_to([3.7, -1.2, 0])
        formula = tex(r"\tilde V(x,y)=\sum c_{ij}\,V_{ij}", 34, GREEN).move_to([3.7, 0.1, 0])
        T.then(3, FadeIn(estimate, scale=1.3), Flash(self.probe, color=GREEN), run_time=1.0)
        T.at(3, 0.66, Write(formula), FadeIn(name), run_time=1.6)
        T.close(3, keep=[self.dots])

    # 4 ----------------------------------------------------------------------
    # علاوةً على ذلك، في الأبعاد الأعلى، قد يتطلب استخدام شبكةٍ دقيقةٍ عدداً هائلاً من النقاط.
    def s4_dimensions(self):
        T = self.T
        N = 5

        def grid2d(origin, step=0.42, r=0.05, color=WHITE):
            return VGroup(*[Dot(origin + np.array([i * step, j * step, 0]), radius=r, color=color)
                            for j in range(N) for i in range(N)])

        def lattice(origin, step=0.42, depth=(0.24, 0.17, 0), r=0.045):
            layers = VGroup()
            for k in range(N):
                shade = interpolate_color(ManimColor(WHITE), ManimColor(BLUE), k / (N - 1))
                layers.add(grid2d(origin + k * np.array(depth), step, r, shade))
            return layers

        flat = grid2d(np.array([-6.3, -1.4, 0]))
        T.at(4, 0.0, ReplacementTransform(self.dots, flat), run_time=1.2)
        n_edge = tex("N", 26, YELLOW).next_to(flat, DOWN, buff=0.15)
        lab2 = tex(r"N^2", 30).next_to(flat, DOWN, buff=0.65)
        T.then(4, FadeIn(n_edge), FadeIn(lab2), run_time=0.6)

        cube = lattice(np.array([-2.6, -1.6, 0]))
        lab3 = tex(r"N^3", 30).next_to(cube, DOWN, buff=0.45)
        T.at(4, 0.22, TransformFromCopy(flat, cube[0]), run_time=0.8)
        T.then(4, LaggedStart(*[FadeIn(layer, shift=UR * 0.2) for layer in cube[1:]], lag_ratio=0.3),
               FadeIn(lab3), run_time=1.4)

        axes = VGroup(*[Arrow(ORIGIN, d, buff=0, color=GREY, stroke_width=3, max_tip_length_to_length_ratio=0.15)
                        .shift([1.6, -2.2, 0]) for d in (RIGHT * 1.1, UP * 1.1, np.array([0.7, 0.5, 0]),
                                                           np.array([-0.6, 0.8, 0]), np.array([0.9, -0.4, 0]))])
        more = VGroup(*[lattice(np.array([2.0 + 0.75 * c, 0.9 - 0.4 * c, 0]), step=0.16, depth=(0.09, 0.06, 0), r=0.022)
                        for c in range(4)])
        dots_more = tex(r"\cdots", 36).next_to(more, RIGHT, buff=0.25)
        labd = tex(r"N^d", 40, YELLOW).move_to([4.6, -2.4, 0])
        huge = ar("عدد هائل من النقاط", 28, YELLOW).move_to([0, 3.1, 0])
        T.at(4, 0.5, LaggedStart(*[GrowArrow(a) for a in axes], lag_ratio=0.2), run_time=1.2)
        T.then(4, LaggedStart(*[FadeIn(m, scale=0.6) for m in more], lag_ratio=0.25), FadeIn(dots_more), run_time=1.5)
        T.at(4, 0.74, Write(labd), FadeIn(huge), run_time=1.0)
        T.then(4, Indicate(labd, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.lattice_points = VGroup(*[d for layer in cube for d in layer])
        T.close(4, keep=[cube])
        self.cube = cube

    # 5 ----------------------------------------------------------------------
    # لذا، سنستخدم في هذا الفيديو نهجاً آخر، وهو: التعلم الآلي.
    # سنقوم بتمثيل الجهد باستخدام شبكةٍ عصبية (neural network).
    def s5_network(self):
        T = self.T
        self.net = Net(xs=(-3.6, -1.2, 1.2, 3.6))
        net = self.net
        title = ar("التعلم الآلي", 36, YELLOW).move_to([0, 3.2, 0])
        T.at(5, 0.08, FadeIn(title, shift=DOWN * 0.2), run_time=1.0)

        nodes = net.nodes()
        edges = net.edges()
        points = list(self.lattice_points)
        chosen = [points[k * (len(points) // len(nodes))] for k in range(len(nodes))]
        movers = VGroup(*[c.copy() for c in chosen])
        self.remove(*self.cube, self.cube)
        self.add(self.cube, movers)
        T.at(5, 0.4, *[m.animate.move_to(nd.get_center()).scale(2.2) for m, nd in zip(movers, nodes)],
             FadeOut(self.cube, shift=DOWN * 0.3), run_time=1.6)
        T.then(5, ReplacementTransform(movers, nodes), run_time=0.5)
        layer_nodes = [VGroup(*nodes[sum(P.LAYERS[:l]):sum(P.LAYERS[:l + 1])]) for l in range(len(P.LAYERS))]
        names = [ar("طبقة المدخلات", 20, GREY).next_to(layer_nodes[0], DOWN, buff=0.35),
                 ar("طبقات خفية", 20, GREY).move_to((layer_nodes[1].get_bottom() + layer_nodes[2].get_bottom()) / 2 + DOWN * 0.35),
                 ar("طبقة المخرجات", 20, GREY).next_to(layer_nodes[3], DOWN, buff=0.35)]
        T.at(5, 0.55, Indicate(layer_nodes[0], color=YELLOW), FadeIn(names[0]), run_time=0.8)
        T.then(5, Create(net.edges_between(edges, 0)), Indicate(layer_nodes[1], color=YELLOW), run_time=0.9)
        T.then(5, Create(net.edges_between(edges, 1)), Indicate(layer_nodes[2], color=YELLOW), FadeIn(names[1]), run_time=0.9)
        T.then(5, Create(net.edges_between(edges, 2)), Indicate(layer_nodes[3], color=YELLOW), FadeIn(names[2]), run_time=0.9)
        self.bring_to_front(nodes)
        rep = ar("تمثيل الجهد", 30, BLUE).move_to([0, -3.35, 0])
        nn = Text("neural network", font_size=22, color=GREY).next_to(rep, RIGHT, buff=0.4)
        T.at(5, 0.84, FadeIn(rep, shift=UP * 0.15), FadeIn(nn), run_time=1.0)
        self.nodes_g, self.edges_g, self.layer_names = nodes, edges, VGroup(*names)
        T.close(5, keep=[nodes, edges])

    # 6 ----------------------------------------------------------------------
    # تتكون الشبكة العصبية من مجموعةٍ من الوحدات الحسابية البسيطة المرتبة في طبقات.
    # تستقبل كل وحدةٍ مجموعةً من الأرقام، وتدمجها معاً، ثم تمرر النتيجة إلى الطبقة التالية.
    def s6_signals(self):
        T, net = self.T, self.net
        nodes, edges = self.nodes_g, self.edges_g
        layer_nodes = [VGroup(*nodes[sum(P.LAYERS[:l]):sum(P.LAYERS[:l + 1])]) for l in range(len(P.LAYERS))]
        units = ar("وحدات حسابية بسيطة مرتبة في طبقات", 26).move_to([0, 3.2, 0])
        T.at(6, 0.02, FadeIn(units), *[Indicate(g, color=YELLOW, scale_factor=1.15) for g in layer_nodes], run_time=1.5)

        a_labels = VGroup(tex("a_1", 26, YELLOW).next_to(layer_nodes[0][0], LEFT, buff=0.2),
                          tex("a_2", 26, YELLOW).next_to(layer_nodes[0][1], LEFT, buff=0.2))
        first = net.edges_between(edges, 0)
        sig = [signal_dot() for _ in first]
        for d, e in zip(sig, first):
            d.move_to(e.get_start())
        T.at(6, 0.24, FadeIn(a_labels), run_time=0.6)
        self.add(*sig)
        T.then(6, LaggedStart(*[travel(d, e) for d, e in zip(sig, first)], lag_ratio=0.05), run_time=2.0)
        T.then(6, *[FadeOut(d) for d in sig], run_time=0.3)

        u = 2  # the unit we follow, hidden layer 1
        unit = layer_nodes[1][u]
        dim = [m.animate.set_opacity(0.18) for k, m in enumerate(edges)]
        T.at(6, 0.45, *dim, unit.animate.set_stroke(YELLOW, 4), run_time=0.8)
        in1, in2 = net.edge_line(0, 0, u), net.edge_line(0, 1, u)
        hi = VGroup(in1, in2).set_stroke(YELLOW, 3)
        self.add(hi)
        p1 = VGroup(signal_dot(), tex("a_1", 20, YELLOW).shift(UP * 0.25)).move_to(in1.get_start())
        p2 = VGroup(signal_dot(), tex("a_2", 20, YELLOW).shift(DOWN * 0.25)).move_to(in2.get_start())
        receive = ar("تستقبل", 24, YELLOW).move_to([-2.4, 2.4, 0])
        T.then(6, FadeIn(receive), travel(p1, in1, 1.3), run_time=1.3)
        T.then(6, travel(p2, in2, 1.3), run_time=1.3)
        combine = ar("تدمج", 24, YELLOW).move_to([0.0, 2.4, 0])
        T.at(6, 0.7, FadeIn(combine), p1.animate.move_to(unit).scale(0.2).set_opacity(0),
             p2.animate.move_to(unit).scale(0.2).set_opacity(0), Flash(unit, color=YELLOW), run_time=1.2)
        out_edge = net.edge_line(1, u, 3).set_stroke(YELLOW, 3)
        out = signal_dot().move_to(out_edge.get_start())
        passes = ar("تمرر النتيجة إلى الطبقة التالية", 24, YELLOW).move_to([2.6, 2.4, 0])
        self.add(out_edge)
        T.at(6, 0.84, FadeIn(passes), travel(out, out_edge, 1.4), run_time=1.4)
        T.then(6, Indicate(layer_nodes[2][3], color=YELLOW), run_time=0.6)
        self.focus = (u, unit, in1, in2, a_labels)
        T.close(6, keep=[nodes, edges, a_labels, hi, unit])
        self.hi = hi

    # 7 ----------------------------------------------------------------------
    # ويُقصد بـ "الدمج" هنا أن كل رقمٍ واردٍ يُضرب في "وزنٍ" معين،
    # وهو ما يحدد مدى تأثير ذلك الرقم في النتيجة النهائية.
    def s7_weights(self):
        T = self.T
        u, unit, in1, in2, a_labels = self.focus
        netgroup = VGroup(self.edges_g, self.nodes_g, a_labels, self.hi)
        # zoom: the network shrinks to the right, the followed unit grows into a large diagram on the left
        A1, A2 = np.array([-6.2, 1.5, 0]), np.array([-6.2, -2.1, 0])
        S = np.array([-2.9, -0.3, 0])
        big_unit = Circle(0.8, color=YELLOW, stroke_width=4, fill_color=DARK, fill_opacity=1).move_to(S)
        l1 = Line(A1, S + 0.8 * normalize(A1 - S), color=WHITE, stroke_width=3)
        l2 = Line(A2, S + 0.8 * normalize(A2 - S), color=WHITE, stroke_width=3)
        a1 = tex("a_1", 34, YELLOW).next_to(A1, LEFT, buff=0.15)
        a2 = tex("a_2", 34, YELLOW).next_to(A2, LEFT, buff=0.15)
        T.at(7, 0.0, netgroup.animate.scale(0.55).move_to([4.6, -0.3, 0]).set_opacity(0.35),
             TransformFromCopy(VGroup(unit, in1, in2), VGroup(big_unit, l1, l2)), run_time=1.6)
        T.then(7, FadeIn(a1), FadeIn(a2), run_time=0.6)

        weight_word = ar("وزن", 26, YELLOW).move_to([-4.5, 2.7, 0])
        m1 = l1.point_from_proportion(0.5)
        m2 = l2.point_from_proportion(0.5)
        w1 = VGroup(tex("w_1", 30, YELLOW), tex("a_1", 30)).arrange(RIGHT, buff=0.04).move_to(m1 + 0.55 * normalize(np.array([0.48, 0.88, 0])))
        w2 = VGroup(tex("w_2", 30, YELLOW), tex("a_2", 30)).arrange(RIGHT, buff=0.04).move_to(m2 + 0.55 * normalize(np.array([0.48, -0.88, 0])))
        rule1 = VGroup(tex("a_1", 28), tex(r"\longrightarrow", 28), tex("w_1", 28, YELLOW), tex("a_1", 28)) \
            .arrange(RIGHT, buff=0.1).move_to([-4.0, 3.2, 0])
        rule2 = VGroup(tex("a_2", 28), tex(r"\longrightarrow", 28), tex("w_2", 28, YELLOW), tex("a_2", 28)) \
            .arrange(RIGHT, buff=0.1).next_to(rule1, RIGHT, buff=0.9)
        T.at(7, 0.25, TransformFromCopy(a1, w1[1]), FadeIn(w1[0], scale=1.5), FadeIn(rule1), FadeIn(weight_word),
             l1.animate.set_stroke(BLUE, 6), run_time=1.3)
        T.then(7, Indicate(w1[0], color=YELLOW, scale_factor=1.4), run_time=0.7)
        T.at(7, 0.47, TransformFromCopy(a2, w2[1]), FadeIn(w2[0], scale=1.5), FadeIn(rule2),
             l2.animate.set_stroke(BLUE, 2), run_time=1.3)
        T.then(7, Indicate(w2[0], color=YELLOW, scale_factor=1.4), run_time=0.7)
        influence = ar("الوزن يحدد مدى تأثير الرقم", 22, GREY).move_to([-4.6, -3.25, 0])
        sigma = tex(r"\Sigma", 44).move_to(S)
        T.at(7, 0.72, w1.animate.move_to(S).scale(0.3).set_opacity(0), w2.animate.move_to(S).scale(0.3).set_opacity(0),
             FadeIn(sigma, scale=0.5), FadeIn(influence), run_time=1.4)
        self.remove(w1, w2)
        self.big = VGroup(big_unit, l1, l2, a1, a2, sigma)
        self.rules = VGroup(rule1, rule2)
        self.netgroup = netgroup
        T.close(7, keep=[self.big, netgroup, self.rules])

    # 8 ----------------------------------------------------------------------
    # كما تضيف الوحدة قيمةً تُعرف بـ "الانحياز"—وهي إزاحةٌ قابلةٌ للتعديل—
    # ثم تُطبق "دالة تنشيط" على الناتج.
    def s8_bias_activation(self):
        T = self.T
        big_unit = self.big[0]
        S = big_unit.get_center()
        b_start = S + DOWN * 2.4
        b_arrow = Arrow(b_start, S + DOWN * 0.8, buff=0, color=GREEN, stroke_width=4)
        b_label = tex("b", 34, GREEN).next_to(b_start, DOWN, buff=0.1)
        b_name = ar("انحياز", 22, GREEN).next_to(b_label, RIGHT, buff=0.25)
        T.at(8, 0.02, GrowArrow(b_arrow), FadeIn(b_label), FadeIn(b_name), run_time=1.2)
        T.then(8, Flash(big_unit, color=GREEN), run_time=0.6)

        box = RoundedRectangle(corner_radius=0.12, width=1.5, height=1.3, color=WHITE, stroke_width=3).move_to(S + RIGHT * 3.0)
        curve = FunctionGraph(lambda t: 0.42 * np.tanh(2.2 * t), x_range=[-0.6, 0.6], color=YELLOW, stroke_width=3) \
            .move_to(box)
        f_label = tex("f", 30).next_to(box, UP, buff=0.1)
        f_name = ar("دالة التنشيط", 22, YELLOW).next_to(box, DOWN, buff=0.15)
        to_f = Arrow(S + RIGHT * 0.8, box.get_left(), buff=0.05, color=WHITE, stroke_width=4)
        T.at(8, 0.45, Create(box), Create(curve), FadeIn(f_label), FadeIn(f_name), GrowArrow(to_f), run_time=1.3)

        eq_z = tex(r"z=w_1a_1+w_2a_2+b", 32).move_to([-3.6, 2.6, 0])
        eq_a = tex(r"a=f(z)", 32, YELLOW).next_to(eq_z, RIGHT, buff=0.8)
        T.then(8, FadeOut(self.rules), Write(eq_z), run_time=1.0)
        z_tok = tex("z", 30).move_to(S + RIGHT * 1.1 + UP * 0.3)
        T.at(8, 0.66, FadeIn(z_tok, scale=1.3), run_time=0.4)
        T.then(8, z_tok.animate.move_to(box.get_center()).scale(0.6).set_opacity(0), run_time=1.0)
        self.remove(z_tok)
        out_arrow = Arrow(box.get_right(), box.get_right() + RIGHT * 1.0, buff=0.05, color=YELLOW, stroke_width=4)
        a_tok = tex("a", 34, YELLOW).next_to(out_arrow, RIGHT, buff=0.12)
        T.then(8, GrowArrow(out_arrow), FadeIn(a_tok, shift=RIGHT * 0.2), Write(eq_a), run_time=1.0)
        T.close(8, keep=[self.netgroup])

    # 9 ----------------------------------------------------------------------
    # تصبح مخرجات إحدى الطبقات هي المدخلات للطبقة التي تليها، وتستمر هذه العملية
    # عبر الطبقات الخفية وصولاً إلى طبقة المخرجات التي تُنتج في النهاية قيمةً عددية.
    def s9_forward(self):
        T = self.T
        net = Net(xs=(-3.6, -1.2, 1.2, 3.6))
        nodes, edges = net.nodes(), net.edges()
        old_edges, old_nodes, a_labels, hi = self.netgroup
        T.at(9, 0.0, ReplacementTransform(VGroup(old_edges, old_nodes), VGroup(edges, nodes)),
             FadeOut(a_labels), FadeOut(hi), run_time=1.2)
        _, acts = P.forward(self.theta, *self.probe_xy)
        acts = [a[:, 0] for a in acts]
        lit = net.nodes(acts)
        T.then(9, Transform(VGroup(*nodes[:2]), VGroup(*lit[:2])), run_time=0.6)
        fracs = (0.2, 0.45, 0.68)
        for l, f in enumerate(fracs):
            layer_edges = net.edges_between(edges, l)
            dots = [signal_dot(r=0.06).move_to(e.get_start()) for e in layer_edges]
            self.add(*dots)
            start = sum(P.LAYERS[:l + 1])
            stop = sum(P.LAYERS[:l + 2])
            T.at(9, f, LaggedStart(*[travel(d, e) for d, e in zip(dots, layer_edges)], lag_ratio=0.02), run_time=2.0)
            T.then(9, *[FadeOut(d) for d in dots],
                   Transform(VGroup(*nodes[start:stop]), VGroup(*lit[start:stop])), run_time=0.6)
        value = float(acts[-1][0])
        out = num(value, 30, YELLOW).next_to(nodes[-1], RIGHT, buff=0.3)
        number = ar("قيمة عددية", 24, YELLOW).next_to(out, DOWN, buff=0.25)
        T.at(9, 0.86, FadeIn(out, scale=1.4), FadeIn(number), Flash(nodes[-1], color=YELLOW), run_time=1.0)
        T.close(9, keep=[nodes, edges])
        self.net9 = (net, nodes, edges)

    # 10 ---------------------------------------------------------------------
    # في سياق مسألتنا، تُمثّل هذه القيمة "الجهد". فعندما نُدخل للشبكة إحداثيات موضعٍ ما
    # فإنها تُرجع قيمةً تقريبيةً للجهد.
    def s10_potential(self):
        T = self.T
        _, nodes9, edges9 = self.net9
        self.net = net = Net(xs=(-0.6, 1.4, 3.4, 5.1), cy=0.1, dy=0.72, r=0.2)
        self.rg = rg = Region((-4.6, 0.5), 3.6)
        sq = rg.square()
        nodes_static, edges_static = net.nodes(), net.edges()
        T.at(10, 0.0, ReplacementTransform(VGroup(edges9, nodes9), VGroup(edges_static, nodes_static)),
             Create(sq), run_time=1.2)
        out_name = ar("الجهد", 24, YELLOW).next_to(net.node(3, 0), DOWN, buff=0.35)
        T.then(10, FadeIn(out_name), Indicate(nodes_static[-1], color=YELLOW), run_time=0.8)

        px, py = ValueTracker(self.probe_xy[0]), ValueTracker(self.probe_xy[1])
        self.px, self.py = px, py

        def acts_now():
            _, a = P.forward(self.theta, px.get_value(), py.get_value())
            return [v[:, 0] for v in a]

        live_nodes = always_redraw(lambda: net.nodes(acts_now()))
        xin = tex("x", 26, YELLOW).next_to(net.node(0, 0), LEFT, buff=0.25)
        yin = tex("y", 26, YELLOW).next_to(net.node(0, 1), LEFT, buff=0.25)
        point = always_redraw(lambda: Dot(rg.p(px.get_value(), py.get_value()), radius=0.09, color=YELLOW))
        coords = always_redraw(lambda: tex(rf"({px.get_value():.2f},\;{py.get_value():.2f})", 20, YELLOW)
                               .next_to(rg.p(px.get_value(), py.get_value()), DOWN + RIGHT * 0.7, buff=0.12))
        T.at(10, 0.3, FadeIn(xin), FadeIn(yin), FadeIn(point), FadeIn(coords), run_time=1.0)
        fly = VGroup(num(px.get_value(), 20, YELLOW), num(py.get_value(), 20, YELLOW))
        fly[0].move_to(point.get_center()); fly[1].move_to(point.get_center())
        T.then(10, fly[0].animate.move_to(net.node(0, 0)).scale(0.8), fly[1].animate.move_to(net.node(0, 1)).scale(0.8),
               run_time=1.2)
        self.remove(fly)
        self.remove(nodes_static)
        self.add(live_nodes)
        readout = always_redraw(lambda: VGroup(tex(r"V(x,y;w_j)=", 24, YELLOW),
                                               num(float(P.forward(self.theta, px.get_value(), py.get_value())[0][0]), 22, YELLOW))
                                .arrange(RIGHT, buff=0.12).move_to([4.3, 2.85, 0]))
        T.then(10, FadeIn(readout), Flash(live_nodes[-1], color=YELLOW), run_time=0.9)
        T.at(10, 0.72, px.animate.set_value(0.22), py.animate.set_value(0.82), run_time=2.4)
        self.live = (live_nodes, edges_static, point, coords, readout, xin, yin, out_name, sq)
        T.wait_until(T.end(10))

    # 11 ---------------------------------------------------------------------
    # وتتمثل عملية التعلم الآلي في ضبط أوزان الشبكة وقيم الانحياز الخاصة بها؛ حيث نعدّلها
    # بحيث تحقق الدالة الناتجة —بدرجةٍ عاليةٍ من الدقة— معادلة لابلاس والشروط الحدية.
    def s11_training(self):
        T, net, rg = self.T, self.net, self.rg
        live_nodes, edges_static, point, coords, readout, xin, yin, out_name, sq = self.live
        k = ValueTracker(0)
        thetas = self.thetas
        order = np.unique(np.round(np.geomspace(1, len(thetas), 80)).astype(int) - 1)  # dense early, sparse late

        def theta_now():
            return thetas[order[min(int(round(k.get_value())), len(order) - 1)]]

        T.at(11, 0.0, FadeOut(point), FadeOut(coords), FadeOut(readout), run_time=0.6)
        live_edges = always_redraw(lambda: net.edges(theta_now()))
        self.remove(edges_static)
        self.add(live_edges)
        self.bring_to_front(live_nodes)
        params = VGroup(tex("w_j", 28, BLUE).move_to([0.4, 2.55, 0]), tex("b", 28, GREEN).move_to([1.4, 2.55, 0]))
        tune = ar("معاملات قابلة للضبط", 22, GREY).next_to(params, RIGHT, buff=0.35)
        T.then(11, FadeIn(params), FadeIn(tune), run_time=0.8)

        top = tex(r"V=\sin\pi x", 20, YELLOW).next_to(rg.square(), UP, buff=0.1)
        zero = tex(r"V=0", 20, GREY).next_to(rg.square(), DOWN, buff=0.1)
        sq_edges = VGroup(Line(rg.p(0, 1), rg.p(1, 1), color=YELLOW, stroke_width=5))
        inside, edges_pts = P.collocation()
        sub_in = inside[::2]
        sub_b = edges_pts[::3]

        def residual_dots():
            th = theta_now()
            _, lap, _ = P.forward(th, sub_in[:, 0], sub_in[:, 1], with_laplacian=True)
            Vb, _ = P.forward(th, sub_b[:, 0], sub_b[:, 1])
            eb = np.abs(Vb - P.boundary_value(sub_b[:, 0], sub_b[:, 1]))
            g = VGroup()
            for (x, y), r in zip(sub_in, np.abs(lap)):
                g.add(Dot(rg.p(x, y), radius=0.035, color=RED).set_opacity(float(np.clip(r / 4.0, 0.06, 1))))
            for (x, y), e in zip(sub_b, eb):
                g.add(Dot(rg.p(x, y), radius=0.05, color=ORANGE).set_opacity(float(np.clip(e / 0.3, 0.06, 1))))
            return g

        dots = always_redraw(residual_dots)
        T.at(11, 0.3, FadeIn(sq_edges), FadeIn(top), FadeIn(zero), FadeIn(dots), run_time=1.0)

        # the two checks, with mismatch bars (lengths on a log scale; no numbers shown)
        r_hist = self.res_hist[order]
        b_hist = self.bnd_hist[order]

        def bar_len(hist, lo, hi):
            v = hist[min(int(round(k.get_value())), len(hist) - 1)]
            return 0.08 + 2.6 * np.clip((np.log10(v) - lo) / (hi - lo), 0, 1)

        r_lo, r_hi = np.log10(r_hist.min()) - 0.3, np.log10(r_hist.max())
        b_lo, b_hi = np.log10(b_hist.min()) - 0.3, np.log10(b_hist.max())
        check1 = VGroup(tex(r"\nabla^2V=0", 24), ar("داخل النطاق", 20, GREY)).arrange(RIGHT, buff=0.25)
        check2 = VGroup(tex(r"V=g", 24), ar("على الحدود", 20, GREY)).arrange(RIGHT, buff=0.25)
        Y1, Y2, X0 = -2.35, -3.15, -3.75
        check1.move_to([-5.45, Y1, 0]); check2.move_to([-5.45, Y2, 0])
        bar1 = always_redraw(lambda: Rectangle(width=bar_len(r_hist, r_lo, r_hi), height=0.22, stroke_width=0,
                                               fill_color=RED, fill_opacity=0.9)
                             .move_to([X0, Y1, 0], aligned_edge=LEFT))
        bar2 = always_redraw(lambda: Rectangle(width=bar_len(b_hist, b_lo, b_hi), height=0.22, stroke_width=0,
                                               fill_color=ORANGE, fill_opacity=0.9)
                             .move_to([X0, Y2, 0], aligned_edge=LEFT))
        mismatch = ar("عدم التطابق", 20, GREY).move_to([X0 + 1.3, -1.85, 0])
        T.at(11, 0.45, FadeIn(check1), FadeIn(check2), FadeIn(bar1), FadeIn(bar2), FadeIn(mismatch), run_time=1.0)
        T.then(11, k.animate.set_value(len(order) - 1), run_time=7.5, rate_func=linear)
        ok1 = tex(r"\checkmark", 26, GREEN).next_to(bar1, RIGHT, buff=0.25)
        ok2 = tex(r"\checkmark", 26, GREEN).next_to(bar2, RIGHT, buff=0.25)
        T.then(11, FadeIn(ok1, scale=1.5), FadeIn(ok2, scale=1.5), run_time=0.7)
        self.s11 = VGroup(params, tune, top, zero, sq_edges, check1, check2, mismatch, ok1, ok2)
        self.s11_live = (live_edges, dots, bar1, bar2)
        T.wait_until(T.end(11) - CLEAR)
        self.play(FadeOut(self.s11), FadeOut(dots), FadeOut(bar1), FadeOut(bar2), FadeOut(xin), FadeOut(yin),
                  run_time=CLEAR * 0.9)
        T.wait_until(T.end(11))
        self.trained_edges = live_edges

    # 12 ---------------------------------------------------------------------
    # والنتيجة هي تقريبٌ متصلٌ لدالة الجهد، يمكننا من خلاله حساب قيمته عند أي نقطةٍ داخل النطاق المحدد.
    def s12_continuous(self):
        T, net, rg = self.T, self.net, self.rg
        n = self.GX.shape[0]
        s = np.linspace(0, 1, n)
        discrete = VGroup(*[Dot(rg.p(s[i], s[j]), radius=0.11, color=potential_color(self.GV[j, i]))
                            for j in range(n) for i in range(n)])
        T.at(12, 0.0, LaggedStart(*[FadeIn(d, scale=2) for d in discrete], lag_ratio=0.02), run_time=1.0)

        m = 120
        xs = np.linspace(0, 1, m)
        X, Y = np.meshgrid(xs, xs)
        V, _ = P.forward(self.theta, X.ravel(), Y.ravel())
        image = ScalarFieldImage(V.reshape(X.shape), rg.s, rg.s, (*rg.c, 0), cmap=potential_cmap)
        image.set_z_index(-1)
        continuous = ar("تقريب متصل لدالة الجهد", 26, YELLOW).move_to([-4.6, -2.0, 0])
        T.at(12, 0.18, FadeIn(image), discrete.animate.scale(0.2).set_opacity(0), FadeIn(continuous), run_time=1.6)
        self.remove(discrete)

        px, py = self.px, self.py
        point = always_redraw(lambda: Dot(rg.p(px.get_value(), py.get_value()), radius=0.09, color=WHITE))
        readout = always_redraw(lambda: VGroup(tex(r"V(x,y;w_j)=", 24, YELLOW),
                                               num(float(P.forward(self.theta, px.get_value(), py.get_value())[0][0]), 22, YELLOW))
                                .arrange(RIGHT, buff=0.12).move_to([4.3, 2.85, 0]))
        anywhere = ar("عند أي نقطة داخل النطاق", 22, GREY).move_to([-4.6, -2.6, 0])
        T.at(12, 0.38, FadeIn(point), FadeIn(readout), FadeIn(anywhere), run_time=0.8)
        t = ValueTracker(0.0)
        px.add_updater(lambda m: m.set_value(0.5 + 0.38 * np.sin(1.3 * t.get_value() + 0.4)))
        py.add_updater(lambda m: m.set_value(0.5 + 0.38 * np.sin(2.1 * t.get_value())))
        self.add(px, py)
        T.then(12, t.animate.set_value(2 * PI), run_time=5.0, rate_func=linear)
        px.clear_updaters(); py.clear_updaters()


if __name__ == "__main__":
    run(NeuralPotential)
