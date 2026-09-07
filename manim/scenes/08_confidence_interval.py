import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, GRAY, styled_number_line


class Konfidenzintervall(StatScene):
    def construct(self):
        x_bar = 100.0
        se = 2.0
        z = 1.96
        margin = z * se
        lower, upper = x_bar - margin, x_bar + margin

        title = self.title("Konfidenzintervall")
        self.play(Write(title))

        number_line = styled_number_line([90, 110, 2], length=10).shift(UP * 0.8)
        self.play(Create(number_line))

        point = Dot(number_line.n2p(x_bar), color=MAROON, radius=0.12)
        point_label = MathTex(r"\bar{x} = 100", color=MAROON, font_size=28).next_to(point, UP, buff=0.2)
        self.play(GrowFromCenter(point), Write(point_label))
        self.wait(0.5)

        formula = MathTex(
            "CI", "=", r"\bar{x} \pm z \cdot SE", "=", "100 \\pm 1{,}96 \\cdot 2", "=",
            f"[{lower:.1f}; {upper:.1f}]",
            color=INK,
        ).scale(0.85).next_to(number_line, DOWN, buff=1.6)
        formula[0].set_color(MAROON)
        formula[-1].set_color(MAGENTA)
        self.play(Write(formula))
        self.wait(0.5)

        bracket = Line(number_line.n2p(lower), number_line.n2p(upper), color=MAGENTA, stroke_width=6)
        tick_l = Line(number_line.n2p(lower) + UP * 0.1, number_line.n2p(lower) + DOWN * 0.1, color=MAGENTA, stroke_width=4)
        tick_u = Line(number_line.n2p(upper) + UP * 0.1, number_line.n2p(upper) + DOWN * 0.1, color=MAGENTA, stroke_width=4)
        self.play(GrowFromCenter(bracket), Create(tick_l), Create(tick_u))
        self.wait(0.7)

        self.play(FadeOut(formula))
        self.play(
            VGroup(number_line, point, point_label, bracket, tick_l, tick_u).animate.shift(UP * 1.3)
        )

        subtitle = Text(
            "Was heißt „95% Konfidenzintervall“? Wiederholte Stichproben:",
            font_size=24, color=INK,
        ).next_to(number_line, DOWN, buff=1.4).shift(UP*1.3)
        self.play(FadeIn(subtitle, shift=UP * 0.2))

        true_mu = 99.3
        mu_line = DashedLine(
            number_line.n2p(true_mu) + DOWN * 0.2,
            number_line.n2p(true_mu) + DOWN * 3.6,
            color=INK,
        )
        mu_label = MathTex(r"\mu", color=INK, font_size=26).next_to(mu_line, DOWN, buff=0.1)
        self.play(Create(mu_line), Write(mu_label))

        sample_offsets = [1.1, -0.6, 0.3, -1.4, 0.8, -0.2, 2.1, -0.9, 0.5, -0.4]
        rows = VGroup()
        for i, off in enumerate(sample_offsets):
            center = x_bar + off
            lo, hi = center - margin, center + margin
            contains = lo <= true_mu <= hi
            color = GRAY if contains else MAGENTA
            y = DOWN * (0.6 + 0.28 * i)
            seg = Line(
                number_line.n2p(lo) + y, number_line.n2p(hi) + y,
                color=color, stroke_width=3,
            )
            dot = Dot(number_line.n2p(center) + y, color=color, radius=0.045)
            rows.add(VGroup(seg, dot))

        self.play(LaggedStart(*[Create(r) for r in rows], lag_ratio=0.1), run_time=2.5)
        self.wait(1)

        note = Text(
            "≈ 95% der so gebauten Intervalle enthalten den wahren Wert μ",
            font_size=22, color=MAGENTA,
        ).next_to(rows, DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2)
