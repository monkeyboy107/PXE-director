import web
import utils
import secrets

# This sets a secret for the web app
secret = secrets.token_urlsafe(16)
web.app.secret_key = secret


settings = utils.correct_path('settings/manager.yaml')


# This loads the settings and checks if it's in debug mode or not
if utils.yaml_to_dict(settings)['debug']:
    port = utils.yaml_to_dict(settings)['debug_port']
    IP = utils.yaml_to_dict(settings)['debug_IP']
else:
    port = utils.yaml_to_dict(settings)['http_port']
    IP = utils.yaml_to_dict(settings)['IP']


if '__main__' == __name__:
    web.host = IP
    web.debug = utils.yaml_to_dict(settings)['debug']
    web.app.run(port=port, host=IP, debug=utils.yaml_to_dict(settings)['debug'])

