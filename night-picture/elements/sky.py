import math

from elements.element import Element


class Sky(Element):
    def __init__(self, width, height, horizon_color, top_color):
        self.width = width
        self.height = height
        self.horizon_color = horizon_color
        self.top_color = top_color

    def render(self, painter, time):
        painter.alpha_blend()
        painter.gradient_rect(0.0, 0.0, self.width, self.height, self.horizon_color, self.top_color)


class Vignette(Element):
    def __init__(self, width, height, color, strength):
        self.center_x = width * 0.5
        self.center_y = height * 0.55
        self.inner_radius = math.hypot(width, height) * 0.30
        self.outer_radius = math.hypot(width, height) * 0.62
        self.clear = (color[0], color[1], color[2], 0.0)
        self.dark = (color[0], color[1], color[2], strength)

    def render(self, painter, time):
        painter.alpha_blend()
        painter.ring(
            self.center_x,
            self.center_y,
            self.inner_radius,
            self.outer_radius,
            self.clear,
            self.dark,
            96,
        )
