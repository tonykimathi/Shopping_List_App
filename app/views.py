from flask import render_template, redirect, url_for, flash, session, request, abort
from functools import wraps
from app.forms import RegisterForm, LoginForm, TextForm
from app.models import Data
from app import app, data


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to log in first")
            return redirect(url_for('login_user'))
    return wrap


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    error = None
    form = RegisterForm()
    if form.validate_on_submit():
        data.create_user(form.username.data, form.email.data, form.password.data,
                         form.first_name.data, form.last_name.data)
        for user in users:
            session['username'] = user.username
        flash("Account successfully created")
        return redirect(url_for('dashboard'))
    return render_template('Sign Up.html', form=form, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ The user login method"""
    error = None
    form = LoginForm()

    if form.validate_on_submit():
        for user in users:
            if user.email == form.email.data:
                if user.password == form.password.data:
                    session['username'] = user.username
                    flash("You have been logged in successfully")
                    return redirect(url_for('dashboard'))
            error = 'Invalid email/password'
    return render_template('login.html',
                           form=form,
                           error=error
                           )


@app.route('/dashboard')
@login_required
def dashboard():
    if session['logged_in'] is True:
        create_shoppinglist = True

        form = TextForm()

        for user in users:
            session['username'] = user.username
        notify = 'You have no shopping lists yet'
        return render_template(
            "dashboard.html",
            notify=notify,
            form=form)
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('You were logged out!')
    return redirect(url_for('login'))

@app.route('/create_bucketlist/', methods=['GET', 'POST'])
@user_in_session
def create_bucketlist():
    """creates a bucketlist"""
    page_title = "Add"
    form = TextForm(request.form)
    user = User(session['username'],
                session['email'],
                session['password'],
                session['id'])
    if request.method == 'POST' and form.validate():
        title = form.title.data
        intro = form.body.data
        user.create_bucketlist(title, intro)
        flash(' You have created a bucketlist', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create.html',
                           form=form,
                           title=page_title)


@app.route('/create_item/<string:_id>/', methods=['GET', 'POST'])
@user_in_session
def create_item(_id):
    """creates an item"""
    page_title = "Add"
    form = TextForm(request.form)
    if request.method == 'POST' and form.validate():
        item_name = form.title.data
        description = form.body.data
        User.create_item(_id, item_name, description)
        flash(' You have created a bucketlist item', 'success')
        return redirect(url_for('bucketlist_items', _id=_id))
    return render_template('add_item.html',
                           form=form,
                           title=page_title)


@app.route('/dashboard/')
@app.route('/bucketlists/')
@user_in_session
def dashboard():
    """method for displaying users bucketlists"""
    page_title = "Dashboard"
    bucketlists = Data.get_the_data(session['id'], Data.bucketlists)
    notify = 'You have no bucketlists yet'
    return render_template('dashboard.html',
                           bucketlists=bucketlists,
                           notify=notify,
                           username=session['username'],
                           title=page_title)


@app.route('/items/<string:_id>/')
@app.route('/items/')
@user_in_session
def bucketlist_items(_id):
    """method used for displaying a bucketlists items"""
    page_title = "Items"
    bucketlist_ = Data.get_the_data(_id, Data.bucketlists)
    items = Data.get_the_data(_id, Data.items)
    notify = 'You have no items in this bucketlist yet'
    return render_template('items.html',
                           items=items,
                           notify=notify,
                           bucketlist_=bucketlist_,
                           title=page_title)


@app.route('/edit_bucketlist/<string:_id>/', methods=['GET', 'POST'])
@user_in_session
def edit_bucketlist(_id):
    """method lets the user  edit existing buckelists"""
    page_title = "Edit"
    index_ = Data.get_index(_id, Data.bucketlists)
    form = TextForm(request.form)

    form.title.data = Data.bucketlists[index_]['title']
    form.body.data = Data.bucketlists[index_]['intro']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        intro = request.form['body']
        Data.bucketlists[index_]['title'] = title
        Data.bucketlists[index_]['intro'] = intro
        flash('Your Bucketlist has been updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create.html', form=form, title=page_title)


@app.route('/edit_bucketlist_item/<string:_id>/', methods=['GET', 'POST'])
@user_in_session
def edit_bucketlist_item(_id):
    """method lets the user  edit existing buckelists"""
    page_title = "Edit"
    index_ = Data.get_index(_id, Data.items)
    form = TextForm(request.form)

#    ### populating the form for user to edit ###

    form.title.data = Data.items[index_]['item_name']
    form.body.data = Data.items[index_]['description']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        intro = request.form['body']
        Data.items[index_]['item_name'] = title
        Data.items[index_]['description'] = intro
        flash('Your Item has been updated', 'success')
        return redirect(url_for('bucketlist_items',
                                _id=Data.items[index_]['owner_id']))
    return render_template('add_item.html', form=form, title=page_title)


@app.route('/delete/<string:_id>/')
def delete_bucketlist(_id):
    """ deletes a bucketlist and its items"""
    Data.delete_dictionary(_id, Data.bucketlists)
    all_items = Data.get_the_data(_id, Data.items)
    if all_items is not None:
        for item in all_items:
            if item['_id'] in Data.items:
                Data.delete_dictionary(item['_id'], Data.items)
    flash('Bucketlist deleted', 'Danger')
    return redirect(url_for('dashboard'))


@app.route('/delete_item/<string:_id>/')
def delete_item(_id):
    """ deletes a bucketlist and its items"""
    index_ = Data.get_index(_id, Data.items)
    b_id = Data.items[index_]['owner_id']
    Data.delete_dictionary(_id, Data.items)
    flash('Item deleted', 'Danger')
    return redirect(url_for('bucketlist_items', _id=b_id))
