
import uuid


class User(object):
    users = []

    def __init__(self, username, email, first_name, last_name, password, Id=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.Id = uuid.uuid4().hex if Id is None else Id

    def return_user_name(self):
        return self.username




class ShoppingList(object):

    def __init__(self, list_name, owner, count=0, content = [], Id=None):
        self.list_name = list_name
        self.owner = owner
        self.content = content
        self.count = count
        self.Id = uuid.uuid4().hex if _id is None else _id

    def return_owner_name(self):
        return self.owner

    def update_name(self, new_title):
        self.list_name = new_title
	return new_title

    def add_item(self, item):
        self.content.append({"Id": self.count, "body": item})
        self.count += 1

    def update_item(self, Id, item):
        for i in self.content:
            if str(i['Id']) == Id:
                i['body'] = item

    def remove_item(self, Id):
        for i in self.content:
            if str(i['Id']) == Id:
                self.content.remove(i)




