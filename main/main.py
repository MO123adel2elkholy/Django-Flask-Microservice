import os
from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import IntegrityError
import requests
from producer import publish


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL', 'sqlite:///products.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='user_product_unique'),)


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())



@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    # USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://127.0.0.1:8000')
    try:
        resp = requests.get(f'http://127.0.0.1:8000/api/user', timeout=5)
        resp.raise_for_status()
        user_json = resp.json()
        print(user_json)

        productUser = ProductUser(user_id=user_json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
    except IntegrityError:
        db.session.rollback()
        abort(400, 'You already liked this product')
    except requests.RequestException:
        abort(502, 'User service unavailable')
    except Exception:
        db.session.rollback()
        abort(500)

    return jsonify({'message': 'success'})





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
