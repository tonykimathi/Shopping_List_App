<<<<<<< HEAD
from flask import render_template, redirect, url_for, flash, session, request
=======
from flask import render_template, redirect, url_for, flash, session
>>>>>>> 1fbc4184b5613da734d9decbe7ec07178c48f828
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegisterForm, LoginForm
from app.models import User
from app.models import ShoppingList
from app import app

<<<<<<< HEAD
users = []
shoppinglists = []

#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_message = "You must be logged in to access this page."
#login_manager.login_view = "login"


#@login_manager.user_loader
#def load_user(email):

 #   return User.check_user(email)
=======
>>>>>>> 1fbc4184b5613da734d9decbe7ec07178c48f828

shoppinglists = []
users = []

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    error = None
    form = RegisterForm()
    if form.validate_on_submit():
        for i in users:
<<<<<<< HEAD
            if i.username == form.username.data
                error = "Username already in use"


        password = generate_password_hash(form.password.data, method='sha256')

        new_user = User(username=form.username.data, first_name=form.first_name,
                        last_name=form.last_name, email=form.email.data, password=password)

        flash('You have been registered!  {} '.format(username), 'successfully')
=======
            if i.username == form.username.data:
                error = 'Username already exists'
                return render_template('Sign Up.html',
                           form=form,
                           error = error
                           )
        Count_users = len(users)
        new_user = User(form.username.data, form.email.data, form.password.data)
        users.append(new_user)
        session['username'] = new_user.username
        flash "You have been registered successfully"
>>>>>>> 1fbc4184b5613da734d9decbe7ec07178c48f828
        return redirect(url_for('dashboard'))
    return render_template('Sign Up.html',
                           form=form,
                           error = error
                           )
                

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ The user login method"""
    error = None
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        for user in users:
            if user.password == form.password.data:
                if user.password == form.password.data:
                    session['username'] = user.username
                    flash "You have been logged in successfully"
                    return redirect(url_for('dashboard'))
                error = 'Invalid password'
            error = 'Invalid username'
    return render_template('login.html',
                           form=form,
                           error=error
                           )

@app.route('/dashboard')
@login_required
def dashboard():
    if 'username' in session:
        if session['username'] not in shoppinglists:
            shoppinglists[session['username']] = []
        return render_template(
            'dashboard.html',
            data = shoppinglists[session['username']],
            user = session['username'])
    else:
        return redirect(url_for('login')) 


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out!')
    return redirect(url_for('login'))

@app.route('/dashboard/create_shoppinglist', methods=['POST'])
@login_required
def create_shoppinglist():
    if session['username'] in shoppinglists:
        data = request.form.to_dict()
        shopping_list = data['shopping_list']
        count_lists = (shoppinglists[session['username']])
        new_shoppinglist = ShoppingList(shopping_list, count_lists)
        shoppinglists[session['username']].append(new_shoppinglist)
        return redirect(url_for('dashboard')) 

@app.route('/bucket/<bucket_id>', methods=['GET', 'POST'])
@login_required
def view_shoppinglist(shoppinglist_id):

    shoppinglist = [
        i for i in buckets[session['username']] if str(i.Id) == bucket_id
    ]
    shoppinglist = shoppinglist[0]
    return render_template('shoppinglist.html', bucket=bucket)



@app.route('/shoppinglist/<shoppinglist_id>/create_item', methods=['GET', 'POST'])
@login_required
def create_item(shoppinglist_id):
    data = request.form.to_dict()
    item = data['item']
    shoppinglist = [
        i for i in shoppinglists[session['username']] if str(i.Id) == shoppinglist_id
    ]
    shoppinglist = shoppinglist[0]
    shoppinglist.add_item(item)
    return redirect('/shoppinglist/' + shoppinglist_id)


@app.route('/shoppinglist/edit_shoppinglist/<shoppinglist_id>/', methods=['POST'])
@login_required
def edit_shoppinglist(shoppinglist_id, item_id):
    if request.method == 'POST':
        title = request.form['title']
        shoppinglist = [
            i for i in shoppinglists[session['username']] if str(i.Id) == shoppinglist_id
        ]
        shoppinglist = shoppinglist[0]
        shoppinglist.update_name(title)
        return redirect(url_for('dashboard'))
 


@app.route('/shoppinglist/<shoppinglist_id>/edit_item/<item_id>', methods=['GET', 'POST'])
@login_required
def edit_shoppinglist_item(shoppinglist_id, item_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        new_text = data['new_text']
        shoppinglist = [
            i for i in shoppinglists[session['username']] if str(i.Id) == shoppinglist_id
        ]
        shoppinglist = shoppinglist[0]
        item = [i for i in shoppinglist.items if str(i['Id']) == item_id]
        item = item[0]
        shoppinglist.update_item(item_id, new_text)
        return redirect('/shoppinglist/' + shoppinglist_id)


@app.route('/delete/<shoppinglist_id>/')
@login_required
def delete_shoppinglist(shoppinglist_id):
    for i in shoppinglists[session['username']]:
        if str(i.Id) == shoppinglist_id:
            shoppinglists[session['username']].remove(i)
    return redirect(url_for('dashboard'))


@app.route('/delete_item/<item_id>/')
@login_required
def delete_item(shoppinglist_id, item_id):

    if request.method == 'POST':
        shoppinglist = [
            i for i in shoppinglists[session['username']] if str(i.Id) == shoppinglist_id
        ]
        shoppinglist = shoppinglist[0]
        item = [i for i in shoppinglist.items if str(i['Id']) == shoppinglist_id]
        shoppinglist.remove_item(item_id)
        return redirect('/shoppinglist/' + bucket_id)
