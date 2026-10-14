from manim import *


# ============================================================
# Scene 19
# اتجاه القوة الكهربائية
#
# الهدف:
#
# 1. الشحنات المتشابهة تتنافر.
# 2. الشحنات المختلفة تتجاذب.
# 3. القوة تكون على الخط الواصل بين الشحنتين.
# 4. القوتان متساويتان في المقدار ومتعاكستان في الاتجاه.
#
# |F12| = |F21|
# F12 = -F21
# ============================================================


class Scene19ForceDirection(Scene):

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

        FORCE_COLOR = "#7EE787"
        LINE_COLOR = "#B7C0CC"

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

        def make_repulsion_arrows(
            left_center,
            right_center,
            length=1.0
        ):

            left_arrow = Arrow(
                start=left_center + LEFT * 0.55,
                end=left_center + LEFT * (0.55 + length),
                buff=0,
                stroke_width=6,
                color=FORCE_COLOR,
                max_tip_length_to_length_ratio=0.17
            )

            right_arrow = Arrow(
                start=right_center + RIGHT * 0.55,
                end=right_center + RIGHT * (0.55 + length),
                buff=0,
                stroke_width=6,
                color=FORCE_COLOR,
                max_tip_length_to_length_ratio=0.17
            )

            return VGroup(
                left_arrow,
                right_arrow
            )

        def make_attraction_arrows(
            left_center,
            right_center,
            length=1.0
        ):

            left_arrow = Arrow(
                start=left_center + RIGHT * 0.55,
                end=left_center + RIGHT * (0.55 + length),
                buff=0,
                stroke_width=6,
                color=FORCE_COLOR,
                max_tip_length_to_length_ratio=0.17
            )

            right_arrow = Arrow(
                start=right_center + LEFT * 0.55,
                end=right_center + LEFT * (0.55 + length),
                buff=0,
                stroke_width=6,
                color=FORCE_COLOR,
                max_tip_length_to_length_ratio=0.17
            )

            return VGroup(
                left_arrow,
                right_arrow
            )

        # ====================================================
        # PART 1 — TITLE
        # ====================================================

        title = arabic_text(
            "ما اتجاه القوة الكهربائية؟",
            size=43,
            weight=BOLD
        )

        self.play(
            FadeIn(title, shift=UP * 0.15),
            run_time=0.9
        )

        self.wait(1.2)

        self.play(
            title.animate.to_edge(
                UP,
                buff=0.42
            ).scale(0.85),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — POSITIVE / POSITIVE
        # ====================================================

        left = LEFT * 2.2 + DOWN * 0.25
        right = RIGHT * 2.2 + DOWN * 0.25

        charge_1 = make_charge(left, "+")
        charge_2 = make_charge(right, "+")

        connection_line = DashedLine(
            left,
            right,
            dash_length=0.12,
            stroke_width=2,
            color=LINE_COLOR
        )

        self.play(
            Create(connection_line),
            FadeIn(charge_1),
            FadeIn(charge_2),
            run_time=0.8
        )

        self.wait(0.6)

        repel_arrows = make_repulsion_arrows(
            left,
            right,
            length=0.95
        )

        self.play(
            GrowArrow(repel_arrows[0]),
            GrowArrow(repel_arrows[1]),
            run_time=0.8
        )

        repel_text = arabic_text(
            "شحنتان متشابهتان  ←  تنافر",
            size=32,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(repel_text),
            run_time=0.7
        )

        self.wait(1.2)

        # ====================================================
        # PART 3 — NEGATIVE / NEGATIVE
        # ====================================================

        negative_1 = make_charge(left, "−")
        negative_2 = make_charge(right, "−")

        self.play(
            ReplacementTransform(
                charge_1,
                negative_1
            ),
            ReplacementTransform(
                charge_2,
                negative_2
            ),
            run_time=0.8
        )

        charge_1 = negative_1
        charge_2 = negative_2

        self.wait(0.8)

        # force direction stays the same: repulsion

        self.play(
            Indicate(
                repel_arrows,
                color=FORCE_COLOR,
                scale_factor=1.05
            ),
            run_time=0.8
        )

        self.wait(0.8)

        # ====================================================
        # PART 4 — OPPOSITE CHARGES
        # ====================================================

        positive_again = make_charge(left, "+")
        negative_again = make_charge(right, "−")

        attract_arrows = make_attraction_arrows(
            left,
            right,
            length=0.95
        )

        attract_text = arabic_text(
            "شحنتان مختلفتان  ←  تجاذب",
            size=32,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            ReplacementTransform(
                charge_1,
                positive_again
            ),
            ReplacementTransform(
                charge_2,
                negative_again
            ),
            ReplacementTransform(
                repel_arrows,
                attract_arrows
            ),
            ReplacementTransform(
                repel_text,
                attract_text
            ),
            run_time=1.0
        )

        charge_1 = positive_again
        charge_2 = negative_again
        force_arrows = attract_arrows

        self.wait(1.3)

        # ====================================================
        # PART 5 — LINE OF ACTION
        # ====================================================

        self.play(
            FadeOut(attract_text),
            run_time=0.5
        )

        line_text = arabic_text(
            "القوة تكون على الخط الواصل بين الشحنتين",
            size=33,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            connection_line.animate.set_stroke(
                width=4,
                color=ACCENT
            ),
            FadeIn(line_text),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 6 — F12 AND F21
        # ====================================================

        self.play(
            FadeOut(line_text),
            run_time=0.4
        )

        f12_label = MathTex(
            r"\vec{F}_{12}",
            font_size=43,
            color=FORCE_COLOR
        ).next_to(
            force_arrows[0],
            UP,
            buff=0.12
        )

        f21_label = MathTex(
            r"\vec{F}_{21}",
            font_size=43,
            color=FORCE_COLOR
        ).next_to(
            force_arrows[1],
            UP,
            buff=0.12
        )

        self.play(
            FadeIn(f12_label),
            FadeIn(f21_label),
            run_time=0.7
        )

        self.wait(1.0)

        equality_text = arabic_text(
            "متساويتان في المقدار",
            size=32,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            DOWN * 2.05
        )

        self.play(
            FadeIn(equality_text),
            run_time=0.7
        )

        self.wait(0.8)

        magnitude_equation = MathTex(
            r"|\vec{F}_{12}|=|\vec{F}_{21}|",
            font_size=57,
            color=FORCE_COLOR
        ).next_to(
            equality_text,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(
                magnitude_equation,
                scale=0.9
            ),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 7 — OPPOSITE DIRECTIONS
        # ====================================================

        self.play(
            FadeOut(equality_text),
            FadeOut(magnitude_equation),
            run_time=0.5
        )

        opposite_text = arabic_text(
            "ومتعاكستان في الاتجاه",
            size=32,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            DOWN * 2.05
        )

        self.play(
            FadeIn(opposite_text),
            run_time=0.7
        )

        self.wait(0.8)

        vector_equation = MathTex(
            r"\vec{F}_{12}=-\vec{F}_{21}",
            font_size=60,
            color=FORCE_COLOR
        ).next_to(
            opposite_text,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(
                vector_equation,
                scale=0.9
            ),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 8 — NEWTON'S THIRD LAW
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    opposite_text,
                    vector_equation,
                    f12_label,
                    f21_label
                )
            ),
            run_time=0.6
        )

        newton_title = arabic_text(
            "هذا مثال على قانون نيوتن الثالث",
            size=35,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            DOWN * 2.10
        )

        self.play(
            FadeIn(newton_title),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 9 — FINAL SUMMARY
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    charge_1,
                    charge_2,
                    connection_line,
                    force_arrows,
                    newton_title,
                    title
                )
            ),
            run_time=0.8
        )

        summary_title = arabic_text(
            "اتجاه القوة الكهربائية",
            size=41,
            weight=BOLD
        ).shift(
            UP * 1.30
        )

        summary_1 = arabic_text(
            "الشحنات المتشابهة تتنافر",
            size=33,
            color=POSITIVE
        ).next_to(
            summary_title,
            DOWN,
            buff=0.40
        )

        summary_2 = arabic_text(
            "الشحنات المختلفة تتجاذب",
            size=33,
            color=NEGATIVE
        ).next_to(
            summary_1,
            DOWN,
            buff=0.28
        )

        summary_3 = arabic_text(
            "والقوة تكون على الخط الواصل بينهما",
            size=32,
            color=TEXT_SECONDARY
        ).next_to(
            summary_2,
            DOWN,
            buff=0.28
        )

        summary_eq = MathTex(
            r"\vec{F}_{12}=-\vec{F}_{21}",
            font_size=58,
            color=ACCENT
        ).next_to(
            summary_3,
            DOWN,
            buff=0.40
        )

        self.play(
            FadeIn(summary_title),
            run_time=0.7
        )

        self.play(
            FadeIn(summary_1),
            FadeIn(summary_2),
            run_time=0.8
        )

        self.play(
            FadeIn(summary_3),
            run_time=0.7
        )

        self.play(
            FadeIn(summary_eq),
            run_time=0.8
        )

        self.wait(2.0)

        self.play(
            FadeOut(
                VGroup(
                    summary_title,
                    summary_1,
                    summary_2,
                    summary_3,
                    summary_eq
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

    config.output_file = "scene_19_force_direction"

    config.preview = True
    config.quality = "high_quality"

    Scene19ForceDirection().render()