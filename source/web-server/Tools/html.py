#!/bin/python3
try:
    from flask import render_template
    from Tools import tools
except ModuleNotFoundError:
    import tools


def top_bottom(html, Title='default-title'):
    file = tools.get_correct_file(paths['top_bottom'])
    with open(file) as stream:
        top_bottom = stream.read()
        html = top_bottom.replace('replace-body', str(html))
        html = html.replace('replace-title', str(Title))
    return html


def menu_retriver():
    dict_path = tools.get_correct_file(paths['coordination'], paths['locked'])
    dict_menu = tools.yaml_to_dict(dict_path)
    return dict_to_menu(dict_menu)


def dict_to_menu(dict_menu):
    html = 'WIP'
    menu = dict_menu
    column1 = []
    column2 = []
    column3 = []
    for entry in menu:
        column1.append(entry)
        column2.append(menu[entry]['ipxe-path'])
    # print(column1, column2)
    for line in zip(column1, column2):
        column3.append(str(line)[2:-1].replace("'", '').replace(',', '') +' <a href=/host_edit/' + line[0] + '>'
                       + 'edit' + '<a/>')
    column3 = '<br>'.join(column3)
    return top_bottom(column3)


def edit_host(mac, pxe, comment):
    file = tools.get_correct_file(paths['edit_host'])
    with open(file) as stream:
        html = stream.read()
    html = html.replace('MAC-address', mac)
    html = html.replace('pxe-server-entry', pxe)
    html = html.replace('client-name', comment)
    return top_bottom(html)


try:
    paths = '../resources/paths.yaml'
    paths = tools.yaml_to_dict(paths)
except FileNotFoundError:
    paths = 'resources/paths.yaml'
    paths = tools.yaml_to_dict(paths)

if __name__ == '__main__':
    print(edit_host('mac', 'pxe', 'comment'))
    # print(dict_to_menu({'default': {'comment': 'default menu entry', 'ipxe-path': 'https://10.107.11.4'}, 'ff:ff:ff:ff:ff:fd': {'comment': 'ff:ff:ff:ff:ff:fd', 'ipxe-path': 'https://10.107.11.2'}, 'ff:ff:ff:ff:ff:ff': {'comment': 'ff:ff:ff:ff:ff:ff', 'ipxe-path': 'https://10.107.11.3'}}))
    # print(menu_retriver())