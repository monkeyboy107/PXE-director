from flask import Flask, request, flash, url_for, redirect, abort, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import host_management
import common_tools
import os


# This defines the web app and instantiates it
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


# This creates the user class for flask_login
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


# This defines the route to login the user
@login_manager.unauthorized_handler
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # This defines the form to make it easier to reference
    form = request.form
    # This checks if it is post request
    if request.method == 'POST':
        # This loads the user from the request
        user = form['username']
        # This loads the password from the request
        password = form['password']
        # This tests the authentication
        if common_tools.test_auth(user, password):
            # This logs in the user
            login_user(User(user))
        else:
            # This tells the user that their creds are wrong
            flash('Invalid username or password')
        # This returns to the login page
        return redirect((url_for('login')))
    # This renders the template
    return render_template('login.html', title='Sign In', css=common_tools.get_css(),
                           pages=common_tools.get_pages(is_logged_on=is_logged_on(current_user)))


# This is for viewing the current hosts
@app.route('/hosts')
def hosts():
    # This checks if the user is signed in before letting them have access to do anything
    if is_logged_on(current_user):
        # This returns the hosts
        return render_template('hosts.html', title='List of hosts', hosts=host_management.get_info('host'),
                               css=common_tools.get_css(), pages=common_tools.get_pages(is_logged_on(current_user)))
    else:
        # This will redirect the user if they are not signed in
        return redirect(url_for('login'))


# This the user edit a host
@app.route('/hosts/<mac_address>', methods=['GET', 'POST'])
def edit_host(mac_address):
    # This checks if the user is signed in
    if is_logged_on(current_user) is True:
        # This checks if the user is trying to post data back after updating a host
        if request.method == 'POST':
            # This loads the description from the posted data
            description = request.form['description']
            # This loads the mac from the requested data
            mac = request.form['mac']
            # This loads the script from the posted data
            script = request.form['ipxe-script'].split('\r\n')
            # This writes the data using the following, mac is the host mac is what is being updated and mac is the key
            host_management.update_host(mac, mac, 'mac')
            # This updates the data using the following, mac is the host script is the data to be written and
            #  ipxe-script is the key
            host_management.update_host(mac, script, 'ipxe-script')
            # This updates the data using the following, mac is the host, description is the data, description is the
            #  key
            host_management.update_host(mac, description, 'description')
            # This redirects to the hosts page
            return redirect(url_for('hosts'))
        else:
            # If not post this will return to the edit host page
            return render_template('edit_host.html', hosts=host_management.get_info('host', mac=mac_address),
                                   css=common_tools.get_css(),
                                   pages=common_tools.get_pages(is_logged_on=is_logged_on(current_user)))
    else:
        # If the user isn't signed in it will redirect
        return redirect(url_for('login'))


# This will be where you can edit the yaml files
@app.route('/settings')
def settings():
    # This checks if the user is signed in
    if is_logged_on(current_user):
        return render_template('settings.html', title='Settings', user=current_user, css=common_tools.get_css(),
                               pages=common_tools.get_pages(is_logged_on=is_logged_on(current_user)))
    else:
        # This will redirect
        return redirect(url_for('login'))


# This loads the all the users for editing and adding new users
@app.route('/manage_users')
def manage_users():
    # This checks if the user is signed in
    if is_logged_on(current_user):
        # This loads the user list
        users = []
        # This loads the settings with the correct path
        settings = common_tools.correct_path('settings/web.yaml')
        # This loads the settings loads the dictonary
        settings = common_tools.yaml_to_dict(settings)
        # This gets all the user's folders as a list
        users_yaml = os.listdir(settings['users'])
        # This goes through the list of all the users
        for user in users_yaml:
            # This appends the users folder with the dicts of every user
            users.append((common_tools.yaml_to_dict(common_tools.correct_path(settings['users'] + '/' + user))))
        return render_template('user_manager.html', title='Manage users',
                               pages=common_tools.get_pages(is_logged_on=True), css=common_tools.get_css(), users=users)
    else:
        # This will redirect the user who isn't signed in
        return redirect(url_for('login'))


# This updates a user
@app.route('/manage_users/update/<username>')
def update_user(username):
    # This checks if the user is signed in
    if is_logged_on(current_user):
        # This checks loads the user_dir that is to be updated
        users_dir = common_tools.yaml_to_dict(common_tools.correct_path('settings/authentication.yaml'))['auth_dir']
        # This goes through every user
        for user in os.listdir(users_dir):
            # This loads the user as a dictonary
            dict_user = common_tools.yaml_to_dict(common_tools.correct_path(users_dir + '/' + user))
            if dict_user['username'] == username:
                # This returns the user information after it renders it
                return render_template('user.html', title='Update user ' + username, css=common_tools.get_css(),
                                       pages=common_tools.get_pages(is_logged_on=True), user=dict_user,
                                       algorithms=types_of_hash)
        # If the user is not found this will flash it
        flash('User not found')
        return redirect(url_for('manage_users'))
    else:
        # This redirects users who aren't signed in
        return redirect(url_for('login'))


# This deletes a user
@app.route('/manage_users/delete/<username>')
def delete_user(username):
    # This checks that the person trying to delete a user is signed in
    if is_logged_on(current_user):
        # This loads the users folder
        users_dir = common_tools.yaml_to_dict(common_tools.correct_path('settings/authentication.yaml'))['auth_dir']
        # This goes through every user
        for user in os.listdir(users_dir):
            # This loads the user as dict_user
            dict_user = common_tools.yaml_to_dict(common_tools.correct_path(users_dir + '/' + user))
            # This checks if the username is the one that we are looking for
            if dict_user['username'] == username:
                # If it is it will then delete it
                common_tools.delete_user(username)
                # This will redirect to users folder
                return redirect(url_for('manage_users'))
        # This flashes that the user was not found
        flash('User not found')
        return redirect(url_for('manage_users'))
    else:
        # This flashes that the user was deleted
        flash(username + ' has been deleted')
        return redirect(url_for('login'))


# This will generate a new user
@app.route('/new_user', methods=['GET', 'POST'])
def add_user():
    # This checks if the person trying to add a new user is signed in
    if is_logged_on(current_user):
        # This checks if it is posting data
        if request.method == 'POST':
            # This makes sure that the password field IS NOT empty
            if not request.form['password'] == '':
                # This writes the new user
                common_tools.add_user(request.form['username'], request.form['password'], request.form['salt'],
                                      request.form['algorithm'])
            # This redirects to the manage_users section
            return redirect(url_for('manage_users'))
        else:
            # This goes to the signed in user section
            return render_template('user.html', title='Add a user', pages=common_tools.get_pages(is_logged_on=True),
                                   css=common_tools.get_css(), user={'username' 'salt' 'hash': 'sha256'},
                                   algorithms=types_of_hash)
    else:
        # This redirects not signed in users
        return redirect(url_for('login'))


# This logs out the current user
@app.route('/logout')
def logout():
    # This logs out the user
    logout_user()
    # This redirects the logged out user
    return redirect((url_for('login')))


# This will register a new mac address. Or return the fact that the host is already registered
@app.route('/register_host/<mac_address>')
def register_host(mac_address):
    # This checks if the host is already registered
    if host_management.is_registered(mac_address):
        # This will return the boot script
        return boot_host(mac_address)
    else:
        # This will register the host
        return host_management.register_host(mac_address)


# This loads the boot script
@app.route('/boot_host/<mac_address>')
def boot_host(mac_address):
    # This checks if the host is registered
    if host_management.is_registered(mac_address):
        # This loads the script
        script = host_management.get_info('ipxe-script', mac=mac_address)
        # This converts the script into a useable format
        script = '\r\n'.join(script)
        # this returns the script as a list
        return str(script)


# This loads the user
@login_manager.user_loader
def load_user(user_id):
    # This will load the user profile
    return User.get(user_id)


# This checks if the user is signed in
def is_logged_on(current_user):
    # If the first letter is a < then the user is likely not signed in
    if str(current_user)[0] == '<':
        return False
    else:
        return True


host = '127.0.0.1'
debug = False
login_manager.login_view = 'user.login'
login_manager.login_message = 'Welcome'
types_of_hash = ['sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s', 'md5', 'plaintext']