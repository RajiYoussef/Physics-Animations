from manim import *


# ============================================================
# Scene 06
# تكميم الشحنة
#
# الفكرة:
# - توجد شحنة أساسية مقدارها e.
# - شحنات الأجسام تظهر كمضاعفات صحيحة من e.
# - نبني q = ne تدريجيًا، ولا نظهرها في البداية.
# - في النهاية نوضح أن 1 C يمثل عددًا هائلًا جدًا
#   من الشحنات الأساسية.
# ============================================================


class Scene06ChargeQuantization(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        # ----------------------------------------------------
        # Consistent color palette
        # ----------------------------------------------------

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"
        ACCENT = "#7EE787"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

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

        def electron(position=ORIGIN, scale_factor=1.0):

            circle = Circle(
                radius=0.27 * scale_factor,
                stroke_width=3,
                color=NEGATIVE,
                fill_color=NEGATIVE,
                fill_opacity=0.2
            ).move_to(position)

            sign = Text(
                "−",
                font_size=30 * scale_factor,
                weight=BOLD,
                color=NEGATIVE
            ).move_to(circle)

            return VGroup(circle, sign)

        # ====================================================
        # PART 1 — OPENING QUESTION
        # ====================================================

        title_1 = arabic_text(
            "هل يمكن للشحنة أن تأخذ أي قيمة؟",
            size=44,
            weight=BOLD
        )

        self.play(
            FadeIn(
                title_1,
                shift=UP * 0.15
            ),
            run_time=1.0
        )

        self.wait(1.8)

        title_2 = arabic_text(
            "أم أنها تأتي في وحدات محددة؟",
            size=38,
            color=ACCENT
        ).next_to(
            title_1,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(title_2),
            run_time=0.8
        )

        self.wait(1.6)

        self.play(
            FadeOut(title_1),
            FadeOut(title_2),
            run_time=0.7
        )

        # ====================================================
        # PART 2 — ONE ELEMENTARY CHARGE
        # ====================================================

        section_title = arabic_text(
            "لنبدأ بشحنة أساسية واحدة",
            size=40,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(section_title),
            run_time=0.8
        )

        self.wait(0.8)

        one_electron = electron(
            ORIGIN + UP * 0.2,
            scale_factor=1.25
        )

        self.play(
            FadeIn(
                one_electron,
                scale=0.6
            ),
            run_time=0.8
        )

        self.wait(1.0)

        e_symbol = MathTex(
            "e",
            font_size=68,
            color=ACCENT
        ).next_to(
            one_electron,
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(e_symbol),
            run_time=0.7
        )

        self.wait(1.2)

        elementary_text = arabic_text(
            "الشحنة الأولية",
            size=31,
            color=ACCENT
        ).next_to(
            e_symbol,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(elementary_text),
            run_time=0.7
        )

        self.wait(1.2)

        e_value = MathTex(
            "e",
            "=",
            "1.602",
            r"\times",
            "10^{-19}",
            r"\,\mathrm{C}",
            font_size=48
        ).to_edge(
            DOWN,
            buff=0.55
        )

        e_value[0].set_color(ACCENT)
        e_value[2].set_color(ACCENT)
        e_value[4].set_color(ACCENT)
        e_value[5].set_color(ACCENT)

        self.play(
            FadeIn(
                e_value,
                shift=UP * 0.1
            ),
            run_time=0.9
        )

        self.wait(1.8)

        # ====================================================
        # PART 3 — BUILD MULTIPLES VISUALLY
        # ====================================================

        self.play(
            FadeOut(section_title),
            FadeOut(elementary_text),
            FadeOut(e_value),
            one_electron.animate.scale(0.75).move_to(
                LEFT * 3.8 + UP * 0.5
            ),
            e_symbol.animate.scale(0.75).next_to(
                LEFT * 3.8 + UP * 0.5,
                DOWN,
                buff=0.35
            ),
            run_time=0.8
        )

        multiples_title = arabic_text(
            "نضيف شحنات أساسية واحدة تلو الأخرى",
            size=38,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(multiples_title),
            run_time=0.8
        )

        # ----------------------------------------------------
        # 1e
        # ----------------------------------------------------

        one_label = MathTex(
            "1e",
            font_size=46,
            color=ACCENT
        ).move_to(
            LEFT * 3.8 + DOWN * 0.8
        )

        self.play(
            ReplacementTransform(
                e_symbol,
                one_label
            ),
            run_time=0.6
        )

        self.wait(0.8)

        # ----------------------------------------------------
        # 2e
        # ----------------------------------------------------

        electron_2a = electron(
            LEFT * 1.1 + UP * 0.5,
            scale_factor=0.95
        )

        electron_2b = electron(
            RIGHT * 1.1 + UP * 0.5,
            scale_factor=0.95
        )

        pair_group = VGroup(
            electron_2a,
            electron_2b
        )

        pair_label = MathTex(
            "2e",
            font_size=46,
            color=ACCENT
        ).move_to(
            DOWN * 0.8
        )

        self.play(
            FadeIn(
                electron_2a,
                scale=0.7
            ),
            run_time=0.6
        )

        self.play(
            FadeIn(
                electron_2b,
                scale=0.7
            ),
            run_time=0.6
        )

        self.play(
            FadeIn(pair_label),
            run_time=0.6
        )

        self.wait(1.0)

        # ----------------------------------------------------
        # 3e
        # ----------------------------------------------------

        electron_3a = electron(
            RIGHT * 2.65 + LEFT * 0.75 + UP * 0.5,
            scale_factor=0.85
        )

        electron_3b = electron(
            RIGHT * 2.65 + UP * 0.5,
            scale_factor=0.85
        )

        electron_3c = electron(
            RIGHT * 2.65 + RIGHT * 0.75 + UP * 0.5,
            scale_factor=0.85
        )

        triple_group = VGroup(
            electron_3a,
            electron_3b,
            electron_3c
        )

        triple_label = MathTex(
            "3e",
            font_size=46,
            color=ACCENT
        ).move_to(
            RIGHT * 2.65 + DOWN * 0.8
        )

        self.play(
            LaggedStart(
                FadeIn(electron_3a, scale=0.7),
                FadeIn(electron_3b, scale=0.7),
                FadeIn(electron_3c, scale=0.7),
                lag_ratio=0.18
            ),
            run_time=1.2
        )

        self.play(
            FadeIn(triple_label),
            run_time=0.6
        )

        self.wait(1.5)

        # ====================================================
        # PART 4 — INTEGER STEPS
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    one_electron,
                    one_label,
                    pair_group,
                    pair_label,
                    triple_group,
                    triple_label,
                    multiples_title
                )
            ),
            run_time=0.8
        )

        integer_title = arabic_text(
            "عدد الشحنات الأساسية يكون عددًا صحيحًا",
            size=39,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(integer_title),
            run_time=0.8
        )

        self.wait(0.8)

        number_line = NumberLine(
            x_range=[0, 5, 1],
            length=8.0,
            include_numbers=True,
            font_size=28,
            color=TEXT_SECONDARY
        ).shift(
            DOWN * 0.15
        )

        self.play(
            Create(number_line),
            run_time=1.0
        )

        self.wait(0.7)

        dot = Dot(
            number_line.n2p(1),
            radius=0.11,
            color=ACCENT
        )

        self.play(
            FadeIn(dot),
            run_time=0.5
        )

        self.wait(0.5)

        self.play(
            dot.animate.move_to(
                number_line.n2p(2)
            ),
            run_time=0.7
        )

        self.wait(0.4)

        self.play(
            dot.animate.move_to(
                number_line.n2p(3)
            ),
            run_time=0.7
        )

        self.wait(0.5)

        n_text = MathTex(
            "n",
            "=",
            "0,\,1,\,2,\,3,\,\ldots",
            font_size=48
        ).to_edge(
            DOWN,
            buff=0.6
        )

        n_text[0].set_color(ACCENT)

        self.play(
            FadeIn(n_text),
            run_time=0.8
        )

        self.wait(1.3)

        # ----------------------------------------------------
        # Show what is NOT allowed as an electron count
        # ----------------------------------------------------

        invalid_value = MathTex(
            "n",
            "=",
            "2.37",
            font_size=48
        ).move_to(
            UP * 1.0
        )

        invalid_value[0].set_color(ACCENT)

        cross = Cross(
            invalid_value,
            stroke_width=5,
            color="#FF6B6B"
        )

        self.play(
            FadeIn(invalid_value),
            run_time=0.6
        )

        self.wait(0.6)

        self.play(
            Create(cross),
            run_time=0.6
        )

        invalid_note = arabic_text(
            "لا يوجد 2.37 إلكترونًا زائدًا",
            size=29,
            color=TEXT_SECONDARY
        ).next_to(
            invalid_value,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(invalid_note),
            run_time=0.7
        )

        self.wait(1.5)

        # ====================================================
        # PART 5 — BUILD q = ne
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    integer_title,
                    number_line,
                    dot,
                    n_text,
                    invalid_value,
                    cross,
                    invalid_note
                )
            ),
            run_time=0.8
        )

        relation_title = arabic_text(
            "كيف نكتب هذه الفكرة رياضيًا؟",
            size=40,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(relation_title),
            run_time=0.8
        )

        self.wait(1.0)

        q_symbol = MathTex(
            "q",
            font_size=72,
            color=TEXT_MAIN
        ).move_to(
            LEFT * 2.8
        )

        q_label = arabic_text(
            "شحنة الجسم",
            size=28,
            color=TEXT_SECONDARY
        ).next_to(
            q_symbol,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(q_symbol),
            FadeIn(q_label),
            run_time=0.8
        )

        self.wait(0.8)

        n_symbol = MathTex(
            "n",
            font_size=72,
            color=ACCENT
        ).move_to(
            ORIGIN
        )

        n_label = arabic_text(
            "عدد صحيح",
            size=28,
            color=ACCENT
        ).next_to(
            n_symbol,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(n_symbol),
            FadeIn(n_label),
            run_time=0.8
        )

        self.wait(0.8)

        e_symbol_2 = MathTex(
            "e",
            font_size=72,
            color=NEGATIVE
        ).move_to(
            RIGHT * 2.8
        )

        e_label_2 = arabic_text(
            "الشحنة الأولية",
            size=28,
            color=NEGATIVE
        ).next_to(
            e_symbol_2,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(e_symbol_2),
            FadeIn(e_label_2),
            run_time=0.8
        )

        self.wait(1.0)

        # ----------------------------------------------------
        # Verbal relationship first
        # ----------------------------------------------------

        verbal_relation = arabic_text(
            "الشحنة = عدد صحيح × الشحنة الأولية",
            size=34,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.5
        )

        self.play(
            FadeIn(verbal_relation),
            run_time=0.8
        )

        self.wait(1.6)

        self.play(
            FadeOut(q_label),
            FadeOut(n_label),
            FadeOut(e_label_2),
            FadeOut(verbal_relation),
            run_time=0.6
        )

        # Move symbols into equation positions
        self.play(
            q_symbol.animate.move_to(
                LEFT * 1.6
            ),
            n_symbol.animate.move_to(
                RIGHT * 0.15
            ),
            e_symbol_2.animate.move_to(
                RIGHT * 1.15
            ),
            run_time=0.8
        )

        equals_sign = MathTex(
            "=",
            font_size=72
        ).move_to(
            LEFT * 0.75
        )

        self.play(
            FadeIn(equals_sign),
            run_time=0.5
        )

        self.wait(0.5)

        equation_group = VGroup(
            q_symbol,
            equals_sign,
            n_symbol,
            e_symbol_2
        )

        equation_box = SurroundingRectangle(
            equation_group,
            buff=0.32,
            stroke_width=3,
            color=ACCENT
        )

        self.play(
            Create(equation_box),
            run_time=0.7
        )

        self.wait(1.4)

        equation_name = arabic_text(
            "تكميم الشحنة",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            equation_box,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(equation_name),
            run_time=0.7
        )

        self.wait(1.5)

        # ====================================================
        # PART 6 — SIGN OF THE CHARGE
        # ====================================================

        self.play(
            FadeOut(relation_title),
            FadeOut(equation_name),
            equation_box.animate.shift(
                UP * 0.4
            ),
            equation_group.animate.shift(
                UP * 0.4
            ),
            run_time=0.7
        )

        sign_note_1 = arabic_text(
            "إذا كان لدينا فائض من الإلكترونات",
            size=31
        ).move_to(
            DOWN * 1.0
        )

        sign_note_2 = arabic_text(
            "تكون الشحنة سالبة",
            size=33,
            weight=BOLD,
            color=NEGATIVE
        ).next_to(
            sign_note_1,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(sign_note_1),
            run_time=0.7
        )

        self.play(
            FadeIn(sign_note_2),
            run_time=0.7
        )

        self.wait(1.4)

        sign_note_3 = arabic_text(
            "أما فقد الإلكترونات فيجعل الشحنة موجبة",
            size=31,
            color=POSITIVE
        ).next_to(
            sign_note_2,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(sign_note_3),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 7 — HOW BIG IS 1 COULOMB?
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    equation_group,
                    equation_box,
                    sign_note_1,
                    sign_note_2,
                    sign_note_3
                )
            ),
            run_time=0.8
        )

        coulomb_title = arabic_text(
            "ما حجم كولوم واحد مقارنة بشحنة إلكترون؟",
            size=39,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(coulomb_title),
            run_time=0.8
        )

        self.wait(0.8)

        single_e = electron(
            LEFT * 4.3 + UP * 0.2,
            scale_factor=1.05
        )

        single_e_label = MathTex(
            "e",
            font_size=48,
            color=NEGATIVE
        ).next_to(
            single_e,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(single_e),
            FadeIn(single_e_label),
            run_time=0.7
        )

        self.wait(0.8)

        # ----------------------------------------------------
        # Build many tiny charge dots
        # ----------------------------------------------------

        charge_cloud = VGroup()

        rows = 7
        cols = 13

        x_start = -1.4
        y_start = 1.15

        for row in range(rows):
            for col in range(cols):

                d = Dot(
                    radius=0.035,
                    color=NEGATIVE
                )

                d.move_to(
                    [
                        x_start + col * 0.38,
                        y_start - row * 0.38,
                        0
                    ]
                )

                charge_cloud.add(d)

        self.play(
            LaggedStart(
                *[
                    FadeIn(dot, scale=0.5)
                    for dot in charge_cloud
                ],
                lag_ratio=0.015
            ),
            run_time=1.7
        )

        self.wait(0.8)

        ellipsis = MathTex(
            "\cdots",
            font_size=60,
            color=TEXT_SECONDARY
        ).next_to(
            charge_cloud,
            RIGHT,
            buff=0.35
        )

        self.play(
            FadeIn(ellipsis),
            run_time=0.5
        )

        self.wait(0.6)

        huge_number = MathTex(
            "1",
            r"\,\mathrm{C}",
            r"\approx",
            "6.24",
            r"\times",
            "10^{18}",
            font_size=50
        ).to_edge(
            DOWN,
            buff=0.55
        )

        huge_number[0].set_color(ACCENT)
        huge_number[1].set_color(ACCENT)
        huge_number[3].set_color(NEGATIVE)
        huge_number[5].set_color(NEGATIVE)

        self.play(
            FadeIn(
                huge_number,
                shift=UP * 0.1
            ),
            run_time=0.9
        )

        self.wait(1.4)

        huge_label = arabic_text(
            "شحنة أولية تقريبًا",
            size=28,
            color=TEXT_SECONDARY
        ).next_to(
            huge_number,
            DOWN,
            buff=0.2
        )

        self.play(
            FadeIn(huge_label),
            run_time=0.6
        )

        self.wait(1.8)

        # ====================================================
        # PART 8 — FINAL SUMMARY
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    coulomb_title,
                    single_e,
                    single_e_label,
                    charge_cloud,
                    ellipsis,
                    huge_number,
                    huge_label
                )
            ),
            run_time=0.8
        )

        summary_title = arabic_text(
            "الفكرة الأساسية",
            size=42,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.5
        )

        summary_1 = arabic_text(
            "الشحنة لا تأتي بأي قيمة اعتباطية",
            size=34
        ).shift(
            UP * 0.6
        )

        summary_2 = arabic_text(
            "بل في مضاعفات من الشحنة الأولية e",
            size=35,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            summary_1,
            DOWN,
            buff=0.35
        )

        final_equation = MathTex(
            "q",
            "=",
            "n",
            "e",
            font_size=64
        ).next_to(
            summary_2,
            DOWN,
            buff=0.55
        )

        final_equation[2].set_color(ACCENT)
        final_equation[3].set_color(NEGATIVE)

        self.play(
            FadeIn(summary_title),
            run_time=0.7
        )

        self.play(
            FadeIn(summary_1),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(summary_2),
            run_time=0.7
        )

        self.wait(0.7)

        self.play(
            FadeIn(final_equation),
            run_time=0.7
        )

        self.wait(1.6)

        # ====================================================
        # PART 9 — TRANSITION TO CHARGE TRANSFER
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    summary_title,
                    summary_1,
                    summary_2,
                    final_equation
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "لكن كيف تنتقل هذه الإلكترونات",
            size=36
        ).shift(
            UP * 0.35
        )

        transition_2 = arabic_text(
            "من جسم إلى آخر؟",
            size=40,
            weight=BOLD
        ).next_to(
            transition_1,
            DOWN,
            buff=0.25
        )

        transition_3 = arabic_text(
            "إحدى الطرق هي الشحن بالاحتكاك",
            size=32,
            color=ACCENT
        ).next_to(
            transition_2,
            DOWN,
            buff=0.38
        )

        self.play(
            FadeIn(transition_1),
            run_time=0.7
        )

        self.play(
            FadeIn(transition_2),
            run_time=0.7
        )

        self.wait(0.7)

        self.play(
            FadeIn(transition_3),
            run_time=0.7
        )

        self.wait(2.0)

        self.play(
            FadeOut(transition_1),
            FadeOut(transition_2),
            FadeOut(transition_3),
            run_time=0.8
        )


# ============================================================
# DIRECT RENDERING FROM PYCHARM
# ============================================================

if __name__ == "__main__":

    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    config.output_file = "scene_06_charge_quantization"

    config.preview = True
    config.quality = "high_quality"

    Scene06ChargeQuantization().render()