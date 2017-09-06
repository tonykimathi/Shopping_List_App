from flask import render_template, redirect, url_for, flash, session, request
from functools import wraps
from app.forms import RegisterForm, LoginForm
from app.models import User
from app.models import ShoppingList
from app.models import Item
from app import app


users = []
shoppinglists = []


def login_required(f):
    @wraps(f)
    def verified(*args, **kwargs):

        if "username" in session:
            return f(*args, **kwargs)

        error = "You need to log in first"
        return render_template("index.html", error=error)
    return verified


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
            if i.username == form.username.data:
                error = 'Username already exists'
                return render_template('Sign Up.html', form=form, error=error)
            new_user = User(form.username.data, form.email.data, form.password.data, form.first_name.data,
                            form.last_name.data)
            users.append(new_user)
            session['username'] = new_user.username
            flash("You have been registered successfully")
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
    if 'username' in session:
        if session['username'] not in shoppinglists:
            shoppinglists[session['username']] = []
        return render_template(
            'dashboard.html',
            data=shoppinglists[session['username']],
            user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
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


@app.route('/bucket/<shoppinglist_id>', methods=['GET', 'POST'])
@login_required
def view_shoppinglist(shoppinglist_id):
    shoppinglist = [
        i for i in shoppinglists[session['username']] if str(i.Id) == shoppinglist_id
    ]
    shoppinglist = shoppinglist[0]
    return render_template('shoppinglist.html', shoppinglist=shoppinglist)


@app.route('/shoppinglist/edit_shoppinglist/<shoppinglist_id>/', methods=['POST'])
@login_required
def edit_shoppinglist(shoppinglist_id):
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
        item.update_item(item_id, new_text)
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
def delete_item(item_id):
    if request.method == 'POST':
        itemlist = [
            i for i in shoppinglists[session['username']] if str(i.Id) == item_id
        ]
        itemlist = itemlist[0]
        item = [i for i in itemlist.items if str(i['Id']) == item_id]
        item.remove_item(item_id)
        return redirect('/shoppinglist/' + item_id)
