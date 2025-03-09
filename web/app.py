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

def login_check():
  if 'username' in session:
    if session['username']:
      return True
  return False
    
# Renders the index page
@app.route('/')
def index():
  return render_template('index.html.j2', user=session['username'])

# Renders login page
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    if UserManagement.test_authentication(request.form.get('username'), request.form.get('password')):
      session['username'] = request.form.get('username')
    return redirect('/')
  else:
    form = [
           {'id': 'username', 'title': 'Username', 'type': 'text', 'placeholder': 'Enter your username', 'value': ''},
           {'id': 'password', 'title': 'Password', 'type': 'password', 'placeholder': 'Enter your password', 'value': ''}
           ]
    return render_template('form.html.j2', form=form, title='Please sign in', name=session['username'])

# Logs out the user
@app.route('/logout')
def logout():
  session['username'] = None
  return redirect('/')

# List all users
@app.route('/users/')
def users():
  if login_check():
    users = [{'name': user.username} for user in UserManagement.find_all_users()]
    return render_template('edit_users.html.j2', users=users)
  else:
    return redirect('/login')


# Edit a specific user
@app.route('/users/<username>', methods=['GET', 'POST'])
def edit_user(username):
  if login_check():
    user = UserManagement.find_user(username)
    if request.method == 'POST':
      display_name = request.form.get('display_name')
      email = request.form.get('email')
      nickname = request.form.get('nickname')
      password = request.form.get('password')
      fields = {}
      if display_name != user.display_name:
        fields['display_name'] = display_name
      if email != user.email:
        fields['email'] = email
      if nickname != user.nickname:
        fields['nickname'] = nickname
      if password:
        fields['password'] = password
      UserManagement.update_field(user.username, **fields)
    form = [
            {'id': 'display_name', 'title': 'Display name', 'type': 'text', 'placeholder': 'Users display name', 'value': user.display_name},
            {'id': 'email', 'title': 'Email', 'type': 'text', 'placeholder': 'Users email', 'value': user.email},
            {'id': 'nickname', 'title': 'Nickname', 'type': 'text', 'placeholder': 'Users nickname', 'value': user.nickname}
           ]
    if username != session['username']:
      form.append({'id': 'password', 'title': 'Password', 'type': 'password', 'placeholder': 'Reset password to'})
    return render_template('form.html.j2', form=form)
  else:
    return redirect('/login')

# Add a user
# @app.route('/users/<username>/add', methods=['GET', 'POST'])


# Delete a user
@app.route('/users/<username>/delete', methods=['GET', 'POST'])
def delete_user(username):
  if login_check() and session['username'] != username:
    if request.method == 'POST':
      print(request.form.get('delete'))
      if request.form.get('delete') == 'on':
        UserManagement.delete_user(username)
      return redirect('/users')
    return render_template('delete_user.html.j2', username=username)
  return redirect('/login')

# Changes current user's password
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
    form = [
      {'id': 'password', 'title': 'Current password', 'type': 'password', 'placeholder': 'Current password', 'value': ''},
      {'id': 'new_password', 'title': 'New password', 'type': 'password', 'placeholder': 'New password', 'value': ''},
      {'id': 'verify_password', 'title': 'Verify password', 'type': 'password', 'placeholder': 'Verify password', 'value': ''}
    ]
    return render_template('form.html.j2', form=form)
  else:
    return redirect('/login')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)
