import os
from dotenv import dotenv_values


# Loads the configs from the .env files.
# .env.local has ah higher priority than .env.
configs = {
    key: value for key, value in (
        dotenv_values('.env') |
        dotenv_values('.env.local') |
        os.environ
    ).items() if key.startswith('GULP_')
}
