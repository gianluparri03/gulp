from os import environ
from dotenv import dotenv_values


configs = {}

def load_configs():
    # Gets the environment type
    env = environ['GULP_ENV']

    # Loads the configs from the .env files.
    # `configs/.env.E.local` has ah higher priority than `configs/.env.E`.
    for key, value in (
            dotenv_values(f'gulp/configs/.env.{env}') |
            dotenv_values(f'gulp/configs/.env.{env}.local') |
            environ
        ).items():

        if key.startswith('GULP_'):
            configs[key] = value
