from files.signal_pulse import SignalPulse


class Synapse:
    def __init__(self, source_neuron, target_neuron, minimum_pulse_speed, maximum_pulse_speed, propagation_probability, random_generator):
        self.source_neuron = source_neuron
        self.target_neuron = target_neuron
        self.minimum_pulse_speed = minimum_pulse_speed
        self.maximum_pulse_speed = maximum_pulse_speed
        self.propagation_probability = propagation_probability
        self.random_generator = random_generator
        self.travelling_pulses = []

    def emit_signal_pulse(self):
        pulse_speed = self.random_generator.uniform(self.minimum_pulse_speed, self.maximum_pulse_speed)
        self.travelling_pulses.append(SignalPulse(pulse_speed))

    def advance(self, elapsed_seconds):
        for pulse in self.travelling_pulses:
            pulse.advance(elapsed_seconds)
        pulses_that_arrived = [pulse for pulse in self.travelling_pulses if pulse.has_arrived]
        for arrived_pulse in pulses_that_arrived:
            self.travelling_pulses.remove(arrived_pulse)
            self.deliver_signal_to_target()

    def deliver_signal_to_target(self):
        if not self.target_neuron.is_ready_to_activate():
            return
        self.target_neuron.receive_activation()
        if self.random_generator.random() <= self.propagation_probability:
            for outgoing_synapse in self.target_neuron.outgoing_synapses:
                outgoing_synapse.emit_signal_pulse()

    def pulse_world_position(self, pulse):
        return self.source_neuron.resting_position.linearly_interpolated_to(self.target_neuron.resting_position, pulse.progress_along_synapse)
