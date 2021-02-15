from flask import Flask, request, flash, url_for, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
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
    return html_renderer.get_html(title='Index', template='index.html', user='')


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
    return html_renderer.get_html(template='login.html', title='Sign In')


@app.route('/settings')
@login_required
def settings():
    return html_renderer.get_html(title='Settings', template='settings.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(index())


@app.route('/register_host/<mac_address>')
def register_host(mac_address):
    pass



@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


host = '127.0.0.1'
debug = False
login_manager.login_view = 'user.login'
login_manager.login_message = 'Welcome'


