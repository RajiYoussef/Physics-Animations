from manim import *


# ============================================================
# Scene 02
# الشحنة داخل الذرة
#
# الأفكار:
# - الانتقال من الظاهرة الماكروسكوبية إلى الذرة.
# - النواة تحتوي على بروتونات ونيوترونات.
# - الإلكترونات سالبة الشحنة.
# - البروتون موجب الشحنة.
# - النيوترون متعادل.
# - الشحنة خاصية فيزيائية وتقاس بالكولوم.
# - مقدار شحنة البروتون يساوي مقدار شحنة الإلكترون
#   لكن بإشارتين متعاكستين.
#
# ملاحظة:
# الرسم الذري هنا تمثيل تعليمي مبسط،
# وليس نموذجًا دقيقًا لحركة الإلكترونات في الذرة.
# ============================================================


class Scene02ChargeInsideAtom(MovingCameraScene):

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
        NEUTRAL = "#B7C0CC"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"
        ACCENT = "#7EE787"

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
        # PART 1 — TRANSITION FROM PREVIOUS SCENE
        # ====================================================

        intro = arabic_text(
            "لنبدأ من الذرة",
            size=48,
            weight=BOLD
        )

        self.play(
            FadeIn(
                intro,
                shift=UP * 0.15
            ),
            run_time=1.0
        )

        self.wait(1.5)

        self.play(
            intro.animate.to_edge(
                UP,
                buff=0.45
            ).scale(0.78),
            run_time=0.8
        )

        # ====================================================
        # PART 2 — SIMPLE ATOM
        # ====================================================

        # ----------------------------------------------------
        # Nucleus
        # ----------------------------------------------------

        proton_1 = Circle(
            radius=0.34,
            stroke_width=3,
            color=POSITIVE,
            fill_color=POSITIVE,
            fill_opacity=0.25
        ).shift(
            LEFT * 0.25 + UP * 0.20
        )

        proton_1_label = Text(
            "+",
            font_size=28,
            weight=BOLD,
            color=POSITIVE
        ).move_to(proton_1)

        neutron_1 = Circle(
            radius=0.34,
            stroke_width=3,
            color=NEUTRAL,
            fill_color=NEUTRAL,
            fill_opacity=0.12
        ).shift(
            RIGHT * 0.25 + UP * 0.20
        )

        neutron_1_label = Text(
            "0",
            font_size=24,
            weight=BOLD,
            color=NEUTRAL
        ).move_to(neutron_1)

        proton_2 = Circle(
            radius=0.34,
            stroke_width=3,
            color=POSITIVE,
            fill_color=POSITIVE,
            fill_opacity=0.25
        ).shift(
            DOWN * 0.32
        )

        proton_2_label = Text(
            "+",
            font_size=28,
            weight=BOLD,
            color=POSITIVE
        ).move_to(proton_2)

        nucleus = VGroup(
            proton_1,
            proton_1_label,
            neutron_1,
            neutron_1_label,
            proton_2,
            proton_2_label
        )

        # ----------------------------------------------------
        # Simplified electron region
        # ----------------------------------------------------

        orbit_1 = Ellipse(
            width=5.5,
            height=2.2,
            stroke_width=2,
            stroke_opacity=0.45,
            color=TEXT_SECONDARY
        )

        orbit_2 = Ellipse(
            width=5.5,
            height=2.2,
            stroke_width=2,
            stroke_opacity=0.45,
            color=TEXT_SECONDARY
        ).rotate(
            60 * DEGREES
        )

        orbit_3 = Ellipse(
            width=5.5,
            height=2.2,
            stroke_width=2,
            stroke_opacity=0.45,
            color=TEXT_SECONDARY
        ).rotate(
            -60 * DEGREES
        )

        electron_1 = Dot(
            orbit_1.point_from_proportion(0.15),
            radius=0.11,
            color=NEGATIVE
        )

        electron_2 = Dot(
            orbit_2.point_from_proportion(0.58),
            radius=0.11,
            color=NEGATIVE
        )

        electron_3 = Dot(
            orbit_3.point_from_proportion(0.86),
            radius=0.11,
            color=NEGATIVE
        )

        electron_sign_1 = Text(
            "−",
            font_size=18,
            weight=BOLD,
            color=TEXT_MAIN
        ).move_to(electron_1)

        electron_sign_2 = Text(
            "−",
            font_size=18,
            weight=BOLD,
            color=TEXT_MAIN
        ).move_to(electron_2)

        electron_sign_3 = Text(
            "−",
            font_size=18,
            weight=BOLD,
            color=TEXT_MAIN
        ).move_to(electron_3)

        atom = VGroup(
            orbit_1,
            orbit_2,
            orbit_3,
            nucleus,
            electron_1,
            electron_2,
            electron_3,
            electron_sign_1,
            electron_sign_2,
            electron_sign_3
        ).scale(0.95)

        # ----------------------------------------------------
        # Build nucleus first
        # ----------------------------------------------------

        self.play(
            FadeIn(nucleus, scale=0.7),
            run_time=1.0
        )

        self.wait(1.2)

        nucleus_label = arabic_text(
            "النواة",
            size=30,
            weight=BOLD,
            color=TEXT_SECONDARY
        ).next_to(
            nucleus,
            DOWN,
            buff=0.4
        )

        self.play(
            FadeIn(nucleus_label),
            run_time=0.7
        )

        self.wait(1.0)

        # ----------------------------------------------------
        # Then electron region
        # ----------------------------------------------------

        self.play(
            Create(orbit_1),
            Create(orbit_2),
            Create(orbit_3),
            run_time=1.3
        )

        self.play(
            LaggedStart(
                FadeIn(electron_1),
                FadeIn(electron_2),
                FadeIn(electron_3),
                FadeIn(electron_sign_1),
                FadeIn(electron_sign_2),
                FadeIn(electron_sign_3),
                lag_ratio=0.08
            ),
            run_time=1.0
        )

        self.wait(1.4)

        model_note = arabic_text(
            "تمثيل مبسط للذرة",
            size=24,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(model_note),
            run_time=0.6
        )

        self.wait(1.1)

        # ====================================================
        # PART 3 — PROTON
        # ====================================================

        self.play(
            FadeOut(model_note),
            FadeOut(nucleus_label),
            run_time=0.5
        )

        proton_title = arabic_text(
            "البروتون",
            size=40,
            weight=BOLD,
            color=POSITIVE
        ).to_edge(
            UP,
            buff=0.45
        )

        proton_description = arabic_text(
            "شحنة موجبة",
            size=33,
            color=POSITIVE
        ).next_to(
            proton_title,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeOut(intro),
            FadeIn(proton_title),
            Indicate(
                proton_1,
                color=POSITIVE,
                scale_factor=1.25
            ),
            run_time=0.9
        )

        self.play(
            FadeIn(proton_description),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 4 — NEUTRON
        # ====================================================

        self.play(
            FadeOut(proton_title),
            FadeOut(proton_description),
            run_time=0.5
        )

        neutron_title = arabic_text(
            "النيوترون",
            size=40,
            weight=BOLD,
            color=NEUTRAL
        ).to_edge(
            UP,
            buff=0.45
        )

        neutron_description = arabic_text(
            "متعادل كهربائيًا",
            size=33,
            color=NEUTRAL
        ).next_to(
            neutron_title,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(neutron_title),
            Indicate(
                neutron_1,
                color=NEUTRAL,
                scale_factor=1.25
            ),
            run_time=0.9
        )

        self.play(
            FadeIn(neutron_description),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 5 — ELECTRON
        # ====================================================

        self.play(
            FadeOut(neutron_title),
            FadeOut(neutron_description),
            run_time=0.5
        )

        electron_title = arabic_text(
            "الإلكترون",
            size=40,
            weight=BOLD,
            color=NEGATIVE
        ).to_edge(
            UP,
            buff=0.45
        )

        electron_description = arabic_text(
            "شحنة سالبة",
            size=33,
            color=NEGATIVE
        ).next_to(
            electron_title,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(electron_title),
            Indicate(
                electron_1,
                color=NEGATIVE,
                scale_factor=1.5
            ),
            run_time=0.9
        )

        self.play(
            FadeIn(electron_description),
            run_time=0.7
        )

        self.wait(1.5)

        # ====================================================
        # PART 6 — COMPACT ATOM AND INTRODUCE CHARGE
        # ====================================================

        self.play(
            FadeOut(electron_title),
            FadeOut(electron_description),
            atom.animate.scale(0.62).shift(RIGHT * 3.2),
            run_time=1.0
        )

        charge_title = arabic_text(
            "الشحنة الكهربائية",
            size=42,
            weight=BOLD,
            color=ACCENT
        ).move_to(
            LEFT * 3.2 + UP * 1.5
        )

        self.play(
            FadeIn(charge_title),
            run_time=0.8
        )

        self.wait(0.7)

        charge_definition_1 = arabic_text(
            "خاصية فيزيائية للمادة",
            size=31
        ).next_to(
            charge_title,
            DOWN,
            buff=0.35
        )

        charge_definition_2 = arabic_text(
            "تحدد مشاركتها في التفاعلات الكهربائية",
            size=28,
            color=TEXT_SECONDARY
        ).next_to(
            charge_definition_1,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(charge_definition_1),
            run_time=0.8
        )

        self.wait(0.8)

        self.play(
            FadeIn(charge_definition_2),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 7 — COULOMB UNIT
        # ====================================================

        self.play(
            FadeOut(charge_definition_1),
            FadeOut(charge_definition_2),
            run_time=0.5
        )

        unit_text = arabic_text(
            "تقاس الشحنة بوحدة الكولوم",
            size=32
        ).next_to(
            charge_title,
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(unit_text),
            run_time=0.8
        )

        self.wait(0.8)

        coulomb_symbol = Text(
            "C",
            font_size=72,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            unit_text,
            DOWN,
            buff=0.4
        )

        self.play(
            FadeIn(
                coulomb_symbol,
                scale=0.7
            ),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 8 — CLEAR AND COMPARE PROTON / ELECTRON
        # ====================================================

        self.play(
            FadeOut(atom),
            FadeOut(charge_title),
            FadeOut(unit_text),
            FadeOut(coulomb_symbol),
            run_time=0.7
        )

        comparison_title = arabic_text(
            "مقداران متساويان... وإشارتان متعاكستان",
            size=37,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(comparison_title),
            run_time=0.8
        )

        self.wait(1.0)

        # ----------------------------------------------------
        # Proton card
        # ----------------------------------------------------

        proton_card = RoundedRectangle(
            width=5.0,
            height=2.7,
            corner_radius=0.25,
            stroke_width=3,
            stroke_color=POSITIVE
        ).shift(
            LEFT * 3
        )

        proton_card_title = arabic_text(
            "البروتون",
            size=34,
            weight=BOLD,
            color=POSITIVE
        ).move_to(
            proton_card.get_top() + DOWN * 0.45
        )

        proton_sign = Text(
            "+",
            font_size=65,
            weight=BOLD,
            color=POSITIVE
        ).move_to(
            proton_card.get_center() + UP * 0.15
        )

        proton_card_group = VGroup(
            proton_card,
            proton_card_title,
            proton_sign
        )

        # ----------------------------------------------------
        # Electron card
        # ----------------------------------------------------

        electron_card = RoundedRectangle(
            width=5.0,
            height=2.7,
            corner_radius=0.25,
            stroke_width=3,
            stroke_color=NEGATIVE
        ).shift(
            RIGHT * 3
        )

        electron_card_title = arabic_text(
            "الإلكترون",
            size=34,
            weight=BOLD,
            color=NEGATIVE
        ).move_to(
            electron_card.get_top() + DOWN * 0.45
        )

        electron_sign = Text(
            "−",
            font_size=65,
            weight=BOLD,
            color=NEGATIVE
        ).move_to(
            electron_card.get_center() + UP * 0.15
        )

        electron_card_group = VGroup(
            electron_card,
            electron_card_title,
            electron_sign
        )

        self.play(
            FadeIn(proton_card_group),
            FadeIn(electron_card_group),
            run_time=1.0
        )

        self.wait(1.2)

        # ====================================================
        # PART 9 — PROTON VALUE
        # ====================================================

        proton_value = MathTex(
            "+1.602",
            r"\times",
            "10^{-19}",
            r"\,\mathrm{C}",
            font_size=48,
            color=POSITIVE
        ).move_to(
            proton_card.get_center() + DOWN * 0.75
        )

        self.play(
            FadeIn(
                proton_value,
                shift=UP * 0.1
            ),
            run_time=0.9
        )

        self.wait(1.6)

        # ====================================================
        # PART 10 — ELECTRON VALUE
        # ====================================================

        electron_value = MathTex(
            "-1.602",
            r"\times",
            "10^{-19}",
            r"\,\mathrm{C}",
            font_size=48,
            color=NEGATIVE
        ).move_to(
            electron_card.get_center() + DOWN * 0.75
        )

        self.play(
            FadeIn(
                electron_value,
                shift=UP * 0.1
            ),
            run_time=0.9
        )

        self.wait(1.5)

        # ====================================================
        # PART 11 — EMPHASIZE EQUAL MAGNITUDE
        # ====================================================

        magnitude_left = SurroundingRectangle(
            proton_value[0:3],
            buff=0.12,
            stroke_width=3,
            color=ACCENT
        )

        magnitude_right = SurroundingRectangle(
            electron_value[0:3],
            buff=0.12,
            stroke_width=3,
            color=ACCENT
        )

        equal_magnitude_text = arabic_text(
            "نفس المقدار",
            size=30,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.45
        )

        self.play(
            Create(magnitude_left),
            Create(magnitude_right),
            FadeIn(equal_magnitude_text),
            run_time=0.9
        )

        self.wait(1.4)

        # ====================================================
        # PART 12 — EMPHASIZE OPPOSITE SIGNS
        # ====================================================

        self.play(
            FadeOut(magnitude_left),
            FadeOut(magnitude_right),
            FadeOut(equal_magnitude_text),
            run_time=0.5
        )

        opposite_text = arabic_text(
            "لكن بإشارتين متعاكستين",
            size=32,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.45
        )

        self.play(
            Indicate(
                proton_sign,
                color=POSITIVE,
                scale_factor=1.25
            ),
            Indicate(
                electron_sign,
                color=NEGATIVE,
                scale_factor=1.25
            ),
            FadeIn(opposite_text),
            run_time=1.0
        )

        self.wait(1.6)

        # ====================================================
        # PART 13 — FINAL SUMMARY
        # ====================================================

        self.play(
            FadeOut(comparison_title),
            FadeOut(proton_card_group),
            FadeOut(electron_card_group),
            FadeOut(proton_value),
            FadeOut(electron_value),
            FadeOut(opposite_text),
            run_time=0.8
        )

        summary_title = arabic_text(
            "داخل الذرة",
            size=42,
            weight=BOLD
        ).shift(
            UP * 1.5
        )

        summary_proton = arabic_text(
            "البروتون → موجب",
            size=34,
            color=POSITIVE
        ).next_to(
            summary_title,
            DOWN,
            buff=0.45
        )

        summary_neutron = arabic_text(
            "النيوترون → متعادل",
            size=34,
            color=NEUTRAL
        ).next_to(
            summary_proton,
            DOWN,
            buff=0.3
        )

        summary_electron = arabic_text(
            "الإلكترون → سالب",
            size=34,
            color=NEGATIVE
        ).next_to(
            summary_neutron,
            DOWN,
            buff=0.3
        )

        self.play(
            FadeIn(summary_title),
            run_time=0.7
        )

        self.play(
            FadeIn(summary_proton),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(summary_neutron),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            FadeIn(summary_electron),
            run_time=0.7
        )

        self.wait(1.5)

        transition = arabic_text(
            "لكن متى يكون الجسم كله متعادلًا أو مشحونًا؟",
            size=32,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.45
        )

        self.play(
            FadeIn(transition),
            run_time=0.8
        )

        self.wait(2.0)

        self.play(
            FadeOut(summary_title),
            FadeOut(summary_proton),
            FadeOut(summary_neutron),
            FadeOut(summary_electron),
            FadeOut(transition),
            run_time=0.8
        )


# ============================================================
# DIRECT RENDERING FROM PYCHARM
# ============================================================

if __name__ == "__main__":

    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    config.output_file = "scene_02_charge_inside_atom"

    config.preview = True
    config.quality = "high_quality"

    Scene02ChargeInsideAtom().render()