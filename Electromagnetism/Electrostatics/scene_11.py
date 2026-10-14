from manim import *


# ============================================================
# Scene 11
# انحناء الماء نحو جسم مشحون — النسخة المصححة
#
# التسلسل الفيزيائي:
#
# 1. جزيئات الماء قطبية أصلًا.
# 2. قبل وجود الجسم المشحون تكون اتجاهاتها متنوعة.
# 3. عند تقريب جسم سالب، يؤثر المجال بعزم على الجزيئات.
# 4. تدور الجزيئات بحيث تتجه الجهة δ+ نحو الجسم السالب.
# 5. بعد إعادة التوجيه تصبح الجهة المخالفة أقرب قليلًا.
# 6. المجال الكهربائي غير منتظم ويكون أقوى قرب الجسم.
# 7. قوة الجذب على الجهة القريبة أكبر من قوة التنافر
#    على الجهة الأبعد.
# 8. المحصلة نحو الجسم المشحون.
#
# لا يصبح الماء ذا شحنة صافية.
# ============================================================


class Scene11WaterBending(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"
        ACCENT = "#7EE787"

        WATER = "#6CB6FF"
        WATER_LIGHT = "#A5D6FF"
        PLASTIC = "#C084FC"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

        ATTRACT = "#7EE787"
        REPEL = "#FFD166"

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

        def negative_marker(position, radius=0.085):

            circle = Circle(
                radius=radius,
                stroke_width=2,
                stroke_color=NEGATIVE,
                fill_color=NEGATIVE,
                fill_opacity=0.22
            ).move_to(position)

            sign = Text(
                "−",
                font_size=13,
                weight=BOLD,
                color=NEGATIVE
            ).move_to(circle)

            return VGroup(circle, sign)

        def make_water_molecule(center=ORIGIN, scale_factor=1.0):
            """
            جزيء ماء مبسط.

            الاتجاه الأساسي:
            H δ+ على اليسار
            O δ− على اليمين

            وهذا مناسب عندما يكون الجسم السالب على اليسار،
            لأن الجزيء بعد إعادة التوجيه يجعل δ+ أقرب إليه.
            """

            oxygen_center = center + RIGHT * 0.24 * scale_factor

            oxygen = Circle(
                radius=0.25 * scale_factor,
                stroke_width=3,
                stroke_color=NEGATIVE,
                fill_color=NEGATIVE,
                fill_opacity=0.16
            ).move_to(oxygen_center)

            oxygen_label = Text(
                "O",
                font_size=22 * scale_factor,
                weight=BOLD,
                color=NEGATIVE
            ).move_to(oxygen)

            oxygen_partial = MathTex(
                r"\delta^-",
                font_size=24 * scale_factor,
                color=NEGATIVE
            ).next_to(
                oxygen,
                RIGHT,
                buff=0.06
            )

            h1_center = (
                center
                + LEFT * 0.42 * scale_factor
                + UP * 0.29 * scale_factor
            )

            h2_center = (
                center
                + LEFT * 0.42 * scale_factor
                + DOWN * 0.29 * scale_factor
            )

            bond_1 = Line(
                oxygen_center,
                h1_center,
                stroke_width=4,
                color=TEXT_SECONDARY
            )

            bond_2 = Line(
                oxygen_center,
                h2_center,
                stroke_width=4,
                color=TEXT_SECONDARY
            )

            hydrogen_1 = Circle(
                radius=0.17 * scale_factor,
                stroke_width=3,
                stroke_color=POSITIVE,
                fill_color=POSITIVE,
                fill_opacity=0.15
            ).move_to(h1_center)

            hydrogen_2 = Circle(
                radius=0.17 * scale_factor,
                stroke_width=3,
                stroke_color=POSITIVE,
                fill_color=POSITIVE,
                fill_opacity=0.15
            ).move_to(h2_center)

            h1_label = Text(
                "H",
                font_size=17 * scale_factor,
                weight=BOLD,
                color=POSITIVE
            ).move_to(hydrogen_1)

            h2_label = Text(
                "H",
                font_size=17 * scale_factor,
                weight=BOLD,
                color=POSITIVE
            ).move_to(hydrogen_2)

            h1_partial = MathTex(
                r"\delta^+",
                font_size=19 * scale_factor,
                color=POSITIVE
            ).next_to(
                hydrogen_1,
                LEFT,
                buff=0.04
            )

            h2_partial = MathTex(
                r"\delta^+",
                font_size=19 * scale_factor,
                color=POSITIVE
            ).next_to(
                hydrogen_2,
                LEFT,
                buff=0.04
            )

            return VGroup(
                bond_1,
                bond_2,
                oxygen,
                oxygen_label,
                oxygen_partial,
                hydrogen_1,
                hydrogen_2,
                h1_label,
                h2_label,
                h1_partial,
                h2_partial
            )

        # ====================================================
        # PART 1 — OPENING
        # ====================================================

        title = arabic_text(
            "لماذا ينحني خيط الماء نحو جسم مشحون؟",
            size=43,
            weight=BOLD
        )

        self.play(
            FadeIn(title, shift=UP * 0.15),
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
        # PART 2 — STRAIGHT WATER STREAM
        # ====================================================

        faucet_horizontal = RoundedRectangle(
            width=3.0,
            height=0.55,
            corner_radius=0.18,
            stroke_width=4,
            stroke_color=TEXT_SECONDARY,
            fill_color=TEXT_SECONDARY,
            fill_opacity=0.10
        ).move_to(
            RIGHT * 2.7 + UP * 2.15
        )

        faucet_vertical = RoundedRectangle(
            width=0.7,
            height=1.1,
            corner_radius=0.15,
            stroke_width=4,
            stroke_color=TEXT_SECONDARY,
            fill_color=TEXT_SECONDARY,
            fill_opacity=0.10
        ).move_to(
            RIGHT * 4.0 + UP * 1.55
        )

        nozzle = RoundedRectangle(
            width=0.85,
            height=0.35,
            corner_radius=0.12,
            stroke_width=4,
            stroke_color=TEXT_SECONDARY,
            fill_color=TEXT_SECONDARY,
            fill_opacity=0.12
        ).move_to(
            RIGHT * 4.0 + UP * 0.85
        )

        faucet = VGroup(
            faucet_horizontal,
            faucet_vertical,
            nozzle
        )

        water_stream = Line(
            start=RIGHT * 4.0 + UP * 0.65,
            end=RIGHT * 4.0 + DOWN * 2.7,
            stroke_width=13,
            color=WATER
        )

        water_highlight = Line(
            start=RIGHT * 3.94 + UP * 0.6,
            end=RIGHT * 3.94 + DOWN * 2.65,
            stroke_width=3,
            color=WATER_LIGHT
        )

        self.play(
            FadeIn(faucet),
            Create(water_stream),
            Create(water_highlight),
            run_time=1.1
        )

        self.wait(1.3)

        # ====================================================
        # PART 3 — CHARGED OBJECT APPROACHES
        # ====================================================

        rod = RoundedRectangle(
            width=4.2,
            height=0.65,
            corner_radius=0.25,
            stroke_width=4,
            stroke_color=PLASTIC,
            fill_color=PLASTIC,
            fill_opacity=0.14
        ).rotate(
            -8 * DEGREES
        ).move_to(
            LEFT * 3.4 + DOWN * 0.1
        )

        rod_charges = VGroup(
            negative_marker(rod.get_center() + LEFT * 1.4),
            negative_marker(rod.get_center() + LEFT * 0.7),
            negative_marker(rod.get_center()),
            negative_marker(rod.get_center() + RIGHT * 0.7),
            negative_marker(rod.get_center() + RIGHT * 1.4)
        )

        rod_label = arabic_text(
            "جسم سالب الشحنة",
            size=29,
            color=NEGATIVE
        ).next_to(
            rod,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(rod),
            FadeIn(rod_charges),
            FadeIn(rod_label),
            run_time=0.9
        )

        self.wait(1.0)

        approach_text = arabic_text(
            "نقرّبه من خيط الماء...",
            size=32,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(approach_text),
            run_time=0.7
        )

        self.play(
            VGroup(
                rod,
                rod_charges,
                rod_label
            ).animate.shift(
                RIGHT * 1.25
            ),
            run_time=1.3
        )

        self.wait(0.7)

        # ====================================================
        # PART 4 — WATER BENDS
        # ====================================================

        curved_water = CubicBezier(
            RIGHT * 4.0 + UP * 0.65,
            RIGHT * 4.0 + DOWN * 0.35,
            RIGHT * 3.45 + DOWN * 1.45,
            RIGHT * 2.85 + DOWN * 2.7,
            stroke_width=13,
            color=WATER
        )

        curved_highlight = CubicBezier(
            RIGHT * 3.94 + UP * 0.60,
            RIGHT * 3.93 + DOWN * 0.35,
            RIGHT * 3.40 + DOWN * 1.45,
            RIGHT * 2.80 + DOWN * 2.65,
            stroke_width=3,
            color=WATER_LIGHT
        )

        self.play(
            ReplacementTransform(
                water_stream,
                curved_water
            ),
            ReplacementTransform(
                water_highlight,
                curved_highlight
            ),
            FadeOut(approach_text),
            run_time=1.5
        )

        bend_text = arabic_text(
            "الماء ينجذب نحو الجسم المشحون",
            size=34,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(bend_text),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 5 — GO MICROSCOPIC
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    faucet,
                    curved_water,
                    curved_highlight,
                    rod,
                    rod_charges,
                    rod_label,
                    bend_text,
                    title
                )
            ),
            run_time=0.8
        )

        molecule_title = arabic_text(
            "جزيء الماء قطبي أصلًا",
            size=39,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.45
        )

        molecule = make_water_molecule(
            ORIGIN,
            scale_factor=1.9
        )

        self.play(
            FadeIn(molecule_title),
            FadeIn(molecule, scale=0.75),
            run_time=1.0
        )

        self.wait(1.1)

        positive_side_text = arabic_text(
            "جهة موجبة جزئيًا",
            size=28,
            color=POSITIVE
        ).move_to(
            LEFT * 3.3 + DOWN * 1.6
        )

        negative_side_text = arabic_text(
            "جهة سالبة جزئيًا",
            size=28,
            color=NEGATIVE
        ).move_to(
            RIGHT * 3.3 + DOWN * 1.6
        )

        self.play(
            FadeIn(positive_side_text),
            FadeIn(negative_side_text),
            run_time=0.8
        )

        self.wait(1.2)

        neutral_note = arabic_text(
            "الجزيء متعادل ككل",
            size=31,
            weight=BOLD
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(neutral_note),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 6 — MANY RANDOMLY ORIENTED MOLECULES
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    molecule,
                    molecule_title,
                    positive_side_text,
                    negative_side_text,
                    neutral_note
                )
            ),
            run_time=0.8
        )

        before_title = arabic_text(
            "قبل وجود الجسم المشحون",
            size=37,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(before_title),
            run_time=0.7
        )

        molecule_data = [
            ([-3.5, 1.0, 0], 25),
            ([-1.2, 1.0, 0], -65),
            ([1.2, 1.0, 0], 95),
            ([3.5, 1.0, 0], -25),
            ([-3.5, -0.8, 0], 140),
            ([-1.2, -0.8, 0], 50),
            ([1.2, -0.8, 0], -120),
            ([3.5, -0.8, 0], 165),
        ]

        molecules = VGroup()

        for pos, angle in molecule_data:

            mol = make_water_molecule(
                pos,
                scale_factor=0.65
            )

            mol.rotate(
                angle * DEGREES,
                about_point=mol.get_center()
            )

            molecules.add(mol)

        self.play(
            LaggedStart(
                *[
                    FadeIn(mol, scale=0.7)
                    for mol in molecules
                ],
                lag_ratio=0.08
            ),
            run_time=1.3
        )

        random_note = arabic_text(
            "اتجاهات الجزيئات متنوعة",
            size=31,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(random_note),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 7 — BRING NEGATIVE BODY
        # ====================================================

        self.play(
            FadeOut(random_note),
            FadeOut(before_title),
            run_time=0.5
        )

        charged_body = RoundedRectangle(
            width=1.1,
            height=5.2,
            corner_radius=0.22,
            stroke_width=4,
            stroke_color=PLASTIC,
            fill_color=PLASTIC,
            fill_opacity=0.12
        ).move_to(
            LEFT * 5.7
        )

        charged_marks = VGroup()

        for y in [-1.8, -0.9, 0, 0.9, 1.8]:

            charged_marks.add(
                negative_marker(
                    LEFT * 5.7 + UP * y
                )
            )

        charged_label = arabic_text(
            "جسم سالب",
            size=28,
            color=NEGATIVE
        ).next_to(
            charged_body,
            UP,
            buff=0.2
        )

        reorient_title = arabic_text(
            "المجال يؤثر بعزم على الجزيئات",
            size=36,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(charged_body),
            FadeIn(charged_marks),
            FadeIn(charged_label),
            FadeIn(reorient_title),
            run_time=0.9
        )

        self.wait(1.2)

        # ====================================================
        # PART 8 — ROTATE FIRST
        # ====================================================

        rotation_note = arabic_text(
            "فتبدأ الجزيئات بإعادة توجيه نفسها",
            size=32,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(rotation_note),
            run_time=0.8
        )

        rotations = []

        for mol, (_, angle) in zip(
            molecules,
            molecule_data
        ):
            rotations.append(
                Rotate(
                    mol,
                    angle=(-angle) * DEGREES,
                    about_point=mol.get_center()
                )
            )

        self.play(
            *rotations,
            run_time=1.8
        )

        self.wait(1.1)

        # ====================================================
        # PART 9 — NOW SAY WHY THE OPPOSITE SIDE IS NEAR
        # ====================================================

        oriented_note_1 = arabic_text(
            "بعد إعادة التوجيه",
            size=31,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.35
        )

        oriented_note_2 = arabic_text(
            "تواجه الجهة δ+ الجسم السالب",
            size=33,
            weight=BOLD,
            color=POSITIVE
        ).next_to(
            oriented_note_1,
            UP,
            buff=0.25
        )

        self.play(
            FadeOut(rotation_note),
            FadeIn(oriented_note_1),
            FadeIn(oriented_note_2),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 10 — ISOLATE ONE MOLECULE
        # ====================================================

        self.play(
            FadeOut(molecules),
            FadeOut(reorient_title),
            FadeOut(oriented_note_1),
            FadeOut(oriented_note_2),
            run_time=0.7
        )

        representative = make_water_molecule(
            RIGHT * 1.1,
            scale_factor=1.8
        )

        self.play(
            FadeIn(representative),
            run_time=0.8
        )

        self.wait(1.0)

        orientation_title = arabic_text(
            "الآن أصبحت الجهة المخالفة أقرب",
            size=36,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(orientation_title),
            run_time=0.8
        )

        self.wait(1.1)

        # ====================================================
        # PART 11 — SHOW NEAR / FAR
        # ====================================================

        positive_side_point = (
            representative[5].get_center()
            + representative[6].get_center()
        ) / 2

        negative_side_point = representative[2].get_center()

        near_arrow = DoubleArrow(
            start=charged_body.get_right() + UP * 0.8,
            end=positive_side_point + UP * 0.8,
            buff=0.06,
            stroke_width=3,
            color=POSITIVE,
            max_tip_length_to_length_ratio=0.12
        )

        far_arrow = DoubleArrow(
            start=charged_body.get_right() + DOWN * 0.8,
            end=negative_side_point + DOWN * 0.8,
            buff=0.06,
            stroke_width=3,
            color=NEGATIVE,
            max_tip_length_to_length_ratio=0.12
        )

        near_label = arabic_text(
            "δ+ أقرب",
            size=26,
            color=POSITIVE
        ).next_to(
            near_arrow,
            UP,
            buff=0.1
        )

        far_label = arabic_text(
            "δ− أبعد",
            size=26,
            color=NEGATIVE
        ).next_to(
            far_arrow,
            DOWN,
            buff=0.1
        )

        self.play(
            GrowFromCenter(near_arrow),
            FadeIn(near_label),
            run_time=0.7
        )

        self.wait(0.5)

        self.play(
            GrowFromCenter(far_arrow),
            FadeIn(far_label),
            run_time=0.7
        )

        self.wait(1.4)

        # ====================================================
        # PART 12 — NONUNIFORM FIELD
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    near_arrow,
                    far_arrow,
                    near_label,
                    far_label,
                    orientation_title
                )
            ),
            run_time=0.5
        )

        field_title = arabic_text(
            "لكن هذا وحده لا يكفي",
            size=37,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        field_subtitle = arabic_text(
            "المجال الكهربائي غير منتظم",
            size=33,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            field_title,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(field_title),
            run_time=0.7
        )

        self.play(
            FadeIn(field_subtitle),
            run_time=0.7
        )

        self.wait(1.0)

        # Field arrows decrease with distance from negative rod.
        field_arrow_1 = Arrow(
            start=LEFT * 3.2 + UP * 1.05,
            end=LEFT * 4.7 + UP * 1.05,
            buff=0,
            stroke_width=6,
            color=ACCENT
        )

        field_arrow_2 = Arrow(
            start=LEFT * 2.3,
            end=LEFT * 3.45,
            buff=0,
            stroke_width=5,
            color=ACCENT
        )

        field_arrow_3 = Arrow(
            start=LEFT * 1.35 + DOWN * 1.05,
            end=LEFT * 2.15 + DOWN * 1.05,
            buff=0,
            stroke_width=4,
            color=ACCENT
        )

        self.play(
            GrowArrow(field_arrow_1),
            GrowArrow(field_arrow_2),
            GrowArrow(field_arrow_3),
            run_time=0.9
        )

        field_note = arabic_text(
            "أقوى قرب الجسم المشحون، وأضعف بعيدًا عنه",
            size=30,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(field_note),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 13 — FORCE COMPARISON
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    field_title,
                    field_subtitle,
                    field_arrow_1,
                    field_arrow_2,
                    field_arrow_3,
                    field_note
                )
            ),
            run_time=0.6
        )

        force_title = arabic_text(
            "إذن ماذا يحدث للقوتين؟",
            size=37,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(force_title),
            run_time=0.7
        )

        self.wait(0.8)

        attraction_arrow = Arrow(
            start=positive_side_point + LEFT * 0.15,
            end=positive_side_point + LEFT * 2.2,
            buff=0,
            stroke_width=7,
            color=ATTRACT,
            max_tip_length_to_length_ratio=0.13
        )

        attraction_label = arabic_text(
            "جذب أقوى",
            size=28,
            weight=BOLD,
            color=ATTRACT
        ).next_to(
            attraction_arrow,
            UP,
            buff=0.18
        )

        repulsion_arrow = Arrow(
            start=negative_side_point + RIGHT * 0.2 + DOWN * 0.65,
            end=negative_side_point + RIGHT * 1.2 + DOWN * 0.65,
            buff=0,
            stroke_width=4,
            color=REPEL,
            max_tip_length_to_length_ratio=0.18
        )

        repulsion_label = arabic_text(
            "تنافر أضعف",
            size=26,
            color=REPEL
        ).next_to(
            repulsion_arrow,
            DOWN,
            buff=0.18
        )

        self.play(
            GrowArrow(attraction_arrow),
            FadeIn(attraction_label),
            run_time=0.8
        )

        self.wait(0.7)

        self.play(
            GrowArrow(repulsion_arrow),
            FadeIn(repulsion_label),
            run_time=0.8
        )

        self.wait(1.5)

        explanation = arabic_text(
            "لأن المجال أقوى عند الجهة الأقرب",
            size=31,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(explanation),
            run_time=0.8
        )

        self.wait(1.5)

        # ====================================================
        # PART 14 — NET FORCE
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    attraction_arrow,
                    attraction_label,
                    repulsion_arrow,
                    repulsion_label,
                    explanation,
                    force_title
                )
            ),
            run_time=0.6
        )

        net_arrow = Arrow(
            start=representative.get_center(),
            end=representative.get_center() + LEFT * 2.25,
            buff=0,
            stroke_width=7,
            color=ACCENT,
            max_tip_length_to_length_ratio=0.14
        )

        net_label = arabic_text(
            "محصلة القوة → نحو الجسم المشحون",
            size=32,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            net_arrow,
            DOWN,
            buff=0.25
        )

        self.play(
            GrowArrow(net_arrow),
            FadeIn(net_label),
            run_time=0.9
        )

        self.wait(1.7)

        # ====================================================
        # PART 15 — RETURN TO WATER
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    charged_body,
                    charged_marks,
                    charged_label,
                    representative,
                    net_arrow,
                    net_label
                )
            ),
            run_time=0.8
        )

        faucet_2 = VGroup(
            faucet_horizontal.copy(),
            faucet_vertical.copy(),
            nozzle.copy()
        )

        curved_water_2 = CubicBezier(
            RIGHT * 4.0 + UP * 0.65,
            RIGHT * 4.0 + DOWN * 0.35,
            RIGHT * 3.4 + DOWN * 1.45,
            RIGHT * 2.75 + DOWN * 2.7,
            stroke_width=13,
            color=WATER
        )

        rod_2 = RoundedRectangle(
            width=4.2,
            height=0.65,
            corner_radius=0.25,
            stroke_width=4,
            stroke_color=PLASTIC,
            fill_color=PLASTIC,
            fill_opacity=0.14
        ).rotate(
            -8 * DEGREES
        ).move_to(
            LEFT * 2.15 + DOWN * 0.1
        )

        rod_2_marks = VGroup(
            negative_marker(rod_2.get_center() + LEFT * 1.4),
            negative_marker(rod_2.get_center() + LEFT * 0.7),
            negative_marker(rod_2.get_center()),
            negative_marker(rod_2.get_center() + RIGHT * 0.7),
            negative_marker(rod_2.get_center() + RIGHT * 1.4)
        )

        self.play(
            FadeIn(faucet_2),
            Create(curved_water_2),
            FadeIn(rod_2),
            FadeIn(rod_2_marks),
            run_time=1.0
        )

        self.wait(1.0)

        result_text = arabic_text(
            "لذلك ينحني خيط الماء نحو الجسم المشحون",
            size=36,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeIn(result_text),
            run_time=0.8
        )

        self.wait(1.3)

        neutral_water = arabic_text(
            "من دون أن يصبح الماء مشحونًا بشحنة صافية",
            size=30,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(neutral_water),
            run_time=0.8
        )

        self.wait(1.6)

        # ====================================================
        # PART 16 — SUMMARY
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    faucet_2,
                    curved_water_2,
                    rod_2,
                    rod_2_marks,
                    result_text,
                    neutral_water
                )
            ),
            run_time=0.8
        )

        summary_title = arabic_text(
            "لماذا ينجذب الماء؟",
            size=41,
            weight=BOLD
        ).to_edge(
            UP,
            buff=0.5
        )

        summary_1 = arabic_text(
            "1. جزيئات الماء قطبية أصلًا",
            size=32,
            color=ACCENT
        ).shift(
            UP * 0.9
        )

        summary_2 = arabic_text(
            "2. المجال يعيد توجيه الجزيئات",
            size=32
        ).next_to(
            summary_1,
            DOWN,
            buff=0.35
        )

        summary_3 = arabic_text(
            "3. الجهة المخالفة تواجه الجسم المشحون",
            size=32,
            color=POSITIVE
        ).next_to(
            summary_2,
            DOWN,
            buff=0.35
        )

        summary_4 = arabic_text(
            "4. المجال أقوى عند الجهة الأقرب",
            size=32
        ).next_to(
            summary_3,
            DOWN,
            buff=0.35
        )

        summary_5 = arabic_text(
            "المحصلة → جذب",
            size=35,
            weight=BOLD,
            color=ACCENT
        ).next_to(
            summary_4,
            DOWN,
            buff=0.4
        )

        self.play(
            FadeIn(summary_title),
            run_time=0.7
        )

        self.play(
            FadeIn(summary_1),
            run_time=0.7
        )

        self.wait(0.4)

        self.play(
            FadeIn(summary_2),
            run_time=0.7
        )

        self.wait(0.4)

        self.play(
            FadeIn(summary_3),
            run_time=0.7
        )

        self.wait(0.4)

        self.play(
            FadeIn(summary_4),
            run_time=0.7
        )

        self.wait(0.4)

        self.play(
            FadeIn(summary_5),
            run_time=0.7
        )

        self.wait(1.8)

        # ====================================================
        # PART 17 — TRANSITION
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    summary_title,
                    summary_1,
                    summary_2,
                    summary_3,
                    summary_4,
                    summary_5
                )
            ),
            run_time=0.8
        )

        transition_1 = arabic_text(
            "لكن الشحنات لا تتحرك بالطريقة نفسها",
            size=35
        ).shift(
            UP * 0.45
        )

        transition_2 = arabic_text(
            "داخل جميع المواد",
            size=40,
            weight=BOLD
        ).next_to(
            transition_1,
            DOWN,
            buff=0.25
        )

        transition_3 = arabic_text(
            "وهنا يظهر الفرق بين الموصل والعازل",
            size=32,
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

    config.output_file = "scene_11_water_bending"

    config.preview = True
    config.quality = "high_quality"

    Scene11WaterBending().render()