import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, GRAY, styled_number_line

# feste, exakt unkorrelierte Basismuster (corr = 0, je Mittelwert = 0, SD = 1)
# Z_STD ist eine Permutation derselben Quantile wie X_STD (Gram-Schmidt-korrigiert
# auf exakt 0 Korrelation) -- dadurch keine Ausreißer, die bei hohem |r| noch
# sichtbar aus der Geraden herausstechen würden.
X_STD = np.array([-1.7484, -1.1615, -0.8201, -0.5538, -0.3217, -0.1056,
                   0.1056, 0.3217, 0.5538, 0.8201, 1.1615, 1.7484])
Z_STD = np.array([1.1042, -1.1661, -0.7466, -1.1718, 1.1332, 0.8579,
                   0.1673, -1.1332, 0.1466, 0.7466, 1.1661, -1.1042])
N = len(X_STD)


def y_for_r(r):
    return r * X_STD + np.sqrt(max(1 - r ** 2, 0)) * Z_STD


def pin_marker(axis, x, color, scale=0.13):
    tri = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(scale).rotate(PI)
    tri.move_to(axis.n2p(x) + UP * scale)
    return tri


class Korrelation(StatScene):
    def construct(self):
        title = self.title("Korrelation")
        self.play(Write(title))

        purpose = Text(
            "Nutzen: Stärke und Richtung eines linearen Zusammenhangs messen",
            font_size=24, color=MAROON,
        ).move_to([0, 3.0, 0])
        self.play(FadeIn(purpose, shift=UP * 0.2))
        self.wait(1.3)
        self.play(FadeOut(purpose))

        # ---------- Formel ----------
        formula = MathTex(
            "r", "=", r"\frac{", "cov_{x,y}", "}{", r"s_x \cdot s_y", "}",
            color=INK,
        ).scale(1.1).move_to([0, 2.3, 0])
        formula[0].set_color(MAGENTA)
        self.play(Write(formula))
        self.wait(1)

        # ---------- gemeinsame Achse (bleibt für das ganze Video) ----------
        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=6.5, y_length=4.0,
            axis_config={"include_tip": False, "color": INK},
        ).move_to([0, -1.0, 0])
        x_lab = Text("X", font_size=20, color=INK).next_to(axes, DOWN, buff=0.3)
        y_lab = Text("Y", font_size=20, color=INK).next_to(axes.y_axis.get_top(), RIGHT, buff=0.15)
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab))

        r0 = 0.7
        y0 = y_for_r(r0)
        dots = VGroup(*[Dot(axes.c2p(x, y), color=MAROON, radius=0.08) for x, y in zip(X_STD, y0)])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08))
        self.wait(0.3)

        info_pos = [0, 1.5, 0]
        info = Text("x̄ = 0, ȳ = 0 (Ursprung)", font_size=18, color=INK).move_to(info_pos)
        self.play(FadeIn(info, shift=DOWN * 0.1))
        self.wait(0.6)

        # ---------- Kovarianz visualisieren ----------
        self.play(Indicate(formula[3], color=MAROON, scale_factor=1.3))
        origin = axes.c2p(0, 0)
        rects = VGroup()
        for x, y in zip(X_STD, y0):
            corner = axes.c2p(x, y)
            prod = x * y
            rect = Polygon(
                origin, np.array([corner[0], origin[1], 0]), corner, np.array([origin[0], corner[1], 0]),
                color=MAROON if prod >= 0 else GRAY, fill_opacity=0.3, stroke_width=1,
            )
            rects.add(rect)
        self.play(LaggedStart(*[FadeIn(r) for r in rects], lag_ratio=0.06), run_time=2)
        self.wait(0.5)

        xbar, ybar = X_STD.mean(), y0.mean()
        cov = float(np.sum((X_STD - xbar) * (y0 - ybar)) / (N - 1))
        cov_note = Text(f"cov_x,y ≈ {cov:.2f}  (mittlere Rechteckfläche, vorzeichenbehaftet)", font_size=18, color=MAROON).move_to(info_pos)
        self.play(FadeOut(info), FadeIn(cov_note, shift=UP * 0.1))
        info = cov_note
        self.wait(1.3)
        self.play(FadeOut(rects), FadeOut(info))

        # ---------- Streuung (SD) visualisieren ----------
        self.play(Indicate(formula[5], color=MAGENTA, scale_factor=1.3))
        sx = float(np.sqrt(np.sum((X_STD - xbar) ** 2) / (N - 1)))
        sy = float(np.sqrt(np.sum((y0 - ybar) ** 2) / (N - 1)))

        sx_band = Rectangle(
            width=axes.x_axis.unit_size * 2 * sx, height=axes.y_length,
            color=MAGENTA, fill_color=MAGENTA, fill_opacity=0.12, stroke_width=0,
        ).move_to(axes.c2p(0, 0))
        sy_band = Rectangle(
            width=axes.x_length, height=axes.y_axis.unit_size * 2 * sy,
            color=MAGENTA, fill_color=MAGENTA, fill_opacity=0.12, stroke_width=0,
        ).move_to(axes.c2p(0, 0))
        sx_line_l = DashedLine(axes.c2p(-sx, -2.5), axes.c2p(-sx, 2.5), color=MAGENTA, stroke_width=1.5)
        sx_line_r = DashedLine(axes.c2p(sx, -2.5), axes.c2p(sx, 2.5), color=MAGENTA, stroke_width=1.5)
        sy_line_b = DashedLine(axes.c2p(-2.5, -sy), axes.c2p(2.5, -sy), color=MAGENTA, stroke_width=1.5)
        sy_line_t = DashedLine(axes.c2p(-2.5, sy), axes.c2p(2.5, sy), color=MAGENTA, stroke_width=1.5)
        sx_tag = MathTex("s_x", color=MAGENTA, font_size=28).next_to(axes.c2p(sx, -2.5), DOWN, buff=0.15)
        sy_tag = MathTex("s_y", color=MAGENTA, font_size=28).next_to(axes.c2p(2.5, sy), RIGHT, buff=0.15)

        self.play(FadeIn(sx_band), FadeIn(sy_band))
        self.play(Create(sx_line_l), Create(sx_line_r), Create(sy_line_b), Create(sy_line_t))
        self.play(FadeIn(sx_tag), FadeIn(sy_tag))
        sd_note = Text(f"s_x ≈ {sx:.2f}, s_y ≈ {sy:.2f}  (Streuung je Variable)", font_size=18, color=MAGENTA).move_to(info_pos)
        self.play(FadeIn(sd_note, shift=UP * 0.1))
        info = sd_note
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            sx_band, sy_band, sx_line_l, sx_line_r, sy_line_b, sy_line_t, sx_tag, sy_tag, info,
        )))

        r_result = MathTex(f"r = {r0:.2f}", color=MAGENTA, font_size=26).move_to(info_pos)
        self.play(Indicate(formula[0], color=MAGENTA, scale_factor=1.3), FadeIn(r_result))
        self.wait(1.2)
        self.play(FadeOut(r_result))

        # ---------- Formel verschwindet, r-Achse übernimmt als Anzeige ----------
        self.play(FadeOut(formula))

        r_tracker = ValueTracker(r0)
        self.remove(dots)
        dots = always_redraw(lambda: VGroup(*[
            Dot(axes.c2p(x, y), color=MAROON, radius=0.08) for x, y in zip(X_STD, y_for_r(r_tracker.get_value()))
        ]))
        self.add(dots)

        r_axis = styled_number_line([-1, 1, 0.5], length=5, include_numbers=False).move_to([0, 2.35, 0])
        neg_num = Text("-1", font_size=20, color=INK).next_to(r_axis.n2p(-1), DOWN, buff=0.08)
        pos_num = Text("1", font_size=20, color=INK).next_to(r_axis.n2p(1), DOWN, buff=0.08)
        neg_tag = Text("negativ", font_size=15, color=INK).next_to(neg_num, DOWN, buff=0.12)
        pos_tag = Text("positiv", font_size=15, color=INK).next_to(pos_num, DOWN, buff=0.12)
        r_marker = always_redraw(lambda: pin_marker(r_axis, r_tracker.get_value(), MAGENTA))
        r_value_label = always_redraw(
            lambda: MathTex(f"r = {r_tracker.get_value():.2f}", color=MAGENTA, font_size=24)
            .next_to(r_axis.n2p(r_tracker.get_value()), UP, buff=0.25)
        )
        self.play(Create(r_axis), FadeIn(neg_num), FadeIn(pos_num), FadeIn(neg_tag), FadeIn(pos_tag))
        self.add(r_marker, r_value_label)
        self.wait(0.5)

        # ---------- Sequenz 1a: positiver Zusammenhang (Beispiel) ----------
        content1 = Text(
            "Beispiel: Lerndauer und Prüfungspunkte (positiver Zusammenhang)",
            font_size=20, color=MAROON,
        ).move_to([0, 1.55, 0])
        self.play(FadeIn(content1, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(content1))

        # ---------- Sequenz 1b: negativer Zusammenhang ----------
        content2 = Text(
            "Beispiel: Bildschirmzeit vor dem Schlafen und Schlafqualität (negativer Zusammenhang)",
            font_size=20, color=MAROON,
        ).move_to([0, 1.55, 0])
        self.play(FadeIn(content2, shift=UP * 0.2))
        self.play(r_tracker.animate.set_value(-0.8), run_time=2.5)
        self.wait(2)
        self.play(FadeOut(content2))

        # ---------- Sequenz 2: Stärke des Zusammenhangs ----------
        content3 = Text(
            "Stärke des Zusammenhangs: 0 (kein Muster) bis 1 (perfekte Gerade)",
            font_size=20, color=MAROON,
        ).move_to([0, 1.55, 0])
        self.play(FadeIn(content3, shift=UP * 0.2))
        self.play(r_tracker.animate.set_value(0.0), run_time=2)
        self.wait(0.6)
        self.play(r_tracker.animate.set_value(0.4), run_time=2)
        self.wait(0.4)
        self.play(r_tracker.animate.set_value(0.0), run_time=1.5)
        self.wait(0.3)
        self.play(r_tracker.animate.set_value(0.95), run_time=2.5)
        self.wait(2)
