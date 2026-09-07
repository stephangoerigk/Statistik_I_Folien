import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, styled_number_line


class Mittelwert(StatScene):
    def construct(self):
        data = [2, 3, 4, 6, 10]
        n = len(data)
        mean_value = sum(data) / n

        title = self.title("Mittelwert")
        self.play(Write(title))

        sum_notation = MathTex(
            r"\bar{x}", "=", r"\frac{", r"\sum_{i=1}^{n} x_i", "}{", "n", "}",
            color=INK,
        ).scale(1.2)
        sum_notation[0].set_color(MAROON)
        self.play(Write(sum_notation))
        self.wait(1)

        general = MathTex(
            r"\bar{x}", "=", r"\frac{", r"x_1+x_2+\cdots+x_n", "}{", "n", "}",
            color=INK,
        ).scale(1.2)
        general[0].set_color(MAROON)
        general.move_to(sum_notation)

        self.play(TransformMatchingTex(sum_notation, general))
        self.wait(1)

        self.play(general.animate.to_edge(UP).shift(DOWN * 1.0))

        number_line = styled_number_line([0, 12, 1]).shift(DOWN * 1.5)
        self.play(Create(number_line))

        dots = VGroup()
        labels = VGroup()
        stack_offsets = {}
        for value in data:
            offset = stack_offsets.get(value, 0)
            stack_offsets[value] = offset + 1
            point = number_line.n2p(value) + UP * (0.4 + 0.5 * offset)
            dot = Dot(point, color=MAROON, radius=0.12)
            label = MathTex(str(value), font_size=30, color=INK).next_to(dot, UP, buff=0.15)
            dots.add(dot)
            labels.add(label)

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15),
            LaggedStart(*[FadeIn(l, shift=DOWN * 0.2) for l in labels], lag_ratio=0.15),
        )
        self.wait(0.5)

        sum_str = "+".join(str(v) for v in data)
        specific = MathTex(
            r"\bar{x}", "=", r"\frac{", sum_str, "}{", str(n), "}", "=", f"{mean_value:.1f}",
            color=INK,
        ).scale(1.2)
        specific[0].set_color(MAROON)
        specific[-1].set_color(MAGENTA)
        specific.move_to(general)

        self.play(TransformMatchingTex(general, specific))
        self.wait(0.5)

        mean_point = number_line.n2p(mean_value) + UP * 0.4
        self.play(
            *[dot.animate.move_to(mean_point) for dot in dots],
            *[FadeOut(l) for l in labels],
            run_time=2,
        )

        mean_dot = Dot(mean_point, color=MAGENTA, radius=0.16)
        marker = Triangle(color=MAGENTA, fill_opacity=1).scale(0.15).rotate(PI).next_to(
            number_line.n2p(mean_value), DOWN, buff=0.05
        )
        mean_label = MathTex(r"\bar{x}", color=MAGENTA, font_size=32).next_to(mean_dot, UP, buff=0.15)

        self.play(FadeOut(dots), FadeIn(mean_dot), FadeIn(marker), Write(mean_label))
        self.play(Indicate(specific[-1], color=MAGENTA))
        self.wait(1.5)
