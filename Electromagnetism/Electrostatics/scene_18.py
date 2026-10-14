from manim import *


# ============================================================
# Scene 18
# تأثير المسافة + بناء قانون كولوم
#
# التسلسل:
#
# الحالة المرجعية:
#       المسافة r
#       القوة F
#
# نضاعف المسافة:
#       r -> 2r
#       F -> F/4
#
# نقلل المسافة إلى النصف:
#       r -> r/2
#       F -> 4F
#
# نستنتج:
#       F ∝ 1/r^2
#
# ومن المشهد السابق:
#       F ∝ |q1 q2|
#
# نجمع العلاقتين:
#       F ∝ |q1 q2| / r^2
#
# نضيف ثابت التناسب k:
#       F = k |q1 q2| / r^2
#
# وهذا هو قانون كولوم.
# ============================================================


class Scene18DistanceAndCoulomb(Scene):

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

        DISTANCE_COLOR = "#FFD166"
        FORCE_COLOR = "#7EE787"

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
                radius=0.48,
                stroke_width=4,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.13
            ).move_to(center)

            sign_text = Text(
                sign,
                font_size=42,
                weight=BOLD,
                color=color
            ).move_to(circle)

            return VGroup(
                circle,
                sign_text
            )

        def make_force_pair(
            left_center,
            right_center,
            length=0.60,
            stroke_width=5
        ):

            left_start = left_center + RIGHT * 0.57

            left_arrow = Arrow(
                start=left_start,
                end=left_start + RIGHT * length,
                buff=0,
                stroke_width=stroke_width,
                color=FORCE_COLOR,
                max_tip_length_to_length_ratio=0.18
            )

            right_start = right_center + LEFT * 0.57

            right_arrow = Arrow(
                start=right_start,
                end=right_start + LEFT * length,
                buff=0,
                stroke_width=stroke_width,
                color=FORCE_COLOR,
                max_tip_length_to_length_ratio=0.18
            )

            return VGroup(
                left_arrow,
                right_arrow
            )

        def make_distance_marker(
            left_center,
            right_center,
            label_tex
        ):

            y = 1.20

            left_point = np.array([
                left_center[0],
                y,
                0
            ])

            right_point = np.array([
                right_center[0],
                y,
                0
            ])

            left_guide = DashedLine(
                left_center + UP * 0.55,
                left_point,
                dash_length=0.08,
                stroke_width=2,
                color=TEXT_SECONDARY
            )

            right_guide = DashedLine(
                right_center + UP * 0.55,
                right_point,
                dash_length=0.08,
                stroke_width=2,
                color=TEXT_SECONDARY
            )

            arrow = DoubleArrow(
                start=left_point,
                end=right_point,
                buff=0.05,
                stroke_width=3,
                color=DISTANCE_COLOR,
                max_tip_length_to_length_ratio=0.08
            )

            label = MathTex(
                label_tex,
                font_size=44,
                color=DISTANCE_COLOR
            ).next_to(
                arrow,
                UP,
                buff=0.08
            )

            return VGroup(
                left_guide,
                right_guide,
                arrow,
                label
            )

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "كيف تؤثر المسافة في القوة؟",
            size=43,
            weight=BOLD
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.15
            ),
            run_time=0.9
        )

        self.wait(1.2)

        fixed_text = arabic_text(
            "نُبقي مقدار الشحنتين ثابتًا",
            size=33,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            title,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(fixed_text),
            run_time=0.7
        )

        self.wait(1.2)

        self.play(
            FadeOut(fixed_text),
            title.animate.to_edge(
                UP,
                buff=0.42
            ).scale(0.85),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — REFERENCE CASE
        # ====================================================

        base_left = LEFT * 2.30 + DOWN * 0.35
        base_right = RIGHT * 2.30 + DOWN * 0.35

        charge_1 = make_charge(
            base_left,
            "+"
        )

        charge_2 = make_charge(
            base_right,
            "−"
        )

        self.play(
            FadeIn(charge_1, scale=0.8),
            FadeIn(charge_2, scale=0.8),
            run_time=0.8
        )

        q1_label = MathTex(
            "q_1",
            font_size=44,
            color=POSITIVE
        ).move_to(
            base_left + DOWN * 0.85
        )

        q2_label = MathTex(
            "q_2",
            font_size=44,
            color=NEGATIVE
        ).move_to(
            base_right + DOWN * 0.85
        )

        self.play(
            FadeIn(q1_label),
            FadeIn(q2_label),
            run_time=0.7
        )

        distance_marker = make_distance_marker(
            base_left,
            base_right,
            "r"
        )

        self.play(
            FadeIn(distance_marker),
            run_time=0.8
        )

        base_force = make_force_pair(
            base_left,
            base_right,
            length=0.58,
            stroke_width=5
        )

        force_label = MathTex(
            "F",
            font_size=52,
            color=FORCE_COLOR
        ).move_to(
            DOWN * 2.20
        )

        self.play(
            GrowArrow(base_force[0]),
            GrowArrow(base_force[1]),
            FadeIn(force_label),
            run_time=0.8
        )

        self.wait(1.3)

        # ====================================================
        # PART 3 — DOUBLE THE DISTANCE
        # ====================================================

        double_text = arabic_text(
            "نضاعف المسافة",
            size=34,
            weight=BOLD,
            color=DISTANCE_COLOR
        ).move_to(
            UP * 2.25
        )

        self.play(
            FadeIn(double_text),
            run_time=0.7
        )

        self.wait(0.6)

        far_left = LEFT * 4.60 + DOWN * 0.35
        far_right = RIGHT * 4.60 + DOWN * 0.35

        distance_2r = make_distance_marker(
            far_left,
            far_right,
            "2r"
        )

        weak_force = make_force_pair(
            far_left,
            far_right,
            length=0.24,
            stroke_width=3
        )

        force_quarter = MathTex(
            r"\frac{F}{4}",
            font_size=52,
            color=FORCE_COLOR
        ).move_to(
            force_label
        )

        self.play(
            charge_1.animate.move_to(far_left),
            charge_2.animate.move_to(far_right),

            q1_label.animate.move_to(
                far_left + DOWN * 0.85
            ),
            q2_label.animate.move_to(
                far_right + DOWN * 0.85
            ),

            ReplacementTransform(
                distance_marker,
                distance_2r
            ),

            ReplacementTransform(
                base_force,
                weak_force
            ),

            ReplacementTransform(
                force_label,
                force_quarter
            ),

            run_time=1.5,
            rate_func=smooth
        )

        distance_marker = distance_2r
        force_arrows = weak_force
        force_label = force_quarter

        self.wait(1.0)

        double_relation = VGroup(
            MathTex(
                "r",
                font_size=42,
                color=DISTANCE_COLOR
            ),
            MathTex(
                "\\rightarrow",
                font_size=38,
                color=TEXT_SECONDARY
            ),
            MathTex(
                "2r",
                font_size=42,
                color=DISTANCE_COLOR
            ),
            MathTex(
                "\\Rightarrow",
                font_size=38,
                color=TEXT_SECONDARY
            ),
            MathTex(
                "F",
                font_size=42,
                color=FORCE_COLOR
            ),
            MathTex(
                "\\rightarrow",
                font_size=38,
                color=TEXT_SECONDARY
            ),
            MathTex(
                r"\frac{F}{4}",
                font_size=42,
                color=FORCE_COLOR
            )
        ).arrange(
            RIGHT,
            buff=0.16
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(double_relation),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 4 — HALF THE ORIGINAL DISTANCE
        # ====================================================

        self.play(
            FadeOut(double_text),
            FadeOut(double_relation),
            run_time=0.5
        )

        half_text = arabic_text(
            "والآن نجعل المسافة نصف قيمتها الأصلية",
            size=33,
            weight=BOLD,
            color=DISTANCE_COLOR
        ).move_to(
            UP * 2.25
        )

        self.play(
            FadeIn(half_text),
            run_time=0.7
        )

        self.wait(0.7)

        half_left = LEFT * 1.15 + DOWN * 0.35
        half_right = RIGHT * 1.15 + DOWN * 0.35

        distance_half = make_distance_marker(
            half_left,
            half_right,
            r"\frac{r}{2}"
        )

        strong_force = make_force_pair(
            half_left,
            half_right,
            length=0.50,
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
            charge_1.animate.move_to(half_left),
            charge_2.animate.move_to(half_right),

            q1_label.animate.move_to(
                half_left + DOWN * 0.85
            ),
            q2_label.animate.move_to(
                half_right + DOWN * 0.85
            ),

            ReplacementTransform(
                distance_marker,
                distance_half
            ),

            ReplacementTransform(
                force_arrows,
                strong_force
            ),

            ReplacementTransform(
                force_label,
                force_4f
            ),

            run_time=1.5,
            rate_func=smooth
        )

        distance_marker = distance_half
        force_arrows = strong_force
        force_label = force_4f

        self.wait(1.0)

        half_relation = VGroup(
            MathTex(
                "r",
                font_size=42,
                color=DISTANCE_COLOR
            ),
            MathTex(
                "\\rightarrow",
                font_size=38,
                color=TEXT_SECONDARY
            ),
            MathTex(
                r"\frac{r}{2}",
                font_size=42,
                color=DISTANCE_COLOR
            ),
            MathTex(
                "\\Rightarrow",
                font_size=38,
                color=TEXT_SECONDARY
            ),
            MathTex(
                "F",
                font_size=42,
                color=FORCE_COLOR
            ),
            MathTex(
                "\\rightarrow",
                font_size=38,
                color=TEXT_SECONDARY
            ),
            MathTex(
                "4F",
                font_size=42,
                color=FORCE_COLOR
            )
        ).arrange(
            RIGHT,
            buff=0.16
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(half_relation),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 5 — INVERSE SQUARE
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    charge_1,
                    charge_2,
                    q1_label,
                    q2_label,
                    distance_marker,
                    force_arrows,
                    force_label,
                    half_text,
                    half_relation,
                    title
                )
            ),
            run_time=0.8
        )

        pattern_title = arabic_text(
            "إذن القوة تعتمد على مربع المسافة",
            size=37,
            weight=BOLD
        ).shift(
            UP * 1.20
        )

        inverse_text = arabic_text(
            "وبصورة عكسية",
            size=32,
            color=TEXT_SECONDARY
        ).next_to(
            pattern_title,
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(pattern_title),
            run_time=0.8
        )

        self.play(
            FadeIn(inverse_text),
            run_time=0.6
        )

        self.wait(0.8)

        distance_relation = MathTex(
            r"F\propto\frac{1}{r^2}",
            font_size=76,
            color=ACCENT
        ).next_to(
            inverse_text,
            DOWN,
            buff=0.40
        )

        self.play(
            FadeIn(
                distance_relation,
                scale=0.85
            ),
            run_time=0.9
        )

        self.wait(1.5)

        # ====================================================
        # PART 6 — BRING BACK CHARGE RELATION
        # ====================================================

        self.play(
            FadeOut(pattern_title),
            FadeOut(inverse_text),
            distance_relation.animate.move_to(
                RIGHT * 3.0 + UP * 0.55
            ).scale(0.76),
            run_time=0.8
        )

        combine_title = arabic_text(
            "ومن المشهد السابق",
            size=35,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        charge_relation = MathTex(
            r"F\propto |q_1q_2|",
            font_size=58,
            color=POSITIVE
        ).move_to(
            LEFT * 3.0 + UP * 0.55
        )

        self.play(
            FadeIn(combine_title),
            FadeIn(charge_relation),
            run_time=0.8
        )

        self.wait(1.2)

        # ====================================================
        # PART 7 — COMBINE
        # ====================================================

        combine_arrow_1 = Arrow(
            start=charge_relation.get_bottom(),
            end=DOWN * 0.50 + LEFT * 0.55,
            buff=0.15,
            stroke_width=3,
            color=TEXT_SECONDARY
        )

        combine_arrow_2 = Arrow(
            start=distance_relation.get_bottom(),
            end=DOWN * 0.50 + RIGHT * 0.55,
            buff=0.15,
            stroke_width=3,
            color=TEXT_SECONDARY
        )

        self.play(
            GrowArrow(combine_arrow_1),
            GrowArrow(combine_arrow_2),
            run_time=0.7
        )

        combined_relation = MathTex(
            r"F\propto\frac{|q_1q_2|}{r^2}",
            font_size=70,
            color=ACCENT
        ).move_to(
            DOWN * 1.15
        )

        self.play(
            FadeIn(
                combined_relation,
                scale=0.85
            ),
            run_time=0.9
        )

        self.wait(1.5)

        # ====================================================
        # PART 8 — INTRODUCE k
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    combine_title,
                    charge_relation,
                    distance_relation,
                    combine_arrow_1,
                    combine_arrow_2
                )
            ),
            combined_relation.animate.move_to(
                UP * 0.55
            ),
            run_time=0.8
        )

        constant_text = arabic_text(
            "نحوّل التناسب إلى معادلة بإضافة ثابت التناسب",
            size=31,
            color=TEXT_SECONDARY
        ).to_edge(
            UP,
            buff=0.48
        )

        self.play(
            FadeIn(constant_text),
            run_time=0.8
        )

        self.wait(0.8)

        k_symbol = MathTex(
            "k",
            font_size=64,
            color=DISTANCE_COLOR
        ).move_to(
            LEFT * 3.5 + UP * 0.55
        )

        self.play(
            FadeIn(
                k_symbol,
                scale=0.8
            ),
            run_time=0.7
        )

        self.wait(0.6)

        coulomb_equation = MathTex(
            r"F=k\frac{|q_1q_2|}{r^2}",
            font_size=78,
            color=TEXT_MAIN
        ).move_to(
            DOWN * 0.50
        )

        coulomb_equation.set_color_by_tex(
            "k",
            DISTANCE_COLOR
        )

        self.play(
            FadeOut(k_symbol),
            ReplacementTransform(
                combined_relation,
                coulomb_equation
            ),
            run_time=1.0
        )

        self.wait(1.5)

        # ====================================================
        # PART 9 — NAME THE LAW
        # ====================================================

        law_title = arabic_text(
            "قانون كولوم",
            size=43,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            coulomb_equation,
            UP,
            buff=0.55
        )

        self.play(
            FadeOut(constant_text),
            FadeIn(law_title),
            run_time=0.8
        )

        self.wait(1.0)

        k_value = MathTex(
            r"k\approx9.0\times10^9\ "
            r"\mathrm{N\,m^2/C^2}",
            font_size=46,
            color=DISTANCE_COLOR
        ).next_to(
            coulomb_equation,
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(k_value),
            run_time=0.8
        )

        self.wait(1.3)

        # ====================================================
        # PART 10 — CONDITIONS
        # ====================================================

        condition = arabic_text(
            "للشحنات النقطية، أو عندما يمكن تقريب الأجسام إليها",
            size=27,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(condition),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 11 — FINAL SUMMARY
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    law_title,
                    coulomb_equation,
                    k_value,
                    condition
                )
            ),
            run_time=0.8
        )

        summary_1 = arabic_text(
            "شحنات أكبر  →  قوة أكبر",
            size=34,
            weight=BOLD,
            color=POSITIVE
        ).shift(
            UP * 0.75
        )

        summary_2 = arabic_text(
            "مسافة أكبر  →  قوة أصغر ",
            size=34,
            weight=BOLD,
            color=DISTANCE_COLOR
        ).next_to(
            summary_1,
            DOWN,
            buff=0.38
        )

        summary_equation = MathTex(
            r"F=k\frac{|q_1q_2|}{r^2}",
            font_size=72,
            color=ACCENT
        ).next_to(
            summary_2,
            DOWN,
            buff=0.55
        )

        self.play(
            FadeIn(summary_1),
            run_time=0.7
        )

        self.play(
            FadeIn(summary_2),
            run_time=0.7
        )

        self.play(
            FadeIn(summary_equation),
            run_time=0.8
        )

        self.wait(1.8)

        # ====================================================
        # END
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    summary_1,
                    summary_2,
                    summary_equation
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

    config.output_file = "scene_18_distance_and_coulomb"

    config.preview = True
    config.quality = "high_quality"

    Scene18DistanceAndCoulomb().render()