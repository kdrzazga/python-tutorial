from linear_algebra import Vector3


class GroundPlane:
    def __init__(self, half_extent=140.0, height=0.0):
        self.corner_points = (
            Vector3(-half_extent, height, -half_extent),
            Vector3(half_extent, height, -half_extent),
            Vector3(half_extent, height, half_extent),
            Vector3(-half_extent, height, half_extent),
        )

    def render_using(self, renderer, palette):
        renderer.render_shaded_quad(self.corner_points, palette.ground_color)
