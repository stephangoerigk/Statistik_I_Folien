from manim import *


class MeanFromData(Scene):
    def construct(self):
        data = [2, 3, 4, 6, 10]
        mean_value = sum(data) / len(data)

        title = Text("Der Mittelwert als Ausgleichspunkt der Daten", font_size=32).to_edge(UP)
        self.play(Write(title))

        number_line = NumberLine(
            x_range=[0, 12, 1],
            length=10,
            include_numbers=True,
            font_size=24,
        ).shift(DOWN * 0.5)
        self.play(Create(number_line))

        # individual data points appear at their positions, stacked so they don't overlap
        dots = VGroup()
        labels = VGroup()
        stack_offsets = {}
        for value in data:
            offset = stack_offsets.get(value, 0)
            stack_offsets[value] = offset + 1
            point = number_line.n2p(value) + UP * (0.4 + 0.5 * offset)
            dot = Dot(point, color=BLUE, radius=0.12)
            label = Text(str(value), font_size=22).next_to(dot, UP, buff=0.1)
            dots.add(dot)
            labels.add(label)

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2),
            LaggedStart(*[FadeIn(l, shift=DOWN * 0.2) for l in labels], lag_ratio=0.2),
        )
        self.wait(0.5)

        # show the formula building up from the same values
        sum_str = " + ".join(str(v) for v in data)
        formula = MathTex(
            r"\bar{x} = \frac{" + sum_str + r"}{" + str(len(data)) + r"} = " + f"{mean_value:.1f}"
        ).next_to(number_line, DOWN, buff=1.2)

        self.play(FadeIn(formula, shift=UP * 0.3))
        self.wait(0.5)

        # data points migrate and merge into the mean
        mean_point = number_line.n2p(mean_value) + UP * 0.4
        self.play(
            *[dot.animate.move_to(mean_point) for dot in dots],
            *[FadeOut(l) for l in labels],
            run_time=2,
        )

        mean_dot = Dot(mean_point, color=YELLOW, radius=0.16)
        mean_label = MathTex(r"\bar{x}", color=YELLOW, font_size=32).next_to(mean_dot, UP, buff=0.15)
        marker = Triangle(color=YELLOW, fill_opacity=1).scale(0.15).rotate(PI).next_to(
            number_line.n2p(mean_value), DOWN, buff=0.05
        )

        self.play(FadeOut(dots), FadeIn(mean_dot), FadeIn(marker), Write(mean_label))
        self.wait(1.5)
