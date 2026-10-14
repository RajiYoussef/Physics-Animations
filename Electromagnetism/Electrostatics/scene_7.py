from manim import *


# ============================================================
# Scene 07
# الشحن بالاحتكاك
#
# الفكرة:
# - الجسمان متعادلان في البداية.
# - عند تلامس مادتين مختلفتين ثم انفصالهما،
#   يمكن أن تنتقل بعض الإلكترونات بين السطحين.
# - اتجاه الانتقال يعتمد على طبيعة المادتين وحالة السطح.
# - الفرك يكرر التلامس والانفصال على مناطق كثيرة.
# - الاحتكاك لا يصنع شحنة جديدة.
# - بعد انتقال الإلكترونات:
#   الجسم الذي اكتسب إلكترونات يصبح سالبًا.
#   الجسم الذي فقد إلكترونات يصبح موجبًا.
# ============================================================


class Scene07ChargingByFriction(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        # ----------------------------------------------------
        # Color palette
        # ----------------------------------------------------

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"
        ACCENT = "#7EE787"

        MATERIAL_A = "#C9A66B"
        MATERIAL_B = "#9C7BC0"

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
        # HELPER FUNCTIONS
        # ====================================================

        def positive_marker(position, scale_factor=1.0):

            circle = Circle(
                radius=0.14 * scale_factor,
                stroke_width=2,
                stroke_color=POSITIVE,
                fill_color=POSITIVE,
                fill_opacity=0.16
            ).move_to(position)

            sign = Text(
                "+",
                font_size=18 * scale_factor,
                weight=BOLD,
                color=POSITIVE
            ).move_to(circle)

            return VGroup(circle, sign)

        def electron_marker(position, scale_factor=1.0):

            circle = Circle(
                radius=0.14 * scale_factor,
                stroke_width=2,
                stroke_color=NEGATIVE,
                fill_color=NEGATIVE,
                fill_opacity=0.18
            ).move_to(position)

            sign = Text(
                "−",
                font_size=18 * scale_factor,
                weight=BOLD,
                color=NEGATIVE
            ).move_to(circle)

            return VGroup(circle, sign)

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "كيف تنتقل الإلكترونات من جسم إلى آخر؟",
            size=43,
            weight=BOLD
        )

        self.play(
            FadeIn(title, shift=UP * 0.15),
            run_time=1.0
        )

        self.wait(1.7)

        subtitle = arabic_text(
            "إحدى الطرق: الشحن بالاحتكاك",
            size=35,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            title,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(subtitle),
            run_time=0.8
        )

        self.wait(1.4)

        self.play(
            FadeOut(title),
            subtitle.animate.to_edge(
                UP,
                buff=0.45
            ),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — TWO NEUTRAL MATERIALS
        # ====================================================

        material_a = RoundedRectangle(
            width=5.2,
            height=1.5,
            corner_radius=0.22,
            stroke_width=3,
            stroke_color=MATERIAL_A,
            fill_color=MATERIAL_A,
            fill_opacity=0.10
        ).move_to(
            LEFT * 3.0 + DOWN * 0.7
        )

        material_b = RoundedRectangle(
            width=5.2,
            height=1.5,
            corner_radius=0.22,
            stroke_width=3,
            stroke_color=MATERIAL_B,
            fill_color=MATERIAL_B,
            fill_opacity=0.10
        ).move_to(
            RIGHT * 3.0 + UP * 0.9
        )

        label_a = arabic_text(
            "المادة A",
            size=28,
            color=MATERIAL_A
        ).next_to(
            material_a,
            DOWN,
            buff=0.22
        )

        label_b = arabic_text(
            "المادة B",
            size=28,
            color=MATERIAL_B
        ).next_to(
            material_b,
            UP,
            buff=0.22
        )

        self.play(
            FadeIn(material_a),
            FadeIn(material_b),
            FadeIn(label_a),
            FadeIn(label_b),
            run_time=1.0
        )

        self.wait(1.0)

        # ----------------------------------------------------
        # Neutral charge distributions
        # ----------------------------------------------------

        a_positive_positions = [
            [-4.7, -0.45, 0],
            [-3.8, -0.95, 0],
            [-2.9, -0.45, 0],
            [-2.0, -0.95, 0],
            [-1.25, -0.45, 0],
        ]

        a_negative_positions = [
            [-4.25, -0.95, 0],
            [-3.35, -0.45, 0],
            [-2.45, -0.95, 0],
            [-1.55, -0.45, 0],
            [-0.95, -0.95, 0],
        ]

        b_positive_positions = [
            [0.95, 1.15, 0],
            [1.85, 0.65, 0],
            [2.75, 1.15, 0],
            [3.65, 0.65, 0],
            [4.55, 1.15, 0],
        ]

        b_negative_positions = [
            [1.4, 0.65, 0],
            [2.3, 1.15, 0],
            [3.2, 0.65, 0],
            [4.1, 1.15, 0],
            [4.85, 0.65, 0],
        ]

        a_positives = VGroup(
            *[
                positive_marker(pos)
                for pos in a_positive_positions
            ]
        )

        a_electrons = VGroup(
            *[
                electron_marker(pos)
                for pos in a_negative_positions
            ]
        )

        b_positives = VGroup(
            *[
                positive_marker(pos)
                for pos in b_positive_positions
            ]
        )

        b_electrons = VGroup(
            *[
                electron_marker(pos)
                for pos in b_negative_positions
            ]
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(mob, scale=0.7)
                    for mob in VGroup(
                        a_positives,
                        a_electrons,
                        b_positives,
                        b_electrons
                    )
                ],
                lag_ratio=0.1
            ),
            run_time=1.2
        )

        self.wait(1.1)

        neutral_a = arabic_text(
            "متعادل",
            size=27,
            color=ACCENT
        ).move_to(
            material_a.get_center()
            + UP * 1.15
        )

        neutral_b = arabic_text(
            "متعادل",
            size=27,
            color=ACCENT
        ).move_to(
            material_b.get_center()
            + DOWN * 1.15
        )

        self.play(
            FadeIn(neutral_a),
            FadeIn(neutral_b),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 3 — CONTACT
        # ====================================================

        self.play(
            FadeOut(neutral_a),
            FadeOut(neutral_b),
            run_time=0.4
        )

        contact_title = arabic_text(
            "أولًا: تلامس",
            size=34,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.4
        )

        self.play(
            FadeIn(contact_title),
            run_time=0.7
        )

        # Move both bodies toward the center
        move_a = RIGHT * 1.35 + UP * 0.6
        move_b = LEFT * 1.35 + DOWN * 0.6

        self.play(
            material_a.animate.shift(move_a),
            label_a.animate.shift(move_a),
            a_positives.animate.shift(move_a),
            a_electrons.animate.shift(move_a),

            material_b.animate.shift(move_b),
            label_b.animate.shift(move_b),
            b_positives.animate.shift(move_b),
            b_electrons.animate.shift(move_b),
            run_time=1.3
        )

        self.wait(1.0)

        # ====================================================
        # PART 4 — ELECTRON TRANSFER DURING CONTACT
        # ====================================================

        transfer_note = arabic_text(
            "يمكن أن تنتقل بعض الإلكترونات بين السطحين",
            size=30,
            color=NEGATIVE
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeOut(contact_title),
            FadeIn(transfer_note),
            run_time=0.8
        )

        self.wait(0.8)

        # ----------------------------------------------------
        # Pick two electrons from A and move them to B
        # ----------------------------------------------------

        moving_electron_1 = a_electrons[1]
        moving_electron_2 = a_electrons[3]

        self.play(
            Indicate(
                moving_electron_1,
                color=NEGATIVE,
                scale_factor=1.4
            ),
            Indicate(
                moving_electron_2,
                color=NEGATIVE,
                scale_factor=1.4
            ),
            run_time=0.8
        )

        self.wait(0.5)

        target_1 = material_b.get_center() + LEFT * 0.75 + DOWN * 0.15
        target_2 = material_b.get_center() + RIGHT * 0.65 + DOWN * 0.20

        self.play(
            moving_electron_1.animate.move_to(target_1),
            moving_electron_2.animate.move_to(target_2),
            run_time=1.5,
            rate_func=smooth
        )

        self.wait(1.2)

        # ====================================================
        # PART 5 — SEPARATE
        # ====================================================

        separation_title = arabic_text(
            "ثم: انفصال",
            size=34,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.4
        )

        self.play(
            FadeOut(transfer_note),
            FadeIn(separation_title),
            run_time=0.7
        )

        self.play(
            material_a.animate.shift(
                LEFT * 1.35 + DOWN * 0.6
            ),
            label_a.animate.shift(
                LEFT * 1.35 + DOWN * 0.6
            ),
            a_positives.animate.shift(
                LEFT * 1.35 + DOWN * 0.6
            ),

            # Only the remaining A electrons move back with A.
            *[
                e.animate.shift(
                    LEFT * 1.35 + DOWN * 0.6
                )
                for i, e in enumerate(a_electrons)
                if i not in [1, 3]
            ],

            material_b.animate.shift(
                RIGHT * 1.35 + UP * 0.6
            ),
            label_b.animate.shift(
                RIGHT * 1.35 + UP * 0.6
            ),
            b_positives.animate.shift(
                RIGHT * 1.35 + UP * 0.6
            ),
            b_electrons.animate.shift(
                RIGHT * 1.35 + UP * 0.6
            ),

            # The transferred electrons now belong visually to B.
            moving_electron_1.animate.shift(
                RIGHT * 1.35 + UP * 0.6
            ),
            moving_electron_2.animate.shift(
                RIGHT * 1.35 + UP * 0.6
            ),
            run_time=1.3
        )

        self.wait(1.0)

        # ====================================================
        # PART 6 — RESULT AFTER ONE CONTACT
        # ====================================================

        self.play(
            FadeOut(separation_title),
            run_time=0.4
        )

        a_result = arabic_text(
            "فقد إلكترونات",
            size=28,
            color=POSITIVE
        ).move_to(
            material_a.get_center()
            + UP * 1.25
        )

        b_result = arabic_text(
            "اكتسب إلكترونات",
            size=28,
            color=NEGATIVE
        ).move_to(
            material_b.get_center()
            + DOWN * 1.25
        )

        self.play(
            FadeIn(a_result),
            FadeIn(b_result),
            run_time=0.8
        )

        self.wait(1.2)

        a_charge = arabic_text(
            "أكثر إيجابية",
            size=30,
            weight=BOLD,
            color=POSITIVE
        ).next_to(
            a_result,
            UP,
            buff=0.18
        )

        b_charge = arabic_text(
            "أكثر سلبية",
            size=30,
            weight=BOLD,
            color=NEGATIVE
        ).next_to(
            b_result,
            DOWN,
            buff=0.18
        )

        self.play(
            FadeIn(a_charge),
            FadeIn(b_charge),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 7 — IMPORTANT CLARIFICATION
        # ====================================================

        self.play(
            FadeOut(a_result),
            FadeOut(b_result),
            FadeOut(a_charge),
            FadeOut(b_charge),
            run_time=0.6
        )

        dependency_note_1 = arabic_text(
            "أي مادة تكتسب الإلكترونات؟",
            size=34,
            weight=BOLD
        ).move_to(
            UP * 0.3
        )

        dependency_note_2 = arabic_text(
            "يعتمد ذلك على طبيعة المادتين وحالة السطح",
            size=31,
            color=TEXT_SECONDARY
        ).next_to(
            dependency_note_1,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(dependency_note_1),
            run_time=0.8
        )

        self.wait(0.7)

        self.play(
            FadeIn(dependency_note_2),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 8 — PREPARE FOR RUBBING
        # ====================================================

        self.play(
            FadeOut(dependency_note_1),
            FadeOut(dependency_note_2),
            FadeOut(subtitle),
            run_time=0.6
        )

        self.play(
            FadeOut(
                VGroup(
                    material_a,
                    material_b,
                    label_a,
                    label_b,
                    a_positives,
                    a_electrons,
                    b_positives,
                    b_electrons
                )
            ),
            run_time=0.8
        )

        # ====================================================
        # PART 9 — RUBBING = REPEATED CONTACT / SEPARATION
        # ====================================================

        rubbing_title = arabic_text(
            "ماذا يضيف الفرك؟",
            size=41,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(rubbing_title),
            run_time=0.8
        )

        self.wait(0.8)

        # ----------------------------------------------------
        # New simplified surfaces
        # ----------------------------------------------------

        lower_surface = RoundedRectangle(
            width=6.5,
            height=1.15,
            corner_radius=0.18,
            stroke_width=3,
            stroke_color=MATERIAL_A,
            fill_color=MATERIAL_A,
            fill_opacity=0.12
        ).move_to(
            DOWN * 0.75
        )

        upper_surface = RoundedRectangle(
            width=3.4,
            height=1.0,
            corner_radius=0.18,
            stroke_width=3,
            stroke_color=MATERIAL_B,
            fill_color=MATERIAL_B,
            fill_opacity=0.15
        ).move_to(
            UP * 0.45 + LEFT * 1.3
        )

        self.play(
            FadeIn(lower_surface),
            FadeIn(upper_surface),
            run_time=0.8
        )

        contact_text = arabic_text(
            "تلامس",
            size=28,
            color=ACCENT
        ).move_to(
            LEFT * 3.8 + DOWN * 2.25
        )

        separation_text = arabic_text(
            "انفصال",
            size=28,
            color=ACCENT
        ).move_to(
            ORIGIN + DOWN * 2.25
        )

        repeat_text = arabic_text(
            "وتكرار...",
            size=28,
            color=ACCENT
        ).move_to(
            RIGHT * 3.8 + DOWN * 2.25
        )

        # ====================================================
        # PART 10 — REPEATED MOTION
        # ====================================================

        self.play(
            FadeIn(contact_text),
            run_time=0.5
        )

        # Touch surface
        self.play(
            upper_surface.animate.shift(
                DOWN * 0.62
            ),
            run_time=0.6
        )

        self.wait(0.3)

        self.play(
            FadeIn(separation_text),
            run_time=0.5
        )

        self.play(
            upper_surface.animate.shift(
                UP * 0.62 + RIGHT * 1.3
            ),
            run_time=0.7
        )

        self.wait(0.3)

        self.play(
            FadeIn(repeat_text),
            run_time=0.5
        )

        # Repeated rubbing movement
        self.play(
            upper_surface.animate.shift(
                LEFT * 2.6 + DOWN * 0.62
            ),
            run_time=0.6
        )

        self.play(
            upper_surface.animate.shift(
                RIGHT * 3.0
            ),
            run_time=0.55
        )

        self.play(
            upper_surface.animate.shift(
                LEFT * 3.0
            ),
            run_time=0.55
        )

        self.play(
            upper_surface.animate.shift(
                RIGHT * 3.0
            ),
            run_time=0.55
        )

        self.play(
            upper_surface.animate.shift(
                LEFT * 1.0 + UP * 0.62
            ),
            run_time=0.6
        )

        self.wait(0.8)

        # ====================================================
        # PART 11 — EXPLAIN WHAT RUBBING DOES
        # ====================================================

        self.play(
            FadeOut(contact_text),
            FadeOut(separation_text),
            FadeOut(repeat_text),
            run_time=0.5
        )

        rubbing_explanation_1 = arabic_text(
            "الفرك يكرر التلامس والانفصال",
            size=35,
            weight=BOLD
        ).move_to(
            UP * 2.0
        )

        self.play(
            FadeOut(rubbing_title),
            FadeIn(rubbing_explanation_1),
            run_time=0.8
        )

        self.wait(0.8)

        rubbing_explanation_2 = arabic_text(
            "على مناطق كثيرة من السطح",
            size=32,
            color=TEXT_SECONDARY
        ).next_to(
            rubbing_explanation_1,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(rubbing_explanation_2),
            run_time=0.8
        )

        self.wait(1.4)

        rubbing_explanation_3 = arabic_text(
            "لذلك يمكن أن تنتقل إلكترونات أكثر",
            size=33,
            weight=BOLD,
            color=NEGATIVE
        ).to_edge(
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(rubbing_explanation_3),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 12 — CHARGE IS NOT CREATED
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    lower_surface,
                    upper_surface,
                    rubbing_explanation_1,
                    rubbing_explanation_2,
                    rubbing_explanation_3
                )
            ),
            run_time=0.8
        )

        important_title = arabic_text(
            "نقطة مهمة",
            size=40,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.55
        )

        self.play(
            FadeIn(important_title),
            run_time=0.7
        )

        self.wait(0.5)

        wrong_text = arabic_text(
            "الاحتكاك يصنع الشحنة",
            size=36
        ).move_to(
            UP * 0.5
        )

        self.play(
            FadeIn(wrong_text),
            run_time=0.7
        )

        wrong_cross = Cross(
            wrong_text,
            stroke_width=6,
            color="#FF6B6B"
        )

        self.play(
            Create(wrong_cross),
            run_time=0.7
        )

        self.wait(1.0)

        correct_text_1 = arabic_text(
            "الشحنة موجودة أصلًا",
            size=34,
            weight=BOLD
        ).move_to(
            DOWN * 0.6
        )

        correct_text_2 = arabic_text(
            "والإلكترونات تنتقل بين المادتين",
            size=35,
            weight=BOLD,
            color=NEGATIVE
        ).next_to(
            correct_text_1,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(correct_text_1),
            run_time=0.7
        )

        self.play(
            FadeIn(correct_text_2),
            run_time=0.7
        )

        self.wait(1.8)

        # ====================================================
        # PART 13 — FINAL SUMMARY
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    important_title,
                    wrong_text,
                    wrong_cross,
                    correct_text_1,
                    correct_text_2
                )
            ),
            run_time=0.8
        )

        summary_title = arabic_text(
            "الشحن بالاحتكاك",
            size=42,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.5
        )

        step_1 = arabic_text(
            "1. مادتان مختلفتان تتلامسان",
            size=32
        ).shift(
            UP * 0.7
        )

        step_2 = arabic_text(
            "2. تنتقل بعض الإلكترونات",
            size=32,
            color=NEGATIVE
        ).next_to(
            step_1,
            DOWN,
            buff=0.35
        )

        step_3 = arabic_text(
            "3. تنفصل المادتان بشحنتين غير متوازنتين",
            size=32
        ).next_to(
            step_2,
            DOWN,
            buff=0.35
        )

        step_4 = arabic_text(
            "الفرك يكرر هذه العملية مرات كثيرة",
            size=32,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            step_3,
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(summary_title),
            run_time=0.7
        )

        self.play(
            FadeIn(step_1),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(step_2),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(step_3),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(step_4),
            run_time=0.7
        )

        self.wait(1.8)

        # ====================================================
        # PART 14 — TRANSITION TO DAILY-LIFE EXAMPLE
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    summary_title,
                    step_1,
                    step_2,
                    step_3,
                    step_4
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "ويمكن أن نشعر بنتيجة هذه العملية",
            size=35
        ).shift(
            UP * 0.35
        )

        transition_2 = arabic_text(
            "في موقف يومي مألوف جدًا",
            size=38,
            weight=BOLD
        ).next_to(
            transition_1,
            DOWN,
            buff=0.25
        )

        transition_3 = arabic_text(
            "المشي على السجادة... ثم لمس مقبض الباب",
            size=31,
            color=ACCENT
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

    config.output_file = "scene_07_charging_by_friction"

    config.preview = True
    config.quality = "high_quality"

    Scene07ChargingByFriction().render()