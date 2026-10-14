from manim import *


# ============================================================
# Scene 15
# قبل الشحن بالحث: الاستقطاب فقط
#
# الفكرة الفيزيائية:
#
# 1. لدينا موصل متعادل كهربائيًا.
# 2. نقرب جسمًا سالب الشحنة من الموصل.
# 3. لا يحدث أي تلامس.
# 4. إلكترونات الموصل الحرة تتنافر مع الجسم السالب.
# 5. بعض الإلكترونات تعيد توزيع نفسها نحو الجانب البعيد.
# 6. الجانب القريب يصبح ناقصًا في الإلكترونات
#    -> شحنة سطحية موجبة مستحثة.
# 7. الجانب البعيد تتراكم فيه إلكترونات زائدة
#    -> شحنة سطحية سالبة مستحثة.
# 8. لم تدخل شحنة إلى الموصل ولم تخرج منه.
# 9. Q_net = 0 طوال العملية.
# 10. حتى الآن: استقطاب فقط، وليس شحنًا صافيًا.
#
# المشهد التالي سيضيف التأريض لتحويل الاستقطاب
# إلى شحنة صافية بالحث.
# ============================================================


class Scene15PolarizationBeforeInduction(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"
        ACCENT = "#7EE787"

        METAL = "#B7C0CC"
        METAL_DARK = "#6E7681"
        ROD_COLOR = "#C084FC"

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

        # ====================================================
        # HELPERS
        # ====================================================

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

            return VGroup(
                circle,
                sign
            )

        def make_neutral_pair(center):
            """
            تمثيل مبسط لمنطقة متعادلة داخل الموصل.

            نعرض + و - معًا بوضوح حتى لا يبدو
            الموصل موجبًا أو سالبًا قبل الاستقطاب.
            """

            shell = Circle(
                radius=0.23,
                stroke_width=1.8,
                stroke_color=METAL_DARK,
                stroke_opacity=0.55
            ).move_to(center)

            positive_circle = Circle(
                radius=0.085,
                stroke_width=2,
                stroke_color=POSITIVE,
                fill_color=POSITIVE,
                fill_opacity=0.16
            ).move_to(
                center + LEFT * 0.075
            )

            positive_sign = Text(
                "+",
                font_size=13,
                weight=BOLD,
                color=POSITIVE
            ).move_to(
                positive_circle
            )

            negative_circle = Circle(
                radius=0.085,
                stroke_width=2,
                stroke_color=NEGATIVE,
                fill_color=NEGATIVE,
                fill_opacity=0.18
            ).move_to(
                center + RIGHT * 0.075
            )

            negative_sign = Text(
                "−",
                font_size=13,
                weight=BOLD,
                color=NEGATIVE
            ).move_to(
                negative_circle
            )

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
            "هل يمكن التأثير في موصل من دون لمسه؟",
            size=42,
            weight=BOLD
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.15
            ),
            run_time=1.0
        )

        self.wait(1.6)

        answer = arabic_text(
            "نعم... لكن أول ما يحدث هو الاستقطاب",
            size=35,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            title,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(answer),
            run_time=0.8
        )

        self.wait(1.5)

        self.play(
            FadeOut(answer),
            title.animate.to_edge(
                UP,
                buff=0.42
            ).scale(0.82),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — NEUTRAL METAL CONDUCTOR
        # ====================================================

        conductor_center = RIGHT * 2.25 + DOWN * 0.15

        conductor = Circle(
            radius=1.65,
            stroke_width=4,
            stroke_color=METAL,
            fill_color=METAL,
            fill_opacity=0.06
        ).move_to(
            conductor_center
        )

        conductor_highlight = Arc(
            radius=1.08,
            start_angle=110 * DEGREES,
            angle=75 * DEGREES,
            stroke_width=3,
            color="#E6EDF3"
        ).move_to(
            conductor_center + LEFT * 0.22 + UP * 0.18
        )

        conductor_group = VGroup(
            conductor,
            conductor_highlight
        )

        conductor_label = arabic_text(
            "موصل متعادل",
            size=31,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            conductor_center + UP * 2.05
        )

        net_charge = MathTex(
            "Q_{\\mathrm{net}}=0",
            font_size=48,
            color=ACCENT
        ).next_to(
            conductor_label,
            DOWN,
            buff=0.18
        )

        self.play(
            FadeIn(conductor_group),
            FadeIn(conductor_label),
            FadeIn(net_charge),
            run_time=1.0
        )

        self.wait(1.2)

        # ====================================================
        # PART 3 — BALANCED MICROSCOPIC REPRESENTATION
        # ====================================================

        surface_positions = [
            conductor_center + LEFT * 1.25 + UP * 0.82,
            conductor_center + LEFT * 1.42 + UP * 0.28,
            conductor_center + LEFT * 1.42 + DOWN * 0.28,
            conductor_center + LEFT * 1.25 + DOWN * 0.82,
        ]

        bulk_positions = [
            conductor_center + LEFT * 0.35 + UP * 0.65,
            conductor_center + RIGHT * 0.38 + UP * 0.62,
            conductor_center + LEFT * 0.35 + DOWN * 0.65,
            conductor_center + RIGHT * 0.38 + DOWN * 0.62,
        ]

        surface_pairs = VGroup(
            *[
                make_neutral_pair(pos)
                for pos in surface_positions
            ]
        )

        bulk_pairs = VGroup(
            *[
                make_neutral_pair(pos)
                for pos in bulk_positions
            ]
        )

        neutral_pairs = VGroup(
            surface_pairs,
            bulk_pairs
        )

        representation_note = arabic_text(
            "تمثيل مبسط لتوازن الشحنات داخل الموصل",
            size=25,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(pair, scale=0.75)
                    for pair in surface_pairs
                ],
                lag_ratio=0.08
            ),
            LaggedStart(
                *[
                    FadeIn(pair, scale=0.75)
                    for pair in bulk_pairs
                ],
                lag_ratio=0.08
            ),
            run_time=1.4
        )

        self.play(
            FadeIn(representation_note),
            run_time=0.7
        )

        self.wait(1.5)

        # ====================================================
        # PART 4 — NEGATIVE ROD APPEARS
        # ====================================================

        self.play(
            FadeOut(representation_note),
            run_time=0.4
        )

        rod = RoundedRectangle(
            width=0.75,
            height=4.3,
            corner_radius=0.22,
            stroke_width=4,
            stroke_color=ROD_COLOR,
            fill_color=ROD_COLOR,
            fill_opacity=0.10
        ).move_to(
            LEFT * 4.4
        )

        rod_charges = VGroup()

        for y in [-1.55, -0.78, 0, 0.78, 1.55]:
            rod_charges.add(
                negative_marker(
                    LEFT * 4.4 + UP * y
                )
            )

        rod_label = arabic_text(
            "جسم سالب الشحنة",
            size=29,
            color=NEGATIVE
        ).move_to(
            LEFT * 4.4 + UP * 2.55
        )

        self.play(
            FadeIn(rod),
            FadeIn(rod_charges),
            FadeIn(rod_label),
            run_time=0.9
        )

        self.wait(1.0)

        # ====================================================
        # PART 5 — APPROACH WITHOUT CONTACT
        # ====================================================

        approach_text = arabic_text(
            "نقرّبه من الموصل...",
            size=33,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(approach_text),
            run_time=0.7
        )

        rod_shift = RIGHT * 3.55

        self.play(
            rod.animate.shift(rod_shift),
            rod_charges.animate.shift(rod_shift),
            rod_label.animate.shift(rod_shift),
            run_time=1.5,
            rate_func=smooth
        )

        self.wait(0.8)

        self.play(
            FadeOut(approach_text),
            run_time=0.4
        )

        # ====================================================
        # PART 6 — CLEARLY SHOW THE GAP
        # ====================================================

        gap_start = rod.get_right() + UP * 1.55
        gap_end = conductor.get_left() + UP * 1.55

        gap_arrow = DoubleArrow(
            start=gap_start,
            end=gap_end,
            buff=0.05,
            stroke_width=3,
            color=ACCENT,
            max_tip_length_to_length_ratio=0.18
        )

        no_contact = arabic_text(
            "لا تلامس",
            size=29,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            gap_arrow,
            UP,
            buff=0.12
        )

        self.play(
            GrowFromCenter(gap_arrow),
            FadeIn(no_contact),
            run_time=0.8
        )

        self.wait(1.2)

        no_transfer_text = arabic_text(
            "لا تنتقل شحنة من الجسم السالب إلى الموصل",
            size=29,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(no_transfer_text),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 7 — ELECTRONS FEEL REPULSION
        # ====================================================

        self.play(
            FadeOut(gap_arrow),
            FadeOut(no_contact),
            FadeOut(no_transfer_text),
            run_time=0.5
        )

        electron_title = arabic_text(
            "لكن إلكترونات الموصل الحرة تتأثر",
            size=34,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(electron_title),
            run_time=0.8
        )

        self.wait(0.8)

        moving_electrons = [
            VGroup(pair[3], pair[4])
            for pair in surface_pairs
        ]

        positive_residues = VGroup(
            *[
                VGroup(pair[1], pair[2])
                for pair in surface_pairs
            ]
        )

        self.play(
            *[
                Indicate(
                    electron,
                    color=NEGATIVE,
                    scale_factor=1.45
                )
                for electron in moving_electrons
            ],
            run_time=1.0
        )

        self.wait(0.6)

        repulsion_text = arabic_text(
            "الجسم السالب يتنافر مع الإلكترونات الحرة",
            size=31,
            color=NEGATIVE
        ).move_to(
            UP * 2.45
        )

        self.play(
            FadeIn(repulsion_text),
            run_time=0.8
        )

        self.wait(1.2)

        # ====================================================
        # PART 8 — ELECTRONS REDISTRIBUTE INSIDE CONDUCTOR
        # ====================================================

        direction_arrow = Arrow(
            start=conductor_center + LEFT * 0.75,
            end=conductor_center + RIGHT * 0.95,
            buff=0,
            stroke_width=6,
            color=NEGATIVE,
            max_tip_length_to_length_ratio=0.13
        )

        movement_label = arabic_text(
            "إعادة توزيع الإلكترونات",
            size=27,
            color=NEGATIVE
        ).next_to(
            direction_arrow,
            UP,
            buff=0.18
        )

        self.play(
            GrowArrow(direction_arrow),
            FadeIn(movement_label),
            run_time=0.8
        )

        self.wait(0.5)

        electron_targets = [
            conductor_center + RIGHT * 1.25 + UP * 0.82,
            conductor_center + RIGHT * 1.42 + UP * 0.28,
            conductor_center + RIGHT * 1.42 + DOWN * 0.28,
            conductor_center + RIGHT * 1.25 + DOWN * 0.82,
        ]

        # Fade the small neutral shells of the selected sites slightly,
        # while only the negative parts move.
        shell_animations = [
            pair[0].animate.set_opacity(0.20)
            for pair in surface_pairs
        ]

        self.play(
            *shell_animations,
            *[
                electron.animate.move_to(target)
                for electron, target in zip(
                    moving_electrons,
                    electron_targets
                )
            ],
            run_time=1.8,
            rate_func=smooth
        )

        self.wait(1.1)

        self.play(
            FadeOut(direction_arrow),
            FadeOut(movement_label),
            FadeOut(electron_title),
            FadeOut(repulsion_text),
            run_time=0.5
        )

        # ====================================================
        # PART 9 — EXPLAIN THE TWO SIDES
        # ====================================================

        polarization_title = arabic_text(
            "الآن أصبح الموصل مستقطبًا",
            size=37,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeOut(title),
            FadeIn(polarization_title),
            run_time=0.8
        )

        self.wait(0.8)

        # ----------------------------------------------------
        # Near side
        # ----------------------------------------------------

        near_side_label_1 = arabic_text(
            "الجانب القريب",
            size=27,
            color=POSITIVE
        ).move_to(
            conductor_center + LEFT * 1.55 + DOWN * 2.05
        )

        near_side_label_2 = arabic_text(
            "نقص في الإلكترونات",
            size=26,
            color=TEXT_SECONDARY
        ).next_to(
            near_side_label_1,
            DOWN,
            buff=0.15
        )

        near_side_label_3 = arabic_text(
            "موجب نسبيًا",
            size=29,
            weight=BOLD,
            color=POSITIVE
        ).next_to(
            near_side_label_2,
            DOWN,
            buff=0.15
        )

        self.play(
            Indicate(
                positive_residues,
                color=POSITIVE,
                scale_factor=1.2
            ),
            run_time=0.8
        )

        self.play(
            FadeIn(near_side_label_1),
            FadeIn(near_side_label_2),
            FadeIn(near_side_label_3),
            run_time=0.8
        )

        self.wait(1.2)

        # ----------------------------------------------------
        # Far side
        # ----------------------------------------------------

        far_electron_group = VGroup(
            *moving_electrons
        )

        far_side_label_1 = arabic_text(
            "الجانب البعيد",
            size=27,
            color=NEGATIVE
        ).move_to(
            conductor_center + RIGHT * 1.55 + DOWN * 2.05
        )

        far_side_label_2 = arabic_text(
            "تراكم إلكترونات",
            size=26,
            color=TEXT_SECONDARY
        ).next_to(
            far_side_label_1,
            DOWN,
            buff=0.15
        )

        far_side_label_3 = arabic_text(
            "سالب نسبيًا",
            size=29,
            weight=BOLD,
            color=NEGATIVE
        ).next_to(
            far_side_label_2,
            DOWN,
            buff=0.15
        )

        self.play(
            Indicate(
                far_electron_group,
                color=NEGATIVE,
                scale_factor=1.2
            ),
            run_time=0.8
        )

        self.play(
            FadeIn(far_side_label_1),
            FadeIn(far_side_label_2),
            FadeIn(far_side_label_3),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 10 — NET CHARGE IS STILL ZERO
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    near_side_label_1,
                    near_side_label_2,
                    near_side_label_3,
                    far_side_label_1,
                    far_side_label_2,
                    far_side_label_3
                )
            ),
            run_time=0.6
        )

        net_question = arabic_text(
            "هل أصبح الموصل مشحونًا الآن؟",
            size=35,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(net_question),
            run_time=0.8
        )

        self.wait(1.0)

        answer_no = arabic_text(
            "لا",
            size=44,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            net_question,
            UP,
            buff=0.35
        )

        self.play(
            FadeIn(answer_no, scale=0.8),
            run_time=0.6
        )

        self.wait(0.8)

        self.play(
            Indicate(
                net_charge,
                color=ACCENT,
                scale_factor=1.18
            ),
            run_time=0.9
        )

        self.wait(0.8)

        conservation_note = arabic_text(
            "لم تدخل إلكترونات إلى الموصل ولم تخرج منه",
            size=30,
            color=TEXT_SECONDARY
        ).move_to(
            DOWN * 2.45
        )

        self.play(
            FadeOut(net_question),
            FadeOut(answer_no),
            FadeIn(conservation_note),
            run_time=0.8
        )

        self.wait(1.3)

        conservation_note_2 = arabic_text(
            "الذي تغير هو توزيع الشحنة فقط",
            size=33,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            conservation_note,
            UP,
            buff=0.28
        )

        self.play(
            FadeIn(conservation_note_2),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 11 — POLARIZATION ONLY
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    conservation_note,
                    conservation_note_2
                )
            ),
            run_time=0.6
        )

        polarization_box = RoundedRectangle(
            width=5.8,
            height=1.55,
            corner_radius=0.22,
            stroke_width=3,
            stroke_color=ACCENT,
            fill_color=ACCENT,
            fill_opacity=0.035
        ).move_to(
            DOWN * 2.35
        )

        polarization_text_1 = arabic_text(
            "حتى الآن",
            size=27,
            color=TEXT_SECONDARY
        ).move_to(
            polarization_box.get_center() + UP * 0.28
        )

        polarization_text_2 = arabic_text(
            "استقطاب فقط",
            size=36,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            polarization_box.get_center() + DOWN * 0.25
        )

        self.play(
            FadeIn(polarization_box),
            FadeIn(polarization_text_1),
            FadeIn(polarization_text_2),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 12 — PREPARE FOR GROUNDING
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    polarization_box,
                    polarization_text_1,
                    polarization_text_2
                )
            ),
            run_time=0.6
        )

        next_question = arabic_text(
            "فكيف نجعل الموصل يحتفظ بشحنة صافية؟",
            size=35,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(next_question),
            run_time=0.8
        )

        self.wait(1.2)

        grounding_tease = arabic_text(
            "نحتاج إلى خطوة إضافية: التأريض",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            next_question,
            UP,
            buff=0.35
        )

        self.play(
            FadeIn(grounding_tease),
            run_time=0.8
        )

        self.wait(1.8)

        # ====================================================
        # PART 13 — END
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    rod,
                    rod_charges,
                    rod_label,
                    conductor_group,
                    conductor_label,
                    net_charge,
                    neutral_pairs,
                    polarization_title,
                    next_question,
                    grounding_tease
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

    config.output_file = "scene_15_polarization_before_induction"

    config.preview = True
    config.quality = "high_quality"

    Scene15PolarizationBeforeInduction().render()