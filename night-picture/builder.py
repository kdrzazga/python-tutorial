import random

from app import App
from elements.cloud import Cloud, CloudBank
from elements.firefly import Swarm
from elements.flower import Garden
from elements.moon import Moon
from elements.moon_shade import MoonShade
from elements.sky import Sky, Vignette
from elements.soil import Soil
from elements.star import StarField
from elements.tree import Crown, Tree
from elements.vine import Vines
from elements.water import Water
from palette import BACKGROUND, CLOUD, NIGHT_HORIZON, NIGHT_TOP, VIGNETTE
from scene import Scene
from terrain import Terrain


class NightPicBuilder:
    def __init__(self, width=1280, height=720, seed=7):
        self.width = width
        self.height = height
        self.seed = seed
        self.rng = random.Random(seed)
        self.background = BACKGROUND
        self.tree_anchor_x = 700.0
        self.terrain = Terrain(
            edge_x=590.0,
            right_x=float(width),
            back_height=310.0,
            front_height=48.0,
            curve=1.0,
        )

        self.sky = None
        self.star_count = None
        self.moon_enabled = False
        self.moon_center_x = 340.0
        self.moon_center_y = 470.0
        self.moon_radius = 150.0
        self.moon_blaze = False
        self.moon_blaze_intensity = 1.0
        self.moon_blaze_scale = 1.0
        self.moon_shade_enabled = False
        self.moon_shade_size = 200.0
        self.cloud_count = None
        self.water_enabled = False
        self.waterline = 310.0
        self.soil_enabled = False
        self.tree_specs = ()
        self.flower_spec = None
        self.firefly_count = None
        self.vignette_strength = None

    def _to_gl_y(self, top_left_y):
        return self.height - top_left_y

    def with_seed(self, seed):
        self.seed = seed
        self.rng = random.Random(seed)
        return self

    def with_background(self, color):
        self.background = color
        return self

    def with_sky(self, top_color=NIGHT_TOP, horizon_color=NIGHT_HORIZON):
        self.sky = (horizon_color, top_color)
        return self

    def with_stars(self, count=150):
        self.star_count = count
        return self

    def with_moon(self, radius=150.0, center_x=340.0, center_y=250.0):
        self.moon_enabled = True
        self.moon_radius = radius
        self.moon_center_x = center_x
        self.moon_center_y = self._to_gl_y(center_y)
        return self

    def with_moon_blaze(self, intensity=1.0, scale=1.0):
        self.moon_enabled = True
        self.moon_blaze = True
        self.moon_blaze_intensity = intensity
        self.moon_blaze_scale = scale
        return self

    def with_moon_shade(self, size=200.0):
        self.moon_shade_enabled = True
        self.moon_shade_size = size
        return self

    def with_clouds(self, count=4):
        self.cloud_count = count
        return self

    def with_water(self, waterline=410.0):
        self.water_enabled = True
        self.waterline = self._to_gl_y(waterline)
        return self

    def with_ground(self, edge_x=590.0, back_y=410.0, front_y=672.0, curve=1.0):
        self.terrain = Terrain(
            edge_x=edge_x,
            right_x=float(self.width),
            back_height=self._to_gl_y(back_y),
            front_height=self._to_gl_y(front_y),
            curve=curve,
        )
        self.soil_enabled = True
        return self

    def with_trees(self, count=1, crown_scale=1.0, vines_per_tree=14):
        specs = []
        left = max(self.terrain.edge_x + 40.0, self.tree_anchor_x)
        right = self.terrain.right_x - 140.0
        for _ in range(count):
            base_x = self.rng.uniform(left, right)
            base_y = self.terrain.height_at(base_x)
            trunk_length = 82.0 * self.rng.uniform(0.85, 1.15)
            trunk_width = 15.0 * self.rng.uniform(0.9, 1.1)
            lean = self.rng.uniform(-0.20, 0.05)
            crown_radius = 175.0 * crown_scale * self.rng.uniform(0.85, 1.1)
            specs.append((base_x, base_y, trunk_length, trunk_width, lean, crown_radius, vines_per_tree))
        self.tree_specs = tuple(specs)
        return self

    def with_flowers(self, count=10, sparks=200):
        self.flower_spec = (count, sparks)
        return self

    def with_fireflies(self, count=30):
        self.firefly_count = count
        return self

    def with_vignette(self, strength=0.82):
        self.vignette_strength = strength
        return self

    def _make_clouds(self, count):
        clouds = []
        for _ in range(count):
            base_y = self.rng.uniform(self.height * 0.5, self.height * 0.9)
            thickness = self.rng.uniform(45.0, 120.0)
            opacity = self.rng.uniform(0.3, 0.5)
            drift = self.rng.uniform(0.05, 0.14)
            terms = (
                (self.rng.uniform(18.0, 34.0), self.rng.uniform(0.005, 0.008), self.rng.uniform(0.0, 6.28)),
                (self.rng.uniform(9.0, 15.0), self.rng.uniform(0.015, 0.022), self.rng.uniform(0.0, 6.28)),
                (self.rng.uniform(4.0, 7.0), self.rng.uniform(0.030, 0.037), self.rng.uniform(0.0, 6.28)),
            )
            clouds.append(Cloud(base_y, thickness, CLOUD, opacity, terms, drift, (0.0, float(self.width))))
        return clouds

    def build(self):
        elements = []

        if self.sky is not None:
            elements.append(Sky(self.width, self.height, self.sky[0], self.sky[1]))

        if self.star_count is not None:
            elements.append(
                StarField(
                    self.width,
                    self.height,
                    self.star_count,
                    self.rng,
                    self.moon_center_x,
                    self.moon_center_y,
                    230.0,
                    self.waterline,
                )
            )

        if self.moon_enabled:
            elements.append(
                Moon(
                    self.moon_center_x,
                    self.moon_center_y,
                    self.moon_radius,
                    self.rng,
                    self.moon_blaze,
                    self.moon_blaze_intensity,
                    self.moon_blaze_scale,
                )
            )

        if self.cloud_count is not None:
            elements.append(CloudBank(self._make_clouds(self.cloud_count)))

        if self.water_enabled:
            elements.append(Water(self.width, self.waterline, self.rng))

        if self.moon_shade_enabled:
            elements.append(MoonShade(self.moon_center_x, self.waterline, self.moon_shade_size))

        if self.soil_enabled:
            elements.append(Soil(self.terrain, self.width))

        for base_x, base_y, trunk_length, trunk_width, lean, crown_radius, vines_per_tree in self.tree_specs:
            crown_x = base_x - 15.0
            crown_y = base_y + 185.0
            elements.append(Crown(crown_x, crown_y, crown_radius, self.rng))
            elements.append(Tree(base_x, base_y, trunk_length, trunk_width, self.rng, lean))
            if vines_per_tree > 0:
                elements.append(
                    Vines(crown_x + 20.0, crown_y - crown_radius * 0.55, crown_radius * 0.9, vines_per_tree, self.rng)
                )

        if self.flower_spec is not None:
            flower_count, spark_count = self.flower_spec
            elements.append(Garden(self.terrain, self.width, self.rng, flower_count, spark_count))

        if self.firefly_count is not None:
            elements.append(
                Swarm(620.0, 60.0, self.width - 640.0, 340.0, self.firefly_count, self.rng)
            )

        if self.vignette_strength is not None:
            elements.append(Vignette(self.width, self.height, VIGNETTE, self.vignette_strength))

        return Scene(self.width, self.height, elements, self.background)

    def run(self, title="Night Picture"):
        App(self.build(), title).run()

    @classmethod
    def default(cls, width=1280, height=720, seed=7):
        return (
            cls(width, height, seed)
            .with_sky()
            .with_stars()
            .with_moon()
            .with_moon_blaze()
            .with_moon_shade()
            .with_clouds()
            .with_water()
            .with_ground()
            .with_trees()
            .with_flowers()
            .with_fireflies()
            .with_vignette()
        )
