
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



#    def add_item(self, item):
#        self.item_content.append({"Id": self.count, "body": item})
#        self.count += 1

#    def update_item(self, item_id, item):
#        for i in self.item_content:
#            if str(i['Id']) == item_id:
 #               i['body'] = item

#    def remove_item(self, item_id):
#        for i in self.item_content:
#            if str(i['Id']) == item_id:
 #               self.item_content.remove(i)


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

    def create_shoppinglist(self):

        create_shopping_list = ShoppingList()


    def add_shoppinglist(self, user_id, name):
        """
            Method to add shoppinglists to a user given the id of the
            user
        """
        new_shoppinglist = ShoppingList(name)
        new_shoppinglist_details = new_shoppinglist.get_details()
        user = self.get_single_user(user_id)
        new_shoppinglist_details['id'] = len(user['shopping_lists']) + 1
        for item in user['shopping_lists']:
            if item['name'] == name:
                return "Shopping list " + str(name) + " exits. Try editing it"
            if new_shoppinglist_details['id'] == item['id']:
                new_shoppinglist_details['id'] = new_shoppinglist_details['id']
                + 1
        user['shopping_lists'].append(new_shoppinglist_details)
        return "Shopping list " + str(name) + " Created"

    def get_shoppinglist(self, user_id, item_id):
        """
            Method to return a single user item based on the user
            item's id and its user's id
        """
        single_user = self.get_single_user(user_id)
        for item in single_user['shopping_lists']:
            if item['id'] == item_id:
                return item

    def remove_shoppinglist(self, user_id, item_id):
        """
            Method to delete a user item based on its id and its
            user's id
        """
        single_user = self.get_single_user(user_id)
        for item in single_user['shopping_lists']:
            if item['id'] == int(item_id):
                single_user['shopping_lists'].remove(item)

    def add_shoppingitems(self, user_id, shoppinglist_id, name, quantity):
        """
            Method to add shopping items to a shopping list
        """
        new_shoppingitem = ShoppingItem(name, quantity)
        new_shoppingitem_details = new_shoppingitem.get_details()
        user = self.get_single_user(user_id)
        for shopinglist in user['shopping_lists']:
            if shopinglist['id'] == int(shoppinglist_id):
                curr_shopinglist = shopinglist
                new_shoppingitem_details['id'] = len(curr_shopinglist['items']) + 1
                for item in curr_shopinglist['items']:
                    if item['name'] == name:
                        return "Item " + str(name) + " exits. Try editing it"
                    if new_shoppingitem_details['id'] == item['id']:
                        new_shoppingitem_details['id'] = new_shoppingitem_details['id'] + 1
                curr_shopinglist['items'].append(new_shoppingitem_details)
                return str(name) + " has been added"

    def get_shoppingitem(self, user_id, shoppinglist_id, item_id):
        """Method to get a single item from the shopping list"""
        shoppinglist = self.get_shoppinglist(user_id, shoppinglist_id)
        for item in shoppinglist['items']:
            if item['id'] == item_id:
                return item

    def remove_shoppingitem(self, user_id, shoppinglist_id, item_id):
        """Method to delete an item from the shoppinglist"""
        shoppinglist = self.get_shoppinglist(user_id, shoppinglist_id)
        for item in shoppinglist['items']:
            if item['id'] == int(item_id):
                shoppinglist['items'].remove(item)