from random import randrange
from flask import url_for
import hashlib
import os
import yaml


# This makes checks if you're in windows or not. If it is in windows then it will correct the path appropriately.
# E.G. if it is windows and is given a windows path, it will return the same path. If it is linux and given a linux path
#   it will then return the same path. But if it is given a windows path on a linux system it will return a linux path.
# In addition the reverse is true.
def correct_path(path):
    # This sets the salsh to be a fordslash
    dir_slash = '/'
    # This asks if it is running windows
    if os.name == 'nt':
        # This sets the path style to be windows compatible
        dir_slash = '\\'
    # This replaces the unix style path with whatever dir_slash is set to
    path = path.replace('/', dir_slash)
    # This replaces the windows style path with whatever dir_slash is set to
    path = path.replace('\\', dir_slash)
    # This will return the updated path
    return path


# This is to directly load a yaml file as a dict
def yaml_to_dict(path_to_yaml):
    # This will open the file that was handed to it
    with open(path_to_yaml) as stream:
        # This will read the data using pyYAML
        data = yaml.safe_load(stream)
    # This will return the data that was read
    return data


# This writes to a yaml file
def dict_to_yaml(path_to_yaml, data):
    # This will open the yaml file in writable form
    with open(path_to_yaml, 'w+') as stream:
        # This writes to the the yaml file
        yaml.safe_dump(data, stream)


# This is to test authentication to see if the password is correct
def test_auth(username, password):
    # This loads the settings
    settings = yaml_to_dict(correct_path('settings/authentication.yaml'))
    # This will go through every single user in the users folder
    for user in os.listdir(settings['auth_dir']):
        # This gets the dictionary of the user to check the password and user
        user_dict = yaml_to_dict(correct_path(settings['auth_dir'] + '/' + user))
        # This checks if the user it loaded is the correct user
        if user_dict['username'] == username:
            # This loads in the hash algorithm
            hash = user_dict['hash']
            # This loads the username
            username = user_dict['username']
            # This loads the salt
            salt = user_dict['salt']
            # This hashes the password as it was hashed when it was saved
            hashed_password = hash_password(password, hash, username, salt)
            # This checks the hash against the hashed password
            if user_dict['password'] == hashed_password:
                # If the hashed password is the same it returns True
                return True
    # If the user wasn't found or if the password was wrong it returns False
    return False


# This loads the web links
def get_pages(is_logged_on=False):
    # This loads the web links into a list for non authenticated users
    web_links = [yaml_to_dict(settings)['links_path']]
    # This check if the user is signed in so it can add more links
    if is_logged_on:
        # This appends the logged in users links
        web_links.append(yaml_to_dict(settings)['logged_on_links_path'])
    # This defines links as a dictionary
    links = {}
    # This goes to the web_links and appends it to the links dictonary
    for link in web_links:
        links.update(yaml_to_dict(correct_path(link)))
    # This defines what pages is
    pages = []
    # This goes through the links dictonary
    for link in links:
        # This converts the dictoanry into a table
        pages.append([link, links[link]])
    return pages


def get_css(css=['style.css'], statics_dir='static', debug=False):
    # This converts the style sheets into a nice iterable format
    stylesheets = []
    # This goes through all the stylesheets files in the css list and formats the way it needs to be returned
    for css_file in css:
        # This formats the where the stylesheet is
        stylesheets.append(statics_dir + '/' + css_file)
        # This will either print out what is being sent to flask or send it to flask
        if debug:
            print(statics_dir, css_file)
            print(stylesheets)
        else:
            # This will serve the css files in the flask
            url_for(statics_dir, filename=css_file)
    return stylesheets


# This salts and hashes the password
def hash_password(password, hash, *salts):
    # This makes the hash variable lower case
    hash = hash.lower()
    # This checks if sha1 is being used
    if 'sha1' == hash:
        hashed = hashlib.sha1()
    # This checks if sha224 is being used
    elif 'sha224' == hash:
        hashed = hashlib.sha224()
    elif 'sha256' == hash:
    # This checks if sha384 is being used
        hashed = hashlib.sha256()
    elif 'sha384' == hash:
        hashed = hashlib.sha384()
    # This checks if sha512 is being used
    elif 'sha512' == hash:
        hashed = hashlib.sha512()
    # This checks if blake2b is being used
    elif 'blake2b' == hash:
        hashed = hashlib.blake2b()
    # This checks if blake2s is being used
    elif 'blake2s' == hash:
        hashed = hashlib.blake2s()
    # This checks if md5 is being used for some god awful reason
    elif 'md5' == hash:
        hashed = hashlib.md5()
    # This checks if plaintext is being used mostly for troubleshooting
    elif 'plaintext' == hash:
        hashed = password
    else:
        # This returns an error if the selected hash was not available
        raise TypeError('Excepted a hash type')
    # This encodes the hashes as utf-8 so it can be hashes
    hashed.update(password.encode('utf-8'))
    # This goes through the salt(s) and add it to the end of the hash. In addition it also converts the salt(s) into
    #  UTF-8 so it is usable
    for salt in salts:
        hashed.update(salt.encode('utf-8'))
    # This formats the data nicely
    return hashed.hexdigest()


# This adds a new user
def add_user(username, password, salt, hash):
    if salt == '':
        # This defines every single character as a list. Im planning to make this into a yaml file that will get loaded
        every_char = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                      'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B',
                      'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                      'V', 'W', 'X', 'Y', 'Z', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ';', ':', '"', "'",
                      ',', '.', '<', '>', '/', '?', '\\', '-', '_', '=', '+', ' ']
        salt = []
        # This goes through 100 characters within every_char list then randomly selects one to be appended to make a
        #  random salt
        for i in range(100):
            salt.append(every_char[randrange(0, len(every_char))])
        # This converts the salt list into a nice list
        salt = ''.join(salt)
    # This sets the local settings file fo this function
    settings = yaml_to_dict(correct_path('settings/authentication.yaml'))
    # This gets the directory where the users are to be stored
    users_folder = settings['auth_dir']
    # This builds teh full path to the user's file
    user_yaml_path = correct_path(users_folder + '/' + username + '.yaml')
    # This hashes the password
    hashed_password = hash_password(password, hash, username, salt)
    # This writes the user's dictonary
    user = {'username': username, 'password': hashed_password, 'salt': salt, 'hash': hash}
    # This writes the user file
    dict_to_yaml(user_yaml_path, user)
    # This returns the user's dictonary for troubleshooting
    return user


def delete_user(username):
    # This gets the user's folder
    folder = yaml_to_dict(correct_path('settings/authentication.yaml'))['auth_dir']
    # This looks at every single file in the folder variable
    users_folder = os.listdir(folder)
    # This goes to every single file in users_folder variable to check if the user is the one to be deleted
    for user in users_folder:
        # This builds the path to the user's yaml file
        user_yaml = correct_path(folder + '/' + user)
        # This checks if the user is the correct one
        if username == yaml_to_dict(user_yaml)['username']:
            # This will remove the user
            os.remove(user_yaml)
            # This returns the path that was deleted for troubleshooting
            return user_yaml
    # This returns the user isn't found
    return print('User not found')


settings = correct_path('settings/common_tools.yaml')


if __name__ == '__main__':
    # print(test_auth('test', 'test'))
    # print(test_auth('admin', 'password'))
    # print(correct_path('hosts\\default.yaml'))
    print(get_pages(is_logged_on=True))
    print(get_pages(is_logged_on=False))
    # print(add_user('admin', 'password', '', 'sha512'))
    # print(delete_user('isaac'))