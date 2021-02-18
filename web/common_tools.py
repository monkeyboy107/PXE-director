from random import randrange
from flask import url_for
import hashlib
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
        user_dict = yaml_to_dict(correct_path(settings['auth_dir'] + '/' + user))
        if user_dict['username'] == username:
            hash = user_dict['hash']
            username = user_dict['username']
            salt = user_dict['salt']
            hashed_password = hash_password(password, hash, username, salt)
            # if yaml_to_dict(settings['auth_dir'] + '/' + user)['password'] == password:
            if user_dict['password'] == hashed_password:
                return True
    return False


def get_links(is_logged_on=False):
    web_links = [yaml_to_dict(settings)['links_path']]

    # This check if the user is signed in so it can add more links
    if is_logged_on:
        web_links.append(yaml_to_dict(settings)['logged_on_links_path'])
    links = {}
    for link in web_links:
        links.update(yaml_to_dict(correct_path(link)))
    pages = []
    for link in links:
        pages.append([link, links[link]])
    return pages


def get_css(css=['style.css'], statics_dir='static', debug=False):
    stylesheets = []
    for css_file in css:
        stylesheets.append(statics_dir + '/' + css_file)

        # This will either print out what is being sent to flask or send it to flask
        if debug:
            pass
            # print(statics_dir, css_file)
            # print(stylesheets)
        else:
            url_for(statics_dir, filename=css_file)
    return stylesheets


def hash_password(password, hash, *salts):
    hash = hash.lower()
    if 'sha1' == hash:
        hashed = hashlib.sha1()
    elif 'sha224' == hash:
        hashed = hashlib.sha224()
    elif 'sha256' == hash:
        hashed = hashlib.sha256()
    elif 'sha384' == hash:
        hashed = hashlib.sha384()
    elif 'sha512' == hash:
        hashed = hashlib.sha512()
    elif 'blake2b' == hash:
        hashed = hashlib.blake2b()
    elif 'blake2s' == hash:
        hashed = hashlib.blake2s()
    elif 'md5' == hash:
        hashed = hashlib.md5()
    elif 'plaintext' == hash:
        hashed = password
        for salt in salts:
            hashed = hashed + salt
        return hashed
    else:
        raise TypeError('Excepted a hash type')
    hashed.update(password.encode('utf-8'))
    for salt in salts:
        hashed.update(salt.encode('utf-8'))
    return hashed.hexdigest()


def add_user(username, password, salt, hash):
    every_char = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                  'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                  'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                  'Y', 'Z', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ';', ':', '"', "'", ',', '.', '<', '>',
                  '/', '?', '\\', '-', '_', '=', '+', ' ']
    if salt == '':
        salt = []
        for i in range(100):
            salt.append(every_char[randrange(0, len(every_char))])
        salt = ''.join(salt)
    settings = yaml_to_dict(correct_path('settings/authentication.yaml'))
    users_folder = settings['auth_dir']
    user_yaml_path = correct_path(users_folder + '/' + username + '.yaml')
    hashed_password = hash_password(password, hash, username, salt)
    user = {'username': username, 'password': hashed_password, 'salt': salt, 'hash': hash}
    dict_to_yaml(user_yaml_path, user)
    return user


def delete_user(username):
    folder = yaml_to_dict(correct_path('settings/authentication.yaml'))['auth_dir']
    users_folder = os.listdir(folder)
    for user in users_folder:
        user_yaml = correct_path(folder + '/' + user)
        if username == yaml_to_dict(user_yaml)['username']:
            os.remove(user_yaml)
            return user_yaml
    return False


settings = correct_path('settings/common_tools.yaml')


if __name__ == '__main__':
    # print(test_auth('test', 'test'))
    # print(test_auth('admin', 'password'))
    # print(correct_path('hosts\\default.yaml'))
    # print(get_links(is_logged_on=True))
    # print(add_user('admin', 'password', '', 'sha512'))
    print(delete_user('isaac'))