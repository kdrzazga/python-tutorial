import math

from linear_algebra import Vector3


class StaircaseShaft:
    def __init__(self, ring_outer_radius, placement_angle, tangential_width,
                 radial_depth, total_height, window_row_count, palette):
        self.palette = palette
        self.radial_direction = Vector3(math.cos(placement_angle), 0.0, math.sin(placement_angle))
        self.tangential_direction = Vector3(-math.sin(placement_angle), 0.0, math.cos(placement_angle))
        self.body_faces = self.build_body_faces(
            ring_outer_radius, tangential_width, radial_depth, total_height)
        self.window_quads = self.build_stairwell_window_quads(
            ring_outer_radius, tangential_width, radial_depth, total_height, window_row_count)

    def horizontal_point_at(self, radius, lateral_offset, height):
        horizontal = self.radial_direction.scaled_by(radius).added_to(
            self.tangential_direction.scaled_by(lateral_offset))
        return Vector3(horizontal.x, height, horizontal.z)

    def build_body_faces(self, ring_outer_radius, tangential_width, radial_depth, total_height):
        half_width = tangential_width * 0.5
        back_radius = ring_outer_radius - 1.5
        front_radius = ring_outer_radius + radial_depth

        back_left_bottom = self.horizontal_point_at(back_radius, -half_width, 0.0)
        back_right_bottom = self.horizontal_point_at(back_radius, half_width, 0.0)
        front_left_bottom = self.horizontal_point_at(front_radius, -half_width, 0.0)
        front_right_bottom = self.horizontal_point_at(front_radius, half_width, 0.0)
        back_left_top = self.horizontal_point_at(back_radius, -half_width, total_height)
        back_right_top = self.horizontal_point_at(back_radius, half_width, total_height)
        front_left_top = self.horizontal_point_at(front_radius, -half_width, total_height)
        front_right_top = self.horizontal_point_at(front_radius, half_width, total_height)

        front_face = (front_left_bottom, front_right_bottom, front_right_top, front_left_top)
        back_face = (back_right_bottom, back_left_bottom, back_left_top, back_right_top)
        left_face = (back_left_bottom, front_left_bottom, front_left_top, back_left_top)
        right_face = (front_right_bottom, back_right_bottom, back_right_top, front_right_top)
        top_face = (front_left_top, front_right_top, back_right_top, back_left_top)
        return (front_face, back_face, left_face, right_face, top_face)

    def build_stairwell_window_quads(self, ring_outer_radius, tangential_width, radial_depth,
                                     total_height, window_row_count):
        front_radius = ring_outer_radius + radial_depth + 0.06
        window_half_width = tangential_width * 0.22
        constructed_quads = []
        for row_index in range(window_row_count):
            band_bottom = total_height * (row_index + 0.35) / (window_row_count + 1)
            band_top = total_height * (row_index + 0.85) / (window_row_count + 1)
            constructed_quads.append((
                self.horizontal_point_at(front_radius, -window_half_width, band_bottom),
                self.horizontal_point_at(front_radius, window_half_width, band_bottom),
                self.horizontal_point_at(front_radius, window_half_width, band_top),
                self.horizontal_point_at(front_radius, -window_half_width, band_top),
            ))
        return tuple(constructed_quads)

    def render_using(self, renderer, palette):
        for face in self.body_faces:
            renderer.render_shaded_quad(face, palette.shaft_color)
        for quad in self.window_quads:
            renderer.render_emissive_quad(quad, palette.lit_window_color)
