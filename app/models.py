class User(object):


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.__password = password





class ShoppingList():

    shopping_list = []

    shopping_lists = []

    def __init__(self, bucket_name, shopping_list_id):
        self.bucket_name = bucket_name
        self.shopping_list_id = shopping_list_id

    def create_list(self, ):


    def edit_list(self, ):


    def view_list(self, ):


    def delete_list(self, ):




class Item(ShoppingList):


    def __init__(self, item_name, item_id):
        self.item_name = item_name
        self.item_id = item_id


    def add_item(self):
        for self.item_name in shopping_list:
            shopping_list.append(self.item_name)



    def remove_item(self):
        for self.item_name in shopping_list:
            shopping_list.remove(self.item_name)


    def view_items(self):
        return shopping_list

