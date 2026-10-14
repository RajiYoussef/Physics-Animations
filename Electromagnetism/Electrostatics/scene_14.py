from manim import *


# ============================================================
# Scene 14
# الشحن بالتوصيل / بالتلامس
#
# الفكرة:
# - لدينا موصل مشحون سالبًا.
# - ولدينا موصل متعادل.
# - قبل التلامس لا تنتقل شحنة بين الجسمين.
# - عند حدوث تلامس مباشر يصبح الجسمان موصلًا واحدًا
#   مؤقتًا، فتستطيع الشحنات الحرة إعادة توزيع نفسها.
# - تنتقل بعض الإلكترونات الزائدة إلى الجسم الثاني.
# - بعد فصل الجسمين يحتفظ الجسم الثاني بشحنة سالبة صافية.
#
# مهم:
# العلامات الزرقاء تمثل الإلكترونات الزائدة فقط،
# وليست جميع إلكترونات المادة.
# ============================================================


class Scene14ChargingByConduction(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        NEGATIVE = "#58A6FF"
        POSITIVE = "#F2A65A"
        ACCENT = "#7EE787"

        METAL = "#B7C0CC"
        METAL_DARK = "#6E7681"

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

        def make_metal_sphere(center, radius=1.15):

            sphere = Circle(
                radius=radius,
                stroke_width=4,
                stroke_color=METAL,
                fill_color=METAL,
                fill_opacity=0.07
            ).move_to(center)

            highlight = Arc(
                radius=radius * 0.67,
                start_angle=110 * DEGREES,
                angle=80 * DEGREES,
                stroke_width=3,
                color="#E6EDF3"
            ).move_to(
                center + LEFT * 0.18 + UP * 0.16
            )

            return VGroup(
                sphere,
                highlight
            )

        def electron_marker(position, radius=0.095):

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

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "الشحن بالتوصيل",
            size=46,
            weight=BOLD,
            color=ACCENT
        )

        subtitle = arabic_text(
            "أو الشحن بالتلامس",
            size=34,
            color=TEXT_SECONDARY
        ).next_to(
            title,
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(title, shift=UP * 0.15),
            run_time=0.9
        )

        self.play(
            FadeIn(subtitle),
            run_time=0.7
        )

        self.wait(1.4)

        self.play(
            FadeOut(subtitle),
            title.animate.to_edge(
                UP,
                buff=0.42
            ).scale(0.85),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — TWO METAL CONDUCTORS
        # ====================================================

        sphere_a = make_metal_sphere(
            LEFT * 3.4 + DOWN * 0.15
        )

        sphere_b = make_metal_sphere(
            RIGHT * 3.4 + DOWN * 0.15
        )

        label_a = arabic_text(
            "موصل مشحون",
            size=29,
            color=NEGATIVE
        ).move_to(
            LEFT * 3.4 + UP * 1.65
        )

        label_b = arabic_text(
            "موصل متعادل",
            size=29,
            color=ACCENT
        ).move_to(
            RIGHT * 3.4 + UP * 1.65
        )

        self.play(
            FadeIn(sphere_a),
            FadeIn(sphere_b),
            FadeIn(label_a),
            FadeIn(label_b),
            run_time=1.0
        )

        self.wait(1.0)

        # ====================================================
        # PART 3 — EXCESS ELECTRONS ON FIRST SPHERE
        # ====================================================

        a_center = sphere_a[0].get_center()

        excess_a = VGroup(
            electron_marker(a_center + LEFT * 1.02 + UP * 0.25),
            electron_marker(a_center + LEFT * 0.65 + UP * 0.85),
            electron_marker(a_center + UP * 1.05),
            electron_marker(a_center + RIGHT * 0.65 + UP * 0.85),
            electron_marker(a_center + RIGHT * 1.02 + UP * 0.20),
            electron_marker(a_center + RIGHT * 0.86 + DOWN * 0.58),
            electron_marker(a_center + DOWN * 1.02),
            electron_marker(a_center + LEFT * 0.86 + DOWN * 0.58)
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(e, scale=0.7)
                    for e in excess_a
                ],
                lag_ratio=0.06
            ),
            run_time=1.1
        )

        self.wait(0.8)

        charge_a_label = MathTex(
            "Q_A<0",
            font_size=44,
            color=NEGATIVE
        ).move_to(
            LEFT * 3.4 + DOWN * 1.75
        )

        charge_b_label = MathTex(
            "Q_B=0",
            font_size=44,
            color=ACCENT
        ).move_to(
            RIGHT * 3.4 + DOWN * 1.75
        )

        self.play(
            FadeIn(charge_a_label),
            FadeIn(charge_b_label),
            run_time=0.8
        )

        self.wait(1.2)

        excess_note = arabic_text(
            "العلامات الزرقاء تمثل الإلكترونات الزائدة فقط",
            size=26,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(excess_note),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 4 — BEFORE CONTACT
        # ====================================================

        self.play(
            FadeOut(excess_note),
            run_time=0.4
        )

        before_contact = arabic_text(
            "قبل التلامس",
            size=34,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(before_contact),
            run_time=0.7
        )

        self.wait(0.8)

        no_transfer = arabic_text(
            "لا يوجد مسار مباشر لانتقال الشحنة بين الجسمين",
            size=29,
            color=TEXT_SECONDARY
        ).next_to(
            before_contact,
            UP,
            buff=0.25
        )

        self.play(
            FadeIn(no_transfer),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 5 — BRING SPHERES TOGETHER
        # ====================================================

        self.play(
            FadeOut(before_contact),
            FadeOut(no_transfer),
            FadeOut(charge_a_label),
            FadeOut(charge_b_label),
            run_time=0.5
        )

        contact_title = arabic_text(
            "الآن يحدث تلامس مباشر",
            size=35,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(contact_title),
            run_time=0.7
        )

        move_left = RIGHT * 2.15
        move_right = LEFT * 2.15

        self.play(
            sphere_a.animate.shift(move_left),
            excess_a.animate.shift(move_left),
            label_a.animate.shift(move_left),

            sphere_b.animate.shift(move_right),
            label_b.animate.shift(move_right),

            run_time=1.5
        )

        self.wait(1.0)

        # ====================================================
        # PART 6 — CONTACT POINT
        # ====================================================

        contact_glow = Dot(
            ORIGIN + DOWN * 0.15,
            radius=0.13,
            color=ACCENT
        )

        self.play(
            FadeIn(contact_glow, scale=1.6),
            run_time=0.4
        )

        self.wait(0.4)

        contact_explanation = arabic_text(
            "أصبح هناك مسار موصل بين الجسمين",
            size=30,
            color=ACCENT
        ).move_to(
            UP * 2.0
        )

        self.play(
            FadeIn(contact_explanation),
            run_time=0.8
        )

        self.wait(1.2)

        # ====================================================
        # PART 7 — ELECTRONS BEGIN TO REDISTRIBUTE
        # ====================================================

        self.play(
            FadeOut(contact_title),
            run_time=0.4
        )

        redistribution_title = arabic_text(
            "الإلكترونات الزائدة تعيد توزيع نفسها",
            size=34,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(redistribution_title),
            run_time=0.8
        )

        self.wait(0.7)

        # ----------------------------------------------------
        # Move selected excess electrons from sphere A
        # onto sphere B.
        # ----------------------------------------------------

        moving_1 = excess_a[1]
        moving_2 = excess_a[3]
        moving_3 = excess_a[5]

        self.play(
            Indicate(
                VGroup(
                    moving_1,
                    moving_2,
                    moving_3
                ),
                color=NEGATIVE,
                scale_factor=1.35
            ),
            run_time=0.8
        )

        self.wait(0.5)

        b_center_now = sphere_b[0].get_center()

        target_1 = b_center_now + UP * 1.03
        target_2 = b_center_now + RIGHT * 0.88 + UP * 0.48
        target_3 = b_center_now + RIGHT * 0.90 + DOWN * 0.45

        self.play(
            moving_1.animate.move_to(target_1),
            moving_2.animate.move_to(target_2),
            moving_3.animate.move_to(target_3),
            run_time=1.7,
            rate_func=smooth
        )

        self.wait(1.0)

        # ====================================================
        # PART 8 — EXPLAIN THAT IT'S CHARGE TRANSFER
        # ====================================================

        transfer_text = arabic_text(
            "بعض الإلكترونات انتقلت إلى الموصل الثاني",
            size=31,
            weight=BOLD,
            color=NEGATIVE
        ).move_to(
            UP * 2.0
        )

        self.play(
            FadeOut(contact_explanation),
            FadeIn(transfer_text),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 9 — DISTRIBUTION WHILE TOUCHING
        # ====================================================

        redistribution_note = arabic_text(
            "أثناء التلامس يتصرف الجسمان كموصل متصل",
            size=29,
            color=TEXT_SECONDARY
        ).next_to(
            redistribution_title,
            UP,
            buff=0.25
        )

        self.play(
            FadeIn(redistribution_note),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 10 — SEPARATE THE SPHERES
        # ====================================================

        self.play(
            FadeOut(transfer_text),
            FadeOut(redistribution_title),
            FadeOut(redistribution_note),
            FadeOut(contact_glow),
            run_time=0.5
        )

        separation_title = arabic_text(
            "ثم نفصل الجسمين",
            size=35,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.32
        )

        self.play(
            FadeIn(separation_title),
            run_time=0.7
        )

        # ----------------------------------------------------
        # Electrons that stayed with A:
        # excess_a indices 0, 2, 4, 6, 7
        #
        # transferred electrons:
        # indices 1, 3, 5
        # ----------------------------------------------------

        left_shift = LEFT * 2.15
        right_shift = RIGHT * 2.15

        self.play(
            sphere_a.animate.shift(left_shift),
            label_a.animate.shift(left_shift),

            *[
                excess_a[i].animate.shift(left_shift)
                for i in [0, 2, 4, 6, 7]
            ],

            sphere_b.animate.shift(right_shift),
            label_b.animate.shift(right_shift),

            moving_1.animate.shift(right_shift),
            moving_2.animate.shift(right_shift),
            moving_3.animate.shift(right_shift),

            run_time=1.5
        )

        self.wait(1.0)

        # ====================================================
        # PART 11 — FINAL CHARGES
        # ====================================================

        self.play(
            FadeOut(separation_title),
            run_time=0.4
        )

        final_title = arabic_text(
            "بعد الفصل",
            size=35,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeOut(title),
            FadeIn(final_title),
            run_time=0.8
        )

        self.wait(0.8)

        left_final = arabic_text(
            "ما زال يحمل شحنة سالبة",
            size=28,
            color=NEGATIVE
        ).move_to(
            LEFT * 3.4 + DOWN * 1.75
        )

        right_final = arabic_text(
            "أصبح ذا شحنة سالبة صافية",
            size=28,
            weight=BOLD,
            color=NEGATIVE
        ).move_to(
            RIGHT * 3.4 + DOWN * 1.75
        )

        self.play(
            FadeIn(left_final),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(right_final),
            run_time=0.8
        )

        self.wait(1.3)

        right_charge = MathTex(
            "Q_B<0",
            font_size=48,
            color=NEGATIVE
        ).move_to(
            RIGHT * 3.4 + UP * 1.75
        )

        self.play(
            ReplacementTransform(
                label_b,
                right_charge
            ),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 12 — EMPHASIZE THE KEY POINT
        # ====================================================

        key_1 = arabic_text(
            "كان الجسم الثاني متعادلًا",
            size=30,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.72
        )

        key_2 = arabic_text(
            "وبعد التلامس أصبح مشحونًا",
            size=33,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(key_1),
            run_time=0.7
        )

        self.wait(0.4)

        self.play(
            FadeIn(key_2),
            run_time=0.7
        )

        self.wait(1.6)

        # ====================================================
        # PART 13 — NAME THE PROCESS
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    sphere_a,
                    sphere_b,
                    excess_a,
                    label_a,
                    right_charge,
                    left_final,
                    right_final,
                    key_1,
                    key_2,
                    final_title
                )
            ),
            run_time=0.8
        )

        process_title = arabic_text(
            "الشحن بالتوصيل",
            size=44,
            weight=BOLD,
            color=ACCENT
        ).shift(
            UP * 0.8
        )

        process_subtitle = arabic_text(
            "تلامس مباشر يسمح بانتقال الشحنة",
            size=34,
            weight=BOLD
        ).next_to(
            process_title,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(process_title),
            run_time=0.8
        )

        self.wait(0.5)

        self.play(
            FadeIn(process_subtitle),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 14 — IMPORTANT DISTINCTION
        # ====================================================

        distinction = arabic_text(
            "هنا حدث انتقال فعلي للإلكترونات بين الجسمين",
            size=30,
            color=NEGATIVE
        ).next_to(
            process_subtitle,
            DOWN,
            buff=0.40
        )

        self.play(
            FadeIn(distinction),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 15 — TRANSITION TO INDUCTION
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    process_title,
                    process_subtitle,
                    distinction
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "لكن هل نستطيع التأثير في شحنة موصل",
            size=34
        ).shift(
            UP * 0.55
        )

        transition_2 = arabic_text(
            "من دون أن نلمسه؟",
            size=40,
            weight=BOLD
        ).next_to(
            transition_1,
            DOWN,
            buff=0.25
        )

        transition_3 = arabic_text(
            "نعم... لكن أول ما يحدث هو الاستقطاب",
            size=32,
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

    config.output_file = "scene_14_charging_by_conduction"

    config.preview = True
    config.quality = "high_quality"

    Scene14ChargingByConduction().render()