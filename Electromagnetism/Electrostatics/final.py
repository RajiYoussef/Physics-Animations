from manim import *
import numpy as np


# ============================================================
# Scene 23
# المجال المنتظم والقوة على شحنة
# ============================================================


class Scene23UniformFieldAndForce(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

        FIELD_COLOR = "#7EE787"
        FORCE_COLOR = "#FFD166"

        # لون الاسم في النهاية
        NAME_COLOR = "#7EE787"

        def arabic_text(
            text,
            size=38,
            weight=NORMAL,
            color=TEXT_MAIN
        ):
            return Text(
                text,
                font=arabic_font,
                font_size=size,
                weight=weight,
                color=color
            )

        # ====================================================
        # HELPERS
        # ====================================================

        def make_plate(
            x_position,
            plate_color
        ):

            plate = RoundedRectangle(
                width=0.28,
                height=4.8,
                corner_radius=0.08,
                stroke_width=3,
                stroke_color=plate_color,
                fill_color=plate_color,
                fill_opacity=0.18
            )

            plate.move_to(
                np.array([
                    x_position,
                    -0.15,
                    0
                ])
            )

            return plate

        def make_plate_signs(
            x_position,
            sign,
            color
        ):

            signs = VGroup()

            y_values = np.linspace(
                -2.0,
                1.7,
                7
            )

            for y in y_values:

                symbol = Text(
                    sign,
                    font=arabic_font,
                    font_size=28,
                    weight=BOLD,
                    color=color
                ).move_to(
                    np.array([
                        x_position,
                        y,
                        0
                    ])
                )

                signs.add(symbol)

            return signs

        def make_uniform_field():

            arrows = VGroup()

            # نترك المنتصف فارغًا قليلًا
            # حتى تكون شحنة الاختبار وسهم القوة واضحين.
            y_values = [
                -1.80,
                -1.20,
                -0.60,
                0.60,
                1.20,
                1.80
            ]

            for y in y_values:

                arrow = Arrow(
                    start=np.array([
                        -3.45,
                        y,
                        0
                    ]),
                    end=np.array([
                        3.45,
                        y,
                        0
                    ]),
                    buff=0,
                    stroke_width=4,
                    color=FIELD_COLOR,
                    max_tip_length_to_length_ratio=0.035
                )

                arrows.add(arrow)

            return arrows

        def make_test_charge(
            sign="+",
            radius=0.32
        ):

            color = (
                POSITIVE
                if sign == "+"
                else NEGATIVE
            )

            circle = Circle(
                radius=radius,
                stroke_width=3,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.16
            )

            symbol = Text(
                sign,
                font=arabic_font,
                font_size=31,
                weight=BOLD,
                color=color
            ).move_to(circle)

            return VGroup(
                circle,
                symbol
            )

        def make_positive_force_arrow(length):

            start = np.array([
                0.40,
                0.0,
                0.0
            ])

            return Arrow(
                start=start,
                end=start + RIGHT * length,
                buff=0,
                stroke_width=7,
                color=FORCE_COLOR,
                max_tip_length_to_length_ratio=0.16
            )

        def make_negative_force_arrow(length):

            start = np.array([
                -0.40,
                0.0,
                0.0
            ])

            return Arrow(
                start=start,
                end=start + LEFT * length,
                buff=0,
                stroke_width=7,
                color=FORCE_COLOR,
                max_tip_length_to_length_ratio=0.16
            )

        # ====================================================
        # FORCE LENGTHS
        #
        # طول 2F يساوي بالضبط ضعفي طول F.
        # ====================================================

        BASE_FORCE_LENGTH = 1.15
        DOUBLE_FORCE_LENGTH = 2 * BASE_FORCE_LENGTH

        # ====================================================
        # PART 1 — TITLE
        # ====================================================

        title = arabic_text(
            "المجال الكهربائي بين لوحين",
            size=43,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.38
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.12
            ),
            run_time=0.9
        )

        self.wait(0.8)

        # ====================================================
        # PART 2 — PARALLEL PLATES
        # ====================================================

        positive_plate = make_plate(
            -4.15,
            POSITIVE
        )

        negative_plate = make_plate(
            4.15,
            NEGATIVE
        )

        positive_signs = make_plate_signs(
            -4.15,
            "+",
            POSITIVE
        )

        negative_signs = make_plate_signs(
            4.15,
            "−",
            NEGATIVE
        )

        self.play(
            FadeIn(
                positive_plate,
                shift=RIGHT * 0.15
            ),
            FadeIn(
                negative_plate,
                shift=LEFT * 0.15
            ),
            run_time=0.8
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(sign)
                    for sign in positive_signs
                ],
                lag_ratio=0.06
            ),
            LaggedStart(
                *[
                    FadeIn(sign)
                    for sign in negative_signs
                ],
                lag_ratio=0.06
            ),
            run_time=0.9
        )

        positive_label = arabic_text(
            "موجب",
            size=26,
            color=POSITIVE
        ).next_to(
            positive_plate,
            DOWN,
            buff=0.20
        )

        negative_label = arabic_text(
            "سالب",
            size=26,
            color=NEGATIVE
        ).next_to(
            negative_plate,
            DOWN,
            buff=0.20
        )

        self.play(
            FadeIn(positive_label),
            FadeIn(negative_label),
            run_time=0.6
        )

        self.wait(1.0)

        # ====================================================
        # PART 3 — ELECTRIC FIELD
        # ====================================================

        field_arrows = make_uniform_field()

        self.play(
            LaggedStart(
                *[
                    GrowArrow(arrow)
                    for arrow in field_arrows
                ],
                lag_ratio=0.10
            ),
            run_time=1.4
        )

        self.wait(1.0)

        direction_label = VGroup(
            MathTex(
                r"\vec{E}",
                font_size=44,
                color=FIELD_COLOR
            ),
            arabic_text(
                "من الموجب إلى السالب",
                size=28,
                color=FIELD_COLOR
            )
        ).arrange(
            RIGHT,
            buff=0.22
        ).move_to(
            DOWN * 2.78
        )

        self.play(
            FadeIn(direction_label),
            run_time=0.7
        )

        self.wait(1.2)

        # ====================================================
        # PART 4 — UNIFORM FIELD
        # ====================================================

        uniform_text_1 = arabic_text(
            "بعيدًا عن الحواف",
            size=28,
            color=TEXT_SECONDARY
        ).move_to(
            UP * 2.55
        )

        uniform_text_2 = arabic_text(
            "المتجهات متوازية ومتساوية في المقدار",
            size=30,
            weight=BOLD,
            color=FIELD_COLOR
        ).next_to(
            uniform_text_1,
            DOWN,
            buff=0.15
        )

        self.play(
            FadeOut(direction_label),
            FadeIn(uniform_text_1),
            run_time=0.7
        )

        self.play(
            FadeIn(uniform_text_2),
            run_time=0.7
        )

        self.wait(1.3)

        uniform_name = arabic_text(
            "مجال كهربائي منتظم",
            size=36,
            weight=BOLD,
            color=FIELD_COLOR
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(
                uniform_name,
                scale=0.9
            ),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 5 — CLEAR EXPLANATION
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    uniform_text_1,
                    uniform_text_2,
                    uniform_name
                )
            ),
            run_time=0.6
        )

        # ====================================================
        # PART 6 — POSITIVE TEST CHARGE
        # ====================================================

        question = arabic_text(
            "ماذا يحدث إذا وضعنا شحنة داخل المجال؟",
            size=31,
            weight=BOLD
        ).move_to(
            UP * 2.55
        )

        self.play(
            FadeIn(question),
            run_time=0.7
        )

        self.wait(0.8)

        positive_test = make_test_charge("+")
        positive_test.move_to(ORIGIN)

        q_positive_label = MathTex(
            "q>0",
            font_size=40,
            color=POSITIVE
        ).next_to(
            positive_test,
            DOWN,
            buff=0.22
        )

        self.play(
            FadeIn(
                positive_test,
                scale=0.7
            ),
            FadeIn(q_positive_label),
            run_time=0.8
        )

        self.wait(0.8)

        # ====================================================
        # FORCE ON POSITIVE CHARGE
        # ====================================================

        positive_force = make_positive_force_arrow(
            BASE_FORCE_LENGTH
        )

        positive_force_label = MathTex(
            r"\vec{F}",
            font_size=45,
            color=FORCE_COLOR
        ).next_to(
            positive_force,
            UP,
            buff=0.10
        )

        self.play(
            GrowArrow(positive_force),
            FadeIn(positive_force_label),
            run_time=0.8
        )

        positive_direction_text = arabic_text(
            "الشحنة الموجبة: القوة في اتجاه المجال",
            size=29,
            weight=BOLD,
            color=POSITIVE
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(positive_direction_text),
            run_time=0.7
        )

        self.wait(1.2)

        # ====================================================
        # EQUATION
        #
        # كل جزء MathTex مستقل حتى لا تتأثر
        # رموز أخرى عند تغيير الألوان.
        # ====================================================

        equation = MathTex(
            r"\vec{F}",
            "=",
            "q",
            r"\vec{E}",
            font_size=60
        )

        equation[0].set_color(FORCE_COLOR)
        equation[1].set_color(TEXT_MAIN)
        equation[2].set_color(TEXT_MAIN)
        equation[3].set_color(FIELD_COLOR)

        # أعلى سهم للمجال عند y = 1.80
        # لذلك المعادلة معزولة في الأعلى.
        equation.move_to(
            UP * 2.55
        )

        self.play(
            FadeOut(question),
            FadeIn(equation),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 7 — NEGATIVE TEST CHARGE
        # ====================================================

        self.play(
            FadeOut(positive_direction_text),
            run_time=0.4
        )

        negative_test = make_test_charge("−")
        negative_test.move_to(ORIGIN)

        q_negative_label = MathTex(
            "q<0",
            font_size=40,
            color=NEGATIVE
        ).move_to(
            q_positive_label
        )

        negative_force = make_negative_force_arrow(
            BASE_FORCE_LENGTH
        )

        negative_force_label = MathTex(
            r"\vec{F}",
            font_size=45,
            color=FORCE_COLOR
        ).next_to(
            negative_force,
            UP,
            buff=0.10
        )

        # أسهم المجال لا تتغير.
        self.play(
            ReplacementTransform(
                positive_test,
                negative_test
            ),
            ReplacementTransform(
                q_positive_label,
                q_negative_label
            ),
            ReplacementTransform(
                positive_force,
                negative_force
            ),
            ReplacementTransform(
                positive_force_label,
                negative_force_label
            ),
            run_time=1.0
        )

        self.wait(0.7)

        negative_direction_text = arabic_text(
            "الشحنة السالبة: القوة عكس اتجاه المجال",
            size=29,
            weight=BOLD,
            color=NEGATIVE
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(negative_direction_text),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 8 — RETURN TO POSITIVE q
        # ====================================================

        self.play(
            FadeOut(negative_direction_text),
            run_time=0.4
        )

        positive_test_again = make_test_charge("+")
        positive_test_again.move_to(ORIGIN)

        q_label_again = MathTex(
            "q",
            font_size=42,
            color=POSITIVE
        ).move_to(
            q_negative_label
        )

        normal_force = make_positive_force_arrow(
            BASE_FORCE_LENGTH
        )

        normal_force_label = MathTex(
            "F",
            font_size=44,
            color=FORCE_COLOR
        ).next_to(
            normal_force,
            UP,
            buff=0.10
        )

        self.play(
            ReplacementTransform(
                negative_test,
                positive_test_again
            ),
            ReplacementTransform(
                q_negative_label,
                q_label_again
            ),
            ReplacementTransform(
                negative_force,
                normal_force
            ),
            ReplacementTransform(
                negative_force_label,
                normal_force_label
            ),
            run_time=1.0
        )

        self.wait(0.7)

        increase_text = arabic_text(
            "نزيد مقدار الشحنة",
            size=29,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(increase_text),
            run_time=0.6
        )

        self.wait(0.6)

        # ====================================================
        # q -> 2q
        #
        # F length  = BASE_FORCE_LENGTH
        # 2F length = 2 × BASE_FORCE_LENGTH
        #
        # ونقطة البداية نفسها.
        # ====================================================

        double_q_label = MathTex(
            "2q",
            font_size=46,
            color=POSITIVE
        ).move_to(
            q_label_again
        )

        double_force = make_positive_force_arrow(
            DOUBLE_FORCE_LENGTH
        )

        double_force_label = MathTex(
            "2F",
            font_size=47,
            color=FORCE_COLOR
        ).next_to(
            double_force,
            UP,
            buff=0.10
        )

        self.play(
            ReplacementTransform(
                q_label_again,
                double_q_label
            ),
            ReplacementTransform(
                normal_force,
                double_force
            ),
            ReplacementTransform(
                normal_force_label,
                double_force_label
            ),
            run_time=1.0
        )

        self.wait(1.0)

        # ====================================================
        # RELATION
        # ====================================================

        relation = MathTex(
            "q",
            r"\rightarrow",
            "2q",
            r"\qquad",
            "F",
            r"\rightarrow",
            "2F",
            font_size=48
        ).to_edge(
            DOWN,
            buff=0.28
        )

        relation[0].set_color(POSITIVE)
        relation[1].set_color(TEXT_SECONDARY)
        relation[2].set_color(POSITIVE)

        relation[3].set_color(TEXT_MAIN)

        relation[4].set_color(FORCE_COLOR)
        relation[5].set_color(TEXT_SECONDARY)
        relation[6].set_color(FORCE_COLOR)

        self.play(
            ReplacementTransform(
                increase_text,
                relation
            ),
            run_time=0.7
        )

        self.wait(1.2)

        # ====================================================
        # PART 9 — FIELD REMAINS UNCHANGED
        # ====================================================

        unchanged_text = arabic_text(
            "المجال بين اللوحين بقي كما هو",
            size=29,
            weight=BOLD,
            color=FIELD_COLOR
        ).move_to(
            UP * 2.55
        )

        self.play(
            FadeOut(equation),
            FadeIn(unchanged_text),
            run_time=0.7
        )

        # لا نحرك ولا نغيّر ولا نكبر field_arrows.
        self.wait(1.6)

        # ====================================================
        # PART 10 — FINAL EQUATION
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    unchanged_text,
                    relation,
                    positive_test_again,
                    double_q_label,
                    double_force,
                    double_force_label
                )
            ),
            run_time=0.7
        )

        final_equation = MathTex(
            r"\vec{F}",
            "=",
            "q",
            r"\vec{E}",
            font_size=66
        )

        final_equation[0].set_color(FORCE_COLOR)
        final_equation[1].set_color(TEXT_MAIN)
        final_equation[2].set_color(TEXT_MAIN)
        final_equation[3].set_color(FIELD_COLOR)

        final_equation.move_to(
            UP * 2.55
        )

        self.play(
            FadeIn(
                final_equation,
                scale=0.9
            ),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 11 — CLEAR THE SCIENTIFIC SCENE
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    title,
                    positive_plate,
                    negative_plate,
                    positive_signs,
                    negative_signs,
                    positive_label,
                    negative_label,
                    field_arrows,
                    final_equation
                )
            ),
            run_time=1.0
        )

        self.wait(0.4)

        # ====================================================
        # PART 12 — SCIENTIFIC CLOSING
        # ====================================================

        closing_line_1 = arabic_text(
            "إذاً الشحنة الكهربائية لا تؤثر فقط عند التلامس.",
            size=35,
            weight=BOLD,
            color=TEXT_MAIN
        )

        closing_line_2 = arabic_text(
            "إنها تنشئ مجالًا كهربائيًا في الفضاء من حولها،",
            size=32,
            color=TEXT_SECONDARY
        )

        closing_line_3 = arabic_text(
            "وهذا المجال هو الذي يحدد القوة التي ستؤثر في أي شحنة توضع داخله.",
            size=30,
            color=TEXT_SECONDARY
        )

        closing_group = VGroup(
            closing_line_1,
            closing_line_2,
            closing_line_3
        ).arrange(
            DOWN,
            buff=0.25
        ).move_to(ORIGIN)

        self.play(
            LaggedStart(
                FadeIn(
                    closing_line_1,
                    shift=UP * 0.12
                ),
                FadeIn(
                    closing_line_2,
                    shift=UP * 0.12
                ),
                FadeIn(
                    closing_line_3,
                    shift=UP * 0.12
                ),
                lag_ratio=0.18
            ),
            run_time=1.4
        )

        # وقت كافٍ للتعليق الصوتي
        self.wait(4.2)

        # اختفاء هادئ للنص العلمي
        self.play(
            LaggedStart(
                FadeOut(
                    closing_line_3,
                    shift=UP * 0.10,
                    scale=0.97
                ),
                FadeOut(
                    closing_line_2,
                    shift=UP * 0.10,
                    scale=0.97
                ),
                FadeOut(
                    closing_line_1,
                    shift=UP * 0.10,
                    scale=0.97
                ),
                lag_ratio=0.12
            ),
            run_time=1.1
        )

        self.wait(0.45)

        # ====================================================
        # PART 13 — FINAL SIGNATURE
        # ====================================================

        outro_name = Text(
            "Raji Youssef",
            font="DejaVu Sans",
            font_size=46,
            weight=BOLD,
            color=NAME_COLOR
        )

        separator = Line(
            LEFT * 1.15,
            RIGHT * 1.15,
            stroke_width=2.5,
            color=NAME_COLOR
        )

        outro_message = arabic_text(
            "اشترك في القناة. مع أطيب التحيات.",
            size=31,
            color=TEXT_MAIN
        )

        outro_group = VGroup(
            outro_name,
            separator,
            outro_message
        ).arrange(
            DOWN,
            buff=0.23
        ).move_to(ORIGIN)

        # ظهور الاسم أولًا
        self.play(
            FadeIn(
                outro_name,
                shift=UP * 0.18,
                scale=0.92
            ),
            run_time=0.8
        )

        # ثم الخط والرسالة
        self.play(
            Create(separator),
            FadeIn(
                outro_message,
                shift=UP * 0.10
            ),
            run_time=0.8
        )

        self.wait(2.5)

        # ====================================================
        # FINAL BEAUTIFUL FADE OUT
        #
        # الاسم يتحرك قليلًا إلى أعلى
        # والعبارة إلى أسفل
        # والخط يختفي في المنتصف.
        # ====================================================

        self.play(
            LaggedStart(
                FadeOut(
                    outro_message,
                    shift=DOWN * 0.16,
                    scale=0.95
                ),
                FadeOut(
                    separator,
                    scale=0.70
                ),
                FadeOut(
                    outro_name,
                    shift=UP * 0.16,
                    scale=1.05
                ),
                lag_ratio=0.10
            ),
            run_time=1.3
        )

        self.wait(0.4)


# ============================================================
# DIRECT RENDERING FROM PYCHARM
# ====================================================

if __name__ == "__main__":

    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    config.output_file = "scene_23_uniform_field_and_force"

    config.preview = True
    config.quality = "high_quality"

    Scene23UniformFieldAndForce().render()