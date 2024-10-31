import os

from flask import Flask
from models import db, connect_db, User, Property, Favorites

from dotenv import load_dotenv

load_dotenv()  # This will load your .env file variables

app = Flask(__name__)

# Configuration settings

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///real_estate_dashboard')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the Real Estate Dashboard!"