from manim import *


# ============================================================
# Scene 17
# القوة الكهربائية: المسافة ومقدار الشحنة
#
# التسلسل:
#
# 1. شحنة موجبة وشحنة سالبة لا تتلامسان.
# 2. تظهر قوتان كهربائيتان متساويتان في المقدار
#    ومتعاكستان في الاتجاه.
# 3. نغير المسافة فقط:
#       أبعد  -> قوة أضعف
#       أقرب  -> قوة أكبر
# 4. نعيد الشحنتين إلى مسافة ثابتة.
# 5. نعرّف q1 و q2 والقوة F.
# 6. q1 -> 2q1  يؤدي إلى  F -> 2F
# 7. نعيد للحالة الأصلية.
# 8. نضاعف الشحنتين:
#       2q1 , 2q2  يؤدي إلى 4F
# 9. نستنتج:
#
#       F ∝ |q1 q2|
#
# 10. نترك العلاقة الدقيقة مع المسافة للمشهد التالي.
# ============================================================


class Scene17ElectricForceAndChargeMagnitude(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"
        ACCENT = "#7EE787"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

        FORCE_COLOR = "#7EE787"
        DISTANCE_COLOR = "#FFD166"

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

        def make_charge(center, sign="+"):

            color = POSITIVE if sign == "+" else NEGATIVE

            circle = Circle(
                radius=0.50,
                stroke_width=4,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.13
            ).move_to(center)

            sign_text = Text(
                sign,
                font_size=43,
                weight=BOLD,
                color=color
            ).move_to(circle)

            return VGroup(
                circle,
                sign_text
            )

        def make_force_arrows(
            left_center,
            right_center,
            length=0.85,
            stroke_width=6
        ):
            """
            Attraction:
            both arrows point toward the other charge.

            The arrows are always equal in length.
            """

            left_start = left_center + RIGHT * 0.60

            left_arrow = Arrow(
                start=left_start,
                end=left_start + RIGHT * length,
                buff=0,
                stroke_width=stroke_width,
                color=FORCE_COLOR,
                max_tip_length_to_length_ratio=0.16
            )

            right_start = right_center + LEFT * 0.60

            right_arrow = Arrow(
                start=right_start,
                end=right_start + LEFT * length,
                buff=0,
                stroke_width=stroke_width,
                color=FORCE_COLOR,
                max_tip_length_to_length_ratio=0.16
            )

            return VGroup(
                left_arrow,
                right_arrow
            )

        def make_distance_marker(
            left_center,
            right_center,
            label="r"
        ):

            arrow = DoubleArrow(
                start=left_center + RIGHT * 0.62 + UP * 1.10,
                end=right_center + LEFT * 0.62 + UP * 1.10,
                buff=0.05,
                stroke_width=3,
                color=DISTANCE_COLOR,
                max_tip_length_to_length_ratio=0.10
            )

            label_math = MathTex(
                label,
                font_size=42,
                color=DISTANCE_COLOR
            ).next_to(
                arrow,
                UP,
                buff=0.08
            )

            return VGroup(
                arrow,
                label_math
            )

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "القوة الكهربائية بين الشحنات",
            size=43,
            weight=BOLD
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.15
            ),
            run_time=1.0
        )

        self.wait(1.3)

        self.play(
            title.animate.to_edge(
                UP,
                buff=0.42
            ).scale(0.86),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — TWO CHARGES
        # ====================================================

        left_center = LEFT * 2.75 + DOWN * 0.30
        right_center = RIGHT * 2.75 + DOWN * 0.30

        positive_charge = make_charge(
            left_center,
            "+"
        )

        negative_charge = make_charge(
            right_center,
            "−"
        )

        self.play(
            FadeIn(
                positive_charge,
                scale=0.8
            ),
            FadeIn(
                negative_charge,
                scale=0.8
            ),
            run_time=0.9
        )

        self.wait(1.0)

        # ====================================================
        # PART 3 — CLEAR GAP / NO CONTACT
        # ====================================================

        gap_marker = make_distance_marker(
            left_center,
            right_center,
            ""
        )

        no_contact = arabic_text(
            "لا يوجد تلامس",
            size=29,
            weight=BOLD,
            color=DISTANCE_COLOR
        ).move_to(
            UP * 1.30
        )

        self.play(
            GrowFromCenter(gap_marker[0]),
            FadeIn(no_contact),
            run_time=0.8
        )

        self.wait(1.2)

        # ====================================================
        # PART 4 — ELECTRIC FORCE
        # ====================================================

        force_arrows = make_force_arrows(
            left_center,
            right_center,
            length=0.82,
            stroke_width=6
        )

        self.play(
            GrowArrow(force_arrows[0]),
            GrowArrow(force_arrows[1]),
            run_time=0.9
        )

        force_text = arabic_text(
            "قوة كهربائية",
            size=33,
            weight=BOLD,
            color=FORCE_COLOR
        ).move_to(
            DOWN * 1.65
        )

        self.play(
            FadeIn(force_text),
            run_time=0.7
        )

        self.wait(1.2)

        noncontact_text = arabic_text(
            "قوة لا تلامسية",
            size=35,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            force_text,
            DOWN,
            buff=0.22
        )

        self.play(
            FadeIn(noncontact_text),
            run_time=0.8
        )

        self.wait(1.5)

        self.play(
            FadeOut(gap_marker),
            FadeOut(no_contact),
            FadeOut(force_text),
            FadeOut(noncontact_text),
            run_time=0.6
        )

        # ====================================================
        # PART 5 — CHANGE DISTANCE ONLY
        # ====================================================

        distance_test_title = arabic_text(
            "لنغيّر المسافة فقط",
            size=36,
            weight=BOLD,
            color=DISTANCE_COLOR
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(distance_test_title),
            run_time=0.8
        )

        self.wait(0.8)

        # ----------------------------------------------------
        # Farther apart
        # ----------------------------------------------------

        far_left = LEFT * 3.75 + DOWN * 0.30
        far_right = RIGHT * 3.75 + DOWN * 0.30

        weak_force_arrows = make_force_arrows(
            far_left,
            far_right,
            length=0.48,
            stroke_width=4
        )

        self.play(
            positive_charge.animate.move_to(far_left),
            negative_charge.animate.move_to(far_right),
            ReplacementTransform(
                force_arrows,
                weak_force_arrows
            ),
            run_time=1.5,
            rate_func=smooth
        )

        force_arrows = weak_force_arrows

        self.wait(0.7)

        far_distance_marker = make_distance_marker(
            far_left,
            far_right,
            "r"
        )

        far_text = arabic_text(
            "مسافة أكبر",
            size=30,
            color=DISTANCE_COLOR
        ).move_to(
            UP * 1.80
        )

        weak_text = arabic_text(
            "قوة أضعف",
            size=34,
            weight=BOLD,
            color=FORCE_COLOR
        ).next_to(
            far_text,
            DOWN,
            buff=0.22
        )

        self.play(
            GrowFromCenter(far_distance_marker[0]),
            FadeIn(far_text),
            run_time=0.7
        )

        self.play(
            FadeIn(weak_text),
            run_time=0.7
        )

        self.wait(1.3)

        # ----------------------------------------------------
        # Closer
        # ----------------------------------------------------

        self.play(
            FadeOut(far_distance_marker),
            FadeOut(far_text),
            FadeOut(weak_text),
            run_time=0.5
        )

        close_left = LEFT * 1.90 + DOWN * 0.30
        close_right = RIGHT * 1.90 + DOWN * 0.30

        strong_force_arrows = make_force_arrows(
            close_left,
            close_right,
            length=0.92,
            stroke_width=8
        )

        self.play(
            positive_charge.animate.move_to(close_left),
            negative_charge.animate.move_to(close_right),
            ReplacementTransform(
                force_arrows,
                strong_force_arrows
            ),
            run_time=1.5,
            rate_func=smooth
        )

        force_arrows = strong_force_arrows

        self.wait(0.7)

        close_distance_marker = make_distance_marker(
            close_left,
            close_right,
            "r"
        )

        close_text = arabic_text(
            "مسافة أصغر",
            size=30,
            color=DISTANCE_COLOR
        ).move_to(
            UP * 1.80
        )

        strong_text = arabic_text(
            "قوة أكبر",
            size=34,
            weight=BOLD,
            color=FORCE_COLOR
        ).next_to(
            close_text,
            DOWN,
            buff=0.22
        )

        self.play(
            GrowFromCenter(close_distance_marker[0]),
            FadeIn(close_text),
            run_time=0.7
        )

        self.play(
            FadeIn(strong_text),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 6 — FIRST CONCLUSION
        # ====================================================

        self.play(
            FadeOut(close_distance_marker),
            FadeOut(close_text),
            FadeOut(strong_text),
            FadeOut(distance_test_title),
            run_time=0.5
        )

        distance_conclusion = arabic_text(
            "المسافة تؤثر في مقدار القوة",
            size=35,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(distance_conclusion),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 7 — RETURN TO FIXED DISTANCE
        # ====================================================

        self.play(
            FadeOut(distance_conclusion),
            run_time=0.4
        )

        base_left = LEFT * 2.75 + DOWN * 0.30
        base_right = RIGHT * 2.75 + DOWN * 0.30

        base_force = make_force_arrows(
            base_left,
            base_right,
            length=0.70,
            stroke_width=5
        )

        self.play(
            positive_charge.animate.move_to(base_left),
            negative_charge.animate.move_to(base_right),
            ReplacementTransform(
                force_arrows,
                base_force
            ),
            run_time=1.3
        )

        force_arrows = base_force

        self.wait(0.7)

        fixed_distance_marker = make_distance_marker(
            base_left,
            base_right,
            "r"
        )

        fixed_distance_text = arabic_text(
            "المسافة ثابتة",
            size=28,
            color=DISTANCE_COLOR
        ).move_to(
            UP * 1.85
        )

        self.play(
            GrowFromCenter(
                fixed_distance_marker[0]
            ),
            FadeIn(
                fixed_distance_marker[1]
            ),
            FadeIn(fixed_distance_text),
            run_time=0.8
        )

        self.wait(1.0)

        # ====================================================
        # PART 8 — INTRODUCE q1, q2, F
        # ====================================================

        q1_label = MathTex(
            "q_1",
            font_size=46,
            color=POSITIVE
        ).next_to(
            positive_charge,
            DOWN,
            buff=0.32
        )

        q2_label = MathTex(
            "q_2",
            font_size=46,
            color=NEGATIVE
        ).next_to(
            negative_charge,
            DOWN,
            buff=0.32
        )

        force_label = MathTex(
            "F",
            font_size=52,
            color=FORCE_COLOR
        ).move_to(
            DOWN * 2.15
        )

        self.play(
            FadeIn(q1_label),
            FadeIn(q2_label),
            FadeIn(force_label),
            run_time=0.8
        )

        self.wait(1.2)

        # ====================================================
        # PART 9 — DOUBLE q1 ONLY
        # ====================================================

        charge_test_title = arabic_text(
            "نغيّر مقدار الشحنة فقط",
            size=34,
            weight=BOLD,
            color=POSITIVE
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeOut(title),
            FadeIn(charge_test_title),
            run_time=0.8
        )

        self.wait(0.8)

        q1_double = MathTex(
            "2q_1",
            font_size=48,
            color=POSITIVE
        ).move_to(
            q1_label
        )

        stronger_force = make_force_arrows(
            base_left,
            base_right,
            length=1.05,
            stroke_width=7
        )

        force_2f = MathTex(
            "2F",
            font_size=54,
            color=FORCE_COLOR
        ).move_to(
            force_label
        )

        change_q1 = VGroup(
            MathTex(
                "q_1",
                font_size=39,
                color=POSITIVE
            ),
            MathTex(
                "\\rightarrow",
                font_size=37,
                color=TEXT_SECONDARY
            ),
            MathTex(
                "2q_1",
                font_size=39,
                color=POSITIVE
            )
        ).arrange(
            RIGHT,
            buff=0.18
        ).move_to(
            UP * 1.30
        )

        self.play(
            FadeIn(change_q1),
            run_time=0.7
        )

        self.wait(0.7)

        self.play(
            ReplacementTransform(
                q1_label,
                q1_double
            ),
            ReplacementTransform(
                force_arrows,
                stronger_force
            ),
            ReplacementTransform(
                force_label,
                force_2f
            ),
            run_time=1.2
        )

        q1_label = q1_double
        force_arrows = stronger_force
        force_label = force_2f

        self.wait(1.0)

        result_2f = VGroup(
            MathTex(
                "F",
                font_size=41,
                color=FORCE_COLOR
            ),
            MathTex(
                "\\rightarrow",
                font_size=37,
                color=TEXT_SECONDARY
            ),
            MathTex(
                "2F",
                font_size=41,
                color=FORCE_COLOR
            )
        ).arrange(
            RIGHT,
            buff=0.18
        ).move_to(
            DOWN * 2.75
        )

        self.play(
            FadeIn(result_2f),
            run_time=0.7
        )

        self.wait(1.4)

        direct_relation = arabic_text(
            "مضاعفة إحدى الشحنتين → مضاعفة القوة",
            size=30,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            UP * 2.15
        )

        self.play(
            FadeIn(direct_relation),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 10 — RESET TO ORIGINAL
        # ====================================================

        self.play(
            FadeOut(change_q1),
            FadeOut(result_2f),
            FadeOut(direct_relation),
            run_time=0.5
        )

        original_q1 = MathTex(
            "q_1",
            font_size=46,
            color=POSITIVE
        ).move_to(
            q1_label
        )

        original_force = make_force_arrows(
            base_left,
            base_right,
            length=0.70,
            stroke_width=5
        )

        original_f = MathTex(
            "F",
            font_size=52,
            color=FORCE_COLOR
        ).move_to(
            force_label
        )

        self.play(
            ReplacementTransform(
                q1_label,
                original_q1
            ),
            ReplacementTransform(
                force_arrows,
                original_force
            ),
            ReplacementTransform(
                force_label,
                original_f
            ),
            run_time=1.0
        )

        q1_label = original_q1
        force_arrows = original_force
        force_label = original_f

        self.wait(0.8)

        # ====================================================
        # PART 11 — DOUBLE BOTH CHARGES
        # ====================================================

        both_title = arabic_text(
            "والآن نضاعف الشحنتين معًا",
            size=34,
            weight=BOLD
        ).move_to(
            UP * 2.20
        )

        self.play(
            FadeIn(both_title),
            run_time=0.8
        )

        self.wait(0.8)

        q1_double_both = MathTex(
            "2q_1",
            font_size=48,
            color=POSITIVE
        ).move_to(
            q1_label
        )

        q2_double_both = MathTex(
            "2q_2",
            font_size=48,
            color=NEGATIVE
        ).move_to(
            q2_label
        )

        self.play(
            ReplacementTransform(
                q1_label,
                q1_double_both
            ),
            ReplacementTransform(
                q2_label,
                q2_double_both
            ),
            run_time=0.9
        )

        q1_label = q1_double_both
        q2_label = q2_double_both

        self.wait(0.8)

        factor_1 = VGroup(
            MathTex(
                "q_1\\rightarrow2q_1",
                font_size=38,
                color=POSITIVE
            ),
            MathTex(
                "\\Rightarrow",
                font_size=36,
                color=TEXT_SECONDARY
            ),
            MathTex(
                "\\times2",
                font_size=38,
                color=FORCE_COLOR
            )
        ).arrange(
            RIGHT,
            buff=0.25
        ).move_to(
            UP * 1.20
        )

        factor_2 = VGroup(
            MathTex(
                "q_2\\rightarrow2q_2",
                font_size=38,
                color=NEGATIVE
            ),
            MathTex(
                "\\Rightarrow",
                font_size=36,
                color=TEXT_SECONDARY
            ),
            MathTex(
                "\\times2",
                font_size=38,
                color=FORCE_COLOR
            )
        ).arrange(
            RIGHT,
            buff=0.25
        ).move_to(
            UP * 0.55
        )

        self.play(
            FadeIn(factor_1),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(factor_2),
            run_time=0.7
        )

        self.wait(0.8)

        multiplication = MathTex(
            "2\\times2=4",
            font_size=56,
            color=ACCENT
        ).move_to(
            DOWN * 1.20
        )

        self.play(
            FadeIn(multiplication),
            run_time=0.8
        )

        self.wait(0.9)

        force_4 = make_force_arrows(
            base_left,
            base_right,
            length=1.42,
            stroke_width=9
        )

        force_4f = MathTex(
            "4F",
            font_size=58,
            color=FORCE_COLOR
        ).move_to(
            force_label
        )

        self.play(
            ReplacementTransform(
                force_arrows,
                force_4
            ),
            ReplacementTransform(
                force_label,
                force_4f
            ),
            run_time=1.2
        )

        force_arrows = force_4
        force_label = force_4f

        self.wait(1.4)

        # ====================================================
        # PART 12 — CLEAR THE EXPERIMENT
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    positive_charge,
                    negative_charge,
                    q1_label,
                    q2_label,
                    force_arrows,
                    force_label,
                    fixed_distance_marker,
                    fixed_distance_text,
                    charge_test_title,
                    both_title,
                    factor_1,
                    factor_2,
                    multiplication
                )
            ),
            run_time=0.8
        )

        # ====================================================
        # PART 13 — BUILD FINAL RELATION
        # ====================================================

        pattern_title = arabic_text(
            "الآن أصبح النمط واضحًا",
            size=39,
            weight=BOLD
        ).shift(
            UP * 1.65
        )

        self.play(
            FadeIn(pattern_title),
            run_time=0.8
        )

        self.wait(0.8)

        product_text = arabic_text(
            "القوة تعتمد على حاصل ضرب مقداري الشحنتين",
            size=32,
            weight=BOLD
        ).next_to(
            pattern_title,
            DOWN,
            buff=0.40
        )

        self.play(
            FadeIn(product_text),
            run_time=0.8
        )

        self.wait(1.0)

        final_relation = MathTex(
            "F\\propto |q_1q_2|",
            font_size=72,
            color=ACCENT
        ).next_to(
            product_text,
            DOWN,
            buff=0.55
        )

        self.play(
            FadeIn(
                final_relation,
                scale=0.85
            ),
            run_time=0.9
        )

        self.wait(1.5)

        conclusion = arabic_text(
            "كلما زاد مقدار الشحنتين، زاد مقدار القوة الكهربائية",
            size=30,
            color=TEXT_SECONDARY
        ).next_to(
            final_relation,
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(conclusion),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 14 — TRANSITION TO DISTANCE LAW
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    pattern_title,
                    product_text,
                    final_relation,
                    conclusion
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "عرفنا الآن كيف تعتمد القوة على مقدار الشحنات",
            size=34
        ).shift(
            UP * 0.70
        )

        transition_2 = arabic_text(
            "لكننا رأينا أيضًا أن المسافة تؤثر في القوة",
            size=34
        ).next_to(
            transition_1,
            DOWN,
            buff=0.28
        )

        transition_3 = arabic_text(
            "فما العلاقة الدقيقة بين القوة والمسافة؟",
            size=38,
            weight=BOLD,
            color=DISTANCE_COLOR
        ).next_to(
            transition_2,
            DOWN,
            buff=0.42
        )

        self.play(
            FadeIn(transition_1),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(transition_2),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(transition_3),
            run_time=0.8
        )

        self.wait(2.0)

        self.play(
            FadeOut(
                VGroup(
                    transition_1,
                    transition_2,
                    transition_3
                )
            ),
            run_time=0.8
        )


# ============================================================
# DIRECT RENDERING FROM PYCHARM
# ============================================================

if __name__ == "__main__":

    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    config.output_file = "scene_17_electric_force_charge_magnitude"

    config.preview = True
    config.quality = "high_quality"

    Scene17ElectricForceAndChargeMagnitude().render()