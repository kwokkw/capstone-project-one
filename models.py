# SQLAlchemy for ORM (Object Relational Mapping) with Flask 
# for handling database interaction 
from flask_sqlalchemy import SQLAlchemy

# Import Bcrypt for password hashing.
from flask_bcrypt import Bcrypt

# Create an instance of Bcrypt for pw hashing.
bcrypt = Bcrypt()

# Create an instance of SQLAlchemy to interact with database.
db = SQLAlchemy()

class User(db.Model):
    """ User in the system. """

    # Specifies the database table name
    __tablename__ = 'users'

    # Define a primary key column
    id = db.Column(db.Integer, primary_key=True)

    # Define an unique, non-nullable Email column
    email = db.Column(db.String(120), nullable=False, unique=True)

    # Define an unique, non-nullable username column
    username = db.Column(db.String(100), nullable=False, unique=True)

    # Define a non-nullable password column
    hashed_password = db.Column(db.Text, nullable=False)

    # Define a many-to-many relationship
    # Delete the favorites record when it's no longer associated with user
    properties = db.relationship('Property', secondary='favorites', backref='users')

    # Dunder methods (double underscores) returns a string representation used for debugging
    def __repr__(self):
        return f'<User #{self.id}: {self.username}>'
    

    def change_password(self, current_password, new_password):
        """ Handle the password change """

        # Check if the provided current password matches stored hash password
        if not bcrypt.check_password_hash(self.hashed_password, current_password):

            # Current password provided does not match the one in database
            # Password change failed
            return False
        
        # Hashes the new password using Bcrypt and update user password
        self.password = bcrypt.generate_password_hash(new_password).decode('UTF-8')

        # Save the user with the new password
        db.session.commit()

        # Password change successful
        return True

    @classmethod
    def signup(cls, username, email, password):
        """ Sign up user, hashes password, adds user to system """

        # Hashed the password using Bcrypt
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        # Create a new User instance with the hashed password
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_pwd
        )

        # Adds the new user to database session
        db.session.add(user)

        # Returns the new user instance
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.hashed_password, password)
            if is_auth:
                return user

        else:
            return False


class Property(db.Model):
    """ Properties in the database. """

    # Specifies the database table name
    __tablename__ = 'properties'

    # Define a primary key column
    id = db.Column(db.Integer, primary_key=True)

    # Define a non-nullable, unique zpid column
    zpid = db.Column(db.String, unique=True, nullable=False)
    
    # Define a non-nullable address column
    address = db.Column(db.String(200), nullable=False)

    # Define a non-nullable price column
    price = db.Column(db.Integer, nullable=False)

    # Defin a bedrooms column
    bedrooms = db.Column(db.Integer)

    # Defin a bathrooms column
    bathrooms = db.Column(db.Integer)

    # Defin a living area column
    living_area = db.Column(db.Integer)

    # TODO: Provide a default image url
    # Define a non-nullable image_url column
    image_src = db.Column(db.String(200), default=('/static/images/single-family-home.jpg'))

    description = db.Column(db.Text)
    monthly_hoa_fee = db.Column(db.Integer)
    annual_homeowners_insurance = db.Column(db.Integer)
    tax_annual_amount = db.Column(db.Integer)
    is_fetched = db.Column(db.Boolean)

    # Dunder methods (double underscores) returns a string representation used for debugging
    def __repr__(self):
        return f'<Property #{self.id}: {self.address} - {self.description}>'


class Favorites(db.Model):
    """ Favorites connect users to their favorite properties. """

    # Specifies the database table name
    __tablename__ = 'favorites'

    # TODO: If user (or property) is deleted, the record associated will be deleted too.
    # Define relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), primary_key=True, nullable=False)


# Establishes a connection between a FLASK APPLICATION and a SQLAlchemy DATABASE
def connect_db(app):
    """ 
        Connect this database to provided Flask app.
        Call this in Flask app.
    """

    # Assign the Flask app instance to the `app` property of the `db` object (an instance of `SQLAlchemy()`).
    # Tell SQLAlchemy which Flask app it should work with.
    db.app = app

    # A helper method that initializes the Flask app with SQLAlchemy.
    # It configures the app so that the database can be accessed within the app's context.
    # This ensures that the Flask app is fully integrated with SQLAlchemy and is ready to handle database queries or operations.
    db.init_app(app)

