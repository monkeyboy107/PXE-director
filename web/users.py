from flask import Blueprint, render_template, abort, request, redirect, session
from flask_session import Session
from jinja2 import TemplateNotFound
from DatabaseManagement import UserManagement
import tools

# Sets up the blueprint
user_management = Blueprint('user_management', __name__, template_folder='templates')

# Renders login page
@user_management.route('/login', methods=['GET', 'POST'])
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
    return render_template('form.html.j2', form=form, title='Please sign in')

# Logs out the user
@user_management.route('/logout')
def logout():
  session['username'] = None
  return redirect('/')

# List all users
@user_management.route('/users/')
def users():
  if tools.login_check():
    users = [{'id': user.username} for user in UserManagement.find_all_users()]
    return render_template('edit_fields.html.j2', fields=users, record_type='user')
  else:
    return redirect('/login')


# Edit a specific user
@user_management.route('/users/<username>', methods=['GET', 'POST'])
def edit_user(username):
  if tools.login_check():
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
@user_management.route('/user/add', methods=['GET', 'POST'])
def add_user():
  if tools.login_check():
    if request.method == 'POST':
      username = request.form.get('username')
      password = request.form.get('password')
      verify_password = request.form.get('verify_password')
      if verify_password != password:
        return redirect('/users/add')
      else:
        UserManagement.add_user(username, password)
        return redirect('/users')
    form = [
           {'id': 'username', 'title': 'Username', 'type': 'text', 'placeholder': 'New users username'},
           {'id': 'password', 'title': 'Password', 'type': 'password', 'placeholder': 'New users password'},
           {'id': 'verify_password', 'title': 'Verify password', 'type': 'password', 'placeholder': 'Verify password'}
           ]
    return render_template('form.html.j2', form=form)
  else:
    return redirect('/login')

# Delete a user
@user_management.route('/users/<username>/delete', methods=['GET', 'POST'])
def delete_user(username):
  if tools.login_check() and session.get('username', None) != username:
    if request.method == 'POST':
      print(request.form.get('delete'))
      if request.form.get('delete') == 'on':
        UserManagement.delete_user(username)
      return redirect('/users')
    return render_template('delete_user.html.j2', username=username)
  return redirect('/login')
