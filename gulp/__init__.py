from flask import Flask

from gulp.configs import load_configs, configs
from gulp.database import init_db

app = Flask(__name__)

from .routes import *


def run():
    # Loads the configs
    load_configs()

    # Initializes the database connection
    init_db()

    # Runs the app according to the configs
    app.run(
        debug=configs['GULP_DEBUG'],
        port=configs['GULP_PORT'],
    )
