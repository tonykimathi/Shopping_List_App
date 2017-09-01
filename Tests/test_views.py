from app import create_app
import unittest
from flask_testing import TestCase



class TestBase(TestCase):
    def create_app(self):
        config_name = 'development'
        app = create_app(config_name)

        return app


class TestViews(TestBase):

    def login(self, email, password):
        """ login helper """
        return self.client.post('/login/',
                                data=dict(email=email,
                                          password=password),
                                follow_redirects=True)

    def sign_up(self, username, email, password, confirm):
        """register helper """
        return self.client.post('/Sign Up/',
                                data=dict(username=username,
                                          email=email,
                                          password=password,
                                          confirm=confirm),
                                follow_redirects=True)

    def logout(self):
        """logout helper   """
        return self.client.get('/logout/',
                               follow_redirects=True)

    def test_sign_up(self):
        result = self.sign_up('johny', 'johndoe@gmail.com', '54321', '54321')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'You have been registered!  johny ', result.data)

    def test_an_existing_user(self):
        result = self.sign_up('johny', 'johndoe@gmail.com', '54321', '54321')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'You have been registered!  jane ', result.data)
        result0 = self.sign_up('jane', 'janedoe@gmail.com', '54321', '54321')
        self.assertEqual(result0.status_code, 200)
        self.assertIn(b'Email exists!!! You can login instead!', result0.data)

    def test_login_success(self):
        result = self.sign_up('johny', 'johndoe@gmail.com', '54321', '54321')
        self.assertIn(b'You have been registered!  sam ', result.data)
        result0 = self.logout()
        self.assertTrue(b'You have successfully logged out' in result0.data)
        result1 = self.login('sam@email.com', '12345')
        self.assertEqual(result1.status_code, 200)
        self.assertIn(b'You have successfully logged in!!', result1.data)

    def test_login_invalid(self):
        result = self.login('sam@email.com', '12345')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Email do not exist!!  first register", result.data)

    def test_logout(self):
        result0 = self.sign_up('johny', 'johndoe@gmail.com', '54321', '54321')
        self.assertEqual(result0.status_code, 200)
        self.assertIn(b'You have been registered!  sam ', result0.data)
        result = self.logout()
        self.assertTrue(b'You have successfully logged out' in result.data)


if __name__ == '__main__':
    unittest.main()
