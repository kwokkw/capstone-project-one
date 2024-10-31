from app import db
from models import User, Property, Favorites

# Clear esisting dta
db.drop_all()
db.create_all()

# Create sample users
user1 = User(username='johndoe', email='john@example.com', hashed_password='hashedpassword')
user2 = User(username='janedoe', email='jane@example.com', hashed_password='hashedpassword')

# Create sample properties
property1 = Property(title='Luxury Apartment', description='A beautiful luxury apartment in the city center.', price=500000, location='New York', image_url='http://example.com/image1.jpg')
property2 = Property(title='Cozy Cottage', description='A cozy cottage in the countryside.', price=250000, location='Kentucky', image_url='http://example.com/image2.jpg')

# Add data to the session
db.session.add(user1)
db.session.add(user2)
db.session.add(property1)
db.session.add(property2)

# Commit the session
db.session.commit()

print("Database seeded!")
