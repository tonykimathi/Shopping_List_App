import uuid


class User(object):
    count = 0

    """main user class"""

    def __init__(self, username, email, password, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def user_exists(email):
        """method checks if the user already exist"""
        data = [i['email'] for i in Data.users if email == i['email']]
        return "".join(data) == email

    @staticmethod
    def user_login_verify(email, password):
        """ methods verifys user password and email"""
        user_exist = User.user_exists(email)
        if user_exist is True:
            emails_password = "".join([i['password'] for i in Data.users if email == i['email']])
            return check_password_hash(emails_password, password)
        return False

    @staticmethod
    def get_username(email):
        """Gets users username for use in session at login"""
        username = [i['username'] for i in Data.users if email == i['email']]
        return "".join(username)

    @classmethod
    def register(cls, username, email, password):
        """method registers a user to the app"""
        user = cls.user_exists(email)
        if user is False:
            new_user = cls(username, email, password)
            new_user.save_to_users()
            return True
        else:
            return False

    def user_data(self):
        """ The method returns user data to be saved"""
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            '_id' : self._id
        }

    def create_bucketlist(self, title, intro):
        """method used for creating a bucketlist"""
        bucketlist_ = Bucketlist(owner_id=self._id,
                                 title=title,
                                 intro=intro,
                                 owner=self.username)
        bucketlist_.save_to_bucketlists()

    @staticmethod
    def create_item(_id, item_name, description):
        """method used to create bucketlist items"""
        data_ = Data.get_the_data(_id, Data.bucketlists)
        for data in data_:
            bucketlist = Bucketlist(data['title'],
                                    data['owner'],
                                    data['intro'],
                                    data['owner_id'],
                                    data['_id'])
            bucketlist.new_item(item_name=item_name,
                                description=description)

    def save_to_users(self):
        """this method saves the user to users"""
        Data.add_data(self.user_data())

    @staticmethod
    def current_user(email):
        """
        method gets user details using the session username to create the instance
         of the user logged so as to create a bucketlist"""
        for user in Data.users:
            if email == user['email']:
                return user


class ShoppingList(object):
    count = 0

    def __init__(self, title, owner, intro, owner_id, _id=None):
        self.title = title
        self.intro = intro
        self.owner = owner
        self.owner_id = owner_id
        self._id = uuid.uuid4().hex if _id is None else _id


    def new_item(self, item_name, description, date=datetime.datetime.utcnow()):
        """method used for creating a  bucket list"""
        item = Item(item_name=item_name,
                    description=description,
                    owner_id=self._id,
                    date=date)
        item.save_to_items()

    def bucketlist_data(self):
        """this method returns bucketlist data to be saved"""
        return {
            'title' : self.title,
            'intro': self.intro,
            '_id' : self._id,
            'owner' : self.owner,
            'owner_id' : self.owner_id
        }

    def save_to_bucketlists(self):
        """this methods saves data to the bucketlists list"""
        Data.add_data(self.bucketlist_data())


class Item(object):
    def __init__(self, item_name, description, owner_id, date, _id=None):
        self.item_name = item_name
        self.description = description
        self.owner_id = owner_id
        self.date = date
        self._id = uuid.uuid4().hex


    def item_data(self):
        """returns the data to be saved to items list"""
        return {
            '_id' : self._id,
            'item_name' : self.item_name,
            'description' : self.description,
            'owner_id' : self.owner_id,
            'date' : self.date
        }

    def save_to_items(self):
        """this method saves data to the item list"""
        Data.add_data(self.item_data())


class Data(object):
    """ main data class """
    users = []
    bucketlists = []
    items = []

    @staticmethod
    def add_data(arg):
        """method for appending items to their respective lists"""
        if 'email' in arg:
            Data.users.append(arg)
        elif 'title' in arg:
            Data.bucketlists.append(arg)
        elif 'item_name' in arg:
            Data.items.append(arg)

    @staticmethod
    def get_the_data(_id, arg):
        """this method uses id attribute to get the dictionary"""
        data_ = [i for i in arg if _id == i['_id']\
         or _id == i['owner_id']]
        return data_

    @staticmethod
    def get_index(_id, arg):
        """gets the index of a dictionary in a list"""
        index_data = [i for i in arg if _id == i['_id']]
        _index = arg.index(index_data[0])
        return _index

    @staticmethod
    def delete_dictionary(_id, arg):
        """ deletes the dictionary in a list"""
        index_ = Data.get_index(_id, arg)
        del arg[index_]