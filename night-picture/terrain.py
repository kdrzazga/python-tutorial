class Terrain:
    def __init__(self, edge_x, right_x, back_height, front_height, curve=1.15):
        self.edge_x = edge_x
        self.right_x = right_x
        self.back_height = back_height
        self.front_height = front_height
        self.curve = curve

    def height_at(self, x):
        if x <= self.edge_x:
            return self.back_height
        span = self.right_x - self.edge_x
        progress = (x - self.edge_x) / span
        if progress < 0.0:
            progress = 0.0
        if progress > 1.0:
            progress = 1.0
        eased = progress ** self.curve
        return self.back_height + (self.front_height - self.back_height) * eased
