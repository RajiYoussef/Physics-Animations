from manim import *


# ============================================================
# Scene 13
# أشباه الموصلات — إعادة بناء كاملة
#
# الهدف:
# شرح معنى "شبه موصل" فعليًا بدل الاكتفاء بقول
# إنه بين الموصل والعازل.
#
# التسلسل:
#
# 1. مثال: السيليكون.
# 2. معظم الإلكترونات ليست حرة للحركة عبر المادة.
# 3. نمثل ذلك بنطاق التكافؤ ونطاق التوصيل.
# 4. بينهما فجوة طاقة.
# 5. إذا حصل إلكترون على طاقة كافية ينتقل إلى نطاق التوصيل.
# 6. عندها يستطيع المساهمة في التوصيل الكهربائي.
# 7. يمكن تغيير عدد حاملات الشحنة بطرق مثل:
#       - الحرارة
#       - الضوء
#       - الإشابة
# 8. لذلك ناقلية شبه الموصل ليست قيمة ثابتة.
# 9. ولهذا أصبح السيليكون أساس الإلكترونيات الحديثة.
#
# ملاحظة:
# الرسم تمثيل مبسط لنطاقات الطاقة.
# ============================================================


class Scene13Semiconductors(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        NEGATIVE = "#58A6FF"
        POSITIVE = "#F2A65A"
        ACCENT = "#7EE787"

        SILICON = "#FFD166"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

        BAND_FILL = "#30363D"
        BAND_BORDER = "#8B949E"

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

        def make_electron(position, radius=0.105):

            circle = Circle(
                radius=radius,
                stroke_width=2,
                stroke_color=NEGATIVE,
                fill_color=NEGATIVE,
                fill_opacity=0.22
            ).move_to(position)

            sign = Text(
                "−",
                font_size=15,
                weight=BOLD,
                color=NEGATIVE
            ).move_to(circle)

            return VGroup(circle, sign)

        def make_hole(position):

            circle = Circle(
                radius=0.11,
                stroke_width=3,
                stroke_color=POSITIVE,
                fill_opacity=0
            ).move_to(position)

            return circle

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "أشباه الموصلات",
            size=46,
            weight=BOLD,
            color=SILICON
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.15
            ),
            run_time=1.0
        )

        self.wait(1.2)

        question = arabic_text(
            "ما الذي يجعل السيليكون مختلفًا؟",
            size=36,
            weight=BOLD
        ).next_to(
            title,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(question),
            run_time=0.8
        )

        self.wait(1.5)

        self.play(
            FadeOut(title),
            FadeOut(question),
            run_time=0.7
        )

        # ====================================================
        # PART 2 — SILICON
        # ====================================================

        silicon_sample = RoundedRectangle(
            width=3.8,
            height=2.5,
            corner_radius=0.22,
            stroke_width=4,
            stroke_color=SILICON,
            fill_color=SILICON,
            fill_opacity=0.06
        )

        silicon_symbol = Text(
            "Si",
            font_size=68,
            weight=BOLD,
            color=SILICON
        ).move_to(
            silicon_sample.get_center()
        )

        silicon_group = VGroup(
            silicon_sample,
            silicon_symbol
        )

        silicon_title = arabic_text(
            "السيليكون",
            size=36,
            weight=BOLD,
            color=SILICON
        ).next_to(
            silicon_group,
            UP,
            buff=0.35
        )

        self.play(
            FadeIn(
                silicon_group,
                scale=0.8
            ),
            FadeIn(silicon_title),
            run_time=0.9
        )

        self.wait(1.2)

        statement_1 = arabic_text(
            "في السيليكون لا تكون معظم الإلكترونات",
            size=31
        ).next_to(
            silicon_group,
            DOWN,
            buff=0.45
        )

        statement_2 = arabic_text(
            "حرة للحركة عبر المادة مثلما يحدث في المعادن",
            size=31,
            weight=BOLD
        ).next_to(
            statement_1,
            DOWN,
            buff=0.20
        )

        self.play(
            FadeIn(statement_1),
            run_time=0.8
        )

        self.play(
            FadeIn(statement_2),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 3 — TRANSITION TO ENERGY BAND MODEL
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    silicon_group,
                    silicon_title,
                    statement_1,
                    statement_2
                )
            ),
            run_time=0.8
        )

        model_title = arabic_text(
            "لنستخدم تمثيلًا مبسطًا للطاقة",
            size=38,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        model_note = arabic_text(
            "تمثيل مبسط لنطاقات الطاقة",
            size=24,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(model_title),
            FadeIn(model_note),
            run_time=0.8
        )

        # ====================================================
        # PART 4 — VALENCE BAND
        # ====================================================

        valence_band = RoundedRectangle(
            width=8.0,
            height=1.45,
            corner_radius=0.18,
            stroke_width=3,
            stroke_color=BAND_BORDER,
            fill_color=BAND_FILL,
            fill_opacity=0.30
        ).move_to(
            DOWN * 1.45
        )

        valence_label = arabic_text(
            "نطاق التكافؤ",
            size=29,
            weight=BOLD
        ).move_to(
            valence_band.get_center()
            + DOWN * 0.40
        )

        self.play(
            FadeIn(valence_band),
            FadeIn(valence_label),
            run_time=0.8
        )

        self.wait(0.7)

        # Electrons initially in valence band
        valence_positions = [
            [-2.9, -1.20, 0],
            [-1.9, -1.20, 0],
            [-0.9, -1.20, 0],
            [0.1, -1.20, 0],
            [1.1, -1.20, 0],
            [2.1, -1.20, 0],
            [3.0, -1.20, 0],
        ]

        valence_electrons = VGroup(
            *[
                make_electron(pos)
                for pos in valence_positions
            ]
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(e, scale=0.6)
                    for e in valence_electrons
                ],
                lag_ratio=0.08
            ),
            run_time=1.1
        )

        self.wait(1.0)

        valence_explanation = arabic_text(
            "هنا تكون الإلكترونات مرتبطة بحالات في المادة",
            size=29,
            color=TEXT_SECONDARY
        ).move_to(
            UP * 0.05
        )

        self.play(
            FadeIn(valence_explanation),
            run_time=0.8
        )

        self.wait(1.3)

        # ====================================================
        # PART 5 — CONDUCTION BAND
        # ====================================================

        conduction_band = RoundedRectangle(
            width=8.0,
            height=1.45,
            corner_radius=0.18,
            stroke_width=3,
            stroke_color=ACCENT,
            fill_color=ACCENT,
            fill_opacity=0.035
        ).move_to(
            UP * 1.45
        )

        conduction_label = arabic_text(
            "نطاق التوصيل",
            size=29,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            conduction_band.get_center()
            + UP * 0.38
        )

        self.play(
            FadeIn(conduction_band),
            FadeIn(conduction_label),
            run_time=0.8
        )

        self.wait(1.0)

        # ====================================================
        # PART 6 — BAND GAP
        # ====================================================

        gap_arrow = DoubleArrow(
            start=DOWN * 0.60,
            end=UP * 0.60,
            buff=0.03,
            stroke_width=3,
            color=SILICON
        ).shift(
            LEFT * 4.65
        )

        gap_label = arabic_text(
            "فجوة طاقة",
            size=27,
            color=SILICON
        ).next_to(
            gap_arrow,
            LEFT,
            buff=0.20
        )

        self.play(
            FadeOut(valence_explanation),
            GrowFromCenter(gap_arrow),
            FadeIn(gap_label),
            run_time=0.8
        )

        self.wait(1.3)

        gap_explanation = arabic_text(
            "يحتاج الإلكترون إلى طاقة كافية للوصول إلى نطاق التوصيل",
            size=30,
            weight=BOLD
        ).move_to(
            ORIGIN
        )

        self.play(
            FadeIn(gap_explanation),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 7 — GIVE ONE ELECTRON ENERGY
        # ====================================================

        self.play(
            FadeOut(gap_explanation),
            run_time=0.5
        )

        selected_electron = valence_electrons[3]

        self.play(
            Indicate(
                selected_electron,
                color=NEGATIVE,
                scale_factor=1.5
            ),
            run_time=0.8
        )

        energy_arrow = Arrow(
            start=selected_electron.get_center() + UP * 0.25,
            end=selected_electron.get_center() + UP * 1.55,
            buff=0,
            stroke_width=5,
            color=SILICON,
            max_tip_length_to_length_ratio=0.14
        )

        energy_label = arabic_text(
            "طاقة كافية",
            size=27,
            weight=BOLD,
            color=SILICON
        ).next_to(
            energy_arrow,
            RIGHT,
            buff=0.20
        )

        self.play(
            GrowArrow(energy_arrow),
            FadeIn(energy_label),
            run_time=0.8
        )

        self.wait(0.8)

        # Save original location for hole
        original_position = selected_electron.get_center()

        target_position = UP * 1.22

        self.play(
            selected_electron.animate.move_to(
                target_position
            ),
            run_time=1.4,
            rate_func=smooth
        )

        self.wait(0.5)

        hole = make_hole(
            original_position
        )

        hole_label = arabic_text(
            "فجوة",
            size=24,
            color=POSITIVE
        ).next_to(
            hole,
            UP,
            buff=0.12
        )

        self.play(
            FadeIn(hole),
            FadeIn(hole_label),
            FadeOut(energy_arrow),
            FadeOut(energy_label),
            run_time=0.7
        )

        self.wait(1.2)

        # ====================================================
        # PART 8 — ELECTRON CAN NOW CONTRIBUTE TO CONDUCTION
        # ====================================================

        conduction_statement = arabic_text(
            "الآن أصبح لدينا حامل شحنة يستطيع المساهمة في التوصيل",
            size=30,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            ORIGIN
        )

        self.play(
            FadeIn(conduction_statement),
            run_time=0.8
        )

        self.wait(1.0)

        movement_arrow = Arrow(
            start=selected_electron.get_center() + LEFT * 0.2,
            end=RIGHT * 2.8 + UP * 1.22,
            buff=0.08,
            stroke_width=4,
            color=NEGATIVE,
            max_tip_length_to_length_ratio=0.10
        )

        self.play(
            GrowArrow(movement_arrow),
            run_time=0.7
        )

        self.play(
            selected_electron.animate.move_to(
                RIGHT * 2.6 + UP * 1.22
            ),
            run_time=1.4,
            rate_func=linear
        )

        self.wait(1.2)

        # ====================================================
        # PART 9 — CLEAN UP FIRST EXAMPLE
        # ====================================================

        self.play(
            FadeOut(conduction_statement),
            FadeOut(movement_arrow),
            FadeOut(hole_label),
            run_time=0.5
        )

        # ====================================================
        # PART 10 — WHAT CAN CHANGE CARRIER NUMBER?
        # ====================================================

        control_title = arabic_text(
            "وهنا تأتي الخاصية المهمة",
            size=37,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeOut(model_title),
            FadeIn(control_title),
            run_time=0.8
        )

        self.wait(0.8)

        control_statement = arabic_text(
            "يمكن تغيير عدد حاملات الشحنة في شبه الموصل",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            UP * 0.15
        )

        self.play(
            FadeIn(control_statement),
            run_time=0.8
        )

        self.wait(1.3)

        # ====================================================
        # PART 11 — THREE REAL METHODS
        # ====================================================

        self.play(
            FadeOut(control_statement),
            run_time=0.5
        )

        method_heat = RoundedRectangle(
            width=2.5,
            height=1.1,
            corner_radius=0.18,
            stroke_width=3,
            stroke_color=POSITIVE,
            fill_color=POSITIVE,
            fill_opacity=0.04
        ).move_to(
            LEFT * 3.0 + UP * 0.10
        )

        method_heat_text = arabic_text(
            "الحرارة",
            size=30,
            weight=BOLD,
            color=POSITIVE
        ).move_to(method_heat)

        method_light = RoundedRectangle(
            width=2.5,
            height=1.1,
            corner_radius=0.18,
            stroke_width=3,
            stroke_color=SILICON,
            fill_color=SILICON,
            fill_opacity=0.04
        ).move_to(
            UP * 0.10
        )

        method_light_text = arabic_text(
            "الضوء",
            size=30,
            weight=BOLD,
            color=SILICON
        ).move_to(method_light)

        method_doping = RoundedRectangle(
            width=2.5,
            height=1.1,
            corner_radius=0.18,
            stroke_width=3,
            stroke_color=ACCENT,
            fill_color=ACCENT,
            fill_opacity=0.04
        ).move_to(
            RIGHT * 3.0 + UP * 0.10
        )

        method_doping_text = arabic_text(
            "الإشابة",
            size=30,
            weight=BOLD,
            color=ACCENT
        ).move_to(method_doping)

        methods_title = arabic_text(
            "أمثلة على طرق تغيير عدد حاملات الشحنة",
            size=29,
            color=TEXT_SECONDARY
        ).move_to(
            UP * 0.95
        )

        self.play(
            FadeIn(methods_title),
            run_time=0.7
        )

        self.play(
            FadeIn(method_heat),
            FadeIn(method_heat_text),
            run_time=0.6
        )

        self.wait(0.3)

        self.play(
            FadeIn(method_light),
            FadeIn(method_light_text),
            run_time=0.6
        )

        self.wait(0.3)

        self.play(
            FadeIn(method_doping),
            FadeIn(method_doping_text),
            run_time=0.6
        )

        self.wait(1.5)

        # ====================================================
        # PART 12 — SHOW MORE CARRIERS
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    method_heat,
                    method_heat_text,
                    method_light,
                    method_light_text,
                    method_doping,
                    method_doping_text,
                    methods_title
                )
            ),
            run_time=0.7
        )

        carrier_title = arabic_text(
            "عندما يزداد عدد حاملات الشحنة",
            size=34,
            weight=BOLD
        ).move_to(
            ORIGIN
        )

        self.play(
            FadeIn(carrier_title),
            run_time=0.8
        )

        self.wait(0.8)

        self.play(
            FadeOut(carrier_title),
            run_time=0.4
        )

        # Select three more electrons
        extra_1 = valence_electrons[1]
        extra_2 = valence_electrons[4]
        extra_3 = valence_electrons[6]

        original_1 = extra_1.get_center()
        original_2 = extra_2.get_center()
        original_3 = extra_3.get_center()

        target_1 = LEFT * 2.1 + UP * 1.20
        target_2 = LEFT * 0.5 + UP * 1.20
        target_3 = RIGHT * 1.1 + UP * 1.20

        self.play(
            extra_1.animate.move_to(target_1),
            extra_2.animate.move_to(target_2),
            extra_3.animate.move_to(target_3),
            run_time=1.5
        )

        hole_1 = make_hole(original_1)
        hole_2 = make_hole(original_2)
        hole_3 = make_hole(original_3)

        extra_holes = VGroup(
            hole_1,
            hole_2,
            hole_3
        )

        self.play(
            FadeIn(extra_holes),
            run_time=0.6
        )

        self.wait(1.1)

        carrier_result_1 = arabic_text(
            "حاملات شحنة أكثر",
            size=31,
            weight=BOLD,
            color=NEGATIVE
        ).move_to(
            UP * 0.15
        )

        self.play(
            FadeIn(carrier_result_1),
            run_time=0.8
        )

        self.wait(0.7)

        carrier_result_2 = arabic_text(
            "→ يمكن أن تزداد الناقلية الكهربائية",
            size=33,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            carrier_result_1,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(carrier_result_2),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 13 — MAIN CONCLUSION
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    carrier_result_1,
                    carrier_result_2,
                    conduction_band,
                    conduction_label,
                    valence_band,
                    valence_label,
                    valence_electrons,
                    selected_electron,
                    hole,
                    extra_holes,
                    gap_arrow,
                    gap_label,
                    model_note,
                    control_title
                )
            ),
            run_time=0.8
        )

        conclusion_title = arabic_text(
            "إذن ما الذي يميز شبه الموصل؟",
            size=39,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.5
        )

        self.play(
            FadeIn(conclusion_title),
            run_time=0.8
        )

        self.wait(0.8)

        wrong_statement = arabic_text(
            "ليس مجرد مادة ذات توصيل متوسط وثابت",
            size=33,
            color=TEXT_SECONDARY
        ).shift(
            UP * 0.45
        )

        self.play(
            FadeIn(wrong_statement),
            run_time=0.8
        )

        self.wait(0.9)

        key_statement = arabic_text(
            "يمكن تغيير ناقليته والتحكم فيها",
            size=39,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            wrong_statement,
            DOWN,
            buff=0.40
        )

        self.play(
            FadeIn(
                key_statement,
                scale=0.85
            ),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 14 — WHY SILICON MATTERS
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    conclusion_title,
                    wrong_statement,
                    key_statement
                )
            ),
            run_time=0.7
        )

        electronics_title = arabic_text(
            "ولهذا أصبح السيليكون مهمًا جدًا",
            size=38,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.5
        )

        chip = RoundedRectangle(
            width=3.3,
            height=3.3,
            corner_radius=0.28,
            stroke_width=4,
            stroke_color=SILICON,
            fill_color=SILICON,
            fill_opacity=0.06
        )

        inner_chip = RoundedRectangle(
            width=2.0,
            height=2.0,
            corner_radius=0.15,
            stroke_width=3,
            stroke_color=ACCENT,
            fill_color=ACCENT,
            fill_opacity=0.035
        )

        chip_symbol = Text(
            "Si",
            font_size=58,
            weight=BOLD,
            color=SILICON
        )

        chip_group = VGroup(
            chip,
            inner_chip,
            chip_symbol
        )

        self.play(
            FadeIn(electronics_title),
            FadeIn(
                chip_group,
                scale=0.8
            ),
            run_time=0.9
        )

        self.wait(1.0)

        electronics_statement = arabic_text(
            "أساس الترانزستورات والرقائق الإلكترونية",
            size=33,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            chip_group,
            DOWN,
            buff=0.40
        )

        self.play(
            FadeIn(electronics_statement),
            run_time=0.8
        )

        self.wait(1.7)

        # ====================================================
        # PART 15 — THIS IS ONLY AN ASIDE
        # ====================================================

        aside = arabic_text(
            "لكن فيزياء أشباه الموصلات تستحق موضوعًا مستقلًا",
            size=29,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.28
        )

        self.play(
            FadeIn(aside),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 16 — RETURN TO ELECTROSTATICS
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    electronics_title,
                    chip_group,
                    electronics_statement,
                    aside
                )
            ),
            run_time=0.8
        )

        return_1 = arabic_text(
            "والآن نعود إلى الكهرباء الساكنة",
            size=37,
            weight=BOLD,
            color=ACCENT
        ).shift(
            UP * 0.65
        )

        return_2 = arabic_text(
            "ماذا يحدث عندما يلمس جسم مشحون",
            size=33
        ).next_to(
            return_1,
            DOWN,
            buff=0.35
        )

        return_3 = arabic_text(
            "موصلًا متعادلًا؟",
            size=37,
            weight=BOLD
        ).next_to(
            return_2,
            DOWN,
            buff=0.20
        )

        self.play(
            FadeIn(return_1),
            run_time=0.8
        )

        self.wait(0.5)

        self.play(
            FadeIn(return_2),
            FadeIn(return_3),
            run_time=0.8
        )

        self.wait(2.0)

        self.play(
            FadeOut(
                VGroup(
                    return_1,
                    return_2,
                    return_3
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

    config.output_file = "scene_13_semiconductors"

    config.preview = True
    config.quality = "high_quality"

    Scene13Semiconductors().render()