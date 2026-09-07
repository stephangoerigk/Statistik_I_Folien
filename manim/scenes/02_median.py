import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK


def fmt(v):
    return f"{v:.0f}" if float(v).is_integer() else f"{v:.1f}"


class Median(StatScene):
    def construct(self):
        title = self.title("Median")
        self.play(Write(title))

        definition = Text(
            "Median = mittlerer Wert der der Größe nach sortierten Daten",
            font_size=28,
            color=INK,
        ).next_to(title, DOWN, buff=0.6)
        self.play(FadeIn(definition, shift=UP * 0.2))
        self.wait(1)
        self.play(FadeOut(definition))

        subtitle_odd = Text("Ungerade Anzahl an Werten (n = 5)", font_size=26, color=MAROON).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle_odd, shift=UP * 0.2))
        self.animate_median_case([6, 2, 10, 4, 3], subtitle_odd)

        subtitle_even = Text("Gerade Anzahl an Werten (n = 6)", font_size=26, color=MAROON).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle_even, shift=UP * 0.2))
        self.animate_median_case([6, 2, 10, 4, 3, 8], subtitle_even)

    def animate_median_case(self, raw_order, subtitle):
        sorted_data = sorted(raw_order)
        n = len(sorted_data)

        tile_width = 1.3
        start_x = -tile_width * (n - 1) / 2
        tiles = VGroup()
        for i, value in enumerate(raw_order):
            box = Square(side_length=1.0, color=INK).set_fill(WHITE, opacity=1)
            label = MathTex(str(value), font_size=36, color=INK)
            tile = VGroup(box, label)
            tile.move_to(RIGHT * (start_x + i * tile_width) + UP * 0.3)
            tiles.add(tile)

        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in tiles], lag_ratio=0.15))
        self.wait(0.3)

        sorted_positions = {}
        for i, value in enumerate(sorted_data):
            sorted_positions.setdefault(value, []).append(start_x + i * tile_width)

        used = {v: 0 for v in sorted_data}
        animations = []
        for tile, value in zip(tiles, raw_order):
            idx = used[value]
            used[value] += 1
            target_x = sorted_positions[value][idx]
            animations.append(tile.animate.move_to(RIGHT * target_x + UP * 0.3))

        self.play(*animations, run_time=2)
        self.wait(0.3)

        if n % 2 == 1:
            middle_x = start_x + (n // 2) * tile_width
            middle_tile = min(tiles, key=lambda t: abs(t.get_center()[0] - middle_x))
            median_value = sorted_data[n // 2]

            brace = Brace(middle_tile, DOWN, color=MAGENTA)
            median_label = brace.get_text("Median").set_color(MAGENTA)

            self.play(
                middle_tile[0].animate.set_fill(MAGENTA, opacity=0.2).set_stroke(MAGENTA, width=3),
                middle_tile[1].animate.set_color(MAGENTA),
            )
            self.play(GrowFromCenter(brace), Write(median_label))
            self.wait(0.3)

            formula = MathTex(
                r"\tilde{x}", "=", r"x_{(\frac{n+1}{2})}", "=", f"x_{{({n // 2 + 1})}}", "=", fmt(median_value),
                color=INK,
            ).scale(1.0).next_to(tiles, DOWN, buff=1.6)
        else:
            left_idx = n // 2 - 1
            right_idx = n // 2
            left_x = start_x + left_idx * tile_width
            right_x = start_x + right_idx * tile_width
            left_tile = min(tiles, key=lambda t: abs(t.get_center()[0] - left_x))
            right_tile = min(tiles, key=lambda t: abs(t.get_center()[0] - right_x))
            v1, v2 = sorted_data[left_idx], sorted_data[right_idx]
            median_value = (v1 + v2) / 2

            brace = Brace(VGroup(left_tile, right_tile), DOWN, color=MAGENTA)
            median_label = brace.get_text("Median").set_color(MAGENTA)

            self.play(
                left_tile[0].animate.set_fill(MAGENTA, opacity=0.2).set_stroke(MAGENTA, width=3),
                left_tile[1].animate.set_color(MAGENTA),
                right_tile[0].animate.set_fill(MAGENTA, opacity=0.2).set_stroke(MAGENTA, width=3),
                right_tile[1].animate.set_color(MAGENTA),
            )
            self.play(GrowFromCenter(brace), Write(median_label))
            self.wait(0.3)

            formula = MathTex(
                r"\tilde{x}", "=", r"\frac{x_{(\frac{n}{2})}+x_{(\frac{n}{2}+1)}}{2}", "=",
                f"\\frac{{{v1}+{v2}}}{{2}}", "=", fmt(median_value),
                color=INK,
            ).scale(0.9).next_to(tiles, DOWN, buff=1.6)

        formula[0].set_color(MAROON)
        formula[-1].set_color(MAGENTA)
        self.play(Write(formula))
        self.wait(1.5)
        self.play(FadeOut(tiles), FadeOut(brace), FadeOut(median_label), FadeOut(formula), FadeOut(subtitle))
