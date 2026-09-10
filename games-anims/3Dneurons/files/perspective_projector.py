from files.projected_point import ProjectedPoint


class PerspectiveProjector:
    def __init__(self, screen_width, screen_height, focal_length, viewer_distance):
        self.horizontal_center = screen_width / 2.0
        self.vertical_center = screen_height / 2.0
        self.focal_length = focal_length
        self.viewer_distance = viewer_distance
        self.minimum_depth_from_viewer = 1.0

    def project(self, world_point):
        depth_from_viewer = world_point.z_component + self.viewer_distance
        if depth_from_viewer < self.minimum_depth_from_viewer:
            return ProjectedPoint(self.horizontal_center, self.vertical_center, depth_from_viewer, 0.0, False)
        perspective_factor = self.focal_length / depth_from_viewer
        screen_x = self.horizontal_center + world_point.x_component * perspective_factor
        screen_y = self.vertical_center - world_point.y_component * perspective_factor
        return ProjectedPoint(screen_x, screen_y, depth_from_viewer, perspective_factor, True)
