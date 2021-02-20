import web
import common_tools
import secrets

# This sets a secret for the web app
secret = secrets.token_urlsafe(16)
web.app.secret_key = secret


settings = common_tools.correct_path('settings/manager.yaml')


# This loads the settings and checks if it's in debug mode or not
if common_tools.yaml_to_dict(settings)['debug']:
    port = common_tools.yaml_to_dict(settings)['debug_port']
    IP = common_tools.yaml_to_dict(settings)['debug_IP']
else:
    port = common_tools.yaml_to_dict(settings)['http_port']
    IP = common_tools.yaml_to_dict(settings)['IP']


if '__main__' == __name__:
    web.host = IP
    web.debug = common_tools.yaml_to_dict(settings)['debug']
    web.app.run(port=port, host=IP, debug=common_tools.yaml_to_dict(settings)['debug'])

