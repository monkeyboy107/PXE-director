import web
import yaml_tools
import path_tools


settings = path_tools.correct_path('settings/manager.yaml')


if yaml_tools.yaml_to_dict(settings)['debug']:
    port = yaml_tools.yaml_to_dict(settings)['debug_port']
    IP = yaml_tools.yaml_to_dict(settings)['debug_IP']
else:
    port = yaml_tools.yaml_to_dict(settings)['http_port']
    IP = yaml_tools.yaml_to_dict(settings)['IP']


if '__main__' == __name__:
    web.app.run(port=port, host=IP, debug=yaml_tools.yaml_to_dict(settings)['debug'])