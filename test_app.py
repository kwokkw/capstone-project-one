import os
from unittest import TestCase
from models import db, User, Property, Favorites
# from sqlalchemy.exc import InterfaceError
from dotenv import load_dotenv
from flask_wtf.csrf import generate_csrf
from flask import session
from forms import LoginForm, SignupForm


load_dotenv()

# Isolating the test database
os.environ['DATABASE_URL'] = os.environ.get('TEST_DATABASE_URL', 'postgresql:///real_estate_dashboard_test')

from app import app
with app.app_context():
    db.create_all()

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
# Prevent Flask-WTF from generating a csrf_token.
app.config['WTF_CSRF_ENABLED'] = False

# Access to different testing methods by inheriting from the base TestCase
class AppTestCase(TestCase):

    # Call before each test case
    def setUp(self):
        """ Create test client """

        # Delete all records in database
        with app.app_context():
            User.query.delete()
            Property.query.delete()
            Favorites.query.delete()

            # Seed the test database
            self.user = User.signup(username='testuser',email='test@test.com', password='password')
            self.property = Property(zpid="12345", address="123 Test St", price=500000, bedrooms=3, bathrooms=2)
            db.session.add_all([self.user, self.property])
            db.session.commit()

            self.client = app.test_client()


    def tearDown(self):
        """ Clean up databaes after each test """

        with app.app_context():
            db.session.rollback()


    def test_homepage(self):
        """Test the homepage renders correctly."""

        with self.client as c:

            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>What's Happening?</h1>", html)



    def test_signup(self):
        """Test user signup process."""

        with app.app_context():
            
            resp = self.client.post(
                "/signup",
                data={"username": "newuser", "email": "newuser@test.com", "password": "password"},
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Welcome", resp.data)
            self.assertEqual(User.query.filter_by(username="newuser").count(), 1)


    def test_login(self):
        """Test user login process."""

        with app.app_context():
            resp = self.client.post(
                "/login",
                data={"username": "testuser", "password": "password"},
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Hello, testuser!", resp.data)

