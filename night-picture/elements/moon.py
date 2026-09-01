import math

from elements.element import Element
from palette import MARIA, MOON_CORE, MOON_EDGE, MOON_HALO, MOON_RIM


class Moon(Element):
    def __init__(self, center_x, center_y, radius, rng, blaze=False, blaze_intensity=1.0, blaze_scale=1.0, maria_count=8):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.blaze = blaze
        self.blaze_intensity = blaze_intensity
        self.blaze_scale = blaze_scale
        self.maria = tuple(self._scatter_maria(rng, maria_count))

    def _scatter_maria(self, rng, count):
        spots = []
        for _ in range(count):
            angle = rng.uniform(0.0, 2.0 * math.pi)
            distance = rng.uniform(0.0, self.radius * 0.68)
            spot_radius = rng.uniform(self.radius * 0.14, self.radius * 0.34)
            spots.append(
                (
                    self.center_x + math.cos(angle) * distance,
                    self.center_y + math.sin(angle) * distance,
                    spot_radius,
                )
            )
        return spots

    def render(self, painter, time):
        if self.blaze:
            breathing = 0.9 + 0.1 * math.sin(time * 0.6)
            halo_rgb = MOON_HALO[:3]
            painter.additive_blend()
            painter.radial(
                self.center_x,
                self.center_y,
                self.radius * 3.7 * self.blaze_scale,
                (halo_rgb[0], halo_rgb[1], halo_rgb[2], 0.28 * self.blaze_intensity * breathing),
                (halo_rgb[0], halo_rgb[1], halo_rgb[2], 0.0),
                96,
            )
            painter.radial(
                self.center_x,
                self.center_y,
                self.radius * 1.9 * self.blaze_scale,
                (halo_rgb[0], halo_rgb[1], halo_rgb[2], 0.5 * self.blaze_intensity * breathing),
                (halo_rgb[0], halo_rgb[1], halo_rgb[2], 0.0),
                96,
            )

        painter.alpha_blend()
        painter.radial(self.center_x, self.center_y, self.radius, MOON_CORE, MOON_EDGE, 96)

        maria_rgb = MARIA[:3]
        for spot_x, spot_y, spot_radius in self.maria:
            painter.radial(
                spot_x,
                spot_y,
                spot_radius,
                (maria_rgb[0], maria_rgb[1], maria_rgb[2], 0.55),
                (maria_rgb[0], maria_rgb[1], maria_rgb[2], 0.0),
                40,
            )

        rim_rgb = MOON_RIM[:3]
        painter.additive_blend()
        painter.ring(
            self.center_x,
            self.center_y,
            self.radius * 0.88,
            self.radius * 1.02,
            (rim_rgb[0], rim_rgb[1], rim_rgb[2], 0.0),
            (rim_rgb[0], rim_rgb[1], rim_rgb[2], 0.5),
            96,
        )
