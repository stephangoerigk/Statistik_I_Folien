import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, GRAY


def fmt(v):
    return f"{v:.0f}" if float(v).is_integer() else f"{v:.1f}"


def quantile_positions(n, alpha):
    """Rückgabe: (Wert-Berechnungsindizes, ist_gemittelt)."""
    pos = n * alpha
    if pos.is_integer():
        return (int(pos), int(pos) + 1), True
    return (math.ceil(pos),), False


class Quartilabstand(StatScene):
    def construct(self):
        title = self.title("Quartilabstand")
        self.play(Write(title))

        definition = Text(
            "Quartilabstand = Bereich, in dem die mittleren 50% der sortierten Daten liegen",
            font_size=26,
            color=INK,
        ).next_to(title, DOWN, buff=0.5)
        formula = MathTex(
            "q_A", "=", r"\tilde{x}_{0.75} - \tilde{x}_{0.25}", color=INK,
        ).scale(1.1).next_to(definition, DOWN, buff=0.5)
        formula[0].set_color(MAGENTA)

        self.play(FadeIn(definition, shift=UP * 0.2))
        self.play(Write(formula))
        self.wait(1)
        self.play(FadeOut(definition), FadeOut(formula))

        subtitle_a = Text("n · α ergibt keine ganze Zahl (n = 9)", font_size=25, color=MAROON).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle_a, shift=UP * 0.2))
        self.animate_iqr_case([8, 3, 12, 5, 9, 2, 11, 6, 7], subtitle_a)

        subtitle_b = Text("n · α ergibt eine ganze Zahl (n = 8)", font_size=25, color=MAROON).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle_b, shift=UP * 0.2))
        self.animate_iqr_case([8, 3, 12, 5, 9, 2, 11, 6], subtitle_b)

    def animate_iqr_case(self, raw_order, subtitle):
        sorted_data = sorted(raw_order)
        n = len(sorted_data)

        tile_width = 1.0
        start_x = -tile_width * (n - 1) / 2
        tiles = VGroup()
        for i, value in enumerate(raw_order):
            box = Square(side_length=0.75, color=INK).set_fill(WHITE, opacity=1)
            label = MathTex(str(value), font_size=28, color=INK)
            tile = VGroup(box, label)
            tile.move_to(RIGHT * (start_x + i * tile_width) + UP * 0.6)
            tiles.add(tile)

        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in tiles], lag_ratio=0.1))
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
            animations.append(tile.animate.move_to(RIGHT * target_x + UP * 0.6))
        self.play(*animations, run_time=1.8)
        self.wait(0.3)

        def tile_at(rank):  # rank: 1-indexiert
            x = start_x + (rank - 1) * tile_width
            return min(tiles, key=lambda t: abs(t.get_center()[0] - x))

        q1_idx, q1_avg = quantile_positions(n, 0.25)
        q3_idx, q3_avg = quantile_positions(n, 0.75)

        q1_tiles = VGroup(*[tile_at(r) for r in q1_idx])
        q3_tiles = VGroup(*[tile_at(r) for r in q3_idx])
        q1_value = sum(sorted_data[r - 1] for r in q1_idx) / len(q1_idx)
        q3_value = sum(sorted_data[r - 1] for r in q3_idx) / len(q3_idx)
        iqr_value = q3_value - q1_value

        span = Rectangle(
            width=q3_tiles.get_right()[0] - q1_tiles.get_left()[0] + 0.3,
            height=1.0,
            color=MAGENTA,
            fill_color=MAGENTA,
            fill_opacity=0.10,
            stroke_width=0,
        ).move_to(VGroup(q1_tiles, q3_tiles).get_center())
        self.play(FadeIn(span))

        self.play(
            *[t[0].animate.set_stroke(MAROON, width=3) for t in q1_tiles],
            *[t[1].animate.set_color(MAROON) for t in q1_tiles],
            *[t[0].animate.set_stroke(MAGENTA, width=3) for t in q3_tiles],
            *[t[1].animate.set_color(MAGENTA) for t in q3_tiles],
        )

        brace_q1 = Brace(q1_tiles, DOWN, color=MAROON)
        label_q1 = brace_q1.get_tex("Q_1").set_color(MAROON)
        brace_q3 = Brace(q3_tiles, DOWN, color=MAGENTA)
        label_q3 = brace_q3.get_tex("Q_3").set_color(MAGENTA)
        self.play(GrowFromCenter(brace_q1), Write(label_q1), GrowFromCenter(brace_q3), Write(label_q3))
        self.wait(0.5)

        if q1_avg:
            q1_formula = MathTex(
                "q_{0.25}", "=", r"\frac{x_{(" + str(q1_idx[0]) + r")} + x_{(" + str(q1_idx[1]) + r")}}{2}",
                "=", fmt(q1_value), color=MAROON,
            )
        else:
            q1_formula = MathTex(
                "q_{0.25}", "=", "x_{(" + str(q1_idx[0]) + ")}", "=", fmt(q1_value), color=MAROON,
            )

        if q3_avg:
            q3_formula = MathTex(
                "q_{0.75}", "=", r"\frac{x_{(" + str(q3_idx[0]) + r")} + x_{(" + str(q3_idx[1]) + r")}}{2}",
                "=", fmt(q3_value), color=MAGENTA,
            )
        else:
            q3_formula = MathTex(
                "q_{0.75}", "=", "x_{(" + str(q3_idx[0]) + ")}", "=", fmt(q3_value), color=MAGENTA,
            )

        q1_formula.scale(0.85)
        q3_formula.scale(0.85)
        result = VGroup(q1_formula, q3_formula).arrange(RIGHT, buff=1.0).next_to(tiles, DOWN, buff=1.6)
        self.play(Write(q1_formula), Write(q3_formula))
        self.wait(0.5)

        qa_formula = MathTex(
            "q_A", "=", "q_{0.75} - q_{0.25}", "=",
            f"{fmt(q3_value)} - {fmt(q1_value)}", "=", fmt(iqr_value),
            color=INK,
        ).scale(0.95).next_to(result, DOWN, buff=0.5)
        qa_formula[0].set_color(INK)
        qa_formula[-1].set_color(MAGENTA)
        self.play(Write(qa_formula))
        self.play(Indicate(qa_formula[-1], color=MAGENTA))
        self.wait(1.5)

        self.play(
            FadeOut(tiles), FadeOut(span), FadeOut(brace_q1), FadeOut(label_q1),
            FadeOut(brace_q3), FadeOut(label_q3), FadeOut(q1_formula), FadeOut(q3_formula),
            FadeOut(qa_formula), FadeOut(subtitle),
        )
