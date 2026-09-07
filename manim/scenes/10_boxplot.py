import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, styled_number_line

BOX_FILL = "#F5E0E8"


def quantile_positions(n, alpha):
    pos = n * alpha
    if pos.is_integer():
        return (int(pos), int(pos) + 1), True
    return (math.ceil(pos),), False


def quantile_value(sorted_data, n, alpha):
    idx, _ = quantile_positions(n, alpha)
    return sum(sorted_data[i - 1] for i in idx) / len(idx)


class Boxplot(StatScene):
    def construct(self):
        data = [5, 7, 8, 8, 9, 10, 10, 11, 12, 13, 25]
        sorted_data = sorted(data)
        n = len(sorted_data)

        q1 = quantile_value(sorted_data, n, 0.25)
        median = quantile_value(sorted_data, n, 0.50)
        q3 = quantile_value(sorted_data, n, 0.75)
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        inliers = [v for v in sorted_data if lower_fence <= v <= upper_fence]
        outliers = [v for v in sorted_data if v < lower_fence or v > upper_fence]
        whisker_min = min(inliers)
        whisker_max = max(inliers)

        title = self.title("Boxplot")
        self.play(Write(title))

        number_line = styled_number_line([0, 27, 3], length=10.5).shift(DOWN * 2.6)
        self.play(Create(number_line))

        base_y = number_line.get_center()[1]
        y = base_y + 1.6
        box_height = 0.9

        # Rohdaten kurz zeigen
        stack = {}
        dots = VGroup()
        for v in data:
            k = stack.get(v, 0)
            stack[v] = k + 1
            point = number_line.n2p(v) + UP * (0.3 + 0.35 * k)
            dots.add(Dot(point, color=MAROON, radius=0.09))

        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08))
        self.wait(0.5)
        self.play(FadeOut(dots))

        # Box (Q1-Q3) + Median
        box = Rectangle(
            width=number_line.n2p(q3)[0] - number_line.n2p(q1)[0],
            height=box_height,
            color=MAROON, fill_color=BOX_FILL, fill_opacity=1, stroke_width=2.5,
        ).move_to([number_line.n2p((q1 + q3) / 2)[0], y, 0])
        median_line = Line(
            [number_line.n2p(median)[0], y - box_height / 2, 0],
            [number_line.n2p(median)[0], y + box_height / 2, 0],
            color=MAGENTA, stroke_width=4,
        )
        self.play(FadeIn(box))
        self.play(Create(median_line))

        def guide(value, text_str, color, tex=False, top=None):
            top = top if top is not None else (y - box_height / 2 - 0.05)
            line = DashedLine(
                [number_line.n2p(value)[0], top, 0],
                [number_line.n2p(value)[0], base_y + 0.1, 0],
                color=color, stroke_width=1.5,
            )
            lab = (MathTex(text_str, color=color, font_size=24) if tex else Text(text_str, color=color, font_size=20))
            lab.next_to(number_line.n2p(value), DOWN, buff=0.3)
            return VGroup(line, lab)

        g_q1 = guide(q1, "Q_1", MAROON, tex=True)
        g_med = guide(median, "Median", MAGENTA)
        g_q3 = guide(q3, "Q_3", MAROON, tex=True)
        self.play(*[Create(g) for g in [g_q1, g_med, g_q3]])
        self.wait(0.3)

        iqr_brace = Brace(box, UP, color=MAROON)
        iqr_label = iqr_brace.get_text("Interquartilsabstand (IQR)").set_color(MAROON).scale(0.6)
        self.play(GrowFromCenter(iqr_brace), Write(iqr_label))
        self.wait(1)
        self.play(FadeOut(iqr_brace), FadeOut(iqr_label), FadeOut(g_q1), FadeOut(g_med), FadeOut(g_q3))

        # --- Wie lang sind die Whisker? ---
        subtitle = Text("Wie weit reichen die Whisker?", font_size=26, color=MAROON).next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(subtitle, shift=UP * 0.2))

        general_fence = MathTex(
            r"\text{Grenze}", "=", "Q_{1/3}", r"\pm", r"1{,}5 \cdot IQR", color=INK,
        ).scale(0.9).next_to(subtitle, DOWN, buff=0.4)
        self.play(Write(general_fence))
        self.wait(1)

        specific_fence_low = MathTex(
            r"\text{untere Grenze}", "=", f"{q1:.0f}", "-", r"1{,}5\cdot", f"{iqr:.0f}", "=", f"{lower_fence:.0f}",
            color=INK,
        ).scale(0.75)
        specific_fence_high = MathTex(
            r"\text{obere Grenze}", "=", f"{q3:.0f}", "+", r"1{,}5\cdot", f"{iqr:.0f}", "=", f"{upper_fence:.0f}",
            color=INK,
        ).scale(0.75)
        specific_fence_low[-1].set_color(MAROON)
        specific_fence_high[-1].set_color(MAROON)
        fences_group = VGroup(specific_fence_low, specific_fence_high).arrange(DOWN, buff=0.25).move_to(general_fence)

        self.play(ReplacementTransform(general_fence, fences_group))
        self.wait(0.7)
        self.play(fences_group.animate.scale(0.8).to_corner(UR))

        g_low = guide(lower_fence, f"{lower_fence:.0f}", MAROON, top=y + box_height / 2 + 0.4)
        g_high = guide(upper_fence, f"{upper_fence:.0f}", MAROON, top=y + box_height / 2 + 0.4)
        self.play(Create(g_low), Create(g_high))
        self.wait(0.5)

        # Rohdaten erneut zeigen: innerhalb vs. außerhalb der Grenze
        dots2 = VGroup()
        for v in data:
            point = number_line.n2p(v) + UP * 0.3
            color = MAROON if lower_fence <= v <= upper_fence else MAGENTA
            dots2.add(Dot(point, color=color, radius=0.09))
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots2], lag_ratio=0.08))
        self.wait(1)

        gap_arrow = DoubleArrow(
            number_line.n2p(whisker_max) + UP * 0.3,
            number_line.n2p(upper_fence) + UP * 0.3,
            color=MAGENTA, buff=0.1, stroke_width=2.5, tip_length=0.15,
        )
        gap_label = Text("hier liegt kein Wert", font_size=18, color=MAGENTA).next_to(gap_arrow, UP, buff=0.1)
        self.play(GrowArrow(gap_arrow), FadeIn(gap_label, shift=DOWN * 0.1))
        self.wait(0.5)

        note = Text(
            "Whisker enden beim letzten Wert INNERHALB der Grenze – nicht an der Grenze selbst!",
            font_size=22, color=MAGENTA,
        ).next_to(number_line, DOWN, buff=1.0)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(1.5)

        self.play(
            FadeOut(dots2), FadeOut(note), FadeOut(g_low), FadeOut(g_high),
            FadeOut(fences_group), FadeOut(subtitle), FadeOut(gap_arrow), FadeOut(gap_label),
        )

        # Whisker + Ausreißer final einzeichnen
        whisker_left = Line([number_line.n2p(whisker_min)[0], y, 0], [number_line.n2p(q1)[0], y, 0], color=MAROON, stroke_width=2.5)
        whisker_right = Line([number_line.n2p(q3)[0], y, 0], [number_line.n2p(whisker_max)[0], y, 0], color=MAROON, stroke_width=2.5)
        cap_left = Line([number_line.n2p(whisker_min)[0], y - 0.25, 0], [number_line.n2p(whisker_min)[0], y + 0.25, 0], color=MAROON, stroke_width=2.5)
        cap_right = Line([number_line.n2p(whisker_max)[0], y - 0.25, 0], [number_line.n2p(whisker_max)[0], y + 0.25, 0], color=MAROON, stroke_width=2.5)
        outlier_dots = VGroup(*[Dot([number_line.n2p(v)[0], y, 0], color=MAGENTA, radius=0.09) for v in outliers])

        self.play(Create(whisker_left), Create(whisker_right), Create(cap_left), Create(cap_right))
        self.play(*[GrowFromCenter(d) for d in outlier_dots])
        self.wait(0.5)

        g_wmin = guide(whisker_min, f"{whisker_min}", MAROON)
        g_wmax = guide(whisker_max, f"{whisker_max}", MAROON)
        outlier_label = Text("Ausreißer", color=MAGENTA, font_size=20).next_to(outlier_dots, UP, buff=0.25)
        self.play(Create(g_wmin), Create(g_wmax), FadeIn(outlier_label, shift=DOWN * 0.2))
        self.wait(1.5)

        range_line = Line([number_line.n2p(min(data))[0], base_y - 0.5, 0], [number_line.n2p(max(data))[0], base_y - 0.5, 0], color=INK, stroke_width=2)
        range_tick_l = Line([number_line.n2p(min(data))[0], base_y - 0.42, 0], [number_line.n2p(min(data))[0], base_y - 0.58, 0], color=INK, stroke_width=2)
        range_tick_r = Line([number_line.n2p(max(data))[0], base_y - 0.42, 0], [number_line.n2p(max(data))[0], base_y - 0.58, 0], color=INK, stroke_width=2)
        range_label = Text("Spannweite (Range)", color=INK, font_size=20).next_to(range_line, DOWN, buff=0.15)
        self.play(Create(range_line), Create(range_tick_l), Create(range_tick_r), Write(range_label))
        self.wait(1.5)

        final_note = Text(
            "Whiskers reichen bis zum letzten verfügbaren Wert",
            font_size=26, color=MAGENTA,
        ).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(final_note, shift=UP * 0.2))
        self.wait(1.5)

        self.play(
            FadeOut(g_wmin), FadeOut(g_wmax), FadeOut(outlier_label),
            FadeOut(range_line), FadeOut(range_tick_l), FadeOut(range_tick_r), FadeOut(range_label),
            FadeOut(final_note),
        )
        self.wait(2)
