from flask import Flask, request, flash, url_for, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from is_safe_url import is_safe_url
import html_renderer
import common_tools

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = self

    def get_id(self):
        return self.id


@app.route('/')
@login_manager.unauthorized_handler
def index():
    return html_renderer.get_html(title='Index', template='index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if common_tools.test_auth(request.form['username'], request.form['password']):
            flash('Login Successful.')
            next = request.args.get('next')
            user = User(request.form['username'])
            # user = User()
            user = login_manager.user_loader(user)
            login_user(user)
            # if not is_safe_url(next, {host}) or not debug:
            #     return abort(400)
            return redirect(next or url_for('login'))
    return html_renderer.get_html(title='Login', template='login.html')


@app.route('/settings')
@login_required
def settings():
    return html_renderer.get_html(title='Settings', template='settings.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(index())


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


host = '127.0.0.1'
debug = False
login_manager.login_view = 'user.login'
login_manager.login_message = 'Welcome'


