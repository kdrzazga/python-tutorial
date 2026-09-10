class WorldRotation:
    def __init__(self, yaw_rotation_speed, pitch_rotation_speed):
        self.yaw_rotation_speed = yaw_rotation_speed
        self.pitch_rotation_speed = pitch_rotation_speed
        self.current_yaw_angle = 0.0
        self.current_pitch_angle = 0.0

    def advance(self, elapsed_seconds):
        self.current_yaw_angle += self.yaw_rotation_speed * elapsed_seconds
        self.current_pitch_angle += self.pitch_rotation_speed * elapsed_seconds

    def apply_to(self, world_point):
        return world_point.rotated_around_vertical_axis(self.current_yaw_angle).rotated_around_horizontal_axis(self.current_pitch_angle)
