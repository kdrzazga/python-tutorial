from animation_configuration import AnimationConfiguration
from neuron_animation_application import NeuronAnimationApplication


def main():
    configuration = AnimationConfiguration()
    application = NeuronAnimationApplication(configuration)
    application.run()


if __name__ == "__main__":
    main()
