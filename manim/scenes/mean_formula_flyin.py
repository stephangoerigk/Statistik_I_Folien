from manim import *


class MeanFormulaFlyIn(Scene):
    def construct(self):
        data = [2, 3, 4, 6, 10]
        n = len(data)
        mean_value = sum(data) / n

        title = Text("Der Mittelwert: von der allgemeinen Formel zu den Daten", font_size=30).to_edge(UP)
        self.play(Write(title))

        # 1. General formula, centered
        general = MathTex(
            r"\bar{x}", "=", r"\frac{", r"x_1+x_2+\cdots+x_n", "}{", "n", "}"
        ).scale(1.2)
        self.play(Write(general))
        self.wait(1)

        # 2. Skeleton with placeholders for the actual data count, still centered
        skeleton = MathTex(
            r"\bar{x}", "=", r"\frac{",
            "?", "+", "?", "+", "?", "+", "?", "+", "?",
            "}{", str(n), "}",
        ).scale(1.2)
        skeleton.move_to(general)

        self.play(
            ReplacementTransform(general[2], skeleton[2]),
            FadeOut(general[3], shift=UP * 0.3),
            LaggedStart(*[FadeIn(skeleton[i], shift=UP * 0.2) for i in range(3, 12)], lag_ratio=0.1),
            ReplacementTransform(general[4], skeleton[12]),
            ReplacementTransform(general[5], skeleton[13]),
            ReplacementTransform(general[6], skeleton[14]),
        )
        self.wait(0.5)

        # 3. Move formula up, bring in the number line with data points below
        self.play(skeleton.animate.to_edge(UP).shift(DOWN * 0.9))

        number_line = NumberLine(
            x_range=[0, 12, 1],
            length=10,
            include_numbers=True,
            font_size=24,
        ).shift(DOWN * 1.8)
        self.play(Create(number_line))

        dots = VGroup()
        labels = VGroup()
        stack_offsets = {}
        for value in data:
            offset = stack_offsets.get(value, 0)
            stack_offsets[value] = offset + 1
            point = number_line.n2p(value) + UP * (0.4 + 0.5 * offset)
            dot = Dot(point, color=BLUE, radius=0.12)
            label = MathTex(str(value), font_size=32).next_to(dot, UP, buff=0.15)
            dots.add(dot)
            labels.add(label)

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2),
            LaggedStart(*[FadeIn(l, shift=DOWN * 0.2) for l in labels], lag_ratio=0.2),
        )
        self.wait(0.5)

        # 4. The numbers fly from the number line up into the formula's placeholders
        placeholder_indices = [3, 5, 7, 9, 11]
        flights = []
        for value, label, dot, ph_index in zip(data, labels, dots, placeholder_indices):
            placeholder = skeleton[ph_index]
            target = MathTex(str(value), font_size=32, color=YELLOW).move_to(placeholder.get_center())
            flights.append(
                AnimationGroup(
                    ReplacementTransform(label, target),
                    FadeOut(placeholder),
                    FadeOut(dot, scale=0.3),
                )
            )
        self.play(LaggedStart(*flights, lag_ratio=0.15), run_time=3)
        self.wait(0.5)

        # 5. Show the result
        result = MathTex("=", f"{mean_value:.1f}", font_size=48, color=YELLOW).next_to(skeleton, RIGHT, buff=0.3)
        self.play(Write(result))
        self.wait(1.5)
