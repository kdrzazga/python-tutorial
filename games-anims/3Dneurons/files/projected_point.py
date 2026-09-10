class ProjectedPoint:
    def __init__(self, screen_x, screen_y, depth_from_viewer, projected_scale, is_in_front_of_viewer):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.depth_from_viewer = depth_from_viewer
        self.projected_scale = projected_scale
        self.is_in_front_of_viewer = is_in_front_of_viewer
