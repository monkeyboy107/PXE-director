#!/bin/python3
import yaml
from multiprocessing import Process
import time


def get_correct_file(file_path):
    try:
        with open(file_path):
            return file_path
    except FileNotFoundError:
        return '../' + file_path


def yaml_to_dict(yaml_path):
    with open(yaml_path) as stream:
        data = yaml.safe_load(stream)
    return data

def dict_to_yaml(yaml_path, dict):
    with open(yaml_path, 'w+') as stream:
        stream.write(yaml.dump(dict))

def new_mac(mac):
    multiprocess = True
    coordination = paths['coordination']
    locked = paths['locked']
    if multiprocess:
        writer = Process(target=write_new_mac, args=(mac, coordination, locked,))
        writer.start()
    else:
        return write_new_mac(mac, coordination, locked)

def write_new_mac(mac, coordination_path, is_locked_path):
    while yaml_to_dict(is_locked_path)['locked'] is True:
        time.sleep(10)
    locked = yaml_to_dict(is_locked_path)
    locked['coordination'] = True
    dict_to_yaml(is_locked_path, locked)
    master_mac_list = yaml_to_dict(coordination_path)
    path_dict = {'ipxe-path': master_mac_list['default']['ipxe-path']}
    master_mac_list[mac] = path_dict
    master_mac_list[mac]['comment'] = mac
    dict_to_yaml(coordination_path, master_mac_list)
    locked['coordination'] = False
    dict_to_yaml(is_locked_path, locked)

def update_mac(dict, coordination_path, is_locked_path):
    multiprocess = True
    if multiprocess:
        writer = Process(target=write_update_mac, args=(dict, coordination_path, is_locked_path,))
        writer.run()
    else:
        return write_new_mac(dict, coordination_path, is_locked_path)

def write_update_mac(dict, coordination_path, is_locked_path):
    while yaml_to_dict(is_locked_path)['coordination'] is True:
        time.sleep(10)
    locked = yaml_to_dict(is_locked_path)
    locked['coordination'] = True
    dict_to_yaml(is_locked_path, locked)
    master_mac_list = yaml_to_dict(coordination_path)
    master_mac_list[dict['MAC']]['comment'] = dict['name']
    master_mac_list[dict['MAC']]['ipxe-path'] = dict['pxe-server']
    dict_to_yaml(coordination_path, master_mac_list)
    locked['coordination'] = False
    dict_to_yaml(is_locked_path, locked)


paths = 'resources/paths.yaml'

try:
    with open(paths) as stream:
        None
except FileNotFoundError:
    paths = '../resources/paths.yaml'

paths = yaml_to_dict(paths)

if __name__ == '__main__':
    # new_mac('MM:MM:MM:SS:SS:SD')
    print(yaml_to_dict('../resources/coordination.yaml'))