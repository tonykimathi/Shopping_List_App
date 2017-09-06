import uuid


class User(object):
    count = 0

    def __init__(self, username, email, first_name, last_name, password, user_id=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.shopping_lists = []
        self.user_id = uuid.uuid4().hex if user_id is None else user_id

        self.info = {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'user_id': self.user_id,
            'shopping_lists': self.shopping_lists
        }

        User.count += 1

    def view_info(self):
        return self.info

    def return_user_name(self):
        return self.username

    @staticmethod
    def count_users():
        return User.count


class ShoppingList(object):
    count = 0

    def __init__(self, list_name, owner, shopping_list_id=None):
        self.list_name = list_name
        self.owner = owner
        self.shopping_list_id = uuid.uuid4().hex if shopping_list_id is None else shopping_list_id

        self.info = {
            'list_name': self.list_name,
            'owner': self.owner,
            'shopping_list_id': self.shopping_list_id,
        }

        ShoppingList.count += 1

    def view_info(self):
        return self.info

    def return_owner_name(self):
        return self.owner

    def update_name(self, new_title):
        self.list_name = new_title
        return new_title


class Item(object):
    count = 0

    def __init__(self, item_name, owner, item_id=None):
        self.item_name = item_name
        self.owner = owner
        self.item_id = uuid.uuid4().hex if item_id is None else item_id

        self.info = {
            'item_name': self.item_name,
            'owner': self.owner,
            'item_id': self.item_id,
        }
        Item.count += 1

    def view_info(self):
        return self.info

    def update_name(self, new_title):
        self.item_name = new_title
        return new_title


class Data ():
    users = [{'username': None, 'first_name': None, 'last_name': None, 'email': None,
              'password': None, 'user_id': None, 'shopping_lists': None}]

    def create_user(self, username, email, first_name, last_name, password):
        created_user = User(username, email, first_name, last_name, password)
        created_user_info = created_user.view_info()
        for user in self.users:
            if created_user_info['email'] == user['email']:
                return 'You already have an account'
            elif created_user_info['username'] == user['username']:
                return 'Username already in use'
            else:
                self.users.append(created_user_info)
            return 'Account successfully created'

    def get_user(self, user_id):
        for user in self.users:
            if user['user_id'] == user_id:
                return user

    def create_shoppinglist(self, user_id, name):

        created_shopping_list = ShoppingList(name)
        created_shopping_list_info = created_shopping_list.view_info()
        user = self.get_user(user_id)

        user['shopping_lists'].append(created_shopping_list_info)
        return "Shopping list " + str(name) + " Created"

    def view_shoppinglist(self, user_id, item_id):
        user = self.get_user(user_id)

        for item in user['shopping_lists']:
            if item['id'] == item_id:
                return item

    def delete_shoppinglist(self, user_id, item_id):
        user = self.get_user(user_id)

        for item in user['shopping_lists']:
            if item['id'] == item_id:
                user['shopping_lists'].remove(item)

    def create_shoppinglist_items(self, user_id, shoppinglist_id, item_name, quantity):
        """
            Method to add shopping items to a shopping list
        """
        created_shopping_list_item = Item(item_name, quantity)
        created_shopping_list_item_info = created_shopping_list_item.view_info()
        user = self.get_user(user_id)
        for shoppinglist in user['shopping_lists']:
            if shoppinglist['id'] == int(shoppinglist_id):
                current_shopinglist = shoppinglist
                for item in current_shopinglist['items']:
                    if item['name'] == item_name:
                        return "This item name already exits. Try editing it"
                current_shopinglist['items'].append(created_shopping_list_item_info)
                return str(item_name) + " has been created"

    def get_shoppingitem(self, user_id, shoppinglist_id, item_id):
        """Method to get a single item from the shopping list"""
        shopping_list = self.view_shoppinglist(user_id, shoppinglist_id)
        for item in shopping_list['items']:
            if item['id'] == item_id:
                return item

    def delete_shoppingitem(self, user_id, shoppinglist_id, item_id):
        """Method to delete an item from the shoppinglist"""
        shopping_list = self.view_shoppinglist(user_id, shoppinglist_id)
        for item in shopping_list['items']:
            if item['id'] == int(item_id):
                shopping_list['items'].remove(item)