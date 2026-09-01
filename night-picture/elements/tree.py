import math

from elements.element import Element
from palette import BARK, BARK_RIM, CROWN_EDGE, CROWN_FILL


class Segment:
    def __init__(self, x0, y0, x1, y1, width0, width1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.width0 = width0
        self.width1 = width1


class Crown(Element):
    def __init__(self, center_x, center_y, radius, rng, lobe_count=4, resolution=140):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        terms = tuple(
            (rng.uniform(0.06, 0.20), rng.randint(2, 6), rng.uniform(0.0, 2.0 * math.pi))
            for _ in range(lobe_count)
        )
        self.outline = tuple(self._build_outline(terms, resolution))

    def _build_outline(self, terms, resolution):
        points = []
        for index in range(resolution + 1):
            angle = 2.0 * math.pi * index / resolution
            radius = self.radius
            for amplitude, harmonic, phase in terms:
                radius *= 1.0 + amplitude * math.sin(harmonic * angle + phase) / len(terms)
            points.append(
                (self.center_x + math.cos(angle) * radius, self.center_y + math.sin(angle) * radius * 0.82)
            )
        return points

    def render(self, painter, time):
        painter.alpha_blend()
        painter.fan(self.center_x, self.center_y, self.outline, CROWN_FILL, CROWN_EDGE)


class Tree(Element):
    def __init__(self, base_x, base_y, trunk_length, trunk_width, rng, lean=-0.12, max_segments=1600):
        self.segments = tuple(
            self._grow(base_x, base_y, trunk_length, trunk_width, rng, lean, max_segments)
        )

    def _grow(self, base_x, base_y, trunk_length, trunk_width, rng, lean, max_segments):
        segments = []
        stack = [(base_x, base_y, math.pi / 2.0 + lean, trunk_length, trunk_width)]
        while stack and len(segments) < max_segments:
            x, y, angle, length, width = stack.pop()
            if length < 5.0 or width < 0.6:
                continue
            step_count = 2
            current_x = x
            current_y = y
            current_angle = angle
            step_length = length / step_count
            for step in range(step_count):
                current_angle += rng.uniform(-0.10, 0.10)
                next_x = current_x + math.cos(current_angle) * step_length
                next_y = current_y + math.sin(current_angle) * step_length
                width_start = width * (1.0 - step / (step_count + 1.0))
                width_end = width * (1.0 - (step + 1.0) / (step_count + 1.0))
                segments.append(
                    Segment(
                        current_x,
                        current_y,
                        next_x,
                        next_y,
                        max(width_start, 0.6),
                        max(width_end, 0.6),
                    )
                )
                current_x = next_x
                current_y = next_y
            child_count = rng.choice((2, 2, 3))
            spread = 0.55
            for child in range(child_count):
                bias = (child - (child_count - 1) / 2.0) * spread
                child_angle = current_angle + bias + rng.uniform(-0.20, 0.20)
                child_length = length * rng.uniform(0.66, 0.80)
                child_width = width * 0.66
                stack.append((current_x, current_y, child_angle, child_length, child_width))
        return segments

    def render(self, painter, time):
        painter.alpha_blend()
        for segment in self.segments:
            painter.tapered_segment(
                segment.x0,
                segment.y0,
                segment.x1,
                segment.y1,
                segment.width0,
                segment.width1,
                BARK,
                BARK,
            )

        painter.additive_blend()
        rim_rgb = BARK_RIM[:3]
        glow = (rim_rgb[0], rim_rgb[1], rim_rgb[2], 0.07)
        for segment in self.segments:
            if segment.width0 < 2.5:
                continue
            painter.tapered_segment(
                segment.x0,
                segment.y0,
                segment.x1,
                segment.y1,
                segment.width0 * 0.35,
                segment.width1 * 0.35,
                glow,
                glow,
            )
