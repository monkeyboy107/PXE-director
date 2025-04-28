from flask import Blueprint, render_template, abort, request, redirect, session
from flask_session import Session
from jinja2 import TemplateNotFound
from DatabaseManagement import ScriptManagement
import tools

# Sets up the blueprint
script_management = Blueprint('script_management', __name__, template_folder='templates')

# Shows the scripts
@script_management.route('/scripts')
def show_scripts():
  if tools.login_check():
    scripts = [{'id': script.id} for script in ScriptManagement.find_all_scripts()]
    return render_template('edit_fields.html.j2', field=scripts, record_type='script')
  return 'Hello world'

# Adds a new script
@script_management.route('/script/add', methods=['GET', 'POST'])
def add_script():
  if tools.login_check():
    if request.method == 'POST':
      return 'POST METHOD'
    form = [
           {'id': 'id', 'title': 'Script id', 'type': 'text', 'placeholder': 'A unique ID for the script'},
           {'id': 'description', 'title': 'Description', 'type': 'text', 'placeholder': 'A description'},
           ]
    text_area = [
                {'id': 'script', 'title': 'IPXE script', 'rows': '50', 'cols': '100'}
                ]
    return render_template('form.html.j2', form=form, text_area=text_area)
