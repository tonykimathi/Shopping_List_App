from flask import render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash
from functools import wraps
from app.forms import RegisterForm, LoginForm, TextForm
from app.models import Data, User
from app import app


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to log in first")
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@app.route('/index')
def index():
    title = "Home"
    return render_template('index.html', title=title)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    title = "Sign Up"
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)

        if User.sign_up_user(username, email, password) is True:
            user = User.current_user(email)
            session['logged_in'] = True
            session['username'] = username
            session['id'] = user['_id']

            flash('{}, You have successfully signed up '.format(username))
            print(Data.users)
            return redirect(url_for('dashboard'))
        else:
            flash('You already have an account! Please log in')

    return render_template('Sign Up.html', form=form, title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        if User.check_user_exists(email):
            if User.verify_user_login_(email, password):
                session['logged_in'] = True
                session['email'] = email
                session['password'] = password
                session['username'] = username

                flash("You have been logged in successfully")
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password or email!')
                return redirect(url_for('login'))
        else:
            flash('Email does not exist! Please Sign Up')
            return redirect(url_for('sign_up'))
    return render_template('login.html', form=form, title=title)


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('You were logged out!')
    return redirect(url_for('login'))


@app.route('/create_shoppinglist/', methods=['GET', 'POST'])
@login_required
def create_shoppinglist():
    title = "Create Shopping List"
    form = TextForm()
    user = User(session['email'], session['password'], session['username'])
    if form.validate_on_submit():
        title = form.name.data
        content = form.content.data
        user.create_shoppinglist(title, content)
        flash(' You have successfully created a shopping list')
        return redirect(url_for('dashboard'))
    return render_template('create_list.html',
                           form=form,
                           title=title)


@app.route('/create_item/<string:_id>/', methods=['GET', 'POST'])
@login_required
def create_item(_id):
    title = "Create Shopping List"
    form = TextForm()
    if form.validate_on_submit():
        item_name = form.name.data
        description = form.content.data
        User.create_item(_id, item_name, description)
        flash(' You have created a shopping list item')
        return redirect(url_for('shoppinglist_items', _id=_id))
    return render_template('create_item.html',
                           form=form,
                           title=title)


@app.route('/dashboard')
@login_required
def dashboard():
    title = "Dashboard"
    shopping_lists = Data.get_the_data(session['id'], Data.shoppinglists)
    notify = 'You have no shopping lists yet!'
    return render_template('dashboard.html',
                           shopping_lists=shopping_lists,
                           notify=notify,
                           username=session['username'],
                           title=title)


@app.route('/list_items/<string:_id>/')
@app.route('/list_items/')
@login_required
def shoppinglist_items(_id):
    title = "Items"
    shopping_list = Data.get_the_data(_id, Data.shoppinglists)
    items = Data.get_the_data(_id, Data.items)
    notify = 'You have no items in this shopping list yet'
    return render_template('list_items.html',
                           items=items,
                           notify=notify,
                           shopping_list=shopping_list,
                           title=title)


@app.route('/edit_shoppinglist/<string:_id>/', methods=['GET', 'POST'])
@login_required
def edit_shoppinglist(_id):
    page_title = "Edit"
    index_ = Data.get_index(_id, Data.shoppinglists)
    form = TextForm(request.form)

    form.name.data = Data.shoppinglists[index_]['Name']
    form.content.data = Data.shoppinglists[index_]['Content']

    if form.validate_on_submit():
        title = request.form['title']
        intro = request.form['body']
        Data.shoppinglists[index_]['title'] = title
        Data.shoppinglists[index_]['intro'] = intro
        flash('Your Shopping list has been updated')
        return redirect(url_for('dashboard'))
    return render_template('create_list.html', form=form, title=page_title)


@app.route('/edit_shoppinglist_item/<string:_id>/', methods=['GET', 'POST'])
@login_required
def edit_shoppinglist_item(_id):

    page_title = "Edit"
    index_ = Data.get_index(_id, Data.items)
    form = TextForm()

#    ### populating the form for user to edit ###

    form.name.data = Data.items[index_]['item_name']
    form.content.data = Data.items[index_]['description']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        intro = request.form['body']
        Data.items[index_]['item_name'] = title
        Data.items[index_]['description'] = intro
        flash('Your Item has been updated', 'success')
        return redirect(url_for('shoppinglist_items', _id=Data.items[index_]['owner_id']))
    return render_template('create_item.html', form=form, title=page_title)


@app.route('/delete/<string:_id>/')
def delete_shoppinglist(_id):
    Data.delete_dictionary(_id, Data.shoppinglists)
    all_items = Data.get_the_data(_id, Data.items)
    if all_items is not None:
        for item in all_items:
            if item['_id'] in Data.items:
                Data.delete_dictionary(item['_id'], Data.items)
    flash('Shopping list deleted')
    return redirect(url_for('dashboard'))


@app.route('/delete_item/<string:_id>/')
def delete_item(_id):
    index_ = Data.get_index(_id, Data.items)
    sh_id = Data.items[index_]['owner_id']
    Data.delete_dictionary(_id, Data.items)
    flash('Item deleted', 'Danger')
    return redirect(url_for('shoppinglist_items', _id=sh_id))
