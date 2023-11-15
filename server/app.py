#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    # response = make_response(all_bakeries, 200,
    #     {'Content-Type': 'application/json'})
    response = all_bakeries, 200
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    bakery_dict = bakery.to_dict()
    response = bakery_dict, 200
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = [good.to_dict() for good in BakedGood.query.order_by(desc('price')).all() ]
    # baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    # baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    response = goods, 200
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    treat = BakedGood.query.order_by(desc('price')).limit(1).first()
    response = treat.to_dict(), 200
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
