from manim import *
import numpy as np


# ============================================================
# Scene 21
# المجال الكهربائي لشحنتين
#
# الحالات:
#
# 1) (+ , +)
#    - المجال يخرج من الشحنتين
#    - بينهما يتعاكس تأثير المجالين
#    - تقريب الشحنة اليمنى
#    - إبعاد الشحنة اليمنى
#
# 2) (- , -)
#    - نفس البنية العامة
#    - لكن اتجاه الأسهم ينعكس نحو الشحنتين
#    - تقريب / إبعاد
#
# 3) (+ , -)
#    - المجال يخرج من الموجب ويتجه نحو السالب
#    - تقريب / إبعاد
#
# لا توجد معادلات جديدة في هذا المشهد.
# التركيز بصري بالكامل على شكل المجال.
# ============================================================


class Scene21TwoChargeFields(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"

        FIELD_COLOR = "#7EE787"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

        # ====================================================
        # FIELD ARROW DENSITY
        #
        # Increase these numbers for a denser field.
        #
        # Example:
        # GRID_X_COUNT = 23
        # GRID_Y_COUNT = 11
        # ====================================================

        GRID_X_COUNT = 25
        GRID_Y_COUNT = 12

        FIELD_X_MIN = -5.2
        FIELD_X_MAX = 5.2

        FIELD_Y_MIN = -2.4
        FIELD_Y_MAX = 2.4

        # ====================================================
        # CHARGE POSITIONS
        # ====================================================

        LEFT_POS = np.array([
            -2.25,
            -0.10,
            0
        ])

        RIGHT_BASE = np.array([
            2.25,
            -0.10,
            0
        ])

        RIGHT_CLOSE = np.array([
            1.05,
            -0.10,
            0
        ])

        RIGHT_FAR = np.array([
            3.55,
            -0.10,
            0
        ])

        # ====================================================
        # TEXT HELPER
        # ====================================================

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
        # CHARGE HELPER
        # ====================================================

        def make_charge(
            center,
            sign="+"
        ):

            color = (
                POSITIVE
                if sign == "+"
                else NEGATIVE
            )

            circle = Circle(
                radius=0.48,
                stroke_width=4,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.16
            ).move_to(center)

            sign_text = Text(
                sign,
                font=arabic_font,
                font_size=44,
                weight=BOLD,
                color=color
            ).move_to(circle)

            return VGroup(
                circle,
                sign_text
            )

        # ====================================================
        # ELECTRIC FIELD CALCULATION
        # ====================================================

        def electric_field_vector(
            point,
            sources
        ):
            """
            المصادر:
            [
                (position, charge_value),
                ...
            ]

            نهمل ثابت كولوم هنا لأننا نحتاج
            فقط الشكل النسبي للمجال.
            """

            total = np.zeros(3)

            for position, charge_value in sources:

                displacement = point - position

                distance = np.linalg.norm(
                    displacement
                )

                if distance < 0.001:
                    continue

                total += (
                    charge_value
                    * displacement
                    / distance ** 3
                )

            return total

        # ====================================================
        # BUILD VECTOR FIELD
        # ====================================================

        def make_vector_field(
            sources
        ):

            field = VGroup()

            x_values = np.linspace(
                FIELD_X_MIN,
                FIELD_X_MAX,
                GRID_X_COUNT
            )

            y_values = np.linspace(
                FIELD_Y_MIN,
                FIELD_Y_MAX,
                GRID_Y_COUNT
            )

            for y in y_values:

                for x in x_values:

                    point = np.array([
                        x,
                        y,
                        0
                    ])

                    # ----------------------------------------
                    # Do not draw arrows inside the charges
                    # ----------------------------------------

                    too_close = False

                    for source_position, _ in sources:

                        if np.linalg.norm(
                            point - source_position
                        ) < 0.70:

                            too_close = True
                            break

                    # ----------------------------------------
                    # Calculate electric field
                    # ----------------------------------------

                    field_vector = electric_field_vector(
                        point,
                        sources
                    )

                    magnitude = np.linalg.norm(
                        field_vector
                    )

                    # ----------------------------------------
                    # Invisible placeholder
                    #
                    # Important:
                    # We keep the same number of objects
                    # so Transform works smoothly when
                    # charges move.
                    # ----------------------------------------

                    if (
                        too_close
                        or magnitude < 0.015
                    ):

                        arrow = Arrow(
                            start=point,
                            end=point + RIGHT * 0.001,
                            buff=0,
                            stroke_width=0.1,
                            color=FIELD_COLOR,
                            max_tip_length_to_length_ratio=0.2
                        )

                        arrow.set_opacity(0)

                        field.add(arrow)

                        continue

                    # ----------------------------------------
                    # Direction
                    # ----------------------------------------

                    direction = (
                        field_vector
                        / magnitude
                    )

                    # ----------------------------------------
                    # Arrow length
                    #
                    # Stronger field = longer arrow.
                    #
                    # Saturating function prevents arrows
                    # near the charges from becoming huge.
                    # ----------------------------------------

                    strength_factor = (
                        magnitude
                        / (magnitude + 0.85)
                    )

                    arrow_length = (
                        0.17
                        + 0.40 * strength_factor
                    )

                    # ----------------------------------------
                    # Opacity also carries some information
                    # about field strength.
                    # ----------------------------------------

                    opacity = (
                        0.48
                        + 0.52
                        * (
                            magnitude
                            / (magnitude + 0.40)
                        )
                    )

                    start = (
                        point
                        - direction
                        * arrow_length
                        * 0.30
                    )

                    end = (
                        point
                        + direction
                        * arrow_length
                        * 0.70
                    )

                    arrow = Arrow(
                        start=start,
                        end=end,
                        buff=0,
                        stroke_width=2.8,
                        color=FIELD_COLOR,
                        max_tip_length_to_length_ratio=0.28
                    )

                    arrow.set_opacity(opacity)

                    field.add(arrow)

            return field

        # ====================================================
        # BOTTOM CAPTION HELPER
        # ====================================================

        def make_caption(
            text,
            color=TEXT_SECONDARY
        ):

            return arabic_text(
                text,
                size=30,
                weight=BOLD,
                color=color
            ).to_edge(
                DOWN,
                buff=0.25
            )

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "ماذا يحدث عندما توجد شحنتان؟",
            size=42,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.42
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.15
            ),
            run_time=0.9
        )

        self.wait(1.0)

        # ====================================================
        # PART 2 — (+ , +)
        # ====================================================

        charge_left = make_charge(
            LEFT_POS,
            "+"
        )

        charge_right = make_charge(
            RIGHT_BASE,
            "+"
        )

        case_pp = arabic_text(
            "شُحنتان موجبتان",
            size=30,
            weight=BOLD,
            color=POSITIVE
        ).next_to(
            title,
            DOWN,
            buff=0.18
        )

        self.play(
            FadeIn(case_pp),
            FadeIn(
                charge_left,
                scale=0.8
            ),
            FadeIn(
                charge_right,
                scale=0.8
            ),
            run_time=0.9
        )

        # ====================================================
        # FIELD FOR (+,+)
        # ====================================================

        field = make_vector_field([
            (LEFT_POS, +1),
            (RIGHT_BASE, +1)
        ])

        self.play(
            LaggedStart(
                *[
                    GrowArrow(arrow)
                    for arrow in field
                ],
                lag_ratio=0.005
            ),
            run_time=1.6
        )

        self.wait(1.2)

        middle_text = make_caption(
            "في المنطقة بينهما يتعاكس اتجاه المجالين"
        )

        self.play(
            FadeIn(middle_text),
            run_time=0.7
        )

        self.wait(1.3)

        # ====================================================
        # (+,+) — MOVE CLOSER
        # ====================================================

        self.play(
            FadeOut(middle_text),
            run_time=0.4
        )

        closer_text = make_caption(
            "نقرّب الشحنتين"
        )

        self.play(
            FadeIn(closer_text),
            run_time=0.6
        )

        field_pp_close = make_vector_field([
            (LEFT_POS, +1),
            (RIGHT_CLOSE, +1)
        ])

        self.play(
            charge_right.animate.move_to(
                RIGHT_CLOSE
            ),
            Transform(
                field,
                field_pp_close
            ),
            run_time=1.8,
            rate_func=smooth
        )

        self.wait(1.2)

        # ====================================================
        # (+,+) — MOVE FARTHER
        # ====================================================

        farther_text = make_caption(
            "نُبعد الشحنتين"
        )

        self.play(
            ReplacementTransform(
                closer_text,
                farther_text
            ),
            run_time=0.5
        )

        field_pp_far = make_vector_field([
            (LEFT_POS, +1),
            (RIGHT_FAR, +1)
        ])

        self.play(
            charge_right.animate.move_to(
                RIGHT_FAR
            ),
            Transform(
                field,
                field_pp_far
            ),
            run_time=1.8,
            rate_func=smooth
        )

        self.wait(1.3)

        # ====================================================
        # PART 3 — CHANGE TO (- , -)
        #
        # First return to normal separation.
        # ====================================================

        field_pp_base = make_vector_field([
            (LEFT_POS, +1),
            (RIGHT_BASE, +1)
        ])

        self.play(
            FadeOut(farther_text),
            charge_right.animate.move_to(
                RIGHT_BASE
            ),
            Transform(
                field,
                field_pp_base
            ),
            run_time=1.2
        )

        self.wait(0.5)

        charge_left_negative = make_charge(
            LEFT_POS,
            "−"
        )

        charge_right_negative = make_charge(
            RIGHT_BASE,
            "−"
        )

        field_nn_base = make_vector_field([
            (LEFT_POS, -1),
            (RIGHT_BASE, -1)
        ])

        case_nn = arabic_text(
            "والآن شُحنتان سالبتان",
            size=30,
            weight=BOLD,
            color=NEGATIVE
        ).next_to(
            title,
            DOWN,
            buff=0.18
        )

        self.play(
            ReplacementTransform(
                case_pp,
                case_nn
            ),
            ReplacementTransform(
                charge_left,
                charge_left_negative
            ),
            ReplacementTransform(
                charge_right,
                charge_right_negative
            ),
            Transform(
                field,
                field_nn_base
            ),
            run_time=1.3
        )

        charge_left = charge_left_negative
        charge_right = charge_right_negative
        case_pp = case_nn

        self.wait(1.4)

        reverse_text = make_caption(
            "الشكل العام مشابه، لكن اتجاه الأسهم انعكس",
            color=NEGATIVE
        )

        self.play(
            FadeIn(reverse_text),
            run_time=0.7
        )

        self.wait(1.2)

        # ====================================================
        # (-,-) — MOVE CLOSER
        # ====================================================

        closer_text = make_caption(
            "نقرّبهما"
        )

        self.play(
            ReplacementTransform(
                reverse_text,
                closer_text
            ),
            run_time=0.5
        )

        field_nn_close = make_vector_field([
            (LEFT_POS, -1),
            (RIGHT_CLOSE, -1)
        ])

        self.play(
            charge_right.animate.move_to(
                RIGHT_CLOSE
            ),
            Transform(
                field,
                field_nn_close
            ),
            run_time=1.7,
            rate_func=smooth
        )

        self.wait(1.0)

        # ====================================================
        # (-,-) — MOVE FARTHER
        # ====================================================

        farther_text = make_caption(
            "ثم نُبعدهما"
        )

        self.play(
            ReplacementTransform(
                closer_text,
                farther_text
            ),
            run_time=0.5
        )

        field_nn_far = make_vector_field([
            (LEFT_POS, -1),
            (RIGHT_FAR, -1)
        ])

        self.play(
            charge_right.animate.move_to(
                RIGHT_FAR
            ),
            Transform(
                field,
                field_nn_far
            ),
            run_time=1.7,
            rate_func=smooth
        )

        self.wait(1.2)

        # ====================================================
        # PART 4 — (+ , -)
        #
        # Return to base separation first.
        # ====================================================

        field_nn_base_again = make_vector_field([
            (LEFT_POS, -1),
            (RIGHT_BASE, -1)
        ])

        self.play(
            FadeOut(farther_text),
            charge_right.animate.move_to(
                RIGHT_BASE
            ),
            Transform(
                field,
                field_nn_base_again
            ),
            run_time=1.1
        )

        self.wait(0.4)

        # ----------------------------------------------------
        # Convert LEFT charge to positive.
        # Right remains negative.
        # ----------------------------------------------------

        charge_left_positive = make_charge(
            LEFT_POS,
            "+"
        )

        field_pn_base = make_vector_field([
            (LEFT_POS, +1),
            (RIGHT_BASE, -1)
        ])

        case_pn = arabic_text(
            "شحنة موجبة وشحنة سالبة",
            size=30,
            weight=BOLD,
            color=TEXT_MAIN
        ).next_to(
            title,
            DOWN,
            buff=0.18
        )

        self.play(
            ReplacementTransform(
                case_pp,
                case_pn
            ),
            ReplacementTransform(
                charge_left,
                charge_left_positive
            ),
            Transform(
                field,
                field_pn_base
            ),
            run_time=1.3
        )

        charge_left = charge_left_positive

        self.wait(1.3)

        # ====================================================
        # HIGHLIGHT FIELD BETWEEN + AND -
        # ====================================================

        pn_text = make_caption(
            "المجال يخرج من الموجبة ويتجه نحو السالبة",
            color=FIELD_COLOR
        )

        self.play(
            FadeIn(pn_text),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # (+,-) — MOVE CLOSER
        # ====================================================

        closer_text = make_caption(
            "نقرّب الشحنتين"
        )

        self.play(
            ReplacementTransform(
                pn_text,
                closer_text
            ),
            run_time=0.5
        )

        field_pn_close = make_vector_field([
            (LEFT_POS, +1),
            (RIGHT_CLOSE, -1)
        ])

        self.play(
            charge_right.animate.move_to(
                RIGHT_CLOSE
            ),
            Transform(
                field,
                field_pn_close
            ),
            run_time=1.8,
            rate_func=smooth
        )

        self.wait(1.3)

        concentrated_text = make_caption(
            "يصبح المجال بينهما أقوى وأكثر تركّزًا",
            color=FIELD_COLOR
        )

        self.play(
            ReplacementTransform(
                closer_text,
                concentrated_text
            ),
            run_time=0.5
        )

        self.wait(1.2)

        # ====================================================
        # (+,-) — MOVE FARTHER
        # ====================================================

        farther_text = make_caption(
            "والآن نُبعدهما"
        )

        self.play(
            ReplacementTransform(
                concentrated_text,
                farther_text
            ),
            run_time=0.5
        )

        field_pn_far = make_vector_field([
            (LEFT_POS, +1),
            (RIGHT_FAR, -1)
        ])

        self.play(
            charge_right.animate.move_to(
                RIGHT_FAR
            ),
            Transform(
                field,
                field_pn_far
            ),
            run_time=1.8,
            rate_func=smooth
        )

        self.wait(1.3)

        # ====================================================
        # PART 5 — FINAL IDEA
        # ====================================================

        self.play(
            FadeOut(farther_text),
            run_time=0.4
        )

        final_text = arabic_text(
            "تغيير إشارة الشحنات أو المسافة بينهما يغيّر شكل المجال",
            size=31,
            weight=BOLD,
            color=FIELD_COLOR
        ).to_edge(
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(final_text),
            run_time=0.8
        )

        self.wait(1.8)

        # ====================================================
        # END
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    title,
                    case_pn,
                    charge_left,
                    charge_right,
                    field,
                    final_text
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

    config.output_file = "scene_21_two_charge_fields"

    config.preview = True
    config.quality = "high_quality"

    Scene21TwoChargeFields().render()