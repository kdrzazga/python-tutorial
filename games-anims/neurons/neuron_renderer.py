import pygame


class NeuronRenderer:
    def __init__(self, glow_sprite_factory, core_color, halo_color, depth_fade_start_distance, depth_fade_end_distance):
        self.glow_sprite_factory = glow_sprite_factory
        self.core_color = core_color
        self.halo_color = halo_color
        self.depth_fade_start_distance = depth_fade_start_distance
        self.depth_fade_end_distance = depth_fade_end_distance

    def depth_fade_factor(self, depth_from_viewer):
        if depth_from_viewer <= self.depth_fade_start_distance:
            return 1.0
        if depth_from_viewer >= self.depth_fade_end_distance:
            return 0.15
        fade_span = self.depth_fade_end_distance - self.depth_fade_start_distance
        return 1.0 - 0.85 * (depth_from_viewer - self.depth_fade_start_distance) / fade_span

    def render_all_neurons(self, target_surface, neural_network, projected_points_by_neuron):
        for neuron in neural_network.neurons:
            self.render_single_neuron(target_surface, projected_points_by_neuron[neuron], neuron)

    def render_single_neuron(self, target_surface, projected_point, neuron):
        if not projected_point.is_in_front_of_viewer:
            return
        brightness = neuron.current_brightness()
        depth_fade = self.depth_fade_factor(projected_point.depth_from_viewer)
        halo_radius = neuron.current_radius() * projected_point.projected_scale * 3.2
        core_radius = neuron.current_radius() * projected_point.projected_scale * 1.1
        halo_glow = self.glow_sprite_factory.create_colored_glow(halo_radius, self.halo_color, brightness * 0.6 * depth_fade)
        core_glow = self.glow_sprite_factory.create_colored_glow(core_radius, self.core_color, brightness * depth_fade)
        self.blit_glow_centered(target_surface, halo_glow, projected_point)
        self.blit_glow_centered(target_surface, core_glow, projected_point)

    def blit_glow_centered(self, target_surface, glow_surface, projected_point):
        half_width = glow_surface.get_width() / 2.0
        half_height = glow_surface.get_height() / 2.0
        target_surface.blit(
            glow_surface,
            (projected_point.screen_x - half_width, projected_point.screen_y - half_height),
            special_flags=pygame.BLEND_RGB_ADD,
        )
