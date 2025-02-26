from psycopg import connect
from .configs import configs


def init_db():
    # Connects to the database
    db = connect(configs['GULP_DATABASE'])
    db.set_autocommit(True)

    # Ensures the schema has been created
    with db.cursor() as cursor:
        cursor.execute(open('gulp/schema.sql').read())
