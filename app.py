import os

from flask import Flask, render_template, redirect, url_for
from models import db, connect_db, User, Property, Favorites

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

connect_db(app)

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


@app.route('/signup')
def signup():

    return render_template('/users/signup.html')


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