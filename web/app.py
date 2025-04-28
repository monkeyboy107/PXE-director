from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from datetime import timedelta

# Import the rest of the flask app
from users import user_management
from scripts import script_management

# Sets up flask app correctly
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)

# Blueprints
for blueprint in [user_management, script_management]:
 app.register_blueprint(blueprint)

Session(app)

# Renders the index page
@app.route('/')
def index():
  return render_template('index.html.j2', user=session.get('username', None))

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)
