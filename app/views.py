from flask import render_template, redirect, url_for, flash, session, request, abort
from functools import wraps
from app.forms import RegisterForm, LoginForm, TextForm
from app.models import Data
from app import app, data


users = []
shoppinglists = []


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        if "username" in session:
            return f(*args, **kwargs)
        for user in users:
            session['username'] = user.username

        error = "You need to log in first"
        return render_template("login.html", error=error)
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


@app.route('/shoppinglist')
@login_required
def shoppinglist():
    if session['logged_in']:
        return render_template(
            "shoppinglist.html"
        )


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('You were logged out!')
    return redirect(url_for('login'))

@app.route('/create_shoppinglist/', methods=['GET', 'POST'])
@login_required
def create_shoppinglist():
    """creates a shoppinglist"""
    page_title = "Add"
    form = TextForm()
    if form.validate_on_submit():
        for user in users:
            session['username'] = user.username
            title = form.title.data
            intro = form.body.data
            user.create_bucketlist(title, intro)
        flash(' You have created a bucketlist', 'success')
        return redirect(url_for('dashboard'))
    return render_template('shoppinglist.html',
                           form=form,
                           title=page_title)

@app.route('/create_item/<string:_id>/', methods=['GET', 'POST'])
@login_required
def create_item(item_id):
    """creates an item"""
    page_title = "Add"
    form = TextForm()
    if form.validate_on_submit():
        for user in users:
            session['username'] = user.username
            title = form.title.data
            intro = form.body.data
            user.create_bucketlist(title, intro)
        flash(' You have created a bucketlist', 'success')
        return redirect(url_for('dashboard'))
    return render_template('shoppinglist.html',
                           form=form,
                           title=page_title)

@app.route('/dashboard/shopping_list/<shoppinglist_id>')
@login_required
def view_shoppinglists(_id):
    """method used for displaying a bucketlists items"""
    if session['logged_in']:
        view_list = data.view_shoppinglist(user_id=, item_id=)
        items = view_list['items']
        form = TextForm()
        if form.validate_on_submit():
            message = data.add_shoppingitems(
                user_id,
                int(id),
                form.name.data,
                form.quantity.data
            )
            flash(message)
            return redirect(url_for('shoppinglist', id=id))
        return render_template(
            'dashboard.html',
            items=items,
            form=form,
            shoppinglist=view_list
        )
    return redirect(url_for('login'))

@app.route('/dashboard/shopping_list/<item_id>')
@login_required
def view_shoppinglist_items(_id):
    """method used for displaying a bucketlists items"""
    if session['logged_in']:
        view_list = data.view_shoppinglist(user_id=, item_id=)
        items = view_list['items']
        form = TextForm()
        if form.validate_on_submit():
            message = data.add_shoppingitems(
                user_id,
                int(id),
                form.name.data,
                form.quantity.data
            )
            flash(message)
            return redirect(url_for('shoppinglist', id=id))
        return render_template(
            'dashboard.html',
            items=items,
            form=form,
            shoppinglist=view_list
        )
    return redirect(url_for('login'))


@app.route('/dashboard/shopping_list/<shoppinglist_id>')
@login_required
def edit_shoppinglist(id, si_id):
    """Edit a shopping list item"""
    if session['logged_in']:
        item = data.get_shoppinglist(user_id, int(id), int(si_id))
        form = TextForm(dict=item)
        current_shoppinglist = data.get_shoppinglist(user_id, int(id))
        all_items = current_shoppinglist['items']
        if form.validate_on_submit():
            for item in current_shoppinglist['items']:
                if item['name'] == form.name.data:
                    flash('Item already exists')
                    break
            else:
                item['name'] = form.name.data
                item['quantity'] = form.quantity.data
            return redirect(url_for('view_shoppinglist', id=id))
        form.name.data = item['name']
        form.quantity.data = item['quantity']
        return render_template(
            'dashboard.html',
            items=all_items,
            form=form,
            shoppinglist=current_shoppinglist
        )
    else:
        return redirect(url_for('login'))

@app.route('/dashboard/shopping_item/<item_id>')
@login_required
def edit_shoppingitem(id, si_id):
    """Edit a shopping list item"""
    if session['logged_in']:
        item = data.get_shoppingitem(user_id, int(id), int(si_id))
        form = TextForm(dict=item)
        current_shoppingitem = data.get_shoppinglist_item(user_id, int(id))
        all_items = current_shoppingitem['items']
        if form.validate_on_submit():
            for item in current_shoppingitem['items']:
                if item['name'] == form.name.data:
                    flash('Item already exists')
                    break
            else:
                item['name'] = form.name.data
                item['quantity'] = form.quantity.data
            return redirect(url_for('view_shoppinglist', id=id))
        form.name.data = item['name']
        form.quantity.data = item['quantity']
        return render_template(
            'dashboard.html',
            items=all_items,
            form=form,
            shoppingitem=current_shoppingitem
        )
    else:
        return redirect(url_for('login'))

@app.route('/delete/<item_id>/')
def delete_shoppingitem(id, si_id):
    """Delete a shopping list item"""
    if session['logged_in']:
        data.remove_shoppingitem(user_id, int(id), int(si_id))
        return redirect(url_for('dashboard.view_shoppinglist', id=id))
    else:
        abort(401)

@app.route('/delete/<shoppinglist_id>/')
def delete_shoppinglist(id, si_id):
    """Delete a shopping list item"""
    if session['logged_in']:
        data.remove_shoppinglist(user_id, int(id), int(si_id))
        return redirect(url_for('dashboard', id=id))
    else:
        abort(401)
