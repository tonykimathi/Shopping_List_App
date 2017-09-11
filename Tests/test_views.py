import unittest
from unittest import TestCase
from app import app


class TestClass(TestCase):
    """Main testing class for the flask app"""
    def setUp(self):
        """ method runs before each test"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

    def login(self, email, password):
        """ login helper """
        return self.client.post('/login',
                                data=dict(email=email,
                                          password=password),
                                follow_redirects=True)

    def sign_up(self, username, email, password, confirm):
        """register helper """
        return self.client.post('/sign_up',
                                data=dict(username=username,
                                          email=email,
                                          password=password,
                                          confirm=confirm),
                                follow_redirects=True)

    def logout(self):
        """logout helper   """
        return self.client.get('/logout',
                               follow_redirects=True)

    def test_sign_up(self):
        result = self.sign_up('jmutua', 'johnmutua@gmail.com', '54321', '54321')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'jmutua, You have successfully signed up', result.data)

    def test_an_existing_user(self):
        result = self.sign_up('jmutua', 'johnmutua@gmail.com', '54321', '54321')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'jmutua, You have successfully signed up', result.data)
        result0 = self.sign_up('jmutua', 'johnmutua@gmail.com', '54321', '54321')
        self.assertEqual(result0.status_code, 200)
        self.assertIn(b'You already have an account! Please log in', result0.data)

    def test_login_success(self):
        result = self.sign_up('jmutua', 'johnmutua@gmail.com', '54321', '54321')
        self.assertIn(b'jmutua, You have successfully signed up', result.data)
        result0 = self.logout()
        self.assertTrue(b'You were logged out!' in result0.data)
        result1 = self.login('johnmutua@gmail.com', '54321')
        self.assertEqual(result1.status_code, 200)
        self.assertIn(b'You have been logged in successfully', result1.data)

    def test_login_invalid(self):
        result = self.login('sam@email.com', '12345')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Email does not exist! Please Sign Up", result.data)

    def test_logout(self):
        result0 = self.sign_up('jmutua', 'johnmutua@gmail.com', '54321', '54321')
        self.assertEqual(result0.status_code, 200)
        self.assertIn(b'jmutua, You have successfully signed up', result0.data)
        result = self.logout()
        self.assertTrue(b'You were logged out!' in result.data)


if __name__ == '__main__':
    unittest.main()
