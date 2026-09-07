from manim import *

# Palette aus xaringan-themer.css (Statistik I Folien)
MAROON = "#621C37"    # header/link/bold Farbe der Folien
MAGENTA = "#EE0071"   # inverse/highlight Farbe der Folien
INK = "#000000"       # Text
PAPER = "#FFFFFF"      # Hintergrund
GRAY = "#8A8A8A"       # sekundäre/dezente Elemente

config.background_color = PAPER


class StatScene(Scene):
    """Basis-Szene mit Folien-Look: weißer Hintergrund, dunkle Standardfarben."""

    def construct(self):
        raise NotImplementedError

    def title(self, text, font_size=30):
        return Text(text, font_size=font_size, color=INK).to_edge(UP)


def axes_style(**kwargs):
    defaults = dict(
        axis_config={"include_tip": False, "color": INK},
        x_axis_config={"font_size_scale": 1},
    )
    defaults.update(kwargs)
    return defaults


def styled_number_line(x_range, length=10, **kwargs):
    defaults = dict(
        color=INK,
        include_numbers=True,
        font_size=24,
        numbers_with_elongated_ticks=[],
    )
    defaults.update(kwargs)
    return NumberLine(x_range=x_range, length=length, **defaults)
