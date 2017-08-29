from werkzeug.security import generate_password_hash, check_password_hash


class User(object):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.__password = password

@property
def password():

    raise AttributeError("password is not a readable attribute.")

@password.setter
def password(self, password):

    self.password_hash = generate_password_hash(password)


def verify_password(self, password):

    return check_password_hash(self.password_hash, password)


class ShoppingList(object):

    cart = {}
    balance = 0
    budget_amount = 0

    def __init__(self, budget_amount):
        self.budget_amount = budget_amount


    def addItem(self, item_name, price, quantity):

        number_types = ( int, float, complex)

        if isinstance(price, number_types) and isinstance(quantity, number_types) and isinstance(item_name, str):
            self.cart[item_name] = price

            total_cost = self.calculatePrice(price, quantity)

            self.balance = self.budget_amount - total_cost
        else:
            raise ValueError


    def removeItem(self, item_name):

        if isinstance( item_name, str):
            pass
        else:
            raise ValueError


    def calculatePrice(self, price, quantity):

        total_amount = price * quantity

        if total_amount > self.balance:
            print("That amount is more than what we have")
            return 0

        return total_amount

