from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def index():
  return render_template('index.html.j2')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    return "You're signed in"
  else:
    return render_template('login.html.j2')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)
