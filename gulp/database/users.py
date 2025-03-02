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
                    raise GULPError(ErrEmailNotAvailable)
                case _:
                    raise GULPError(ErrUnknown)

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
            raise GULPError(ErrWrongCredentials)

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
            raise GULPError(ErrUserUnknown)

    @use_db
    def reset_password(cur, email, token, new):
        user = Users.get(0, email=email)

        # Ensures the token is valid
        try:
            ph.verify(user.token, token)
        except (VerificationError, InvalidHashError):
            raise GULPError(ErrWrongToken)

        # Saves the new password
        user.change_password('', new, False)
        return user

@dataclass
class User:
    id: int
    name: str = ''
    email: str = ''
    password: str = ''
    token: str = ''

    @use_db
    def check(cur, self):
        # Raises an error if the user does not exists
        cur.execute('SELECT id FROM gulp_user WHERE id=%s;', [self.id])
        if not cur.fetchone():
            raise GULPError(ErrUserUnknown)


    @use_db
    def change_name(cur, self, name):
        self.check()

        # Saves the new name
        cur.execute('UPDATE gulp_user SET name=%s WHERE id=%s;', [name, self.id])
        self.name = name

    @use_db
    def change_email(cur, self, email):
        self.check()

        # Tries to save the new email
        try:
            data = [email, self.id]
            cur.execute('UPDATE gulp_user SET email=%s WHERE id=%s;', data)
            self.email = email

        # Handles the error
        except DBError as e:
            match (e.diag.constraint_name):
                case 'gulp_user_uq_email':
                    raise GULPError(ErrEmailNotAvailable)
                case _:
                    raise GULPError(ErrUnknown)

    @use_db
    def change_password(cur, self, old, new, check=True):
        if check:
            # Ensures the user exists and the old password is right
            Users.login(Users.get(self.id).email, old)

        # Hashes and saves the password
        new = ph.hash(new)
        cur.execute('UPDATE gulp_user SET password=%s WHERE id=%s;', [new, self.id])
        self.password = new

    @use_db
    def generate_token(cur, self):
        self.check()
        token = token_hex(18)

        # Hashes and saves the token
        data = [ph.hash(token), self.id]
        cur.execute('UPDATE gulp_user SET token=%s WHERE id=%s;', data)

        # Returns it in plain
        self.token = token
        return token

    @use_db
    def delete(cur, self, token):
        self.check()

        # Ensures the token is valid
        try:
            ph.verify(self.token, token)
        except (VerificationError, InvalidHashError):
            raise GULPError(ErrWrongToken)

        # Deletes the user
        cur.execute('DELETE FROM gulp_user WHERE id=%s;', [self.id])
