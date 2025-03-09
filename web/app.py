from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from DatabaseManagement import UserManagement
from datetime import timedelta

# Sets up flask app correctly
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)

Session(app)

# Wanting to ensure that the session username is maintained.
def add_username(values):
  if login_check():
    values['username'] = session['username']
    values['name'] = session['username'] # This is placeholder. In the future I want to be able to reference the actual name
                                         # But for now I can live with just referencing the user's name
  return values

def login_check():
  if 'username' in session:
    if session['username']:
      return True
  return False
    
# Renders the index page
@app.route('/')
def index():
  values = add_username({})
  return render_template('index.html.j2', **values)

# Renders login page
@app.route('/login', methods=['GET', 'POST'])
def login():
  values = {'title': 'Please sign in'}
  values = add_username(values)
  if request.method == 'POST':
    if UserManagement.test_authentication(request.form.get('username'), request.form.get('password')):
      session['username'] = request.form.get('username')
    return redirect('/')
  else:
    return render_template('login.html.j2', **values)

# Logs out the user
@app.route('/logout')
def logout():
  session['username'] = None
  return redirect('/')

# List all users
@app.route('/users/')
def users():
  if login_check():
    values = add_username({})
    # return render_template('users.html.j2', **values)
    return str(values['name'])
  else:
    return redirect('/login')


# Edit a specific user
@app.route('/users/<username>')
def edit_user(username):
  if login_check():
    values = add_username({})
    # return render_template('edit_user.html.j2', **values)
    # return render_template('form.html.j2') 
    return username
  else:
    return redirect('/login')

@app.route('/users/<username>/password', methods=['GET', 'POST'])
def update_password(username):
  if login_check():
    if request.method == 'POST':
      user = session['username']
      old_password = request.form.get('password')
      new_password = request.form.get('new_password')
      verify_password = request.form.get('verify_password')
      if UserManagement.test_authentication(user, old_password):
        if new_password == verify_password:
          UserManagement.reset_password(user, new_password)
        return redirect(f'/users/{session["username"]}/password')
    values = add_username({})
    form = [
      {'id': 'password', 'title': 'Current password', 'type': 'password', 'placeholder': 'Current password'},
      {'id': 'new_password', 'title': 'New password', 'type': 'password', 'placeholder': 'New password'},
      {'id': 'verify_password', 'title': 'Verify password', 'type': 'password', 'placeholder': 'Verify password'}
    ]
    return render_template('form.html.j2', form=form)
  else:
    return redirect('/login')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)
