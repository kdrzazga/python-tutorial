from .facade_segment import FacadeSegment


class BuildingFloor:
    def __init__(self, floor_index, bottom_height, top_height, boundary_angles,
                 outer_footprint, inner_footprint, window_footprint,
                 window_margin_ratio, window_sill_ratio, illumination_scheme, color_scheme):
        self.floor_index = floor_index
        self.segments = self.build_encircling_segments(
            bottom_height, top_height, boundary_angles, outer_footprint, inner_footprint,
            window_footprint, window_margin_ratio, window_sill_ratio, illumination_scheme,
            color_scheme)

    def build_encircling_segments(self, bottom_height, top_height, boundary_angles,
                                  outer_footprint, inner_footprint, window_footprint,
                                  window_margin_ratio, window_sill_ratio, illumination_scheme,
                                  color_scheme):
        constructed_segments = []
        for segment_index in range(len(boundary_angles) - 1):
            start_angle = boundary_angles[segment_index]
            end_angle = boundary_angles[segment_index + 1]
            is_illuminated = illumination_scheme.is_window_illuminated(self.floor_index, segment_index)
            wall_color = color_scheme.facade_color_at(self.floor_index, segment_index)
            window_color = color_scheme.window_color_at(self.floor_index, segment_index, is_illuminated)
            constructed_segments.append(FacadeSegment(
                start_angle, end_angle, bottom_height, top_height, outer_footprint,
                inner_footprint, window_footprint, window_margin_ratio, window_sill_ratio,
                wall_color, window_color))
        return tuple(constructed_segments)

    def render_using(self, renderer, palette):
        for segment in self.segments:
            segment.render_using(renderer, palette)
