from manim import *
import numpy as np


# ============================================================
# Scene 23
# المجال الكهربائي
#
# التسلسل:
#
# 1. شحنة مصدر +Q.
# 2. نقطة P في الفضاء.
# 3. نضع عندها شحنة اختبار موجبة صغيرة q.
# 4. تظهر القوة F على شحنة الاختبار.
# 5. نبني:
#
#       E = F / q
#
# 6. نزيل شحنة الاختبار، ونُبقي سهم E عند النقطة.
#
# 7. نعرض اتجاه المجال حول +Q
#    باستخدام 12 سهمًا شعاعيًا موزعة بانتظام.
#
# 8. نستبدل +Q بـ -Q
#    فتنعكس الأسهم وتتجه نحو الشحنة.
#
# 9. نعود لشحنة نقطية Q ونبني:
#
#       E = k |Q| / r^2
#
# ثم نُظهر أن مقدار المجال يضعف مع المسافة.
# ============================================================


class Scene23ElectricField(Scene):

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

        ACCENT = "#7EE787"
        FIELD_COLOR = "#7EE787"
        FORCE_COLOR = "#FFD166"
        POINT_COLOR = "#B7C0CC"

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

        def make_source_charge(
            center,
            sign="+",
            radius=0.58
        ):

            color = POSITIVE if sign == "+" else NEGATIVE

            circle = Circle(
                radius=radius,
                stroke_width=4,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.14
            ).move_to(center)

            sign_text = Text(
                sign,
                font_size=48,
                weight=BOLD,
                color=color
            ).move_to(circle)

            return VGroup(
                circle,
                sign_text
            )

        def make_test_charge(center):

            circle = Circle(
                radius=0.28,
                stroke_width=3,
                stroke_color=POSITIVE,
                fill_color=POSITIVE,
                fill_opacity=0.13
            ).move_to(center)

            plus = Text(
                "+",
                font_size=29,
                weight=BOLD,
                color=POSITIVE
            ).move_to(circle)

            return VGroup(
                circle,
                plus
            )

        def make_point(
            position,
            radius=0.055
        ):

            return Dot(
                point=position,
                radius=radius,
                color=POINT_COLOR
            )

        def make_field_arrow(
            point,
            source_center=ORIGIN,
            positive_source=True,
            length=0.75,
            stroke_width=5
        ):

            radial_vector = point - source_center

            if np.linalg.norm(radial_vector) == 0:
                radial_vector = RIGHT

            radial_unit = radial_vector / np.linalg.norm(radial_vector)

            if positive_source:
                direction = radial_unit
            else:
                direction = -radial_unit

            return Arrow(
                start=point,
                end=point + direction * length,
                buff=0,
                stroke_width=stroke_width,
                color=FIELD_COLOR,
                max_tip_length_to_length_ratio=0.22
            )

        def make_radial_field(
            center,
            positive_source=True,
            number_of_arrows=12,
            inner_radius=0.82,
            outer_radius=2.05
        ):
            """
            رسم شعاعي كثيف ومنتظم مثل النموذج المرجعي.

            +Q:
            الأسهم تبدأ قرب الشحنة وتتجه إلى الخارج.

            -Q:
            الأسهم تبدأ من الخارج وتتجه نحو الشحنة.
            """

            arrows = VGroup()

            for i in range(number_of_arrows):

                angle = TAU * i / number_of_arrows

                direction = np.array([
                    np.cos(angle),
                    np.sin(angle),
                    0
                ])

                inner_point = center + direction * inner_radius
                outer_point = center + direction * outer_radius

                if positive_source:
                    start = inner_point
                    end = outer_point
                else:
                    start = outer_point
                    end = inner_point

                arrow = Arrow(
                    start=start,
                    end=end,
                    buff=0,
                    stroke_width=5,
                    color=FIELD_COLOR,
                    max_tip_length_to_length_ratio=0.16
                )

                arrows.add(arrow)

            return arrows

        # ====================================================
        # PART 1 — INTRODUCTION
        # ====================================================

        title = arabic_text(
            "المجال الكهربائي",
            size=44,
            weight=BOLD,
            color=ACCENT
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.15
            ),
            run_time=0.9
        )

        self.wait(1.0)

        intro = arabic_text(
            "يمكننا وصف تأثير الشحنة الكهربائية في كل نقطة حولها",
            size=32
        ).next_to(
            title,
            DOWN,
            buff=0.38
        )

        self.play(
            FadeIn(intro),
            run_time=0.8
        )

        self.wait(1.4)

        self.play(
            FadeOut(intro),
            title.animate.to_edge(
                UP,
                buff=0.42
            ).scale(0.84),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — SOURCE CHARGE
        # ====================================================

        source_center = LEFT * 2.5 + DOWN * 0.25

        source_charge = make_source_charge(
            source_center,
            "+"
        )

        source_label = VGroup(
            arabic_text(
                "شحنة المصدر",
                size=27,
                color=TEXT_SECONDARY
            ),
            MathTex(
                "+Q",
                font_size=42,
                color=POSITIVE
            )
        ).arrange(
            DOWN,
            buff=0.10
        ).next_to(
            source_charge,
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(
                source_charge,
                scale=0.8
            ),
            FadeIn(source_label),
            run_time=0.9
        )

        self.wait(1.0)

        # ====================================================
        # PART 3 — SELECT A POINT
        # ====================================================

        point_position = RIGHT * 2.2 + DOWN * 0.25

        point_p = make_point(
            point_position,
            radius=0.07
        )

        point_label = MathTex(
            "q",
            font_size=38,
            color=TEXT_MAIN
        ).next_to(
            point_p,
            UP,
            buff=0.18
        )

        point_text = arabic_text(
            "نريد معرفة المجال عند هذه النقطة",
            size=30,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(point_p, scale=1.5),
            FadeIn(point_label),
            run_time=0.7
        )

        self.play(
            FadeIn(point_text),
            run_time=0.7
        )

        self.wait(1.2)

        # ====================================================
        # PART 4 — TEST CHARGE
        # ====================================================

        self.play(
            FadeOut(point_text),
            run_time=0.4
        )

        test_text = arabic_text(
            "نضع شحنة اختبار موجبة صغيرة جدًا",
            size=31,
            weight=BOLD,
            color=POSITIVE
        ).move_to(
            UP * 2.15
        )

        self.play(
            FadeIn(test_text),
            run_time=0.7
        )

        test_charge = make_test_charge(
            point_position
        )

        test_q_label = MathTex(
            "q>0",
            font_size=38,
            color=POSITIVE
        ).next_to(
            test_charge,
            DOWN,
            buff=0.22
        )

        self.play(
            FadeOut(point_p),
            FadeIn(
                test_charge,
                scale=0.7
            ),
            FadeIn(test_q_label),
            run_time=0.8
        )

        self.wait(1.0)

        small_note = arabic_text(
            "صغيرة بحيث لا تغيّر توزيع الشحنات بشكل ملحوظ",
            size=26,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(small_note),
            run_time=0.7
        )

        self.wait(1.3)

        # ====================================================
        # PART 5 — FORCE ON TEST CHARGE
        # ====================================================

        self.play(
            FadeOut(small_note),
            FadeOut(test_text),
            run_time=0.5
        )

        force_arrow = Arrow(
            start=point_position + RIGHT * 0.35,
            end=point_position + RIGHT * 1.70,
            buff=0,
            stroke_width=7,
            color=FORCE_COLOR,
            max_tip_length_to_length_ratio=0.16
        )

        force_label = MathTex(
            r"\vec{F}",
            font_size=45,
            color=FORCE_COLOR
        ).next_to(
            force_arrow,
            UP,
            buff=0.12
        )

        force_text = arabic_text(
            "المجال يؤثر في شحنة الاختبار بقوة",
            size=31,
            color=FORCE_COLOR
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            GrowArrow(force_arrow),
            FadeIn(force_label),
            run_time=0.8
        )

        self.play(
            FadeIn(force_text),
            run_time=0.7
        )

        self.wait(1.3)

        # ====================================================
        # PART 6 — DEFINE E
        # ====================================================

        self.play(
            FadeOut(force_text),
            run_time=0.4
        )

        definition_intro = arabic_text(
            "مقدار المجال عند النقطة",
            size=31,
            weight=BOLD
        ).move_to(
            UP * 2.05
        )

        self.play(
            FadeIn(definition_intro),
            run_time=0.7
        )

        field_equation = MathTex(
            r"E=\frac{F}{q}",
            font_size=72,
            color=ACCENT
        ).move_to(
            DOWN * 2.25
        )

        self.play(
            FadeIn(
                field_equation,
                scale=0.85
            ),
            run_time=0.9
        )

        self.wait(1.4)

        meaning_text = arabic_text(
            "القوة لكل وحدة شحنة موجبة اختبارية",
            size=29,
            color=TEXT_SECONDARY
        ).next_to(
            field_equation,
            UP,
            buff=0.30
        )

        self.play(
            FadeIn(meaning_text),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 7 — DIRECTION OF E
        # ====================================================

        self.play(
            FadeOut(definition_intro),
            FadeOut(meaning_text),
            run_time=0.5
        )

        direction_text = arabic_text(
            "اتجاه المجال = اتجاه القوة على شحنة اختبار موجبة",
            size=30,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            UP * 2.05
        )

        self.play(
            FadeIn(direction_text),
            run_time=0.7
        )

        field_arrow_single = Arrow(
            start=point_position,
            end=point_position + RIGHT * 1.35,
            buff=0,
            stroke_width=7,
            color=FIELD_COLOR,
            max_tip_length_to_length_ratio=0.17
        )

        field_label_single = MathTex(
            r"\vec{E}",
            font_size=46,
            color=FIELD_COLOR
        ).next_to(
            field_arrow_single,
            UP,
            buff=0.12
        )

        self.play(
            FadeOut(force_arrow),
            FadeOut(force_label),
            GrowArrow(field_arrow_single),
            FadeIn(field_label_single),
            run_time=0.9
        )

        self.wait(1.1)

        # ====================================================
        # PART 8 — REMOVE TEST CHARGE
        # ====================================================

        remove_test_text = arabic_text(
            "والآن نزيل شحنة الاختبار",
            size=29,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.34
        )

        self.play(
            FadeOut(field_equation),
            FadeIn(remove_test_text),
            run_time=0.7
        )

        self.wait(0.7)

        self.play(
            FadeOut(test_charge),
            FadeOut(test_q_label),
            run_time=0.8
        )

        self.wait(0.7)

        field_remains_text = arabic_text(
            "ويبقى المجال موصوفًا عند هذه النقطة",
            size=30,
            weight=BOLD,
            color=FIELD_COLOR
        ).to_edge(
            DOWN,
            buff=0.34
        )

        self.play(
            ReplacementTransform(
                remove_test_text,
                field_remains_text
            ),
            run_time=0.7
        )

        point_p_again = make_point(
            point_position,
            radius=0.06
        )

        self.play(
            FadeIn(point_p_again),
            run_time=0.5
        )

        self.wait(1.4)

        # ====================================================
        # PART 9 — RADIAL FIELD AROUND +Q
        # ====================================================

        self.play(
            FadeOut(direction_text),
            FadeOut(field_remains_text),
            FadeOut(field_arrow_single),
            FadeOut(field_label_single),
            FadeOut(point_p_again),
            FadeOut(point_label),
            FadeOut(source_label),
            source_charge.animate.move_to(ORIGIN),
            run_time=0.8
        )

        source_center = ORIGIN

        field_space_text = arabic_text(
            "حول الشحنة الموجبة يتجه المجال إلى الخارج",
            size=32,
            weight=BOLD,
            color=POSITIVE
        ).to_edge(
            UP,
            buff=0.48
        )

        self.play(
            Transform(
                title,
                field_space_text
            ),
            run_time=0.7
        )

        # ----------------------------------------------------
        # 12 evenly spaced radial arrows
        # ----------------------------------------------------

        positive_field = make_radial_field(
            center=ORIGIN,
            positive_source=True,
            number_of_arrows=18,
            inner_radius=0.82,
            outer_radius=2.15
        )

        # Grow them progressively around the charge
        self.play(
            LaggedStart(
                *[
                    GrowArrow(arrow)
                    for arrow in positive_field
                ],
                lag_ratio=0.055
            ),
            run_time=1.6
        )

        self.wait(1.6)

        # ====================================================
        # PART 10 — RADIAL FIELD AROUND -Q
        # ====================================================

        negative_source = make_source_charge(
            ORIGIN,
            "−"
        )

        negative_field = make_radial_field(
            center=ORIGIN,
            positive_source=False,
            number_of_arrows=18,
            inner_radius=0.82,
            outer_radius=2.15
        )

        inward_text = arabic_text(
            "حول الشحنة السالبة يتجه المجال نحو الشحنة",
            size=32,
            weight=BOLD,
            color=NEGATIVE
        ).to_edge(
            UP,
            buff=0.48
        )

        self.play(
            ReplacementTransform(
                source_charge,
                negative_source
            ),
            ReplacementTransform(
                positive_field,
                negative_field
            ),
            ReplacementTransform(
                title,
                inward_text
            ),
            run_time=1.3
        )

        source_charge = negative_source
        title = inward_text

        self.wait(1.7)

        # ====================================================
        # PART 11 — CLEAR RADIAL FIELD
        # ====================================================

        self.play(
            FadeOut(negative_field),
            FadeOut(title),
            run_time=0.7
        )

        # ====================================================
        # PART 12 — RETURN TO POSITIVE POINT CHARGE
        # ====================================================

        positive_source_again = make_source_charge(
            LEFT * 3.0 + DOWN * 0.15,
            "+"
        )

        self.play(
            ReplacementTransform(
                source_charge,
                positive_source_again
            ),
            run_time=0.7
        )

        source_charge = positive_source_again
        source_center = source_charge.get_center()

        source_q_label = MathTex(
            "Q",
            font_size=44,
            color=POSITIVE
        ).next_to(
            source_charge,
            DOWN,
            buff=0.28
        )

        equation_title = arabic_text(
            "مقدار المجال لشحنة نقطية",
            size=34,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.48
        )

        self.play(
            FadeIn(source_q_label),
            FadeIn(equation_title),
            run_time=0.7
        )

        # ====================================================
        # PART 13 — FIELD AT DISTANCE r
        # ====================================================

        point_r = RIGHT * 1.55 + DOWN * 0.15

        point_dot = make_point(
            point_r,
            radius=0.07
        )

        point_label_r = MathTex(
            "P",
            font_size=38,
            color=TEXT_MAIN
        ).next_to(
            point_dot,
            UP,
            buff=0.15
        )

        self.play(
            FadeIn(point_dot),
            FadeIn(point_label_r),
            run_time=0.6
        )

        distance_line = DoubleArrow(
            start=source_center + RIGHT * 0.65 + UP * 1.0,
            end=point_r + UP * 1.0,
            buff=0.05,
            stroke_width=3,
            color=TEXT_SECONDARY,
            max_tip_length_to_length_ratio=0.09
        )

        r_label = MathTex(
            "r",
            font_size=43,
            color=TEXT_SECONDARY
        ).next_to(
            distance_line,
            UP,
            buff=0.08
        )

        self.play(
            GrowFromCenter(distance_line),
            FadeIn(r_label),
            run_time=0.7
        )

        selected_field_arrow = make_field_arrow(
            point=point_r,
            source_center=source_center,
            positive_source=True,
            length=1.15,
            stroke_width=7
        )

        selected_e_label = MathTex(
            r"\vec{E}",
            font_size=44,
            color=FIELD_COLOR
        ).next_to(
            selected_field_arrow,
            UP,
            buff=0.10
        )

        self.play(
            GrowArrow(selected_field_arrow),
            FadeIn(selected_e_label),
            run_time=0.8
        )

        self.wait(0.8)

        # ====================================================
        # PART 14 — POINT CHARGE FIELD EQUATION
        # ====================================================

        point_field_equation = MathTex(
            r"E=k\frac{|Q|}{r^2}",
            font_size=72,
            color=ACCENT
        ).move_to(
            DOWN * 2.10
        )

        self.play(
            FadeIn(
                point_field_equation,
                scale=0.85
            ),
            run_time=0.9
        )

        self.wait(1.5)

        # ====================================================
        # PART 15 — MOVE POINT FARTHER AWAY
        # ====================================================

        inverse_square_text = arabic_text(
            "كلما ابتعدنا عن الشحنة، يضعف المجال",
            size=30,
            color=TEXT_SECONDARY
        ).next_to(
            point_field_equation,
            UP,
            buff=0.30
        )

        self.play(
            FadeIn(inverse_square_text),
            run_time=0.7
        )

        self.wait(0.7)

        farther_point = RIGHT * 3.25 + DOWN * 0.15

        farther_dot = make_point(
            farther_point,
            radius=0.07
        )

        farther_label = MathTex(
            "P",
            font_size=38,
            color=TEXT_MAIN
        ).next_to(
            farther_dot,
            UP,
            buff=0.15
        )

        farther_distance = DoubleArrow(
            start=source_center + RIGHT * 0.65 + UP * 1.0,
            end=farther_point + UP * 1.0,
            buff=0.05,
            stroke_width=3,
            color=TEXT_SECONDARY,
            max_tip_length_to_length_ratio=0.07
        )

        farther_r = MathTex(
            "r",
            font_size=43,
            color=TEXT_SECONDARY
        ).next_to(
            farther_distance,
            UP,
            buff=0.08
        )

        farther_field_arrow = make_field_arrow(
            point=farther_point,
            source_center=source_center,
            positive_source=True,
            length=0.48,
            stroke_width=4
        )

        farther_e_label = MathTex(
            r"\vec{E}",
            font_size=40,
            color=FIELD_COLOR
        ).next_to(
            farther_field_arrow,
            UP,
            buff=0.10
        )

        self.play(
            ReplacementTransform(
                point_dot,
                farther_dot
            ),
            ReplacementTransform(
                point_label_r,
                farther_label
            ),
            ReplacementTransform(
                distance_line,
                farther_distance
            ),
            ReplacementTransform(
                r_label,
                farther_r
            ),
            ReplacementTransform(
                selected_field_arrow,
                farther_field_arrow
            ),
            ReplacementTransform(
                selected_e_label,
                farther_e_label
            ),
            run_time=1.6,
            rate_func=smooth
        )

        self.wait(1.3)

        square_note = arabic_text(
            "وفق علاقة التربيع العكسي",
            size=31,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            inverse_square_text,
            DOWN,
            buff=0.20
        )

        self.play(
            FadeIn(square_note),
            run_time=0.7
        )

        self.wait(1.7)

        # ====================================================
        # PART 16 — END
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    equation_title,
                    source_charge,
                    source_q_label,
                    farther_dot,
                    farther_label,
                    farther_distance,
                    farther_r,
                    farther_field_arrow,
                    farther_e_label,
                    inverse_square_text,
                    square_note,
                    point_field_equation
                )
            ),
            run_time=0.9
        )


# ============================================================
# DIRECT RENDERING FROM PYCHARM
# ============================================================

if __name__ == "__main__":

    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    config.output_file = "scene_20_electric_field"

    config.preview = True
    config.quality = "high_quality"

    Scene23ElectricField().render()