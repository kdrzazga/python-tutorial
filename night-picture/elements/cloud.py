import math

from elements.element import Element


class Cloud:
    def __init__(self, base_y, thickness, color, opacity, terms, drift, x_span, samples=72, layers=11):
        self.base_y = base_y
        self.thickness = thickness
        self.color = color
        self.opacity = opacity
        self.terms = terms
        self.drift = drift
        self.x_span = x_span
        self.samples = samples
        self.layers = layers

    def _centerline(self, x, time):
        y = self.base_y
        for amplitude, frequency, phase in self.terms:
            y += amplitude * math.sin(frequency * x + phase + time * self.drift)
        return y

    def render(self, painter, time):
        x_start, x_end = self.x_span
        rgb = self.color[:3]
        for layer in range(-self.layers, self.layers + 1):
            fraction = layer / self.layers
            alpha = self.opacity * math.exp(-(fraction * fraction) * 3.0)
            offset = fraction * self.thickness * 0.5
            band_color = (rgb[0], rgb[1], rgb[2], alpha)
            columns = []
            for index in range(self.samples + 1):
                x = x_start + (x_end - x_start) * index / self.samples
                center = self._centerline(x, time) + offset
                columns.append((x, center - 2.0, center + 2.0, band_color, band_color))
            painter.column_strip(columns)


class CloudBank(Element):
    def __init__(self, clouds):
        self.clouds = tuple(clouds)

    def render(self, painter, time):
        painter.alpha_blend()
        for cloud in self.clouds:
            cloud.render(painter, time)
