import math


class Vector3:
    def __init__(self, x_component, y_component, z_component):
        self.x_component = x_component
        self.y_component = y_component
        self.z_component = z_component

    def subtracted_by(self, other_vector):
        return Vector3(
            self.x_component - other_vector.x_component,
            self.y_component - other_vector.y_component,
            self.z_component - other_vector.z_component,
        )

    def scaled_by(self, scalar_factor):
        return Vector3(
            self.x_component * scalar_factor,
            self.y_component * scalar_factor,
            self.z_component * scalar_factor,
        )

    def length(self):
        return math.sqrt(
            self.x_component * self.x_component
            + self.y_component * self.y_component
            + self.z_component * self.z_component
        )

    def distance_to(self, other_vector):
        return self.subtracted_by(other_vector).length()

    def linearly_interpolated_to(self, other_vector, interpolation_amount):
        return Vector3(
            self.x_component + (other_vector.x_component - self.x_component) * interpolation_amount,
            self.y_component + (other_vector.y_component - self.y_component) * interpolation_amount,
            self.z_component + (other_vector.z_component - self.z_component) * interpolation_amount,
        )

    def rotated_around_vertical_axis(self, angle_in_radians):
        cosine_value = math.cos(angle_in_radians)
        sine_value = math.sin(angle_in_radians)
        return Vector3(
            self.x_component * cosine_value + self.z_component * sine_value,
            self.y_component,
            -self.x_component * sine_value + self.z_component * cosine_value,
        )

    def rotated_around_horizontal_axis(self, angle_in_radians):
        cosine_value = math.cos(angle_in_radians)
        sine_value = math.sin(angle_in_radians)
        return Vector3(
            self.x_component,
            self.y_component * cosine_value - self.z_component * sine_value,
            self.y_component * sine_value + self.z_component * cosine_value,
        )
