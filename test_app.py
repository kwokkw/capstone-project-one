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
            Favorites.query.delete()
            User.query.delete()
            Property.query.delete()

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
            LoginForm.csrf_token = MockCsrfToken()
            SignupForm.csrf_token = MockCsrfToken()

            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)



    def test_signup(self):
        """Test user signup."""

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
        """Test user login."""

        with app.app_context():
            resp = self.client.post(
                "/login",
                data={"username": "testuser", "password": "password"},
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Hello, testuser!", resp.data)

            
    def test_logout(self):
        """Test user logout."""

        with app.app_context():
            self.user = User.query.filter_by(username="testuser").first()
            with self.client.session_transaction() as session:
                session["curr_user"] = self.user.id
            self.client.get("/")

            response = self.client.get("/logout", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(self.user.id, session)


    def test_add_to_favorites(self):
        """Test adding a property to favorites."""

        with app.app_context():
            self.user = User.query.filter_by(username="testuser").first()
            prop = Property(zpid="13579", address="246 Test ave", price=900000, bedrooms=3, bathrooms=1)
            db.session.add(prop)
            db.session.commit()
            
            with self.client.session_transaction() as session:
                session["curr_user"] = self.user.id
            response = self.client.post(f"/favorites/{prop.id}/", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Property added to favorites!", response.data)

            
    def test_search_address(self):
        """Test searching for an address."""
        
        response = self.client.get("/search_address?q=123")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"123 Test St", response.data)



class MockCsrfToken:
    def __call__(self, *args, **kwargs):
        return '<input type="hidden" name="csrf_token" value="dummy_csrf_token">'

    def __html__(self):
        return self()