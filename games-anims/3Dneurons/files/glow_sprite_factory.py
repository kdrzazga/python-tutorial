import pygame


class GlowSpriteFactory:
    def __init__(self, base_resolution, edge_falloff_power):
        self.base_resolution = base_resolution
        self.edge_falloff_power = edge_falloff_power
        self.base_glow_surface = self.build_base_glow_surface()
        self.scaled_white_glow_cache = {}

    def build_base_glow_surface(self):
        glow_surface = pygame.Surface((self.base_resolution, self.base_resolution))
        glow_surface.fill((0, 0, 0))
        center_position = int(self.base_resolution / 2)
        maximum_radius = self.base_resolution / 2.0
        radius = int(maximum_radius)
        while radius > 0:
            normalized_distance = radius / maximum_radius
            brightness = int((1.0 - normalized_distance) ** self.edge_falloff_power * 255)
            pygame.draw.circle(glow_surface, (brightness, brightness, brightness), (center_position, center_position), radius)
            radius -= 1
        return glow_surface

    def scaled_white_glow(self, glow_diameter):
        cached_surface = self.scaled_white_glow_cache.get(glow_diameter)
        if cached_surface is None:
            cached_surface = pygame.transform.smoothscale(self.base_glow_surface, (glow_diameter, glow_diameter))
            self.scaled_white_glow_cache[glow_diameter] = cached_surface
        return cached_surface

    def create_colored_glow(self, glow_radius, glow_color, glow_intensity):
        glow_diameter = max(2, int(glow_radius * 2.0))
        colored_glow = self.scaled_white_glow(glow_diameter).copy()
        clamped_intensity = max(0.0, min(1.0, glow_intensity))
        tint_color = (
            int(glow_color[0] * clamped_intensity),
            int(glow_color[1] * clamped_intensity),
            int(glow_color[2] * clamped_intensity),
        )
        colored_glow.fill(tint_color, special_flags=pygame.BLEND_RGB_MULT)
        return colored_glow
