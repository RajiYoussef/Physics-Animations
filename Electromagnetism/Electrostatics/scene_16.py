from manim import *


# ============================================================
# Scene 16
# الشحن بالحث
#
# التسلسل الفيزيائي الصحيح:
#
# 1. نبدأ بموصل مستقطب بسبب جسم سالب قريب.
#    - الجانب القريب: موجب نسبيًا
#    - الجانب البعيد: سالب نسبيًا
#    - Q_net = 0
#
# 2. مع بقاء الجسم السالب في مكانه:
#    نوصل الموصل بالأرض.
#
# 3. الجسم السالب يطرد بعض إلكترونات الموصل،
#    فتغادر عبر مسار التأريض إلى الأرض.
#    يصبح الموصل ذا شحنة موجبة صافية.
#
# 4. نفصل التأريض أولًا،
#    والجسم السالب ما زال قريبًا.
#
# 5. بعد ذلك فقط نبعد الجسم السالب.
#
# 6. تعيد الإلكترونات المتبقية توزيع نفسها،
#    ويصبح النقص في الإلكترونات موزعًا على
#    السطح الخارجي للموصل.
#
# النتيجة:
# موصل ذو شحنة موجبة صافية من دون أن يلمسه
# الجسم المشحون الأصلي.
#
# مهم:
# علامات + تمثل نقصًا في الإلكترونات،
# ولا تعني أن البروتونات تتحرك داخل المعدن.
# ============================================================


class Scene16ChargingByInduction(Scene):

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

        GROUND_COLOR = "#B7C0CC"

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

        def positive_marker(position, radius=0.095):

            circle = Circle(
                radius=radius,
                stroke_width=2,
                stroke_color=POSITIVE,
                fill_color=POSITIVE,
                fill_opacity=0.20
            ).move_to(position)

            sign = Text(
                "+",
                font_size=14,
                weight=BOLD,
                color=POSITIVE
            ).move_to(circle)

            return VGroup(
                circle,
                sign
            )

        def make_ground_symbol(center):

            vertical = Line(
                center + UP * 0.45,
                center,
                stroke_width=4,
                color=GROUND_COLOR
            )

            line_1 = Line(
                center + LEFT * 0.60,
                center + RIGHT * 0.60,
                stroke_width=4,
                color=GROUND_COLOR
            )

            line_2 = Line(
                center + LEFT * 0.40 + DOWN * 0.18,
                center + RIGHT * 0.40 + DOWN * 0.18,
                stroke_width=4,
                color=GROUND_COLOR
            )

            line_3 = Line(
                center + LEFT * 0.20 + DOWN * 0.36,
                center + RIGHT * 0.20 + DOWN * 0.36,
                stroke_width=4,
                color=GROUND_COLOR
            )

            return VGroup(
                vertical,
                line_1,
                line_2,
                line_3
            )

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "كيف نحول الاستقطاب إلى شحنة صافية؟",
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

        self.wait(1.5)

        induction_title = arabic_text(
            "الشحن بالحث",
            size=40,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            title,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(induction_title),
            run_time=0.8
        )

        self.wait(1.3)

        self.play(
            FadeOut(title),
            induction_title.animate.to_edge(
                UP,
                buff=0.42
            ).scale(0.88),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — START FROM SCENE 15
        # ====================================================

        conductor_center = RIGHT * 2.1 + DOWN * 0.15

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

        # ----------------------------------------------------
        # Negative rod
        # ----------------------------------------------------

        rod_center = LEFT * 0.65 + DOWN * 0.15

        rod = RoundedRectangle(
            width=0.75,
            height=4.3,
            corner_radius=0.22,
            stroke_width=4,
            stroke_color=ROD_COLOR,
            fill_color=ROD_COLOR,
            fill_opacity=0.10
        ).move_to(
            rod_center
        )

        rod_charges = VGroup()

        for y in [-1.50, -0.75, 0, 0.75, 1.50]:

            rod_charges.add(
                negative_marker(
                    rod_center + UP * y
                )
            )

        rod_label = arabic_text(
            "جسم سالب",
            size=27,
            color=NEGATIVE
        ).next_to(
            rod,
            UP,
            buff=0.22
        )

        # ====================================================
        # PART 3 — POLARIZED NEUTRAL CONDUCTOR
        # ====================================================

        near_positive_positions = [
            conductor_center + LEFT * 1.38 + UP * 0.68,
            conductor_center + LEFT * 1.55 + UP * 0.22,
            conductor_center + LEFT * 1.55 + DOWN * 0.22,
            conductor_center + LEFT * 1.38 + DOWN * 0.68,
        ]

        far_negative_positions = [
            conductor_center + RIGHT * 1.38 + UP * 0.68,
            conductor_center + RIGHT * 1.55 + UP * 0.22,
            conductor_center + RIGHT * 1.55 + DOWN * 0.22,
            conductor_center + RIGHT * 1.38 + DOWN * 0.68,
        ]

        near_positive = VGroup(
            *[
                positive_marker(pos)
                for pos in near_positive_positions
            ]
        )

        far_negative = VGroup(
            *[
                negative_marker(pos)
                for pos in far_negative_positions
            ]
        )

        conductor_label = arabic_text(
            "موصل مستقطب",
            size=29,
            weight=BOLD
        ).move_to(
            conductor_center + UP * 2.10
        )

        net_zero = MathTex(
            "Q_{\\mathrm{net}}=0",
            font_size=48,
            color=ACCENT
        ).next_to(
            conductor_label,
            DOWN,
            buff=0.16
        )

        self.play(
            FadeIn(rod),
            FadeIn(rod_charges),
            FadeIn(rod_label),

            FadeIn(conductor_group),
            FadeIn(near_positive),
            FadeIn(far_negative),

            FadeIn(conductor_label),
            FadeIn(net_zero),

            run_time=1.0
        )

        self.wait(1.4)

        # ====================================================
        # PART 4 — IMPORTANT SYMBOL CLARIFICATION
        # ====================================================

        symbol_note = arabic_text(
            "علامات + تمثل نقصًا في الإلكترونات، وليست بروتونات تتحرك",
            size=25,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(symbol_note),
            run_time=0.8
        )

        self.wait(1.5)

        self.play(
            FadeOut(symbol_note),
            run_time=0.4
        )

        # ====================================================
        # STEP 1
        # KEEP THE CHARGED OBJECT NEARBY
        # ====================================================

        step_1 = arabic_text(
            "1. نُبقي الجسم السالب قريبًا",
            size=34,
            weight=BOLD,
            color=NEGATIVE
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(step_1),
            run_time=0.7
        )

        self.wait(1.1)

        gap_arrow = DoubleArrow(
            start=rod.get_right() + UP * 1.55,
            end=conductor.get_left() + UP * 1.55,
            buff=0.05,
            stroke_width=3,
            color=ACCENT,
            max_tip_length_to_length_ratio=0.18
        )

        gap_label = arabic_text(
            "لا تلامس",
            size=25,
            color=ACCENT
        ).next_to(
            gap_arrow,
            UP,
            buff=0.10
        )

        self.play(
            GrowFromCenter(gap_arrow),
            FadeIn(gap_label),
            run_time=0.7
        )

        self.wait(1.0)

        self.play(
            FadeOut(gap_arrow),
            FadeOut(gap_label),
            FadeOut(step_1),
            run_time=0.5
        )

        # ====================================================
        # STEP 2
        # CONNECT TO GROUND
        # ====================================================

        step_2 = arabic_text(
            "2. نوصل الموصل بالأرض",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(step_2),
            run_time=0.7
        )

        self.wait(0.7)

        # ----------------------------------------------------
        # Ground connection geometry
        # ----------------------------------------------------

        conductor_right = conductor.get_right()

        joint_1 = np.array([
            4.35,
            conductor_center[1],
            0
        ])

        joint_2 = np.array([
            4.80,
            conductor_center[1],
            0
        ])

        ground_top = np.array([
            4.80,
            -2.15,
            0
        ])

        wire_1 = Line(
            conductor_right,
            joint_1,
            stroke_width=5,
            color=GROUND_COLOR
        )

        switch_segment = Line(
            joint_1,
            joint_2,
            stroke_width=5,
            color=GROUND_COLOR
        )

        wire_2 = Line(
            joint_2,
            ground_top,
            stroke_width=5,
            color=GROUND_COLOR
        )

        ground_symbol = make_ground_symbol(
            ground_top + DOWN * 0.45
        )

        ground_label = arabic_text(
            "الأرض",
            size=27,
            color=TEXT_SECONDARY
        ).next_to(
            ground_symbol,
            RIGHT,
            buff=0.18
        )

        self.play(
            Create(wire_1),
            Create(switch_segment),
            Create(wire_2),
            FadeIn(ground_symbol),
            FadeIn(ground_label),
            run_time=1.0
        )

        self.wait(1.1)

        grounding_note = arabic_text(
            "أصبح للإلكترونات مسار إلى الأرض",
            size=29,
            color=TEXT_SECONDARY
        ).move_to(
            UP * 2.45
        )

        self.play(
            FadeIn(grounding_note),
            run_time=0.8
        )

        self.wait(1.3)

        # ====================================================
        # PART 5 — ELECTRONS LEAVE
        # ====================================================

        self.play(
            FadeOut(step_2),
            run_time=0.4
        )

        electron_motion_title = arabic_text(
            "الجسم السالب يطرد بعض إلكترونات الموصل",
            size=32,
            weight=BOLD,
            color=NEGATIVE
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(electron_motion_title),
            run_time=0.8
        )

        self.wait(0.8)

        # ----------------------------------------------------
        # Build separate paths from each electron to ground
        # ----------------------------------------------------

        electron_paths = []

        for electron in far_negative:

            p = VMobject()

            start = electron.get_center()

            p.set_points_as_corners([
                start,
                conductor_right,
                joint_1,
                joint_2,
                ground_top
            ])

            electron_paths.append(p)

        # Electrons leave sequentially
        for electron, path in zip(
            list(far_negative),
            electron_paths
        ):

            self.play(
                MoveAlongPath(
                    electron,
                    path,
                    rate_func=linear
                ),
                run_time=0.65
            )

            self.play(
                FadeOut(
                    electron,
                    scale=0.6
                ),
                run_time=0.20
            )

        self.wait(0.8)

        # ====================================================
        # PART 6 — NET CHARGE IS NOW POSITIVE
        # ====================================================

        positive_net = MathTex(
            "Q_{\\mathrm{net}}>0",
            font_size=50,
            color=POSITIVE
        ).move_to(
            net_zero
        )

        self.play(
            ReplacementTransform(
                net_zero,
                positive_net
            ),
            run_time=0.8
        )

        self.wait(0.7)

        lost_electrons_note = arabic_text(
            "الموصل فقد إلكترونات",
            size=31,
            weight=BOLD,
            color=POSITIVE
        ).move_to(
            UP * 2.45
        )

        self.play(
            FadeOut(grounding_note),
            FadeIn(lost_electrons_note),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # STEP 3 — DISCONNECT GROUND FIRST
        # ====================================================

        self.play(
            FadeOut(electron_motion_title),
            FadeOut(lost_electrons_note),
            run_time=0.5
        )

        step_3 = arabic_text(
            "3. نفصل التأريض أولًا",
            size=37,
            weight=BOLD,
            color=POSITIVE
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(step_3),
            run_time=0.8
        )

        self.wait(1.0)

        first_emphasis = arabic_text(
            "أولًا",
            size=33,
            weight=BOLD,
            color=POSITIVE
        ).move_to(
            RIGHT * 4.75 + UP * 1.10
        )

        self.play(
            FadeIn(first_emphasis),
            run_time=0.6
        )

        self.wait(0.5)

        # ----------------------------------------------------
        # Open the grounding switch
        # ----------------------------------------------------

        self.play(
            Rotate(
                switch_segment,
                angle=50 * DEGREES,
                about_point=joint_1
            ),
            run_time=0.9
        )

        self.wait(1.0)

        disconnected_note = arabic_text(
            "الموصل أصبح معزولًا عن الأرض",
            size=29,
            color=ACCENT
        ).move_to(
            UP * 2.45
        )

        self.play(
            FadeIn(disconnected_note),
            run_time=0.8
        )

        self.wait(1.4)

        # ----------------------------------------------------
        # Explicitly emphasize:
        # rod still remains
        # ----------------------------------------------------

        rod_still_here = arabic_text(
            "والجسم السالب ما زال في مكانه",
            size=29,
            color=NEGATIVE
        ).next_to(
            rod_label,
            DOWN,
            buff=0.25
        )

        self.play(
            Indicate(
                rod,
                color=NEGATIVE,
                scale_factor=1.03
            ),
            FadeIn(rod_still_here),
            run_time=0.9
        )

        self.wait(1.5)

        # ====================================================
        # STEP 4 — REMOVE CHARGED OBJECT
        # ====================================================

        self.play(
            FadeOut(step_3),
            FadeOut(first_emphasis),
            FadeOut(disconnected_note),
            FadeOut(rod_still_here),
            run_time=0.5
        )

        step_4 = arabic_text(
            "4. الآن نبعد الجسم المشحون",
            size=35,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(step_4),
            run_time=0.8
        )

        self.wait(0.8)

        self.play(
            VGroup(
                rod,
                rod_charges,
                rod_label
            ).animate.shift(
                LEFT * 3.7
            ),
            run_time=1.5,
            rate_func=smooth
        )

        self.play(
            FadeOut(
                VGroup(
                    rod,
                    rod_charges,
                    rod_label
                )
            ),
            run_time=0.5
        )

        self.wait(0.8)

        # ====================================================
        # PART 7 — POSITIVE CHARGE REDISTRIBUTES
        # ====================================================

        self.play(
            FadeOut(step_4),
            run_time=0.4
        )

        redistribution_title = arabic_text(
            "بعد إبعاد الجسم السالب",
            size=34,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(redistribution_title),
            run_time=0.7
        )

        self.wait(0.8)

        redistribution_note = arabic_text(
            "تعيد الإلكترونات المتبقية ترتيب نفسها داخل الموصل",
            size=29,
            color=TEXT_SECONDARY
        ).move_to(
            UP * 2.45
        )

        self.play(
            FadeIn(redistribution_note),
            run_time=0.8
        )

        self.wait(1.0)

        # ----------------------------------------------------
        # Final positive surface-charge representation
        # Do NOT animate positive particles traveling.
        # Fade old representation out, new distribution in.
        # ----------------------------------------------------

        final_positive_positions = [
            conductor_center + LEFT * 1.48,
            conductor_center + RIGHT * 1.48,
            conductor_center + UP * 1.48,
            conductor_center + DOWN * 1.48,

            conductor_center + LEFT * 1.03 + UP * 1.03,
            conductor_center + RIGHT * 1.03 + UP * 1.03,
            conductor_center + LEFT * 1.03 + DOWN * 1.03,
            conductor_center + RIGHT * 1.03 + DOWN * 1.03,
        ]

        final_positive_surface = VGroup(
            *[
                positive_marker(
                    pos,
                    radius=0.085
                )
                for pos in final_positive_positions
            ]
        )

        self.play(
            FadeOut(near_positive),
            run_time=0.5
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(marker, scale=0.6)
                    for marker in final_positive_surface
                ],
                lag_ratio=0.06
            ),
            run_time=1.2
        )

        self.wait(1.0)

        distribution_explanation = arabic_text(
            "نقص الإلكترونات أصبح موزعًا على السطح الخارجي",
            size=30,
            weight=BOLD,
            color=POSITIVE
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeOut(redistribution_title),
            FadeIn(distribution_explanation),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 8 — REMOVE GROUND VISUAL
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    wire_1,
                    switch_segment,
                    wire_2,
                    ground_symbol,
                    ground_label
                )
            ),
            FadeOut(redistribution_note),
            run_time=0.7
        )

        # ====================================================
        # PART 9 — FINAL RESULT
        # ====================================================

        final_title = arabic_text(
            "النتيجة",
            size=37,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeOut(induction_title),
            FadeIn(final_title),
            run_time=0.8
        )

        self.wait(0.6)

        final_label = arabic_text(
            "الموصل أصبح موجب الشحنة",
            size=34,
            weight=BOLD,
            color=POSITIVE
        ).move_to(
            conductor_center + DOWN * 2.20
        )

        self.play(
            FadeOut(distribution_explanation),
            FadeIn(final_label),
            run_time=0.8
        )

        self.wait(0.8)

        self.play(
            Indicate(
                positive_net,
                color=POSITIVE,
                scale_factor=1.15
            ),
            run_time=0.9
        )

        self.wait(1.3)

        # ====================================================
        # PART 10 — KEY IDEA
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    conductor_group,
                    conductor_label,
                    positive_net,
                    final_positive_surface,
                    final_label,
                    final_title
                )
            ),
            run_time=0.8
        )

        key_title = arabic_text(
            "الشحن بالحث",
            size=44,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.48
        )

        key_1 = arabic_text(
            "الجسم المشحون الأصلي لم يلمس الموصل",
            size=33,
            weight=BOLD
        ).shift(
            UP * 0.65
        )

        key_2 = arabic_text(
            "لكن التأريض سمح للإلكترونات بمغادرة الموصل",
            size=31,
            color=NEGATIVE
        ).next_to(
            key_1,
            DOWN,
            buff=0.35
        )

        key_3 = arabic_text(
            "فبقي الموصل بشحنة موجبة صافية",
            size=33,
            weight=BOLD,
            color=POSITIVE
        ).next_to(
            key_2,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(key_title),
            run_time=0.7
        )

        self.play(
            FadeIn(key_1),
            run_time=0.8
        )

        self.wait(0.5)

        self.play(
            FadeIn(key_2),
            run_time=0.8
        )

        self.wait(0.5)

        self.play(
            FadeIn(key_3),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 11 — ORDER IS CRITICAL
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    key_title,
                    key_1,
                    key_2,
                    key_3
                )
            ),
            run_time=0.7
        )

        order_title = arabic_text(
            "ترتيب الخطوات مهم جدًا",
            size=39,
            weight=BOLD,
            color=POSITIVE
        ).to_edge(
            UP,
            buff=0.48
        )

        self.play(
            FadeIn(order_title),
            run_time=0.8
        )

        order_1 = arabic_text(
            "1. قرّب الجسم المشحون",
            size=29,
            color=NEGATIVE
        )

        order_2 = arabic_text(
            "2. صِل الموصل بالأرض",
            size=29
        )

        order_3 = arabic_text(
            "3. افصل التأريض أولًا",
            size=31,
            weight=BOLD,
            color=POSITIVE
        )

        order_4 = arabic_text(
            "4. ثم أبعد الجسم المشحون",
            size=29,
            color=ACCENT
        )

        order_group = VGroup(
            order_1,
            order_2,
            order_3,
            order_4
        ).arrange(
            DOWN,
            buff=0.35
        ).move_to(
            DOWN * 0.15
        )

        self.play(
            FadeIn(order_1),
            run_time=0.6
        )

        self.play(
            FadeIn(order_2),
            run_time=0.6
        )

        self.play(
            FadeIn(order_3),
            run_time=0.7
        )

        self.play(
            FadeIn(order_4),
            run_time=0.6
        )

        self.wait(1.5)

        self.play(
            Indicate(
                order_3,
                color=POSITIVE,
                scale_factor=1.08
            ),
            run_time=0.8
        )

        self.wait(1.3)

        # ====================================================
        # PART 12 — TRANSITION TO ELECTRIC FORCE
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    order_title,
                    order_group
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "كل هذا حدث من دون تلامس",
            size=36,
            weight=BOLD
        ).shift(
            UP * 0.55
        )

        transition_2 = arabic_text(
            "بين الجسم المشحون والموصل",
            size=34
        ).next_to(
            transition_1,
            DOWN,
            buff=0.25
        )

        transition_3 = arabic_text(
            "فكيف تؤثر الشحنات في بعضها عبر المسافة؟",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            transition_2,
            DOWN,
            buff=0.40
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
            run_time=0.8
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

    config.output_file = "scene_16_charging_by_induction"

    config.preview = True
    config.quality = "high_quality"

    Scene16ChargingByInduction().render()