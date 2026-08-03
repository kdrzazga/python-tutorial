from building_floor import BuildingFloor
from color_palette import BuildingColorPalette
from elliptical_footprint import EllipticalFootprint
from ground_plane import GroundPlane
from illumination_scheme import WindowIlluminationScheme
from staircase_shaft import StaircaseShaft


class RingBuilding:
    def __init__(self, outer_semi_width=30.0, outer_semi_depth=7.5, wall_depth=3.0,
                 upper_floor_count=8, upper_floor_height=2.4, ground_floor_height=4.4,
                 upper_segment_count=64, ground_segment_count=32, pillar_availability=True,
                 pillar_placement_angle=0.9, palette=None, illumination_scheme=None,
                 window_protrusion=0.1, ground_window_margin_ratio=0.05,
                 ground_window_sill_ratio=0.10, upper_window_margin_ratio=0.16,
                 upper_window_sill_ratio=0.18):
        self.pillar_availability = pillar_availability
        self.palette = palette if palette is not None else BuildingColorPalette()
        illumination = illumination_scheme if illumination_scheme is not None else WindowIlluminationScheme()
        self.outer_footprint = EllipticalFootprint(outer_semi_width, outer_semi_depth)
        self.inner_footprint = self.outer_footprint.resized_by(-wall_depth)
        self.window_footprint = self.outer_footprint.resized_by(window_protrusion)
        self.total_height = ground_floor_height + upper_floor_count * upper_floor_height
        self.upper_boundary_angles = self.outer_footprint.evenly_spaced_boundary_angles(upper_segment_count)
        self.ground_boundary_angles = self.outer_footprint.evenly_spaced_boundary_angles(ground_segment_count)
        self.floors = self.build_stacked_floors(
            upper_floor_count, upper_floor_height, ground_floor_height, illumination,
            ground_window_margin_ratio, ground_window_sill_ratio,
            upper_window_margin_ratio, upper_window_sill_ratio)
        self.roof_ring_quads = self.build_roof_ring_quads()
        self.ground_plane = GroundPlane()
        self.staircase_shaft = self.build_staircase_shaft(pillar_placement_angle, upper_floor_count)

    def build_stacked_floors(self, upper_floor_count, upper_floor_height, ground_floor_height,
                             illumination, ground_window_margin_ratio, ground_window_sill_ratio,
                             upper_window_margin_ratio, upper_window_sill_ratio):
        stacked_floors = [BuildingFloor(
            0, 0.0, ground_floor_height, self.ground_boundary_angles, self.outer_footprint,
            self.inner_footprint, self.window_footprint, ground_window_margin_ratio,
            ground_window_sill_ratio, illumination)]
        for upper_index in range(upper_floor_count):
            bottom_height = ground_floor_height + upper_index * upper_floor_height
            top_height = bottom_height + upper_floor_height
            stacked_floors.append(BuildingFloor(
                upper_index + 1, bottom_height, top_height, self.upper_boundary_angles,
                self.outer_footprint, self.inner_footprint, self.window_footprint,
                upper_window_margin_ratio, upper_window_sill_ratio, illumination))
        return tuple(stacked_floors)

    def build_roof_ring_quads(self):
        constructed_quads = []
        boundary_angles = self.upper_boundary_angles
        for segment_index in range(len(boundary_angles) - 1):
            start_angle = boundary_angles[segment_index]
            end_angle = boundary_angles[segment_index + 1]
            constructed_quads.append((
                self.outer_footprint.perimeter_point(start_angle, self.total_height),
                self.outer_footprint.perimeter_point(end_angle, self.total_height),
                self.inner_footprint.perimeter_point(end_angle, self.total_height),
                self.inner_footprint.perimeter_point(start_angle, self.total_height),
            ))
        return tuple(constructed_quads)

    def build_staircase_shaft(self, placement_angle, upper_floor_count):
        anchor_point = self.outer_footprint.perimeter_point(placement_angle, 0.0)
        outward_normal = self.outer_footprint.outward_normal_at(placement_angle)
        tangent_direction = self.outer_footprint.tangent_at(placement_angle)
        return StaircaseShaft(
            anchor_point=anchor_point,
            outward_normal=outward_normal,
            tangent_direction=tangent_direction,
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
