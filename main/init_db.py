from main import app, db, Product

with app.app_context():
    db.create_all()
    if not Product.query.first():
        sample = [
            Product(id=1, title="Sample Product 1", image="https://via.placeholder.com/150"),
            Product(id=2, title="Sample Product 2", image="https://via.placeholder.com/150"),
        ]
        db.session.add_all(sample)
        db.session.commit()
    print("Database initialized")