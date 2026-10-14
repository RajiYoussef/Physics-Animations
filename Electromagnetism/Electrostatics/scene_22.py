from manim import *
import numpy as np


# ============================================================
# Scene 22
# مبدأ التراكب
#
# الفكرة:
#
# عند نقطة P:
#
# الشحنة الأولى تنشئ E1
# الشحنة الثانية تنشئ E2
#
# المجال الكلي هو الجمع المتجهي:
#
#       E_net = E1 + E2
#
# في المثال:
# شحنتان موجبتان متساويتان
# والنقطة P فوق منتصفهما.
#
# المركبتان الأفقيتان تتعاكسان،
# بينما المركبتان الرأسيتان تتضافران.
#
# المحصلة تتجه إلى أعلى.
# ============================================================


class Scene22Superposition(Scene):

    def construct(self):

        # ====================================================
        # GENERAL SETTINGS
        # ====================================================

        self.camera.background_color = "#0D1117"

        arabic_font = "DejaVu Sans"

        POSITIVE = "#F2A65A"
        NEGATIVE = "#58A6FF"

        TEXT_MAIN = "#F4F4F4"
        TEXT_SECONDARY = "#B7C0CC"

        ACCENT = "#7EE787"
        FIELD_COLOR = "#7EE787"
        GUIDE_COLOR = "#B7C0CC"

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

        def make_charge(
            center,
            sign="+"
        ):

            color = (
                POSITIVE
                if sign == "+"
                else NEGATIVE
            )

            circle = Circle(
                radius=0.47,
                stroke_width=4,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.15
            ).move_to(center)

            sign_text = Text(
                sign,
                font=arabic_font,
                font_size=43,
                weight=BOLD,
                color=color
            ).move_to(circle)

            return VGroup(
                circle,
                sign_text
            )

        def unit_vector(vector):

            norm = np.linalg.norm(vector)

            if norm == 0:
                return RIGHT

            return vector / norm

        # ====================================================
        # POSITIONS
        # ====================================================

        q1_pos = np.array([
            -2.6,
            -1.25,
            0
        ])

        q2_pos = np.array([
            2.6,
            -1.25,
            0
        ])

        p_pos = np.array([
            0,
            1.05,
            0
        ])

        # ====================================================
        # PART 1 — TITLE
        # ====================================================

        title = arabic_text(
            "مبدأ التراكب",
            size=44,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.42
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.15
            ),
            run_time=0.9
        )

        self.wait(0.9)

        question = arabic_text(
            "من أين يأتي المجال عند نقطة بين عدة شحنات؟",
            size=31
        ).next_to(
            title,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(question),
            run_time=0.8
        )

        self.wait(1.3)

        # ====================================================
        # PART 2 — TWO SOURCE CHARGES
        # ====================================================

        q1 = make_charge(
            q1_pos,
            "+"
        )

        q2 = make_charge(
            q2_pos,
            "+"
        )

        q1_label = MathTex(
            "Q_1",
            font_size=38,
            color=POSITIVE
        ).next_to(
            q1,
            DOWN,
            buff=0.18
        )

        q2_label = MathTex(
            "Q_2",
            font_size=38,
            color=POSITIVE
        ).next_to(
            q2,
            DOWN,
            buff=0.18
        )

        self.play(
            FadeIn(q1, scale=0.8),
            FadeIn(q2, scale=0.8),
            FadeIn(q1_label),
            FadeIn(q2_label),
            run_time=0.9
        )

        self.wait(0.8)

        # ====================================================
        # PART 3 — POINT P
        # ====================================================

        point_p = Dot(
            p_pos,
            radius=0.075,
            color=TEXT_MAIN
        )

        p_label = MathTex(
            "P",
            font_size=40,
            color=TEXT_MAIN
        ).next_to(
            point_p,
            UP,
            buff=0.15
        )

        self.play(
            FadeIn(
                point_p,
                scale=1.5
            ),
            FadeIn(p_label),
            run_time=0.7
        )

        self.wait(0.8)

        self.play(
            FadeOut(question),
            run_time=0.4
        )

        # ====================================================
        # PART 4 — FIELD FROM Q1
        # ====================================================

        direction_1 = unit_vector(
            p_pos - q1_pos
        )

        e1_length = 1.55

        e1_end = (
            p_pos
            + direction_1 * e1_length
        )

        e1_arrow = Arrow(
            start=p_pos,
            end=e1_end,
            buff=0,
            stroke_width=6,
            color=TEXT_SECONDARY,
            max_tip_length_to_length_ratio=0.16
        )

        e1_label = MathTex(
            r"\vec{E}_1",
            font_size=43,
            color=TEXT_SECONDARY
        ).next_to(
            e1_arrow,
            RIGHT,
            buff=0.10
        )

        e1_text = arabic_text(
            "الشحنة الأولى تنشئ مجالًا عند النقطة",
            size=29,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            GrowArrow(e1_arrow),
            FadeIn(e1_label),
            FadeIn(e1_text),
            run_time=0.9
        )

        self.wait(1.2)

        # ====================================================
        # PART 5 — FIELD FROM Q2
        # ====================================================

        direction_2 = unit_vector(
            p_pos - q2_pos
        )

        e2_end = (
            p_pos
            + direction_2 * e1_length
        )

        e2_arrow = Arrow(
            start=p_pos,
            end=e2_end,
            buff=0,
            stroke_width=6,
            color=TEXT_SECONDARY,
            max_tip_length_to_length_ratio=0.16
        )

        e2_label = MathTex(
            r"\vec{E}_2",
            font_size=43,
            color=TEXT_SECONDARY
        ).next_to(
            e2_arrow,
            LEFT,
            buff=0.10
        )

        e2_text = arabic_text(
            "والشحنة الثانية تنشئ مجالًا آخر",
            size=29,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            ReplacementTransform(
                e1_text,
                e2_text
            ),
            GrowArrow(e2_arrow),
            FadeIn(e2_label),
            run_time=0.9
        )

        self.wait(1.2)

        # ====================================================
        # PART 6 — VECTOR ADDITION
        # ====================================================

        add_text = arabic_text(
            "المجال الحقيقي هو محصلة المتجهين",
            size=31,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            ReplacementTransform(
                e2_text,
                add_text
            ),
            run_time=0.7
        )

        self.wait(0.8)

        # ====================================================
        # PARALLELOGRAM CONSTRUCTION
        # ====================================================

        vector_1 = e1_end - p_pos
        vector_2 = e2_end - p_pos

        resultant_vector = (
            vector_1 + vector_2
        )

        resultant_end = (
            p_pos + resultant_vector
        )

        guide_1 = DashedLine(
            start=e1_end,
            end=resultant_end,
            dash_length=0.08,
            stroke_width=2,
            color=GUIDE_COLOR
        ).set_opacity(0.55)

        guide_2 = DashedLine(
            start=e2_end,
            end=resultant_end,
            dash_length=0.08,
            stroke_width=2,
            color=GUIDE_COLOR
        ).set_opacity(0.55)

        self.play(
            Create(guide_1),
            Create(guide_2),
            run_time=0.8
        )

        self.wait(0.5)

        # ====================================================
        # RESULTANT FIELD
        # ====================================================

        net_arrow = Arrow(
            start=p_pos,
            end=resultant_end,
            buff=0,
            stroke_width=8,
            color=FIELD_COLOR,
            max_tip_length_to_length_ratio=0.14
        )

        net_label = MathTex(
            r"\vec{E}_{\mathrm{net}}",
            font_size=45,
            color=FIELD_COLOR
        ).next_to(
            net_arrow,
            RIGHT,
            buff=0.15
        )

        self.play(
            GrowArrow(net_arrow),
            FadeIn(net_label),
            run_time=0.9
        )

        self.wait(1.2)

        # ====================================================
        # PART 7 — EQUATION
        # ====================================================

        equation = MathTex(
            r"\vec{E}_{\mathrm{net}}"
            r"="
            r"\vec{E}_1"
            r"+"
            r"\vec{E}_2",
            font_size=58
        )

        equation.set_color_by_tex(
            r"\vec{E}_{\mathrm{net}}",
            FIELD_COLOR
        )

        equation.set_color_by_tex(
            r"\vec{E}_1",
            TEXT_SECONDARY
        )

        equation.set_color_by_tex(
            r"\vec{E}_2",
            TEXT_SECONDARY
        )

        equation.move_to(
            DOWN * 2.35
        )

        self.play(
            FadeOut(add_text),
            FadeIn(equation),
            run_time=0.8
        )

        self.wait(1.4)

        # ====================================================
        # PART 8 — WHY RESULTANT IS VERTICAL
        # ====================================================

        horizontal_text = arabic_text(
            "هنا تتعاكس الأجزاء الأفقية",
            size=29,
            color=TEXT_SECONDARY
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeOut(equation),
            FadeIn(horizontal_text),
            run_time=0.7
        )

        # ----------------------------------------------------
        # Horizontal component indicators
        # ----------------------------------------------------

        horizontal_left = Arrow(
            start=p_pos + DOWN * 0.28,
            end=p_pos + LEFT * 0.82 + DOWN * 0.28,
            buff=0,
            stroke_width=4,
            color=TEXT_SECONDARY,
            max_tip_length_to_length_ratio=0.20
        )

        horizontal_right = Arrow(
            start=p_pos + DOWN * 0.28,
            end=p_pos + RIGHT * 0.82 + DOWN * 0.28,
            buff=0,
            stroke_width=4,
            color=TEXT_SECONDARY,
            max_tip_length_to_length_ratio=0.20
        )

        self.play(
            GrowArrow(horizontal_left),
            GrowArrow(horizontal_right),
            run_time=0.7
        )

        self.wait(0.9)

        cancel_cross = Cross(
            VGroup(
                horizontal_left,
                horizontal_right
            ),
            stroke_width=4,
            color="#F85149"
        ).scale(0.75)

        self.play(
            Create(cancel_cross),
            run_time=0.6
        )

        self.wait(0.8)

        vertical_text = arabic_text(
            "بينما تتضافر الأجزاء المتجهة إلى أعلى",
            size=29,
            weight=BOLD,
            color=FIELD_COLOR
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeOut(horizontal_text),
            FadeOut(horizontal_left),
            FadeOut(horizontal_right),
            FadeOut(cancel_cross),
            FadeIn(vertical_text),
            run_time=0.7
        )

        self.play(
            Indicate(
                net_arrow,
                color=FIELD_COLOR,
                scale_factor=1.06
            ),
            run_time=0.9
        )

        self.wait(1.2)

        # ====================================================
        # PART 9 — GENERAL PRINCIPLE
        # ====================================================

        self.play(
            FadeOut(vertical_text),
            FadeOut(guide_1),
            FadeOut(guide_2),
            run_time=0.5
        )

        principle_title = arabic_text(
            "وهذا هو مبدأ التراكب",
            size=35,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            DOWN,
            buff=0.30
        )

        self.play(
            FadeIn(principle_title),
            run_time=0.8
        )

        self.wait(1.1)

        # ====================================================
        # GENERALIZE WITH EXTRA SOURCE
        # ====================================================

        q3_pos = np.array([
            0,
            -2.55,
            0
        ])

        q3 = make_charge(
            q3_pos,
            "+"
        )

        q3_label = MathTex(
            "Q_3",
            font_size=36,
            color=POSITIVE
        ).next_to(
            q3,
            DOWN,
            buff=0.12
        )

        self.play(
            FadeIn(
                q3,
                scale=0.8
            ),
            FadeIn(q3_label),
            run_time=0.7
        )

        self.wait(0.5)

        e3_direction = unit_vector(
            p_pos - q3_pos
        )

        e3_end = (
            p_pos
            + e3_direction * 1.15
        )

        e3_arrow = Arrow(
            start=p_pos,
            end=e3_end,
            buff=0,
            stroke_width=5,
            color=TEXT_SECONDARY,
            max_tip_length_to_length_ratio=0.17
        )

        e3_label = MathTex(
            r"\vec{E}_3",
            font_size=40,
            color=TEXT_SECONDARY
        ).next_to(
            e3_arrow,
            LEFT,
            buff=0.10
        )

        self.play(
            GrowArrow(e3_arrow),
            FadeIn(e3_label),
            run_time=0.7
        )

        self.wait(0.8)

        many_equation = MathTex(
            r"\vec{E}_{\mathrm{net}}"
            r"="
            r"\vec{E}_1"
            r"+"
            r"\vec{E}_2"
            r"+"
            r"\vec{E}_3"
            r"+\cdots",
            font_size=48
        ).to_edge(
            DOWN,
            buff=0.25
        )

        many_equation.set_color_by_tex(
            r"\vec{E}_{\mathrm{net}}",
            FIELD_COLOR
        )

        self.play(
            FadeOut(principle_title),
            FadeIn(many_equation),
            run_time=0.8
        )

        self.wait(1.4)

        final_text = arabic_text(
            "نحسب مجال كل شحنة، ثم نجمع المتجهات",
            size=31,
            weight=BOLD,
            color=ACCENT
        ).to_edge(
            UP,
            buff=0.45
        )

        self.play(
            FadeOut(title),
            FadeIn(final_text),
            run_time=0.7
        )

        self.wait(1.7)

        # ====================================================
        # END
        # ====================================================

        self.play(
            FadeOut(
                VGroup(
                    final_text,
                    q1,
                    q2,
                    q3,
                    q1_label,
                    q2_label,
                    q3_label,
                    point_p,
                    p_label,
                    e1_arrow,
                    e2_arrow,
                    e3_arrow,
                    e1_label,
                    e2_label,
                    e3_label,
                    net_arrow,
                    net_label,
                    many_equation
                )
            ),
            run_time=0.9
        )


# ============================================================
# DIRECT RENDERING FROM PYCHARM
# ============================================================

if __name__ == "__main__":

    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    config.output_file = "scene_22_superposition"

    config.preview = True
    config.quality = "high_quality"

    Scene22Superposition().render()