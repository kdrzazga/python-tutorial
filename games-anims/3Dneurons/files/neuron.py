import math


class Neuron:
    def __init__(self, resting_position, base_radius, idle_pulse_frequency, idle_pulse_phase_offset, activation_decay_rate, refractory_period):
        self.resting_position = resting_position
        self.base_radius = base_radius
        self.idle_pulse_frequency = idle_pulse_frequency
        self.idle_pulse_phase_offset = idle_pulse_phase_offset
        self.activation_decay_rate = activation_decay_rate
        self.refractory_period = refractory_period
        self.activation_level = 0.0
        self.elapsed_lifetime = 0.0
        self.time_since_last_activation = refractory_period
        self.outgoing_synapses = []

    def register_outgoing_synapse(self, synapse):
        self.outgoing_synapses.append(synapse)

    def advance(self, elapsed_seconds):
        self.elapsed_lifetime += elapsed_seconds
        self.time_since_last_activation += elapsed_seconds
        self.activation_level = max(0.0, self.activation_level - self.activation_decay_rate * elapsed_seconds)

    def is_ready_to_activate(self):
        return self.time_since_last_activation >= self.refractory_period

    def receive_activation(self):
        self.activation_level = 1.0
        self.time_since_last_activation = 0.0

    def current_idle_pulse(self):
        return 0.5 + 0.5 * math.sin(self.elapsed_lifetime * self.idle_pulse_frequency * math.tau + self.idle_pulse_phase_offset)

    def current_brightness(self):
        idle_brightness = 0.28 + 0.12 * self.current_idle_pulse()
        return min(1.0, idle_brightness + self.activation_level)

    def current_radius(self):
        return self.base_radius * (1.0 + 0.5 * self.activation_level + 0.12 * self.current_idle_pulse())
