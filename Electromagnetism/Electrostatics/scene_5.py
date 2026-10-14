from manim import *


# ============================================================
# Scene 05
# حفظ الشحنة الكهربائية
#
# الفكرة:
# - الشحنة يمكن أن تنتقل بين الأجسام.
# - لا تُخلق الشحنة ولا تختفي في نظام معزول.
# - الذي يبقى ثابتًا هو الشحنة الكلية للنظام،
#   وليس بالضرورة شحنة كل جسم منفرد.
#
# المثال:
# البداية:
# A = +4 μC
# B = +8 μC
# Q_total = +12 μC
#
# تنتقل شحنة سالبة مقدارها -6 μC من A إلى B
#
# النهاية:
# A = +10 μC
# B = +2 μC
# Q_total = +12 μC
#
# ثم فقط يظهر قانون الحفظ:
# Q_total, initial = Q_total, final
# ============================================================


class Scene05ConservationOfCharge(Scene):

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

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "هل يمكن أن تظهر الشحنة أو تختفي؟",
            size=44,
            weight=BOLD
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.15
            ),
            run_time=1.0
        )

        self.wait(1.8)

        self.play(
            title.animate.to_edge(
                UP,
                buff=0.45
            ).scale(0.82),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — TWO OBJECTS
        # ====================================================

        object_a = Circle(
            radius=1.15,
            stroke_width=4,
            stroke_color=POSITIVE,
            fill_color=POSITIVE,
            fill_opacity=0.08
        ).shift(
            LEFT * 3.4 + DOWN * 0.15
        )

        object_b = Circle(
            radius=1.15,
            stroke_width=4,
            stroke_color=POSITIVE,
            fill_color=POSITIVE,
            fill_opacity=0.08
        ).shift(
            RIGHT * 3.4 + DOWN * 0.15
        )

        label_a = Text(
            "A",
            font_size=32,
            weight=BOLD,
            color=TEXT_SECONDARY
        ).next_to(
            object_a,
            UP,
            buff=0.2
        )

        label_b = Text(
            "B",
            font_size=32,
            weight=BOLD,
            color=TEXT_SECONDARY
        ).next_to(
            object_b,
            UP,
            buff=0.2
        )

        self.play(
            FadeIn(object_a),
            FadeIn(object_b),
            FadeIn(label_a),
            FadeIn(label_b),
            run_time=1.0
        )

        self.wait(1.0)

        # ====================================================
        # PART 3 — INITIAL CHARGES
        # ====================================================

        charge_a_initial = MathTex(
            "+4",
            r"\,\mu\mathrm{C}",
            font_size=58,
            color=POSITIVE
        ).move_to(
            object_a
        )

        charge_b_initial = MathTex(
            "+8",
            r"\,\mu\mathrm{C}",
            font_size=58,
            color=POSITIVE
        ).move_to(
            object_b
        )

        initial_text = arabic_text(
            "في البداية",
            size=31,
            color=TEXT_SECONDARY
        ).move_to(
            UP * 2.0
        )

        self.play(
            FadeIn(initial_text),
            run_time=0.7
        )

        self.play(
            FadeIn(
                charge_a_initial,
                scale=0.8
            ),
            run_time=0.8
        )

        self.wait(0.6)

        self.play(
            FadeIn(
                charge_b_initial,
                scale=0.8
            ),
            run_time=0.8
        )

        self.wait(1.2)

        # ====================================================
        # PART 4 — FIND THE INITIAL TOTAL
        # ====================================================

        plus_sign = MathTex(
            "+",
            font_size=48,
            color=TEXT_SECONDARY
        ).move_to(
            DOWN * 0.15
        )

        self.play(
            FadeIn(plus_sign),
            run_time=0.5
        )

        self.wait(0.5)

        total_initial_expression = MathTex(
            "+4",
            "+",
            "8",
            "=",
            "+12",
            r"\,\mu\mathrm{C}",
            font_size=48
        ).to_edge(
            DOWN,
            buff=0.55
        )

        total_initial_expression[0].set_color(POSITIVE)
        total_initial_expression[2].set_color(POSITIVE)
        total_initial_expression[4].set_color(ACCENT)
        total_initial_expression[5].set_color(ACCENT)

        self.play(
            FadeIn(
                total_initial_expression,
                shift=UP * 0.1
            ),
            run_time=0.9
        )

        self.wait(1.4)

        total_box = SurroundingRectangle(
            VGroup(
                total_initial_expression[4],
                total_initial_expression[5]
            ),
            buff=0.12,
            color=ACCENT,
            stroke_width=3
        )

        self.play(
            Create(total_box),
            run_time=0.6
        )

        self.wait(1.3)

        # ====================================================
        # PART 5 — KEEP THE TOTAL VISIBLE
        # ====================================================

        total_tracker_box = RoundedRectangle(
            width=3.7,
            height=1.15,
            corner_radius=0.18,
            stroke_width=3,
            stroke_color=ACCENT,
            fill_color=ACCENT,
            fill_opacity=0.05
        ).move_to(
            DOWN * 2.55
        )

        total_tracker_title = arabic_text(
            "الشحنة الكلية",
            size=24,
            color=TEXT_SECONDARY
        ).move_to(
            total_tracker_box.get_center() + UP * 0.25
        )

        total_tracker_value = MathTex(
            "+12",
            r"\,\mu\mathrm{C}",
            font_size=40,
            color=ACCENT
        ).move_to(
            total_tracker_box.get_center() + DOWN * 0.22
        )

        total_tracker = VGroup(
            total_tracker_box,
            total_tracker_title,
            total_tracker_value
        )

        self.play(
            FadeOut(total_box),
            FadeOut(total_initial_expression),
            FadeOut(plus_sign),
            FadeIn(total_tracker),
            run_time=0.9
        )

        self.wait(1.2)

        # ====================================================
        # PART 6 — CHARGE TRANSFER
        # ====================================================

        self.play(
            FadeOut(initial_text),
            run_time=0.4
        )

        transfer_title = arabic_text(
            "الآن تنتقل شحنة بين الجسمين",
            size=35,
            weight=BOLD
        ).move_to(
            UP * 2.0
        )

        self.play(
            FadeIn(transfer_title),
            run_time=0.8
        )

        self.wait(1.0)

        # ----------------------------------------------------
        # Negative charge packet:
        # moving -6 μC from A to B
        #
        # Removing negative charge from A:
        # +4 -> +10
        #
        # Adding negative charge to B:
        # +8 -> +2
        # ----------------------------------------------------

        negative_packet = RoundedRectangle(
            width=2.1,
            height=0.9,
            corner_radius=0.2,
            stroke_width=3,
            stroke_color=NEGATIVE,
            fill_color=NEGATIVE,
            fill_opacity=0.12
        ).move_to(
            object_a.get_center() + RIGHT * 0.15
        )

        packet_label = MathTex(
            "-6",
            r"\,\mu\mathrm{C}",
            font_size=38,
            color=NEGATIVE
        ).move_to(
            negative_packet
        )

        packet_group = VGroup(
            negative_packet,
            packet_label
        )

        transfer_label = arabic_text(
            "شحنة سالبة تنتقل",
            size=29,
            color=NEGATIVE
        ).next_to(
            packet_group,
            UP,
            buff=0.25
        )

        # Fade original A value slightly
        self.play(
            charge_a_initial.animate.set_opacity(0.35),
            run_time=0.5
        )

        self.play(
            FadeIn(packet_group),
            FadeIn(transfer_label),
            run_time=0.7
        )

        self.wait(0.9)

        # Arrow showing actual transfer direction
        transfer_arrow = Arrow(
            start=object_a.get_right() + RIGHT * 0.2,
            end=object_b.get_left() + LEFT * 0.2,
            buff=0,
            color=NEGATIVE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.12
        ).shift(
            UP * 0.35
        )

        self.play(
            GrowArrow(transfer_arrow),
            run_time=0.8
        )

        self.wait(0.7)

        # Move packet to B
        self.play(
            packet_group.animate.move_to(
                object_b.get_center() + LEFT * 0.15
            ),
            transfer_label.animate.next_to(
                object_b,
                UP,
                buff=0.55
            ),
            run_time=1.8,
            rate_func=smooth
        )

        self.wait(0.8)

        # ====================================================
        # PART 7 — UPDATE OBJECT A
        # ====================================================

        charge_a_final = MathTex(
            "+10",
            r"\,\mu\mathrm{C}",
            font_size=58,
            color=POSITIVE
        ).move_to(
            object_a
        )

        a_explanation = arabic_text(
            "فقد شحنة سالبة",
            size=25,
            color=NEGATIVE
        ).next_to(
            object_a,
            DOWN,
            buff=0.28
        )

        self.play(
            ReplacementTransform(
                charge_a_initial,
                charge_a_final
            ),
            FadeIn(a_explanation),
            run_time=0.9
        )

        self.wait(1.0)

        # ====================================================
        # PART 8 — UPDATE OBJECT B
        # ====================================================

        charge_b_final = MathTex(
            "+2",
            r"\,\mu\mathrm{C}",
            font_size=58,
            color=POSITIVE
        ).move_to(
            object_b
        )

        b_explanation = arabic_text(
            "اكتسب شحنة سالبة",
            size=25,
            color=NEGATIVE
        ).next_to(
            object_b,
            DOWN,
            buff=0.28
        )

        self.play(
            FadeOut(packet_group),
            FadeOut(transfer_label),
            ReplacementTransform(
                charge_b_initial,
                charge_b_final
            ),
            FadeIn(b_explanation),
            run_time=0.9
        )

        self.wait(1.1)

        self.play(
            FadeOut(transfer_arrow),
            run_time=0.5
        )

        # ====================================================
        # PART 9 — IMPORTANT OBSERVATION
        # ====================================================

        observation = arabic_text(
            "شحنة كل جسم تغيّرت",
            size=32,
            weight=BOLD
        ).move_to(
            UP * 2.0
        )

        self.play(
            FadeOut(transfer_title),
            FadeIn(observation),
            run_time=0.7
        )

        self.wait(1.1)

        observation_2 = arabic_text(
            "لكن ماذا حدث للمجموع؟",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            observation,
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(observation_2),
            run_time=0.7
        )

        self.wait(1.3)

        # ====================================================
        # PART 10 — CALCULATE FINAL TOTAL
        # ====================================================

        final_calculation = MathTex(
            "+10",
            "+",
            "2",
            "=",
            "+12",
            r"\,\mu\mathrm{C}",
            font_size=48
        ).move_to(
            DOWN * 1.72
        )

        final_calculation[0].set_color(POSITIVE)
        final_calculation[2].set_color(POSITIVE)
        final_calculation[4].set_color(ACCENT)
        final_calculation[5].set_color(ACCENT)

        # Move tracker slightly lower to create space
        self.play(
            total_tracker.animate.shift(
                DOWN * 0.45
            ),
            run_time=0.5
        )

        self.play(
            FadeIn(
                final_calculation,
                shift=UP * 0.1
            ),
            run_time=0.9
        )

        self.wait(1.2)

        final_box = SurroundingRectangle(
            VGroup(
                final_calculation[4],
                final_calculation[5]
            ),
            buff=0.12,
            color=ACCENT,
            stroke_width=3
        )

        self.play(
            Create(final_box),
            Indicate(
                total_tracker_value,
                color=ACCENT,
                scale_factor=1.12
            ),
            run_time=0.9
        )

        self.wait(1.5)

        # ====================================================
        # PART 11 — BEFORE / AFTER COMPARISON
        # ====================================================

        self.play(
            FadeOut(observation),
            FadeOut(observation_2),
            FadeOut(a_explanation),
            FadeOut(b_explanation),
            FadeOut(final_box),
            FadeOut(final_calculation),
            FadeOut(total_tracker),
            FadeOut(label_a),
            FadeOut(label_b),
            run_time=0.7
        )

        # Reposition final objects for comparison
        self.play(
            object_a.animate.scale(0.72).move_to(
                LEFT * 2.0 + DOWN * 0.45
            ),
            object_b.animate.scale(0.72).move_to(
                RIGHT * 2.0 + DOWN * 0.45
            ),
            charge_a_final.animate.scale(0.78).move_to(
                LEFT * 2.0 + DOWN * 0.45
            ),
            charge_b_final.animate.scale(0.78).move_to(
                RIGHT * 2.0 + DOWN * 0.45
            ),
            run_time=0.8
        )

        after_title = arabic_text(
            "بعد انتقال الشحنة",
            size=31,
            color=TEXT_SECONDARY
        ).move_to(
            UP * 1.1
        )

        self.play(
            FadeIn(after_title),
            run_time=0.6
        )

        self.wait(0.8)

        after_total = MathTex(
            "Q_{\\text{total}}",
            "=",
            "+12",
            r"\,\mu\mathrm{C}",
            font_size=47
        ).move_to(
            DOWN * 2.0
        )

        after_total[2].set_color(ACCENT)
        after_total[3].set_color(ACCENT)

        self.play(
            FadeIn(after_total),
            run_time=0.8
        )

        self.wait(1.3)

        # ====================================================
        # PART 12 — BUILD CONSERVATION LAW
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    object_a,
                    object_b,
                    charge_a_final,
                    charge_b_final,
                    after_title,
                    after_total
                )
            ),
            run_time=0.8
        )

        conclusion_1 = arabic_text(
            "الشحنة انتقلت من مكان إلى آخر",
            size=36
        ).shift(
            UP * 1.15
        )

        conclusion_2 = arabic_text(
            "لكن الشحنة الكلية بقيت ثابتة",
            size=38,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            conclusion_1,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(conclusion_1),
            run_time=0.8
        )

        self.wait(0.8)

        self.play(
            FadeIn(conclusion_2),
            run_time=0.8
        )

        self.wait(1.4)

        self.play(
            VGroup(
                conclusion_1,
                conclusion_2
            ).animate.shift(
                UP * 0.7
            ),
            run_time=0.6
        )

        initial_total = MathTex(
            "Q_{\\text{total, initial}}",
            font_size=48
        ).move_to(
            LEFT * 2.8 + DOWN * 0.55
        )

        final_total = MathTex(
            "Q_{\\text{total, final}}",
            font_size=48
        ).move_to(
            RIGHT * 2.8 + DOWN * 0.55
        )

        self.play(
            FadeIn(initial_total),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(final_total),
            run_time=0.7
        )

        self.wait(0.6)

        equals_sign = MathTex(
            "=",
            font_size=58,
            color=ACCENT
        ).move_to(
            DOWN * 0.55
        )

        self.play(
            FadeIn(
                equals_sign,
                scale=0.7
            ),
            run_time=0.6
        )

        self.wait(1.5)

        # ====================================================
        # PART 13 — NAME THE LAW
        # ====================================================

        law_box = SurroundingRectangle(
            VGroup(
                initial_total,
                equals_sign,
                final_total
            ),
            buff=0.3,
            stroke_width=3,
            color=ACCENT
        )

        law_name = arabic_text(
            "قانون حفظ الشحنة",
            size=36,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            law_box,
            DOWN,
            buff=0.38
        )

        self.play(
            Create(law_box),
            run_time=0.7
        )

        self.play(
            FadeIn(law_name),
            run_time=0.7
        )

        self.wait(1.8)

        isolated_note = arabic_text(
            "في نظام معزول",
            size=27,
            color=TEXT_SECONDARY
        ).next_to(
            law_name,
            DOWN,
            buff=0.22
        )

        self.play(
            FadeIn(isolated_note),
            run_time=0.6
        )

        self.wait(1.6)

        # ====================================================
        # PART 14 — IMPORTANT CLARIFICATION
        # ====================================================

        self.play(
            FadeOut(conclusion_1),
            FadeOut(conclusion_2),
            FadeOut(law_box),
            FadeOut(law_name),
            FadeOut(isolated_note),
            FadeOut(initial_total),
            FadeOut(equals_sign),
            FadeOut(final_total),
            run_time=0.8
        )

        clarification_1 = arabic_text(
            "شحنة كل جسم يمكن أن تتغير",
            size=38,
            weight=BOLD
        ).shift(
            UP * 0.55
        )

        clarification_2 = arabic_text(
            "لكن مجموع الشحنة في النظام المعزول لا يتغير",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            clarification_1,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(clarification_1),
            run_time=0.8
        )

        self.wait(0.8)

        self.play(
            FadeIn(clarification_2),
            run_time=0.8
        )

        self.wait(1.8)

        # ====================================================
        # PART 15 — TRANSITION TO QUANTIZATION
        # ====================================================

        self.play(
            FadeOut(clarification_1),
            FadeOut(clarification_2),
            run_time=0.7
        )

        transition_1 = arabic_text(
            "لكن هل يمكن للشحنة أن تأخذ",
            size=35
        ).shift(
            UP * 0.35
        )

        transition_2 = arabic_text(
            "أي قيمة نريدها؟",
            size=40,
            weight=BOLD
        ).next_to(
            transition_1,
            DOWN,
            buff=0.25
        )

        transition_3 = arabic_text(
            "الإجابة تقودنا إلى تكميم الشحنة",
            size=31,
            color=NEGATIVE
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

    config.output_file = "scene_05_conservation_of_charge"

    config.preview = True
    config.quality = "high_quality"

    Scene05ConservationOfCharge().render()