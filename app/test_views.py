import unittest
from run import app


class ViewsTestCase(unittest.TestCase):

    def test_flask_application_is_up_and_running(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.code, 200)

    def test_flask_login(self):
        tester = app.test_client(self)
        response = tester.login
        assert b'You have now been logged in!' in response.data

    def test_flask_logout(self):
        tester = app.test_client(self)
        response = tester.login
        assert b'You were logged out!' in response.data

    def test_flask_logout(self):
        tester = app.test_client(self)
        response = tester.login
        assert b'Invalid username or password' in response.data


if __name__ == '__main__':
    unittest.main()
