import yaml
import os


def read_yml():
    config = None

    filename = "props.yml"
    script_dir = os.path.dirname(__file__) + "\\data"
    abs_file_path = os.path.join(script_dir, "props.yml")
    with open(abs_file_path, 'r') as stream:
        try:
            config = yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)

    return config