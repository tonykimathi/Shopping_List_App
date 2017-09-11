import uuid
from werkzeug.security import check_password_hash
import datetime


class User(object):

    def __init__(self, username, email, password, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def check_user_exists(email):
        data = [user['email'] for user in Data.users if email == user['email']]
        email_entered = "".join(data)
        if email_entered == email:
            return True
        return False

    @staticmethod
    def verify_user_login_(email, password):

        user_exists = User.check_user_exists(email)
        if user_exists is True:
            emails_password = "".join([user['password'] for user in Data.users if email == user['email']])
            return check_password_hash(emails_password, password)
        return False

    @staticmethod
    def get_username(email):
        username = [user['username'] for user in Data.users if email == user['email']]
        user_name = "".join(username)
        return user_name

    @classmethod
    def sign_up_user(cls, username, email, password):
        user = cls.check_user_exists(email)
        if user is False:
            registered_user = cls(username, email, password)
            registered_user.save_to_users()
            return True
        return False

    def user_data(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            '_id': self._id
        }

    def create_shoppinglist(self, title):
        shopping_list = ShoppingList(owner_id=self._id, title=title, owner=self.username)
        shopping_list.save_to_shoppinglists()

    @staticmethod
    def create_item(_id, item_name, quantity):

        shoppinglist_data = Data.get_the_data(_id, Data.shoppinglists)
        for data in shoppinglist_data:
            shoppinglist = ShoppingList(data['title'], data['owner'], data['owner_id'], data['_id'])
            shoppinglist.new_item(item_name=item_name, quantity=quantity)

    def save_to_users(self):
        Data.add_data(self.user_data())

    @staticmethod
    def current_user(email):
        for user in Data.users:
            if email == user['email']:
                return user


class ShoppingList(object):

    def __init__(self, title, owner, owner_id, _id=None):
        self.title = title
        self.owner = owner
        self.owner_id = owner_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_item(self, item_name, quantity, date=datetime.datetime.utcnow()):
        item = Item(item_name=item_name,
                    quantity=quantity,
                    owner_id=self._id,
                    date=date)
        item.save_to_items()

    def shoppinglist_data(self):
        return {
            'title': self.title,
            '_id': self._id,
            'owner': self.owner,
            'owner_id': self.owner_id
        }

    def save_to_shoppinglists(self):
        Data.add_data(self.shoppinglist_data())


class Item(object):
    def __init__(self, item_name, quantity, owner_id, date, _id=None):
        self.item_name = item_name
        self.quantity = quantity
        self.owner_id = owner_id
        self.date = date
        self._id = uuid.uuid4().hex if _id is None else _id

    def item_data(self):
        return {
            '_id': self._id,
            'item_name': self.item_name,
            'quantity': self.quantity,
            'owner_id': self.owner_id,
            'date': self.date
        }

    def save_to_items(self):
        Data.add_data(self.item_data())


class Data(object):
    users = []
    shoppinglists = []
    items = []

    @staticmethod
    def add_data(arg):
        if 'email' in arg:
            Data.users.append(arg)
        elif 'title' in arg:
            Data.shoppinglists.append(arg)
        elif 'item_name' in arg:
            Data.items.append(arg)

    @staticmethod
    def get_the_data(_id, arg):
        data_retrieved = [data for data in arg if _id == data['_id'] or _id == data['owner_id']]
        return data_retrieved

    @staticmethod
    def get_index(_id, arg):
        dict_index = [index for index in arg if _id == index['_id']]
        dict_index = arg.index(dict_index[0])
        return dict_index

    @staticmethod
    def delete_dictionary(_id, arg):
        dict_index = Data.get_index(_id, arg)
        del arg[dict_index]