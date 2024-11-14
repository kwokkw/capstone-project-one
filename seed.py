from app import app, db
from models import User, Property, Favorites

with app.app_context():
    # Clear existing dta
    db.drop_all()
    db.create_all()

    # Create sample users
    user1 = User(username='johndoe', email='john@example.com', hashed_password='hashedpassword')
    user2 = User(username='janedoe', email='jane@example.com', hashed_password='hashedpassword')

    # Create sample properties
    property1 = Property(
            zpid="20477746",
            address="443 Euclid St, Santa Monica, CA 90402",
            price=4495000,
            bedrooms=4,
            bathrooms=2,
            living_area=1500,
        )
    property2 = Property(
            zpid="56877746",
            address="443 Example St,  Monica, HI 90402",
            price=600300,
            bedrooms=3,
            bathrooms=2,
            living_area=2500,
        )


    # Add data to the session
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(property1)
    db.session.add(property2)

    # Commit the session
    db.session.commit()

print("Database seeded!")
