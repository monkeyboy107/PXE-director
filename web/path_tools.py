import os


def correct_path(path):
    dir_slash = '/'
    if os.name == 'nt':
        dir_slash = '\\'

    path = path.replace('/', dir_slash)
    path = path.replace('\\', dir_slash)
    return path

if __name__ == '__main__':
    print(correct_path('/home'))