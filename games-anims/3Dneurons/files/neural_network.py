from files.vector3 import Vector3
from files.neuron import Neuron
from files.synapse import Synapse


class NeuralNetwork:
    def __init__(self, configuration, random_generator):
        self.configuration = configuration
        self.random_generator = random_generator
        self.neurons = []
        self.synapses = []
        self.time_until_next_spontaneous_firing = 0.0
        self.build_neurons()
        self.build_synapses()
        self.schedule_next_spontaneous_firing()

    def build_neurons(self):
        for neuron_index in range(self.configuration.neuron_count):
            resting_position = self.random_position_within_sphere(self.configuration.network_radius)
            base_radius = self.random_generator.uniform(*self.configuration.neuron_base_radius_range)
            idle_pulse_frequency = self.random_generator.uniform(*self.configuration.neuron_idle_pulse_frequency_range)
            idle_pulse_phase_offset = self.random_generator.uniform(0.0, 6.283185307179586)
            neuron = Neuron(
                resting_position,
                base_radius,
                idle_pulse_frequency,
                idle_pulse_phase_offset,
                self.configuration.neuron_activation_decay_rate,
                self.configuration.neuron_refractory_period,
            )
            self.neurons.append(neuron)

    def random_position_within_sphere(self, sphere_radius):
        while True:
            candidate_direction = Vector3(
                self.random_generator.uniform(-1.0, 1.0),
                self.random_generator.uniform(-1.0, 1.0),
                self.random_generator.uniform(-1.0, 1.0),
            )
            if 0.0 < candidate_direction.length() <= 1.0:
                return candidate_direction.scaled_by(sphere_radius)

    def build_synapses(self):
        for source_neuron in self.neurons:
            neighbours_sorted_by_distance = sorted(
                (candidate_neuron for candidate_neuron in self.neurons if candidate_neuron is not source_neuron),
                key=lambda candidate_neuron: source_neuron.resting_position.distance_to(candidate_neuron.resting_position),
            )
            established_connection_count = 0
            for candidate_neuron in neighbours_sorted_by_distance:
                if established_connection_count >= self.configuration.maximum_synapses_per_neuron:
                    break
                if source_neuron.resting_position.distance_to(candidate_neuron.resting_position) > self.configuration.maximum_synapse_connection_distance:
                    break
                synapse = Synapse(
                    source_neuron,
                    candidate_neuron,
                    self.configuration.signal_pulse_speed_range[0],
                    self.configuration.signal_pulse_speed_range[1],
                    self.configuration.firing_propagation_probability,
                    self.random_generator,
                )
                source_neuron.register_outgoing_synapse(synapse)
                self.synapses.append(synapse)
                established_connection_count += 1

    def schedule_next_spontaneous_firing(self):
        self.time_until_next_spontaneous_firing = self.random_generator.uniform(*self.configuration.spontaneous_firing_interval_range)

    def trigger_spontaneous_firing(self):
        ready_neurons = [neuron for neuron in self.neurons if neuron.is_ready_to_activate()]
        if not ready_neurons:
            return
        firing_neuron = self.random_generator.choice(ready_neurons)
        firing_neuron.receive_activation()
        for outgoing_synapse in firing_neuron.outgoing_synapses:
            outgoing_synapse.emit_signal_pulse()

    def advance(self, elapsed_seconds):
        self.time_until_next_spontaneous_firing -= elapsed_seconds
        if self.time_until_next_spontaneous_firing <= 0.0:
            self.trigger_spontaneous_firing()
            self.schedule_next_spontaneous_firing()
        for neuron in self.neurons:
            neuron.advance(elapsed_seconds)
        for synapse in self.synapses:
            synapse.advance(elapsed_seconds)
