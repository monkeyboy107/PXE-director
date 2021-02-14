import os
import yaml


def correct_path(path):
    dir_slash = '/'
    if os.name == 'nt':
        dir_slash = '\\'

    path = path.replace('/', dir_slash)
    path = path.replace('\\', dir_slash)
    return path


def yaml_to_dict(path_to_yaml):
    with open(path_to_yaml) as stream:
        data = yaml.safe_load(stream)
    return data


def dict_to_yaml(path_to_yaml, data):
    with open(path_to_yaml, 'w+') as stream:
        yaml.safe_dump(data, stream)


def test_auth(username, password):
    settings = yaml_to_dict(correct_path('settings/authentication.yaml'))
    for user in os.listdir(settings['auth_dir']):
        if yaml_to_dict(settings['auth_dir'] + '/' + user)['username'] == username:
            if yaml_to_dict(settings['auth_dir'] + '/' + user)['password'] == password:
                return True
    return False


if __name__ == '__main__':
    print(test_auth('Test', 'Test'))
    print(test_auth('admin', 'password'))