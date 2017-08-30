import unittest
from app.models import ShoppingList


class ShoppingListTest(unittest.TestCase):
    def setUp(self):
        budget_amount = 500
        self.shoppingList = ShoppingList(budget_amount)


    def test_addItem_method_returns_error_for_nonInt(self):
        self.assertRaises(ValueError, self.shoppingList.addItem, 1, "one", "thirty")


    def test_addItem_method_returns_error_for_quantityArg_string(self):
        self.assertRaises(ValueError, self.shoppingList.addItem, "rice", "four", 400)


    def test_addItem_method_returns_error_for_priceArg_string(self):
        self.assertRaises(ValueError, self.shoppingList.addItem, "Water", 4, "hundred")


    def test_removeItem_method_returns_error_for_numbers(self):
        self.assertRaises(ValueError, self.shoppingList.removeItem, 2)


    def test_calculatePrice_returns_err_for_exceedingBudget(self):
        result = self.shoppingList.calculatePrice(2, 150)
        self.assertGreaterEqual(self.shoppingList.balance, result)


if __name__ == '__main__':
    unittest.main()
