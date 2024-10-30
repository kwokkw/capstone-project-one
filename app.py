import os
from flask import Flask

app = Flask(__name__)

# Configuration settings

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'postgresql:///real-estate-dashboard')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def home():
    return "Welcome to the Real Estate Dashboard!"