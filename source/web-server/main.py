#!/bin/python3
import director
from multiprocessing import Process
from Tools import tools, unlock_failsafe

failsafe = Process(target=unlock_failsafe.lock_checker)
failsafe.start()

paths = 'resources/paths.yaml'
paths = tools.yaml_to_dict(paths)
debug = tools.yaml_to_dict(paths['production'])
settings_path = paths['settings']
settings_loaded = tools.yaml_to_dict(paths['settings'])
debug = debug['debug']

if debug:
    port = settings_loaded['debug']['port']
    host = settings_loaded['debug']['host']
else:
    port = settings_loaded['production']['port']
    host = settings_loaded['production']['host']

app = director.get_app()
app.run(port=port, host=host, debug=debug)
