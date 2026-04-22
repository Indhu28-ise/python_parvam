# seed_db.py
from app import app, db
from models import Product

with app.app_context():
    db.create_all()
    # Remove existing products (optional)
    Product.query.delete()
    db.session.commit()

    products = [
        Product(name="Wireless Headphones", price=1999.00, description="Bluetooth, noise-cancelling"),
        Product(name="USB-C Charger", price=799.00, description="65W fast charger"),
        Product(name="Smart Watch", price=4999.00, description="Heart rate, GPS"),
    ]
    db.session.bulk_save_objects(products)
    db.session.commit()
    print("Seeded products:", Product.query.count())
