from flask import Blueprint, render_template, abort, request, redirect, session
from flask_session import Session
from jinja2 import TemplateNotFound

# Sets up the blueprint
script_management = Blueprint('script_management', __name__, template_folder='templates')

# Shows the scripts
@script_management.route('/scripts')
def show_scripts():
  return 'Hello world'
