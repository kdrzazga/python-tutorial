import math

from elements.element import Element
from palette import FLOWER_GLOW, FLOWER_HEART, PETAL_CORE, PETAL_TIP, VINE


class Petal:
    def __init__(self, length, width, angle, resolution=14):
        self.length = length
        self.width = width
        self.angle = angle
        self.outline = tuple(self._build_outline(resolution))

    def _build_outline(self, resolution):
        points = []
        for index in range(resolution + 1):
            u = index / resolution
            half = self.width * math.sin(math.pi * u) ** 0.7
            points.append((-half, u * self.length))
        for index in range(resolution + 1):
            u = 1.0 - index / resolution
            half = self.width * math.sin(math.pi * u) ** 0.7
            points.append((half, u * self.length))
        return points

    def render(self, painter, center_x, center_y, scale, brightness):
        cosine = math.cos(self.angle)
        sine = math.sin(self.angle)
        transformed = []
        for local_x, local_y in self.outline:
            scaled_x = local_x * scale
            scaled_y = local_y * scale
            rotated_x = scaled_x * cosine - scaled_y * sine
            rotated_y = scaled_x * sine + scaled_y * cosine
            transformed.append((center_x + rotated_x, center_y + rotated_y))
        core = (PETAL_CORE[0], PETAL_CORE[1], PETAL_CORE[2], PETAL_CORE[3] * brightness)
        tip = (PETAL_TIP[0], PETAL_TIP[1], PETAL_TIP[2], PETAL_TIP[3] * brightness * 0.4)
        painter.fan(center_x, center_y, transformed, core, tip)


class Flower:
    def __init__(self, x, y, scale, petal_count, rng, phase):
        self.x = x
        self.y = y
        self.scale = scale
        self.phase = phase
        self.pulse_speed = rng.uniform(1.2, 2.4)
        self.petals = tuple(self._build_petals(petal_count, rng))

    def _build_petals(self, petal_count, rng):
        petals = []
        base_length = 26.0
        base_width = 9.0
        for index in range(petal_count):
            angle = 2.0 * math.pi * index / petal_count + rng.uniform(-0.12, 0.12)
            length = base_length * rng.uniform(0.85, 1.15)
            width = base_width * rng.uniform(0.85, 1.15)
            petals.append(Petal(length, width, angle))
        return petals

    def render(self, painter, time):
        pulse = 0.7 + 0.3 * math.sin(time * self.pulse_speed + self.phase)
        painter.additive_blend()

        glow_rgb = FLOWER_GLOW[:3]
        painter.glow_dot(
            self.x,
            self.y,
            self.scale * 46.0,
            (glow_rgb[0], glow_rgb[1], glow_rgb[2], 0.35 * pulse),
            24,
        )

        for petal in self.petals:
            petal.render(painter, self.x, self.y, self.scale, pulse)

        heart_rgb = FLOWER_HEART[:3]
        painter.glow_dot(
            self.x,
            self.y,
            self.scale * 8.0,
            (heart_rgb[0], heart_rgb[1], heart_rgb[2], 0.9 * pulse),
            16,
        )


class Garden(Element):
    def __init__(self, terrain, right_x, rng, flower_count=70, spark_count=260):
        self.flowers = tuple(self._plant(terrain, right_x, rng, flower_count))
        self.sparks = tuple(self._scatter_sparks(terrain, right_x, rng, spark_count))

    def _plant(self, terrain, right_x, rng, count):
        flowers = []
        for _ in range(count):
            x = rng.uniform(terrain.edge_x + 20.0, right_x - 6.0)
            surface = terrain.height_at(x)
            y = surface - rng.uniform(2.0, 52.0)
            front = (x - terrain.edge_x) / (right_x - terrain.edge_x)
            scale = (0.35 + 1.05 * front) * rng.uniform(0.7, 1.25)
            petal_count = rng.choice((5, 5, 6))
            phase = rng.uniform(0.0, 2.0 * math.pi)
            flowers.append(Flower(x, y, scale, petal_count, rng, phase))
        flowers.sort(key=lambda flower: flower.y, reverse=True)
        return flowers

    def _scatter_sparks(self, terrain, right_x, rng, count):
        sparks = []
        for _ in range(count):
            x = rng.uniform(terrain.edge_x + 10.0, right_x - 2.0)
            surface = terrain.height_at(x)
            y = surface - rng.uniform(0.0, 70.0)
            size = rng.uniform(1.0, 2.6)
            phase = rng.uniform(0.0, 2.0 * math.pi)
            speed = rng.uniform(1.0, 2.8)
            brightness = rng.uniform(0.3, 0.8)
            sparks.append((x, y, size, phase, speed, brightness))
        return sparks

    def render(self, painter, time):
        painter.additive_blend()
        spark_rgb = VINE[:3]
        for x, y, size, phase, speed, brightness in self.sparks:
            twinkle = 0.4 + 0.6 * math.sin(time * speed + phase)
            painter.glow_dot(x, y, size, (spark_rgb[0], spark_rgb[1], spark_rgb[2], brightness * twinkle), 8)

        for flower in self.flowers:
            flower.render(painter, time)
