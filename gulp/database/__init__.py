from psycopg import connect
from functools import wraps

from gulp.configs import configs


def init_db():
    global conn

    # Connects to the database
    conn = connect(configs['GULP_DATABASE'])
    conn.set_autocommit(True)

    # Ensures the schema has been created
    with conn.cursor() as cursor:
        cursor.execute(open('gulp/database/schema.sql').read())

def use_db(func):
    # Create a cursor for each function
    @wraps(func)
    def inner(*args, **kwargs):
        with conn.cursor() as cur:
            return func(cur, *args, **kwargs)

    return inner

from .errors import GULPError
from .users import Users
