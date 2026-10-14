from manim import *


# ============================================================
# Scene 04
# التجاذب والتنافر بين الشحنات
#
# الفكرة:
# - الشحنات المتشابهة تتنافر.
# - الشحنات المختلفة تتجاذب.
# - نعرض السلوك بصريًا أولًا.
# - ثم تظهر القاعدة المكتوبة في النهاية.
# ============================================================


class Scene04AttractionRepulsion(Scene):

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
        FORCE = "#7EE787"

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

        def charge_object(sign="+", position=ORIGIN):

            color = POSITIVE if sign == "+" else NEGATIVE

            circle = Circle(
                radius=0.62,
                stroke_width=4,
                color=color,
                fill_color=color,
                fill_opacity=0.12
            ).move_to(position)

            symbol = Text(
                sign,
                font_size=52,
                weight=BOLD,
                color=color
            ).move_to(circle)

            return VGroup(
                circle,
                symbol
            )

        def force_arrow(start, end):

            return Arrow(
                start=start,
                end=end,
                buff=0,
                stroke_width=5,
                color=FORCE,
                max_tip_length_to_length_ratio=0.16
            )

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "ماذا يحدث عندما نقرّب جسمين مشحونين؟",
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

        self.wait(1.8)

        self.play(
            title.animate.to_edge(
                UP,
                buff=0.45
            ).scale(0.82),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — POSITIVE + POSITIVE
        # ====================================================

        positive_left = charge_object(
            "+",
            LEFT * 3.2
        )

        positive_right = charge_object(
            "+",
            RIGHT * 3.2
        )

        self.play(
            FadeIn(positive_left),
            FadeIn(positive_right),
            run_time=0.9
        )

        self.wait(1.2)

        # Bring them closer
        self.play(
            positive_left.animate.move_to(
                LEFT * 1.8
            ),
            positive_right.animate.move_to(
                RIGHT * 1.8
            ),
            run_time=1.3
        )

        self.wait(0.8)

        # ----------------------------------------------------
        # Force arrows point outward
        # ----------------------------------------------------

        arrow_left_positive = force_arrow(
            LEFT * 2.45,
            LEFT * 4.0
        )

        arrow_right_positive = force_arrow(
            RIGHT * 2.45,
            RIGHT * 4.0
        )

        self.play(
            GrowArrow(arrow_left_positive),
            GrowArrow(arrow_right_positive),
            run_time=0.9
        )

        self.wait(1.0)

        # Actual motion caused by repulsion
        self.play(
            positive_left.animate.shift(
                LEFT * 1.0
            ),
            positive_right.animate.shift(
                RIGHT * 1.0
            ),
            arrow_left_positive.animate.shift(
                LEFT * 1.0
            ),
            arrow_right_positive.animate.shift(
                RIGHT * 1.0
            ),
            run_time=1.3
        )

        self.wait(1.1)

        observation_1 = arabic_text(
            "تتحركان بعيدًا عن بعضهما",
            size=32,
            color=FORCE
        ).to_edge(
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(observation_1),
            run_time=0.8
        )

        self.wait(1.3)

        self.play(
            FadeOut(positive_left),
            FadeOut(positive_right),
            FadeOut(arrow_left_positive),
            FadeOut(arrow_right_positive),
            FadeOut(observation_1),
            run_time=0.7
        )

        # ====================================================
        # PART 3 — NEGATIVE + NEGATIVE
        # ====================================================

        negative_left = charge_object(
            "−",
            LEFT * 3.2
        )

        negative_right = charge_object(
            "−",
            RIGHT * 3.2
        )

        self.play(
            FadeIn(negative_left),
            FadeIn(negative_right),
            run_time=0.9
        )

        self.wait(1.0)

        self.play(
            negative_left.animate.move_to(
                LEFT * 1.8
            ),
            negative_right.animate.move_to(
                RIGHT * 1.8
            ),
            run_time=1.3
        )

        self.wait(0.7)

        arrow_left_negative = force_arrow(
            LEFT * 2.45,
            LEFT * 4.0
        )

        arrow_right_negative = force_arrow(
            RIGHT * 2.45,
            RIGHT * 4.0
        )

        self.play(
            GrowArrow(arrow_left_negative),
            GrowArrow(arrow_right_negative),
            run_time=0.9
        )

        self.wait(0.8)

        self.play(
            negative_left.animate.shift(
                LEFT * 1.0
            ),
            negative_right.animate.shift(
                RIGHT * 1.0
            ),
            arrow_left_negative.animate.shift(
                LEFT * 1.0
            ),
            arrow_right_negative.animate.shift(
                RIGHT * 1.0
            ),
            run_time=1.3
        )

        self.wait(1.0)

        observation_2 = arabic_text(
            "والنتيجة نفسها هنا",
            size=32,
            color=FORCE
        ).to_edge(
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(observation_2),
            run_time=0.8
        )

        self.wait(1.3)

        self.play(
            FadeOut(negative_left),
            FadeOut(negative_right),
            FadeOut(arrow_left_negative),
            FadeOut(arrow_right_negative),
            FadeOut(observation_2),
            run_time=0.7
        )

        # ====================================================
        # PART 4 — POSITIVE + NEGATIVE
        # ====================================================

        mixed_positive = charge_object(
            "+",
            LEFT * 3.2
        )

        mixed_negative = charge_object(
            "−",
            RIGHT * 3.2
        )

        self.play(
            FadeIn(mixed_positive),
            FadeIn(mixed_negative),
            run_time=0.9
        )

        self.wait(1.0)

        self.play(
            mixed_positive.animate.move_to(
                LEFT * 2.0
            ),
            mixed_negative.animate.move_to(
                RIGHT * 2.0
            ),
            run_time=1.3
        )

        self.wait(0.8)

        # ----------------------------------------------------
        # Force arrows point inward
        # ----------------------------------------------------

        arrow_positive_inward = force_arrow(
            LEFT * 1.3,
            LEFT * 0.25
        )

        arrow_negative_inward = force_arrow(
            RIGHT * 1.3,
            RIGHT * 0.25
        )

        self.play(
            GrowArrow(arrow_positive_inward),
            GrowArrow(arrow_negative_inward),
            run_time=0.9
        )

        self.wait(1.0)

        # Move toward one another but do not overlap
        self.play(
            mixed_positive.animate.shift(
                RIGHT * 0.75
            ),
            mixed_negative.animate.shift(
                LEFT * 0.75
            ),
            arrow_positive_inward.animate.shift(
                RIGHT * 0.75
            ),
            arrow_negative_inward.animate.shift(
                LEFT * 0.75
            ),
            run_time=1.3
        )

        self.wait(1.0)

        observation_3 = arabic_text(
            "هذه المرة تتحركان نحو بعضهما",
            size=32,
            color=FORCE
        ).to_edge(
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(observation_3),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 5 — ASK FOR THE PATTERN
        # ====================================================

        self.play(
            FadeOut(title),
            FadeOut(arrow_positive_inward),
            FadeOut(arrow_negative_inward),
            FadeOut(observation_3),
            run_time=0.6
        )

        pattern_question = arabic_text(
            "ما النمط الذي نراه؟",
            size=40,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(pattern_question),
            run_time=0.8
        )

        self.wait(1.4)

        self.play(
            FadeOut(mixed_positive),
            FadeOut(mixed_negative),
            run_time=0.6
        )

        # ====================================================
        # PART 6 — BUILD THE RULES
        # ====================================================

        # ----------------------------------------------------
        # Positive + Positive
        # ----------------------------------------------------

        pp_left = charge_object(
            "+",
            LEFT * 1.0
        ).scale(0.65)

        pp_right = charge_object(
            "+",
            RIGHT * 1.0
        ).scale(0.65)

        pp_pair = VGroup(
            pp_left,
            pp_right
        ).shift(
            LEFT * 3.6 + UP * 0.85
        )

        pp_result = arabic_text(
            "تنافر",
            size=30,
            weight=BOLD,
            color=FORCE
        ).next_to(
            pp_pair,
            RIGHT,
            buff=0.4
        )

        self.play(
            FadeIn(pp_pair),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(pp_result),
            run_time=0.6
        )

        # ----------------------------------------------------
        # Negative + Negative
        # ----------------------------------------------------

        nn_left = charge_object(
            "−",
            LEFT * 1.0
        ).scale(0.65)

        nn_right = charge_object(
            "−",
            RIGHT * 1.0
        ).scale(0.65)

        nn_pair = VGroup(
            nn_left,
            nn_right
        ).shift(
            LEFT * 3.6 + DOWN * 0.85
        )

        nn_result = arabic_text(
            "تنافر",
            size=30,
            weight=BOLD,
            color=FORCE
        ).next_to(
            nn_pair,
            RIGHT,
            buff=0.4
        )

        self.play(
            FadeIn(nn_pair),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(nn_result),
            run_time=0.6
        )

        # ----------------------------------------------------
        # Positive + Negative
        # ----------------------------------------------------

        pn_positive = charge_object(
            "+",
            LEFT * 1.0
        ).scale(0.65)

        pn_negative = charge_object(
            "−",
            RIGHT * 1.0
        ).scale(0.65)

        pn_pair = VGroup(
            pn_positive,
            pn_negative
        ).shift(
            RIGHT * 2.7
        )

        pn_result = arabic_text(
            "تجاذب",
            size=32,
            weight=BOLD,
            color=FORCE
        ).next_to(
            pn_pair,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(pn_pair),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(pn_result),
            run_time=0.6
        )

        self.wait(1.6)

        # ====================================================
        # PART 7 — GENERAL RULE
        # ====================================================

        self.play(
            FadeOut(pattern_question),
            FadeOut(pp_pair),
            FadeOut(pp_result),
            FadeOut(nn_pair),
            FadeOut(nn_result),
            FadeOut(pn_pair),
            FadeOut(pn_result),
            run_time=0.8
        )

        rule_1 = arabic_text(
            "الشحنات المتشابهة",
            size=40,
            weight=BOLD
        ).shift(
            UP * 1.0
        )

        rule_1_result = arabic_text(
            "تتنافر",
            size=43,
            weight=BOLD,
            color=FORCE
        ).next_to(
            rule_1,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(rule_1),
            run_time=0.7
        )

        self.wait(0.6)

        self.play(
            FadeIn(
                rule_1_result,
                scale=0.8
            ),
            run_time=0.7
        )

        self.wait(1.2)

        self.play(
            VGroup(
                rule_1,
                rule_1_result
            ).animate.shift(
                UP * 1.2
            ),
            run_time=0.7
        )

        rule_2 = arabic_text(
            "الشحنات المختلفة",
            size=40,
            weight=BOLD
        ).shift(
            DOWN * 0.65
        )

        rule_2_result = arabic_text(
            "تتجاذب",
            size=43,
            weight=BOLD,
            color=FORCE
        ).next_to(
            rule_2,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(rule_2),
            run_time=0.7
        )

        self.wait(0.6)

        self.play(
            FadeIn(
                rule_2_result,
                scale=0.8
            ),
            run_time=0.7
        )

        self.wait(1.6)

        # ====================================================
        # PART 8 — FINAL VISUAL SUMMARY
        # ====================================================

        self.play(
            FadeOut(rule_1),
            FadeOut(rule_1_result),
            FadeOut(rule_2),
            FadeOut(rule_2_result),
            run_time=0.7
        )

        summary_title = arabic_text(
            "نوع الشحنتين يحدد نوع التفاعل",
            size=39,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(summary_title),
            run_time=0.8
        )

        # ----------------------------------------------------
        # Repulsion summary
        # ----------------------------------------------------

        repulsion_positive = charge_object(
            "+",
            LEFT * 0.7
        ).scale(0.7)

        repulsion_positive_2 = charge_object(
            "+",
            RIGHT * 0.7
        ).scale(0.7)

        repulsion_group = VGroup(
            repulsion_positive,
            repulsion_positive_2
        ).shift(
            LEFT * 3.3 + UP * 0.2
        )

        rep_arrow_left = Arrow(
            repulsion_group.get_center() + LEFT * 0.9,
            repulsion_group.get_center() + LEFT * 1.8,
            buff=0,
            stroke_width=4,
            color=FORCE
        )

        rep_arrow_right = Arrow(
            repulsion_group.get_center() + RIGHT * 0.9,
            repulsion_group.get_center() + RIGHT * 1.8,
            buff=0,
            stroke_width=4,
            color=FORCE
        )

        repulsion_text = arabic_text(
            "تنافر",
            size=31,
            weight=BOLD,
            color=FORCE
        ).next_to(
            repulsion_group,
            DOWN,
            buff=0.5
        )

        # ----------------------------------------------------
        # Attraction summary
        # ----------------------------------------------------

        attraction_positive = charge_object(
            "+",
            LEFT * 0.7
        ).scale(0.7)

        attraction_negative = charge_object(
            "−",
            RIGHT * 0.7
        ).scale(0.7)

        attraction_group = VGroup(
            attraction_positive,
            attraction_negative
        ).shift(
            RIGHT * 3.3 + UP * 0.2
        )

        att_arrow_left = Arrow(
            attraction_group.get_center() + LEFT * 1.4,
            attraction_group.get_center() + LEFT * 0.65,
            buff=0,
            stroke_width=4,
            color=FORCE
        )

        att_arrow_right = Arrow(
            attraction_group.get_center() + RIGHT * 1.4,
            attraction_group.get_center() + RIGHT * 0.65,
            buff=0,
            stroke_width=4,
            color=FORCE
        )

        attraction_text = arabic_text(
            "تجاذب",
            size=31,
            weight=BOLD,
            color=FORCE
        ).next_to(
            attraction_group,
            DOWN,
            buff=0.5
        )

        self.play(
            FadeIn(repulsion_group),
            GrowArrow(rep_arrow_left),
            GrowArrow(rep_arrow_right),
            FadeIn(repulsion_text),
            run_time=1.0
        )

        self.wait(0.8)

        self.play(
            FadeIn(attraction_group),
            GrowArrow(att_arrow_left),
            GrowArrow(att_arrow_right),
            FadeIn(attraction_text),
            run_time=1.0
        )

        self.wait(1.8)

        # ====================================================
        # PART 9 — TRANSITION TO CONSERVATION
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    summary_title,
                    repulsion_group,
                    rep_arrow_left,
                    rep_arrow_right,
                    repulsion_text,
                    attraction_group,
                    att_arrow_left,
                    att_arrow_right,
                    attraction_text
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "لكن الشحنة لا تحدد التجاذب والتنافر فقط",
            size=36
        ).shift(
            UP * 0.35
        )

        transition_2 = arabic_text(
            "لها أيضًا خاصية مهمة جدًا: الحفظ",
            size=38,
            weight=BOLD,
            color=FORCE
        ).next_to(
            transition_1,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(transition_1),
            run_time=0.8
        )

        self.wait(0.6)

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

    config.output_file = "scene_04_attraction_repulsion"

    config.preview = True
    config.quality = "high_quality"

    Scene04AttractionRepulsion().render()