import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, GRAY, styled_number_line


def stats_of(data):
    n = len(data)
    mean = sum(data) / n
    var = sum((v - mean) ** 2 for v in data) / (n - 1)
    sd = var ** 0.5
    z = [(v - mean) / sd for v in data]
    return mean, sd, z


class Standardisierung(StatScene):
    def construct(self):
        data_a = [2, 3, 4, 6, 10]
        data_b = [440, 460, 480, 520, 600]
        mean_a, sd_a, z_a = stats_of(data_a)
        mean_b, sd_b, z_b = stats_of(data_b)
        example_idx = 3  # 6 / 520 -> z = 0.32 für beide

        title = self.title("Standardisierung (z-Werte)")
        self.play(Write(title))

        problem = Text(
            "Wie vergleicht man Werte auf unterschiedlichen Skalen?",
            font_size=26, color=MAROON,
        ).next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(problem, shift=UP * 0.2))
        self.wait(1.3)
        self.play(FadeOut(problem))

        # ---------- Variable A ----------
        label_a = Text("Extraversion (Fragebogen, 0-10)", font_size=22, color=INK).next_to(title, DOWN, buff=0.55)
        line_a = styled_number_line([0, 12, 2], length=6).next_to(label_a, DOWN, buff=1.0).set_x(-2.3)
        self.play(FadeIn(label_a, shift=UP * 0.1), Create(line_a))

        dots_a = VGroup()
        labels_a = VGroup()
        for v in data_a:
            point = line_a.n2p(v) + UP * 0.3
            dots_a.add(Dot(point, color=MAROON, radius=0.09))
            labels_a.add(MathTex(str(v), font_size=22, color=INK).next_to(line_a.n2p(v), DOWN, buff=0.2))
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots_a], lag_ratio=0.12),
            LaggedStart(*[FadeIn(l) for l in labels_a], lag_ratio=0.12),
        )

        mean_a_x = line_a.n2p(mean_a)[0]
        line_a_y = line_a.get_center()[1]
        mline_a = DashedLine([mean_a_x, line_a_y - 0.3, 0], [mean_a_x, line_a_y + 0.75, 0], color=MAGENTA, stroke_width=2)
        mtag_a = MathTex(
            r"\bar{x} = " + f"{mean_a:.0f}" + r",\ s = " + f"{sd_a:.2f}",
            color=MAGENTA, font_size=20,
        ).next_to(mline_a, UP, buff=0.08)
        self.play(Create(mline_a), Write(mtag_a))
        self.wait(0.3)

        # ---------- Variable B ----------
        label_b = Text("Reaktionszeit (ms)", font_size=22, color=INK).next_to(labels_a, DOWN, buff=0.6)
        line_b = styled_number_line([400, 650, 50], length=6).next_to(label_b, DOWN, buff=1.0).set_x(-2.3)
        self.play(FadeIn(label_b, shift=UP * 0.1), Create(line_b))

        dots_b = VGroup()
        labels_b = VGroup()
        for v in data_b:
            point = line_b.n2p(v) + UP * 0.3
            dots_b.add(Dot(point, color=GRAY, radius=0.09))
            labels_b.add(MathTex(str(v), font_size=22, color=INK).next_to(line_b.n2p(v), DOWN, buff=0.2))
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots_b], lag_ratio=0.12),
            LaggedStart(*[FadeIn(l) for l in labels_b], lag_ratio=0.12),
        )

        mean_b_x = line_b.n2p(mean_b)[0]
        line_b_y = line_b.get_center()[1]
        mline_b = DashedLine([mean_b_x, line_b_y - 0.3, 0], [mean_b_x, line_b_y + 0.75, 0], color=MAGENTA, stroke_width=2)
        mtag_b = MathTex(
            r"\bar{x} = " + f"{mean_b:.0f}" + r",\ s = " + f"{sd_b:.2f}",
            color=MAGENTA, font_size=20,
        ).next_to(mline_b, UP, buff=0.08)
        self.play(Create(mline_b), Write(mtag_b))
        self.wait(0.5)

        compare_note = Text(
            "6 vs. 520 ms – unterschiedliche Skalen, nicht direkt vergleichbar",
            font_size=18, color=MAROON,
        )
        compare_note.next_to(labels_b, DOWN, buff=0.35).set_x(0)
        self.play(FadeIn(compare_note, shift=UP * 0.2))
        self.wait(1.0)

        formula = MathTex("z_i", "=", r"\frac{x_i - \bar{x}}{s}", color=INK).scale(0.8)
        formula[0].set_color(MAGENTA)
        formula.next_to(compare_note, DOWN, buff=0.3)
        self.play(Write(formula))
        self.wait(1.0)

        # ---------- Beispielrechnung: beide Variablen simultan, rechts neben der Skala ----------
        calc_a = MathTex(
            "z", "=", r"\frac{" + f"{data_a[example_idx]}-{mean_a:.0f}" + "}{" + f"{sd_a:.2f}" + "}",
            "=", f"{z_a[example_idx]:.2f}", color=INK,
        ).scale(0.75)
        calc_a[0].set_color(MAGENTA)
        calc_a[-1].set_color(MAGENTA)
        calc_a.next_to(line_a, RIGHT, buff=0.7)

        calc_b = MathTex(
            "z", "=", r"\frac{" + f"{data_b[example_idx]}-{mean_b:.0f}" + "}{" + f"{sd_b:.2f}" + "}",
            "=", f"{z_b[example_idx]:.2f}", color=INK,
        ).scale(0.75)
        calc_b[0].set_color(MAGENTA)
        calc_b[-1].set_color(MAGENTA)
        calc_b.next_to(line_b, RIGHT, buff=0.7)

        self.play(
            Indicate(dots_a[example_idx], color=MAGENTA, scale_factor=1.6),
            Indicate(dots_b[example_idx], color=MAGENTA, scale_factor=1.6),
        )
        flying_a = dots_a[example_idx].copy()
        flying_b = dots_b[example_idx].copy()
        self.play(
            flying_a.animate.move_to(calc_a.get_left() + LEFT * 0.15),
            flying_b.animate.move_to(calc_b.get_left() + LEFT * 0.15),
            run_time=0.8,
        )
        self.play(FadeOut(flying_a), FadeOut(flying_b), Write(calc_a), Write(calc_b))
        self.wait(1.0)

        same_z_note = Text("Gleicher z-Wert für beide Variablen!", font_size=18, color=MAGENTA).next_to(
            formula, DOWN, buff=0.3
        )
        self.play(FadeIn(same_z_note, shift=UP * 0.1))
        self.wait(1.5)

        self.play(
            FadeOut(label_a), FadeOut(label_b), FadeOut(mtag_a), FadeOut(mtag_b),
            FadeOut(mline_a), FadeOut(mline_b), FadeOut(labels_a), FadeOut(labels_b),
            FadeOut(line_a), FadeOut(line_b), FadeOut(calc_a), FadeOut(calc_b),
            FadeOut(compare_note), FadeOut(same_z_note), FadeOut(formula),
        )

        # ---------- gemeinsame z-Achse ----------
        z_axis = styled_number_line([-3, 3, 1], length=9).move_to([0, -0.3, 0])
        z_axis_label = Text("Standardwerte z (für beide Variablen)", font_size=22, color=MAGENTA).next_to(z_axis, UP, buff=0.4)
        self.play(Create(z_axis), FadeIn(z_axis_label, shift=UP * 0.1))

        z_dots_a = VGroup(*[Dot(z_axis.n2p(z) + UP * 0.3, color=MAROON, radius=0.09) for z in z_a])
        z_dots_b = VGroup(*[Dot(z_axis.n2p(z) + DOWN * 0.3, color=GRAY, radius=0.09) for z in z_b])

        self.play(
            LaggedStart(*[
                AnimationGroup(ReplacementTransform(d.copy(), zd))
                for d, zd in zip(dots_a, z_dots_a)
            ], lag_ratio=0.15),
            LaggedStart(*[
                AnimationGroup(ReplacementTransform(d.copy(), zd))
                for d, zd in zip(dots_b, z_dots_b)
            ], lag_ratio=0.15),
            FadeOut(dots_a), FadeOut(dots_b),
            run_time=3,
        )
        self.wait(0.3)

        z_value_labels = VGroup(*[
            MathTex(f"{z:.2f}", font_size=20, color=MAGENTA).next_to(z_axis.n2p(z), DOWN, buff=0.65)
            for z in z_a
        ])
        self.play(LaggedStart(*[FadeIn(l) for l in z_value_labels], lag_ratio=0.12))
        self.wait(0.5)

        same_note = Text("Gleiche z-Skala -> jetzt vergleichbar!", font_size=24, color=MAGENTA).next_to(z_value_labels, DOWN, buff=0.5)
        self.play(FadeIn(same_note, shift=UP * 0.2))
        self.wait(1.8)

        self.play(
            FadeOut(z_axis), FadeOut(z_axis_label), FadeOut(z_dots_a), FadeOut(z_dots_b),
            FadeOut(z_value_labels), FadeOut(same_note),
        )

        # ---------- Standardnormalverteilung ----------
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=9,
            y_length=3.0,
            axis_config={"include_tip": False, "color": INK},
        ).move_to([0, 0.55, 0])

        def phi(x):
            return (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x ** 2)

        curve = axes.plot(phi, x_range=[-4, 4], color=MAROON, stroke_width=3)
        curve_label = Text("Standardnormalverteilung N(0,1)", font_size=22, color=INK).next_to(axes, UP, buff=0.55)
        self.play(Create(axes), FadeIn(curve_label))
        self.play(Create(curve))

        explain_note = Text(
            "Die z-Verteilung erlaubt uns,\nAuftretenswahrscheinlichkeiten\nfür Werte abzulesen",
            font_size=16, color=MAROON, line_spacing=0.9,
        ).to_corner(UR, buff=0.3)
        self.play(FadeIn(explain_note, shift=UP * 0.1))

        mu_line = DashedLine(axes.c2p(0, 0), axes.c2p(0, 0.5), color=MAGENTA, stroke_width=2)
        mu_tag = MathTex(r"\mu = 0", color=MAGENTA, font_size=24).next_to(mu_line, UP, buff=0.12)
        self.play(Create(mu_line), Write(mu_tag))

        full_area = axes.get_area(curve, x_range=[-4, 4], color=MAROON, opacity=0.25)
        area_tag = Text("Fläche = 1", font_size=22, color=MAROON).move_to(axes.c2p(-2.4, 0.15))
        self.play(FadeIn(full_area), Write(area_tag))
        self.wait(1.3)
        self.play(FadeOut(full_area), FadeOut(area_tag))

        # ---------- Wahrscheinlichkeit ablesen ----------
        z_mark = 1.0
        mark_line = DashedLine(axes.c2p(z_mark, 0), axes.c2p(z_mark, 0.46), color=GRAY, stroke_width=2)
        mark_tag = MathTex("z = 1{,}00", color=GRAY, font_size=22).next_to(mark_line, UP, buff=0.1)
        self.play(Create(mark_line), Write(mark_tag))

        left_area = axes.get_area(curve, x_range=[-4, z_mark], color=MAGENTA, opacity=0.35)
        self.play(FadeIn(left_area))

        # echte z-Tabellen-Struktur: Zeilen = 1. Nachkommastelle, Spalten = 2. Nachkommastelle
        row_vals = [0.9, 1.0, 1.1]
        col_vals = [0.00, 0.01, 0.02, 0.03]
        grid = [["z"] + [f".{round(c * 100):02d}" for c in col_vals]]
        highlight_row = None
        highlight_col = None
        for ri, r in enumerate(row_vals):
            row = [f"{r:.1f}"]
            for ci, c in enumerate(col_vals):
                z_val = round(r + c, 2)
                row.append(f"{norm.cdf(z_val):.4f}")
                if abs(z_val - z_mark) < 1e-9:
                    highlight_row, highlight_col = ri + 2, ci + 2  # 1-indexiert, +1 für Kopfzeile/-spalte
            grid.append(row)

        table = Table(
            grid,
            include_outer_lines=True,
            line_config={"color": INK, "stroke_width": 1.2},
            element_to_mobject=lambda s: Text(s, color=INK, font_size=17),
        ).scale(0.55).next_to(axes, DOWN, buff=0.35)
        self.play(Create(table))

        highlight_box = SurroundingRectangle(table.get_entries((highlight_row, highlight_col)), color=MAGENTA, buff=0.06)
        self.play(Create(highlight_box))
        self.wait(0.5)

        prob_label = MathTex(
            r"P(Z \leq 1{,}00) = 0{,}841", color=MAGENTA, font_size=24,
        ).next_to(table, RIGHT, buff=0.6)
        self.play(Write(prob_label))
        self.wait(1)

        interpretation = Text(
            "Für z = 1,00:\n84,1% Wahrscheinlichkeit,\ndiesen oder einen kleineren\nWert zu beobachten",
            font_size=16, color=MAGENTA, line_spacing=0.9,
        ).next_to(explain_note, DOWN, buff=0.4).align_to(explain_note, RIGHT)
        self.play(FadeIn(interpretation, shift=UP * 0.1))
        self.wait(2)
