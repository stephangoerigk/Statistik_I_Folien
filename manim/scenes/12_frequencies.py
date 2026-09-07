import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK

SYMBOL = {"F": "♀", "M": "♂"}


def symbol_tile(code, side=0.85, font_size=32):
    box = Square(side_length=side, color=INK).set_fill(WHITE, opacity=1)
    label = Text(SYMBOL[code], font_size=font_size, color=INK)
    return VGroup(box, label)


class Haeufigkeiten(StatScene):
    def construct(self):
        title = self.title("Häufigkeiten")
        self.play(Write(title))

        subtitle = Text("Absolute und relative Häufigkeiten", font_size=26, color=INK).next_to(title, DOWN, buff=0.35)
        var_label = Text("Variable: Geschlecht (nominalskaliert)", font_size=22, color=INK).next_to(subtitle, DOWN, buff=0.25)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.play(FadeIn(var_label, shift=UP * 0.2))
        self.wait(0.5)

        # Urliste
        sequence = ["M", "F", "F", "M", "F", "M", "F", "M", "F", "F"]
        n_total = len(sequence)
        tw = 1.05
        start_x = -tw * (n_total - 1) / 2
        tiles = VGroup()
        for i, code in enumerate(sequence):
            t = symbol_tile(code)
            t.move_to(RIGHT * (start_x + i * tw) + UP * 0.5)
            tiles.add(t)

        urliste_label = Text("N = 10", font_size=20, color=INK).next_to(tiles, UP, buff=0.3)
        self.play(FadeIn(urliste_label, shift=UP * 0.2))
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tiles], lag_ratio=0.1))
        self.wait(0.7)
        self.play(FadeOut(subtitle), FadeOut(var_label))

        # Zählprozess: Elemente wandern in Bins, Zähler laufen mit
        f_bin_x, m_bin_x = -3.0, 3.0
        bin_base_y = -2.0

        f_header = VGroup(
            Text("♀", font_size=40, color=MAROON),
        ).move_to([f_bin_x, -0.7, 0])
        m_header = VGroup(
            Text("♂", font_size=40, color=MAROON),
        ).move_to([m_bin_x, -0.7, 0])

        f_count = Text("0", font_size=30, color=MAGENTA).next_to(f_header, RIGHT, buff=0.3)
        m_count = Text("0", font_size=30, color=MAGENTA).next_to(m_header, RIGHT, buff=0.3)

        self.play(FadeIn(f_header), FadeIn(m_header), FadeIn(f_count), FadeIn(m_count))
        self.wait(0.3)

        f_stack, m_stack = 0, 0
        for i, code in enumerate(sequence):
            tile = tiles[i]
            if code == "F":
                target = [f_bin_x + (f_stack % 3) * 0.6 - 0.6, bin_base_y - (f_stack // 3) * 0.7, 0]
                f_stack += 1
                new_count = Text(str(f_stack), font_size=30, color=MAGENTA).move_to(f_count)
                self.play(tile.animate.scale(0.7).move_to(target), Transform(f_count, new_count), run_time=0.4)
            else:
                target = [m_bin_x + (m_stack % 3) * 0.6 - 0.6, bin_base_y - (m_stack // 3) * 0.7, 0]
                m_stack += 1
                new_count = Text(str(m_stack), font_size=30, color=MAGENTA).move_to(m_count)
                self.play(tile.animate.scale(0.7).move_to(target), Transform(m_count, new_count), run_time=0.4)

        self.wait(0.7)
        self.play(FadeOut(urliste_label))
        self.play(FadeOut(tiles), FadeOut(f_header), FadeOut(m_header), FadeOut(f_count), FadeOut(m_count))

        n_f = sequence.count("F")
        n_m = sequence.count("M")

        # Häufigkeitstabelle (absolut)
        abs_title = Text("Häufigkeitstabelle (absolute Häufigkeiten)", font_size=24, color=MAROON).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(abs_title, shift=UP * 0.2))

        abs_table = Table(
            [["Ausprägung", "n"], ["♀", str(n_f)], ["♂", str(n_m)], ["Gesamt", str(n_total)]],
            include_outer_lines=True,
            line_config={"color": INK, "stroke_width": 1.5},
            element_to_mobject=lambda s: Text(s, color=INK, font_size=28),
        ).scale(0.9).next_to(abs_title, DOWN, buff=0.5)
        self.play(Create(abs_table))
        self.wait(1.5)
        self.play(FadeOut(abs_table), FadeOut(abs_title))

        # Relative Häufigkeit: Formel
        rel_title = Text("Relative Häufigkeiten (%)", font_size=24, color=MAROON).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(rel_title, shift=UP * 0.2))

        general_rel = MathTex("f_j", "=", r"\frac{n_j}{N}", r"\cdot 100\%", color=INK).scale(1.1).next_to(rel_title, DOWN, buff=0.5)
        general_rel[0].set_color(MAROON)
        self.play(Write(general_rel))
        self.wait(1)

        specific_rel = MathTex(
            "f_w", "=", r"\frac{" + str(n_f) + "}{" + str(n_total) + "}", r"\cdot 100\%", "=", f"{n_f / n_total * 100:.0f}\\%",
            color=INK,
        ).scale(1.1)
        specific_rel[0].set_color(MAROON)
        specific_rel[-1].set_color(MAGENTA)
        specific_rel.move_to(general_rel)
        self.play(TransformMatchingTex(general_rel, specific_rel))
        self.wait(1.5)
        self.play(FadeOut(specific_rel))

        # Häufigkeitstabelle (relativ)
        rel_pct_f = f"{n_f / n_total * 100:.0f}%"
        rel_pct_m = f"{n_m / n_total * 100:.0f}%"
        rel_table = Table(
            [["Ausprägung", "%"], ["♀", rel_pct_f], ["♂", rel_pct_m], ["Gesamt", "100%"]],
            include_outer_lines=True,
            line_config={"color": INK, "stroke_width": 1.5},
            element_to_mobject=lambda s: Text(s, color=INK, font_size=28),
        ).scale(0.9).next_to(rel_title, DOWN, buff=0.5)
        self.play(Create(rel_table))
        self.wait(1.5)
        self.play(FadeOut(rel_table), FadeOut(rel_title))

        # Abschluss: kombinierte Schreibweise N (%)
        closing_label = Text("Übliche Schreibweise von Häufigkeiten in Publikationen:", font_size=24, color=INK).next_to(title, DOWN, buff=0.6)
        template = Text("absolut (relativ)", font_size=32, color=INK).next_to(closing_label, DOWN, buff=0.5)
        result = Text(f"♀: {n_f} ({rel_pct_f})", font_size=36, color=MAGENTA).move_to(template)

        self.play(FadeIn(closing_label, shift=UP * 0.2))
        self.play(FadeIn(template, shift=UP * 0.2))
        self.wait(1.2)
        self.play(ReplacementTransform(template, result))
        self.wait(2)
