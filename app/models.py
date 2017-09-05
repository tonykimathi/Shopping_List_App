from flask_login import UserMixin
import uuid


class User(UserMixin):
    users = []

    def __init__(self, username, email, first_name, last_name, password, _userid=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self._id = uuid.uuid4().hex if _userid is None else _userid

    @classmethod
    def register(cls, username, email, first_name, last_name, password):
        user_info = {}

        for user in User.users:
            if username == user['username']:
                return "Username already exists."

            else:
                user_info['username'] = username
                user_info['email'] = email
                user_info['first_name'] = first_name
                user_info['last_name'] = last_name
                user_info['password'] = password
                User.users.append(user_info)

                return "You have been registered successfully"

    @classmethod
    def login(cls, username, password):

        for user in User.users:
            if username == user['username']:
                if password == user['password']:
                    return "You have been logged in successfully"
                else:
                    return "Password is incorrect"
            return "Please insert correct username"

    @classmethod
    def check_user(cls, email):
        for user in User.users:
            if email in User.users:
                return user[email]


class ShoppingList(object):

    def __init__(self, list_name, owner, owner_id, content, _id=None):
        self.list_name = list_name
        self.owner = owner
        self.owner_id = owner_id
        self.content = content
        self._id = uuid.uuid4().hex if _id is None else _id
        self.shopping_lists = []

    def create_shopping_list(self, list_name, content, owner, owner_id):

        if list_name is None:
            return "Please input an list name"

        if content is None:
            return "Please input a list item"

        if not isinstance(list_name, str):
            return "Shopping list name must be a string"

        if not isinstance(content, str):
            return "Content must be a string"

        for shopping_list in self.shopping_lists:
            if shopping_list.list_name in self.shopping_lists:
                return "Shopping list name already exists"

        added_list = ShoppingList(list_name, content, owner_id, owner)
        self.shopping_lists.append(added_list)

    def delete_shopping_list(self, shopping_list_id):

        if not isinstance(shopping_list_id, int):
            return "Shopping list id should be an Integer"

        for shopping_list in self.shopping_lists:
            if shopping_list.id == shopping_list_id:
                del shopping_list

        return "Shopping list deleted"

    def view_shopping_list(self):
        shopping_list_names = [item for item in self.shopping_lists if item['owner'] == self.username]

        for shopping_list in self.shopping_lists:
            shopping_list_names.append(shopping_list.list_name)

        return shopping_list_names


class ShoppingList(object):

    def __init__(self, list_name, owner, owner_id, content, _id=None):
        self.list_name = list_name
        self.owner = owner
        self.owner_id = owner_id
        self.content = content
        self._id = uuid.uuid4().hex if _id is None else _id
        self.list_items = []

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