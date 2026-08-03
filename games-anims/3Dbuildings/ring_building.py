import math

from building_floor import BuildingFloor
from color_palette import BuildingColorPalette
from ground_plane import GroundPlane
from illumination_scheme import WindowIlluminationScheme
from linear_algebra import point_on_circular_ring
from staircase_shaft import StaircaseShaft


class RingBuilding:
    def __init__(self, outer_radius=18.0, wall_depth=3.0, upper_floor_count=8,
                 upper_floor_height=2.4, ground_floor_height=4.4, upper_segment_count=48,
                 ground_segment_count=24, pillar_availability=True,
                 pillar_placement_angle=0.0, palette=None, illumination_scheme=None,
                 ground_window_margin_ratio=0.05, ground_window_sill_ratio=0.10,
                 upper_window_margin_ratio=0.16, upper_window_sill_ratio=0.18):
        self.outer_radius = outer_radius
        self.wall_depth = wall_depth
        self.pillar_availability = pillar_availability
        self.palette = palette if palette is not None else BuildingColorPalette()
        illumination = illumination_scheme if illumination_scheme is not None else WindowIlluminationScheme()
        self.total_height = ground_floor_height + upper_floor_count * upper_floor_height
        self.floors = self.build_stacked_floors(
            upper_floor_count, upper_floor_height, ground_floor_height, upper_segment_count,
            ground_segment_count, illumination, ground_window_margin_ratio,
            ground_window_sill_ratio, upper_window_margin_ratio, upper_window_sill_ratio)
        self.roof_ring_quads = self.build_roof_ring_quads(upper_segment_count)
        self.ground_plane = GroundPlane()
        self.staircase_shaft = self.build_staircase_shaft(pillar_placement_angle, upper_floor_count)

    def build_stacked_floors(self, upper_floor_count, upper_floor_height, ground_floor_height,
                             upper_segment_count, ground_segment_count, illumination,
                             ground_window_margin_ratio, ground_window_sill_ratio,
                             upper_window_margin_ratio, upper_window_sill_ratio):
        stacked_floors = [BuildingFloor(
            0, 0.0, ground_floor_height, ground_segment_count, self.outer_radius,
            self.wall_depth, ground_window_margin_ratio, ground_window_sill_ratio, illumination)]
        for upper_index in range(upper_floor_count):
            bottom_height = ground_floor_height + upper_index * upper_floor_height
            top_height = bottom_height + upper_floor_height
            stacked_floors.append(BuildingFloor(
                upper_index + 1, bottom_height, top_height, upper_segment_count,
                self.outer_radius, self.wall_depth, upper_window_margin_ratio,
                upper_window_sill_ratio, illumination))
        return tuple(stacked_floors)

    def build_roof_ring_quads(self, segment_count):
        constructed_quads = []
        full_revolution = 2.0 * math.pi
        inner_radius = self.outer_radius - self.wall_depth
        for segment_index in range(segment_count):
            start_angle = full_revolution * segment_index / segment_count
            end_angle = full_revolution * (segment_index + 1) / segment_count
            constructed_quads.append((
                point_on_circular_ring(self.outer_radius, start_angle, self.total_height),
                point_on_circular_ring(self.outer_radius, end_angle, self.total_height),
                point_on_circular_ring(inner_radius, end_angle, self.total_height),
                point_on_circular_ring(inner_radius, start_angle, self.total_height),
            ))
        return tuple(constructed_quads)

    def build_staircase_shaft(self, placement_angle, upper_floor_count):
        return StaircaseShaft(
            ring_outer_radius=self.outer_radius,
            placement_angle=placement_angle,
            tangential_width=6.0,
            radial_depth=4.5,
            total_height=self.total_height + 3.0,
            window_row_count=upper_floor_count + 2,
            palette=self.palette)

    def render_using(self, renderer):
        self.ground_plane.render_using(renderer, self.palette)
        for floor in self.floors:
            floor.render_using(renderer, self.palette)
        for quad in self.roof_ring_quads:
            renderer.render_shaded_quad(quad, self.palette.roof_color)
        if self.pillar_availability:
            self.staircase_shaft.render_using(renderer, self.palette)
