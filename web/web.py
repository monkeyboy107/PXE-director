from flask import Flask, request, flash, url_for, redirect, abort, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import host_management
import html_renderer
import common_tools
import os


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        # self.id = self

    def get_id(self):
        # return self
        return self.id

    def is_authenticated(self):
        return True

    def get(self):
        return self


@app.route('/')
@login_manager.unauthorized_handler
def index():
    return html_renderer.get_html(title='Index', template='index.html', user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = request.form
    if request.method == 'POST':
        user = form['username']
        password = form['password']
        if not common_tools.test_auth(user, password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(User(user))
        # return redirect(url_for('index'))
        return redirect(url_for('login'))
    return html_renderer.get_html(template='login.html', title='Sign In', user=current_user)


@app.route('/hosts')
def hosts():
    if is_signed_in(current_user) is True:
        return html_renderer.get_html(template='hosts.html', title='List of hosts', user=current_user,
                                      hosts=host_management.get_info('host'))
    else:
        return is_signed_in(current_user)


@app.route('/hosts/<mac_address>', methods=['GET', 'POST'])
def edit_host(mac_address):
    if is_signed_in(current_user) is True:
        if request.method == 'POST':
            description = request.form['description']
            mac = request.form['mac']
            script = request.form['ipxe-script'].split('\r\n')
            host_management.update_host(mac, mac, 'mac')
            host_management.update_host(mac, script, 'ipxe-script')
            host_management.update_host(mac, description, 'description')
            return redirect(url_for('hosts'))
        else:
            return html_renderer.get_html(template='edit_host.html',
                                          hosts=host_management.get_info('host', mac=mac_address))
    else:
        return is_signed_in(current_user)


@app.route('/settings')
def settings():
    if is_signed_in(current_user) is True:
        os.listdir()
        return html_renderer.get_html(title='Settings', template='settings.html', user=current_user)
    else:
        return is_signed_in(current_user)


@app.route('/manage_users')
def manage_users():
    if is_signed_in(current_user) is True:
        users = []
        settings = common_tools.correct_path('settings/web.yaml')
        settings = common_tools.yaml_to_dict(settings)
        users_yaml = os.listdir(settings['users'])
        for user in users_yaml:
            users.append((common_tools.yaml_to_dict(common_tools.correct_path(settings['users'] + '/' + user))))
            # users.append(user)
        return render_template('user_manager.html', title='Manage users',
                               pages=common_tools.get_links(is_logged_on=True), css=common_tools.get_css(), users=users)
    else:
        return is_signed_in(current_user)


@app.route('/manage_users/update/<username>')
def update_user(username):
    if is_signed_in(current_user):
        users_dir = common_tools.yaml_to_dict(common_tools.correct_path('settings/authentication.yaml'))['auth_dir']
        for user in os.listdir(users_dir):
            dict_user = common_tools.yaml_to_dict(common_tools.correct_path(users_dir + '/' + user))
            if dict_user['username'] == username:
                return render_template('user.html', title='Update user ' + username, css=common_tools.get_css(),
                                       pages=common_tools.get_links(is_logged_on=True), user=dict_user,
                                       algorithms=types_of_hash)
        flash('User not found')
        return redirect(url_for('manage_users'))
    else:
        return is_signed_in(current_user)


@app.route('/manage_users/delete/<username>')
def delete_user(username):
    if is_signed_in(current_user):
        users_dir = common_tools.yaml_to_dict(common_tools.correct_path('settings/authentication.yaml'))['auth_dir']
        for user in os.listdir(users_dir):
            dict_user = common_tools.yaml_to_dict(common_tools.correct_path(users_dir + '/' + user))
            if dict_user['username'] == username:
                common_tools.delete_user(username)
                return redirect(url_for('manage_users'))
        flash('User not found')
        return redirect(url_for('manage_users'))
    else:
        return is_signed_in(current_user)


@app.route('/new_user', methods=['GET', 'POST'])
def add_user():
    if is_signed_in(current_user) is True:
        if request.method == 'POST':
            if not request.form['password'] == '':
                common_tools.add_user(request.form['username'], request.form['password'], request.form['salt'],
                                      request.form['algorithm'])
            return redirect(url_for('manage_users'))
        else:
            return render_template('user.html', title='Add a user', pages=common_tools.get_links(is_logged_on=True),
                               css=common_tools.get_css(), user={'username', 'salt', 'hash'}, algorithms=types_of_hash)
    else:
        return is_signed_in(current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register_host/<mac_address>')
def register_host(mac_address):
    if host_management.is_registered(mac_address):
        return 'Already registered!'
    else:
        return host_management.register_host(mac_address)


@app.route('/boot_host/<mac_address>')
def boot_host(mac_address):
    if host_management.is_registered(mac_address):
        script = host_management.get_info('ipxe-script', mac=mac_address)
        script = '\r\n'.join(script['ipxe-script'])
        return str(script)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


def is_signed_in(current_user):
    if str(current_user)[0] == '<':
        return redirect(url_for('index'))
    else:
        return True


host = '127.0.0.1'
debug = False
login_manager.login_view = 'user.login'
login_manager.login_message = 'Welcome'
types_of_hash = ['sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s', 'md5', 'plaintext']

