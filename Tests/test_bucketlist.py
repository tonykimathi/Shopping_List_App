import unittest
from app.models import Item, ShoppingList, User


class TestItem(unittest.TestCase):
    def setUp(self):
        self.item = Item("name")

    def tearDown(self):
        self.item = None

    def test_item_name_is_str(self):
        self.assertIsInstance(self.item.name, str)

    def test_update_item_without_name(self):
        self.assertTrue(self.item.update(None), "Item must have a name")

    def test_update_item_with_invalid_name(self):
        self.assertTrue(self.item.update(["name"]), "Item name must be a string")

    def test_update_item(self):
        self.item.update("new name")

        self.assertEqual(
            self.item.name,
            "new name",
            msg="Method update should update the items name"
        )


class TestShoppingList(unittest.TestCase):
    def setUp(self):
        self.shopping_list = ShoppingList("name")

    def tearDown(self):
        self.shopping_list = None

    def test_shopping_list_id_is_int(self):
        self.assertIsInstance(self.shopping_list.id, int)

    def test_shopping_title_is_str(self):
        self.assertIsInstance(self.shopping_list.list_name, str)

    def test_shopping_list_items_is_list(self):
        self.assertIsInstance(self.shopping_list.list_items, list)

    def test_add_item_without_name(self):
        self.assertTrue(self.shopping_list.add_item(None), "Please input an item name")

    def test_add_item_with_invalid_name(self):
        self.assertTrue(self.shopping_list.add_item(["name"]), "Wrong input. Please input a string")

    def test_add_item(self):
        # attempt to create a shopping list item
        item_name = "School shoes"
        self.shopping_list.add_item(item_name)

    def test_update_list_without_title(self):
        self.assertTrue(self.shopping_list.update_shopping_list(None), "Please input a shopping list name")

    def test_update_list_with_invalid_title(self):
        self.assertTrue(self.shopping_list.update_shopping_list(["new"]), "Wrong input. Please input a string")

    def test_update_list(self):
        self.shopping_list.update_shopping_list("new shopping list")

        self.assertEqual(
            self.shopping_list.list_name,
            "new shopping list",
            msg="Update method should update the shopping lists name"
        )

    def test_delete_item_invalid_argument(self):
        self.assertEqual(
            self.shopping_list.delete_item([]), "Item id should be an Integer"
        )


    def test_delete_item_that_do_not_exist(self):
        non_existent_id=10

        self.assertEqual(
            self.shopping_list.delete_item(non_existent_id),
            "Item does not exist"
        )


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("username", "email", "first_name", "last_name", "password")

    def tearDown(self):
        self.user = None

    def test_user_id_is_int(self):
        self.assertIsInstance(self.user.id, int)

    def test_username_is_str(self):
        self.assertIsInstance(self.user.username, str)

    def test_email_is_str(self):
        self.assertIsInstance(self.user.email, str)

    def test_user_first_name_is_str(self):
        self.assertIsInstance(self.user.first_name, str)

    def test_user_last_name_is_str(self):
        self.assertIsInstance(self.user.last_name, str)

    def test_user_password_is_str(self):
        self.assertIsInstance(self.user.password_hash, str)

    def test_user_shopping_list_is_list(self):
        self.assertIsInstance(self.user.shopping_lists, list)

    def test_create_shopping_list_without_title(self):
        self.assertTrue(self.user.create_shopping_list(None), "Please input an list name")

    def test_create_shopping_list_with_invalid_title(self):
        self.assertTrue(
            self.user.create_shopping_list(["33", "45", "76"]),
            "shopping list name must be a string"
        )

    def test_create_shopping_list_with_duplicate_title(self):

        shopping_list_name = "grocery list"
        self.user.create_shopping_list(shopping_list_name)

        shopping_list_name = "grocery list"
        self.user.create_shopping_list(shopping_list_name)


    def test_delete_shopping_list_invalid_argument(self):
        self.assertEqual(
            self.user.delete_shopping_list([]), "Shopping list id should be an Integer"
        )

    def test_delete_shopping_list(self):
        shopping_list_id = 23
        self.assertEqual(
            self.user.delete_shopping_list(shopping_list_id), "Shopping list deleted"
        )

if __name__ == '__main__':
    unittest.main()
