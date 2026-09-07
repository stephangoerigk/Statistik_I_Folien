import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm, t as t_dist, f as f_dist, chi2, binom

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, GRAY


def dashed_vline(axes, x, y_max, color):
    return DashedLine(axes.c2p(x, 0), axes.c2p(x, y_max), color=color, stroke_width=2)


def tail_area(axes, curve, x_lo, x_hi, color):
    return axes.get_area(curve, x_range=[x_lo, x_hi], color=color, opacity=0.3)


def pin_marker(axes, x, color):
    tri = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.13).rotate(PI)
    tri.move_to(axes.c2p(x, 0) + UP * 0.13)
    return tri


class Testverteilungen(StatScene):
    def construct(self):
        main_title = self.title("Wahrscheinlichkeitsverteilungen der Hypothesentests")
        self.play(Write(main_title))

        intro = Text(
            "Jeder Test vergleicht eine beobachtete Testgröße mit ihrer Verteilung unter H0",
            font_size=24, color=MAROON,
        ).next_to(main_title, DOWN, buff=0.4)
        self.play(FadeIn(intro, shift=UP * 0.2))
        self.wait(1.8)
        self.play(FadeOut(intro))

        grid_slots = {
            "binom": [-4.7, 1.7, 0],
            "z": [0, 1.7, 0],
            "t": [4.7, 1.7, 0],
            "f": [-2.35, -2.1, 0],
            "chi2": [2.35, -2.1, 0],
        }

        mini_refs = {}
        mini_groups = []

        # ================= 1. Binomialverteilung =================
        sec = Text("Binomialverteilung (Binomialtest)", font_size=26, color=MAROON).next_to(main_title, DOWN, buff=0.35)
        tests_txt = Text("Testet: Anteilswert / Wahrscheinlichkeit", font_size=20, color=INK).next_to(sec, DOWN, buff=0.2)
        formula = MathTex("k", "=", r"\text{Anzahl Erfolge}", color=INK).scale(0.9).next_to(tests_txt, DOWN, buff=0.25)
        note = Text("Bei H0 (π=0,5): erwartet k = n·π₀ = 10", font_size=18, color=MAGENTA).next_to(formula, DOWN, buff=0.2)

        axes_b = Axes(
            x_range=[0, 20, 5], y_range=[0, 0.2, 0.05], x_length=8, y_length=2.6,
            axis_config={"include_tip": False, "color": INK},
        ).next_to(note, DOWN, buff=0.35)
        bars_b = VGroup()
        for k in range(21):
            p = binom.pmf(k, 20, 0.5)
            bar = Rectangle(
                width=axes_b.x_axis.unit_size * 0.8, height=axes_b.y_axis.unit_size * p,
                stroke_width=0.5, stroke_color=INK, fill_color=MAROON, fill_opacity=0.6,
            )
            bar.move_to(axes_b.c2p(k, p / 2))
            bars_b.add(bar)

        crit_lo_b, crit_hi_b = 5, 15
        shade_b = VGroup(
            *[bars_b[k].copy().set_fill(MAGENTA, opacity=0.5) for k in range(0, crit_lo_b + 1)],
            *[bars_b[k].copy().set_fill(MAGENTA, opacity=0.5) for k in range(crit_hi_b, 21)],
        )
        crit_label_b = Text(f"k≤{crit_lo_b} oder k≥{crit_hi_b}: Ablehnungsbereich", font_size=16, color=MAGENTA).next_to(axes_b, DOWN, buff=0.3)
        h0_dot_b = pin_marker(axes_b, 10, MAGENTA)
        h0_lab_b = Text("H0", font_size=16, color=MAGENTA).next_to(h0_dot_b, DOWN, buff=0.08)

        self.play(FadeIn(sec, shift=UP * 0.1))
        self.play(FadeIn(tests_txt, shift=UP * 0.1))
        self.play(Write(formula))
        self.play(FadeIn(note, shift=UP * 0.1))
        self.play(Create(axes_b), *[GrowFromCenter(b) for b in bars_b])
        self.play(FadeIn(shade_b), FadeIn(crit_label_b))
        self.play(FadeIn(h0_dot_b), FadeIn(h0_lab_b))
        self.wait(1.5)

        big_group_b = VGroup(sec, tests_txt, formula, note, axes_b, bars_b, shade_b, crit_label_b, h0_dot_b, h0_lab_b)
        self.play(FadeOut(big_group_b))

        mini_axes_b = Axes(
            x_range=[0, 20, 5], y_range=[0, 0.2, 0.05], x_length=3.6, y_length=1.5,
            axis_config={"include_tip": False, "color": INK, "stroke_width": 1.5},
        ).move_to(grid_slots["binom"])
        mini_bars_b = VGroup()
        for k in range(21):
            p = binom.pmf(k, 20, 0.5)
            color = MAGENTA if (k <= crit_lo_b or k >= crit_hi_b) else MAROON
            bar = Rectangle(
                width=mini_axes_b.x_axis.unit_size * 0.8, height=max(mini_axes_b.y_axis.unit_size * p, 0.001),
                stroke_width=0, fill_color=color, fill_opacity=0.55,
            )
            bar.move_to(mini_axes_b.c2p(k, p / 2))
            mini_bars_b.add(bar)
        mini_label_b = Text("Binomial", font_size=16, color=MAROON).next_to(mini_axes_b, UP, buff=0.1)
        mini_val_b = Text("k = 10", font_size=15, color=MAGENTA).next_to(mini_axes_b, DOWN, buff=0.1)
        mini_group_b = VGroup(mini_label_b, mini_axes_b, mini_bars_b, mini_val_b)
        self.play(FadeIn(mini_group_b, shift=UP * 0.1))
        mini_groups.append(mini_group_b)
        mini_refs["binom"] = {"axes": mini_axes_b, "val_label": mini_val_b, "stat": lambda p: 10 + p * 8}

        # ================= 2. z-Verteilung =================
        self.play(FadeOut(VGroup(*mini_groups)))
        sec = Text("Standardnormalverteilung (z-Test)", font_size=26, color=MAROON).next_to(main_title, DOWN, buff=0.35)
        tests_txt = Text("Testet: Gleichheit von Mittelwerten (σ bekannt)", font_size=20, color=INK).next_to(sec, DOWN, buff=0.2)
        formula = MathTex("z", "=", r"\frac{\bar{x}-\mu_0}{\sigma/\sqrt{n}}", color=INK).scale(0.9).next_to(tests_txt, DOWN, buff=0.25)
        note = Text("Bei H0 (Gleichheit): Zähler = 0 → z = 0", font_size=18, color=MAGENTA).next_to(formula, DOWN, buff=0.2)

        axes_z = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.45, 0.1], x_length=8, y_length=2.6,
            axis_config={"include_tip": False, "color": INK},
        ).next_to(note, DOWN, buff=0.35)
        curve_z = axes_z.plot(lambda x: norm.pdf(x), x_range=[-4, 4], color=MAROON, stroke_width=3)
        crit_z = 1.96
        shade_z = VGroup(
            tail_area(axes_z, curve_z, -4, -crit_z, MAGENTA),
            tail_area(axes_z, curve_z, crit_z, 4, MAGENTA),
        )
        lines_z = VGroup(dashed_vline(axes_z, -crit_z, norm.pdf(crit_z) + 0.05, MAGENTA), dashed_vline(axes_z, crit_z, norm.pdf(crit_z) + 0.05, MAGENTA))
        crit_label_z = Text(f"kritische Werte: z=±{crit_z}", font_size=16, color=MAGENTA).next_to(axes_z, DOWN, buff=0.3)
        h0_dot_z = pin_marker(axes_z, 0, MAGENTA)
        h0_lab_z = Text("H0", font_size=16, color=MAGENTA).next_to(h0_dot_z, DOWN, buff=0.08)

        self.play(FadeIn(sec, shift=UP * 0.1))
        self.play(FadeIn(tests_txt, shift=UP * 0.1))
        self.play(Write(formula))
        self.play(FadeIn(note, shift=UP * 0.1))
        self.play(Create(axes_z), Create(curve_z))
        self.play(Create(lines_z), FadeIn(shade_z), FadeIn(crit_label_z))
        self.play(FadeIn(h0_dot_z), FadeIn(h0_lab_z))
        self.wait(1.5)

        big_group_z = VGroup(sec, tests_txt, formula, note, axes_z, curve_z, lines_z, shade_z, crit_label_z, h0_dot_z, h0_lab_z)
        self.play(FadeOut(big_group_z))

        mini_axes_z = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.45, 0.1], x_length=3.6, y_length=1.5,
            axis_config={"include_tip": False, "color": INK, "stroke_width": 1.5},
        ).move_to(grid_slots["z"])
        mini_curve_z = mini_axes_z.plot(lambda x: norm.pdf(x), x_range=[-4, 4], color=MAROON, stroke_width=2)
        mini_shade_z = VGroup(
            tail_area(mini_axes_z, mini_curve_z, -4, -crit_z, MAGENTA),
            tail_area(mini_axes_z, mini_curve_z, crit_z, 4, MAGENTA),
        )
        mini_label_z = Text("z-Verteilung", font_size=16, color=MAROON).next_to(mini_axes_z, UP, buff=0.1)
        mini_val_z = Text("z = 0.00", font_size=15, color=MAGENTA).next_to(mini_axes_z, DOWN, buff=0.1)
        mini_group_z = VGroup(mini_label_z, mini_axes_z, mini_curve_z, mini_shade_z, mini_val_z)
        self.play(FadeIn(VGroup(*mini_groups, mini_group_z), shift=UP * 0.1))
        mini_groups.append(mini_group_z)
        mini_refs["z"] = {"axes": mini_axes_z, "val_label": mini_val_z, "stat": lambda p: p * 3.5}

        # ================= 3. t-Verteilung =================
        self.play(FadeOut(VGroup(*mini_groups)))
        sec = Text("t-Verteilung (t-Test)", font_size=26, color=MAROON).next_to(main_title, DOWN, buff=0.35)
        tests_txt = Text("Testet: Gleichheit von Mittelwerten (σ unbekannt)", font_size=20, color=INK).next_to(sec, DOWN, buff=0.2)
        formula = MathTex("t", "=", r"\frac{\bar{x}_1-\bar{x}_2}{SE}", color=INK).scale(0.9).next_to(tests_txt, DOWN, buff=0.25)
        note = Text("Bei H0 (Gleichheit): Zähler = 0 → t = 0", font_size=18, color=MAGENTA).next_to(formula, DOWN, buff=0.2)

        df_t = 10
        axes_t = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.45, 0.1], x_length=8, y_length=2.6,
            axis_config={"include_tip": False, "color": INK},
        ).next_to(note, DOWN, buff=0.35)
        curve_t = axes_t.plot(lambda x: t_dist.pdf(x, df_t), x_range=[-4, 4], color=MAROON, stroke_width=3)
        crit_t = round(t_dist.ppf(0.975, df_t), 3)
        shade_t = VGroup(
            tail_area(axes_t, curve_t, -4, -crit_t, MAGENTA),
            tail_area(axes_t, curve_t, crit_t, 4, MAGENTA),
        )
        lines_t = VGroup(dashed_vline(axes_t, -crit_t, t_dist.pdf(crit_t, df_t) + 0.05, MAGENTA), dashed_vline(axes_t, crit_t, t_dist.pdf(crit_t, df_t) + 0.05, MAGENTA))
        crit_label_t = Text(f"kritische Werte: t=±{crit_t:.2f} (df=10)", font_size=16, color=MAGENTA).next_to(axes_t, DOWN, buff=0.3)
        h0_dot_t = pin_marker(axes_t, 0, MAGENTA)
        h0_lab_t = Text("H0", font_size=16, color=MAGENTA).next_to(h0_dot_t, DOWN, buff=0.08)

        self.play(FadeIn(sec, shift=UP * 0.1))
        self.play(FadeIn(tests_txt, shift=UP * 0.1))
        self.play(Write(formula))
        self.play(FadeIn(note, shift=UP * 0.1))
        self.play(Create(axes_t), Create(curve_t))
        self.play(Create(lines_t), FadeIn(shade_t), FadeIn(crit_label_t))
        self.play(FadeIn(h0_dot_t), FadeIn(h0_lab_t))
        self.wait(1.5)

        big_group_t = VGroup(sec, tests_txt, formula, note, axes_t, curve_t, lines_t, shade_t, crit_label_t, h0_dot_t, h0_lab_t)
        self.play(FadeOut(big_group_t))

        mini_axes_t = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.45, 0.1], x_length=3.6, y_length=1.5,
            axis_config={"include_tip": False, "color": INK, "stroke_width": 1.5},
        ).move_to(grid_slots["t"])
        mini_curve_t = mini_axes_t.plot(lambda x: t_dist.pdf(x, df_t), x_range=[-4, 4], color=MAROON, stroke_width=2)
        mini_shade_t = VGroup(
            tail_area(mini_axes_t, mini_curve_t, -4, -crit_t, MAGENTA),
            tail_area(mini_axes_t, mini_curve_t, crit_t, 4, MAGENTA),
        )
        mini_label_t = Text("t-Verteilung", font_size=16, color=MAROON).next_to(mini_axes_t, UP, buff=0.1)
        mini_val_t = Text("t = 0.00", font_size=15, color=MAGENTA).next_to(mini_axes_t, DOWN, buff=0.1)
        mini_group_t = VGroup(mini_label_t, mini_axes_t, mini_curve_t, mini_shade_t, mini_val_t)
        self.play(FadeIn(VGroup(*mini_groups, mini_group_t), shift=UP * 0.1))
        mini_groups.append(mini_group_t)
        mini_refs["t"] = {"axes": mini_axes_t, "val_label": mini_val_t, "stat": lambda p: p * 3.5}

        # ================= 4. F-Verteilung =================
        self.play(FadeOut(VGroup(*mini_groups)))
        sec = Text("F-Verteilung (F-Test)", font_size=26, color=MAROON).next_to(main_title, DOWN, buff=0.35)
        tests_txt = Text("Testet: Gleichheit von Varianzen", font_size=20, color=INK).next_to(sec, DOWN, buff=0.2)
        formula = MathTex("F", "=", r"\frac{s_1^2}{s_2^2}", color=INK).scale(0.9).next_to(tests_txt, DOWN, buff=0.25)
        note = Text("Bei H0 (Gleichheit): Verhältnis = 1 → F = 1", font_size=18, color=MAGENTA).next_to(formula, DOWN, buff=0.2)

        dfn, dfd = 10, 10
        axes_f = Axes(
            x_range=[0, 6, 1], y_range=[0, 0.85, 0.2], x_length=8, y_length=2.6,
            axis_config={"include_tip": False, "color": INK},
        ).next_to(note, DOWN, buff=0.35)
        curve_f = axes_f.plot(lambda x: f_dist.pdf(x, dfn, dfd), x_range=[0.02, 6], color=MAROON, stroke_width=3)
        crit_f = round(f_dist.ppf(0.95, dfn, dfd), 3)
        shade_f = tail_area(axes_f, curve_f, crit_f, 6, MAGENTA)
        line_f = dashed_vline(axes_f, crit_f, f_dist.pdf(crit_f, dfn, dfd) + 0.35, MAGENTA)
        crit_label_f = Text(f"kritischer Wert: F={crit_f:.2f} (df=10,10)", font_size=16, color=MAGENTA).next_to(axes_f, DOWN, buff=0.3)
        h0_dot_f = pin_marker(axes_f, 1, MAGENTA)
        h0_lab_f = Text("H0", font_size=16, color=MAGENTA).next_to(h0_dot_f, DOWN, buff=0.08)

        self.play(FadeIn(sec, shift=UP * 0.1))
        self.play(FadeIn(tests_txt, shift=UP * 0.1))
        self.play(Write(formula))
        self.play(FadeIn(note, shift=UP * 0.1))
        self.play(Create(axes_f), Create(curve_f))
        self.play(Create(line_f), FadeIn(shade_f), FadeIn(crit_label_f))
        self.play(FadeIn(h0_dot_f), FadeIn(h0_lab_f))
        self.wait(1.5)

        big_group_f = VGroup(sec, tests_txt, formula, note, axes_f, curve_f, line_f, shade_f, crit_label_f, h0_dot_f, h0_lab_f)
        self.play(FadeOut(big_group_f))

        mini_axes_f = Axes(
            x_range=[0, 6, 1], y_range=[0, 0.85, 0.2], x_length=3.6, y_length=1.5,
            axis_config={"include_tip": False, "color": INK, "stroke_width": 1.5},
        ).move_to(grid_slots["f"])
        mini_curve_f = mini_axes_f.plot(lambda x: f_dist.pdf(x, dfn, dfd), x_range=[0.02, 6], color=MAROON, stroke_width=2)
        mini_shade_f = tail_area(mini_axes_f, mini_curve_f, crit_f, 6, MAGENTA)
        mini_label_f = Text("F-Verteilung", font_size=16, color=MAROON).next_to(mini_axes_f, UP, buff=0.1)
        mini_val_f = Text("F = 1.00", font_size=15, color=MAGENTA).next_to(mini_axes_f, DOWN, buff=0.1)
        mini_group_f = VGroup(mini_label_f, mini_axes_f, mini_curve_f, mini_shade_f, mini_val_f)
        self.play(FadeIn(VGroup(*mini_groups, mini_group_f), shift=UP * 0.1))
        mini_groups.append(mini_group_f)
        mini_refs["f"] = {"axes": mini_axes_f, "val_label": mini_val_f, "stat": lambda p: 1 + p * 4}

        # ================= 5. Chi²-Verteilung =================
        self.play(FadeOut(VGroup(*mini_groups)))
        sec = Text("Chi²-Verteilung (χ²-Test)", font_size=26, color=MAROON).next_to(main_title, DOWN, buff=0.35)
        tests_txt = Text("Testet: Übereinstimmung von Häufigkeiten", font_size=20, color=INK).next_to(sec, DOWN, buff=0.2)
        formula = MathTex(r"\chi^2", "=", r"\sum \frac{(O-E)^2}{E}", color=INK).scale(0.9).next_to(tests_txt, DOWN, buff=0.25)
        note = Text("Bei H0 (O=E): Zähler = 0 → χ² = 0", font_size=18, color=MAGENTA).next_to(formula, DOWN, buff=0.2)

        df_c = 4
        axes_c = Axes(
            x_range=[0, 16, 4], y_range=[0, 0.22, 0.05], x_length=8, y_length=2.6,
            axis_config={"include_tip": False, "color": INK},
        ).next_to(note, DOWN, buff=0.35)
        curve_c = axes_c.plot(lambda x: chi2.pdf(x, df_c), x_range=[0.02, 16], color=MAROON, stroke_width=3)
        crit_c = round(chi2.ppf(0.95, df_c), 3)
        shade_c = tail_area(axes_c, curve_c, crit_c, 16, MAGENTA)
        line_c = dashed_vline(axes_c, crit_c, chi2.pdf(crit_c, df_c) + 0.09, MAGENTA)
        crit_label_c = Text(f"kritischer Wert: χ²={crit_c:.2f} (df=4)", font_size=16, color=MAGENTA).next_to(axes_c, DOWN, buff=0.3)
        h0_dot_c = pin_marker(axes_c, 0, MAGENTA)
        h0_lab_c = Text("H0", font_size=16, color=MAGENTA).next_to(h0_dot_c, DOWN, buff=0.08)

        self.play(FadeIn(sec, shift=UP * 0.1))
        self.play(FadeIn(tests_txt, shift=UP * 0.1))
        self.play(Write(formula))
        self.play(FadeIn(note, shift=UP * 0.1))
        self.play(Create(axes_c), Create(curve_c))
        self.play(Create(line_c), FadeIn(shade_c), FadeIn(crit_label_c))
        self.play(FadeIn(h0_dot_c), FadeIn(h0_lab_c))
        self.wait(1.5)

        big_group_c = VGroup(sec, tests_txt, formula, note, axes_c, curve_c, line_c, shade_c, crit_label_c, h0_dot_c, h0_lab_c)
        self.play(FadeOut(big_group_c))

        mini_axes_c = Axes(
            x_range=[0, 16, 4], y_range=[0, 0.22, 0.05], x_length=3.6, y_length=1.5,
            axis_config={"include_tip": False, "color": INK, "stroke_width": 1.5},
        ).move_to(grid_slots["chi2"])
        mini_curve_c = mini_axes_c.plot(lambda x: chi2.pdf(x, df_c), x_range=[0.02, 16], color=MAROON, stroke_width=2)
        mini_shade_c = tail_area(mini_axes_c, mini_curve_c, crit_c, 16, MAGENTA)
        mini_label_c = Text("χ²-Verteilung", font_size=16, color=MAROON).next_to(mini_axes_c, UP, buff=0.1)
        mini_val_c = Text("χ² = 0.00", font_size=15, color=MAGENTA).next_to(mini_axes_c, DOWN, buff=0.1)
        mini_group_c = VGroup(mini_label_c, mini_axes_c, mini_curve_c, mini_shade_c, mini_val_c)
        self.play(FadeIn(VGroup(*mini_groups, mini_group_c), shift=UP * 0.1))
        mini_groups.append(mini_group_c)
        mini_refs["chi2"] = {"axes": mini_axes_c, "val_label": mini_val_c, "stat": lambda p: p * 14}

        # ================= Simultaner Vergleich =================
        compare_note = Text(
            "Simultaner Vergleich: mit wachsendem Effekt wandert jede Testgröße Richtung Ablehnungsbereich",
            font_size=20, color=MAROON,
        ).move_to([0, -3.5, 0])
        self.play(FadeIn(compare_note, shift=UP * 0.2))
        self.wait(0.5)

        effect = ValueTracker(0.0)

        markers = {}
        for key, ref in mini_refs.items():
            axes_ref = ref["axes"]
            stat_fn = ref["stat"]
            marker = always_redraw(lambda axes_ref=axes_ref, stat_fn=stat_fn: pin_marker(axes_ref, stat_fn(effect.get_value()), MAROON).scale(0.7))
            markers[key] = marker
            self.add(marker)

        def make_updater(val_label_mobj, stat_fn, fmt):
            def updater(m):
                new_text = Text(fmt.format(stat_fn(effect.get_value())), font_size=15, color=MAGENTA).move_to(m)
                m.become(new_text)
            return updater

        mini_refs["binom"]["val_label"].add_updater(make_updater(mini_refs["binom"]["val_label"], mini_refs["binom"]["stat"], "k = {:.0f}"))
        mini_refs["z"]["val_label"].add_updater(make_updater(mini_refs["z"]["val_label"], mini_refs["z"]["stat"], "z = {:.2f}"))
        mini_refs["t"]["val_label"].add_updater(make_updater(mini_refs["t"]["val_label"], mini_refs["t"]["stat"], "t = {:.2f}"))
        mini_refs["f"]["val_label"].add_updater(make_updater(mini_refs["f"]["val_label"], mini_refs["f"]["stat"], "F = {:.2f}"))
        mini_refs["chi2"]["val_label"].add_updater(make_updater(mini_refs["chi2"]["val_label"], mini_refs["chi2"]["stat"], "χ² = {:.2f}"))

        self.play(effect.animate.set_value(1.0), run_time=6, rate_func=smooth)
        self.wait(2.5)
