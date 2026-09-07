import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from style import StatScene, MAROON, MAGENTA, INK, styled_number_line


def make_tile(text, side=0.9, font_size=28):
    box = Square(side_length=side, color=INK).set_fill(WHITE, opacity=1)
    label = Text(text, font_size=font_size, color=INK)
    return VGroup(box, label)


class Skalenniveaus(StatScene):
    def construct(self):
        title = self.title("Skalenniveaus")
        self.play(Write(title))

        subtitle = Text("Wie viel Information trägt eine Variable?", font_size=26, color=INK).next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(1)

        names = ["Nominal", "Ordinal", "Intervall", "Verhältnis"]
        xs = [-4.8, -1.6, 1.6, 4.8]
        chips = VGroup()
        for name, x in zip(names, xs):
            box = RoundedRectangle(corner_radius=0.15, width=2.6, height=0.9, color=MAROON, fill_color=WHITE, fill_opacity=1, stroke_width=2.5)
            label = Text(name, font_size=24, color=MAROON)
            chip = VGroup(box, label).move_to([x, 0, 0])
            chips.add(chip)

        arrows = VGroup(*[
            Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.1, color=INK, stroke_width=2)
            for i in range(3)
        ])

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.2))
        self.play(*[GrowArrow(a) for a in arrows])
        self.wait(0.5)
        note = Text("je höher das Niveau, desto mehr Aussagen und Rechenoperationen möglich", font_size=20, color=INK).next_to(chips, DOWN, buff=0.5)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(note), FadeOut(subtitle), FadeOut(arrows))

        self.play(chips.animate.arrange(RIGHT, buff=0.25).scale(0.45).next_to(title, DOWN, buff=0.35))

        def highlight_chip(i):
            chip = chips[i]
            return AnimationGroup(
                chip[0].animate.set_fill(MAGENTA, opacity=0.15).set_stroke(MAGENTA, width=3),
                chip[1].animate.set_color(MAGENTA),
            )

        # ---------- 1. Nominalskala ----------
        self.play(highlight_chip(0))
        sub = Text("Nominalskala – nur Gleichheit / Verschiedenheit", font_size=24, color=MAROON).next_to(chips, DOWN, buff=0.4)
        self.play(FadeIn(sub, shift=UP * 0.2))

        blood_types = ["A", "B", "A", "AB", "0"]
        tw = 1.3
        start_x = -tw * (len(blood_types) - 1) / 2
        tiles1 = VGroup()
        for i, v in enumerate(blood_types):
            t = make_tile(v)
            t.move_to(RIGHT * (start_x + i * tw) + UP * 0.5)
            tiles1.add(t)
        var_label1 = Text("Variable: Blutgruppe", font_size=20, color=INK).move_to([0, -3.3, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tiles1], lag_ratio=0.15), FadeIn(var_label1))
        self.wait(0.3)

        # Reihenfolge ist austauschbar: zwei Kacheln tauschen
        pos0, pos1 = tiles1[0].get_center(), tiles1[1].get_center()
        self.play(tiles1[0].animate.move_to(pos1), tiles1[1].animate.move_to(pos0))
        self.wait(0.3)
        swap_note = Text("Reihenfolge ist austauschbar – Information bleibt gleich", font_size=20, color=INK).next_to(tiles1, DOWN, buff=1.0)
        self.play(FadeIn(swap_note, shift=UP * 0.2))
        self.wait(1)
        self.play(FadeOut(swap_note))

        a_tiles = [t for t, v in zip(tiles1, blood_types) if v == "A"]
        b_tile = [t for t, v in zip(tiles1, blood_types) if v == "B"][0]

        eq = MathTex("=", color=MAGENTA, font_size=36).move_to(
            (a_tiles[0].get_center() + a_tiles[1].get_center()) / 2 + UP * 0.9
        )
        self.play(
            a_tiles[0][0].animate.set_stroke(MAGENTA, width=3),
            a_tiles[1][0].animate.set_stroke(MAGENTA, width=3),
            Write(eq),
        )
        self.wait(0.7)

        neq = MathTex(r"\neq", color=MAGENTA, font_size=36).move_to(
            (a_tiles[0].get_center() + b_tile.get_center()) / 2 + DOWN * 0.9
        )
        self.play(b_tile[0].animate.set_stroke(MAGENTA, width=3), Write(neq))
        self.wait(1.2)

        self.play(FadeOut(tiles1), FadeOut(eq), FadeOut(neq), FadeOut(sub), FadeOut(var_label1))

        # ---------- 2. Ordinalskala ----------
        self.play(highlight_chip(1))
        sub2 = Text("Ordinalskala – Rangfolge, aber Abstände unbekannt", font_size=24, color=MAROON).next_to(chips, DOWN, buff=0.4)
        self.play(FadeIn(sub2, shift=UP * 0.2))

        times = [15.1, 9.8, 10.0]
        tiles2 = VGroup()
        for i, v in enumerate(times):
            t = make_tile(f"{v:.1f}s", font_size=24)
            t.move_to(RIGHT * (start_x + 1 * tw) + RIGHT * ((i - 1) * tw) + UP * 0.6)
            tiles2.add(t)
        var_label2 = Text("Variable: Wettlauf-Zeit / Rang", font_size=20, color=INK).move_to([0, -3.3, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tiles2], lag_ratio=0.15), FadeIn(var_label2))
        self.wait(0.3)

        order = sorted(range(len(times)), key=lambda i: times[i])
        sorted_x = [start_x + i * tw for i in range(len(times))]
        self.play(*[
            tiles2[orig_i].animate.move_to(RIGHT * sorted_x[rank] + UP * 0.6)
            for rank, orig_i in enumerate(order)
        ])
        self.wait(0.3)

        sorted_tiles = [tiles2[i] for i in order]
        gap1 = abs(times[order[1]] - times[order[0]])
        gap2 = abs(times[order[2]] - times[order[1]])
        b1 = Brace(VGroup(sorted_tiles[0], sorted_tiles[1]), DOWN, color=INK, buff=0.15)
        b1_label = b1.get_tex(r"\Delta=" + f"{gap1:.1f}" + r"\text{s}").scale(0.6)
        b2 = Brace(VGroup(sorted_tiles[1], sorted_tiles[2]), DOWN, color=INK, buff=0.15).shift(DOWN * 0.7)
        b2_label = b2.get_tex(r"\Delta=" + f"{gap2:.1f}" + r"\text{s}").scale(0.6)
        self.play(GrowFromCenter(b1), Write(b1_label), GrowFromCenter(b2), Write(b2_label))
        gap_note = Text("sehr unterschiedliche Abstände trotz gleicher Rang-„Abstände“", font_size=20, color=INK).next_to(VGroup(b1, b2, b1_label, b2_label), DOWN, buff=0.35)
        self.play(FadeIn(gap_note, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(b1), FadeOut(b1_label), FadeOut(b2), FadeOut(b2_label), FadeOut(gap_note))

        rank_labels = ["1.", "2.", "3."]
        self.play(*[
            Transform(sorted_tiles[i][1], Text(rank_labels[i], font_size=28, color=MAGENTA).move_to(sorted_tiles[i][1]))
            for i in range(3)
        ])
        rank_note = Text("nur die Reihenfolge bleibt übrig", font_size=20, color=MAGENTA).next_to(tiles2, DOWN, buff=0.6)
        self.play(FadeIn(rank_note, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(tiles2), FadeOut(rank_note), FadeOut(sub2), FadeOut(var_label2))

        # ---------- 3. Intervallskala ----------
        self.play(highlight_chip(2))
        sub3 = Text("Intervallskala – gleiche Abstände, aber kein echter Nullpunkt", font_size=23, color=MAROON).next_to(chips, DOWN, buff=0.4)
        self.play(FadeIn(sub3, shift=UP * 0.2))

        temp_line = styled_number_line([-10, 30, 10], length=9).shift(DOWN * 1.3)
        temp_axis_label = Text("Temperatur in °C", font_size=20, color=INK).next_to(temp_line, DOWN, buff=0.3)
        self.play(Create(temp_line), FadeIn(temp_axis_label))

        p10 = Dot(temp_line.n2p(10), color=MAROON, radius=0.1)
        p20 = Dot(temp_line.n2p(20), color=MAROON, radius=0.1)
        l10 = Text("10°C", font_size=22, color=MAROON).next_to(p10, UP, buff=0.2)
        l20 = Text("20°C", font_size=22, color=MAROON).next_to(p20, UP, buff=0.2)
        self.play(GrowFromCenter(p10), GrowFromCenter(p20), Write(l10), Write(l20))

        diff_brace = Brace(Line(p10.get_center() + UP * 0.55, p20.get_center() + UP * 0.55), UP, color=MAGENTA)
        diff_label = Text("Δ = 10° (gültig)", color=MAGENTA, font_size=22).next_to(diff_brace, UP, buff=0.1)
        self.play(GrowFromCenter(diff_brace), Write(diff_label))
        self.wait(0.7)

        ratio_claim = Text("„20°C ist doppelt so warm wie 10°C“  ✗", font_size=22, color=MAGENTA).next_to(temp_axis_label, DOWN, buff=0.4)
        zero_note = Text("0°C ist kein „Nichts“ – nur ein beliebiger Bezugspunkt", font_size=20, color=INK).next_to(ratio_claim, DOWN, buff=0.25)
        self.play(FadeIn(ratio_claim, shift=UP * 0.2))
        self.play(FadeIn(zero_note, shift=UP * 0.2))
        self.wait(2)

        self.play(FadeOut(VGroup(temp_line, temp_axis_label, p10, p20, l10, l20, diff_brace, diff_label, ratio_claim, zero_note, sub3)))

        # ---------- 4. Verhältnisskala ----------
        self.play(highlight_chip(3))
        sub4 = Text("Verhältnisskala – gleiche Abstände UND echter Nullpunkt", font_size=23, color=MAROON).next_to(chips, DOWN, buff=0.4)
        self.play(FadeIn(sub4, shift=UP * 0.2))

        weight_line = styled_number_line([0, 10, 2], length=9).shift(DOWN * 1.3)
        weight_axis_label = Text("Gewicht in kg", font_size=20, color=INK).next_to(weight_line, DOWN, buff=0.3)
        self.play(Create(weight_line), FadeIn(weight_axis_label))

        zero_tag = Text("0 = nichts vorhanden", font_size=20, color=MAGENTA).next_to(weight_line.n2p(0), UP, buff=1.2).shift(LEFT * 0.3)
        zero_arrow = Arrow(zero_tag.get_bottom(), weight_line.n2p(0) + UP * 0.15, buff=0.1, color=MAGENTA, stroke_width=2)
        self.play(FadeIn(zero_tag, shift=DOWN * 0.2), GrowArrow(zero_arrow))

        p2 = Dot(weight_line.n2p(2), color=MAROON, radius=0.1)
        p4 = Dot(weight_line.n2p(4), color=MAROON, radius=0.1)
        lg2 = Text("2 kg", font_size=22, color=MAROON).next_to(p2, UP, buff=0.2)
        lg4 = Text("4 kg", font_size=22, color=MAROON).next_to(p4, UP, buff=0.2)
        self.play(GrowFromCenter(p2), GrowFromCenter(p4), Write(lg2), Write(lg4))

        ratio_ok = Text("„4 kg ist doppelt so viel wie 2 kg“  ✓", font_size=22, color=MAGENTA).next_to(weight_axis_label, DOWN, buff=0.4)
        self.play(FadeIn(ratio_ok, shift=UP * 0.2))
        self.wait(2)

        self.play(FadeOut(VGroup(weight_line, weight_axis_label, zero_tag, zero_arrow, p2, p4, lg2, lg4, ratio_ok, sub4)))

        # ---------- Abschluss: Treppen-Anordnung nach Informationsgehalt ----------
        step_positions = [[-3.6, -1.1, 0], [-1.2, -0.35, 0], [1.2, 0.4, 0], [3.6, 1.15, 0]]
        self.play(
            *[chips[i].animate.scale(1.7).move_to(step_positions[i]) for i in range(4)],
        )
        self.wait(0.5)

        down_arrows = VGroup()
        for i in range(3):
            start = chips[i + 1].get_left() + LEFT * 0.1
            end = chips[i].get_top() + UP * 0.1
            mid = np.array([end[0], start[1], 0])
            h_seg = Line(start, mid, color=MAGENTA, stroke_width=3)
            v_seg = Arrow(mid, end, buff=0, color=MAGENTA, stroke_width=3, tip_length=0.18)
            down_arrows.add(VGroup(h_seg, v_seg))
        self.play(*[Create(a) for a in down_arrows])
        self.wait(0.3)

        closing = Text("Man kann immer nach unten wechseln (fein → grob) – nie umgekehrt", font_size=24, color=MAGENTA).next_to(chips, DOWN, buff=0.7)
        self.play(FadeIn(closing, shift=UP * 0.2))
        self.wait(2.5)
