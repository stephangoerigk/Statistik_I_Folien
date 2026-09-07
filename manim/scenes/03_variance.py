import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, GRAY, styled_number_line


class Varianz(StatScene):
    def construct(self):
        data = [2, 3, 4, 6, 10]
        n = len(data)
        mean_value = sum(data) / n
        deviations = [v - mean_value for v in data]
        squares = [d ** 2 for d in deviations]
        variance = sum(squares) / (n - 1)
        sd = variance ** 0.5

        title = self.title("Varianz & Standardabweichung")
        self.play(Write(title))

        intro1 = Text("Streuung = Unterschiedlichkeit der Werte", font_size=28, color=MAROON).next_to(title, DOWN, buff=0.5)
        intro2 = Text("Definiert über quadrierte Abstände der Punkte vom Mittelwert (x̄)", font_size=26, color=INK).next_to(intro1, DOWN, buff=0.3)
        self.play(FadeIn(intro1, shift=UP * 0.2))
        self.wait(0.8)
        self.play(FadeIn(intro2, shift=UP * 0.2))
        self.wait(1.2)
        self.play(FadeOut(intro1), FadeOut(intro2))

        general = MathTex(
            r"s^2", "=", r"\frac{", r"\sum_{i=1}^{n}(x_i-\bar{x})^2", "}{", "n-1", "}",
            color=INK,
        ).scale(1.1)
        general[0].set_color(MAROON)
        self.play(Write(general))
        self.wait(1)
        self.play(general.animate.to_edge(UP).shift(DOWN * 0.9))

        number_line = styled_number_line([0, 12, 1], include_numbers=False).shift(DOWN * 2.0)
        self.play(Create(number_line))

        mean_x = number_line.n2p(mean_value)[0]
        mean_line = DashedLine(
            [mean_x, number_line.get_bottom()[1] - 0.3, 0],
            [mean_x, number_line.get_top()[1] + 1.6, 0],
            color=MAGENTA,
        )
        mean_tag = MathTex(r"\bar{x} = " + f"{mean_value:.0f}", color=MAGENTA, font_size=30).next_to(mean_line, UP, buff=0.1)
        self.play(Create(mean_line), Write(mean_tag))

        dots = VGroup()
        val_labels = VGroup()
        for value in data:
            point = number_line.n2p(value) + UP * 0.4
            dot = Dot(point, color=MAROON, radius=0.11)
            label = MathTex(str(value), font_size=26, color=INK).next_to(number_line.n2p(value), DOWN, buff=0.2)
            dots.add(dot)
            val_labels.add(label)

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15),
            LaggedStart(*[FadeIn(l) for l in val_labels], lag_ratio=0.15),
        )
        self.wait(0.3)

        # deviation arrows from mean to each point, vertikal gestaffelt nach |Abstand|
        neg_side = sorted([i for i, d in enumerate(deviations) if d < 0], key=lambda i: abs(deviations[i]))
        pos_side = sorted([i for i, d in enumerate(deviations) if d > 0], key=lambda i: abs(deviations[i]))

        tier_of = {}
        for tier, i in enumerate(neg_side):
            tier_of[i] = tier
        for tier, i in enumerate(pos_side):
            tier_of[i] = tier

        arrows = VGroup()
        dev_labels = VGroup()
        base_y = number_line.get_center()[1] + 0.65
        for i, (value, dot, dev) in enumerate(zip(data, dots, deviations)):
            y = base_y + tier_of[i] * 0.55
            start = np.array([mean_x, y, 0])
            end = np.array([dot.get_center()[0], y, 0])
            arrow = Arrow(start, end, buff=0, color=GRAY, stroke_width=3, tip_length=0.15)
            label = MathTex(f"{dev:+.0f}", font_size=24, color=GRAY).next_to(arrow, UP, buff=0.08)
            arrows.add(arrow)
            dev_labels.add(label)

        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
            LaggedStart(*[FadeIn(l) for l in dev_labels], lag_ratio=0.15),
        )
        self.wait(0.5)

        # deviations become squared deviations: erst "hoch 2" dazu, dann Ergebnis
        power_labels = VGroup()
        for dev, label in zip(deviations, dev_labels):
            p = MathTex(f"({dev:+.0f})^2", font_size=20, color=GRAY).move_to(label)
            power_labels.add(p)

        self.play(
            *[Transform(dl, p) for dl, p in zip(dev_labels, power_labels)],
            FadeOut(arrows),
        )
        self.wait(0.6)

        squared_labels = VGroup()
        for dev, label in zip(squares, dev_labels):
            sq = MathTex(f"{dev:.0f}", font_size=26, color=MAROON).move_to(label)
            squared_labels.add(sq)

        self.play(*[Transform(dl, sq) for dl, sq in zip(dev_labels, squared_labels)])
        self.wait(0.5)

        sum_str = "+".join(f"{s:.0f}" for s in squares)
        specific = MathTex(
            r"s^2", "=", r"\frac{", sum_str, "}{", str(n - 1), "}", "=", f"{variance:.0f}",
            color=INK,
        ).scale(1.1)
        specific[0].set_color(MAROON)
        specific[-1].set_color(MAGENTA)
        specific.move_to(general)

        self.play(TransformMatchingTex(general, specific))
        self.wait(0.7)

        sd_formula = MathTex(
            "s", "=", r"\sqrt{" + f"{variance:.0f}" + "}", "=", f"{sd:.2f}",
            color=INK,
        ).scale(1.1).next_to(specific, DOWN, buff=0.25)
        sd_formula[0].set_color(MAROON)
        sd_formula[-1].set_color(MAGENTA)
        self.play(Write(sd_formula))
        self.play(Indicate(specific[-1], color=MAGENTA), Indicate(sd_formula[-1], color=MAGENTA))
        self.wait(1.5)

        # ---------- Dynamische Streuungs-Demo ----------
        self.play(FadeOut(dev_labels), FadeOut(dots), FadeOut(val_labels), FadeOut(specific), FadeOut(sd_formula))

        spread_tracker = ValueTracker(1.0)

        s2_tag = MathTex("s^2", "=", color=INK).scale(1.1)
        s2_tag[0].set_color(MAROON)
        s2_val = DecimalNumber(variance, num_decimal_places=2, color=MAGENTA, font_size=34)
        s_tag = MathTex("s", "=", color=INK).scale(1.1)
        s_tag[0].set_color(MAROON)
        s_val = DecimalNumber(sd, num_decimal_places=2, color=MAGENTA, font_size=34)
        dyn_formula = VGroup(s2_tag, s2_val, s_tag, s_val).arrange(RIGHT, buff=0.2)
        dyn_formula.move_to(general)

        def update_s2(m):
            d = spread_tracker.get_value()
            m.set_value(d ** 2 * variance)

        def update_s(m):
            d = spread_tracker.get_value()
            m.set_value(abs(d) * sd)

        s2_val.add_updater(update_s2)
        s_val.add_updater(update_s)

        def make_dyn_dots():
            d = spread_tracker.get_value()
            group = VGroup()
            for dev in deviations:
                val = mean_value + d * dev
                point = number_line.n2p(val) + UP * 0.4
                group.add(Dot(point, color=MAROON, radius=0.11))
            return group

        dyn_dots = always_redraw(make_dyn_dots)

        self.play(Write(dyn_formula))
        self.add(dyn_dots)
        self.wait(0.5)

        high_label = Text("Hohe Streuung", font_size=22, color=INK).next_to(number_line, DOWN, buff=1.3)
        self.play(FadeIn(high_label, shift=UP * 0.2))
        self.play(spread_tracker.animate.set_value(1.3), run_time=3)
        self.wait(1)

        low_label = Text("Geringe Streuung", font_size=22, color=INK).move_to(high_label)
        self.play(Transform(high_label, low_label))
        self.play(spread_tracker.animate.set_value(0.4), run_time=3)
        self.wait(1)

        zero_label = Text("Keine Streuung: alle Werte = Mittelwert", font_size=22, color=MAGENTA).move_to(high_label)
        self.play(Transform(high_label, zero_label))
        self.play(spread_tracker.animate.set_value(0.0), run_time=3)
        self.wait(2)
