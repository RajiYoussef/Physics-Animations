import numpy as np
from manim import *
from settings import BACKGROUND, CYAN, GOLD, WHITE, render
from support import ar, caption_panel
from tools import field_arrows


class ConductorOpening(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        heading = ar("الموصلات الكهربائية", size=37).move_to([0, 3.45, 0])
        box, first = caption_panel("تحتوي الموصلات على شحنات كهربائية تستطيع الحركة داخل المادة.")
        _, second = caption_panel("في الفلزات، تستطيع بعض الإلكترونات الحركة بين الأيونات الموجبة.")
        _, third = caption_panel("تتوزع إلكترونات التوصيل بين الأيونات داخل البلورة الفلزية.")
        _, fourth = caption_panel("عند تطبيق مجال كهربائي، تتحرك الإلكترونات عكس اتجاه المجال.")
        self.add(heading, box)

        # A copper wire gives the microscopic view a recognizable starting point.
        wire = VGroup(
            RoundedRectangle(width=8.4, height=1.6, corner_radius=.7, stroke_color=GOLD,
                             fill_color="#a95725", fill_opacity=.9, stroke_width=2.5),
            *[Line([-3.8, y, 0], [3.8, y, 0], color=c, stroke_width=3, stroke_opacity=.5)
              for y, c in [(-.48, "#7c351b"), (-.20, "#cf834a"), (.13, "#ffd493"), (.46, "#e69c58")]],
        ).move_to([0, .25, 0])
        wire_title = ar("سلك فلزي", size=28, color=GOLD).next_to(wire, UP, buff=.3)
        sweep = Line([-3.7, .3, 0], [3.7, .3, 0], color=WHITE, stroke_width=5)
        self.play(FadeIn(wire, scale=.8), FadeIn(wire_title), FadeIn(first), run_time=1.6)
        self.play(ShowPassingFlash(sweep, time_width=.25), run_time=2)

        # Enlarge an atom, then reveal electrons able to travel through the metal.
        atom_centre = np.array([-3.1, .35, 0])
        nucleus = VGroup(Circle(radius=.32, stroke_color=GOLD, fill_color="#c67836", fill_opacity=.8),
                         Text("+", font="Arial", font_size=32, color=WHITE)).move_to(atom_centre)
        shells = VGroup(Circle(radius=.78, color="#536f80", stroke_width=1.5),
                        Circle(radius=1.3, color="#538a9f", stroke_width=1.5)).move_to(atom_centre)
        atom_electrons = VGroup(*[Dot(atom_centre + np.array([1.3*np.cos(a), 1.3*np.sin(a), 0]), radius=.07, color=CYAN)
                                   for a in [0, TAU/3, 2*TAU/3]])
        atom_caption = ar("إلكترونات الأغلفة الخارجية", size=26, color=CYAN).move_to([2.5, 1.2, 0])
        pointer = Arrow([1.0, .85, 0], [-1.75, .6, 0], buff=.1, color=CYAN, stroke_width=2)
        self.play(FadeOut(wire), FadeOut(wire_title), FadeOut(first), FadeIn(second),
                  GrowFromCenter(nucleus), Create(shells), FadeIn(atom_electrons),
                  FadeIn(atom_caption), GrowArrow(pointer), run_time=2.2)
        self.play(Rotate(atom_electrons, angle=PI/2, about_point=atom_centre), run_time=3, rate_func=linear)
        moving = atom_electrons[0].copy()
        trail = TracedPath(moving.get_center, stroke_color=CYAN, stroke_width=2.5, dissipating_time=1.3)
        path = CubicBezier(moving.get_center(), [-.6, 1.7, 0], [1.0, -1.4, 0], [3.5, .25, 0])
        self.add(trail, moving)
        self.play(MoveAlongPath(moving, path), FadeOut(atom_caption), FadeOut(pointer), run_time=3.5)

        # Build the extended metal around the same moving electron.
        ions = VGroup()
        for row, y in enumerate(np.linspace(-1.7, 1.65, 4)):
            for x in np.linspace(-5.0, 5.0, 8):
                p = np.array([x + (row % 2)*.25, y, 0])
                halo = Circle(radius=.34, stroke_width=0, fill_color=GOLD, fill_opacity=.08)
                core = Circle(radius=.14, stroke_color=GOLD, fill_color="#9b5428", fill_opacity=.9, stroke_width=1.5)
                plus = Text("+", font="Arial", font_size=19, color=WHITE)
                ions.add(VGroup(halo, core, plus).move_to(p))
        time = ValueTracker(0)
        drift = ValueTracker(0)
        rng = np.random.default_rng(14)
        electrons = VGroup()
        for _ in range(34):
            x, y, phase = rng.uniform(-4.85, 4.85), rng.uniform(-1.6, 1.6), rng.uniform(0, TAU)
            dot = VGroup(Circle(radius=.13, stroke_width=0, fill_color=CYAN, fill_opacity=.12),
                         Dot(radius=.055, color=CYAN))
            def move(m, x=x, y=y, phase=phase):
                t = time.get_value()
                m.move_to([x + .24*np.sin(.8*t+phase) - drift.get_value(),
                           y + .16*np.cos(.7*t+phase*1.3), 0])
            dot.add_updater(move)
            electrons.add(dot)
        self.play(FadeOut(nucleus), FadeOut(shells), FadeOut(atom_electrons), FadeOut(moving),
                  FadeOut(trail), FadeOut(second), FadeIn(third),
                  LaggedStart(*[FadeIn(ion, scale=.5) for ion in ions], lag_ratio=.025),
                  FadeIn(electrons), run_time=2.6)
        self.play(time.animate.set_value(5), run_time=5, rate_func=linear)
        ion_label = ar("أيونات موجبة", size=25, color=GOLD).move_to([4.5, 2.45, 0])
        electron_label = ar("إلكترونات التوصيل", size=25, color=CYAN).move_to([-4.0, 2.45, 0])
        self.play(FadeIn(ion_label), FadeIn(electron_label), time.animate.set_value(7), run_time=2)
        self.play(time.animate.set_value(10), run_time=3, rate_func=linear)

        # An applied field produces an opposite net electron displacement.
        field = field_arrows(np.array([[x, 2.12] for x in np.linspace(-4.8, 4.8, 7)]),
                             np.tile([1.0, 0.0], (7, 1)), max_length=1.3, color=CYAN)
        field_label = ar("اتجاه المجال الكهربائي", size=23, color=CYAN).move_to([0, 2.72, 0])
        self.play(FadeOut(ion_label), FadeOut(electron_label), FadeOut(third), FadeIn(fourth),
                  LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=.1), FadeIn(field_label), run_time=2)
        self.play(drift.animate.set_value(.8), run_time=6, rate_func=linear)
        self.wait(.5)


if __name__ == "__main__":
    render(ConductorOpening, filename="scene_01_conductor", preview=True)
