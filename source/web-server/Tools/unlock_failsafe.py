#!/bin/python3/
import time
try:
    import tools
except ModuleNotFoundError:
    from Tools import tools

paths = tools.get_correct_file('resources/paths.yaml')
paths = tools.yaml_to_dict(paths)
locked = tools.get_correct_file(paths['locked'])

def lock_checker():
    count = 0
    try:
        while True:
            if tools.yaml_to_dict(tools.get_correct_file(locked))['locked']:
                count = count + 1
                time.sleep(1)
            else:
                count = 0
            if count >= 10:
                tools.dict_to_yaml(locked, {'coordination': False})
    except TypeError:
        lock_checker()