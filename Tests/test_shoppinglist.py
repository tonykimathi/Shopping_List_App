import unittest
from app.models import Data, ShoppingList, User
import datetime


class Testclass(unittest.TestCase):
    """ main test class"""
    def setUp(self):
        self.user1 = {'username': 'sammy',
                      '_id': '528drrdd9540dab149eceedb14',
                      'password': '12345',
                      'email': 'samysam@email'}
        self.shoppinglist1 = {'title': 'shoppinglist one',
                              '_id': 'sdf528drr0dab149eceedb14',
                              'owner': 'sammy',
                              'owner_id': '528drrdd9540dab149eceedb14'}
        self.item1 = {'shoppinglist_id': 'sdf528drr0dab149eceedb14',
                      '_id': '098un528drr0dab149eceedb14',
                      'item_name': 'dancing in town',
                      'owner_id': '528drrdd9540dab149eceedb14',
                      'date': '9 - 08 - 2017'}
        self.data = Data
        del self.data.users[:]
        del self.data.items[:]
        del self.data.shoppinglists[:]

    def test_new_item(self):
        list1 = ShoppingList('bucket 1', 'sammy',
                             '528drrdd9540dab149eceedb14', _id=None)
        list1.new_item('dancing in town', '5', date=datetime.datetime.utcnow())
        result = self.data.get_the_data('528drrdd9540dab149eceedb14', self.data.items)
        self.assertIsInstance(result, list)

    def test_user_exists(self):
        self.data.add_data(self.user1)
        result = User.check_user_exists('samysam@email')
        self.assertTrue(result)
        result1 = User.check_user_exists('johndoe@email')
        self.assertFalse(result1)

    def test_register(self):
        self.data.add_data(self.user1)
        result = User.sign_up_user('johndoe', 'johndoe@email', '12345')
        self.assertTrue(result)
        result1 = User.sign_up_user('sammy', 'samysam@email', '12345')
        self.assertFalse(result1)

    def test_user_login_verify(self):
        result1 = User.sign_up_user('johndoe@email', '1234567')
        self.assertFalse(result1)

    def test_get_username(self):
        User.sign_up_user('johny', 'johndoe@email', '54321')
        result = User.get_username('johndoe@email')
        self.assertEqual(result, 'johny')

    def test_current_user(self):
        User.sign_up_user('john', 'johndoe@email', '54321')
        result = User.current_user('johndoe@email')
        self.assertIsInstance(result, dict)
        self.assertEqual(result['username'], 'john')

if __name__ == '__main__':
    unittest.main()
