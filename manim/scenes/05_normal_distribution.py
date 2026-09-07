import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, GRAY


def normal_pdf(x, mu=0, sigma=1):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


class Normalverteilung(StatScene):
    def construct(self):
        title = self.title("Normalverteilung")
        self.play(Write(title))

        formula = MathTex(
            r"f(x)", "=", r"\frac{1}{\sigma\sqrt{2\pi}}",
            r"e^{-\frac{(x-\mu)^2}{2\sigma^2}}",
            color=INK,
        ).scale(0.9).next_to(title, DOWN, buff=0.5)
        formula[0].set_color(MAROON)
        self.play(Write(formula))
        self.wait(1)

        mu_tracker = ValueTracker(100)
        sigma_tracker = ValueTracker(15)

        axes = Axes(
            x_range=[55, 145, 15],
            y_range=[0, 0.06, 0.01],
            x_length=9,
            y_length=3.0,
            axis_config={"include_tip": False, "color": INK},
        ).next_to(formula, DOWN, buff=1.15)
        axes.x_axis.add_numbers(color=INK, font_size=20)
        x_label = Text("x", font_size=20, color=INK).next_to(axes.x_axis, RIGHT, buff=0.2)
        y_label = Text("f(x)", font_size=20, color=INK).next_to(axes.y_axis, UP, buff=0.15)

        curve = always_redraw(
            lambda: axes.plot(
                lambda x: normal_pdf(x, mu=mu_tracker.get_value(), sigma=sigma_tracker.get_value()),
                x_range=[55, 145],
                color=MAROON,
                stroke_width=4,
            )
        )

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))
        self.play(Create(curve))
        self.wait(0.3)

        # ---------- μ-Linie und ±1σ-Linien (dynamisch) ----------
        def mu_line_func():
            mu, sigma = mu_tracker.get_value(), sigma_tracker.get_value()
            top = normal_pdf(mu, mu, sigma)
            return DashedLine(axes.c2p(mu, 0), axes.c2p(mu, top), color=MAGENTA, stroke_width=2.5)

        def mu_label_func():
            mu, sigma = mu_tracker.get_value(), sigma_tracker.get_value()
            top = normal_pdf(mu, mu, sigma)
            return MathTex(r"\mu", color=MAGENTA, font_size=26).next_to(axes.c2p(mu, top), UP, buff=0.12)

        def sigma_lines_func():
            mu, sigma = mu_tracker.get_value(), sigma_tracker.get_value()
            x1, x2 = mu - sigma, mu + sigma
            y1, y2 = normal_pdf(x1, mu, sigma), normal_pdf(x2, mu, sigma)
            l1 = DashedLine(axes.c2p(x1, 0), axes.c2p(x1, y1), color=GRAY, stroke_width=2)
            l2 = DashedLine(axes.c2p(x2, 0), axes.c2p(x2, y2), color=GRAY, stroke_width=2)
            lab1 = MathTex(r"-1\sigma", color=GRAY, font_size=20).next_to(l1, UP, buff=0.35)
            lab2 = MathTex(r"+1\sigma", color=GRAY, font_size=20).next_to(l2, UP, buff=0.35)
            return VGroup(l1, l2, lab1, lab2)

        mu_line = always_redraw(mu_line_func)
        mu_label = always_redraw(mu_label_func)
        sigma_lines = always_redraw(sigma_lines_func)

        self.play(Create(mu_line), Write(mu_label))
        self.play(Create(sigma_lines))
        self.wait(0.5)

        # ---------- Erklärung: häufig vs. selten ----------
        peak_point = axes.c2p(100, normal_pdf(100, 100, 15))
        tail_point_r = axes.c2p(129, normal_pdf(129, 100, 15))
        tail_point_l = axes.c2p(71, normal_pdf(71, 100, 15))

        explain_bold = Text("Annahme:", font_size=18, color=MAROON, weight=BOLD)
        explain_l1 = Text("Viele Größen in den", font_size=16, color=INK)
        explain_l2 = Text("Naturwissenschaften folgen", font_size=16, color=INK)
        explain_l3 = Text("dieser Verteilung: mittlere", font_size=16, color=INK)
        explain_l4 = Text("Werte häufig, extreme selten", font_size=16, color=INK)
        explain = VGroup(explain_bold, explain_l1, explain_l2, explain_l3, explain_l4).arrange(
            DOWN, buff=0.14, aligned_edge=LEFT
        )
        explain.to_corner(UR, buff=0.3).shift(DOWN * 0.9)
        explain2 = VGroup()
        self.play(FadeIn(explain, shift=UP * 0.15))

        haeufig_label = Text("häufig", font_size=20, color=MAGENTA).move_to(peak_point + UP * 1.1)
        haeufig_arrow = Arrow(haeufig_label.get_bottom(), peak_point + UP * 0.45, buff=0.08, color=MAGENTA, stroke_width=2)
        selten_label_r = Text("selten", font_size=20, color=MAGENTA).move_to(tail_point_r + UP * 0.9 + RIGHT * 0.2)
        selten_arrow_r = Arrow(selten_label_r.get_bottom(), tail_point_r + UP * 0.05, buff=0.08, color=MAGENTA, stroke_width=2)
        selten_label_l = Text("selten", font_size=20, color=MAGENTA).move_to(tail_point_l + UP * 0.9 + LEFT * 0.2)
        selten_arrow_l = Arrow(selten_label_l.get_bottom(), tail_point_l + UP * 0.05, buff=0.08, color=MAGENTA, stroke_width=2)

        self.play(FadeIn(haeufig_label), GrowArrow(haeufig_arrow))
        self.play(
            FadeIn(selten_label_r), GrowArrow(selten_arrow_r),
            FadeIn(selten_label_l), GrowArrow(selten_arrow_l),
        )
        self.wait(2)
        self.play(FadeOut(VGroup(
            explain, explain2, haeufig_label, haeufig_arrow,
            selten_label_r, selten_arrow_r, selten_label_l, selten_arrow_l,
        )))

        # ---------- μ / σ live rechts neben der Achse ----------
        nv_heading = Text("NV definiert durch:", font_size=15, color=INK).next_to(axes, RIGHT, buff=0.35).shift(UP * 0.9)

        mu_tag = MathTex(r"\mu", "=", color=MAGENTA, font_size=28)
        mu_val = DecimalNumber(mu_tracker.get_value(), num_decimal_places=0, color=MAGENTA, font_size=28)
        mu_group = VGroup(mu_tag, mu_val).arrange(RIGHT, buff=0.1)
        sigma_tag = MathTex(r"\sigma", "=", color=MAGENTA, font_size=28)
        sigma_val = DecimalNumber(sigma_tracker.get_value(), num_decimal_places=0, color=MAGENTA, font_size=28)
        sigma_group = VGroup(sigma_tag, sigma_val).arrange(RIGHT, buff=0.1)
        side_labels = VGroup(mu_group, sigma_group).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side_labels.next_to(nv_heading, DOWN, buff=0.3).align_to(nv_heading, LEFT)

        mu_val.add_updater(lambda m: m.set_value(mu_tracker.get_value()))
        sigma_val.add_updater(lambda m: m.set_value(sigma_tracker.get_value()))

        self.play(FadeIn(nv_heading), FadeIn(side_labels))
        self.wait(0.5)

        def move_label(text):
            return Text(text, font_size=24, color=MAROON).move_to([0, -3.2, 0])

        lbl = move_label("höhere Streuung")
        self.play(FadeIn(lbl, shift=UP * 0.15))
        self.play(sigma_tracker.animate.set_value(20), run_time=1.8)
        self.wait(0.3)
        self.play(FadeOut(lbl))

        lbl = move_label("geringere Streuung")
        self.play(FadeIn(lbl, shift=UP * 0.15))
        self.play(sigma_tracker.animate.set_value(8), run_time=1.8)
        self.wait(0.3)
        self.play(FadeOut(lbl))

        self.play(sigma_tracker.animate.set_value(15), run_time=1.5)
        self.wait(0.5)

        lbl = move_label("höherer Mittelwert")
        self.play(FadeIn(lbl, shift=UP * 0.15))
        self.play(mu_tracker.animate.set_value(108), run_time=1.8)
        self.wait(0.3)
        self.play(FadeOut(lbl))

        lbl = move_label("niedrigerer Mittelwert")
        self.play(FadeIn(lbl, shift=UP * 0.15))
        self.play(mu_tracker.animate.set_value(92), run_time=1.8)
        self.wait(0.3)
        self.play(FadeOut(lbl))

        self.play(mu_tracker.animate.set_value(100), run_time=1.5)
        self.wait(0.5)

        mu_val.clear_updaters()
        sigma_val.clear_updaters()

        # ---------- 68-95-99,7-Regel ----------
        peak = normal_pdf(100, 100, 15)
        b68 = Brace(Line(axes.c2p(85, peak), axes.c2p(115, peak)), UP, color=MAGENTA, buff=0.5)
        l68 = Text("68%", font_size=16, color=MAGENTA).next_to(b68, UP, buff=0.05)
        b95 = Brace(Line(axes.c2p(70, peak), axes.c2p(130, peak)), UP, color=MAGENTA, buff=1.2)
        l95 = Text("~95%", font_size=16, color=MAGENTA).next_to(b95, UP, buff=0.05)
        b997 = Brace(Line(axes.c2p(55, peak), axes.c2p(145, peak)), UP, color=MAGENTA, buff=1.9)
        l997 = Text("~99,7%", font_size=16, color=MAGENTA).next_to(b997, UP, buff=0.05)

        def sigma_marker(x, tex):
            y = max(normal_pdf(x, 100, 15), 0.012)
            line = DashedLine(axes.c2p(x, 0), axes.c2p(x, y), color=GRAY, stroke_width=2)
            label = MathTex(tex, color=GRAY, font_size=18).next_to(line, UP, buff=0.15)
            return VGroup(line, label)

        lines_2s = VGroup(sigma_marker(70, r"-2\sigma"), sigma_marker(130, r"+2\sigma"))
        lines_3s = VGroup(sigma_marker(55, r"-3\sigma"), sigma_marker(145, r"+3\sigma"))

        self.play(GrowFromCenter(b68), Write(l68))
        self.wait(0.4)
        self.play(GrowFromCenter(b95), Write(l95), Create(lines_2s))
        self.wait(0.4)
        self.play(GrowFromCenter(b997), Write(l997), Create(lines_3s))
        self.wait(1.8)

        self.play(FadeOut(VGroup(b68, l68, b95, l95, b997, l997, lines_2s, lines_3s)))

        # Nebeninfos und Dichteformel ausblenden, ursprüngliche NV (Achse + Kurve) bleibt sichtbar
        self.play(FadeOut(VGroup(
            x_label, y_label, mu_line, mu_label, sigma_lines, nv_heading, side_labels,
        )))
        self.play(FadeOut(formula))

        # ---------- Standardisierung (oben, gleiche Größe wie die Dichteformel) – bleibt während des Morphs sichtbar ----------
        std_explain = Text(
            "Jede NV kann mittels Standardisierung (z-Transformation)",
            font_size=22, color=MAROON,
        ).next_to(title, DOWN, buff=0.5)
        std_explain2 = Text(
            "in eine Standardnormalverteilung umgewandelt werden",
            font_size=22, color=MAROON,
        ).next_to(std_explain, DOWN, buff=0.15)
        std_formula = MathTex("z", "=", r"\frac{x-\mu}{\sigma}", color=INK).scale(0.9)
        std_formula[0].set_color(MAGENTA)
        std_formula.next_to(std_explain2, DOWN, buff=0.4)

        self.play(FadeIn(std_explain, shift=UP * 0.15), FadeIn(std_explain2, shift=UP * 0.15))
        self.wait(0.5)
        self.play(Write(std_formula))
        self.wait(1.5)

        # ---------- ursprüngliche NV morpht zur Standardnormalverteilung ----------
        curve.clear_updaters()
        axes_center = axes.get_center()

        axes2 = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.5, 0.1], x_length=9, y_length=3.0,
            axis_config={"include_tip": False, "color": INK},
        ).move_to(axes_center)
        axes2.x_axis.add_numbers(color=INK, font_size=20)
        ref_num = axes2.x_axis.numbers[0]
        zero_label = Text("0", font_size=20, color=INK).move_to([axes2.c2p(0, 0)[0], ref_num.get_y(), 0])
        curve2 = axes2.plot(lambda x: normal_pdf(x, 0, 1), x_range=[-4, 4], color=MAGENTA, stroke_width=4)
        z_label = Text("z", font_size=20, color=INK).next_to(axes2.x_axis, RIGHT, buff=0.2)

        mu2_line = DashedLine(axes2.c2p(0, 0), axes2.c2p(0, 0.5), color=MAGENTA, stroke_width=2.5)
        mu2_label = MathTex(r"\mu", color=MAGENTA, font_size=26).next_to(mu2_line, UP, buff=0.12)
        s2_l = DashedLine(axes2.c2p(-1, 0), axes2.c2p(-1, normal_pdf(-1, 0, 1)), color=GRAY, stroke_width=2)
        s2_r = DashedLine(axes2.c2p(1, 0), axes2.c2p(1, normal_pdf(1, 0, 1)), color=GRAY, stroke_width=2)
        s2_l_lab = MathTex(r"-1\sigma", color=GRAY, font_size=20).next_to(s2_l, UP, buff=0.35)
        s2_r_lab = MathTex(r"+1\sigma", color=GRAY, font_size=20).next_to(s2_r, UP, buff=0.35)

        self.play(Transform(curve, curve2), FadeOut(axes), FadeIn(axes2), FadeIn(zero_label), run_time=2.5)
        self.play(FadeIn(z_label))
        self.play(Create(mu2_line), Write(mu2_label))
        self.play(Create(s2_l), Create(s2_r), Write(s2_l_lab), Write(s2_r_lab))
        self.wait(2)
        self.wait(2)
