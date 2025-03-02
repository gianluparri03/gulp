from unittest import TestCase

from gulp.database.users import Users, User, ph
from gulp.database.errors import *

class TestUsers(TestCase):
    def test_create(self):
        Users.create('name', 'create1@test_users.com', 'password')
        Users.create('name', 'create2@test_users.com', 'password')
        self.assertRaisesRegex(GULPError, ErrEmailNotAvailable, Users.create, 'name_', 'create2@test_users.com', 'password_')

    def test_login(self):
        created = Users.create('name', 'login1@test_users.com', 'password')
        loggedin = Users.login('login1@test_users.com', 'password')
        self.assertEqual(created, loggedin)
        
        self.assertRaisesRegex(GULPError, ErrWrongCredentials, Users.login, 'login2@test_users.com', 'password')

    def test_get(self):
        u = Users.create('name', 'get@test_users.com', 'password')
        token = u.generate_token()

        got = Users.get(u.id)
        self.assertEqual(got.id, u.id)
        self.assertEqual(got.email, 'get@test_users.com')
        self.assertEqual(got.name, 'name')
        ph.verify(got.password, 'password')
        ph.verify(got.token, token)

        self.assertEqual(got, Users.get(0, email='get@test_users.com'))

        self.assertRaisesRegex(GULPError, ErrUserUnknown, Users.get, 0)

    def test_reset_password(self):
        u = Users.create('name', 'reset_password@test_users.com', 'password')
        Users.reset_password('reset_password@test_users.com', u.generate_token(), 'password_')
        Users.login('reset_password@test_users.com', 'password_')

        self.assertRaisesRegex(GULPError, ErrWrongToken, Users.reset_password, 'reset_password@test_users.com', '', 'password')
        self.assertRaisesRegex(GULPError, ErrWrongCredentials, Users.login, 'reset_password@test_users.com', 'password')

        self.assertRaisesRegex(GULPError, ErrUserUnknown, Users.reset_password, '', '', '')

class TestUser(TestCase):
    def test_check(self):
        Users.create('name', 'check@test_user.com', 'password').check()

        self.assertRaisesRegex(GULPError, ErrUserUnknown, User(id=0).check)

    def test_change_name(self):
        u = Users.create('name', 'change_name@test_user.com', 'password')
        u.change_name('name_')
        self.assertEqual(Users.get(u.id).name, 'name_')

        self.assertRaisesRegex(GULPError, ErrUserUnknown, User(id=0).change_name, '')

    def test_change_email(self):
        Users.create('name', 'change_email1@test_user.com', 'password')

        u = Users.create('name', 'change_email2@test_user.com', 'password')
        u.change_email('change_email2_@test_user.com')
        self.assertEqual(Users.get(u.id).email, 'change_email2_@test_user.com')

        self.assertRaisesRegex(GULPError, ErrEmailNotAvailable, u.change_email, 'change_email1@test_user.com')

        self.assertRaisesRegex(GULPError, ErrUserUnknown, User(id=0).change_email, '')

    def test_change_password(self):
        u = Users.create('name', 'change_password@test_user.com', 'password')
        u.change_password('password', 'password_')
        Users.login('change_password@test_user.com', 'password_')

        self.assertRaisesRegex(GULPError, ErrWrongCredentials, u.change_password, 'password', 'password__')
        Users.login('change_password@test_user.com', 'password_')

        self.assertRaisesRegex(GULPError, ErrUserUnknown, User(id=0).change_password, '', '')

    def test_generate_token(self):
        u = Users.create('name', 'generate_token@test_user.com', 'password')
        token = u.generate_token()
        ph.verify(Users.get(u.id).token, token)

        self.assertRaisesRegex(GULPError, ErrUserUnknown, User(id=0).generate_token)

    def test_delete(self):
        u = Users.create('name', 'delete@test_user.com', 'password')
        token = u.generate_token()
        self.assertRaisesRegex(GULPError, ErrWrongToken, u.delete, 'token')

        Users.get(u.id).delete(token)
        self.assertRaisesRegex(GULPError, ErrUserUnknown, Users.get, u.id)
        
        self.assertRaisesRegex(GULPError, ErrUserUnknown, User(id=0).delete, '')
