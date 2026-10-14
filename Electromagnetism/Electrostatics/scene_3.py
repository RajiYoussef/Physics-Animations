from manim import *


# ============================================================
# Scene 03
# التعادل الكهربائي والشحنة الصافية
#
# الأفكار:
# - الجسم المتعادل: الشحنة الموجبة والسالبة متوازنتان.
# - اكتساب إلكترونات -> شحنة سالبة.
# - فقد إلكترونات -> شحنة موجبة.
# - في شحن الأجسام الصلبة عادةً الإلكترونات هي التي تنتقل،
#   بينما تبقى البروتونات مرتبطة داخل الأنوية.
#
# الرسم تمثيل مبسط لموازنة الشحنات داخل جسم.
# ============================================================


class Scene03NeutralPositiveNegative(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        # ----------------------------------------------------
        # Color palette — consistent with previous scenes
        # ----------------------------------------------------

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"
        NEUTRAL = "#B7C0CC"
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
        # HELPER FUNCTIONS
        # ====================================================

        def positive_charge(position):

            circle = Circle(
                radius=0.18,
                stroke_width=2.5,
                color=POSITIVE,
                fill_color=POSITIVE,
                fill_opacity=0.18
            ).move_to(position)

            sign = Text(
                "+",
                font_size=22,
                weight=BOLD,
                color=POSITIVE
            ).move_to(position)

            return VGroup(circle, sign)

        def electron(position):

            circle = Circle(
                radius=0.16,
                stroke_width=2.5,
                color=NEGATIVE,
                fill_color=NEGATIVE,
                fill_opacity=0.22
            ).move_to(position)

            sign = Text(
                "−",
                font_size=21,
                weight=BOLD,
                color=NEGATIVE
            ).move_to(position)

            return VGroup(circle, sign)

        # ====================================================
        # PART 1 — OPENING QUESTION
        # ====================================================

        title = arabic_text(
            "متى يكون الجسم متعادلًا أو مشحونًا؟",
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
            ).scale(0.8),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — NEUTRAL OBJECT
        # ====================================================

        body = RoundedRectangle(
            width=6.2,
            height=3.4,
            corner_radius=0.3,
            stroke_width=3,
            stroke_color=NEUTRAL,
            fill_color=NEUTRAL,
            fill_opacity=0.035
        ).shift(
            DOWN * 0.15
        )

        self.play(
            FadeIn(body),
            run_time=0.8
        )

        # ----------------------------------------------------
        # Simplified fixed positive charges
        # ----------------------------------------------------

        positive_positions = [
            [-2.1, 0.75, 0],
            [-0.7, 0.75, 0],
            [0.7, 0.75, 0],
            [2.1, 0.75, 0],
            [-1.4, -0.60, 0],
            [1.4, -0.60, 0],
        ]

        positives = VGroup(
            *[
                positive_charge(pos)
                for pos in positive_positions
            ]
        )

        # ----------------------------------------------------
        # Equal number of electrons
        # ----------------------------------------------------

        electron_positions = [
            [-1.75, 0.15, 0],
            [-0.35, 0.15, 0],
            [1.05, 0.15, 0],
            [2.35, 0.15, 0],
            [-2.15, -1.05, 0],
            [0.15, -1.05, 0],
        ]

        electrons = VGroup(
            *[
                electron(pos)
                for pos in electron_positions
            ]
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(p, scale=0.6)
                    for p in positives
                ],
                lag_ratio=0.08
            ),
            run_time=1.1
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(e, scale=0.6)
                    for e in electrons
                ],
                lag_ratio=0.08
            ),
            run_time=1.1
        )

        self.wait(1.2)

        simplified_note = arabic_text(
            "تمثيل مبسط لتوازن الشحنات",
            size=24,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(simplified_note),
            run_time=0.6
        )

        self.wait(1.0)

        # ====================================================
        # PART 3 — COUNT BOTH TYPES
        # ====================================================

        positive_counter = VGroup(
            Text(
                "+",
                font_size=34,
                weight=BOLD,
                color=POSITIVE
            ),
            Text(
                "6",
                font_size=34,
                weight=BOLD,
                color=POSITIVE
            )
        ).arrange(
            RIGHT,
            buff=0.15
        ).move_to(
            LEFT * 1.3 + DOWN * 2.25
        )

        negative_counter = VGroup(
            Text(
                "−",
                font_size=34,
                weight=BOLD,
                color=NEGATIVE
            ),
            Text(
                "6",
                font_size=34,
                weight=BOLD,
                color=NEGATIVE
            )
        ).arrange(
            RIGHT,
            buff=0.15
        ).move_to(
            RIGHT * 1.3 + DOWN * 2.25
        )

        self.play(
            FadeOut(simplified_note),
            FadeIn(positive_counter),
            FadeIn(negative_counter),
            run_time=0.8
        )

        self.wait(1.1)

        balance_text = arabic_text(
            "الشحنة الموجبة = الشحنة السالبة",
            size=32
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeOut(positive_counter),
            FadeOut(negative_counter),
            FadeIn(balance_text),
            run_time=0.8
        )

        self.wait(1.3)

        # ====================================================
        # PART 4 — NEUTRAL
        # ====================================================

        neutral_label = arabic_text(
            "متعادل كهربائيًا",
            size=38,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            UP * 2.0
        )

        net_zero = MathTex(
            "Q_{\\text{net}}",
            "=",
            "0",
            font_size=56,
            color=ACCENT
        ).next_to(
            neutral_label,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeOut(title),
            FadeOut(balance_text),
            FadeIn(neutral_label),
            run_time=0.8
        )

        self.wait(0.7)

        self.play(
            FadeIn(net_zero),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 5 — ELECTRONS CAN MOVE
        # ====================================================

        self.play(
            FadeOut(neutral_label),
            FadeOut(net_zero),
            run_time=0.5
        )

        movement_title = arabic_text(
            "ما الذي يمكن أن يغيّر هذا التوازن؟",
            size=38,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(movement_title),
            run_time=0.8
        )

        self.wait(1.1)

        # Highlight an electron
        self.play(
            Indicate(
                electrons[1],
                color=NEGATIVE,
                scale_factor=1.5
            ),
            run_time=0.9
        )

        electron_move_text = arabic_text(
            "الإلكترونات الخارجية يمكن أن تنتقل",
            size=32,
            color=NEGATIVE
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(electron_move_text),
            run_time=0.8
        )

        self.wait(1.4)

        # Highlight positive charges but keep them fixed
        self.play(
            Indicate(
                positives,
                color=POSITIVE,
                scale_factor=1.05
            ),
            run_time=0.8
        )

        proton_fixed_text = arabic_text(
            "أما البروتونات فتبقى مرتبطة داخل الأنوية",
            size=30,
            color=POSITIVE
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeOut(electron_move_text),
            FadeIn(proton_fixed_text),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 6 — GAIN ELECTRONS
        # ====================================================

        self.play(
            FadeOut(movement_title),
            FadeOut(proton_fixed_text),
            run_time=0.6
        )

        gain_title = arabic_text(
            "ماذا لو اكتسب الجسم إلكترونات؟",
            size=38,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(gain_title),
            run_time=0.8
        )

        self.wait(1.0)

        # ----------------------------------------------------
        # Two new electrons begin outside body
        # ----------------------------------------------------

        new_electron_1 = electron(
            RIGHT * 5.2 + UP * 0.5
        )

        new_electron_2 = electron(
            RIGHT * 5.2 + DOWN * 0.5
        )

        self.play(
            FadeIn(new_electron_1),
            FadeIn(new_electron_2),
            run_time=0.6
        )

        self.wait(0.5)

        # Move into body
        self.play(
            new_electron_1.animate.move_to(
                [1.55, 0.10, 0]
            ),
            new_electron_2.animate.move_to(
                [-0.95, -1.05, 0]
            ),
            run_time=1.6
        )

        self.wait(1.0)

        acquired_text = arabic_text(
            "إلكترونات إضافية",
            size=31,
            color=NEGATIVE
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(acquired_text),
            run_time=0.7
        )

        self.wait(1.0)

        # ====================================================
        # PART 7 — NEGATIVE BODY
        # ====================================================

        negative_label = arabic_text(
            "الشحنات السالبة أصبحت أكثر",
            size=32
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeOut(acquired_text),
            FadeIn(negative_label),
            run_time=0.7
        )

        self.wait(1.1)

        negative_result = arabic_text(
            "الجسم أصبح سالب الشحنة",
            size=38,
            weight=BOLD,
            color=NEGATIVE
        ).move_to(
            UP * 2.0
        )

        self.play(
            FadeOut(gain_title),
            FadeIn(negative_result),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 8 — RESET TO NEUTRAL
        # ====================================================

        reset_text = arabic_text(
            "نعود إلى الجسم المتعادل",
            size=30,
            color=TEXT_SECONDARY
        ).to_edge(
            UP,
            buff=0.5
        )

        self.play(
            FadeOut(negative_result),
            FadeOut(negative_label),
            FadeIn(reset_text),
            run_time=0.6
        )

        self.play(
            FadeOut(new_electron_1),
            FadeOut(new_electron_2),
            run_time=0.8
        )

        self.wait(1.1)

        self.play(
            FadeOut(reset_text),
            run_time=0.4
        )

        # ====================================================
        # PART 9 — LOSE ELECTRONS
        # ====================================================

        lose_title = arabic_text(
            "وماذا لو فقد الجسم بعض الإلكترونات؟",
            size=38,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(lose_title),
            run_time=0.8
        )

        self.wait(1.0)

        # Select two existing electrons to leave
        leaving_1 = electrons[0]
        leaving_2 = electrons[4]

        self.play(
            Indicate(
                leaving_1,
                color=NEGATIVE,
                scale_factor=1.4
            ),
            Indicate(
                leaving_2,
                color=NEGATIVE,
                scale_factor=1.4
            ),
            run_time=0.8
        )

        self.play(
            leaving_1.animate.move_to(
                LEFT * 5.2 + UP * 0.5
            ),
            leaving_2.animate.move_to(
                LEFT * 5.2 + DOWN * 0.5
            ),
            run_time=1.6
        )

        self.play(
            FadeOut(leaving_1),
            FadeOut(leaving_2),
            run_time=0.5
        )

        self.wait(0.7)

        lost_text = arabic_text(
            "فقد إلكترونات",
            size=31,
            color=NEGATIVE
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(lost_text),
            run_time=0.7
        )

        self.wait(1.0)

        # ====================================================
        # PART 10 — POSITIVE BODY
        # ====================================================

        positive_excess_text = arabic_text(
            "أصبحت الشحنة الموجبة هي الغالبة",
            size=31
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeOut(lost_text),
            FadeIn(positive_excess_text),
            run_time=0.7
        )

        self.wait(1.1)

        positive_result = arabic_text(
            "الجسم أصبح موجب الشحنة",
            size=38,
            weight=BOLD,
            color=POSITIVE
        ).move_to(
            UP * 2.0
        )

        self.play(
            FadeOut(lose_title),
            FadeIn(positive_result),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 11 — CLEAR MAIN DEMONSTRATION
        # ====================================================

        self.play(
            FadeOut(body),
            FadeOut(positives),
            FadeOut(electrons),
            FadeOut(positive_result),
            FadeOut(positive_excess_text),
            run_time=0.8
        )

        # ====================================================
        # PART 12 — FINAL THREE-STATE SUMMARY
        # ====================================================

        summary_title = arabic_text(
            "إذن لدينا ثلاث حالات",
            size=40,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(summary_title),
            run_time=0.8
        )

        self.wait(0.8)

        # ----------------------------------------------------
        # Neutral card
        # ----------------------------------------------------

        neutral_card = RoundedRectangle(
            width=3.7,
            height=2.7,
            corner_radius=0.22,
            stroke_width=3,
            stroke_color=ACCENT
        ).shift(
            LEFT * 4.1 + DOWN * 0.25
        )

        neutral_card_title = arabic_text(
            "متعادل",
            size=32,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            neutral_card.get_center() + UP * 0.65
        )

        neutral_card_symbol = VGroup(
            Text(
                "+",
                font_size=40,
                color=POSITIVE
            ),
            Text(
                "=",
                font_size=34,
                color=TEXT_MAIN
            ),
            Text(
                "−",
                font_size=40,
                color=NEGATIVE
            )
        ).arrange(
            RIGHT,
            buff=0.25
        ).move_to(
            neutral_card.get_center()
        )

        neutral_card_text = arabic_text(
            "توازن الشحنات",
            size=24
        ).move_to(
            neutral_card.get_center() + DOWN * 0.75
        )

        neutral_group = VGroup(
            neutral_card,
            neutral_card_title,
            neutral_card_symbol,
            neutral_card_text
        )

        # ----------------------------------------------------
        # Negative card
        # ----------------------------------------------------

        negative_card = RoundedRectangle(
            width=3.7,
            height=2.7,
            corner_radius=0.22,
            stroke_width=3,
            stroke_color=NEGATIVE
        ).shift(
            DOWN * 0.25
        )

        negative_card_title = arabic_text(
            "سالب",
            size=32,
            weight=BOLD,
            color=NEGATIVE
        ).move_to(
            negative_card.get_center() + UP * 0.65
        )

        negative_card_symbol = Text(
            "−  −",
            font_size=44,
            weight=BOLD,
            color=NEGATIVE
        ).move_to(
            negative_card.get_center()
        )

        negative_card_text = arabic_text(
            "اكتسب إلكترونات",
            size=24
        ).move_to(
            negative_card.get_center() + DOWN * 0.75
        )

        negative_group = VGroup(
            negative_card,
            negative_card_title,
            negative_card_symbol,
            negative_card_text
        )

        # ----------------------------------------------------
        # Positive card
        # ----------------------------------------------------

        positive_card = RoundedRectangle(
            width=3.7,
            height=2.7,
            corner_radius=0.22,
            stroke_width=3,
            stroke_color=POSITIVE
        ).shift(
            RIGHT * 4.1 + DOWN * 0.25
        )

        positive_card_title = arabic_text(
            "موجب",
            size=32,
            weight=BOLD,
            color=POSITIVE
        ).move_to(
            positive_card.get_center() + UP * 0.65
        )

        positive_card_symbol = Text(
            "+  +",
            font_size=44,
            weight=BOLD,
            color=POSITIVE
        ).move_to(
            positive_card.get_center()
        )

        positive_card_text = arabic_text(
            "فقد إلكترونات",
            size=24
        ).move_to(
            positive_card.get_center() + DOWN * 0.75
        )

        positive_group = VGroup(
            positive_card,
            positive_card_title,
            positive_card_symbol,
            positive_card_text
        )

        self.play(
            FadeIn(neutral_group),
            run_time=0.8
        )

        self.wait(0.6)

        self.play(
            FadeIn(negative_group),
            run_time=0.8
        )

        self.wait(0.6)

        self.play(
            FadeIn(positive_group),
            run_time=0.8
        )

        self.wait(1.8)

        # ====================================================
        # PART 13 — EMPHASIZE ELECTRON TRANSFER
        # ====================================================

        final_note = arabic_text(
            "في شحن الأجسام الصلبة: الإلكترونات هي التي تنتقل عادة",
            size=31,
            weight=BOLD,
            color=NEGATIVE
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(final_note),
            run_time=0.8
        )

        self.wait(1.8)

        # ====================================================
        # PART 14 — TRANSITION TO NEXT SCENE
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    summary_title,
                    neutral_group,
                    negative_group,
                    positive_group,
                    final_note
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "لكن ماذا يحدث عندما نقرّب",
            size=36
        ).shift(
            UP * 0.35
        )

        transition_2 = arabic_text(
            "جسمين مشحونين من بعضهما؟",
            size=38,
            weight=BOLD
        ).next_to(
            transition_1,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(transition_1),
            run_time=0.8
        )

        self.play(
            FadeIn(transition_2),
            run_time=0.8
        )

        self.wait(2.0)

        self.play(
            FadeOut(transition_1),
            FadeOut(transition_2),
            run_time=0.8
        )


# ============================================================
# DIRECT RENDERING FROM PYCHARM
# ============================================================

if __name__ == "__main__":

    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    config.output_file = "scene_03_neutral_positive_negative"

    config.preview = True
    config.quality = "high_quality"

    Scene03NeutralPositiveNegative().render()