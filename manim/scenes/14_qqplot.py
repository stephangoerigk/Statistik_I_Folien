import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK

N = 60
PROBS = (np.arange(1, N + 1) - 0.5) / N
Q = stats.norm.ppf(PROBS)  # feste theoretische Standardnormal-Quantile

# Ziel-Quantile einer stark rechtsschiefen Verteilung (Chi²), standardisiert
_SKEW_RAW = stats.chi2.ppf(PROBS, df=3)
SKEW_TARGET = (_SKEW_RAW - _SKEW_RAW.mean()) / _SKEW_RAW.std()


def deviate(t):
    # t=0 -> perfekt normal (Q), t=1 -> stark schiefe Zielverteilung
    return (1 - t) * Q + t * SKEW_TARGET


class QQPlot(StatScene):
    def construct(self):
        title = self.title("QQ-Plot")
        self.play(Write(title))

        purpose = Text(
            "Nutzen: Prüfen, ob Daten (annähernd) normalverteilt sind",
            font_size=24, color=MAROON,
        ).next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(purpose, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(purpose))

        d_tracker = ValueTracker(0.0)

        hist_axes = Axes(
            x_range=[-4, 6, 2],
            y_range=[0, 0.6, 0.2],
            x_length=5.6,
            y_length=3.7,
            axis_config={"include_tip": False, "color": INK},
        ).shift(LEFT * 3.3 + DOWN * 0.5)
        hist_x_label = Text("Wert", font_size=18, color=INK).next_to(hist_axes.x_axis, DOWN, buff=0.25)
        hist_title = Text("Histogramm", font_size=20, color=INK).next_to(hist_axes, UP, buff=0.6)

        qq_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-4, 5, 1],
            x_length=5.2,
            y_length=3.7,
            axis_config={"include_tip": False, "color": INK},
        ).shift(RIGHT * 3.3 + DOWN * 0.5)
        qq_x_label = Text("Theoretische Quantile", font_size=16, color=INK).next_to(qq_axes, DOWN, buff=0.25)
        qq_title = Text("QQ-Plot", font_size=20, color=INK).next_to(qq_axes, UP, buff=0.6)

        legend_line = Line(LEFT * 0.25, RIGHT * 0.25, color=MAGENTA, stroke_width=3)
        legend_text = Text("= perfekte Normalverteilung", font_size=16, color=MAGENTA)
        legend = VGroup(legend_line, legend_text).arrange(RIGHT, buff=0.12).next_to(hist_title, DOWN, buff=0.15)

        mean_val = DecimalNumber(0, num_decimal_places=2, color=INK, font_size=22)
        sd_val = DecimalNumber(1, num_decimal_places=2, color=INK, font_size=22)
        stats_line = VGroup(
            Text("Mittelwert = ", font_size=22, color=INK), mean_val,
            Text("   SD = ", font_size=22, color=INK), sd_val,
        ).arrange(RIGHT, buff=0.08).next_to(hist_title, UP, buff=0.25)

        self.play(Create(hist_axes), Create(qq_axes))
        self.play(FadeIn(hist_title), FadeIn(qq_title), FadeIn(hist_x_label), FadeIn(qq_x_label))
        self.play(FadeIn(legend, shift=UP * 0.1))
        self.play(Write(stats_line))
        self.wait(0.5)

        def current_data():
            return deviate(d_tracker.get_value())

        def make_histogram():
            data = current_data()
            bins = np.linspace(-4, 6, 21)
            counts, edges = np.histogram(data, bins=bins)
            width = edges[1] - edges[0]
            density = counts / (N * width)
            bars = VGroup()
            for c, left, right in zip(density, edges[:-1], edges[1:]):
                if c <= 0:
                    continue
                bar = Rectangle(
                    width=hist_axes.x_axis.unit_size * width,
                    height=hist_axes.y_axis.unit_size * c,
                    stroke_color=INK, stroke_width=1,
                    fill_color=MAROON, fill_opacity=0.6,
                )
                bar.move_to(hist_axes.c2p((left + right) / 2, c / 2))
                bars.add(bar)
            return bars

        def make_normal_curve():
            data = current_data()
            mu, sigma = float(np.mean(data)), max(float(np.std(data)), 0.05)
            return hist_axes.plot(
                lambda x: (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2),
                x_range=[-4, 6], color=MAGENTA, stroke_width=3,
            )

        def make_qq_points():
            data = current_data()
            mu, sigma = float(np.mean(data)), max(float(np.std(data)), 1e-6)
            standardized = np.sort((data - mu) / sigma)
            return VGroup(*[
                Dot(qq_axes.c2p(q, s), color=MAROON, radius=0.045)
                for q, s in zip(Q, standardized)
            ])

        histogram = always_redraw(make_histogram)
        normal_curve = always_redraw(make_normal_curve)
        qq_points = always_redraw(make_qq_points)
        qq_line = Line(qq_axes.c2p(-3, -3), qq_axes.c2p(3, 3), color=MAGENTA, stroke_width=2.5)

        def update_mean(m):
            m.set_value(np.mean(current_data()))

        def update_sd(m):
            m.set_value(np.std(current_data()))

        mean_val.add_updater(update_mean)
        sd_val.add_updater(update_sd)

        self.play(Create(qq_line))
        self.add(histogram, normal_curve, qq_points)
        self.wait(0.5)

        self.play(d_tracker.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(1)
        self.play(d_tracker.animate.set_value(0.35), run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(d_tracker.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(1.2)
        self.play(d_tracker.animate.set_value(0.0), run_time=4, rate_func=smooth)
        self.wait(0.5)

        mean_val.clear_updaters()
        sd_val.clear_updaters()

        perfect_label = Text(
            "Perfekte Normalverteilung: Punkte liegen exakt auf der Linie",
            font_size=22, color=MAGENTA,
        ).next_to(VGroup(hist_x_label, qq_x_label), DOWN, buff=0.4)
        self.play(FadeIn(perfect_label, shift=UP * 0.2))
        self.wait(2)
