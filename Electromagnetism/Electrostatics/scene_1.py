from manim import *


# ============================================================
# Scene 01
# الكهرمان وبداية الحكاية
#
# الفكرة:
# - نبدأ بظاهرة تاريخية بسيطة.
# - القش لا يتحرك قبل فرك الكهرمان.
# - بعد الفرك ينجذب القش.
# - لا نفسر الظاهرة بعد.
# - ننتهي بثلاثة أسئلة تقود إلى الذرة.
# ============================================================


class Scene01AmberIntro(MovingCameraScene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        # ----------------------------------------------------
        # Color palette
        # ----------------------------------------------------

        AMBER = "#F2A65A"
        AMBER_DARK = "#C77A2B"
        STRAW = "#E5C07B"
        FUR = "#B8A99A"
        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"
        ACCENT = "#58A6FF"

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
        # PART 1 — HISTORICAL OPENING
        # ====================================================

        opening = arabic_text(
            "منذ أكثر من ألفي عام...",
            size=46,
            weight=BOLD
        )

        self.play(
            FadeIn(
                opening,
                shift=UP * 0.2
            ),
            run_time=1.2
        )

        self.wait(2.0)

        self.play(
            opening.animate.to_edge(
                UP,
                buff=0.5
            ).scale(0.78),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — AMBER
        # ====================================================

        amber_outer = RoundedRectangle(
            width=3.0,
            height=1.55,
            corner_radius=0.5,
            stroke_width=4,
            stroke_color=AMBER,
            fill_color=AMBER_DARK,
            fill_opacity=0.55
        ).shift(
            LEFT * 2.7 + DOWN * 0.4
        )

        amber_inner = RoundedRectangle(
            width=2.45,
            height=1.05,
            corner_radius=0.38,
            stroke_width=2,
            stroke_color=AMBER,
            fill_color=AMBER,
            fill_opacity=0.18
        ).move_to(
            amber_outer
        )

        amber_highlight = Arc(
            radius=0.7,
            start_angle=40 * DEGREES,
            angle=90 * DEGREES,
            stroke_width=5,
            color=AMBER
        ).move_to(
            amber_outer.get_center()
            + LEFT * 0.5
            + UP * 0.15
        )

        amber = VGroup(
            amber_outer,
            amber_inner,
            amber_highlight
        )

        amber_label = arabic_text(
            "الكهرمان",
            size=30,
            color=AMBER
        ).next_to(
            amber,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(
                amber,
                scale=0.9
            ),
            FadeIn(amber_label),
            run_time=1.1
        )

        self.wait(1.3)

        # ====================================================
        # PART 3 — STRAW PIECES
        # ====================================================

        straw_positions = [
            [1.0, -1.45, 0],
            [1.9, -1.25, 0],
            [2.8, -1.55, 0],
            [3.7, -1.15, 0],
            [4.4, -1.55, 0],
            [1.45, -0.8, 0],
            [2.55, -0.7, 0],
            [3.55, -0.72, 0]
        ]

        straw_angles = [
            20,
            -15,
            35,
            -25,
            10,
            45,
            -35,
            18
        ]

        straws = VGroup()

        for pos, angle in zip(
            straw_positions,
            straw_angles
        ):

            straw_piece = RoundedRectangle(
                width=0.55,
                height=0.08,
                corner_radius=0.03,
                stroke_width=2,
                stroke_color=STRAW,
                fill_color=STRAW,
                fill_opacity=0.65
            ).move_to(pos)

            straw_piece.rotate(
                angle * DEGREES
            )

            straws.add(
                straw_piece
            )

        straw_label = arabic_text(
            "قطع خفيفة من القش",
            size=28,
            color=STRAW
        ).next_to(
            straws,
            DOWN,
            buff=0.3
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(piece)
                    for piece in straws
                ],
                lag_ratio=0.08
            ),
            FadeIn(straw_label),
            run_time=1.2
        )

        self.wait(1.5)

        # ====================================================
        # PART 4 — BEFORE RUBBING
        # ====================================================

        before_text = arabic_text(
            "قبل الفرك",
            size=32,
            weight=BOLD,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(before_text),
            run_time=0.7
        )

        self.wait(1.5)

        # Amber approaches the straw but nothing happens
        self.play(
            amber.animate.shift(
                RIGHT * 0.55
            ),
            amber_label.animate.shift(
                RIGHT * 0.55
            ),
            run_time=1.0
        )

        self.wait(1.2)

        self.play(
            amber.animate.shift(
                LEFT * 0.55
            ),
            amber_label.animate.shift(
                LEFT * 0.55
            ),
            run_time=0.8
        )

        self.wait(0.8)

        self.play(
            FadeOut(before_text),
            run_time=0.5
        )

        # ====================================================
        # PART 5 — FUR
        # ====================================================

        fur_base = RoundedRectangle(
            width=2.2,
            height=0.8,
            corner_radius=0.25,
            stroke_width=3,
            stroke_color=FUR,
            fill_color=FUR,
            fill_opacity=0.22
        )

        fur_hairs = VGroup()

        for x in [
            -0.85,
            -0.55,
            -0.25,
            0.05,
            0.35,
            0.65,
            0.90
        ]:

            hair = Line(
                [x, 0.2, 0],
                [x + 0.12, 0.62, 0],
                stroke_width=3,
                color=FUR
            )

            fur_hairs.add(
                hair
            )

        fur = VGroup(
            fur_base,
            fur_hairs
        ).move_to(
            LEFT * 2.7 + UP * 1.3
        )

        fur_label = arabic_text(
            "فرو",
            size=28,
            color=FUR
        ).next_to(
            fur,
            UP,
            buff=0.2
        )

        rubbing_text = arabic_text(
            "فرك الكهرمان بالفرو",
            size=33,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(fur),
            FadeIn(fur_label),
            FadeIn(rubbing_text),
            run_time=0.9
        )

        # ====================================================
        # PART 6 — RUBBING MOTION
        # ====================================================

        self.play(
            fur.animate.shift(
                RIGHT * 1.0 + DOWN * 0.45
            ),
            fur_label.animate.shift(
                RIGHT * 1.0 + DOWN * 0.45
            ),
            run_time=0.65
        )

        self.play(
            fur.animate.shift(
                LEFT * 1.6
            ),
            fur_label.animate.shift(
                LEFT * 1.6
            ),
            run_time=0.65
        )

        self.play(
            fur.animate.shift(
                RIGHT * 1.6
            ),
            fur_label.animate.shift(
                RIGHT * 1.6
            ),
            run_time=0.65
        )

        self.play(
            fur.animate.shift(
                LEFT * 1.6
            ),
            fur_label.animate.shift(
                LEFT * 1.6
            ),
            run_time=0.65
        )

        self.play(
            fur.animate.shift(
                RIGHT * 0.6 + UP * 0.45
            ),
            fur_label.animate.shift(
                RIGHT * 0.6 + UP * 0.45
            ),
            run_time=0.6
        )

        self.wait(0.8)

        self.play(
            FadeOut(fur),
            FadeOut(fur_label),
            FadeOut(rubbing_text),
            run_time=0.6
        )

        # ====================================================
        # PART 7 — ATTRACTION AFTER RUBBING
        # ====================================================

        after_text = arabic_text(
            "بعد الفرك...",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(after_text),
            run_time=0.7
        )

        self.wait(0.8)

        # Amber approaches again
        self.play(
            amber.animate.shift(
                RIGHT * 0.8
            ),
            amber_label.animate.shift(
                RIGHT * 0.8
            ),
            run_time=1.0
        )

        self.wait(0.5)

        # Straw pieces are attracted
        target_shifts = [
            LEFT * 1.15 + UP * 0.15,
            LEFT * 1.35 + UP * 0.10,
            LEFT * 1.70 + UP * 0.15,
            LEFT * 2.0 + UP * 0.05,
            LEFT * 2.35 + UP * 0.10,
            LEFT * 1.25 + DOWN * 0.05,
            LEFT * 1.55,
            LEFT * 1.90 + DOWN * 0.05
        ]

        self.play(
            *[
                straw.animate.shift(shift)
                for straw, shift in zip(
                    straws,
                    target_shifts
                )
            ],
            run_time=1.8,
            rate_func=smooth
        )

        self.wait(1.5)

        # Small pulse emphasizing the effect
        self.play(
            Indicate(
                amber_outer,
                scale_factor=1.05,
                color=AMBER
            ),
            run_time=0.8
        )

        self.wait(1.0)

        # ====================================================
        # PART 8 — MODERN INTERPRETATION
        # ====================================================

        self.play(
            FadeOut(after_text),
            run_time=0.4
        )

        explanation_1 = arabic_text(
            "ليست قوة غامضة",
            size=35,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.55
        )

        self.play(
            FadeOut(opening),
            FadeIn(explanation_1),
            run_time=0.8
        )

        self.wait(1.0)

        explanation_2 = arabic_text(
            "بل انتقال وإعادة توزيع للشحنات الكهربائية",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            explanation_1,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(explanation_2),
            run_time=0.9
        )

        self.wait(1.6)

        # ====================================================
        # PART 9 — CLEAR EXPERIMENT
        # ====================================================

        self.play(
            FadeOut(amber),
            FadeOut(amber_label),
            FadeOut(straws),
            FadeOut(straw_label),
            FadeOut(explanation_1),
            FadeOut(explanation_2),
            run_time=0.8
        )

        # ====================================================
        # PART 10 — QUESTIONS
        # ====================================================

        question_1 = arabic_text(
            "ما الشحنة الكهربائية؟",
            size=42,
            weight=BOLD
        ).shift(
            UP * 1.4
        )

        question_2 = arabic_text(
            "كيف يصبح جسم متعادل مشحونًا؟",
            size=38
        ).next_to(
            question_1,
            DOWN,
            buff=0.45
        )

        question_3 = arabic_text(
            "لماذا يحدث التجاذب أو التنافر؟",
            size=38
        ).next_to(
            question_2,
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(
                question_1,
                shift=UP * 0.1
            ),
            run_time=0.8
        )

        self.wait(1.0)

        self.play(
            FadeIn(
                question_2,
                shift=UP * 0.1
            ),
            run_time=0.8
        )

        self.wait(1.0)

        self.play(
            FadeIn(
                question_3,
                shift=UP * 0.1
            ),
            run_time=0.8
        )

        self.wait(1.8)

        # ====================================================
        # PART 11 — TRANSITION TO THE ATOM
        # ====================================================

        self.play(
            FadeOut(question_1),
            FadeOut(question_2),
            FadeOut(question_3),
            run_time=0.7
        )

        transition_text = arabic_text(
            "لنبدأ من الذرة",
            size=46,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.55
        )

        # Stylized atom — teaser only
        nucleus = Circle(
            radius=0.38,
            stroke_width=3,
            color=AMBER,
            fill_color=AMBER,
            fill_opacity=0.25
        )

        orbit_1 = Ellipse(
            width=4.2,
            height=1.7,
            stroke_width=2,
            stroke_opacity=0.65
        )

        orbit_2 = Ellipse(
            width=4.2,
            height=1.7,
            stroke_width=2,
            stroke_opacity=0.65
        ).rotate(
            60 * DEGREES
        )

        orbit_3 = Ellipse(
            width=4.2,
            height=1.7,
            stroke_width=2,
            stroke_opacity=0.65
        ).rotate(
            -60 * DEGREES
        )

        electron_1 = Dot(
            orbit_1.point_from_proportion(0.12),
            radius=0.09,
            color=ACCENT
        )

        electron_2 = Dot(
            orbit_2.point_from_proportion(0.62),
            radius=0.09,
            color=ACCENT
        )

        electron_3 = Dot(
            orbit_3.point_from_proportion(0.88),
            radius=0.09,
            color=ACCENT
        )

        atom = VGroup(
            orbit_1,
            orbit_2,
            orbit_3,
            nucleus,
            electron_1,
            electron_2,
            electron_3
        ).scale(0.9)

        self.play(
            FadeIn(transition_text),
            run_time=0.8
        )

        self.wait(0.8)

        self.play(
            Create(orbit_1),
            Create(orbit_2),
            Create(orbit_3),
            FadeIn(nucleus),
            run_time=1.2
        )

        self.play(
            FadeIn(electron_1),
            FadeIn(electron_2),
            FadeIn(electron_3),
            run_time=0.7
        )

        self.wait(1.5)

        # Gentle zoom toward atom, preparing Scene 2
        self.play(
            self.camera.frame.animate.scale(0.78).move_to(atom),
            run_time=1.3
        )

        self.wait(1.5)

        self.play(
            FadeOut(transition_text),
            FadeOut(atom),
            run_time=0.8
        )


# ============================================================
# DIRECT RENDERING FROM PYCHARM
# ============================================================

if __name__ == "__main__":

    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    config.output_file = "scene_01_amber_intro"

    config.preview = True
    config.quality = "high_quality"

    Scene01AmberIntro().render()