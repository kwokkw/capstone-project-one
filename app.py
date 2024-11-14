import os

from flask import Flask, render_template, redirect, url_for, session, flash, g, jsonify
from models import db, connect_db, User, Property, Favorites
from forms import SignupForm, LoginForm, UserEditForm
from sqlalchemy.exc import IntegrityError
from functools import wraps
from flask_debugtoolbar import DebugToolbarExtension

import requests

from dotenv import load_dotenv

load_dotenv()  # This will load your .env file variables

app = Flask(__name__)

# Configuration settings

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///real_estate_dashboard')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


API_KEY = os.environ.get('API_KEY')
CURR_USER_KEY = 'curr_user'

connect_db(app)
debug = DebugToolbarExtension(app)


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
            # image_src=prop["imgSrc"],
        )

        db.session.add(new_prop)
    db.session.commit()


@app.route('/')
def homepage():

    properties = Property.query.all()
    loginForm = LoginForm()
    signupForm = SignupForm()

    return render_template('home.html', properties=properties, loginForm=loginForm, signupForm=signupForm)


### USERS ROUTES

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        # Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            form.username.errors.append("Username already taken")

        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already taken", 'danger')
            return render_template('users/signup.html', form=form)

        # If no conflicts, proceed to create the new user
        try:
            user = User.signup(
                username=form.username.data, 
                email=form.email.data, 
                password=form.password.data
            )
            db.session.commit()
            do_login(user)
            flash('Welcome ', user.username)
            return redirect(url_for('homepage'))

        except IntegrityError:
            db.session.rollback()
            flash("An unexpected error occurred. Please try again.", 'danger')
            return render_template('users/signup.html', form=form)

    return redirect(url_for('homepage'))


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

    flash('You have been logout.', 'primary')
    do_logout()
    return redirect(url_for('homepage'))


@app.route('/users/profile', methods=['GET', 'POST'])
@login_required
def profile():

    form = UserEditForm()

    if form.validate_on_submit():
        breakpoint()
        g.user.username = form.username.data
        g.user.email = form.email.data
        db.session.commit()
        flash("Account settings updated!", "success")
        return redirect(url_for('profile'))

    return render_template('users/edit.html', form=form)


@app.route('/favorites/<int:prop_id>/', methods=['POST'])
@login_required
def add_to_favorites(prop_id):
    try:
        prop = Property.query.get_or_404(prop_id)

        if prop in g.user.properties:
            g.user.properties.remove(prop)
            db.session.commit()
            return jsonify({"favorite": False, "message": "Property removed from favorites!"})
        else:
            g.user.properties.append(prop)
            db.session.commit()
            return jsonify({"favorite": True, "message": "Property added to favorites!"})
    except Exception as e:
        print("Error:", e)  # Prints the error to the console
        breakpoint()
        return jsonify({"success": False, "message": "An error occurred while adding to favorites"}), 500


@app.route('/users/favorite', methods=['GET'])
@login_required
def favorites_list():

    return render_template('/users/favorites.html', properties=g.user.properties)


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


@app.route('/api/property_detail/<int:prop_id>', methods=['GET'])
def get_prop_detail(prop_id):

    prop = Property.query.get_or_404(prop_id)    

    if prop.is_fetched:

        return render_template('/properties/detail.html', prop=prop)
    
    url = "https://zillow-com1.p.rapidapi.com/property"

    querystring = {"zpid":prop.zpid}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "zillow-com1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    prop.description = response.json().get("description")
    prop.monthly_hoa_fee = response.json().get("monthlyHoaFee")
    prop.annual_homeowners_insurance = response.json().get("annualHomeownersInsurance")
    prop.tax_annual_amount = response.json().get("taxAnnualAmount")
    prop.is_fetched = True

    db.session.commit()

    # return (response.json())

    return render_template('/properties/detail.html', prop=prop)


@app.route('/api/get-interest-rate')
def get_interest_rate():

    try:
        url = "https://zillow-com1.p.rapidapi.com/mortgageRates"

        querystring = {"program":"Fixed30Year","state":"US","refinance":"false","loanType":"Conventional","loanAmount":"Conforming","loanToValue":"Normal","creditScore":"Low","duration":"30"}

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": "zillow-com1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        last_item = response.json().get("rates")["Fixed30Year"]["samples"][-1]

        return jsonify(last_item["rate"])
    except Exception as e:
        return "error"