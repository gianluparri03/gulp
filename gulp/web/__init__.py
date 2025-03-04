from flask import Flask, redirect, send_from_directory
from datetime import timedelta

from gulp.configs import configs


app = Flask(__name__)


def init_app():
    # Sets some parameters of the app
    app.url_map.strict_slashes = True
    app.config['SECRET_KEY'] = configs['GULP_SESSIONS_SECRET']
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=90)
    app.config['SESSION_COOKIE_SECURE'] = configs['GULP_SESSIONS_SECURE']
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/', path='icon.png')

@app.errorhandler(404)
def handle_404(e):
    return render_template('error.html', error='Page not found')

from gulp.web.user import *
