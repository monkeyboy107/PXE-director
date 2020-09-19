#!/bin/python3
from flask import Flask, redirect, request
import yaml
from Tools import tools, html

app = Flask(__name__)

def get_app():
    return app

def update_host():
    global coordination
    coordination = tools.yaml_to_dict(paths['coordination'])

paths = 'resources/paths.yaml'
paths = tools.yaml_to_dict(paths)

coordination = tools.yaml_to_dict(paths['coordination'])


@app.route('/')
def root():
    return html.top_bottom('Hello world', Title='Default Menu')


@app.route('/test/<arg>')
def test(args):
    return args


@app.route('/checkin/<mac>')
def director(mac):
    coordination = tools.yaml_to_dict(paths['coordination'])
    if len(mac) == 17 or mac == 'default':
        try:
            return 'chain ' + coordination[mac]['ipxe-path']
        except KeyError:
            tools.new_mac(mac)
            return 'chain ' + coordination['default']['ipxe-path']
    else:
        return 'echo ERROR\npause'


@app.route('/list_of_hosts/')
def list_of_hosts():
    update_host()
    return html.menu_retriver()


@app.route('/host_edit/<mac>')
def host_edit(mac):
    update_host()
    try:
        comment = coordination[mac]['comment']
        pxe = coordination[mac]['ipxe-path']
        return html.edit_host(mac, pxe, comment)
    except KeyError:
        return 'MAC not found'


@app.route('/coordinator/', methods=['GET', 'POST'])
def coordinator():
    if request.method == 'POST':
        updates = dict(request.form)
        tools.update_mac(updates, paths['coordination'], paths['locked'])
        return redirect(request.url)
    update_host()
    menu = tools.yaml_to_dict(paths['coordination'])
    return html.dict_to_menu(menu)


if __name__ == '__main__':
    app.run(debug=True)
