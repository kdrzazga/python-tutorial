from linear_algebra import point_on_circular_ring
from window_panel import WindowPanel


class FacadeSegment:
    def __init__(self, start_angle, end_angle, bottom_height, top_height,
                 outer_radius, wall_depth, window_margin_ratio, window_sill_ratio,
                 is_illuminated):
        self.outer_wall_corners = self.build_outer_facing_wall(
            start_angle, end_angle, bottom_height, top_height, outer_radius)
        self.inner_wall_corners = self.build_courtyard_facing_wall(
            start_angle, end_angle, bottom_height, top_height, outer_radius - wall_depth)
        self.window_panel = self.build_window_panel(
            start_angle, end_angle, bottom_height, top_height, outer_radius,
            window_margin_ratio, window_sill_ratio, is_illuminated)

    def build_outer_facing_wall(self, start_angle, end_angle, bottom_height, top_height, radius):
        return (
            point_on_circular_ring(radius, start_angle, bottom_height),
            point_on_circular_ring(radius, end_angle, bottom_height),
            point_on_circular_ring(radius, end_angle, top_height),
            point_on_circular_ring(radius, start_angle, top_height),
        )

    def build_courtyard_facing_wall(self, start_angle, end_angle, bottom_height, top_height, radius):
        return (
            point_on_circular_ring(radius, end_angle, bottom_height),
            point_on_circular_ring(radius, start_angle, bottom_height),
            point_on_circular_ring(radius, start_angle, top_height),
            point_on_circular_ring(radius, end_angle, top_height),
        )

    def build_window_panel(self, start_angle, end_angle, bottom_height, top_height,
                           outer_radius, window_margin_ratio, window_sill_ratio, is_illuminated):
        angular_span = end_angle - start_angle
        window_start_angle = start_angle + angular_span * window_margin_ratio
        window_end_angle = end_angle - angular_span * window_margin_ratio
        vertical_span = top_height - bottom_height
        window_bottom_height = bottom_height + vertical_span * window_sill_ratio
        window_top_height = top_height - vertical_span * window_sill_ratio
        protruding_radius = outer_radius + 0.06
        corner_points = (
            point_on_circular_ring(protruding_radius, window_start_angle, window_bottom_height),
            point_on_circular_ring(protruding_radius, window_end_angle, window_bottom_height),
            point_on_circular_ring(protruding_radius, window_end_angle, window_top_height),
            point_on_circular_ring(protruding_radius, window_start_angle, window_top_height),
        )
        return WindowPanel(corner_points, is_illuminated)

    def render_using(self, renderer, palette):
        renderer.render_shaded_quad(self.outer_wall_corners, palette.facade_color)
        renderer.render_shaded_quad(self.inner_wall_corners, palette.courtyard_wall_color)
        self.window_panel.render_using(renderer, palette)
