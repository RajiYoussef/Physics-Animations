
from explainer_tools import *

def fix_axis_labels(axes, labels, x_ticks, y_ticks, x_name, y_name):
    labels.set_opacity(0)
    result = VGroup()
    for x, value in x_ticks:
        result.add(formula(value, 20).next_to(axes.c2p(x, 0), DOWN, buff=.12))
    for y, value in y_ticks:
        if y != 0:
            result.add(formula(value, 20).next_to(axes.c2p(0, y), LEFT, buff=.14))
    result.add(formula(x_name, 25, CYAN).next_to(axes.x_axis.get_end(), RIGHT, buff=.12))
    result.add(formula(y_name, 23).next_to(axes.y_axis.get_end(), UP, buff=.12))
    return result


class InteriorLoss(Explainer):
    chapter = 4

    def construct(self):
        with self.beat(0):
            self.heading('ماذا يعني أن تحقق الدالة معادلة لابلاس؟')
            self.reveal(formula(r'V(x,y)=x^2-y^2', 34).move_to([0, 2.5, 0]))

            xt = [(-1, '-1'), (0, '0'), (1, '1')]
            yt = [(-2, '-2'), (0, '0'), (2, '2')]
            a, l = graph([-1.5, 1.5, 1], [-2.5, 2.5, 1], 4.8, 3, [-3.5, 0, 0], 'x', 'V(x,0)', xt, yt)
            b, bl = graph([-1.5, 1.5, 1], [-2.5, 2.5, 1], 4.8, 3, [3.5, 0, 0], 'y', 'V(0,y)', xt, yt)

            la = fix_axis_labels(a, l, xt, yt, 'x', 'V(x,0)')
            lb = fix_axis_labels(b, bl, xt, yt, 'y', 'V(0,y)')
            self.add(a, b, la, lb)

            xs = np.linspace(-1.5, 1.5, 100)
            self.play(Create(sampled(a, xs, xs**2, CYAN)), Create(sampled(b, xs, -xs**2, PURPLE)), run_time=2)

            t = ValueTracker(-1)
            tangents = always_redraw(lambda: VGroup(
                TangentLine(a, lambda x: x*x, t.get_value(), derivative=lambda x: 2*x, span=.65, color=AMBER),
                TangentLine(b, lambda y: -y*y, t.get_value(), derivative=lambda y: -2*y, span=.65, color=AMBER)
            ))
            self.add(tangents)
            self.cue('الانحناء موجب في اتجاه "x"،'
                     ' وسالب بالمقدار نفسه في اتجاه "y"')
            self.play(t.animate.set_value(1), run_time=5)

            ex = formula('V_{xx}=2', 31, CYAN).move_to([-3.5, -2.3, 0])
            ey = formula('V_{yy}=-2', 31, PURPLE).move_to([3.5, -2.3, 0])
            self.reveal(ex, ey)

            total = formula('2+(-2)=0', 32, WHITE).move_to([0, -2.4, 0])
            self.play(TransformFromCopy(VGroup(ex, ey), total), run_time=1.5)
            self.cue('يتمثل الشرط في أن يكون مجموع الانحناءين مساويًا للصفر، وليس في أن يكون كل منهما على حدة')
            self.wait(2)
            self.code_flash('derivatives', 2)

        self.reset()
        with self.beat(1):
            self.heading('نختبر مخرجات الشبكة عند نقاط فعلية.')
            a, l = domain()
            self.add(a, l)

            p = self.data['weights'][0]
            pts = self.data['points'][:1000]
            values = derivatives(p, pts[:, 0], pts[:, 1])
            res = values[0] + values[1]

            dots = VGroup(*[
                Dot(a.c2p(x, y), radius=.045, color=CYAN if r >= 0 else PURPLE)
                for (x, y), r in zip(pts, res)
            ])
            self.play(LaggedStart(*[FadeIn(q) for q in dots], lag_ratio=.04), run_time=2)
            self.cue('.')

            info = None
            for k in [0, 4, 12, 20]:
                x, y = pts[k]
                rx, ry = float(values[0][k]), float(values[1][k])
                new = VGroup(
                    formula(f'(x,y)=({x:.2f},{y:.2f})', 24),
                    formula(f'V_{{xx}}={rx:.3f}', 27, CYAN),
                    formula(f'V_{{yy}}={ry:.3f}', 27, PURPLE),
                    formula(f'R={rx+ry:.3f}', 30, AMBER)
                ).arrange(DOWN, buff=.3).move_to([3.4, 0, 0])

                self.play(Indicate(dots[k], scale_factor=2, color=AMBER), run_time=.7)
                if info is None:
                    self.reveal(new)
                else:
                    self.play(ReplacementTransform(info, new), run_time=.6)
                info = new
                self.wait(1)

            self.reveal(ar('نستخدم هنا 1000 نقطة', 23, width=10).move_to([0, -2.8, 0]))
            self.wait(1)

        self.reset()
        with self.beat(2):
            self.heading('كيف نحول هذه الأخطاء إلى عدد واحد؟')

            xt = [(1, '1'), (2, '2')]
            yt = [(-1, '-1'), (0, '0'), (1, '1')]
            a, l = graph([0, 3, 1], [-2, 2, 1], 6, 3, [0, .2, 0], 'k', 'R_k', xt, yt)
            labels = fix_axis_labels(a, l, xt, yt, 'k', 'R_k')
            self.add(a, labels)

            bars = VGroup(
                Line(a.c2p(1, 0), a.c2p(1, 1), color=CYAN, stroke_width=18),
                Line(a.c2p(2, 0), a.c2p(2, -1), color=PURPLE, stroke_width=18)
            )
            self.play(Create(bars), run_time=1.5)

            equation = formula('1+(-1)=0', 32, AMBER).move_to([0, 2.5, 0])
            self.reveal(equation)
            self.cue('مثال بسيط: يؤدي جمع الخطأين إلى إخفائهما، على الرغم من أن كلاً منهما لا يساوي صفً.')
            self.wait(2)

            self.play(Transform(bars[1], Line(a.c2p(2, 0), a.c2p(2, 1), color=PURPLE, stroke_width=18)), run_time=2)
            equation = self.change(equation, formula(r'\frac{1^2+(-1)^2}{2}=1', 35, AMBER))
            self.cue('نقوم بتربيع كل قيمة، ثم نحسب المتوسط.')
            self.reveal(formula(r'\mathcal{L}_{PDE}=\frac{1}{N}\sum_{k=1}^{N}R_k^2', 32).move_to([0, -2.5, 0]))
            self.wait(2)
            self.code_flash('points', 2)


if __name__ == '__main__':
    run_independent(InteriorLoss)
