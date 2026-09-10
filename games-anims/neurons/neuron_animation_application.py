import random

import pygame

from perspective_projector import PerspectiveProjector
from world_rotation import WorldRotation
from glow_sprite_factory import GlowSpriteFactory
from neuron_renderer import NeuronRenderer
from synapse_renderer import SynapseRenderer
from scene_renderer import SceneRenderer
from neural_network import NeuralNetwork


class NeuronAnimationApplication:
    def __init__(self, configuration):
        self.configuration = configuration
        self.random_generator = random.Random()
        self.is_running = False
        self.display_surface = None
        self.frame_clock = None
        self.world_rotation = None
        self.neural_network = None
        self.scene_renderer = None

    def initialize(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.configuration.window_width, self.configuration.window_height))
        pygame.display.set_caption(self.configuration.window_title)
        self.frame_clock = pygame.time.Clock()
        self.neural_network = NeuralNetwork(self.configuration, self.random_generator)
        glow_sprite_factory = GlowSpriteFactory(self.configuration.glow_sprite_resolution, self.configuration.glow_edge_falloff_power)
        perspective_projector = PerspectiveProjector(
            self.configuration.window_width,
            self.configuration.window_height,
            self.configuration.focal_length,
            self.configuration.viewer_distance,
        )
        self.world_rotation = WorldRotation(self.configuration.world_yaw_rotation_speed, self.configuration.world_pitch_rotation_speed)
        neuron_renderer = NeuronRenderer(
            glow_sprite_factory,
            self.configuration.neuron_core_color,
            self.configuration.neuron_halo_color,
            self.configuration.depth_fade_start_distance,
            self.configuration.depth_fade_end_distance,
        )
        synapse_renderer = SynapseRenderer(
            glow_sprite_factory,
            self.configuration.synapse_line_color,
            self.configuration.signal_pulse_color,
            self.configuration.signal_pulse_glow_radius,
            self.configuration.depth_fade_start_distance,
            self.configuration.depth_fade_end_distance,
        )
        self.scene_renderer = SceneRenderer(perspective_projector, self.world_rotation, neuron_renderer, synapse_renderer)

    def run(self):
        self.initialize()
        self.is_running = True
        while self.is_running:
            elapsed_seconds = min(
                self.frame_clock.tick(self.configuration.target_frames_per_second) / 1000.0,
                self.configuration.maximum_elapsed_seconds_per_frame,
            )
            self.process_events()
            self.update(elapsed_seconds)
            self.render_frame()
        pygame.quit()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_running = False

    def update(self, elapsed_seconds):
        self.world_rotation.advance(elapsed_seconds)
        self.neural_network.advance(elapsed_seconds)

    def render_frame(self):
        self.display_surface.fill(self.configuration.background_color)
        self.scene_renderer.render(self.display_surface, self.neural_network)
        pygame.display.flip()
