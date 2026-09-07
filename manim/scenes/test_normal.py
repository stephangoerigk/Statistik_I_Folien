from manim import *


class NormalDistributionIntro(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": False},
        )
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        def normal_pdf(x, mu=0, sigma=1):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

        sigma_tracker = ValueTracker(2.0)

        curve = always_redraw(
            lambda: axes.plot(
                lambda x: normal_pdf(x, sigma=sigma_tracker.get_value()),
                color=BLUE,
            )
        )

        title = Text("Normalverteilung", font_size=36).to_edge(UP)

        self.play(Write(title))
        self.play(Create(axes), Write(labels))
        self.play(Create(curve))
        self.wait(0.5)

        self.play(sigma_tracker.animate.set_value(0.5), run_time=2)
        self.wait(0.5)
        self.play(sigma_tracker.animate.set_value(2.0), run_time=2)
        self.wait(1)
