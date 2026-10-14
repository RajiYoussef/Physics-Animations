from manim import *


# ============================================================
# Scene 08
# السجادة وشرارة مقبض الباب
#
# الفكرة:
# - أثناء المشي على السجادة يمكن أن تنتقل إلكترونات
#   بين الحذاء والسجادة.
# - مع تكرار الخطوات قد تتراكم شحنة صافية على الجسم.
# - عند تقريب اليد من جسم معدني موصل، تزداد شدة
#   المجال الكهربائي عبر الفجوة الصغيرة من الهواء.
# - إذا أصبح المجال قويًا بما يكفي، يحدث تفريغ سريع
#   عبر الهواء وتظهر شرارة.
# - الشحنة لم تُخلق؛ بل انتقلت بين المواد ثم أعيد
#   توزيعها أثناء التفريغ.
#
# ملاحظة:
# اتجاه انتقال الإلكترونات الفعلي يعتمد على نوعي
# الحذاء والسجادة والظروف المحيطة. هذا المشهد يعرض
# مثالًا توضيحيًا تصبح فيه شحنة الشخص سالبة.
# ============================================================


class Scene08CarpetDoorSpark(Scene):

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

        CARPET = "#8B5E3C"
        METAL = "#B7C0CC"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

        SPARK = "#FFD166"

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

        def electron(position=ORIGIN, radius=0.09):

            dot = Circle(
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
            ).move_to(dot)

            return VGroup(dot, sign)

        def make_person(center=ORIGIN):

            head = Circle(
                radius=0.38,
                stroke_width=4,
                color=TEXT_MAIN
            ).move_to(
                center + UP * 1.65
            )

            body = Line(
                center + UP * 1.27,
                center + DOWN * 0.35,
                stroke_width=5,
                color=TEXT_MAIN
            )

            left_arm = Line(
                center + UP * 0.75,
                center + LEFT * 0.85 + UP * 0.15,
                stroke_width=5,
                color=TEXT_MAIN
            )

            right_arm = Line(
                center + UP * 0.75,
                center + RIGHT * 0.85 + UP * 0.15,
                stroke_width=5,
                color=TEXT_MAIN
            )

            left_leg = Line(
                center + DOWN * 0.35,
                center + LEFT * 0.65 + DOWN * 1.35,
                stroke_width=5,
                color=TEXT_MAIN
            )

            right_leg = Line(
                center + DOWN * 0.35,
                center + RIGHT * 0.65 + DOWN * 1.35,
                stroke_width=5,
                color=TEXT_MAIN
            )

            left_shoe = RoundedRectangle(
                width=0.7,
                height=0.20,
                corner_radius=0.07,
                stroke_width=3,
                stroke_color=TEXT_SECONDARY
            ).move_to(
                center + LEFT * 0.82 + DOWN * 1.42
            )

            right_shoe = RoundedRectangle(
                width=0.7,
                height=0.20,
                corner_radius=0.07,
                stroke_width=3,
                stroke_color=TEXT_SECONDARY
            ).move_to(
                center + RIGHT * 0.82 + DOWN * 1.42
            )

            return VGroup(
                head,
                body,
                left_arm,
                right_arm,
                left_leg,
                right_leg,
                left_shoe,
                right_shoe
            )

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "ماذا يحدث عندما نمشي على سجادة؟",
            size=44,
            weight=BOLD
        )

        self.play(
            FadeIn(title, shift=UP * 0.15),
            run_time=1.0
        )

        self.wait(1.8)

        subtitle = arabic_text(
            "مثال يومي على انتقال الشحنة",
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
        # PART 2 — CARPET AND PERSON
        # ====================================================

        carpet = RoundedRectangle(
            width=11.5,
            height=1.0,
            corner_radius=0.12,
            stroke_width=3,
            stroke_color=CARPET,
            fill_color=CARPET,
            fill_opacity=0.22
        ).move_to(
            DOWN * 2.55
        )

        carpet_lines = VGroup()

        for x in [
            -5.0, -4.2, -3.4, -2.6, -1.8, -1.0,
            -0.2, 0.6, 1.4, 2.2, 3.0, 3.8, 4.6
        ]:
            fiber = Line(
                [x, -2.85, 0],
                [x + 0.18, -2.25, 0],
                stroke_width=2,
                color=CARPET
            )
            carpet_lines.add(fiber)

        carpet_label = arabic_text(
            "سجادة",
            size=27,
            color=CARPET
        ).next_to(
            carpet,
            DOWN,
            buff=0.2
        )

        person = make_person(
            LEFT * 3.9 + UP * 0.1
        )

        self.play(
            FadeIn(carpet),
            FadeIn(carpet_lines),
            FadeIn(carpet_label),
            FadeIn(person),
            run_time=1.0
        )

        self.wait(1.1)

        # ====================================================
        # PART 3 — FIRST CONTACT / SEPARATION
        # ====================================================

        explanation_1 = arabic_text(
            "مع كل خطوة: تلامس ثم انفصال",
            size=32,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(explanation_1),
            run_time=0.8
        )

        self.wait(1.0)

        # Electrons appear near carpet surface
        e1 = electron(
            LEFT * 4.6 + DOWN * 2.10
        )

        e2 = electron(
            LEFT * 3.8 + DOWN * 2.10
        )

        e3 = electron(
            LEFT * 3.0 + DOWN * 2.10
        )

        self.play(
            FadeIn(e1),
            FadeIn(e2),
            FadeIn(e3),
            run_time=0.7
        )

        self.wait(0.5)

        # Example transfer: electrons move from carpet toward person
        self.play(
            e1.animate.move_to(
                person.get_center() + LEFT * 0.55 + DOWN * 0.45
            ),
            run_time=0.9
        )

        self.wait(0.4)

        # Small walking motion
        self.play(
            person.animate.shift(RIGHT * 1.3),
            e1.animate.shift(RIGHT * 1.3),
            run_time=0.8
        )

        self.play(
            e2.animate.move_to(
                person.get_center() + RIGHT * 0.55 + UP * 0.15
            ),
            run_time=0.9
        )

        self.play(
            person.animate.shift(RIGHT * 1.3),
            e1.animate.shift(RIGHT * 1.3),
            e2.animate.shift(RIGHT * 1.3),
            run_time=0.8
        )

        self.play(
            e3.animate.move_to(
                person.get_center() + LEFT * 0.45 + UP * 1.0
            ),
            run_time=0.9
        )

        self.wait(1.0)

        # ====================================================
        # PART 4 — REPEATED STEPS / CHARGE ACCUMULATION
        # ====================================================

        self.play(
            FadeOut(explanation_1),
            run_time=0.4
        )

        accumulation_title = arabic_text(
            "مع تكرار الخطوات يمكن أن تتراكم الشحنة",
            size=34,
            weight=BOLD,
            color=NEGATIVE
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeOut(subtitle),
            FadeIn(accumulation_title),
            run_time=0.8
        )

        # More electrons appear on person
        extra_electrons = VGroup(
            electron(person.get_center() + LEFT * 0.75 + UP * 1.25),
            electron(person.get_center() + RIGHT * 0.80 + UP * 1.05),
            electron(person.get_center() + LEFT * 0.90 + UP * 0.15),
            electron(person.get_center() + RIGHT * 0.95 + DOWN * 0.50),
            electron(person.get_center() + LEFT * 0.45 + DOWN * 1.00),
            electron(person.get_center() + RIGHT * 0.50 + UP * 0.55)
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(e, scale=0.6)
                    for e in extra_electrons
                ],
                lag_ratio=0.12
            ),
            run_time=1.3
        )

        self.wait(1.2)

        charged_person_label = arabic_text(
            "شحنة سالبة زائدة",
            size=31,
            color=NEGATIVE
        ).next_to(
            person,
            RIGHT,
            buff=0.45
        )

        self.play(
            FadeIn(charged_person_label),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 5 — IMPORTANT CAVEAT
        # ====================================================

        caveat = arabic_text(
            "اتجاه انتقال الإلكترونات يعتمد على نوع المادتين والظروف",
            size=27,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(caveat),
            run_time=0.7
        )

        self.wait(1.5)

        # ====================================================
        # PART 6 — TRANSITION TO DOORKNOB
        # ====================================================

        self.play(
            FadeOut(caveat),
            FadeOut(accumulation_title),
            FadeOut(carpet_label),
            FadeOut(charged_person_label),
            run_time=0.6
        )

        transition_text = arabic_text(
            "ثم نقترب من مقبض باب معدني...",
            size=37,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(transition_text),
            run_time=0.8
        )

        self.wait(0.8)

        # Move person to left side for second setup
        charged_group = VGroup(
            person,
            e1,
            e2,
            e3,
            extra_electrons
        )

        self.play(
            FadeOut(carpet),
            FadeOut(carpet_lines),
            charged_group.animate.scale(0.8).move_to(
                LEFT * 3.6 + DOWN * 0.15
            ),
            run_time=1.1
        )

        # ====================================================
        # PART 7 — DOOR AND METAL KNOB
        # ====================================================

        door = Rectangle(
            width=3.0,
            height=6.0,
            stroke_width=4,
            stroke_color="#6E7681",
            fill_color="#6E7681",
            fill_opacity=0.05
        ).move_to(
            RIGHT * 4.7
        )

        knob_stem = Line(
            RIGHT * 3.85,
            RIGHT * 4.25,
            stroke_width=8,
            color=METAL
        ).shift(
            DOWN * 0.1
        )

        knob = Circle(
            radius=0.32,
            stroke_width=4,
            stroke_color=METAL,
            fill_color=METAL,
            fill_opacity=0.18
        ).move_to(
            RIGHT * 3.65 + DOWN * 0.1
        )

        metal_highlight = Arc(
            radius=0.17,
            start_angle=40 * DEGREES,
            angle=100 * DEGREES,
            stroke_width=3,
            color=TEXT_MAIN
        ).move_to(
            knob.get_center() + LEFT * 0.05 + UP * 0.04
        )

        knob_group = VGroup(
            knob_stem,
            knob,
            metal_highlight
        )

        knob_label = arabic_text(
            "مقبض معدني",
            size=28,
            color=METAL
        ).next_to(
            knob,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(door),
            FadeIn(knob_group),
            FadeIn(knob_label),
            run_time=0.9
        )

        self.wait(1.2)

        # ====================================================
        # PART 8 — HAND APPROACHES
        # ====================================================

        # Hand/finger simplified
        finger = RoundedRectangle(
            width=2.1,
            height=0.34,
            corner_radius=0.16,
            stroke_width=3,
            stroke_color="#E6C6A8",
            fill_color="#E6C6A8",
            fill_opacity=0.16
        ).move_to(
            LEFT * 0.75 + DOWN * 0.1
        )

        fingertip = Circle(
            radius=0.17,
            stroke_width=3,
            stroke_color="#E6C6A8",
            fill_color="#E6C6A8",
            fill_opacity=0.16
        ).move_to(
            finger.get_right()
        )

        hand_group = VGroup(
            finger,
            fingertip
        )

        self.play(
            FadeIn(hand_group),
            run_time=0.7
        )

        self.wait(0.7)

        approach_label = arabic_text(
            "الفجوة الهوائية تصغر",
            size=29,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(approach_label),
            run_time=0.7
        )

        # Move hand near knob without touching
        self.play(
            hand_group.animate.shift(
                RIGHT * 1.65
            ),
            run_time=1.5,
            rate_func=smooth
        )

        self.wait(1.0)

        # ====================================================
        # PART 9 — LOCAL FIELD BUILDS
        # ====================================================

        self.play(
            FadeOut(approach_label),
            run_time=0.4
        )

        gap_arrow = DoubleArrow(
            start=hand_group.get_right() + UP * 0.55,
            end=knob.get_left() + UP * 0.55,
            buff=0.03,
            stroke_width=3,
            color=ACCENT,
            max_tip_length_to_length_ratio=0.20
        )

        gap_label = arabic_text(
            "فجوة صغيرة من الهواء",
            size=27,
            color=ACCENT
        ).next_to(
            gap_arrow,
            UP,
            buff=0.18
        )

        self.play(
            GrowFromCenter(gap_arrow),
            FadeIn(gap_label),
            run_time=0.8
        )

        self.wait(1.0)

        field_text_1 = arabic_text(
            "عبر هذه الفجوة يزداد تأثير المجال الكهربائي",
            size=31
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(field_text_1),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 10 — SPARK
        # ====================================================

        self.play(
            FadeOut(gap_arrow),
            FadeOut(gap_label),
            FadeOut(field_text_1),
            run_time=0.4
        )

        spark_path = VMobject(
            stroke_color=SPARK,
            stroke_width=7
        )

        p1 = hand_group.get_right()
        p6 = knob.get_left()

        p2 = p1 + RIGHT * 0.18 + UP * 0.10
        p3 = p1 + RIGHT * 0.38 + DOWN * 0.08
        p4 = p1 + RIGHT * 0.58 + UP * 0.12
        p5 = p1 + RIGHT * 0.78 + DOWN * 0.04

        spark_path.set_points_as_corners(
            [p1, p2, p3, p4, p5, p6]
        )

        glow_1 = Circle(
            radius=0.22,
            stroke_width=0,
            fill_color=SPARK,
            fill_opacity=0.14
        ).move_to(
            (p1 + p6) / 2
        )

        glow_2 = Circle(
            radius=0.42,
            stroke_width=0,
            fill_color=SPARK,
            fill_opacity=0.06
        ).move_to(
            (p1 + p6) / 2
        )

        spark_text = arabic_text(
            "تفريغ كهربائي سريع",
            size=34,
            weight=BOLD,
            color=SPARK
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeOut(transition_text),
            FadeIn(spark_text),
            Create(spark_path),
            FadeIn(glow_1),
            FadeIn(glow_2),
            run_time=0.35
        )

        self.wait(0.25)

        self.play(
            FadeOut(spark_path),
            FadeOut(glow_1),
            FadeOut(glow_2),
            run_time=0.25
        )

        self.wait(0.7)

        # ====================================================
        # PART 11 — CHARGE MOVES DURING DISCHARGE
        # ====================================================

        discharge_electrons = VGroup(
            electron(hand_group.get_right() + LEFT * 0.45, radius=0.07),
            electron(hand_group.get_right() + LEFT * 0.75, radius=0.07),
            electron(hand_group.get_right() + LEFT * 1.00, radius=0.07)
        )

        self.play(
            FadeIn(discharge_electrons),
            run_time=0.4
        )

        target_positions = [
            knob.get_center() + LEFT * 0.10 + UP * 0.10,
            knob.get_center() + RIGHT * 0.05,
            knob.get_center() + LEFT * 0.05 + DOWN * 0.10,
        ]

        self.play(
            *[
                e.animate.move_to(target)
                for e, target in zip(
                    discharge_electrons,
                    target_positions
                )
            ],
            run_time=0.65,
            rate_func=linear
        )

        self.play(
            FadeOut(discharge_electrons),
            run_time=0.35
        )

        self.wait(0.7)

        discharge_note = arabic_text(
            "تنتقل الشحنة بسرعة بين الجسم والمعدن",
            size=31,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(discharge_note),
            run_time=0.8
        )

        self.wait(1.5)

        # Remove much of the visible excess charge on person
        visible_charges = VGroup(
            e1,
            e2,
            e3,
            *extra_electrons
        )

        self.play(
            LaggedStart(
                *[
                    FadeOut(e, scale=0.6)
                    for e in visible_charges
                ],
                lag_ratio=0.06
            ),
            run_time=1.0
        )

        self.wait(0.8)

        # ====================================================
        # PART 12 — WHAT ACTUALLY HAPPENED?
        # ====================================================

        self.play(
            FadeOut(spark_text),
            FadeOut(discharge_note),
            FadeOut(knob_label),
            run_time=0.5
        )

        summary_title = arabic_text(
            "ما الذي حدث؟",
            size=41,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(summary_title),
            run_time=0.7
        )

        self.wait(0.7)

        step_1 = arabic_text(
            "1. انتقال إلكترونات أثناء المشي",
            size=31,
            color=NEGATIVE
        ).move_to(
            UP * 0.75
        )

        step_2 = arabic_text(
            "2. تراكم شحنة صافية على الجسم",
            size=31
        ).next_to(
            step_1,
            DOWN,
            buff=0.35
        )

        step_3 = arabic_text(
            "3. تفريغ سريع عند الاقتراب من المعدن",
            size=31,
            color=SPARK
        ).next_to(
            step_2,
            DOWN,
            buff=0.35
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

        self.wait(1.5)

        # ====================================================
        # PART 13 — CONSERVATION CONNECTION
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    person,
                    hand_group,
                    door,
                    knob_group,
                    summary_title,
                    step_1,
                    step_2,
                    step_3
                )
            ),
            run_time=0.8
        )

        conservation_1 = arabic_text(
            "لم تُخلق شحنة جديدة",
            size=39,
            weight=BOLD
        ).shift(
            UP * 0.65
        )

        conservation_2 = arabic_text(
            "الإلكترونات انتقلت بين المواد",
            size=38,
            weight=BOLD,
            color=NEGATIVE
        ).next_to(
            conservation_1,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(conservation_1),
            run_time=0.8
        )

        self.wait(0.6)

        self.play(
            FadeIn(conservation_2),
            run_time=0.8
        )

        self.wait(1.6)

        conservation_3 = arabic_text(
            "وهذا يتفق مع قانون حفظ الشحنة",
            size=31,
            color=ACCENT
        ).next_to(
            conservation_2,
            DOWN,
            buff=0.4
        )

        self.play(
            FadeIn(conservation_3),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 14 — TRANSITION TO BALLOON / POLARIZATION
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    conservation_1,
                    conservation_2,
                    conservation_3
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "لكن هناك ظاهرة تبدو أغرب",
            size=36
        ).shift(
            UP * 0.55
        )

        transition_2 = arabic_text(
            "يمكن لجسم مشحون أن يجذب جسمًا متعادلًا",
            size=38,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            transition_1,
            DOWN,
            buff=0.3
        )

        transition_3 = arabic_text(
            "مثل بالون يلتصق بحائط",
            size=32
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
            run_time=0.8
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

    config.output_file = "scene_08_carpet_door_spark"

    config.preview = True
    config.quality = "high_quality"

    Scene08CarpetDoorSpark().render()