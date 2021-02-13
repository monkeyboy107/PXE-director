import yaml


def yaml_to_dict(path_to_yaml):
    with open(path_to_yaml) as stream:
        data = yaml.safe_load(stream)
    return data
