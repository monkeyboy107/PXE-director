from flask import Flask, request, flash, url_for, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import host_management
import html_renderer
import common_tools


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


@app.route('/settings')
def settings():
    if is_signed_in(current_user) is True:
        return html_renderer.get_html(title='Settings', template='settings.html', user=current_user)
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


