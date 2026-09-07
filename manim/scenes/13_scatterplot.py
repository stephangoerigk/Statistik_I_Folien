import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK


class Streudiagramm(StatScene):
    def construct(self):
        title = self.title("Streudiagramm")
        self.play(Write(title))

        people = list(range(1, 8))
        schlaf = [4, 5, 6, 6, 7, 8, 10]
        konz = [40, 55, 58, 66, 72, 80, 95]

        purpose = Text(
            "Nutzen: Zusammenhang zwischen zwei Variablen darstellen",
            font_size=24, color=MAROON,
        ).next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(purpose, shift=UP * 0.2))
        self.wait(1)

        table_data = [["Person", "Schlaf (h)", "Konzentration"]]
        for p, s, k in zip(people, schlaf, konz):
            table_data.append([str(p), str(s), str(k)])

        table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"color": INK, "stroke_width": 1.5},
            element_to_mobject=lambda s: Text(s, color=INK, font_size=24),
        ).scale(0.55).next_to(purpose, DOWN, buff=0.5)
        self.play(Create(table))
        self.wait(1.5)

        self.play(table.animate.scale(0.6).to_corner(DL).shift(UP * 0.3))
        self.play(FadeOut(purpose))

        axes = Axes(
            x_range=[0, 12, 2],
            y_range=[0, 100, 20],
            x_length=7.0,
            y_length=4.6,
            axis_config={"include_tip": False, "color": INK},
        ).shift(DOWN * 0.6 + RIGHT * 1.6)
        axes.x_axis.add_numbers(color=INK, font_size=20)
        axes.y_axis.add_numbers(color=INK, font_size=20)

        x_tip_label = Text("X", font_size=22, color=INK).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_tip_label = Text("Y", font_size=22, color=INK).next_to(axes.y_axis.get_end(), UP, buff=0.2)

        x_label = Text("Schlaf (Stunden)", font_size=22, color=INK).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Konzentration", font_size=20, color=INK).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.55)

        wirkrichtung1 = Text("AV = abhängige Variable (Y-Achse)", font_size=16, color=MAROON)
        wirkrichtung2 = Text("UV = unabhängige Variable (X-Achse) – wenn Wirkrichtung angenommen", font_size=16, color=MAROON)
        wirkrichtung = VGroup(wirkrichtung1, wirkrichtung2).arrange(DOWN, buff=0.1).next_to(x_label, DOWN, buff=0.25)

        self.play(Create(axes))
        self.play(FadeIn(x_tip_label), FadeIn(y_tip_label))
        self.play(Write(x_label), Write(y_label))
        self.play(FadeIn(wirkrichtung, shift=UP * 0.1))
        self.wait(1)

        rows = table.get_rows()
        origin = axes.c2p(0, 0)
        dots = []

        for i in range(3):
            start = rows[i + 1].get_center()
            target = axes.c2p(schlaf[i], konz[i])
            dot = Dot(start, color=MAROON, radius=0.09)
            self.add(dot)
            self.play(dot.animate.move_to(target), run_time=0.8)

            guide_x = DashedLine(target, [target[0], origin[1], 0], color=MAROON, stroke_width=1.5)
            guide_y = DashedLine(target, [origin[0], target[1], 0], color=MAROON, stroke_width=1.5)
            self.play(Create(guide_x), Create(guide_y), run_time=0.5)
            self.wait(0.2)
            self.play(FadeOut(guide_x), FadeOut(guide_y))
            dots.append(dot)

        remaining_anims = []
        for i in range(3, len(schlaf)):
            start = rows[i + 1].get_center()
            target = axes.c2p(schlaf[i], konz[i])
            dot = Dot(start, color=MAROON, radius=0.09)
            self.add(dot)
            remaining_anims.append(dot.animate.move_to(target))
            dots.append(dot)
        self.play(LaggedStart(*remaining_anims, lag_ratio=0.15), run_time=2)
        self.wait(1)

        self.play(FadeOut(table), FadeOut(x_tip_label), FadeOut(y_tip_label))

        trend_note = Text("Es können auch statistische Trends dargestellt werden,", font_size=22, color=INK).next_to(title, DOWN, buff=0.4)
        trend_note2 = Text("z.B. ein linearer Zusammenhang → Regressionsgerade", font_size=22, color=INK).next_to(trend_note, DOWN, buff=0.15)
        self.play(FadeIn(trend_note, shift=UP * 0.2), FadeIn(trend_note2, shift=UP * 0.2))
        self.wait(1)

        slope, intercept = np.polyfit(schlaf, konz, 1)
        reg_line = axes.plot(
            lambda x: slope * x + intercept,
            x_range=[min(schlaf) - 0.5, max(schlaf) + 0.5],
            color=MAGENTA, stroke_width=3,
        )
        self.play(Create(reg_line))
        self.wait(2)
