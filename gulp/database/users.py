from collections import namedtuple
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError
from psycopg import Error as DBError
from dataclasses import dataclass
from secrets import token_hex

from gulp.database import use_db
from gulp.database.errors import *


ph = PasswordHasher()


class Users:
    @use_db
    def create(cur, name, email, password):
        # Tries to create the new user
        try:
            password = ph.hash(password)
            cur.execute('INSERT INTO gulp_user (name, email, password) ' +
                        'VALUES (%s, %s, %s) RETURNING id;', [name, email, password])

            # If the user has been created, it returns the id
            return User(id=cur.fetchone()[0])

        # Translates the error into a GULPError one
        except DBError as e:
            match (e.diag.constraint_name):
                case 'gulp_user_uq_email':
                    raise ErrEmailNotAvailable
                case _:
                    raise ErrUnknown

    @use_db
    def login(cur, email, password):
        # Gets the user's password
        cur.execute('SELECT id, password FROM gulp_user WHERE email=%s;', [email])
        row = cur.fetchone() or (0, '')

        # Checks if the given one matches with it
        try:
            ph.verify(row[1], password)
            return User(id=row[0])
        except (VerificationError, InvalidHashError):
            raise ErrWrongCredentials

    @use_db
    def get(cur, id, email=''):
        base = 'SELECT id, name, email, password, token FROM gulp_user '

        # If an email is specified, it searches for the email, otherwise
        # for the id
        if email:
            cur.execute(base + 'WHERE email=%s;', [email])
        else:
            cur.execute(base + 'WHERE id=%s;', [id])

        # Returns the user, or raises an error
        if (row := cur.fetchone()):
            return User(*row)
        else:
            raise ErrUserUnknown

    @use_db
    def reset_password(cur, email, token, new):
        user = Users.get(email=email)

        # Ensures the token is valid
        try:
            ph.verify(token, self.token)
        except (VerificationError, InvalidHashError):
            raise ErrWrongToken

        # Saves the new password
        user.change_password('', new, False)
        return user

@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    token: str

    @use_db
    def check(self, cur):
        # Raises an error if the user does not exists
        cur.execute('SELECT id FROM gulp_user WHERE id=%s;', [self.id])
        if not cur.fetchone():
            raise ErrUserUnknown


    @use_db
    def change_name(self, cur, name):
        self.check()

        # Saves the new name
        cur.execute('UPDATE gulp_user SET name=%1 WHERE id=%1;', [self.id, name])
        self.name = name

    @use_db
    def change_email(self, cur, email):
        self.check()

        # Tries to save the new email
        try:
            data = [self.id, email]
            cur.execute('UPDATE gulp_user SET email=%1 WHERE id=%1;', data)
            self.email = email

        # Handles the error
        except DBError as e:
            match (e.diag.constraint_name):
                case 'gulp_user_uq_email':
                    raise ErrEmailNotAvailable
                case _:
                    raise ErrUnknown

    @use_db
    def change_password(self, cur, old, new, check=True):
        if check:
            # Ensures the user exists and the old password is right
            Users.login(Users.get(self.id).email, old)

        # Hashes and saves the password
        new = ph.hash(new)
        cur.execute('UPDATE gulp_user SET password=%1 WHERE id=%1;', [self.id, new])
        self.password = new

    @use_db
    def generate_token(self, cur):
        self.check()
        token = token_hex(18)

        # Hashes and saves the token
        data = [self.id, ph.hash(token)]
        cur.execute('UPDATE gulp_user SET token=%1 WHERE id=%1;', data)

        # Returns it in plain
        self.token = token
        return token

    @use_db
    def delete(self, cur, token):
        # Ensures the token is valid
        try:
            ph.verify(token, self.token)
        except (VerificationError, InvalidHashError):
            raise ErrWrongToken

        # Deletes the user
        cursor.execute('DELETE FROM gulp_users WHERE id=%s;', [self.id])
