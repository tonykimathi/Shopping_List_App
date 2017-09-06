
import uuid


class User(object):
    users = []
    count = 0

    def __init__(self, username, email, first_name, last_name, password, user_id=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.user_id = uuid.uuid4().hex if user_id is None else user_id

        User.count += 1

    def view_info(self):
        return self.info

    def return_user_name(self):
        return self.username

    @staticmethod
    def count_users():
        return User.count


class ShoppingList(object):

    def __init__(self, list_name, owner, count=0, shopping_list_id=None):
        self.list_name = list_name
        self.owner = owner
        self.list_content = []
        self.count = count
        self.shopping_list_id = uuid.uuid4().hex if shopping_list_id is None else shopping_list_id

    def return_owner_name(self):
        return self.owner

    def update_name(self, new_title):
        self.list_name = new_title
        return new_title


class Item(object):

    def __init__(self, item_name, owner, count=0, item_id=None):
        self.list_name = item_name
        self.owner = owner
        self.item_content = []
        self.count = count
        self.item_id = uuid.uuid4().hex if item_id is None else item_id

    def add_item(self, item):
        self.item_content.append({"Id": self.count, "body": item})
        self.count += 1

    def update_item(self, item_id, item):
        for i in self.item_content:
            if str(i['Id']) == item_id:
                i['body'] = item

    def remove_item(self, item_id):
        for i in self.item_content:
            if str(i['Id']) == item_id:
                self.item_content.remove(i)
