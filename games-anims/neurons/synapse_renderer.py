import pygame


class SynapseRenderer:
    def __init__(self, glow_sprite_factory, synapse_line_color, signal_pulse_color, signal_pulse_glow_radius, depth_fade_start_distance, depth_fade_end_distance):
        self.glow_sprite_factory = glow_sprite_factory
        self.synapse_line_color = synapse_line_color
        self.signal_pulse_color = signal_pulse_color
        self.signal_pulse_glow_radius = signal_pulse_glow_radius
        self.depth_fade_start_distance = depth_fade_start_distance
        self.depth_fade_end_distance = depth_fade_end_distance

    def depth_fade_factor(self, depth_from_viewer):
        if depth_from_viewer <= self.depth_fade_start_distance:
            return 1.0
        if depth_from_viewer >= self.depth_fade_end_distance:
            return 0.15
        fade_span = self.depth_fade_end_distance - self.depth_fade_start_distance
        return 1.0 - 0.85 * (depth_from_viewer - self.depth_fade_start_distance) / fade_span

    def render_all_synapse_lines(self, target_surface, neural_network, projected_points_by_neuron):
        for synapse in neural_network.synapses:
            source_point = projected_points_by_neuron[synapse.source_neuron]
            target_point = projected_points_by_neuron[synapse.target_neuron]
            if not source_point.is_in_front_of_viewer or not target_point.is_in_front_of_viewer:
                continue
            activity_level = min(1.0, 0.22 + 0.7 * len(synapse.travelling_pulses))
            average_depth = (source_point.depth_from_viewer + target_point.depth_from_viewer) / 2.0
            depth_fade = self.depth_fade_factor(average_depth)
            line_color = (
                int(self.synapse_line_color[0] * activity_level * depth_fade),
                int(self.synapse_line_color[1] * activity_level * depth_fade),
                int(self.synapse_line_color[2] * activity_level * depth_fade),
            )
            pygame.draw.line(
                target_surface,
                line_color,
                (int(source_point.screen_x), int(source_point.screen_y)),
                (int(target_point.screen_x), int(target_point.screen_y)),
                1,
            )

    def render_all_travelling_pulses(self, target_surface, neural_network, world_rotation, perspective_projector):
        for synapse in neural_network.synapses:
            for pulse in synapse.travelling_pulses:
                rotated_position = world_rotation.apply_to(synapse.pulse_world_position(pulse))
                projected_point = perspective_projector.project(rotated_position)
                if not projected_point.is_in_front_of_viewer:
                    continue
                depth_fade = self.depth_fade_factor(projected_point.depth_from_viewer)
                glow_radius = self.signal_pulse_glow_radius * projected_point.projected_scale
                pulse_glow = self.glow_sprite_factory.create_colored_glow(glow_radius, self.signal_pulse_color, depth_fade)
                half_extent = pulse_glow.get_width() / 2.0
                target_surface.blit(
                    pulse_glow,
                    (projected_point.screen_x - half_extent, projected_point.screen_y - half_extent),
                    special_flags=pygame.BLEND_RGB_ADD,
                )
