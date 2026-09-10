import math


class FogParticle:
    def __init__(self, home_position, base_size, drift_amplitude, drift_speed, drift_phase, pulse_speed, pulse_phase):
        self.home_position = home_position
        self.base_size = base_size
        self.drift_amplitude = drift_amplitude
        self.drift_speed = drift_speed
        self.drift_phase = drift_phase
        self.pulse_speed = pulse_speed
        self.pulse_phase = pulse_phase

    def position_at(self, elapsed_seconds):
        wobble_x = self.drift_amplitude * math.sin(self.drift_speed * elapsed_seconds + self.drift_phase)
        wobble_y = self.drift_amplitude * 0.5 * math.sin(self.drift_speed * 0.7 * elapsed_seconds + self.drift_phase * 1.7)
        wobble_z = self.drift_amplitude * math.cos(self.drift_speed * elapsed_seconds + self.drift_phase)
        return (self.home_position[0] + wobble_x,
                self.home_position[1] + wobble_y,
                self.home_position[2] + wobble_z)

    def half_size_at(self, elapsed_seconds):
        return self.base_size * (1.0 + 0.35 * math.sin(self.pulse_speed * elapsed_seconds + self.pulse_phase))

    def opacity_at(self, elapsed_seconds):
        return 0.20 + 0.12 * math.sin(self.pulse_speed * elapsed_seconds + self.pulse_phase)
