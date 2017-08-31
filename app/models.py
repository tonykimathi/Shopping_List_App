import random


class User(object):
    def __init__(self, username, email, first_name, last_name, password):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password
        self.shopping_lists = []
        self.id = int(random.random()*500)

    def create_shopping_list(self, list_name):

        if list_name is None:
            return "Please input an list name"

        if not isinstance(list_name, str):
            return "Shopping list name must be a string"

        for shopping_list in self.shopping_lists:
            if shopping_list.list_name in self.shopping_lists:
                return "Shopping list already exists"

        added_list = ShoppingList(list_name)
        self.shopping_lists.append(added_list)

        return added_list.id

    def delete_shopping_list(self, shopping_list_id):

        if not isinstance(shopping_list_id, int):
            return "Shopping list id should be an Integer"

        for shopping_list in self.shopping_lists:
            if shopping_list.id == shopping_list_id:
                del shopping_list

        return "Shopping list deleted"

    def view_shopping_lists(self):
        shopping_list_names = []
        for shopping_list in self.shopping_lists:
            shopping_list_names.append(shopping_list.list_name)

        return shopping_list_names


class ShoppingList(object):

    def __init__(self, list_name):
        self.list_name = list_name
        self.list_items = []
        self.id = int(random.random()*500)

    def add_item(self, item_name):

        for item in self.list_items:
            if item.name == item_name:
                return 'Item already exists'

        if item_name is None:
            return "Please input an item name"

        if not isinstance(item_name, str):
            return "Wrong input. Please input a string"

        new_item = Item(item_name)
        self.list_items.append(new_item)

        return new_item.id

    def delete_item(self, item_id):

        if not isinstance(item_id, int):
            return "Item id should be an Integer"

        for item in self.list_items:
            if item.id == item_id:
                del item
                return True

        return "Item does not exist"

    def update_shopping_list(self, added_list_name):
        if added_list_name is None:
            return "Please input a shopping list name"

        if not isinstance(added_list_name, str):
            return "Wrong input. Please input a string"

        self.list_name = added_list_name


class Item(object):
    def __init__(self, name):
        self.name = name
        self.id = id

    def update(self, name):
        if name is None or len(name) < 1:
            return "Item must have a name"

        if not isinstance(name, str):
            return "Item name must be a string"

        self.name = name