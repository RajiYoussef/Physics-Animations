"""Ideal conductors — Arabic introduction (scene 00).

Every beat follows one segment of the narration in intro_hook_AR.txt (taken word
for word from intro.txt). Animations are cued to the spoken phrases through the
raji_sci narration planner, and the whole stage runs on one clock, so nothing
stands still while the narrator talks.

Timing
  * By default every segment's length is estimated from the Arabic text
    (LETTERS_PER_SECOND, a slow clear reading pace).
  * After recording the voice, put the measured length of each of the 14
    segments (seconds) in intro_hook_durations.json, e.g. [11.2, 13.9, ...],
    and the whole intro re-times itself to your narration.

Render from PyCharm with the Run button (uses settings.render), or from a
terminal:  manim -qh scene_00_intro_hook.py IdealConductorHook
Optional:  CONDUCTOR_BEATS="5,6" renders only those beats (fast previews).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

from settings import BACKGROUND, CYAN, GOLD, WHITE
from support import ar
from hbar_character import hbar_character
from intro_fx import (
    CLOCK, DEEP, DIM, GREEN, ICE, METAL, ORANGE, RED, VIOLET, Beat, LiveNumber,
    ScalarFieldImage, ambient_dust, contour_paths, crack_lines, dial, drive, eq,
    eq_row, expelled_field_lines, field_arrows, floating_marks, freeze, globe,
    glow, glow_text, heading, hud_brackets, influence_rings, install_clock,
    live_bob, live_breathe, live_spin, metal_sphere, now, num_text, polyline,
    rtl_reveal, scan_lines, simulate_surface_migration, sphere_in_uniform_field,
    spinning_rim, stamp, star_radius, starfield, thermometer, tk, trace_field_line,
    tracker, warning_sign, zigzag,
)
from raji_sci.presentation.narration import load_plan

ROOT = Path(__file__).resolve().parent
_trapz = getattr(np, "trapezoid", None) or np.trapz
SCRIPT = ROOT / "intro_hook_AR.txt"
DURATIONS_FILE = ROOT / "intro_hook_durations.json"
LETTERS_PER_SECOND = 8.0


def build_plan():
    if DURATIONS_FILE.is_file():
        durations = json.loads(DURATIONS_FILE.read_text(encoding="utf-8"))
        return load_plan(SCRIPT, durations, lead_in=0.4, gap=0.8, tail=1.2)
    return load_plan(SCRIPT, letters_per_second=LETTERS_PER_SECOND)


def chip(text, color=CYAN, size=27, icon=None):
    """Arabic keyword chip; optional icon sits on the right (reading start)."""
    label = ar(text, size=size, color=WHITE)
    parts = VGroup(label)
    if icon is not None:
        icon.scale_to_fit_height(0.36)
        parts = VGroup(label, icon).arrange(RIGHT, buff=0.22)
    box = RoundedRectangle(width=parts.width + 0.5, height=parts.height + 0.34, corner_radius=0.2,
                           stroke_color=color, stroke_width=1.8, fill_color="#06121a", fill_opacity=0.92)
    box.move_to(parts)
    return VGroup(box, parts)


def card(width=3.7, height=2.45, color=CYAN):
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.22, stroke_color=color,
                             stroke_width=1.8, fill_color="#050d13", fill_opacity=0.95)
    halo = frame.copy().set_fill(opacity=0).set_stroke(color, width=9, opacity=0.08)
    return VGroup(halo, frame)


def light_burst(center, color=GOLD, count=18, r0=0.4, r1=2.6):
    rays = VGroup(*[Line(r0 * np.array([np.cos(a), np.sin(a), 0]), r1 * np.array([np.cos(a), np.sin(a), 0]),
                         stroke_color=color, stroke_width=2) for a in np.linspace(0, TAU, count, endpoint=False)])
    rays.move_to(center)
    return LaggedStart(*[ShowPassingFlash(r, time_width=0.5) for r in rays], lag_ratio=0.02)


class IdealConductorHook(MovingCameraScene):
    # ------------------------------------------------------------------ setup
    def construct(self):
        self.camera.background_color = BACKGROUND
        install_clock(self)
        self.camera.frame.save_state()
        self.plan = build_plan()
        self.dust = ambient_dust()
        self.add(self.dust)
        Beat.report = []

        wanted = os.environ.get("CONDUCTOR_BEATS")
        indices = [s.index for s in self.plan.segments]
        if wanted:
            indices = [i for i in indices if str(i) in {w.strip() for w in wanted.split(",")}]
        self.wait(self.plan.segments[0].start if indices and indices[0] == 1 else 0.3)
        carry, previous = None, None
        for index in indices:
            beat = Beat(self, self.plan.segment(index))
            carry = getattr(self, f"beat_{index:02d}")(beat, carry if previous == index - 1 else None)
            beat.finish()
            previous = index
        print(f"Intro length: {self.time:.2f}s (plan {self.plan.total:.2f}s)")
        for line in Beat.report:
            print("  timing:", line)

    # --------------------------------------------------------------- helpers
    def purge(self, *mobs):
        """Stop and remove mobjects AND every scene object inside their families
        (children added on their own would otherwise stay on stage)."""
        family = set()
        for m in mobs:
            if isinstance(m, Mobject):
                freeze(m)
                family.update(m.get_family())
        self.remove(*[x for x in self.mobjects if x in family])

    def clear(self, *mobs, run_time=0.6, shift=ORIGIN, extra=()):
        """Freeze (so families stay fixed during the fade), fade out, then remove."""
        mobs = [m for m in mobs if isinstance(m, Mobject)]
        for m in mobs:
            freeze(m)
        if mobs:
            self.play(*[FadeOut(m, shift=shift) for m in mobs], *extra, run_time=run_time)
        self.purge(*mobs)

    def fade_carry(self, carry, run_time=0.6, keep=(), extra=()):
        if carry:
            items = carry.values() if isinstance(carry, dict) else [carry]
            self.clear(*[m for m in items if isinstance(m, Mobject) and all(m is not k for k in keep)],
                       run_time=run_time, extra=extra)

    def hbar(self, height=1.25):
        h = hbar_character(height)
        h.eyes = VGroup(h[2], h[3], h[4])
        return h

    def blink(self, h, run_time=0.28):
        self.play(h.eyes.animate.stretch(0.1, 1), rate_func=there_and_back, run_time=run_time)

    @staticmethod
    def track_pupils(h, target):
        """Pupils follow a mobject — the character watches the action."""
        eyes, pupils = (h[2], h[3]), h[4]

        def upd(p):
            for eye, pupil in zip(eyes, pupils):
                d = target.get_center() - eye.get_center()
                n = np.linalg.norm(d)
                off = d / n * eye.width * 0.22 if n > 1e-6 else ORIGIN
                pupil.move_to(eye.get_center() + off)
        pupils.add_updater(upd)

    # =================================================================== 1
    def beat_01(self, b, carry):
        """تخيّل لو أخبرتك أن تيارًا كهربائيًا يمكنه الاستمرار إلى الأبد...
        دون أن يفقد شيئًا من طاقته!"""
        frame = self.camera.frame
        c, R = np.array([-3.75, 0.05, 0]), 1.8
        electron = glow(CYAN, 0.08)
        orbit = Arc(radius=R, start_angle=PI / 2, angle=TAU, arc_center=c)
        electron.move_to(orbit.get_start())
        trail = TracedPath(electron.get_center, stroke_color=CYAN, stroke_width=3.5, dissipating_time=0.8)
        frame.scale(0.55).move_to(c + UP * 0.9)
        self.add(trail)
        self.play(FadeIn(electron, scale=0.2), run_time=0.45)
        self.play(MoveAlongPath(electron, orbit), Restore(frame), run_time=2.2, rate_func=smooth)

        # the conducting ring and its eternal current
        path = Circle(radius=R).move_to(c)
        ring = tk.conductor_track(path, color=METAL, inner_color="#0b2430", width=15)
        halo = tk.glowing_path(path.copy(), color=CYAN, width=1.0, passes=4, outer_opacity=0.05)
        flow = tk.FlowParticles(path, count=30, radius=0.05, color=ICE)
        flow.add_updater(lambda m, dt: m.phase.increment_value(0.09 * dt))
        current = CurvedArrow(c + R * 1.28 * np.array([np.cos(2.0), np.sin(2.0), 0]),
                              c + R * 1.28 * np.array([np.cos(1.1), np.sin(1.1), 0]),
                              angle=-0.75, color=GOLD, stroke_width=3)
        i_label = eq("I", 40, GOLD).next_to(current, UP, buff=0.08)
        ring_eq = eq(r"I(t)=I_0", 40, CYAN).move_to(c + DOWN * (R + 0.75))
        live_breathe(halo, 0.4, 1.0, freq=0.35, fill=False)
        self.play(FadeOut(electron), FadeIn(ring, scale=0.94), FadeIn(halo), FadeIn(flow),
                  run_time=1.0)
        self.purge(trail, electron)
        self.play(Create(current), FadeIn(i_label), FadeIn(ring_eq, shift=UP * 0.1), run_time=0.8)

        # live graph: zoom the time axis out — the ideal current never decays
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 1.25, 0.25], x_length=5.6, y_length=2.8, tips=True,
                    axis_config={"stroke_opacity": 0.65, "stroke_width": 1.6, "include_ticks": False})
        axes.move_to([3.5, 0.55, 0])
        t_lab = eq("t", 36, METAL).next_to(axes.x_axis.get_end(), DOWN, buff=0.12)
        I_lab = eq("I", 36, METAL).next_to(axes.y_axis.get_end(), LEFT, buff=0.12)
        draw = tracker(self, 0.0)
        logT = tracker(self, 1.0)
        tau = 2.5

        def ideal_curve():
            x1 = max(0.02, 10 * draw.get_value())
            return Line(axes.c2p(0, 1), axes.c2p(x1, 1), stroke_color=CYAN, stroke_width=4)

        def ghost_curve():
            T = 10 ** logT.get_value()
            xs = 10 * np.linspace(0, 1, 160) ** 3 * draw.get_value()
            ys = np.exp(-xs * T / 10 / tau)
            return VMobject(stroke_color=ORANGE, stroke_width=3, stroke_opacity=0.8).set_points_smoothly(
                [axes.c2p(x, y) for x, y in zip(xs, ys)])
        ideal = always_redraw(ideal_curve)
        ghost = always_redraw(ghost_curve)
        ideal_glow = always_redraw(lambda: ideal_curve().set_stroke(width=14, opacity=0.12))
        legend = VGroup(
            VGroup(ar("موصل مثالي", 22, CYAN), Line(ORIGIN, RIGHT * 0.5, stroke_color=CYAN, stroke_width=4)
                   ).arrange(LEFT, buff=0.15),
            VGroup(ar("موصل عادي", 22, ORANGE), Line(ORIGIN, RIGHT * 0.5, stroke_color=ORANGE, stroke_width=3)
                   ).arrange(LEFT, buff=0.15),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.12).next_to(axes, UP, buff=0.1).align_to(axes, RIGHT)

        # time-scale word under the end of the time axis: seconds ... centuries ... ∞
        stages = [(1.78, "ثوانٍ"), (3.56, "دقائق"), (4.94, "ساعات"), (6.41, "أيام"), (7.5, "أشهر"),
                  (9.5, "سنوات"), (99, "قرون")]
        words = VGroup(*[ar(w, 24, METAL) for _, w in stages])
        inf_mark = num_text("∞", 44, CYAN)
        scale_box = VGroup(*words, inf_mark)
        for w in scale_box:
            w.move_to(axes.c2p(9.2, 0) + DOWN * 0.42)
        finale = tracker(self, 0.0)

        def show_stage(group):
            v = logT.get_value()
            idx = next(i for i, (lim, _) in enumerate(stages) if v < lim)
            for i, w in enumerate(words):
                w.set_opacity((1 - finale.get_value()) if (i == idx and draw.get_value() > 0.99) else 0)
            inf_mark.set_opacity(finale.get_value())
        scale_box.add_updater(show_stage)
        title = heading("تيار إلى الأبد", size=36, y=3.35)
        self.play(Create(axes), FadeIn(t_lab), FadeIn(I_lab), FadeIn(legend, shift=LEFT * 0.2),
                  FadeIn(title[0], shift=DOWN * 0.1), Create(title[1]), run_time=1.0)
        self.add(ideal_glow, ideal, ghost, scale_box)
        self.play(draw.animate.set_value(1), run_time=1.3, rate_func=linear)
        drive(self, logT, 10.2, 4.6, rate=rate_functions.ease_in_quad)
        drive(self, finale, 1.0, 0.8, delay=4.4)

        # دون أن يفقد شيئًا من طاقته
        b.at(1)
        bars = VGroup()
        for row, (txt, col) in enumerate([("الطاقة: موصل مثالي", CYAN), ("الطاقة: موصل عادي", ORANGE)]):
            shell = RoundedRectangle(width=3.4, height=0.3, corner_radius=0.12, stroke_color=METAL,
                                     stroke_width=1.2).move_to([2.1, -1.75 - 0.6 * row, 0])
            lab = ar(txt, 22, col).next_to(shell, RIGHT, buff=0.2)
            bars.add(VGroup(shell, lab))
        energy = tracker(self, 1.0)

        def fill_bar(shell, value, col):
            w = max(0.02, 3.3 * value)
            return RoundedRectangle(width=w, height=0.2, corner_radius=0.08, stroke_width=0, fill_color=col,
                                    fill_opacity=0.9).align_to(shell, LEFT).shift(RIGHT * 0.05).set_y(shell.get_y())
        fill_ideal = always_redraw(lambda: fill_bar(bars[0][0], 1.0, CYAN))
        fill_real = always_redraw(lambda: fill_bar(bars[1][0], energy.get_value(), ORANGE))
        pct_ideal = num_text("100%", 22, CYAN).next_to(bars[0][0], LEFT, buff=0.18)
        pct_real = LiveNumber(lambda: 100 * energy.get_value(), "{:.0f}%", 22, ORANGE, align=RIGHT,
                              at=bars[1][0].get_left() + LEFT * 0.18)
        self.play(FadeIn(bars), FadeIn(fill_ideal), FadeIn(fill_real), FadeIn(pct_ideal), FadeIn(pct_real),
                  run_time=0.8)
        drive(self, energy, 0.0, 2.2, rate=rate_functions.ease_out_cubic)
        law = eq(r"\frac{dE}{dt}=0", 46, CYAN).move_to([-3.75, -3.05, 0])
        self.play(ReplacementTransform(ring_eq, law), run_time=0.9)
        tk.equation_impact(self, law, color=CYAN, run_time=0.9)
        return dict(ring=VGroup(ring, halo, flow, current, i_label, law), center=c, radius=R,
                    graph=VGroup(axes, t_lab, I_lab, legend, ideal, ghost, ideal_glow, scale_box, title),
                    bars=VGroup(bars, fill_ideal, fill_real, pct_ideal, pct_real))

    # =================================================================== 2
    def beat_02(self, b, carry):
        """لا مقاومة كهربائية... لا طاقة تتبدد على شكل حرارة...
        فقط شحنات كهربائية تتحرك بحرية تامة، دون أي مقاومة!"""
        frame = self.camera.frame
        if carry:
            dive = carry["center"] + carry["radius"] * RIGHT
            self.play(FadeOut(carry["graph"]), FadeOut(carry["bars"]),
                      frame.animate.scale(0.09).move_to(dive), run_time=0.9, rate_func=rate_functions.ease_in_cubic)
            self.purge(carry["graph"], carry["bars"], carry["ring"])
            frame.restore()

        heat = tracker(self, 1.0)    # thermal agitation of the lattice
        chaos = tracker(self, 1.0)   # scattering of the electrons
        R_val = tracker(self, 4.7)
        y0, half_h, half_w = -0.25, 1.15, 6.25
        body = RoundedRectangle(width=2 * half_w, height=2 * half_h, corner_radius=0.45,
                                fill_color="#07131a", fill_opacity=0.97, stroke_color=ORANGE, stroke_width=2.4)
        body.move_to([0, y0, 0])
        rails = VGroup(*[Line([-half_w + 0.3, y0 + s * (half_h - 0.12), 0], [half_w - 0.3, y0 + s * (half_h - 0.12), 0],
                              stroke_color=METAL, stroke_width=1, stroke_opacity=0.35) for s in (1, -1)])
        lattice = tk.CrystalLattice(rows=4, cols=23, spacing=0.52, stagger=True, bond_opacity=0.16,
                                    ion_radius=0.06, color=GOLD).move_to([0, y0, 0])
        rng = np.random.default_rng(3)
        ion_data = [(ion.get_center().copy(), rng.uniform(5, 9), rng.uniform(5, 9), rng.uniform(0, TAU))
                    for ion in lattice.ions]
        hot_halos = VGroup(*[Circle(radius=0.2, stroke_width=0, fill_color=ORANGE, fill_opacity=0.2).move_to(p)
                             for p, *_ in ion_data])

        def jiggle(group):
            t, a = now(), 0.085 * heat.get_value()
            for ion, (p, w1, w2, ph) in zip(group, ion_data):
                ion.move_to(p + a * np.array([np.sin(w1 * t + ph), np.cos(w2 * t + 2 * ph), 0]))
        lattice.ions.add_updater(jiggle)
        hot_halos.add_updater(lambda g: [h.set_fill(opacity=0.22 * heat.get_value() * (0.6 + 0.4 * np.sin(6 * now() + i)))
                                         for i, h in enumerate(g)])

        electrons = VGroup()
        e_data = []
        for k in range(30):
            e = glow(ICE, 0.055, n=3, opacity=0.22)
            e_data.append(dict(x=rng.uniform(-half_w + 0.4, half_w - 0.4), y=rng.uniform(-0.8, 0.8),
                               w=rng.uniform(5, 9), ph=rng.uniform(0, TAU)))
            electrons.add(e)

        def drift(group, dt):
            c = chaos.get_value()
            for e, d in zip(group, e_data):
                d["x"] += (2.4 - 1.9 * c) * dt
                if d["x"] > half_w - 0.35:
                    d["x"] -= 2 * half_w - 0.7
                tri = 2 / PI * np.arcsin(np.sin(d["w"] * now() + d["ph"]))
                e.move_to([d["x"] - 0.12 * c * np.cos(3 * d["w"] * now()), y0 + d["y"] + 0.32 * c * tri, 0])
        electrons.add_updater(drift)

        def heat_waves():
            h = heat.get_value()
            waves = VGroup()
            if h < 0.02:
                return waves
            for i, x in enumerate(np.linspace(-5.4, 5.4, 10)):
                ts = np.linspace(0, 1, 30)
                phase = 2.2 * now() + i
                pts = [[x + 0.13 * np.sin(9 * u - phase), y0 + half_h + 0.15 + 1.05 * u, 0] for u in ts]
                waves.add(VMobject(stroke_color=ORANGE, stroke_width=2.2,
                                   stroke_opacity=0.55 * h * (0.6 + 0.4 * np.sin(phase))).set_points_smoothly(pts))
            return waves
        waves = always_redraw(heat_waves)

        wire = VGroup(body, rails, hot_halos, lattice, electrons)
        self.play(FadeIn(wire, scale=1.25), run_time=0.8)
        self.add(waves)

        # لا مقاومة كهربائية
        res = always_redraw(lambda: zigzag([-6.3, 2.75, 0], [-3.7, 2.75, 0], 0.24 * R_val.get_value() / 4.7,
                                           teeth=6, color=interpolate_color(ManimColor(CYAN), ManimColor(ORANGE),
                                                                            R_val.get_value() / 4.7)))
        r_read = LiveNumber(lambda: R_val.get_value(), "R = {:.2f} Ω", 28, WHITE, align=LEFT, at=[-6.3, 2.05, 0])
        chips = VGroup(chip("لا مقاومة", ORANGE), chip("لا حرارة", ORANGE), chip("حركة حرة", CYAN))
        for k, ch in enumerate(chips):
            ch.move_to([4.3 - 4.3 * k, -2.65, 0])  # right-to-left reading order
        self.play(Create(res), FadeIn(r_read), run_time=0.8)
        self.play(FadeIn(chips[0], shift=UP * 0.15), run_time=0.4)
        drive(self, R_val, 0.0, 1.6)
        drive(self, chaos, 0.55, 1.6)

        # لا طاقة تتبدد على شكل حرارة
        b.at(1)
        thermo = thermometer(height=2.0, level=0.85).move_to([6.35, 2.45, 0])
        power = eq(r"P=I^2R", 46, ORANGE).move_to([1.6, 2.65, 0])
        self.play(FadeIn(thermo), Write(power), FadeIn(chips[1], shift=UP * 0.15), run_time=0.9)
        power0 = eq(r"P=0", 46, CYAN).move_to(power)
        self.play(TransformMatchingShapes(power, power0), run_time=0.9)
        drive(self, heat, 0.0, 2.2)
        drive(self, thermo.level, 0.08, 2.2)

        # فقط شحنات كهربائية تتحرك بحرية تامة
        b.at(2)
        drive(self, chaos, 0.0, 1.4)
        self.play(FadeIn(chips[2], shift=UP * 0.15), body.animate.set_stroke(CYAN, width=3), run_time=0.8)
        top_rail = Line([-half_w + 0.3, y0 + half_h - 0.12, 0], [half_w - 0.3, y0 + half_h - 0.12, 0])
        tk.travelling_pulse(self, top_rail, color=CYAN, width=5, run_time=1.1)

        # دون أي مقاومة!
        b.at(3)
        r0 = eq(r"R=0", 52, CYAN).move_to([-5.0, 1.95, 0])
        self.play(FadeOut(r_read, shift=UP * 0.2), FadeIn(r0, scale=1.6), run_time=0.5)
        self.purge(r_read)
        tk.equation_impact(self, r0, color=CYAN, run_time=0.9)
        return dict(wire=wire, waves=waves, top=VGroup(res, thermo, power0, r0), chips=chips)

    # =================================================================== 3
    def beat_03(self, b, carry):
        """يبدو الأمر وكأنه ضربٌ من الخيال العلمي، أليس كذلك؟"""
        stars = starfield()
        scan = scan_lines()
        brackets = hud_brackets()
        veil = Rectangle(width=15, height=9, stroke_width=0, fill_color=BACKGROUND, fill_opacity=0)
        self.add(veil, stars, scan)
        drive(self, stars.level, 1.0, 1.4)
        drive(self, scan.level, 1.0, 1.0)
        olds = []
        if carry:
            olds = [carry["wire"], carry["waves"], carry["top"], carry["chips"]]
            self.play(veil.animate.set_fill(opacity=0.62), FadeOut(carry["chips"]), Create(brackets),
                      run_time=1.0)
        else:
            self.play(Create(brackets), run_time=1.0)
        glitch = VGroup(*[Rectangle(width=np.random.uniform(1, 5), height=0.06, stroke_width=0,
                                    fill_color=np.random.choice([CYAN, RED, VIOLET]), fill_opacity=0) for _ in range(9)])
        rng = np.random.default_rng(9)

        def flicker(g):
            on = (int(now() * 12) % 7) == 0
            for r in g:
                r.move_to([rng.uniform(-6, 6), rng.uniform(-3.6, 3.6), 0])
                r.set_fill(opacity=0.35 if on and rng.random() < 0.6 else 0)
        glitch.add_updater(flicker)
        self.add(glitch)
        question = ar("هل يبدو هذا خيالًا علميًا؟", 44, WHITE).move_to([0, 2.9, 0])
        halo = glow_text(question, CYAN)
        self.play(rtl_reveal(question, run_time=1.4), FadeIn(halo), run_time=1.4)
        self.play(self.camera.frame.animate.rotate(0.035).scale(0.96), run_time=1.6, rate_func=there_and_back)

        # أليس كذلك؟
        b.at(1)
        h = self.hbar(1.35).move_to([5.0, -2.2, 0])
        marks = floating_marks(center=[5.0, -1.0, 0], spread=1.4, count=6)
        self.add(marks)
        drive(self, marks.level, 1.0, 0.8)
        self.play(FadeIn(h, shift=UP * 0.6, scale=0.6), run_time=0.6, rate_func=rate_functions.ease_out_back)
        self.play(Rotate(h, 0.18), run_time=0.4)
        self.blink(h)
        return dict(olds=olds, veil=veil, stars=stars, scan=scan, brackets=brackets, glitch=glitch,
                    question=VGroup(question, halo), hbar=h, marks=marks)

    # =================================================================== 4
    def beat_04(self, b, carry):
        """لكن في عالم الفيزياء، هناك مفهوم يصف هذه المادة العجيبة... إنه الموصل المثالي."""
        grid = NumberPlane(x_range=[-8, 8, 0.5], y_range=[-5, 5, 0.5],
                           background_line_style={"stroke_color": CYAN, "stroke_width": 0.6, "stroke_opacity": 0.12},
                           axis_config={"stroke_opacity": 0}).set_z_index(-5)
        grid.x_axis.set_stroke(opacity=0)
        grid.y_axis.set_stroke(opacity=0)
        self.grid = grid
        laws = VGroup(eq(r"\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}", 34, WHITE),
                      eq(r"\mathbf{J}=\sigma\mathbf{E}", 34, WHITE), eq(r"V=IR", 34, WHITE),
                      eq(r"\mathbf{F}=q\mathbf{E}", 34, WHITE), eq(r"\oint\mathbf{E}\cdot d\boldsymbol{\ell}=0", 34, WHITE),
                      eq(r"\nabla^2V=0", 34, WHITE))
        spots = [[-5.4, 2.6], [5.3, 2.7], [-5.9, -0.4], [5.8, -0.2], [-4.6, -2.9], [4.7, -2.9]]
        for i, (lw, p) in enumerate(zip(laws, spots)):
            lw.move_to([*p, 0]).set_opacity(0.22)
            live_bob(lw, 0.08, 0.18 + 0.04 * i, phase=i)
        if carry:
            drive(self, carry["stars"].level, 0.0, 1.2)
            drive(self, carry["scan"].level, 0.0, 1.0)
            freeze(carry["glitch"], carry["hbar"])
            self.remove(carry["glitch"])
            fade = [carry["veil"], carry["brackets"], carry["question"], carry["hbar"], *carry["olds"]]
            drive(self, carry["marks"].level, 0.0, 0.5)
            self.play(*[FadeOut(m) for m in fade], Create(grid, lag_ratio=0.02), run_time=1.3)
            self.purge(*fade)
        else:
            self.play(Create(grid, lag_ratio=0.02), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(lw, shift=UP * 0.2) for lw in laws], lag_ratio=0.15), run_time=1.2)

        # هناك مفهوم يصف هذه المادة العجيبة...
        b.at(1)
        center, R = np.array([0, -0.45, 0]), 1.6
        rng = np.random.default_rng(21)
        motes = VGroup()
        targets = []
        for k in range(90):
            a = rng.uniform(0, TAU)
            m = glow(rng.choice([CYAN, ICE, GOLD]), rng.uniform(0.025, 0.05), n=3, opacity=0.18)
            m.move_to(rng.uniform(5, 8) * np.array([np.cos(a), 0.6 * np.sin(a), 0]))
            motes.add(m)
            th = TAU * k / 90
            targets.append(center + R * np.array([np.cos(th), np.sin(th), 0]))
        self.add(motes)
        self.play(LaggedStart(*[m.animate(path_arc=PI / 3).move_to(t) for m, t in zip(motes, targets)],
                              lag_ratio=0.012), run_time=2.4, rate_func=smooth)
        sphere = spinning_rim(metal_sphere(R, center))
        shell = globe(R * 1.002, center, color=CYAN, opacity=0.18, rate=0.25)
        self.play(FadeIn(sphere, scale=0.9), FadeIn(shell), FadeOut(motes, scale=1.1), run_time=1.1)
        self.purge(motes)

        # إنه الموصل المثالي.
        b.at(2)
        title = ar("الموصل المثالي", 66, WHITE).move_to([0, 2.55, 0])
        halo = glow_text(title, CYAN, layers=4)
        sweep = Line(title.get_corner(DL) + DOWN * 0.15, title.get_corner(DR) + DOWN * 0.15,
                     stroke_color=GOLD, stroke_width=5)
        self.play(rtl_reveal(title, run_time=1.0), light_burst(center, CYAN, 24, R + 0.15, R + 2.2), run_time=1.0)
        self.play(FadeIn(halo), run_time=0.4)
        self.play(ShowPassingFlash(sweep, time_width=0.6), Indicate(title, color=ICE, scale_factor=1.04),
                  run_time=0.9)
        return dict(grid=grid, laws=laws, sphere=sphere, shell=shell, title=VGroup(title, halo),
                    center=center, R=R)

    # =================================================================== 5
    def beat_05(self, b, carry):
        """الموصل المثالي هو مادة افتراضية تتمتع بموصلية كهربائية لا نهائية، أو بعبارة أخرى،
        بمقاومة كهربائية معدومة تمامًا، مما يسمح للشحنات الكهربائية بالحركة دون فقدان الطاقة بسبب المقاومة."""
        top = heading("الموصل المثالي", 38, y=3.35)
        sc = np.array([-4.65, 0.35, 0])
        if carry:
            sphere, shell, grid, laws = carry["sphere"], carry["shell"], carry["grid"], carry["laws"]
            self.play(ReplacementTransform(carry["title"], top), sphere.animate.scale(0.78).move_to(sc),
                      shell.animate.scale(0.78).move_to(sc), laws.animate.set_opacity(0.1), run_time=1.2)
        else:
            sphere, shell = spinning_rim(metal_sphere(1.25, sc)), globe(1.25, sc, opacity=0.18, rate=0.25)
            grid, laws = VGroup(), VGroup()
            self.play(FadeIn(top), FadeIn(sphere), FadeIn(shell), run_time=1.2)
        Rs = sphere.width / 2
        dashed = DashedVMobject(Circle(radius=Rs * 1.2, stroke_color=GOLD, stroke_width=2), num_dashes=40).move_to(sc)
        live_spin(dashed, 0.3)
        hypo = chip("مادة افتراضية", GOLD).move_to(sc + DOWN * (Rs + 0.75))
        self.play(Create(dashed), FadeIn(hypo, shift=UP * 0.15), run_time=0.9)

        # موصلية كهربائية لا نهائية — the conductivity gauge runs to infinity
        g = dial(radius=1.0, color=CYAN).move_to([-0.6, 1.45, 0])

        def sigma_text(v):
            if v > 0.985:
                return "σ = ∞"
            n = int(6 + 9 * v)
            return "σ = " + f"{10 ** n:,}" + " S/m"
        sig = LiveNumber(lambda: g.value.get_value(), sigma_text, 30, CYAN, align=LEFT, at=[0.85, 1.6, 0])
        ohm = eq(r"\mathbf{J}=\sigma\mathbf{E}", 42, WHITE).move_to([-0.9, -0.8, 0])
        j_arrows = VGroup(*[Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=CYAN, stroke_width=4) for _ in range(6)])

        def grow_j(group):
            v = g.value.get_value()
            length = 0.15 + 0.85 * min(1.0, v * 1.15)
            for k, a in enumerate(group):
                x = 0.9 + 0.95 * k
                a.put_start_and_end_on([x - length / 2, -0.8, 0], [x + length / 2, -0.8, 0])
                a.set_opacity(0.35 + 0.65 * v)
        j_arrows.add_updater(grow_j)
        j_dots = VGroup(*[Dot(radius=0.03, color=ICE) for _ in range(18)])
        j_dots.add_updater(lambda grp: [d.move_to([0.6 + ((k / 18 + (0.05 + 0.6 * g.value.get_value()) * now()) % 1.0) * 5.7,
                                                   -0.8 + 0.28 * np.sin(k * 2.3), 0]).set_opacity(0.3 + 0.7 * g.value.get_value())
                                         for k, d in enumerate(grp)])
        self.play(FadeIn(g, shift=UP * 0.2), FadeIn(sig), run_time=0.7)
        self.play(Write(ohm), FadeIn(j_arrows), FadeIn(j_dots), run_time=0.8)
        drive(self, g.value, 1.0, 3.4, rate=rate_functions.ease_in_quad)
        self.wait(1.4)
        inf_chip = chip("موصلية لا نهائية", CYAN).move_to([2.6, 0.75, 0])
        self.play(FadeIn(inf_chip, shift=UP * 0.15), run_time=0.6)

        # أو بعبارة أخرى
        b.at(1)
        rho = eq(r"\rho=\frac{1}{\sigma}", 44, GOLD).move_to([5.75, 1.6, 0])
        self.play(TransformFromCopy(g[-1], rho), run_time=0.9)
        rho2 = eq(r"\rho=\frac{1}{\sigma}\to 0", 44, GOLD).move_to([5.55, 1.6, 0])
        self.play(TransformMatchingShapes(rho, rho2), run_time=0.7)

        # بمقاومة كهربائية معدومة تمامًا
        b.at(2)
        self.play(FadeOut(VGroup(ohm, j_arrows, j_dots)), run_time=0.4)
        self.purge(ohm, j_arrows, j_dots)
        R_val = tracker(self, 3.2)
        res = always_redraw(lambda: zigzag([-1.7, -0.75, 0], [1.5, -0.75, 0], 0.28 * R_val.get_value() / 3.2,
                                           teeth=7, color=interpolate_color(ManimColor(CYAN), ManimColor(ORANGE),
                                                                            R_val.get_value() / 3.2), width=5))
        r_read = LiveNumber(lambda: R_val.get_value(), "R = {:.2f} Ω", 26, WHITE, align=ORIGIN, at=[-0.1, -1.35, 0])
        law = eq(r"R=\rho\,\frac{L}{A}", 46, WHITE).move_to([3.6, -0.75, 0])
        self.play(Create(res), FadeIn(r_read), Write(law), run_time=1.0)
        drive(self, R_val, 0.0, 1.6)
        self.wait(1.1)
        law0 = eq(r"R=0", 52, CYAN).move_to(law)
        self.play(TransformMatchingShapes(law, law0), run_time=0.7)
        zero_chip = chip("مقاومة معدومة", CYAN).move_to([3.7, -1.55, 0])
        self.play(FadeIn(zero_chip, shift=UP * 0.15), run_time=0.5)

        # مما يسمح للشحنات بالحركة دون فقدان الطاقة بسبب المقاومة
        b.at(3)
        surface = Circle(radius=Rs * 1.02).move_to(sc)
        orbit = tk.FlowParticles(surface, count=22, radius=0.04, color=ICE)
        orbit.add_updater(lambda m, dt: m.phase.increment_value(0.12 * dt))
        loss = tracker(self, 0.3)
        yc, th = -2.6, 0.5
        x_in, x_split, x_out = 6.5, 4.2, -1.7

        def sankey():
            w = loss.get_value()
            top_y, bot_y = yc + th / 2, yc - th / 2
            main = Polygon([x_in, top_y, 0], [x_out, top_y, 0], [x_out, top_y - (th - w), 0],
                           [x_split - 0.35, top_y - (th - w), 0], [x_split, bot_y, 0], [x_in, bot_y, 0],
                           stroke_width=0, fill_color=CYAN, fill_opacity=0.35)
            grp = VGroup(main)
            if w > 0.01:
                ts = np.linspace(0, 1, 24)
                outer = [[x_split - 0.35 - 1.3 * t, top_y - (th - w) - 0.95 * t ** 1.6, 0] for t in ts]
                inner = [[x_split - 1.3 * t + 0.1 * t, bot_y - 0.95 * t ** 1.6 + w * 0.2 * t, 0] for t in ts]
                branch = VMobject(stroke_width=0, fill_color=ORANGE, fill_opacity=0.6)
                branch.set_points_as_corners(outer + inner[::-1] + [outer[0]])
                grp.add(branch)
            return grp
        flow_band = always_redraw(sankey)
        band_dots = VGroup(*[Dot(radius=0.035, color=ICE) for _ in range(16)])

        def run_dots(group):
            for k, d in enumerate(group):
                u = (k / 16 + 0.22 * now()) % 1.0
                d.move_to([x_in - u * (x_in - x_out), yc + 0.12 * np.sin(7 * u + k), 0])
        band_dots.add_updater(run_dots)
        lab_in = ar("طاقة داخلة", 22, CYAN).next_to([x_in, yc, 0], UP, buff=0.35).shift(LEFT * 0.6)
        lab_out = ar("طاقة خارجة", 22, CYAN).next_to([x_out, yc, 0], UP, buff=0.35).shift(RIGHT * 0.7)
        lab_heat = ar("حرارة", 22, ORANGE).move_to([2.35, -3.45, 0])
        heat_lab_op = lambda m: m.set_opacity(min(1, loss.get_value() / 0.15))
        lab_heat.add_updater(heat_lab_op)
        self.play(FadeIn(flow_band), FadeIn(band_dots), FadeIn(lab_in), FadeIn(lab_out), FadeIn(lab_heat),
                  FadeIn(orbit), run_time=1.0)
        self.wait(1.0)
        drive(self, loss, 0.0, 2.6)
        self.wait(2.7)
        w_eq = eq(r"\int I^2R\,dt=0", 36, CYAN).move_to([0.2, -3.45, 0])
        self.play(Write(w_eq), run_time=0.8)
        tk.equation_impact(self, w_eq, color=CYAN, run_time=0.8)
        return dict(sphere=sphere, shell=shell, grid=grid, laws=laws, top=top,
                    rest=VGroup(dashed, hypo, g, sig, inf_chip, rho2, res, r_read, law0, zero_chip, flow_band,
                                band_dots, lab_in, lab_out, lab_heat, w_eq),
                    orbit=orbit)

    # =================================================================== 6
    def beat_06(self, b, carry):
        """ولكن... هناك مشكلة صغيرة! فهذا الموصل المثالي... ليس سوى نموذج نظري،
        لا وجود له في الطبيعة بصورته المثالية التامة!"""
        center, R = np.array([0, -0.2, 0]), 1.6
        vignette = Rectangle(width=13.9, height=7.7, stroke_color=RED, stroke_width=70, fill_opacity=0)
        live_breathe(vignette, 0.05, 0.32, freq=0.7, fill=False)
        if carry:
            sphere, shell = carry["sphere"], carry["shell"]
            scale = R / (sphere.width / 2)
            self.play(*[FadeOut(m) for m in (carry["rest"], carry["top"], carry["orbit"], carry["laws"])],
                      sphere.animate.scale(scale).move_to(center), shell.animate.scale(scale).move_to(center),
                      FadeIn(vignette), run_time=1.3)
            self.purge(carry["rest"], carry["top"], carry["orbit"], carry["laws"])
            grid = carry["grid"]
        else:
            sphere, shell = spinning_rim(metal_sphere(R, center)), globe(R, center, opacity=0.18, rate=0.25)
            grid = VGroup()
            self.play(FadeIn(sphere), FadeIn(shell), FadeIn(vignette), run_time=1.3)

        # هناك مشكلة صغيرة!
        b.at(1)
        warn = VGroup(ar("مشكلة صغيرة!", 40, GOLD), warning_sign(0.95)).arrange(RIGHT, buff=0.3).move_to([0, 2.85, 0])
        self.play(GrowFromCenter(warn[1]), FadeIn(warn[0], shift=LEFT * 0.2), run_time=0.6,
                  rate_func=rate_functions.ease_out_back)
        self.play(Wiggle(warn[1], scale_value=1.15, rotation_angle=0.08 * TAU), run_time=0.8)

        # فهذا الموصل المثالي...
        b.at(2)
        self.play(FocusOn(sphere, color=GOLD), run_time=0.4)
        self.play(Circumscribe(sphere, Circle, color=GOLD, fade_out=True, buff=0.1), run_time=0.6)
        cracks = crack_lines(center, R, seed=8, count=6, color=ICE)
        self.play(LaggedStart(*[Create(c) for c in cracks], lag_ratio=0.15),
                  self.camera.frame.animate.shift(RIGHT * 0.05), run_time=0.9, rate_func=rate_functions.rush_into)
        self.play(self.camera.frame.animate.shift(LEFT * 0.05), run_time=0.2)

        # ليس سوى نموذج نظري — the metal dissolves into a blueprint
        b.at(3)
        blue_circle = DashedVMobject(Circle(radius=R, stroke_color=CYAN, stroke_width=2.5), num_dashes=60).move_to(center)
        radius_line = Line(center, center + R * np.array([np.cos(0.6), np.sin(0.6), 0]), stroke_color=GOLD, stroke_width=2.5)
        r_lab = eq("R", 36, GOLD).move_to(radius_line.get_center() + UP * 0.25 + LEFT * 0.1)
        axes_bp = VGroup(DashedLine(center + LEFT * (R + 0.6), center + RIGHT * (R + 0.6), dash_length=0.12,
                                    stroke_color=CYAN, stroke_opacity=0.5),
                         DashedLine(center + DOWN * (R + 0.6), center + UP * (R + 0.6), dash_length=0.12,
                                    stroke_color=CYAN, stroke_opacity=0.5))
        dot = Dot(center, radius=0.05, color=GOLD)
        blueprint = VGroup(blue_circle, axes_bp, radius_line, r_lab, dot)
        st = stamp("نموذج نظري", RED, 44).move_to([3.7, 1.25, 0])
        self.play(FadeOut(sphere), FadeOut(cracks), shell.animate.set_stroke(opacity=0.55),
                  Create(blue_circle), Create(axes_bp), run_time=0.9)
        self.play(Create(radius_line), FadeIn(r_lab), FadeIn(dot), run_time=0.5)
        self.purge(sphere, cracks)
        self.play(FadeIn(st, scale=2.4), run_time=0.35, rate_func=rate_functions.rush_into)
        self.play(Flash(st.get_center(), color=RED, line_length=0.5, num_lines=14, flash_radius=1.6),
                  self.camera.frame.animate.shift(DOWN * 0.06), run_time=0.3)
        self.play(self.camera.frame.animate.shift(UP * 0.06), run_time=0.15)

        # لا وجود له في الطبيعة بصورته المثالية التامة!
        b.at(4)
        model = VGroup(shell, blueprint)
        self.play(model.animate.scale(0.6).move_to([-4.75, 0.5, 0]), st.animate.scale(0.7).move_to([-4.75, -1.55, 0]),
                  FadeOut(warn), run_time=1.0)
        axes = Axes(x_range=[0, 5, 1], y_range=[0, 3, 1], x_length=7.4, y_length=3.7, tips=False,
                    axis_config={"stroke_opacity": 0.6, "include_ticks": False}).move_to([2.6, -0.6, 0])
        y_lab = eq(r"\rho\;(10^{-8}\,\Omega\,\mathrm{m})", 30, METAL).next_to(axes.y_axis.get_end(), UP, buff=0.15).shift(RIGHT * 0.8)
        data = [("فضة", 1.59), ("نحاس", 1.68), ("ذهب", 2.44), ("ألومنيوم", 2.65)]
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for k, (name, v) in enumerate(data):
            x = 0.6 + k
            bar = Rectangle(width=0.95, height=axes.c2p(0, v)[1] - axes.c2p(0, 0)[1], stroke_width=0,
                            fill_color=ORANGE, fill_opacity=0.8)
            bar.move_to(axes.c2p(x, 0), aligned_edge=DOWN)
            bars.add(bar)
            names.add(ar(name, 22, WHITE).next_to(axes.c2p(x, 0), DOWN, buff=0.18))
            vals.add(num_text(f"{v:.2f}", 22, ORANGE).next_to(bar, UP, buff=0.1))
        x_id = 4.5
        ghost = DashedVMobject(Rectangle(width=0.95, height=1.6, stroke_color=CYAN, stroke_width=2), num_dashes=24)
        ghost.move_to(axes.c2p(x_id, 0), aligned_edge=DOWN)
        live_breathe(ghost, 0.15, 0.8, freq=0.8, fill=False)
        id_name = ar("مثالي", 22, CYAN).next_to(axes.c2p(x_id, 0), DOWN, buff=0.18)
        id_val = num_text("0", 26, CYAN).next_to(axes.c2p(x_id, 0), UP, buff=0.12)
        cross = VGroup(Line(UL, DR), Line(UR, DL)).set_stroke(RED, 5).scale(0.28).move_to(axes.c2p(x_id, 1.0))
        nature = chip("لا وجود له في الطبيعة", RED).move_to([2.6, -3.35, 0])
        self.play(Create(axes), FadeIn(y_lab), run_time=0.6)
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.18),
                  LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.18), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.1) for v in vals], lag_ratio=0.1), run_time=0.6)
        self.play(Create(ghost), FadeIn(id_name), FadeIn(id_val), run_time=0.6)
        self.play(GrowFromCenter(cross), FadeIn(nature, shift=UP * 0.15), run_time=0.6)
        return dict(grid=grid, vignette=vignette, model=model, stamp=st,
                    chart=VGroup(axes, y_lab, bars, names, vals, ghost, id_name, id_val, cross), nature=nature)

    # =================================================================== 7
    def beat_07(self, b, carry):
        """وهنا يبرز سؤال مثير للاهتمام... إذا كانت الموصلات المثالية غير موجودة في الواقع،
        فلماذا يدرسها الفيزيائيون أصلًا؟ ولماذا نهتم بدراسة مادة لا يمكننا الحصول عليها بصورة مثالية؟"""
        keep = {}
        if carry:
            keep = carry
            self.play(FadeOut(carry["vignette"]), FadeOut(carry["nature"]), FadeOut(carry["stamp"]),
                      carry["chart"].animate.scale(0.5).move_to([3.9, 0.55, 0]).set_opacity(0),
                      carry["model"].animate.scale(1.0).move_to([-3.9, 0.55, 0]).set_opacity(0),
                      run_time=0.9)
            self.purge(carry["vignette"], carry["nature"], carry["stamp"], carry["chart"], carry["model"])
        h = self.hbar(1.7).move_to([0, -2.45, 0])
        big_q = ar("؟", 190, GOLD).move_to([0, 0.75, 0])
        q_halo = glow_text(big_q, GOLD, layers=4, opacity=0.25)
        marks = floating_marks(center=[0, -0.3, 0], spread=5.5, count=10, seed=5)
        self.add(marks)
        self.play(FadeIn(h, shift=UP * 1.0), run_time=0.7, rate_func=rate_functions.ease_out_back)
        drive(self, marks.level, 0.8, 1.2)
        self.play(DrawBorderThenFill(big_q), FadeIn(q_halo), run_time=1.2)
        self.track_pupils(h, big_q)
        self.blink(h)
        live_bob(big_q, 0.08, 0.5)
        live_bob(q_halo, 0.08, 0.5)

        # إذا كانت الموصلات المثالية غير موجودة في الواقع
        b.at(1)
        right_card = card(4.4, 3.1, ORANGE).move_to([3.9, 0.45, 0])
        left_card = card(4.4, 3.1, CYAN).move_to([-3.9, 0.45, 0])
        real_t = ar("الواقع", 30, ORANGE).move_to(right_card.get_top() + DOWN * 0.38)
        ideal_t = ar("النموذج المثالي", 30, CYAN).move_to(left_card.get_top() + DOWN * 0.38)
        mini_bars = VGroup(*[Rectangle(width=0.42, height=h_, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8)
                             for h_ in (0.95, 1.0, 1.45, 1.58)]).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)
        mini_bars.move_to(right_card.get_center() + DOWN * 0.35)
        mini_bars.shift(RIGHT * 0.6)
        rho_real = eq(r"\rho>0", 34, ORANGE).next_to(mini_bars, LEFT, buff=0.35)
        mini_globe = globe(0.85, left_card.get_center() + DOWN * 0.3 + RIGHT * 0.55, opacity=0.5, rate=0.4)
        rho_ideal = eq(r"\rho=0", 34, CYAN).move_to(left_card.get_center() + DOWN * 0.3 + LEFT * 1.25)
        neq = eq(r"\neq", 90, GOLD).move_to([0, 0.45, 0])
        self.play(FadeIn(right_card), FadeIn(real_t), LaggedStart(*[GrowFromEdge(m, DOWN) for m in mini_bars]),
                  FadeIn(rho_real), run_time=1.1)
        self.play(FadeIn(left_card), FadeIn(ideal_t), FadeIn(mini_globe), FadeIn(rho_ideal), run_time=0.9)
        h[4].clear_updaters()
        self.track_pupils(h, neq)
        self.play(ReplacementTransform(VGroup(big_q, q_halo), neq), h.animate.scale(0.8).move_to([0, -2.75, 0]),
                  run_time=0.9)
        h[4].clear_updaters()
        self.track_pupils(h, right_card)

        # فلماذا يدرسها الفيزيائيون أصلًا؟
        b.at(2)
        question = ar("فلماذا يدرسها الفيزيائيون أصلًا؟", 42, WHITE).move_to([0, 3.2, 0])
        q_glow = glow_text(question, GOLD, layers=3, opacity=0.2)
        self.play(rtl_reveal(question, run_time=1.3), run_time=1.3)
        self.add(q_glow)
        h[4].clear_updaters()
        self.track_pupils(h, question)
        self.play(Wiggle(h, scale_value=1.08, rotation_angle=0.06 * TAU, n_wiggles=4), run_time=1.0)
        drive(self, marks.level, 1.0, 0.5)
        self.blink(h)

        # ولماذا نهتم بدراسة مادة لا يمكننا الحصول عليها بصورة مثالية؟
        b.at(3)
        cards = VGroup(right_card, left_card, real_t, ideal_t, mini_bars, rho_real, mini_globe, rho_ideal, neq)
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 1.8, 0.5], x_length=8.6, y_length=4.0, tips=True,
                    axis_config={"stroke_opacity": 0.6, "include_ticks": False}).move_to([0.9, -0.3, 0])
        x_lab = ar("تحسين المادة", 22, METAL).next_to(axes.x_axis.get_end(), DOWN, buff=0.15).shift(LEFT * 0.6)
        y_lab = eq(r"\rho", 36, METAL).next_to(axes.y_axis.get_end(), LEFT, buff=0.12)
        curve = axes.plot(lambda x: 1.55 / (1 + 0.6 * x), x_range=[0, 10], color=ORANGE, stroke_width=4)
        zero_line = DashedLine(axes.c2p(0, 0.02), axes.c2p(10, 0.02), dash_length=0.15, stroke_color=CYAN, stroke_width=3)
        zero_lab = ar("المثالي", 24, CYAN).move_to(axes.c2p(1.6, 0) + UP * 0.25)
        drive(self, marks.level, 0.0, 0.8)
        self.play(FadeOut(cards), Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=0.9)
        self.purge(cards)
        self.play(Create(curve), Create(zero_line), FadeIn(zero_lab), run_time=1.2)
        xt = tracker(self, 0.0)
        seeker = glow(GOLD, 0.08)
        seeker.add_updater(lambda m: m.move_to(axes.c2p(xt.get_value(), 1.55 / (1 + 0.6 * xt.get_value()))))
        gap = always_redraw(lambda: DashedLine(seeker.get_center(), axes.c2p(xt.get_value(), 0.02),
                                               dash_length=0.06, stroke_color=GOLD, stroke_width=2))
        gap_val = LiveNumber(lambda: 1.55 / (1 + 0.6 * xt.get_value()), "ρ = {:.3f}", 28, GOLD, align=LEFT,
                             at=[2.2, 1.6, 0])
        h[4].clear_updaters()
        self.track_pupils(h, seeker)
        self.play(FadeIn(seeker), FadeIn(gap), FadeIn(gap_val), h.animate.move_to([-5.7, -2.6, 0]), run_time=0.6)
        drive(self, xt, 9.7, 4.5, rate=rate_functions.ease_out_cubic)
        limit = eq(r"\lim_{n\to\infty}\rho_n=0,\qquad \rho_n\neq 0", 42, WHITE).move_to([2.4, -3.2, 0])
        never = ar("لا يمكننا الحصول عليها بصورة مثالية", 26, CYAN).move_to([0.9, 0.45, 0]).shift(RIGHT * 2.2)
        self.wait(1.5)
        self.play(Write(limit), FadeIn(never, shift=UP * 0.1), run_time=1.2)
        return dict(grid=keep.get("grid") if keep else None, hbar=h, marks=marks,
                    rest=VGroup(question, q_glow, axes, x_lab, y_lab, curve, zero_line, zero_lab, seeker, gap,
                                gap_val, limit, never))

    # =================================================================== 8
    def beat_08(self, b, carry):
        """الجواب أبسط مما قد تتوقع... وأكثر إثارة أيضًا! لأننا أحيانًا، لكي نفهم العالم المعقّد من حولنا،
        نحتاج أولًا إلى تخيّل عالم أبسط... عالم تختفي فيه التعقيدات، وتصبح القوانين الفيزيائية أكثر وضوحًا."""
        if carry:
            h, marks = carry["hbar"], carry["marks"]
            drive(self, marks.level, 0.0, 0.6)
            h[4].clear_updaters()
            self.play(FadeOut(carry["rest"]), h.animate.scale(1.5).move_to([0, -0.7, 0]), run_time=0.9)
            self.purge(carry["rest"])
        else:
            h, marks = self.hbar(1.9).move_to([0, -0.7, 0]), None
            self.play(FadeIn(h), run_time=0.9)
        h[4].clear_updaters()
        self.play(*[m.animate.scale(1.3) for m in (h[2], h[3], h[4][0], h[4][1])],
                  light_burst(h.get_center(), GOLD, 22, 1.2, 3.4), run_time=0.9)
        ans = ar("الجواب أبسط مما قد تتوقع", 42, GOLD).move_to([0, 2.7, 0])
        self.play(rtl_reveal(ans, run_time=1.1), run_time=1.1)

        # وأكثر إثارة أيضًا!
        b.at(1)
        self.play(h.animate.shift(UP * 0.5), rate_func=there_and_back, run_time=0.5)
        self.play(*[Flash(p, color=c, line_length=0.35, num_lines=10, flash_radius=0.5)
                    for p, c in [([-3.2, 1.0, 0], CYAN), ([3.4, 0.6, 0], GOLD), ([-2.0, -2.2, 0], VIOLET),
                                 ([2.6, -2.5, 0], CYAN)]],
                  h.animate.shift(UP * 0.4), rate_func=there_and_back, run_time=0.7)

        # لكي نفهم العالم المعقّد من حولنا — a real conductor, in all its mess
        b.at(2)
        front = tracker(self, 7.6)
        mess_mask = lambda x: float(np.clip((front.get_value() - x) / 0.7, 0, 1))
        clean_mask = lambda x: float(np.clip((x - front.get_value()) / 0.7, 0, 1))
        cy = -0.35
        thetas = np.linspace(0, TAU, 220)
        rr = 2.35 * (1 + 0.1 * np.sin(3 * thetas) + 0.07 * np.cos(5 * thetas) + 0.04 * np.sin(11 * thetas))
        blob_pts = np.column_stack([2.05 * rr * np.cos(thetas), cy + 0.98 * rr * np.sin(thetas), 0 * thetas])
        blob_pts = np.clip(blob_pts, [-6.4, -3.1, 0], [6.4, 2.25, 0])
        inside = lambda p: abs(p[0]) < 6.2 and np.interp(np.arctan2((p[1] - cy) / 0.98, p[0] / 2.05) % TAU, thetas, rr) > \
            np.hypot(p[0] / 2.05, (p[1] - cy) / 0.98) * 1.06
        # outline split into pieces so the sweep can erase it gradually
        outline = VGroup(*[Line(blob_pts[i], blob_pts[i + 1], stroke_color=ORANGE, stroke_width=2.4)
                           for i in range(len(blob_pts) - 1)])
        rng = np.random.default_rng(12)
        lattice = tk.CrystalLattice(rows=9, cols=24, spacing=0.5, stagger=True, bond_opacity=0.12, ion_radius=0.05,
                                    color=GOLD).move_to([0, cy, 0])
        ions_data = []
        keep_ions = VGroup()
        for ion in lattice.ions:
            p = ion.get_center()
            if inside(p) and rng.random() > 0.06:
                keep_ions.add(ion)
                ions_data.append((p.copy(), rng.uniform(5, 10), rng.uniform(5, 10), rng.uniform(0, TAU)))
        impurities = VGroup()
        imp_data = []
        for k in range(10):
            idx = rng.integers(len(ions_data))
            p = ions_data[idx][0]
            m = glow(rng.choice([VIOLET, GREEN, RED]), 0.1, n=3, opacity=0.25).move_to(p + rng.uniform(-0.2, 0.2, 3) * [1, 1, 0])
            impurities.add(m)
            imp_data.append(m.get_center().copy())
        defects = VGroup(*[num_text("⊥", 26, RED).move_to(ions_data[rng.integers(len(ions_data))][0])
                           for _ in range(7)])
        e_mess = VGroup(*[glow(ICE, 0.045, n=3, opacity=0.2) for _ in range(30)])
        e_pos = [ions_data[rng.integers(len(ions_data))][0][:2].copy() for _ in range(30)]
        e_vel = [rng.normal(0, 1, 2) for _ in range(30)]

        def mess_update(group, dt):
            t = now()
            for ion, (p, w1, w2, ph) in zip(keep_ions, ions_data):
                ion.move_to(p + 0.07 * np.array([np.sin(w1 * t + ph), np.cos(w2 * t + ph), 0]))
                ion.set_opacity(mess_mask(p[0]))
            for m, p in zip(impurities, imp_data):
                m.move_to(p + 0.04 * np.array([np.sin(7 * t + p[0]), np.cos(6 * t + p[1]), 0]))
                m.set_opacity(mess_mask(p[0]))
            for d in defects:
                d.set_opacity(0.9 * mess_mask(d.get_x()))
            for k, e in enumerate(e_mess):
                if rng.random() < 0.08:
                    e_vel[k] = rng.normal(0, 1, 2) * 1.6
                new = e_pos[k] + e_vel[k] * dt
                if inside(np.array([new[0], new[1], 0])):
                    e_pos[k] = new
                else:
                    e_vel[k] = -e_vel[k]
                e.move_to([e_pos[k][0], e_pos[k][1], 0])
                e.set_opacity(mess_mask(e_pos[k][0]))
            for seg in outline:
                seg.set_stroke(opacity=mess_mask(seg.get_x()))
            for bond in lattice.bonds:
                bond.set_stroke(opacity=0.12 * mess_mask(bond.get_x()))
        mess = VGroup(lattice.bonds, keep_ions, impurities, defects, e_mess, outline)
        mess.add_updater(mess_update)
        heading_mess = heading("العالم المعقّد", 38, ORANGE, y=3.35, accent=ORANGE)
        self.play(FadeOut(ans), h.animate.scale(0.45).move_to([-6.2, -3.3, 0]).set_opacity(0),
                  FadeIn(mess), FadeIn(heading_mess), run_time=1.2)
        self.purge(h)
        if marks is not None:
            self.purge(marks)

        # labels with live leader lines
        def callout(text, target, pos, color=ORANGE):
            lab = ar(text, 26, color).move_to(pos)
            leader = always_redraw(lambda: Line(lab.get_center() + 0.35 * normalize(target.get_center() - lab.get_center()) * lab.width,
                                                target.get_center(), stroke_color=color, stroke_width=1.6,
                                                stroke_opacity=0.8 * mess_mask(target.get_x())))
            dotm = always_redraw(lambda: Dot(target.get_center(), radius=0.05, color=color).set_opacity(mess_mask(target.get_x())))
            return VGroup(lab, leader, dotm)
        nearest = lambda group, pos: min(group, key=lambda m: np.linalg.norm(m.get_center() - np.array(pos)))
        calls = VGroup(
            callout("شوائب", nearest(impurities, [5.15, 2.75, 0]), [5.15, 2.75, 0]),
            callout("اهتزازات حرارية", nearest(keep_ions, [-4.9, 2.75, 0]), [-4.9, 2.75, 0]),
            callout("تصادمات", nearest(e_mess, [5.2, -3.45, 0]), [5.2, -3.45, 0]),
            callout("عيوب بلورية", nearest(defects, [-5.1, -3.45, 0]), [-5.1, -3.45, 0]),
        )
        self.play(LaggedStart(*[FadeIn(c) for c in calls], lag_ratio=0.35), run_time=2.6)

        # نحتاج أولًا إلى تخيّل عالم أبسط — a sweep from right to left simplifies the world
        b.at(4)
        R = 1.55
        field = sphere_in_uniform_field(R)
        seeds = np.linspace(-2.45, 2.45, 11)
        _, after = expelled_field_lines(R, seeds, x_start=-6.9)
        clean_lines = VGroup()
        for pts in after:
            pts = pts.copy()
            pts[:, 1] += cy
            for side in (1, -1):
                q = pts.copy()
                q[:, 0] *= side
                for i in range(0, len(q) - 1, 6):
                    seg = VMobject(stroke_color=GOLD, stroke_width=2.2).set_points_as_corners(q[i:i + 7])
                    clean_lines.add(seg)
        circle_pieces = VGroup(*[Arc(radius=R, start_angle=a, angle=TAU / 40, arc_center=[0, cy, 0],
                                     stroke_color=CYAN, stroke_width=3.5) for a in np.linspace(0, TAU, 40, endpoint=False)])
        core = Circle(radius=R, stroke_width=0, fill_color=DEEP, fill_opacity=0.95).move_to([0, cy, 0])
        signs = VGroup()
        for a in np.linspace(0, TAU, 24, endpoint=False):
            neg = np.cos(a) < 0
            sgn = num_text("−" if neg else "+", 22, CYAN if neg else RED)
            sgn.move_to([0, cy, 0] + (R + 0.17) * np.array([np.cos(a), np.sin(a), 0]))
            sgn.base = abs(np.cos(a))
            signs.add(sgn)

        def clean_update(group):
            for seg in clean_lines:
                seg.set_stroke(opacity=0.85 * clean_mask(seg.get_x()))
            for arc in circle_pieces:
                arc.set_stroke(opacity=clean_mask(arc.get_x()))
            core.set_fill(opacity=0.95 * clean_mask(0.0))
            for s_ in signs:
                s_.set_opacity((0.25 + 0.75 * s_.base) * clean_mask(s_.get_x()))
        clean = VGroup(core, clean_lines, circle_pieces, signs)
        clean.add_updater(clean_update)
        clean_update(clean)
        self.add(clean)
        beam = Line([0, -4.2, 0], [0, 4.2, 0])
        beam_glow = tk.glowing_path(beam, color=ICE, width=2.5, passes=5, outer_opacity=0.12)
        beam_glow.add_updater(lambda m: m.set_x(front.get_value()))
        sparks = VGroup(*[Dot(radius=0.025, color=ICE) for _ in range(26)])
        sp_rng = np.random.default_rng(1)
        sparks.add_updater(lambda g: [d.move_to([front.get_value() + sp_rng.normal(0, 0.18), sp_rng.uniform(-3.9, 3.9), 0])
                                      .set_opacity(sp_rng.uniform(0.2, 0.9)) for d in g])
        self.add(beam_glow, sparks)
        drive(self, front, -7.7, 3.6, rate=rate_functions.ease_in_out_sine)
        heading_clean = heading("عالم أبسط", 40, CYAN, y=3.35)
        self.play(ReplacementTransform(heading_mess, heading_clean), run_time=1.0)
        self.wait(2.7)
        self.purge(beam_glow, sparks)

        # عالم تختفي فيه التعقيدات
        b.at(5)
        strikes = VGroup(*[Line(c[0].get_left() + LEFT * 0.1, c[0].get_right() + RIGHT * 0.1, stroke_color=RED,
                                stroke_width=4) for c in calls])
        self.play(LaggedStart(*[Create(s_) for s_ in strikes], lag_ratio=0.2), run_time=0.8)
        self.play(LaggedStart(*[FadeOut(VGroup(c, s_), shift=UP * 0.4) for c, s_ in zip(calls, strikes)],
                              lag_ratio=0.15), run_time=1.1)
        self.purge(calls, strikes, mess)

        # وتصبح القوانين الفيزيائية أكثر وضوحًا
        b.at(6)
        x = np.linspace(-7.1, 7.1, 220)
        y = np.linspace(-3.0, 2.3, 90)
        X, Y = np.meshgrid(x, y)
        rr2 = X ** 2 + (Y - cy) ** 2
        safe = np.maximum(rr2, 1e-9)
        V = np.where(rr2 <= R * R, 0.0, -X * (1 - R ** 3 / safe ** 1.5))
        heat = ScalarFieldImage(V, width=14.2, height=5.3, center=(0, (2.3 - 3.0) / 2, 0), vmax=4.5,
                                positive="#df8448", negative="#176b9b", zero="#02070a", opacity=0.55)
        heat.set_z_index(-3)
        masked = V.copy()
        masked[rr2 <= R * R] = np.nan
        contours = VGroup()
        for level in [-3.6, -2.6, -1.7, -0.9, 0.9, 1.7, 2.6, 3.6]:
            for path in contour_paths(X, Y, masked, level):
                contours.add(polyline(path, color=CYAN if level < 0 else ORANGE, stroke_width=1.4, smooth=False)
                             .set_stroke(opacity=0.7))
        self.play(FadeIn(heat), LaggedStart(*[Create(c) for c in contours], lag_ratio=0.03), run_time=1.4)
        laws = VGroup(eq(r"\nabla^2V=0", 46, WHITE).move_to([-4.9, 2.55, 0]),
                      eq(r"\mathbf{E}=-\nabla V", 46, GOLD).move_to([4.9, 2.55, 0]),
                      eq(r"V=\mathrm{const.}", 40, CYAN).move_to([0, cy, 0]))
        backs = VGroup(*[BackgroundRectangle(l, color=BACKGROUND, fill_opacity=0.75, buff=0.15) for l in laws[:2]])
        self.play(FadeIn(backs), Write(laws[0]), Write(laws[1]), run_time=1.0)
        tk.equation_impact(self, laws[0], color=CYAN, run_time=0.8)
        self.play(FadeIn(laws[2], scale=1.3), run_time=0.6)
        self.play(LaggedStart(*[ShowPassingFlash(seg.copy().set_stroke(ICE, 4), time_width=0.6) for seg in clean_lines],
                              lag_ratio=0.004), run_time=1.2)
        return dict(clean=clean, heat=heat, contours=contours, laws=VGroup(backs, laws), title=heading_clean,
                    grid=carry.get("grid") if carry else None)

    # =================================================================== 9
    def minis(self):
        """The four phenomena as small living diagrams (used by the montage and the finale)."""
        out = []
        # 1. charges spread over the surface
        c1 = Circle(radius=0.6, stroke_color=METAL, stroke_width=2.5, fill_color=DEEP, fill_opacity=1)
        p1 = Circle(radius=0.62).set_stroke(opacity=0)
        f1 = tk.FlowParticles(p1, count=16, radius=0.035, color=ICE)
        f1.add_updater(lambda m, dt: m.phase.increment_value(0.1 * dt))
        out.append(VGroup(c1, p1, f1))
        # 2. field lines bend around, none inside
        _, after = expelled_field_lines(0.5, np.linspace(-0.75, 0.75, 7), x_start=-1.5, n=50)
        lines = VGroup()
        for pts in after:
            for side in (1, -1):
                q = pts.copy()
                q[:, 0] *= side
                lines.add(VMobject(stroke_color=GOLD, stroke_width=1.6).set_points_as_corners(q))
        c2 = Circle(radius=0.5, stroke_color=CYAN, stroke_width=2.5, fill_color=DEEP, fill_opacity=1)
        e0 = eq(r"\mathbf{E}=0", 20, CYAN)
        out.append(VGroup(lines, c2, e0))
        # 3. induction without contact
        src = tk.ChargedParticle(charge=1, radius=0.13).move_to([-1.15, 0, 0])
        c3 = Circle(radius=0.55, stroke_color=METAL, stroke_width=2.5, fill_color=DEEP, fill_opacity=1).move_to([0.5, 0, 0])
        s3 = VGroup(*[num_text("−" if np.cos(a) < 0 else "+", 16, CYAN if np.cos(a) < 0 else RED)
                      .move_to([0.5, 0, 0] + 0.7 * np.array([np.cos(a), np.sin(a), 0]))
                      for a in np.linspace(0, TAU, 12, endpoint=False)])
        rings = VGroup(*[Arc(radius=r, start_angle=-0.6, angle=1.2, arc_center=[-1.15, 0, 0], stroke_color=RED,
                             stroke_width=1.5, stroke_opacity=0.5) for r in (0.35, 0.6, 0.85)])
        live_breathe(rings, 0.1, 0.7, freq=1.0, fill=False)
        out.append(VGroup(src, rings, c3, s3))
        # 4. total charge stays zero
        bal = eq_row((r"Q_{-}", CYAN, 30), ("+", WHITE, 28), (r"Q_{+}", RED, 30), ("=0", WHITE, 30))
        bars = VGroup(Rectangle(width=0.32, height=0.7, stroke_width=0, fill_color=CYAN, fill_opacity=0.8),
                      Rectangle(width=0.32, height=0.7, stroke_width=0, fill_color=RED, fill_opacity=0.8)
                      ).arrange(RIGHT, buff=0.3).next_to(bal, UP, buff=0.18)
        out.append(VGroup(bars, bal))
        return out

    def beat_09(self, b, carry):
        """وهنا تكمن أهمية الموصل المثالي! فمن خلال هذا النموذج البسيط، يمكننا فهم ظواهر كهربائية مذهلة..."""
        center = np.array([0, 0.0, 0])
        core = spinning_rim(metal_sphere(0.95, center))
        top = heading("أهمية الموصل المثالي", 40, CYAN, y=3.35)
        if carry:
            olds = [carry["heat"], carry["contours"], carry["laws"]]
            self.play(*[FadeOut(o) for o in olds], ReplacementTransform(carry["title"], top),
                      carry["clean"].animate.scale(0.6).move_to(center), run_time=1.0)
            self.play(FadeOut(carry["clean"]), FadeIn(core, scale=0.5), light_burst(center, CYAN, 28, 1.1, 3.4),
                      run_time=1.0)
            self.purge(*olds, carry["clean"])
        else:
            self.play(FadeIn(top), FadeIn(core), light_burst(center, CYAN, 28, 1.1, 3.4), run_time=2.0)
        halo = VGroup(*[Circle(radius=1.15 + 0.22 * i, stroke_color=CYAN, stroke_width=1.2,
                               stroke_opacity=0.25 / (i + 1)) for i in range(4)]).move_to(center)
        live_breathe(halo, 0.3, 1.0, freq=0.5, fill=False)
        self.play(FadeIn(halo), run_time=0.5)

        # فمن خلال هذا النموذج البسيط
        b.at(1)
        spots = [[4.5, 1.45, 0], [-4.5, 1.45, 0], [4.5, -2.05, 0], [-4.5, -2.05, 0]]  # right-to-left order
        captions = ["توزيع الشحنات على السطح", "انعدام المجال في الداخل", "الحث دون تلامس", "الشحنة الكلية صفر"]
        colors = [CYAN, GOLD, RED, VIOLET]
        cards = VGroup()
        links = VGroup()
        for spot, cap, col, mini in zip(spots, captions, colors, self.minis()):
            frame_ = card(3.9, 2.55, col).move_to(spot)
            mini.scale_to_fit_height(min(1.35, mini.height)).move_to(frame_.get_center() + UP * 0.25)
            if mini.width > 3.3:
                mini.scale_to_fit_width(3.3)
            lab = ar(cap, 22, WHITE, max_width=3.5).move_to(frame_.get_bottom() + UP * 0.33)
            cards.add(VGroup(frame_, mini, lab))
            d = normalize(np.array(spot) - center)
            links.add(tk.glowing_path(Line(center + 1.0 * d, frame_[1].get_center() - 1.25 * d * np.array([1.4, 0.9, 0])),
                                      color=col, width=1.5, passes=3, outer_opacity=0.08))
        for link, cd in zip(links, cards):
            self.play(Create(link), GrowFromPoint(cd, center), run_time=0.75)

        # يمكننا فهم ظواهر كهربائية مذهلة...
        b.at(2)
        for cd, col in zip(cards, colors):
            self.play(Circumscribe(cd[0][1], color=col, fade_out=True, buff=0.02), run_time=0.6)
        self.wait(max(0.0, b.remaining() - 1.45))
        self.play(self.camera.frame.animate.move_to(cards[0]).set(width=4.6), run_time=1.3,
                  rate_func=rate_functions.ease_in_cubic)
        return dict(all=VGroup(core, top, halo, cards, links), grid=carry.get("grid") if carry else None)

    # ================================================================== 10
    def beat_10(self, b, carry):
        """كيف تعيد الشحنات الكهربائية توزيع نفسها على سطح الموصل؟"""
        frame = self.camera.frame
        if carry:
            self.clear(carry["all"], run_time=0.35)
            frame.restore()
        head = heading("كيف تعيد الشحنات توزيع نفسها على سطح الموصل؟", 34, y=3.35)
        oc, S = np.array([-1.7, -0.35, 0]), 1.15
        th = np.linspace(0, TAU, 240)
        outline_pts = [oc + S * star_radius(t) * np.array([np.cos(t), np.sin(t), 0]) for t in th]
        shape = Polygon(*outline_pts, stroke_color=METAL, stroke_width=2.8, fill_color="#0a1b23", fill_opacity=0.95)
        ions = VGroup(*[Dot(oc + S * np.array([x, y, 0]), radius=0.022, color=METAL, fill_opacity=0.3)
                        for x in np.arange(-1.6, 2.4, 0.32) for y in np.arange(-1.4, 1.5, 0.32)
                        if np.hypot(x, y) < 0.9 * star_radius(np.arctan2(y, x))])
        frames = simulate_surface_migration(n=64, steps=240, seed=7)
        kf = tracker(self, 0.0)

        def pos_at(k):
            i = int(np.clip(np.floor(k), 0, len(frames) - 2))
            u = k - i
            return frames[i] * (1 - u) + frames[i + 1] * u
        electrons = VGroup(*[tk.ChargedParticle(charge=-1, radius=0.05, color=ICE, show_sign=False) for _ in range(64)])

        def place(group):
            P = pos_at(kf.get_value())
            for e, p in zip(group, P):
                e.move_to(oc + S * np.array([p[0], p[1], 0]))
        electrons.add_updater(place)
        place(electrons)
        trails = VGroup(*[TracedPath(e.get_center, stroke_color=CYAN, stroke_width=1.6, dissipating_time=0.7)
                          for e in electrons[:28]])

        def count(inside):
            P = pos_at(kf.get_value())
            ang = np.arctan2(P[:, 1], P[:, 0])
            on_surface = np.linalg.norm(P, axis=1) > 0.93 * star_radius(ang)
            return float(np.sum(~on_surface if inside else on_surface))
        panel = card(3.6, 2.7, CYAN).move_to([4.75, 0.15, 0])
        row_in = ar("داخل الموصل", 26, WHITE).move_to([5.6, 0.9, 0])
        row_out = ar("على السطح", 26, WHITE).move_to([5.6, 0.0, 0])
        n_in = LiveNumber(lambda: count(True), "{:.0f}", 40, ORANGE, align=ORIGIN, at=[3.7, 0.9, 0])
        n_out = LiveNumber(lambda: count(False), "{:.0f}", 40, CYAN, align=ORIGIN, at=[3.7, 0.0, 0])
        if carry:
            self.play(FadeIn(head[0], shift=DOWN * 0.1), Create(head[1]), FadeIn(shape, scale=1.15), FadeIn(ions),
                      run_time=0.9)
        else:
            self.play(FadeIn(head), FadeIn(shape), FadeIn(ions), run_time=0.9)
        self.add(electrons)  # the group carries the simulation updater
        self.play(LaggedStart(*[FadeIn(e, scale=0.3) for e in electrons], lag_ratio=0.01), FadeIn(panel),
                  FadeIn(row_in), FadeIn(row_out), FadeIn(n_in), FadeIn(n_out), run_time=0.7)
        self.add(trails)
        self.play(kf.animate.set_value(240), run_time=3.6, rate_func=rate_functions.ease_out_quad)
        # surface charge density from the final positions (Gaussian kernel along the surface)
        P = frames[-1]
        spikes = VGroup()
        angles = np.linspace(0, TAU, 80, endpoint=False)
        dens = []
        for a in angles:
            bp = star_radius(a) * np.array([np.cos(a), np.sin(a)])
            dens.append(np.exp(-np.sum((P - bp) ** 2, axis=1) / (2 * 0.16 ** 2)).sum())
        dens = np.array(dens) / max(dens)
        for a, d in zip(angles, dens):
            r0 = S * star_radius(a)
            n = np.array([np.cos(a), np.sin(a), 0])
            spikes.add(Line(oc + (r0 + 0.08) * n, oc + (r0 + 0.08 + 0.75 * d) * n, stroke_color=GOLD,
                            stroke_width=2.5, stroke_opacity=0.35 + 0.65 * d))
        sigma = eq(r"\sigma", 40, GOLD).move_to(oc + (S * star_radius(0) + 1.15) * RIGHT + UP * 0.35)
        rho0 = VGroup(eq(r"\rho=0", 38, CYAN), ar("في الداخل", 24, CYAN)).arrange(LEFT, buff=0.2).move_to([4.75, -0.85, 0])
        self.play(LaggedStart(*[Create(sp) for sp in spikes], lag_ratio=0.01), FadeIn(sigma), FadeIn(rho0),
                  run_time=1.0)
        return dict(shape=shape, ions=ions, electrons=electrons, trails=trails, spikes=spikes, sigma=sigma,
                    panel=VGroup(panel, row_in, row_out, n_in, n_out, rho0), head=head)

    # ================================================================== 11
    def beat_11(self, b, carry):
        """ولماذا ينعدم المجال الكهربائي داخل الموصل عند الاتزان الكهروستاتيكي؟"""
        c, R = np.array([0, -0.2, 0]), 1.55
        head = heading("لماذا ينعدم المجال داخل الموصل؟", 36, y=3.35)
        disk = Circle(radius=R, stroke_color=METAL, stroke_width=2.8, fill_color="#0a1b23", fill_opacity=0.95).move_to(c)
        if carry:
            self.play(Transform(carry["shape"], disk), FadeOut(carry["electrons"]), FadeOut(carry["trails"]),
                      FadeOut(carry["spikes"]), FadeOut(carry["sigma"]), FadeOut(carry["panel"]),
                      FadeOut(carry["ions"]), ReplacementTransform(carry["head"], head), run_time=1.0)
            self.purge(carry["electrons"], carry["trails"], carry["spikes"], carry["sigma"], carry["panel"], carry["ions"])
            disk = carry["shape"]
        else:
            self.play(FadeIn(disk), FadeIn(head), run_time=1.0)
        seeds = np.linspace(-1.95, 1.95, 9)
        before, after = expelled_field_lines(R, seeds, x_start=-6.9, n=80)
        lines_b, lines_a, flows = VGroup(), VGroup(), VGroup()
        for pb, pa in zip(before, after):
            for side in (1, -1):
                qb, qa = pb.copy(), pa.copy()
                if side < 0:
                    qb, qa = qb[::-1], qa[::-1]
                    qb[:, 0] *= -1
                    qa[:, 0] *= -1
                qb += c
                qa += c
                lb = VMobject(stroke_color=GOLD, stroke_width=2.2, stroke_opacity=0.85).set_points_as_corners(qb)
                la = VMobject(stroke_color=GOLD, stroke_width=2.2, stroke_opacity=0.85).set_points_as_corners(qa)
                lines_b.add(lb)
                lines_a.add(la)
                fp = tk.FlowParticles(lb, count=2, radius=0.03, color=GOLD, negative=False,
                                      phase_offset=0.5 * (side > 0))
                fp.add_updater(lambda m, dt: m.phase.increment_value(0.18 * dt))
                flows.add(fp)
        e0_lab = eq(r"\mathbf{E}_0", 36, GOLD).move_to([-6.2, 2.45, 0])
        self.play(LaggedStart(*[Create(l) for l in lines_b], lag_ratio=0.03), FadeIn(e0_lab), run_time=1.0)
        self.add(flows)
        s = tracker(self, 0.0)
        pts = [c + np.array([x, y, 0]) for x, y in [(-0.75, 0.55), (0.45, 0.55), (-0.75, -0.55), (0.45, -0.55), (-0.15, 0)]]
        ext_arrows = VGroup(*[Arrow(p + LEFT * 0.0, p + RIGHT * 0.6, buff=0, color=GOLD, stroke_width=4) for p in pts])
        ind_arrows = always_redraw(lambda: VGroup(*[
            Arrow(p + RIGHT * 0.6 + DOWN * 0.16, p + RIGHT * (0.6 - 0.6 * max(s.get_value(), 0.02)) + DOWN * 0.16,
                  buff=0, color=CYAN, stroke_width=4, max_tip_length_to_length_ratio=0.35) for p in pts]))
        signs = VGroup()
        for a in np.linspace(0, TAU, 30, endpoint=False):
            neg = np.cos(a) < 0
            sg = num_text("−" if neg else "+", 24, CYAN if neg else RED).move_to(c + (R + 0.2) * np.array([np.cos(a), np.sin(a), 0]))
            sg.base = 0.25 + 0.75 * abs(np.cos(a))
            signs.add(sg)
        signs.add_updater(lambda g: [m.set_opacity(m.base * s.get_value()) for m in g])
        self.play(LaggedStart(*[GrowArrow(a) for a in ext_arrows], lag_ratio=0.1), run_time=0.6)
        self.add(ind_arrows, signs)

        # inset: E_in = E0 + E_ind -> 0, live
        panel = RoundedRectangle(width=4.7, height=1.45, corner_radius=0.18, stroke_color=CYAN, stroke_width=1.5,
                                 fill_color="#050d13", fill_opacity=0.96).move_to([4.5, -3.1, 0])
        law = eq(r"\mathbf{E}_{\mathrm{in}}=\mathbf{E}_0+\mathbf{E}_{\mathrm{ind}}", 34, WHITE).move_to([4.5, -2.75, 0])
        mag = LiveNumber(lambda: 1 - s.get_value(), "|E_in| = {:.2f} E₀", 26, GOLD, align=ORIGIN, at=[4.5, -3.42, 0])
        self.play(FadeIn(panel), Write(law), FadeIn(mag), run_time=0.7)
        drive(self, s, 1.0, 3.0)
        self.play(*[Transform(lb, la) for lb, la in zip(lines_b, lines_a)], run_time=3.0)
        self.purge(ext_arrows, ind_arrows)
        zero_in = eq(r"\mathbf{E}=0", 54, CYAN).move_to(c)
        law0 = eq(r"\mathbf{E}_{\mathrm{in}}=0", 40, CYAN).move_to(law)
        self.play(FadeIn(zero_in, scale=1.4), TransformMatchingShapes(law, law0), run_time=0.6)
        tk.equation_impact(self, zero_in, color=CYAN, run_time=0.8)
        eq_chip = chip("الاتزان الكهروستاتيكي", GREEN).move_to([-4.6, -3.1, 0])
        self.play(FadeIn(eq_chip, shift=UP * 0.15), run_time=0.5)
        return dict(disk=disk, head=head, lines=lines_b, flows=flows, signs=signs, e0=e0_lab,
                    inset=VGroup(panel, law0, mag), zero=zero_in, chip=eq_chip, c=c, R=R)

    # ================================================================== 12
    def beat_12(self, b, carry):
        """وماذا يحدث عندما نقرّب جسمًا مشحونًا من موصل متعادل كهربائيًا... دون أن نلمسه حتى؟"""
        sc, R = np.array([2.7, -0.35, 0]), 1.55
        head = heading("ماذا يحدث عندما نقرّب جسمًا مشحونًا؟", 36, y=3.35)
        sphere = spinning_rim(metal_sphere(R, sc))
        e_in = eq(r"\mathbf{E}=0", 30, CYAN).move_to(sc + DOWN * 0.15).set_opacity(0.8)
        if carry:
            olds = [carry["lines"], carry["flows"], carry["signs"], carry["e0"], carry["inset"], carry["chip"]]
            self.play(*[FadeOut(o) for o in olds], ReplacementTransform(carry["head"], head),
                      carry["disk"].animate.move_to(sc), carry["zero"].animate.scale(0.55).move_to(e_in), run_time=0.9)
            self.play(FadeIn(sphere), FadeOut(carry["disk"]), FadeOut(carry["zero"]), FadeIn(e_in), run_time=0.5)
            self.purge(*olds, carry["disk"], carry["zero"])
        else:
            self.play(FadeIn(head), FadeIn(sphere), FadeIn(e_in), run_time=1.4)
        xs = tracker(self, -7.6)
        src = VGroup(glow(RED, 0.3, n=5, opacity=0.18), tk.ChargedParticle(charge=1, radius=0.24, color=RED))
        src.add_updater(lambda m: m.move_to([xs.get_value(), sc[1], 0]))
        model_at = lambda x: tk.NeutralConductingSphere(center=tuple(sc), radius=R,
                                                        external_position=(x, sc[1], 0.0), external_charge=1.0)
        angles = np.linspace(0, TAU, 30, endpoint=False)
        normals = [np.array([np.cos(a), np.sin(a), 0]) for a in angles]
        closest = model_at(sc[0] - R - 1.05)
        kmax = max(abs(closest.surface_induced_charge_density(sc + R * n)) for n in normals)
        minus = VGroup(*[num_text("−", 26, CYAN).move_to(sc + (R + 0.2) * n) for n in normals])
        plus = VGroup(*[num_text("+", 26, RED).move_to(sc + (R + 0.2) * n) for n in normals])
        pairs = VGroup(*[VGroup(num_text("+", 16, RED), num_text("−", 16, CYAN)).arrange(RIGHT, buff=0.02)
                         .move_to(sc + (R + 0.2) * n) for n in normals[::2]])

        def polarize(group):
            model = model_at(xs.get_value())
            dens = np.array([model.surface_induced_charge_density(sc + R * n) for n in normals]) / kmax
            strength = float(np.clip(np.abs(dens).max() * 1.3, 0, 1))
            for m, p, d in zip(minus, plus, dens):
                m.set_opacity(float(np.clip(-d * 1.4, 0, 1)))
                p.set_opacity(float(np.clip(d * 4.0, 0, 1)))
            pairs.set_opacity(1 - strength)
        polar = VGroup(minus, plus, pairs)
        polar.add_updater(polarize)
        self.add(src, polar)
        self.play(FadeIn(pairs), run_time=0.3)
        rings = influence_rings(src, color=RED, period=0.6, speed=2.6, max_r=8.5)
        self.add(rings)
        drive(self, xs, sc[0] - R - 1.05, 5.0, rate=rate_functions.ease_in_out_sine)
        self.wait(5.1)

        # دون أن نلمسه حتى؟
        b.at(1)
        gap = always_redraw(lambda: DoubleArrow([xs.get_value() + 0.3, sc[1] - 0.9, 0], [sc[0] - R - 0.05, sc[1] - 0.9, 0],
                                                buff=0, color=WHITE, stroke_width=2, tip_length=0.15))
        no_touch = chip("دون تلامس", WHITE).move_to([sc[0] - R - 0.55, sc[1] - 1.6, 0])
        model = model_at(sc[0] - R - 1.05)
        seeds = [[sc[0] - R - 1.05 + 0.32 * np.cos(a), sc[1] + 0.32 * np.sin(a), 0] for a in np.linspace(0.3, TAU - 0.3, 12)]
        lines = tk.FieldLineBundle(model.field, seeds, color=GOLD, line_width=1.6, step=0.05, max_steps=260,
                                   bounds=(-7.0, 7.0, -3.3, 3.0))
        self.play(GrowFromCenter(gap), FadeIn(no_touch, shift=UP * 0.1),
                  LaggedStart(*[Create(l) for l in lines.curves], lag_ratio=0.06), FadeIn(lines.arrows), run_time=1.3)
        return dict(head=head, sphere=sphere, e_in=e_in, src=src, xs=xs, rings=rings, polar=polar, gap=gap,
                    no_touch=no_touch, lines=lines, sc=sc, R=R, model_at=model_at)

    # ================================================================== 13
    def beat_13(self, b, carry):
        """والأكثر إثارة... كيف يمكن أن يتغير توزيع الشحنات داخل الموصل، بينما تبقى شحنته الكلية صفرًا؟"""
        if not carry:
            carry = self.beat_12_stage()
        sc, R, xs, model_at = carry["sc"], carry["R"], carry["xs"], carry["model_at"]
        head = heading("يتغير التوزيع... والشحنة الكلية صفر", 36, y=3.35)
        self.play(FadeOut(carry["lines"]), FadeOut(carry["gap"]), FadeOut(carry["no_touch"]),
                  ReplacementTransform(carry["head"], head), run_time=0.8)
        self.purge(carry["lines"], carry["gap"], carry["no_touch"])
        thetas = np.linspace(0, PI, 120)

        def band_charge(x):
            """dQ/dθ on the sphere: σ(θ)·2πR²·sinθ, θ measured from the side facing the charge."""
            model = model_at(x)
            sig = np.array([model.surface_induced_charge_density(sc + R * np.array([-np.cos(t), np.sin(t), 0]))
                            for t in thetas])
            return sig * 2 * PI * R ** 2 * np.sin(thetas)
        ref = band_charge(sc[0] - R - 0.75)
        fmax = np.abs(ref).max()
        qmax = _trapz(np.clip(ref, 0, None), thetas)
        axes = Axes(x_range=[0, PI, PI / 2], y_range=[-1.1, 1.1, 0.5], x_length=5.6, y_length=2.3, tips=False,
                    axis_config={"stroke_opacity": 0.6, "include_ticks": False}).move_to([-3.75, -2.5, 0])
        th_lab = eq(r"\theta", 32, METAL).next_to(axes.x_axis.get_end(), RIGHT, buff=0.1)
        f_lab = eq(r"\frac{dQ}{d\theta}", 30, METAL).next_to(axes.y_axis.get_end(), LEFT, buff=0.1)
        cache = {}

        def current():
            x = round(xs.get_value(), 4)
            if x not in cache:
                cache.clear()
                cache[x] = band_charge(x)
            return cache[x]

        def graph():
            f = current() / fmax
            pts = [axes.c2p(t, v) for t, v in zip(thetas, f)]
            curve = VMobject(stroke_color=WHITE, stroke_width=3).set_points_as_corners(pts)
            pos = [axes.c2p(t, max(v, 0)) for t, v in zip(thetas, f)]
            neg = [axes.c2p(t, min(v, 0)) for t, v in zip(thetas, f)]
            base = [axes.c2p(thetas[-1], 0), axes.c2p(thetas[0], 0)]
            fill_p = VMobject(stroke_width=0, fill_color=RED, fill_opacity=0.45).set_points_as_corners(pos + base + [pos[0]])
            fill_n = VMobject(stroke_width=0, fill_color=CYAN, fill_opacity=0.45).set_points_as_corners(neg + base + [neg[0]])
            return VGroup(fill_p, fill_n, curve)
        plot = always_redraw(graph)
        q_neg = lambda: _trapz(np.clip(current(), None, 0), thetas) / qmax
        q_pos = lambda: _trapz(np.clip(current(), 0, None), thetas) / qmax
        q_tot = lambda: (lambda v: 0.0 if abs(v) < 0.005 else v)(q_neg() + q_pos())
        rows = VGroup(
            VGroup(eq(r"Q_{-}=", 38, CYAN), LiveNumber(q_neg, "{:+.2f}", 34, CYAN, align=LEFT)),
            VGroup(eq(r"Q_{+}=", 38, RED), LiveNumber(q_pos, "{:+.2f}", 34, RED, align=LEFT)),
            VGroup(eq(r"Q_{\mathrm{tot}}=", 38, WHITE), LiveNumber(q_tot, "{:.2f}", 34, WHITE, align=LEFT)),
        )
        for k, row in enumerate(rows):
            row[0].move_to([-5.2, 2.35 - 0.78 * k, 0], aligned_edge=RIGHT).shift(RIGHT * 0.6)
            row[1].place(row[0].get_right() + RIGHT * 0.15)
        tot_box = SurroundingRectangle(rows[2], buff=0.15, corner_radius=0.1, stroke_color=GOLD, stroke_width=2)
        self.play(Create(axes), FadeIn(th_lab), FadeIn(f_lab), FadeIn(plot), LaggedStart(*[FadeIn(r) for r in rows]),
                  run_time=1.2)

        # كيف يمكن أن يتغير توزيع الشحنات داخل الموصل
        b.at(1)
        far, near = sc[0] - R - 2.2, sc[0] - R - 0.75
        drive(self, xs, far, 1.9, rate=rate_functions.ease_in_out_sine)
        drive(self, xs, near, 2.2, rate=rate_functions.ease_in_out_sine, delay=2.0, start=far)
        self.play(Create(tot_box), run_time=0.6)
        self.wait(1.4)
        self.play(Indicate(rows[2], color=GOLD, scale_factor=1.08), run_time=0.8)

        # بينما تبقى شحنته الكلية صفرًا؟
        b.at(2)
        total = eq(r"\oint_S \sigma\,dA=0", 46, GOLD).move_to([-4.2, -0.6, 0])
        zero_chip = chip("الشحنة الكلية تبقى صفرًا", GOLD).next_to(tot_box, RIGHT, buff=0.3)
        self.play(Write(total), FadeIn(zero_chip, shift=UP * 0.1), run_time=0.9)
        tk.equation_impact(self, total, color=GOLD, run_time=0.9)
        drive(self, xs, sc[0] - R - 1.6, 1.4, rate=rate_functions.ease_in_out_sine, delay=0.1)
        return dict(all=VGroup(head, axes, th_lab, f_lab, plot, rows, tot_box, total, zero_chip, carry["sphere"],
                               carry["e_in"], carry["src"], carry["rings"], carry["polar"]))

    def beat_12_stage(self):
        """Minimal induction stage so beat 13 can be previewed on its own."""
        sc, R = np.array([2.7, -0.35, 0]), 1.55
        sphere = metal_sphere(R, sc)
        xs = tracker(self, sc[0] - R - 1.05)
        src = tk.ChargedParticle(charge=1, radius=0.24).move_to([xs.get_value(), sc[1], 0])
        src.add_updater(lambda m: m.move_to([xs.get_value(), sc[1], 0]))
        model_at = lambda x: tk.NeutralConductingSphere(center=tuple(sc), radius=R, external_position=(x, sc[1], 0.0))
        self.add(sphere, src)
        return dict(sc=sc, R=R, xs=xs, model_at=model_at, sphere=sphere, src=src, e_in=VGroup(), rings=VGroup(),
                    polar=VGroup(), lines=VGroup(), gap=VGroup(), no_touch=VGroup(), head=heading(" ", 36))

    # ================================================================== 14
    def beat_14(self, b, carry):
        """كل هذه الأسئلة تقودنا إلى واحدة من أجمل الأفكار في الفيزياء... أحيانًا، تكون أفضل طريقة لفهم العالم
        الحقيقي... هي أن نبدأ بتخيّل عالم مثالي. وهذا بالضبط ما سنفعله في هذا الفيديو..."""
        frame = self.camera.frame
        if carry:
            self.clear(carry["all"], run_time=0.8)
        idea = heading("واحدة من أجمل الأفكار في الفيزياء", 38, GOLD, y=3.35, accent=GOLD)
        minis = self.minis()
        cards = VGroup()
        for mini, col in zip(minis, [CYAN, GOLD, RED, VIOLET]):
            fr = card(2.9, 1.9, col)
            mini.scale_to_fit_height(min(1.3, mini.height))
            if mini.width > 2.5:
                mini.scale_to_fit_width(2.5)
            cards.add(VGroup(fr, mini.move_to(fr)))
        spin = tracker(self, 0.0)
        rad = tracker(self, 1.0)
        spin.add_updater(lambda m, dt: m.increment_value(0.35 * dt))

        def orbit(group):
            for k, cd in enumerate(group):
                a = spin.get_value() + TAU * k / 4 + PI / 4
                r = rad.get_value()
                cd.move_to([4.4 * r * np.cos(a), -0.15 + 2.0 * r * np.sin(a), 0])
        cards.add_updater(orbit)
        orbit(cards)
        self.add(cards)
        self.play(FadeIn(idea[0], shift=DOWN * 0.1), Create(idea[1]),
                  LaggedStart(*[GrowFromCenter(cd) for cd in cards], lag_ratio=0.2), run_time=1.6)
        self.wait(1.5)
        drive(self, rad, 0.0, 1.6, rate=rate_functions.ease_in_cubic)
        self.play(*[cd.animate.scale(0.05) for cd in cards], run_time=1.6, rate_func=rate_functions.ease_in_cubic)
        self.purge(cards)
        star = VGroup(Circle(radius=0.55, stroke_width=0, fill_color=ICE, fill_opacity=0.12),
                      glow(WHITE, 0.2, n=6, opacity=0.3)).move_to([0, -0.15, 0])
        live_breathe(star[0], 0.05, 0.22, freq=1.2, stroke=False)
        shock = Circle(radius=0.2, stroke_color=ICE, stroke_width=6).move_to(star)
        self.play(FadeIn(star, scale=0.2), Flash(star.get_center(), color=ICE, num_lines=20, flash_radius=1.2,
                                                 line_length=0.6), run_time=0.6)
        self.play(shock.animate.scale(30).set_stroke(width=0.5, opacity=0), run_time=0.9)
        self.purge(shock)

        # أحيانًا، تكون أفضل طريقة لفهم العالم الحقيقي...
        b.at(1)
        divider = tk.glowing_path(Line([0, -3.7, 0], [0, 2.5, 0]), color=METAL, width=1.2, passes=3, outer_opacity=0.06)
        real_t = ar("العالم الحقيقي", 34, ORANGE).move_to([-3.6, 2.45, 0])
        ideal_t = ar("العالم المثالي", 34, CYAN).move_to([3.6, 2.45, 0])
        lattice = tk.CrystalLattice(rows=7, cols=11, spacing=0.5, stagger=True, bond_opacity=0.15, ion_radius=0.06,
                                    color=ORANGE).move_to([-3.6, -0.5, 0])
        base = [ion.get_center().copy() for ion in lattice.ions]
        rng = np.random.default_rng(4)
        ph = rng.uniform(0, TAU, (len(base), 2))
        lit = tracker(self, 0.0)

        def jiggle(group):
            t = now()
            amp = 0.07 * (1 - 0.6 * lit.get_value())
            col = interpolate_color(ManimColor(ORANGE), ManimColor(ICE), lit.get_value())
            for ion, p, (a1, a2) in zip(group, base, ph):
                ion.move_to(p + amp * np.array([np.sin(7 * t + a1), np.cos(8 * t + a2), 0]))
                ion[1].set_fill(col)
        lattice.ions.add_updater(jiggle)
        wander = VGroup(*[glow(ICE, 0.04, n=2, opacity=0.2) for _ in range(14)])
        w_pos = [np.array([rng.uniform(-6.2, -1.0), rng.uniform(-2.0, 1.0)]) for _ in wander]
        w_vel = [rng.normal(0, 1.4, 2) for _ in wander]

        def wander_upd(group, dt):
            for k, e in enumerate(group):
                if rng.random() < 0.07:
                    w_vel[k] = rng.normal(0, 1.4, 2) * (1 - 0.5 * lit.get_value())
                w_pos[k] = np.clip(w_pos[k] + w_vel[k] * dt, [-6.3, -2.1], [-0.9, 1.1])
                e.move_to([*w_pos[k], 0])
        wander.add_updater(wander_upd)
        sc = np.array([3.6, -0.5, 0])
        self.add(wander)
        self.play(Create(divider), FadeIn(real_t, shift=DOWN * 0.1), FadeIn(ideal_t, shift=DOWN * 0.1),
                  FadeIn(lattice), star.animate.move_to(sc), run_time=1.3)
        sphere = spinning_rim(metal_sphere(1.25, sc))
        self.play(FadeIn(sphere, scale=0.3), FadeOut(star), run_time=0.8)
        self.purge(star)
        laws = VGroup(eq(r"R=0", 32, CYAN), eq(r"\mathbf{E}=0", 32, GOLD), eq(r"\rho=0", 32, GOLD),
                      eq(r"V=\mathrm{const.}", 30, CYAN))
        ang = tracker(self, 0.0)
        ang.add_updater(lambda m, dt: m.increment_value(0.4 * dt))

        def orbit_laws(group):
            for k, lw in enumerate(group):
                a = ang.get_value() + TAU * k / 4
                lw.move_to(sc + np.array([2.25 * np.cos(a), 1.55 * np.sin(a), 0]))
        laws.add_updater(orbit_laws)
        orbit_laws(laws)
        self.add(laws)
        self.play(LaggedStart(*[FadeIn(lw, scale=0.5) for lw in laws], lag_ratio=0.2), run_time=1.2)

        # هي أن نبدأ بتخيّل عالم مثالي — light travels from the ideal model to the real world
        b.at(3)
        arc = ArcBetweenPoints(sc + UP * 1.3 + LEFT * 0.6, np.array([-3.4, 1.15, 0]), angle=0.75)
        bridge = tk.glowing_path(arc, color=CYAN, width=2.0, passes=4, outer_opacity=0.08)
        carriers = tk.FlowParticles(arc, count=10, radius=0.05, color=ICE)
        carriers.add_updater(lambda m, dt: m.phase.increment_value(0.35 * dt))
        self.play(Create(bridge), run_time=0.9)
        self.add(carriers)
        drive(self, lit, 1.0, 2.2)
        self.wait(2.0)

        # وهذا بالضبط ما سنفعله في هذا الفيديو...
        b.at(4)
        stage = VGroup(divider, real_t, ideal_t, lattice, sphere, laws, bridge, carriers, idea, wander)
        if getattr(self, "grid", None) is not None and self.grid in self.mobjects:
            stage.add(self.grid)
        self.clear(stage, run_time=0.9)
        title = ar("الموصلات المثالية", 72, WHITE).move_to([0, 0.45, 0])
        halo = glow_text(title, CYAN, layers=4, opacity=0.22)
        sub = ar("لفهم العالم الحقيقي، نبدأ بعالمٍ مثالي", 32, CYAN).move_to([0, -0.85, 0])
        rule = Line([-3.8, -0.25, 0], [3.8, -0.25, 0], stroke_color=GOLD, stroke_width=1.5)
        self.play(rtl_reveal(title, run_time=1.2), light_burst(title.get_center(), CYAN, 30, 1.5, 4.5), run_time=1.2)
        self.play(FadeIn(halo), Create(rule), FadeIn(sub, shift=UP * 0.12), run_time=0.9)
        self.play(frame.animate.scale(0.93), run_time=max(0.5, b.remaining() - 1.3), rate_func=linear)
        drive(self, self.dust.level, 0.0, 1.0)
        self.play(FadeOut(VGroup(title, halo, sub, rule)), run_time=1.0)
        return None


if __name__ == "__main__":
    # PyCharm Run button: quality and preview come from settings.py
    # (set QUALITY = "high_quality" there for the final 1080p60 render).
    from settings import render

    render(IdealConductorHook, "scene_00_intro_hook")
