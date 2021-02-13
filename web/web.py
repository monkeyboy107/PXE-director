from flask import Flask
import html_renderer

app = Flask(__name__)


@app.route('/')
def index():
    return html_renderer.get_html(title='Index', template='index.html')