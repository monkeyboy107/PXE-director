from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask import url_for, render_template
import common_tools


settings = common_tools.correct_path('settings/html_renderer.yaml')


def get_html(debug=False, template='layout.html', title='Title', statics_dir='static', css=['style.css'],
             is_logged_on=False, user=None):
    stylesheets = []
    links = [common_tools.yaml_to_dict(settings)['links_path']]

    # This check if the user is signed in so it can add more links
    if is_logged_on:
        links.append(common_tools.yaml_to_dict(settings)['logged_on_links_path'])

    # This will prep the list being handed to jinja
    for dict in list(links):
        links.append(get_links(common_tools.yaml_to_dict(dict)))
        # links.append(get_links(common_tools.yaml_to_dict(common_tools.yaml_to_dict(dict))))
        print(dict)
        links.pop(0)
    passable = []

    # This combines the lists for jinja
    for element in links:
        passable.append(element)
    links = passable[0]

    # This will prep the css link for jinja and flask
    for css_file in css:
        stylesheets.append(statics_dir + '/' + css_file)

        # This will either print out what is being sent to flask or send it to flask
        if debug:
            print(statics_dir, css_file)
            print(stylesheets)
        else:
            url_for(statics_dir, filename=css_file)

    return render_template(template, title=title, css=stylesheets, pages=links)


def get_links(links_dict):
    pages = []
    # links_path = common_tools.correct_path(common_tools.yaml_to_dict(links_dict)['links_path'])
    # links = common_tools.yaml_to_dict(links_path)
    # for link in links:
    #     pages.append([link, links[link]])
    for link in links_dict:
        pages.append([link, links_dict[link]])
    return pages


if '__main__' == __name__:
    # print(get_html(debug=True))
    get_html(debug=True, is_logged_on=True)
    # print(get_links(settings))