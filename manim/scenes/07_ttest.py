import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, GRAY, styled_number_line

DARK_GRAY = "#4A4A4A"


class TTest(StatScene):
    def construct(self):
        group1 = [98, 100, 102, 101, 99]
        group2 = [103, 105, 104, 106, 102]
        n1, n2 = len(group1), len(group2)
        m1, m2 = sum(group1) / n1, sum(group2) / n2
        s1 = (sum((v - m1) ** 2 for v in group1) / (n1 - 1)) ** 0.5
        s2 = (sum((v - m2) ** 2 for v in group2) / (n2 - 1)) ** 0.5
        pooled_var = ((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)
        se = (pooled_var * (1 / n1 + 1 / n2)) ** 0.5
        diff = m2 - m1
        t_value = diff / se

        title = self.title("t-Test für unabhängige Stichproben: die Grundidee")
        self.play(Write(title))

        number_line = styled_number_line([95, 110, 1], length=10).shift(DOWN * 1.0)
        self.play(Create(number_line))

        g1_label = Text("Gruppe 1", font_size=22, color=MAROON).next_to(number_line, UP, buff=1.8).align_to(number_line, LEFT)
        g2_label = Text("Gruppe 2", font_size=22, color=DARK_GRAY).next_to(g1_label, DOWN, buff=1.2)
        self.play(FadeIn(g1_label), FadeIn(g2_label))

        dots1 = VGroup(*[
            Dot(number_line.n2p(v) + UP * (2.6 + 0.3 * i), color=MAROON, radius=0.1)
            for i, v in enumerate(group1)
        ])
        dots2 = VGroup(*[
            Dot(number_line.n2p(v) + UP * (1.2 + 0.3 * i), color=DARK_GRAY, radius=0.1)
            for i, v in enumerate(group2)
        ])
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots1], lag_ratio=0.15),
            LaggedStart(*[GrowFromCenter(d) for d in dots2], lag_ratio=0.15),
        )
        self.wait(0.5)

        mean1_point = number_line.n2p(m1) + UP * 0.4
        mean2_point = number_line.n2p(m2) + UP * 0.4
        self.play(
            *[d.animate.move_to(mean1_point) for d in dots1],
            *[d.animate.move_to(mean2_point) for d in dots2],
            FadeOut(g1_label), FadeOut(g2_label),
            run_time=2,
        )

        marker1 = Triangle(color=MAROON, fill_opacity=1).scale(0.15).rotate(PI).next_to(number_line.n2p(m1), DOWN, buff=0.05)
        marker2 = Triangle(color=DARK_GRAY, fill_opacity=1).scale(0.15).rotate(PI).next_to(number_line.n2p(m2), DOWN, buff=0.05)
        tag1 = MathTex(r"\bar{x}_1", color=MAROON, font_size=28).next_to(mean1_point, UP, buff=0.15)
        tag2 = MathTex(r"\bar{x}_2", color=DARK_GRAY, font_size=28).next_to(mean2_point, UP, buff=0.15)
        self.play(FadeOut(dots1), FadeOut(dots2), FadeIn(marker1), FadeIn(marker2), Write(tag1), Write(tag2))
        self.wait(0.5)

        diff_arrow = DoubleArrow(number_line.n2p(m1), number_line.n2p(m2), color=MAGENTA, buff=0, stroke_width=3).shift(UP * 0.9)
        diff_label = MathTex(f"\\bar{{x}}_2 - \\bar{{x}}_1 = {diff:.0f}", color=MAGENTA, font_size=28).next_to(diff_arrow, UP, buff=0.15)
        self.play(GrowArrow(diff_arrow), Write(diff_label))
        self.wait(0.7)

        se_note = Text(f"Streuung innerhalb der Gruppen → Standardfehler SE = {se:.0f}", font_size=24, color=DARK_GRAY).next_to(number_line, DOWN, buff=0.6)
        self.play(FadeIn(se_note, shift=UP * 0.2))
        self.wait(1)

        formula = MathTex(
            "t", "=", r"\frac{\bar{x}_2 - \bar{x}_1}{SE}", "=", r"\frac{" + f"{diff:.0f}" + "}{" + f"{se:.0f}" + "}", "=", f"{t_value:.1f}",
            color=INK,
        ).scale(1.0).next_to(se_note, DOWN, buff=0.5)
        formula[0].set_color(MAROON)
        formula[-1].set_color(MAGENTA)
        self.play(Write(formula))
        self.play(Indicate(formula[-1], color=MAGENTA))
        self.wait(1.5)
