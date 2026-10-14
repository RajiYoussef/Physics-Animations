from manim import *


# ============================================================
# Scene 12
# الموصلات والعوازل
#
# التصحيح:
# - بطاقتان منفصلتان وواضحتان للأمثلة.
# - جميع أمثلة الموصلات داخل بطاقة الموصلات فقط.
# - جميع أمثلة العوازل داخل بطاقة العوازل فقط.
# - استخدام VGroup + arrange بدل next_to المتكرر
#   لتجنب تداخل النص العربي.
# ============================================================


class Scene12ConductorsInsulators(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"
        ACCENT = "#7EE787"

        CONDUCTOR_COLOR = "#9DA7B3"
        INSULATOR_COLOR = "#C084FC"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

        DIVIDER_COLOR = "#30363D"

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
        # HELPER
        # ====================================================

        def electron_marker(position, radius=0.10):

            circle = Circle(
                radius=radius,
                stroke_width=2,
                stroke_color=NEGATIVE,
                fill_color=NEGATIVE,
                fill_opacity=0.20
            ).move_to(position)

            sign = Text(
                "−",
                font_size=15,
                weight=BOLD,
                color=NEGATIVE
            ).move_to(circle)

            return VGroup(circle, sign)

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "هل تتحرك الشحنات بالطريقة نفسها في كل المواد؟",
            size=42,
            weight=BOLD
        )

        self.play(
            FadeIn(title, shift=UP * 0.15),
            run_time=1.0
        )

        self.wait(1.7)

        answer = arabic_text(
            "لا",
            size=48,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            title,
            DOWN,
            buff=0.4
        )

        self.play(
            FadeIn(answer, scale=0.8),
            run_time=0.7
        )

        self.wait(1.1)

        self.play(
            FadeOut(answer),
            title.animate.to_edge(
                UP,
                buff=0.45
            ).scale(0.82),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — SPLIT SCREEN
        # ====================================================

        divider = Line(
            UP * 2.45,
            DOWN * 2.65,
            stroke_width=2,
            color=DIVIDER_COLOR
        )

        conductor_title = arabic_text(
            "موصل",
            size=39,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            LEFT * 3.4 + UP * 2.05
        )

        insulator_title = arabic_text(
            "عازل",
            size=39,
            weight=BOLD,
            color=INSULATOR_COLOR
        ).move_to(
            RIGHT * 3.4 + UP * 2.05
        )

        self.play(
            Create(divider),
            FadeIn(conductor_title),
            FadeIn(insulator_title),
            run_time=0.9
        )

        self.wait(1.0)

        # ====================================================
        # PART 3 — OBJECTS
        # ====================================================

        conductor = Circle(
            radius=1.30,
            stroke_width=4,
            stroke_color=CONDUCTOR_COLOR,
            fill_color=CONDUCTOR_COLOR,
            fill_opacity=0.08
        ).move_to(
            LEFT * 3.4 + DOWN * 0.05
        )

        insulator = Circle(
            radius=1.30,
            stroke_width=4,
            stroke_color=INSULATOR_COLOR,
            fill_color=INSULATOR_COLOR,
            fill_opacity=0.08
        ).move_to(
            RIGHT * 3.4 + DOWN * 0.05
        )

        self.play(
            FadeIn(conductor),
            FadeIn(insulator),
            run_time=0.9
        )

        self.wait(1.0)

        conductor_description = arabic_text(
            "الشحنة تتحرك بسهولة نسبيًا",
            size=26,
            color=ACCENT
        ).move_to(
            LEFT * 3.4 + DOWN * 1.75
        )

        insulator_description = arabic_text(
            "حركة الشحنة أكثر تقييدًا",
            size=26,
            color=TEXT_SECONDARY
        ).move_to(
            RIGHT * 3.4 + DOWN * 1.75
        )

        self.play(
            FadeIn(conductor_description),
            run_time=0.7
        )

        self.wait(0.6)

        self.play(
            FadeIn(insulator_description),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 4 — ADD EXCESS CHARGE
        # ====================================================

        self.play(
            FadeOut(conductor_description),
            FadeOut(insulator_description),
            run_time=0.5
        )

        experiment_title = arabic_text(
            "نضع شحنة سالبة زائدة في منطقة صغيرة من كل جسم",
            size=30,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(experiment_title),
            run_time=0.8
        )

        self.wait(0.8)

        conductor_charges = VGroup(
            electron_marker(
                conductor.get_center() + LEFT * 0.62 + UP * 0.22
            ),
            electron_marker(
                conductor.get_center() + LEFT * 0.54
            ),
            electron_marker(
                conductor.get_center() + LEFT * 0.61 + DOWN * 0.23
            ),
            electron_marker(
                conductor.get_center() + LEFT * 0.82 + DOWN * 0.04
            )
        )

        insulator_charges = VGroup(
            electron_marker(
                insulator.get_center() + LEFT * 0.62 + UP * 0.22
            ),
            electron_marker(
                insulator.get_center() + LEFT * 0.54
            ),
            electron_marker(
                insulator.get_center() + LEFT * 0.61 + DOWN * 0.23
            ),
            electron_marker(
                insulator.get_center() + LEFT * 0.82 + DOWN * 0.04
            )
        )

        self.play(
            FadeIn(conductor_charges),
            FadeIn(insulator_charges),
            run_time=0.8
        )

        self.wait(1.2)

        # ====================================================
        # PART 5 — CONDUCTOR
        # ====================================================

        self.play(
            FadeOut(experiment_title),
            run_time=0.4
        )

        conductor_focus = arabic_text(
            "في الموصل",
            size=33,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(conductor_focus),
            run_time=0.7
        )

        self.wait(0.7)

        conductor_final_positions = [
            conductor.get_center() + LEFT * 1.15,
            conductor.get_center() + UP * 1.15,
            conductor.get_center() + RIGHT * 1.15,
            conductor.get_center() + DOWN * 1.15
        ]

        self.play(
            *[
                charge.animate.move_to(target)
                for charge, target in zip(
                    conductor_charges,
                    conductor_final_positions
                )
            ],
            run_time=1.7,
            rate_func=smooth
        )

        self.wait(0.8)

        conductor_result_1 = arabic_text(
            "الشحنات تعيد توزيع نفسها",
            size=28,
            color=ACCENT
        ).move_to(
            LEFT * 3.4 + DOWN * 1.72
        )

        conductor_result_2 = arabic_text(
            "على السطح الخارجي",
            size=27,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            LEFT * 3.4 + DOWN * 2.15
        )

        self.play(
            FadeOut(conductor_focus),
            FadeIn(conductor_result_1),
            run_time=0.7
        )

        self.play(
            FadeIn(conductor_result_2),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 6 — INSULATOR
        # ====================================================

        self.play(
            FadeOut(conductor_result_1),
            FadeOut(conductor_result_2),
            run_time=0.5
        )

        insulator_focus = arabic_text(
            "أما في العازل",
            size=33,
            weight=BOLD,
            color=INSULATOR_COLOR
        ).to_edge(
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(insulator_focus),
            run_time=0.7
        )

        self.wait(0.7)

        self.play(
            insulator_charges[0].animate.shift(RIGHT * 0.06),
            insulator_charges[1].animate.shift(UP * 0.05),
            insulator_charges[2].animate.shift(DOWN * 0.05),
            insulator_charges[3].animate.shift(RIGHT * 0.04),
            run_time=1.0
        )

        self.wait(0.7)

        insulator_result = arabic_text(
            "تبقى الشحنة قريبة من مكان وضعها",
            size=27,
            weight=BOLD,
            color=INSULATOR_COLOR
        ).move_to(
            RIGHT * 3.4 + DOWN * 1.9
        )

        self.play(
            FadeOut(insulator_focus),
            FadeIn(insulator_result),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 7 — DIRECT COMPARISON
        # ====================================================

        self.play(
            FadeOut(insulator_result),
            FadeOut(title),
            run_time=0.5
        )

        comparison_title = arabic_text(
            "الفرق الأساسي",
            size=38,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        left_key = arabic_text(
            "الشحنة تستطيع إعادة التوزيع",
            size=27,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            LEFT * 3.4 + DOWN * 2.15
        )

        right_key = arabic_text(
            "الشحنة تبقى محلية بدرجة أكبر",
            size=27,
            weight=BOLD,
            color=INSULATOR_COLOR
        ).move_to(
            RIGHT * 3.4 + DOWN * 2.15
        )

        self.play(
            FadeIn(comparison_title),
            FadeIn(left_key),
            FadeIn(right_key),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 8 — REMOVE EXPERIMENT
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    conductor,
                    insulator,
                    conductor_charges,
                    insulator_charges,
                    divider,
                    conductor_title,
                    insulator_title,
                    comparison_title,
                    left_key,
                    right_key
                )
            ),
            run_time=0.8
        )

        # ====================================================
        # PART 9 — EXAMPLES
        # ====================================================

        examples_title = arabic_text(
            "أمثلة على الموصلات والعوازل",
            size=39,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.42
        )

        self.play(
            FadeIn(examples_title),
            run_time=0.8
        )

        # ----------------------------------------------------
        # LEFT CARD — CONDUCTORS
        # ----------------------------------------------------

        conductor_card = RoundedRectangle(
            width=5.4,
            height=4.5,
            corner_radius=0.22,
            stroke_width=3,
            stroke_color=ACCENT,
            fill_color=ACCENT,
            fill_opacity=0.035
        ).move_to(
            LEFT * 3.25 + DOWN * 0.45
        )

        conductor_card_title = arabic_text(
            "موصلات",
            size=38,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            conductor_card.get_center()
            + UP * 1.55
        )

        conductor_separator = Line(
            conductor_card.get_center() + LEFT * 2.05 + UP * 1.05,
            conductor_card.get_center() + RIGHT * 2.05 + UP * 1.05,
            stroke_width=2,
            color=ACCENT
        )

        conductor_copper = arabic_text(
            "النحاس",
            size=31
        )

        conductor_silver = arabic_text(
            "الفضة",
            size=31
        )

        conductor_aluminum = arabic_text(
            "الألومنيوم",
            size=31
        )

        conductor_examples = VGroup(
            conductor_copper,
            conductor_silver,
            conductor_aluminum
        ).arrange(
            DOWN,
            buff=0.42
        )

        conductor_examples.move_to(
            conductor_card.get_center()
            + DOWN * 0.30
        )

        # ----------------------------------------------------
        # RIGHT CARD — INSULATORS
        # ----------------------------------------------------

        insulator_card = RoundedRectangle(
            width=5.4,
            height=4.5,
            corner_radius=0.22,
            stroke_width=3,
            stroke_color=INSULATOR_COLOR,
            fill_color=INSULATOR_COLOR,
            fill_opacity=0.035
        ).move_to(
            RIGHT * 3.25 + DOWN * 0.45
        )

        insulator_card_title = arabic_text(
            "عوازل",
            size=38,
            weight=BOLD,
            color=INSULATOR_COLOR
        ).move_to(
            insulator_card.get_center()
            + UP * 1.55
        )

        insulator_separator = Line(
            insulator_card.get_center() + LEFT * 2.05 + UP * 1.05,
            insulator_card.get_center() + RIGHT * 2.05 + UP * 1.05,
            stroke_width=2,
            color=INSULATOR_COLOR
        )

        insulator_plastic = arabic_text(
            "البلاستيك",
            size=30
        )

        insulator_glass = arabic_text(
            "الزجاج",
            size=30
        )

        insulator_rubber = arabic_text(
            "المطاط",
            size=30
        )

        insulator_wood = arabic_text(
            "الخشب الجاف",
            size=30
        )

        insulator_examples = VGroup(
            insulator_plastic,
            insulator_glass,
            insulator_rubber,
            insulator_wood
        ).arrange(
            DOWN,
            buff=0.31
        )

        insulator_examples.move_to(
            insulator_card.get_center()
            + DOWN * 0.32
        )

        # ====================================================
        # PART 10 — SHOW CARDS
        # ====================================================

        self.play(
            FadeIn(conductor_card),
            FadeIn(insulator_card),
            run_time=0.8
        )

        self.wait(0.4)

        self.play(
            FadeIn(conductor_card_title),
            Create(conductor_separator),
            run_time=0.7
        )

        self.play(
            FadeIn(insulator_card_title),
            Create(insulator_separator),
            run_time=0.7
        )

        self.wait(0.7)

        # Conductors one by one
        self.play(
            FadeIn(conductor_copper),
            run_time=0.6
        )

        self.wait(0.35)

        self.play(
            FadeIn(conductor_silver),
            run_time=0.6
        )

        self.wait(0.35)

        self.play(
            FadeIn(conductor_aluminum),
            run_time=0.6
        )

        self.wait(0.8)

        # Insulators one by one
        self.play(
            FadeIn(insulator_plastic),
            run_time=0.6
        )

        self.wait(0.3)

        self.play(
            FadeIn(insulator_glass),
            run_time=0.6
        )

        self.wait(0.3)

        self.play(
            FadeIn(insulator_rubber),
            run_time=0.6
        )

        self.wait(0.3)

        self.play(
            FadeIn(insulator_wood),
            run_time=0.6
        )

        self.wait(1.5)

        # ====================================================
        # PART 11 — EMPHASIZE CLASSIFICATION
        # ====================================================

        self.play(
            Indicate(
                conductor_card_title,
                color=ACCENT,
                scale_factor=1.07
            ),
            run_time=0.7
        )

        self.wait(0.3)

        self.play(
            Indicate(
                conductor_examples,
                color=ACCENT,
                scale_factor=1.03
            ),
            run_time=0.8
        )

        self.wait(0.7)

        self.play(
            Indicate(
                insulator_card_title,
                color=INSULATOR_COLOR,
                scale_factor=1.07
            ),
            run_time=0.7
        )

        self.wait(0.3)

        self.play(
            Indicate(
                insulator_examples,
                color=INSULATOR_COLOR,
                scale_factor=1.03
            ),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 12 — DRY WOOD NOTE
        # ====================================================

        dry_wood_note = arabic_text(
            "الخشب الجاف عازل جيد نسبيًا، أما الرطوبة فتزيد التوصيل",
            size=26,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.24
        )

        self.play(
            FadeIn(dry_wood_note),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 13 — SUMMARY
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    examples_title,
                    conductor_card,
                    conductor_card_title,
                    conductor_separator,
                    conductor_examples,
                    insulator_card,
                    insulator_card_title,
                    insulator_separator,
                    insulator_examples,
                    dry_wood_note
                )
            ),
            run_time=0.8
        )

        summary_title = arabic_text(
            "الخلاصة",
            size=42,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.5
        )

        summary_conductor_title = arabic_text(
            "الموصل",
            size=36,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            LEFT * 3.2 + UP * 0.8
        )

        summary_conductor_text = arabic_text(
            "الشحنات تتحرك فيه بسهولة نسبية",
            size=28
        ).move_to(
            LEFT * 3.2
        )

        summary_insulator_title = arabic_text(
            "العازل",
            size=36,
            weight=BOLD,
            color=INSULATOR_COLOR
        ).move_to(
            RIGHT * 3.2 + UP * 0.8
        )

        summary_insulator_text = arabic_text(
            "حركة الشحنات فيه أكثر تقييدًا",
            size=28
        ).move_to(
            RIGHT * 3.2
        )

        self.play(
            FadeIn(summary_title),
            run_time=0.7
        )

        self.play(
            FadeIn(summary_conductor_title),
            FadeIn(summary_conductor_text),
            run_time=0.8
        )

        self.wait(0.7)

        self.play(
            FadeIn(summary_insulator_title),
            FadeIn(summary_insulator_text),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 14 — TRANSITION TO SEMICONDUCTORS
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    summary_title,
                    summary_conductor_title,
                    summary_conductor_text,
                    summary_insulator_title,
                    summary_insulator_text
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "وهناك فئة مهمة أخرى من المواد",
            size=35
        ).shift(
            UP * 0.45
        )

        transition_2 = arabic_text(
            "يمكن التحكم في قدرتها على التوصيل",
            size=37,
            weight=BOLD
        ).next_to(
            transition_1,
            DOWN,
            buff=0.25
        )

        transition_3 = arabic_text(
            "أشباه الموصلات",
            size=36,
            weight=BOLD,
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

    config.output_file = "scene_12_conductors_insulators"

    config.preview = True
    config.quality = "high_quality"

    Scene12ConductorsInsulators().render()