from manim import *


# ============================================================
# Scene 10
# الاستقطاب — النسخة المصححة
#
# التصحيح الأساسي:
# قبل اقتراب البالون لا نظهر + و - منفصلتين داخل الحائط.
# تظهر الذرات/الجزيئات كوحدات متعادلة رمادية.
#
# فقط بعد اقتراب البالون:
# - يظهر فصل مجهري صغير بين مركزي الشحنة.
# - الجهة الأقرب تصبح أكثر إيجابية نسبيًا.
# - الجهة الأبعد تصبح أكثر سلبية نسبيًا.
#
# بهذه الطريقة لا يبدو الحائط موجبًا قبل الاستقطاب.
# ============================================================


class Scene10Polarization(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"
        ACCENT = "#7EE787"

        WALL_COLOR = "#8B949E"
        BALLOON_COLOR = "#D77BF3"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

        FORCE_ATTRACTION = "#7EE787"
        FORCE_REPULSION = "#FFD166"

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

        def make_balloon(center=ORIGIN, scale_factor=1.0):

            body = Ellipse(
                width=2.2 * scale_factor,
                height=2.8 * scale_factor,
                stroke_width=4,
                stroke_color=BALLOON_COLOR,
                fill_color=BALLOON_COLOR,
                fill_opacity=0.14
            ).move_to(center)

            knot = Polygon(
                center + DOWN * 1.38 * scale_factor,
                center + LEFT * 0.16 * scale_factor + DOWN * 1.62 * scale_factor,
                center + RIGHT * 0.16 * scale_factor + DOWN * 1.62 * scale_factor,
                stroke_width=3,
                stroke_color=BALLOON_COLOR,
                fill_color=BALLOON_COLOR,
                fill_opacity=0.16
            )

            string = CubicBezier(
                center + DOWN * 1.62 * scale_factor,
                center + LEFT * 0.25 * scale_factor + DOWN * 2.0 * scale_factor,
                center + RIGHT * 0.30 * scale_factor + DOWN * 2.4 * scale_factor,
                center + DOWN * 2.85 * scale_factor,
                stroke_width=2,
                color=TEXT_SECONDARY
            )

            return VGroup(
                body,
                knot,
                string
            )

        def negative_marker(position, radius=0.095):

            circle = Circle(
                radius=radius,
                stroke_width=2,
                stroke_color=NEGATIVE,
                fill_color=NEGATIVE,
                fill_opacity=0.22
            ).move_to(position)

            sign = Text(
                "−",
                font_size=14,
                weight=BOLD,
                color=NEGATIVE
            ).move_to(circle)

            return VGroup(circle, sign)

        def make_neutral_unit(center):
            """
            قبل الاستقطاب:
            وحدة متعادلة رمادية بلا فصل بصري بين + و -.
            """

            shell = Circle(
                radius=0.24,
                stroke_width=2.5,
                stroke_color=TEXT_SECONDARY,
                fill_color=TEXT_SECONDARY,
                fill_opacity=0.08
            ).move_to(center)

            neutral_dot = Dot(
                center,
                radius=0.055,
                color=TEXT_SECONDARY
            )

            return VGroup(
                shell,
                neutral_dot
            )

        def make_polarized_unit(center, separation=0.24):
            """
            بعد الاستقطاب:
            + أقرب إلى البالون الموجود يسار الشاشة.
            - أبعد عنه قليلًا.
            """

            shell = Circle(
                radius=0.24,
                stroke_width=2,
                stroke_color=TEXT_SECONDARY,
                stroke_opacity=0.45
            ).move_to(center)

            positive_circle = Circle(
                radius=0.105,
                stroke_width=2,
                stroke_color=POSITIVE,
                fill_color=POSITIVE,
                fill_opacity=0.18
            ).move_to(
                center + LEFT * separation / 2
            )

            positive_sign = Text(
                "+",
                font_size=14,
                weight=BOLD,
                color=POSITIVE
            ).move_to(positive_circle)

            negative_circle = Circle(
                radius=0.105,
                stroke_width=2,
                stroke_color=NEGATIVE,
                fill_color=NEGATIVE,
                fill_opacity=0.18
            ).move_to(
                center + RIGHT * separation / 2
            )

            negative_sign = Text(
                "−",
                font_size=14,
                weight=BOLD,
                color=NEGATIVE
            ).move_to(negative_circle)

            return VGroup(
                shell,
                positive_circle,
                positive_sign,
                negative_circle,
                negative_sign
            )

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "كيف يجذب البالون حائطًا متعادلًا؟",
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

        self.wait(1.5)

        polarization_word = arabic_text(
            "الاستقطاب",
            size=39,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            title,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(polarization_word),
            run_time=0.8
        )

        self.wait(1.4)

        self.play(
            FadeOut(title),
            polarization_word.animate.to_edge(
                UP,
                buff=0.45
            ),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — BALLOON AND NEUTRAL WALL
        # ====================================================

        balloon = make_balloon(
            LEFT * 4.3 + DOWN * 0.1,
            scale_factor=0.85
        )

        balloon_negatives = VGroup(
            negative_marker(
                balloon[0].get_center() + LEFT * 0.55 + UP * 0.65
            ),
            negative_marker(
                balloon[0].get_center() + RIGHT * 0.45 + UP * 0.60
            ),
            negative_marker(
                balloon[0].get_center() + LEFT * 0.60
            ),
            negative_marker(
                balloon[0].get_center() + RIGHT * 0.55 + DOWN * 0.10
            ),
            negative_marker(
                balloon[0].get_center() + LEFT * 0.35 + DOWN * 0.70
            ),
            negative_marker(
                balloon[0].get_center() + RIGHT * 0.35 + DOWN * 0.75
            )
        )

        balloon_label = arabic_text(
            "بالون سالب الشحنة",
            size=29,
            color=NEGATIVE
        ).next_to(
            balloon[0],
            DOWN,
            buff=0.35
        )

        wall = Rectangle(
            width=5.4,
            height=5.8,
            stroke_width=4,
            stroke_color=WALL_COLOR,
            fill_color=WALL_COLOR,
            fill_opacity=0.05
        ).move_to(
            RIGHT * 3.9
        )

        wall_label = arabic_text(
            "حائط متعادل",
            size=30,
            color=ACCENT
        ).move_to(
            wall.get_top() + DOWN * 0.45
        )

        net_zero = MathTex(
            "Q_{\\mathrm{net}}=0",
            font_size=45,
            color=ACCENT
        ).next_to(
            wall_label,
            DOWN,
            buff=0.2
        )

        self.play(
            FadeIn(balloon),
            FadeIn(balloon_negatives),
            FadeIn(balloon_label),
            FadeIn(wall),
            FadeIn(wall_label),
            FadeIn(net_zero),
            run_time=1.0
        )

        self.wait(1.5)

        # ====================================================
        # PART 3 — LOOK INSIDE THE WALL
        # ====================================================

        zoom_text = arabic_text(
            "لننظر داخل مادة الحائط",
            size=33,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(zoom_text),
            run_time=0.7
        )

        self.wait(1.0)

        micro_panel = RoundedRectangle(
            width=7.2,
            height=4.5,
            corner_radius=0.22,
            stroke_width=3,
            stroke_color=WALL_COLOR,
            fill_color=WALL_COLOR,
            fill_opacity=0.035
        ).move_to(
            RIGHT * 2.7 + DOWN * 0.15
        )

        self.play(
            FadeOut(wall),
            FadeOut(wall_label),
            FadeOut(net_zero),
            FadeOut(zoom_text),
            FadeIn(micro_panel),
            run_time=0.8
        )

        # ====================================================
        # PART 4 — NEUTRAL UNITS BEFORE POLARIZATION
        # ====================================================

        unit_positions = [
            [0.4, 1.15, 0],
            [2.0, 1.15, 0],
            [3.6, 1.15, 0],
            [5.2, 1.15, 0],

            [0.4, -0.15, 0],
            [2.0, -0.15, 0],
            [3.6, -0.15, 0],
            [5.2, -0.15, 0],

            [0.4, -1.45, 0],
            [2.0, -1.45, 0],
            [3.6, -1.45, 0],
            [5.2, -1.45, 0],
        ]

        neutral_units = VGroup(
            *[
                make_neutral_unit(pos)
                for pos in unit_positions
            ]
        )

        neutral_state_title = arabic_text(
            "قبل اقتراب البالون",
            size=34,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        neutral_state_note = arabic_text(
            "لا يوجد فصل واضح بين جانبي الشحنة",
            size=29,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeOut(polarization_word),
            FadeIn(neutral_state_title),
            LaggedStart(
                *[
                    FadeIn(unit, scale=0.7)
                    for unit in neutral_units
                ],
                lag_ratio=0.05
            ),
            run_time=1.3
        )

        self.wait(1.0)

        self.play(
            FadeIn(neutral_state_note),
            run_time=0.7
        )

        self.wait(1.5)

        still_neutral_before = MathTex(
            "Q_{\\mathrm{net}}=0",
            font_size=50,
            color=ACCENT
        ).move_to(
            RIGHT * 2.7 + UP * 2.15
        )

        self.play(
            FadeIn(still_neutral_before),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 5 — BALLOON APPROACHES
        # ====================================================

        self.play(
            FadeOut(neutral_state_note),
            FadeOut(neutral_state_title),
            FadeOut(still_neutral_before),
            run_time=0.5
        )

        approach_title = arabic_text(
            "نقرّب البالون السالب",
            size=34,
            weight=BOLD,
            color=NEGATIVE
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(approach_title),
            run_time=0.7
        )

        self.play(
            VGroup(
                balloon,
                balloon_negatives,
                balloon_label
            ).animate.shift(
                RIGHT * 1.0
            ),
            run_time=1.2
        )

        self.wait(1.0)

        # ====================================================
        # PART 6 — POLARIZATION APPEARS
        # ====================================================

        polarized_units = VGroup(
            *[
                make_polarized_unit(pos)
                for pos in unit_positions
            ]
        )

        polarization_explanation = arabic_text(
            "الآن يحدث فصل مجهري صغير داخل المادة",
            size=31,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(polarization_explanation),
            run_time=0.8
        )

        self.wait(0.7)

        # Transform each neutral gray unit into a polarized unit.
        self.play(
            *[
                ReplacementTransform(
                    neutral,
                    polarized
                )
                for neutral, polarized in zip(
                    neutral_units,
                    polarized_units
                )
            ],
            run_time=1.6
        )

        self.wait(1.3)

        # ====================================================
        # PART 7 — EMPHASIZE SMALL LOCAL SHIFT
        # ====================================================

        microscopic_note = arabic_text(
            "الحائط عازل: لا تسافر الإلكترونات بحرية خلاله",
            size=29,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeOut(polarization_explanation),
            FadeIn(microscopic_note),
            run_time=0.8
        )

        self.wait(1.3)

        microscopic_note_2 = arabic_text(
            "إنما يتغير توزيع الشحنة مسافة مجهرية صغيرة",
            size=31,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            microscopic_note,
            UP,
            buff=0.25
        )

        self.play(
            FadeIn(microscopic_note_2),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 8 — NEAR SIDE / FAR SIDE
        # ====================================================

        self.play(
            FadeOut(approach_title),
            FadeOut(microscopic_note),
            FadeOut(microscopic_note_2),
            run_time=0.6
        )

        near_side = RoundedRectangle(
            width=1.15,
            height=4.0,
            corner_radius=0.15,
            stroke_width=3,
            stroke_color=POSITIVE,
            fill_color=POSITIVE,
            fill_opacity=0.03
        ).move_to(
            LEFT * 0.05 + DOWN * 0.15
        )

        far_side = RoundedRectangle(
            width=1.15,
            height=4.0,
            corner_radius=0.15,
            stroke_width=3,
            stroke_color=NEGATIVE,
            fill_color=NEGATIVE,
            fill_opacity=0.03
        ).move_to(
            RIGHT * 5.45 + DOWN * 0.15
        )

        near_label = arabic_text(
            "الجانب الأقرب",
            size=27,
            color=POSITIVE
        ).next_to(
            near_side,
            UP,
            buff=0.2
        )

        far_label = arabic_text(
            "الجانب الأبعد",
            size=27,
            color=NEGATIVE
        ).next_to(
            far_side,
            UP,
            buff=0.2
        )

        self.play(
            FadeIn(near_side),
            FadeIn(near_label),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(far_side),
            FadeIn(far_label),
            run_time=0.7
        )

        self.wait(0.7)

        near_text = arabic_text(
            "أكثر إيجابية نسبيًا",
            size=29,
            weight=BOLD,
            color=POSITIVE
        ).move_to(
            LEFT * 0.1 + DOWN * 2.55
        )

        far_text = arabic_text(
            "أكثر سلبية نسبيًا",
            size=29,
            weight=BOLD,
            color=NEGATIVE
        ).move_to(
            RIGHT * 4.7 + DOWN * 2.55
        )

        self.play(
            FadeIn(near_text),
            FadeIn(far_text),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 9 — WALL STILL HAS ZERO NET CHARGE
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    near_side,
                    far_side,
                    near_label,
                    far_label,
                    near_text,
                    far_text
                )
            ),
            run_time=0.6
        )

        neutral_title = arabic_text(
            "لكن الحائط ما زال متعادلًا ككل",
            size=36,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(neutral_title),
            run_time=0.8
        )

        self.wait(0.7)

        net_zero_again = MathTex(
            "Q_{\\mathrm{net}}=0",
            font_size=62,
            color=ACCENT
        ).move_to(
            RIGHT * 2.7 + UP * 1.9
        )

        self.play(
            FadeIn(net_zero_again),
            run_time=0.8
        )

        self.wait(1.1)

        redistribution_text = arabic_text(
            "لم تتغير كمية الشحنة الكلية",
            size=30,
            color=TEXT_SECONDARY
        ).next_to(
            net_zero_again,
            DOWN,
            buff=0.25
        )

        redistribution_text_2 = arabic_text(
            "الذي تغير هو توزيعها",
            size=32,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            redistribution_text,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(redistribution_text),
            run_time=0.7
        )

        self.play(
            FadeIn(redistribution_text_2),
            run_time=0.7
        )

        self.wait(1.6)

        # ====================================================
        # PART 10 — WHY IS THERE NET ATTRACTION?
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    neutral_title,
                    net_zero_again,
                    redistribution_text,
                    redistribution_text_2
                )
            ),
            run_time=0.6
        )

        force_question = arabic_text(
            "فلماذا تكون محصلة القوة جذبًا؟",
            size=38,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(force_question),
            run_time=0.8
        )

        self.wait(1.0)

        representative_unit = polarized_units[4]

        self.play(
            Indicate(
                representative_unit,
                color=ACCENT,
                scale_factor=1.5
            ),
            run_time=0.9
        )

        self.wait(0.7)

        # ====================================================
        # PART 11 — SHOW NEAR AND FAR CHARGES
        # ====================================================

        positive_center = representative_unit[1].get_center()
        negative_center = representative_unit[3].get_center()

        balloon_reference = balloon[0].get_right()

        near_distance = DoubleArrow(
            start=balloon_reference + UP * 0.65,
            end=positive_center + UP * 0.65,
            buff=0.05,
            stroke_width=3,
            color=POSITIVE,
            max_tip_length_to_length_ratio=0.13
        )

        far_distance = DoubleArrow(
            start=balloon_reference + DOWN * 0.7,
            end=negative_center + DOWN * 0.7,
            buff=0.05,
            stroke_width=3,
            color=NEGATIVE,
            max_tip_length_to_length_ratio=0.13
        )

        near_distance_label = arabic_text(
            "الشحنة المخالفة أقرب",
            size=24,
            color=POSITIVE
        ).next_to(
            near_distance,
            UP,
            buff=0.1
        )

        far_distance_label = arabic_text(
            "الشحنة المشابهة أبعد",
            size=24,
            color=NEGATIVE
        ).next_to(
            far_distance,
            DOWN,
            buff=0.1
        )

        self.play(
            GrowFromCenter(near_distance),
            FadeIn(near_distance_label),
            run_time=0.8
        )

        self.wait(0.6)

        self.play(
            GrowFromCenter(far_distance),
            FadeIn(far_distance_label),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 12 — FORCE COMPARISON
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    near_distance,
                    far_distance,
                    near_distance_label,
                    far_distance_label
                )
            ),
            run_time=0.5
        )

        attraction_arrow = Arrow(
            start=representative_unit.get_center() + LEFT * 0.35,
            end=representative_unit.get_center() + LEFT * 2.0,
            buff=0,
            stroke_width=6,
            color=FORCE_ATTRACTION,
            max_tip_length_to_length_ratio=0.16
        )

        attraction_label = arabic_text(
            "جذب أقوى",
            size=27,
            weight=BOLD,
            color=FORCE_ATTRACTION
        ).next_to(
            attraction_arrow,
            UP,
            buff=0.18
        )

        repulsion_arrow = Arrow(
            start=representative_unit.get_center() + RIGHT * 0.35 + DOWN * 0.7,
            end=representative_unit.get_center() + RIGHT * 1.25 + DOWN * 0.7,
            buff=0,
            stroke_width=4,
            color=FORCE_REPULSION,
            max_tip_length_to_length_ratio=0.20
        )

        repulsion_label = arabic_text(
            "تنافر أضعف",
            size=25,
            color=FORCE_REPULSION
        ).next_to(
            repulsion_arrow,
            DOWN,
            buff=0.18
        )

        self.play(
            GrowArrow(attraction_arrow),
            FadeIn(attraction_label),
            run_time=0.8
        )

        self.wait(0.7)

        self.play(
            GrowArrow(repulsion_arrow),
            FadeIn(repulsion_label),
            run_time=0.8
        )

        self.wait(1.5)

        force_explanation = arabic_text(
            "القوة تكون أكبر على الشحنات الأقرب",
            size=30
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(force_explanation),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 13 — NET FORCE
        # ====================================================

        self.play(
            FadeOut(attraction_arrow),
            FadeOut(attraction_label),
            FadeOut(repulsion_arrow),
            FadeOut(repulsion_label),
            FadeOut(force_explanation),
            run_time=0.6
        )

        net_force_arrow = Arrow(
            start=micro_panel.get_center(),
            end=micro_panel.get_center() + LEFT * 2.2,
            buff=0,
            stroke_width=7,
            color=ACCENT,
            max_tip_length_to_length_ratio=0.14
        )

        net_force_label = arabic_text(
            "محصلة القوة → جذب",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            net_force_arrow,
            UP,
            buff=0.25
        )

        self.play(
            GrowArrow(net_force_arrow),
            FadeIn(net_force_label),
            run_time=0.9
        )

        self.wait(1.7)

        # ====================================================
        # PART 14 — RETURN TO MACROSCOPIC VIEW
        # ====================================================

        self.play(
            FadeOut(force_question),
            FadeOut(net_force_arrow),
            FadeOut(net_force_label),
            FadeOut(polarized_units),
            FadeOut(micro_panel),
            run_time=0.8
        )

        macro_wall = Rectangle(
            width=3.3,
            height=6.0,
            stroke_width=4,
            stroke_color=WALL_COLOR,
            fill_color=WALL_COLOR,
            fill_opacity=0.06
        ).move_to(
            RIGHT * 5.0
        )

        self.play(
            FadeIn(macro_wall),
            run_time=0.6
        )

        self.play(
            VGroup(
                balloon,
                balloon_negatives,
                balloon_label
            ).animate.shift(
                RIGHT * 1.15
            ),
            run_time=1.1
        )

        self.wait(0.6)

        result_text = arabic_text(
            "جسم مشحون يستطيع جذب جسم متعادل",
            size=36,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.5
        )

        self.play(
            FadeIn(result_text),
            run_time=0.8
        )

        self.wait(1.2)

        result_text_2 = arabic_text(
            "من دون أن يصبح الجسم المتعادل مشحونًا ككل",
            size=30,
            color=TEXT_SECONDARY
        ).next_to(
            result_text,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(result_text_2),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 15 — FINAL SUMMARY
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    balloon,
                    balloon_negatives,
                    balloon_label,
                    macro_wall,
                    result_text,
                    result_text_2
                )
            ),
            run_time=0.8
        )

        summary_title = arabic_text(
            "الاستقطاب",
            size=44,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.5
        )

        summary_1 = arabic_text(
            "قبل المجال: لا يوجد فصل واضح في توزيع الشحنة",
            size=31
        ).shift(
            UP * 0.8
        )

        summary_2 = arabic_text(
            "بعد اقتراب الجسم المشحون: يحدث فصل مجهري صغير",
            size=31,
            color=ACCENT
        ).next_to(
            summary_1,
            DOWN,
            buff=0.35
        )

        summary_3 = arabic_text(
            "صافي الشحنة يبقى صفرًا",
            size=32,
            weight=BOLD
        ).next_to(
            summary_2,
            DOWN,
            buff=0.35
        )

        summary_4 = arabic_text(
            "لكن المحصلة يمكن أن تكون قوة جذب",
            size=33,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            summary_3,
            DOWN,
            buff=0.4
        )

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

        self.wait(0.5)

        self.play(
            FadeIn(summary_3),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(summary_4),
            run_time=0.7
        )

        self.wait(1.8)

        # ====================================================
        # PART 16 — TRANSITION TO WATER
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    summary_title,
                    summary_1,
                    summary_2,
                    summary_3,
                    summary_4
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "ويمكن رؤية فكرة مرتبطة بذلك",
            size=35
        ).shift(
            UP * 0.45
        )

        transition_2 = arabic_text(
            "في شيء مألوف جدًا: الماء",
            size=39,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            transition_1,
            DOWN,
            buff=0.3
        )

        transition_3 = arabic_text(
            "لماذا ينحني خيط الماء نحو جسم مشحون؟",
            size=31
        ).next_to(
            transition_2,
            DOWN,
            buff=0.4
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

        self.wait(0.6)

        self.play(
            FadeIn(transition_3),
            run_time=0.7
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

    config.output_file = "scene_10_polarization"

    config.preview = True
    config.quality = "high_quality"

    Scene10Polarization().render()