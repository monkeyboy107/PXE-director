from flask import Flask, render_template, request, session, redirect
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

@app.route('/')
def index():
  return render_template('index.html.j2')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    session['name'] = request.form.get('username')
    print(session)
    return render_template('values.html.j2', value=session['name'])
  else:
    return render_template('login.html.j2', title='Please sign in')

@app.route('/logout')
def logout():
  session['name'] = None
  return redirect('/')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)
