class SignalPulse:
    def __init__(self, travel_speed):
        self.travel_speed = travel_speed
        self.progress_along_synapse = 0.0
        self.has_arrived = False

    def advance(self, elapsed_seconds):
        self.progress_along_synapse += self.travel_speed * elapsed_seconds
        if self.progress_along_synapse >= 1.0:
            self.progress_along_synapse = 1.0
            self.has_arrived = True
