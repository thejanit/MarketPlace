from MarketPlace import app
from flask import render_template, redirect, url_for, flash, request
from MarketPlace.models import Item, User
from MarketPlace.forms import RegisterForm, LoginForm, BuyingItemForm, SellingItemForm
from MarketPlace import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    items = Item.query.filter_by(owner=None)
    buying_form = BuyingItemForm()
    selling_form = SellingItemForm()

    if request.method == "POST":

        # Buying Item Logic
        buy_item = request.form.get('buy_item')
        b_item_object = Item.query.filter_by(name=buy_item).first()

        if b_item_object:
            if current_user.can_buy(b_item_object):
                b_item_object.bought_owner(current_user)
                flash(f'Congratulations!! You purchased {b_item_object.name} for ₹ {b_item_object.price}', category='success')

            else:
                flash(f"Unfortunately!!, You don't have enough budget to buy {b_item_object.name}!", category='danger')

        # Selling Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()

        if s_item_object:
            if current_user.can_sell(current_user):
                s_item_object.sold_owner(current_user)
                flash(f'Congratulations!! You sold {s_item_object.name} back to market!', category='success')

            else:
                flash(f"Something went wrong!!, You don't have right to sold {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        owned_items = Item.query.filter_by(owner=current_user.id)

        return render_template('market.html', items= items, buying_form=buying_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_created = User(username=form.username.data,
                            email_add=form.email_add.data,
                            password=form.passwd1.data)
        db.session.add(user_created)
        db.session.commit()

        login_user(user_created)
        flash(f'Account created successfully! You ar logged in as {user_created.username}', category='success')

        return redirect(url_for('market_page'))

    if form.errors != {}: #if there are no error from the validations
        for error_msg in form.errors.values():
            flash(f'There was an error with creation a user: {error_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.passwd.data):
            login_user(attempted_user)
            flash(f'You have successfully logged in: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))

        else:
            flash('Username and Password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You hav been logged out!', category='info')
    return redirect(url_for('home_page'))