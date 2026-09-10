class AnimationConfiguration:
    def __init__(self):
        self.window_width = 1280
        self.window_height = 800
        self.window_title = "Neural Network Animation"
        self.background_color = (4, 6, 14)
        self.target_frames_per_second = 60
        self.maximum_elapsed_seconds_per_frame = 0.05

        self.neuron_count = 64
        self.network_radius = 260.0
        self.maximum_synapse_connection_distance = 165.0
        self.maximum_synapses_per_neuron = 3

        self.neuron_base_radius_range = (5.0, 9.0)
        self.neuron_idle_pulse_frequency_range = (0.35, 1.05)
        self.neuron_activation_decay_rate = 2.2
        self.neuron_refractory_period = 0.25

        self.signal_pulse_speed_range = (0.3, 0.55)
        self.signal_pulse_glow_radius = 13.0
        self.firing_propagation_probability = 0.42
        self.spontaneous_firing_interval_range = (0.5, 1.2)

        self.focal_length = 720.0
        self.viewer_distance = 620.0
        self.world_yaw_rotation_speed = 0.18
        self.world_pitch_rotation_speed = 0.07

        self.neuron_core_color = (150, 215, 255)
        self.neuron_halo_color = (40, 120, 220)
        self.synapse_line_color = (70, 120, 200)
        self.signal_pulse_color = (190, 245, 255)

        self.glow_sprite_resolution = 128
        self.glow_edge_falloff_power = 2.0

        self.depth_fade_start_distance = 380.0
        self.depth_fade_end_distance = 920.0
