from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask import url_for
import path_tools
import yaml_tools


settings = path_tools.correct_path('settings/html_renderer.yaml')


def get_html(debug=False, template='layout.html', title='Title', statics_dir='static', css=['style.css']):
    stylesheets = []
    for css_file in css:
        stylesheets.append(statics_dir + '/' + css_file)
        if debug:
            print(statics_dir, css_file)
            print(stylesheets)
        else:
            url_for(statics_dir, filename=css_file)
    jinja_loader = FileSystemLoader(path_tools.correct_path(yaml_tools.yaml_to_dict(settings)['html_path']))
    jinja_autoescape = select_autoescape(yaml_tools.yaml_to_dict(settings)['autoescape'])
    jinja_environment = Environment(loader=jinja_loader, autoescape=jinja_autoescape)
    jinja_template = jinja_environment.get_template(template)
    jinja_rendered = jinja_template.render(title=title, css=stylesheets)
    return jinja_rendered


if '__main__' == __name__:
    # print(get_html(debug=True))
    get_html(debug=True)