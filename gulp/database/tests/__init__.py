from gulp.database import init_db
from gulp.configs import load_configs

load_configs()
init_db()

from .users import *
