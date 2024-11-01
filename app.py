import os

from flask import Flask, render_template, redirect, url_for, session, flash, g
from models import db, connect_db, User, Property, Favorites
from forms import SignupForm, LoginForm, UserEditForm
from sqlalchemy.exc import IntegrityError
from functools import wraps

import requests

from dotenv import load_dotenv

load_dotenv()  # This will load your .env file variables

app = Flask(__name__)

# Configuration settings

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///real_estate_dashboard')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

API_KEY = os.environ.get('API_KEY')
CURR_USER_KEY = 'curr_user'

connect_db(app)


@app.before_request
def add_user_to_g():
    """ If we're logged in, add curr user to Flask global. """

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def login_required(f):

    @wraps(f)
    def check_login(*args, **kwargs):

        if not g.user:
            flash('Access unauthorized.', 'danger')
            return redirect(url_for('homepage'))
        
        return f(*args, **kwargs)

    return check_login


def do_login(user):
    """ Log in user """

    session[CURR_USER_KEY] = user.id


def do_logout():
    """ Log out user """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


def save_properties_to_database(properties):
    for prop in properties:

        new_prop = Property(
            zpid=prop["zpid"],
            address=prop["address"],
            price=prop["price"],
            bedrooms=prop["bedrooms"],
            bathrooms=prop["bathrooms"],
            living_area=prop["livingArea"],
            image_src=prop["imgSrc"],
        )

        db.session.add(new_prop)
    db.session.commit()


@app.route('/')
def homepage():

    properties = Property.query.all()

    return render_template('home.html', properties=properties)


### USERS ROUTES

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data, 
                email=form.email.data, 
                password=form.password.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)
        return redirect(url_for('homepage'))

    return render_template('/users/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(url_for('homepage'))

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

    
@app.route('/logout')
def logout():
    """Handle logout of user."""

    flash("You have been logout.", 'primary')
    do_logout()
    return redirect(url_for('login'))


@app.route('/users/profile', methods=['GET'])
@login_required
def profile():

    form = UserEditForm()

    return render_template('users/edit.html', form=form)


### PROPERTIES ROUTES

@app.route('/properties/<int:prop_id>', methods=['GET'])
def prop_detail(prop_id):

    prop = Property.query.get_or_404(prop_id)

    return render_template('/properties/detail.html', prop=prop)

### FETCH DATA FROM API

@app.route('/api/properties', methods=['GET'])
def get_properties():

    # Get a list of properties by providing Zillow's search results URL

    url = 'https://zillow-com1.p.rapidapi.com/propertyExtendedSearch'

    querystring = {"location":"Los Angeles, CA","status_type":"ForSale"}

    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'zillow-com1.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        properties_data = response.json().get('props')
        save_properties_to_database(properties_data)

        return properties_data

    else:
        return ("Error: Unable to fetch data"), 500