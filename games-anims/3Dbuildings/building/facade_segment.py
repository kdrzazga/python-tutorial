from .window_panel import WindowPanel


class FacadeSegment:
    def __init__(self, start_angle, end_angle, bottom_height, top_height,
                 outer_footprint, inner_footprint, window_footprint,
                 window_margin_ratio, window_sill_ratio, is_illuminated):
        self.outer_wall_corners = self.build_outer_facing_wall(
            outer_footprint, start_angle, end_angle, bottom_height, top_height)
        self.inner_wall_corners = self.build_courtyard_facing_wall(
            inner_footprint, start_angle, end_angle, bottom_height, top_height)
        self.window_panel = self.build_window_panel(
            window_footprint, start_angle, end_angle, bottom_height, top_height,
            window_margin_ratio, window_sill_ratio, is_illuminated)

    def build_outer_facing_wall(self, footprint, start_angle, end_angle, bottom_height, top_height):
        return (
            footprint.perimeter_point(start_angle, bottom_height),
            footprint.perimeter_point(end_angle, bottom_height),
            footprint.perimeter_point(end_angle, top_height),
            footprint.perimeter_point(start_angle, top_height),
        )

    def build_courtyard_facing_wall(self, footprint, start_angle, end_angle, bottom_height, top_height):
        return (
            footprint.perimeter_point(end_angle, bottom_height),
            footprint.perimeter_point(start_angle, bottom_height),
            footprint.perimeter_point(start_angle, top_height),
            footprint.perimeter_point(end_angle, top_height),
        )

    def build_window_panel(self, footprint, start_angle, end_angle, bottom_height, top_height,
                           window_margin_ratio, window_sill_ratio, is_illuminated):
        angular_span = end_angle - start_angle
        window_start_angle = start_angle + angular_span * window_margin_ratio
        window_end_angle = end_angle - angular_span * window_margin_ratio
        vertical_span = top_height - bottom_height
        window_bottom_height = bottom_height + vertical_span * window_sill_ratio
        window_top_height = top_height - vertical_span * window_sill_ratio
        corner_points = (
            footprint.perimeter_point(window_start_angle, window_bottom_height),
            footprint.perimeter_point(window_end_angle, window_bottom_height),
            footprint.perimeter_point(window_end_angle, window_top_height),
            footprint.perimeter_point(window_start_angle, window_top_height),
        )
        return WindowPanel(corner_points, is_illuminated)

    def render_using(self, renderer, palette):
        renderer.render_shaded_quad(self.outer_wall_corners, palette.facade_color)
        renderer.render_shaded_quad(self.inner_wall_corners, palette.courtyard_wall_color)
        self.window_panel.render_using(renderer, palette)
