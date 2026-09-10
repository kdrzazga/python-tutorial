class SceneRenderer:
    def __init__(self, perspective_projector, world_rotation, neuron_renderer, synapse_renderer):
        self.perspective_projector = perspective_projector
        self.world_rotation = world_rotation
        self.neuron_renderer = neuron_renderer
        self.synapse_renderer = synapse_renderer

    def render(self, target_surface, neural_network):
        projected_points_by_neuron = self.project_all_neurons(neural_network)
        self.synapse_renderer.render_all_synapse_lines(target_surface, neural_network, projected_points_by_neuron)
        self.synapse_renderer.render_all_travelling_pulses(target_surface, neural_network, self.world_rotation, self.perspective_projector)
        self.neuron_renderer.render_all_neurons(target_surface, neural_network, projected_points_by_neuron)

    def project_all_neurons(self, neural_network):
        projected_points_by_neuron = {}
        for neuron in neural_network.neurons:
            rotated_position = self.world_rotation.apply_to(neuron.resting_position)
            projected_points_by_neuron[neuron] = self.perspective_projector.project(rotated_position)
        return projected_points_by_neuron
