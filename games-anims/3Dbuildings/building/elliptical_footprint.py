import math

from linear_algebra import Vector3


class EllipticalFootprint:
    def __init__(self, semi_width, semi_depth):
        self.semi_width = semi_width
        self.semi_depth = semi_depth

    def perimeter_point(self, angle, height):
        return Vector3(self.semi_width * math.cos(angle), height, self.semi_depth * math.sin(angle))

    def outward_normal_at(self, angle):
        return Vector3(math.cos(angle) / self.semi_width, 0.0, math.sin(angle) / self.semi_depth).normalized()

    def tangent_at(self, angle):
        return Vector3(-self.semi_width * math.sin(angle), 0.0, self.semi_depth * math.cos(angle)).normalized()

    def resized_by(self, offset):
        return EllipticalFootprint(self.semi_width + offset, self.semi_depth + offset)

    def evenly_spaced_boundary_angles(self, segment_count, sample_count=2000):
        full_revolution = 2.0 * math.pi
        sampled_angles = tuple(full_revolution * index / sample_count for index in range(sample_count + 1))
        cumulative_lengths = [0.0]
        for index in range(1, sample_count + 1):
            previous_point = self.perimeter_point(sampled_angles[index - 1], 0.0)
            current_point = self.perimeter_point(sampled_angles[index], 0.0)
            step_length = math.hypot(current_point.x - previous_point.x, current_point.z - previous_point.z)
            cumulative_lengths.append(cumulative_lengths[-1] + step_length)
        total_length = cumulative_lengths[-1]
        boundary_angles = []
        sample_cursor = 0
        for boundary_index in range(segment_count + 1):
            target_length = total_length * boundary_index / segment_count
            while sample_cursor < sample_count and cumulative_lengths[sample_cursor + 1] < target_length:
                sample_cursor += 1
            lower_length = cumulative_lengths[sample_cursor]
            upper_length = cumulative_lengths[sample_cursor + 1]
            occupied_span = upper_length - lower_length
            interpolation_fraction = 0.0 if occupied_span == 0.0 else (target_length - lower_length) / occupied_span
            lower_angle = sampled_angles[sample_cursor]
            upper_angle = sampled_angles[sample_cursor + 1]
            boundary_angles.append(lower_angle + interpolation_fraction * (upper_angle - lower_angle))
        return tuple(boundary_angles)
