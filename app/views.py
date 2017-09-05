from flask import render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegisterForm, LoginForm
from app.models import User
from app.models import ShoppingList
from app import app

users = []
shoppinglists = []

#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_message = "You must be logged in to access this page."
#login_manager.login_view = "login"


#@login_manager.user_loader
#def load_user(email):

 #   return User.check_user(email)


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
            if i.username == form.username.data
                error = "Username already in use"


        password = generate_password_hash(form.password.data, method='sha256')

        new_user = User(username=form.username.data, first_name=form.first_name,
                        last_name=form.last_name, email=form.email.data, password=password)

        flash('You have been registered!  {} '.format(username), 'successfully')
        return redirect(url_for('dashboard'))

    return render_template('Sign Up.html',
                           form=form
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ The user login method"""
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        user = User.check_user(form.email.data)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('You have been logged in successfully')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid Login!! Password or Email incorrect', 'error')
                return redirect(url_for('login'))
        else:
            flash("Email does not exist!! Register first")
            return redirect(url_for('sign_up'))
    return render_template('login.html',
                           form=form
                           )


@app.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out!')
    return redirect(url_for('login'))

@app.route('/create_shoppinglist', methods=['GET', 'POST'])
@login_required
def create_shoppinglist():
    form = TextForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            title = form.title.data
            body = form.body.data
            current_user.create_shoppinglist(title, body)
            flash(' You have created a shoppinglist', 'success')
            return redirect(url_for('dashboard'))
        return render_template('create.html',
                           form=form)
    return redirect(url_for('index'))


@app.route('/create_item/<string:_id>/', methods=['GET', 'POST'])
@login_required
def create_item(_id):
    form = TextForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            title = form.title.data
            body = form.body.data
            current_user.create_shoppinglist(title, body)
            flash(' You have created a shoppinglist item', 'success')
            return redirect(url_for('shoppinglist_items', _id=_id))
        return render_template('add_item.html',
                           form=form)
    return redirect(url_for('index'))


@app.route('/edit_shoppinglist/<string:_id>/', methods=['GET', 'POST'])
@login_required
def edit_shoppinglist(_id):
    form = TextForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            title = form.title.data
            body = form.body.data
            current_user.edit_shoppinglist(title, body)
            flash(' You have edited your shoppinglist', 'success')
            return redirect(url_for('dashboard'))
        return render_template('create.html', form=form)
    return redirect(url_for('index'))


@app.route('/edit_bucketlist_item/<string:_id>/', methods=['GET', 'POST'])
@login_required
def edit_shoppinglist_item(_id):
    form = TextForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            title = form.title.data
            body = form.body.data
            current_user.edit_shoppinglist(title, body)
            flash(' You have edited this shoppinglist item', 'success')
            return redirect(url_for('dashboard'))
        return render_template('create.html', form=form)
    return redirect(url_for('index'))

@app.route('/items/<string:_id>/')
@app.route('/items/')
@login_required
def bucketlist_items(_id):


    bucketlist_ = Data.get_the_data(_id, Data.bucketlists)
    items = Data.get_the_data(_id, Data.items)
    notify = 'You have no items in this bucketlist yet'
    return render_template('items.html',
                           items=items,
                           notify=notify,
                           bucketlist_=bucketlist_,
                           title=page_title)

@app.route('/delete/<string:_id>/')
def delete_shoppinglist(_id):


    flash('Shoppinglist deleted', 'Danger')
    return redirect(url_for('dashboard'))


@app.route('/delete_item/<string:_id>/')
def delete_item(_id):


    flash('Item deleted', 'Danger')
    return redirect(url_for('shoppinglist_items', _id=b_id))