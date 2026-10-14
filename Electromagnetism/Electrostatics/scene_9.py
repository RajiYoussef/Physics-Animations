from manim import *


# ============================================================
# Scene 09
# لغز البالون والحائط
#
# الفكرة:
# - نراجع بسرعة شحن بالون بالاحتكاك.
# - في هذا المثال يكتسب البالون إلكترونات ويصبح سالبًا.
# - الحائط متعادل كهربائيًا: Q_net = 0.
# - رغم ذلك ينجذب البالون إلى الحائط ويلتصق به.
# - لا نشرح الاستقطاب في هذا المشهد.
# - ننتهي بالسؤال الذي سيجيب عنه المشهد التالي.
# ============================================================


class Scene09BalloonWallMystery(Scene):

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

        BALLOON_COLOR = "#D77BF3"
        CLOTH_COLOR = "#E5A66B"
        WALL_COLOR = "#8B949E"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

        QUESTION_COLOR = "#FFD166"

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

        def electron_marker(position, radius=0.09):
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

        def make_balloon(center=ORIGIN, scale_factor=1.0):

            body = Ellipse(
                width=2.2 * scale_factor,
                height=2.75 * scale_factor,
                stroke_width=4,
                stroke_color=BALLOON_COLOR,
                fill_color=BALLOON_COLOR,
                fill_opacity=0.14
            ).move_to(center)

            knot = Polygon(
                center + DOWN * 1.35 * scale_factor,
                center + LEFT * 0.16 * scale_factor + DOWN * 1.58 * scale_factor,
                center + RIGHT * 0.16 * scale_factor + DOWN * 1.58 * scale_factor,
                stroke_width=3,
                stroke_color=BALLOON_COLOR,
                fill_color=BALLOON_COLOR,
                fill_opacity=0.18
            )

            string = CubicBezier(
                center + DOWN * 1.58 * scale_factor,
                center + LEFT * 0.35 * scale_factor + DOWN * 2.0 * scale_factor,
                center + RIGHT * 0.30 * scale_factor + DOWN * 2.4 * scale_factor,
                center + DOWN * 2.9 * scale_factor,
                stroke_width=2.5,
                color=TEXT_SECONDARY
            )

            highlight = Arc(
                radius=0.55 * scale_factor,
                start_angle=120 * DEGREES,
                angle=70 * DEGREES,
                stroke_width=4,
                color="#F2D7FA"
            ).move_to(
                center + LEFT * 0.38 * scale_factor + UP * 0.45 * scale_factor
            )

            return VGroup(
                body,
                knot,
                string,
                highlight
            )

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "هل يستطيع جسم مشحون جذب جسم متعادل؟",
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

        subtitle = arabic_text(
            "لنجرّب بالونًا وحائطًا",
            size=34,
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

        self.wait(1.3)

        self.play(
            FadeOut(title),
            subtitle.animate.to_edge(
                UP,
                buff=0.45
            ),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — BALLOON BEFORE RUBBING
        # ====================================================

        balloon = make_balloon(
            LEFT * 2.6 + DOWN * 0.15,
            scale_factor=0.9
        )

        balloon_label = arabic_text(
            "بالون",
            size=28,
            color=BALLOON_COLOR
        ).next_to(
            balloon[0],
            LEFT,
            buff=0.4
        )

        self.play(
            FadeIn(balloon),
            FadeIn(balloon_label),
            run_time=0.9
        )

        self.wait(1.0)

        # ====================================================
        # PART 3 — CLOTH / RUBBING
        # ====================================================

        cloth = RoundedRectangle(
            width=2.1,
            height=1.25,
            corner_radius=0.18,
            stroke_width=3,
            stroke_color=CLOTH_COLOR,
            fill_color=CLOTH_COLOR,
            fill_opacity=0.15
        ).move_to(
            LEFT * 4.6 + UP * 0.4
        )

        cloth_lines = VGroup()

        for dy in [-0.35, -0.1, 0.15, 0.4]:
            line = Line(
                cloth.get_left() + RIGHT * 0.25 + UP * dy,
                cloth.get_right() + LEFT * 0.25 + UP * dy,
                stroke_width=1.5,
                color=CLOTH_COLOR
            )
            cloth_lines.add(line)

        cloth_group = VGroup(
            cloth,
            cloth_lines
        )

        cloth_label = arabic_text(
            "قماش",
            size=26,
            color=CLOTH_COLOR
        ).next_to(
            cloth_group,
            UP,
            buff=0.15
        )

        self.play(
            FadeIn(cloth_group),
            FadeIn(cloth_label),
            run_time=0.8
        )

        rubbing_text = arabic_text(
            "نفرك البالون بالقماش",
            size=32,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(rubbing_text),
            run_time=0.7
        )

        # Move cloth onto balloon
        self.play(
            cloth_group.animate.shift(
                RIGHT * 1.2 + DOWN * 0.2
            ),
            cloth_label.animate.shift(
                RIGHT * 1.2 + DOWN * 0.2
            ),
            run_time=0.6
        )

        # Rubbing motion
        self.play(
            cloth_group.animate.shift(
                RIGHT * 0.75
            ),
            cloth_label.animate.shift(
                RIGHT * 0.75
            ),
            run_time=0.45
        )

        self.play(
            cloth_group.animate.shift(
                LEFT * 0.75
            ),
            cloth_label.animate.shift(
                LEFT * 0.75
            ),
            run_time=0.45
        )

        self.play(
            cloth_group.animate.shift(
                RIGHT * 0.75
            ),
            cloth_label.animate.shift(
                RIGHT * 0.75
            ),
            run_time=0.45
        )

        self.play(
            cloth_group.animate.shift(
                LEFT * 0.75
            ),
            cloth_label.animate.shift(
                LEFT * 0.75
            ),
            run_time=0.45
        )

        self.wait(0.5)

        # ====================================================
        # PART 4 — ELECTRONS TRANSFER TO BALLOON
        # ====================================================

        self.play(
            FadeOut(rubbing_text),
            run_time=0.4
        )

        transfer_text = arabic_text(
            "في هذا المثال يكتسب البالون إلكترونات",
            size=31,
            color=NEGATIVE
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(transfer_text),
            run_time=0.8
        )

        # Electrons begin near cloth
        moving_e_1 = electron_marker(
            cloth_group.get_center() + RIGHT * 0.2
        )

        moving_e_2 = electron_marker(
            cloth_group.get_center() + DOWN * 0.25
        )

        moving_e_3 = electron_marker(
            cloth_group.get_center() + LEFT * 0.15 + UP * 0.2
        )

        moving_electrons = VGroup(
            moving_e_1,
            moving_e_2,
            moving_e_3
        )

        self.play(
            FadeIn(moving_electrons),
            run_time=0.5
        )

        balloon_targets = [
            balloon[0].get_center() + LEFT * 0.55 + UP * 0.55,
            balloon[0].get_center() + RIGHT * 0.45 + UP * 0.15,
            balloon[0].get_center() + LEFT * 0.25 + DOWN * 0.55,
        ]

        self.play(
            *[
                e.animate.move_to(target)
                for e, target in zip(
                    moving_electrons,
                    balloon_targets
                )
            ],
            run_time=1.3,
            rate_func=smooth
        )

        self.wait(0.8)

        # Extra visible negative markers around balloon
        extra_negative = VGroup(
            electron_marker(
                balloon[0].get_center() + RIGHT * 0.70 + UP * 0.65
            ),
            electron_marker(
                balloon[0].get_center() + LEFT * 0.72 + UP * 0.05
            ),
            electron_marker(
                balloon[0].get_center() + RIGHT * 0.62 + DOWN * 0.55
            ),
            electron_marker(
                balloon[0].get_center() + LEFT * 0.48 + DOWN * 0.80
            )
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(e, scale=0.6)
                    for e in extra_negative
                ],
                lag_ratio=0.1
            ),
            run_time=0.9
        )

        self.wait(0.8)

        # Remove cloth
        self.play(
            FadeOut(cloth_group),
            FadeOut(cloth_label),
            FadeOut(transfer_text),
            run_time=0.7
        )

        # ====================================================
        # PART 5 — BALLOON IS NEGATIVE
        # ====================================================

        negative_label = arabic_text(
            "البالون أصبح سالب الشحنة",
            size=34,
            weight=BOLD,
            color=NEGATIVE
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeOut(subtitle),
            FadeIn(negative_label),
            run_time=0.8
        )

        self.wait(1.4)

        self.play(
            Indicate(
                VGroup(
                    moving_electrons,
                    extra_negative
                ),
                color=NEGATIVE,
                scale_factor=1.05
            ),
            run_time=0.9
        )

        self.wait(1.0)

        # ====================================================
        # PART 6 — INTRODUCE THE WALL
        # ====================================================

        wall = Rectangle(
            width=4.2,
            height=7.2,
            stroke_width=4,
            stroke_color=WALL_COLOR,
            fill_color=WALL_COLOR,
            fill_opacity=0.07
        ).move_to(
            RIGHT * 5.2
        )

        # Simple brick pattern
        wall_lines = VGroup()

        for y in [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]:
            wall_lines.add(
                Line(
                    [3.1, y, 0],
                    [7.3, y, 0],
                    stroke_width=1.3,
                    color="#6E7681"
                )
            )

        for x, offset in [
            (4.1, 0),
            (5.2, 0),
            (6.3, 0)
        ]:
            wall_lines.add(
                Line(
                    [x, -3.6, 0],
                    [x, 3.6, 0],
                    stroke_width=1.0,
                    color="#6E7681"
                )
            )

        wall_group = VGroup(
            wall,
            wall_lines
        )

        wall_label = arabic_text(
            "حائط",
            size=30,
            color=WALL_COLOR
        ).move_to(
            RIGHT * 5.15 + UP * 2.8
        )

        self.play(
            FadeIn(wall_group),
            FadeIn(wall_label),
            run_time=0.9
        )

        self.wait(1.0)

        # ====================================================
        # PART 7 — WALL IS NEUTRAL
        # ====================================================

        neutral_wall_text = arabic_text(
            "الحائط متعادل كهربائيًا",
            size=32,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            RIGHT * 3.2 + DOWN * 2.1
        )

        net_zero = MathTex(
            "Q_{\\mathrm{net}}",
            "=",
            "0",
            font_size=52,
            color=ACCENT
        ).next_to(
            neutral_wall_text,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(neutral_wall_text),
            run_time=0.8
        )

        self.wait(0.5)

        self.play(
            FadeIn(net_zero),
            run_time=0.7
        )

        self.wait(1.5)

        # ====================================================
        # PART 8 — SET UP THE PUZZLE
        # ====================================================

        self.play(
            FadeOut(negative_label),
            run_time=0.5
        )

        setup_text = arabic_text(
            "بالون سالب",
            size=31,
            weight=BOLD,
            color=NEGATIVE
        ).move_to(
            LEFT * 3.7 + UP * 2.5
        )

        setup_text_2 = arabic_text(
            "حائط متعادل",
            size=31,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            RIGHT * 4.7 + UP * 2.5
        )

        self.play(
            FadeIn(setup_text),
            FadeIn(setup_text_2),
            run_time=0.8
        )

        self.wait(1.0)

        # ====================================================
        # PART 9 — APPROACH THE WALL
        # ====================================================

        approach_text = arabic_text(
            "نقرّب البالون من الحائط...",
            size=33
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeOut(neutral_wall_text),
            FadeOut(net_zero),
            FadeIn(approach_text),
            run_time=0.8
        )

        self.wait(0.7)

        balloon_full = VGroup(
            balloon,
            balloon_label,
            moving_electrons,
            extra_negative
        )

        self.play(
            balloon_full.animate.shift(
                RIGHT * 3.7
            ),
            run_time=1.8,
            rate_func=smooth
        )

        self.wait(1.2)

        # ====================================================
        # PART 10 — THE BALLOON STICKS
        # ====================================================

        self.play(
            FadeOut(approach_text),
            run_time=0.4
        )

        unexpected_text = arabic_text(
            "والبالون ينجذب!",
            size=38,
            weight=BOLD,
            color=QUESTION_COLOR
        ).to_edge(
            DOWN,
            buff=0.35
        )

        # Small final move until balloon visually touches wall
        self.play(
            balloon_full.animate.shift(
                RIGHT * 0.65
            ),
            run_time=0.9
        )

        self.play(
            FadeIn(
                unexpected_text,
                scale=0.8
            ),
            run_time=0.8
        )

        self.wait(1.6)

        # Gentle indication of the stuck balloon
        self.play(
            Indicate(
                balloon[0],
                color=QUESTION_COLOR,
                scale_factor=1.03
            ),
            run_time=0.8
        )

        self.wait(1.0)

        # ====================================================
        # PART 11 — EMPHASIZE THE CONTRADICTION
        # ====================================================

        self.play(
            FadeOut(unexpected_text),
            run_time=0.4
        )

        mystery_title = arabic_text(
            "لكن انتظر...",
            size=40,
            weight=BOLD,
            color=QUESTION_COLOR
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeOut(setup_text),
            FadeOut(setup_text_2),
            FadeIn(mystery_title),
            run_time=0.8
        )

        self.wait(0.8)

        balloon_fact = VGroup(
            arabic_text(
                "البالون",
                size=30
            ),
            arabic_text(
                "سالب الشحنة",
                size=31,
                weight=BOLD,
                color=NEGATIVE
            )
        ).arrange(
            DOWN,
            buff=0.15
        ).move_to(
            LEFT * 3.1 + UP * 0.8
        )

        wall_fact = VGroup(
            arabic_text(
                "الحائط",
                size=30
            ),
            arabic_text(
                "متعادل كهربائيًا",
                size=31,
                weight=BOLD,
                color=ACCENT
            )
        ).arrange(
            DOWN,
            buff=0.15
        ).move_to(
            RIGHT * 3.2 + UP * 0.8
        )

        self.play(
            FadeIn(balloon_fact),
            FadeIn(wall_fact),
            run_time=0.8
        )

        self.wait(1.0)

        wall_zero = MathTex(
            "Q_{\\mathrm{net}}=0",
            font_size=47,
            color=ACCENT
        ).next_to(
            wall_fact,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(wall_zero),
            run_time=0.7
        )

        self.wait(1.3)

        # ====================================================
        # PART 12 — THE QUESTION
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    wall_group,
                    wall_label,
                    balloon_full,
                    balloon_fact,
                    wall_fact,
                    wall_zero
                )
            ),
            run_time=0.8
        )

        question_1 = arabic_text(
            "إذا كان الحائط متعادلًا...",
            size=39,
            weight=BOLD
        ).shift(
            UP * 0.8
        )

        question_2 = arabic_text(
            "فلماذا يجذب بالونًا مشحونًا؟",
            size=43,
            weight=BOLD,
            color=QUESTION_COLOR
        ).next_to(
            question_1,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeOut(mystery_title),
            FadeIn(question_1),
            run_time=0.8
        )

        self.wait(0.8)

        self.play(
            FadeIn(question_2),
            run_time=0.9
        )

        self.wait(2.0)

        # ====================================================
        # PART 13 — TEASE POLARIZATION
        # ====================================================

        self.play(
            VGroup(
                question_1,
                question_2
            ).animate.shift(
                UP * 0.65
            ),
            run_time=0.7
        )

        answer_tease_1 = arabic_text(
            "الإجابة لا تحتاج إلى أن يصبح الحائط مشحونًا",
            size=31,
            color=TEXT_SECONDARY
        ).next_to(
            question_2,
            DOWN,
            buff=0.6
        )

        self.play(
            FadeIn(answer_tease_1),
            run_time=0.8
        )

        self.wait(1.3)

        answer_tease_2 = arabic_text(
            "بل إلى تغير صغير في توزيع الشحنات داخله",
            size=33,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            answer_tease_1,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(answer_tease_2),
            run_time=0.8
        )

        self.wait(1.6)

        # Do not explain further yet
        self.play(
            FadeOut(
                VGroup(
                    question_1,
                    question_2,
                    answer_tease_1
                )
            ),
            run_time=0.6
        )

        polarization_title = arabic_text(
            "الاستقطاب",
            size=48,
            weight=BOLD,
            color=ACCENT
        )

        self.play(
            ReplacementTransform(
                answer_tease_2,
                polarization_title
            ),
            run_time=0.9
        )

        self.wait(2.0)

        self.play(
            FadeOut(polarization_title),
            run_time=0.8
        )


# ============================================================
# DIRECT RENDERING FROM PYCHARM
# ============================================================

if __name__ == "__main__":

    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    config.output_file = "scene_09_balloon_wall_mystery"

    config.preview = True
    config.quality = "high_quality"

    Scene09BalloonWallMystery().render()