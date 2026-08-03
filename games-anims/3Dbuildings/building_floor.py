import math

from facade_segment import FacadeSegment


class BuildingFloor:
    def __init__(self, floor_index, bottom_height, top_height, segment_count,
                 outer_radius, wall_depth, window_margin_ratio, window_sill_ratio,
                 illumination_scheme):
        self.floor_index = floor_index
        self.segments = self.build_encircling_segments(
            bottom_height, top_height, segment_count, outer_radius, wall_depth,
            window_margin_ratio, window_sill_ratio, illumination_scheme)

    def build_encircling_segments(self, bottom_height, top_height, segment_count, outer_radius,
                                  wall_depth, window_margin_ratio, window_sill_ratio,
                                  illumination_scheme):
        constructed_segments = []
        full_revolution = 2.0 * math.pi
        for segment_index in range(segment_count):
            start_angle = full_revolution * segment_index / segment_count
            end_angle = full_revolution * (segment_index + 1) / segment_count
            is_illuminated = illumination_scheme.is_window_illuminated(self.floor_index, segment_index)
            constructed_segments.append(FacadeSegment(
                start_angle, end_angle, bottom_height, top_height, outer_radius,
                wall_depth, window_margin_ratio, window_sill_ratio, is_illuminated))
        return tuple(constructed_segments)

    def render_using(self, renderer, palette):
        for segment in self.segments:
            segment.render_using(renderer, palette)
