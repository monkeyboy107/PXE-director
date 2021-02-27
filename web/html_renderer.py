from flask import url_for, render_template
import utils

settings = utils.correct_path('settings/html_renderer.yaml')


def get_html(debug=False, template='layout.html', title='Title', statics_dir='static', css=['style.css'],
             is_logged_on=False, user=None, hosts=None):
    '''
    This is here currently as legacy and will be removed
    :param debug: If you are debugging then set this to be True
    :param template: The string of the name of the template
    :param title: The title of the html page
    :param statics_dir: Where you have CSS files
    :param css: A list of strings of the different CSS files
    :param is_logged_on: If you know the user is signed on then you set this to True
    :param user: The user's username
    :param hosts: The host you're referencing
    :return: The rendered HTML
    '''
    user = str(user)
    if user[0] != '<':
        is_logged_on = True
    stylesheets = []
    links = []
    web_links = [utils.yaml_to_dict(settings)['links_path']]

    # This check if the user is signed in so it can add more links
    if is_logged_on:
        web_links.append(utils.yaml_to_dict(settings)['logged_on_links_path'])

    # This will prep the list being handed to jinja
    for dict in web_links:
        links.append(get_links(utils.yaml_to_dict(dict)))
    passable = []

    # This combines the lists for jinja
    for element in links:
        passable.append(element)

    if is_logged_on:
        links = passable[0] + passable[1]
    else:
        links = passable[0]

    # This will prep the css link for jinja and flask
    for css_file in css:
        stylesheets.append(statics_dir + '/' + css_file)

        # This will either print out what is being sent to flask or send it to flask
        if debug:
            pass
            # print(statics_dir, css_file)
            # print(stylesheets)
        else:
            url_for(statics_dir, filename=css_file)
    if not debug:
        return render_template(template, title=title, css=stylesheets, pages=links, user=user, hosts=hosts)


def get_links(links_dict):
    '''
    This will return links as a nicely usable dictonary
    :param links_dict: The dictonary
    :return: returns the list
    '''
    pages = []
    # links_path = common_tools.correct_path(common_tools.yaml_to_dict(links_dict)['links_path'])
    # links = common_tools.yaml_to_dict(links_path)
    # for link in links:
    #     pages.append([link, links[link]])
    for link in links_dict:
        pages.append([link, links_dict[link]])
    return pages


if '__main__' == __name__:
    print(get_html(debug=True, is_logged_on=True, is_host=True))
    # get_html(debug=True, is_logged_on=True, is_host=True)
    # print(get_links(settings))