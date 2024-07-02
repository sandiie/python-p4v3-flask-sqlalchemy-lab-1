#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Earthquake
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)
@app.route('/earthquakes/<int:earthquake_id>', methods=['GET'])
def get_earthquake(earthquake_id):
    earthquake = Earthquake.query.get(earthquake_id)
    if earthquake:
        return jsonify(earthquake.to_dict())
    else:
        return jsonify({'message': f'Earthquake {earthquake_id} not found.'}), 404

@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    earthquakes = Earthquake.query.all()
    return jsonify([earthquake.to_dict() for earthquake in earthquakes])

@app.route('/earthquakes', methods=['POST'])
def create_earthquake():
    data = request.get_json()
    earthquake = Earthquake(
        magnitude=data['magnitude'],
        depth=data['depth'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        location=data['location'],
        time=datetime.fromisoformat(data['time'])
    )
    db.session.add(earthquake)
    db.session.commit()
    return jsonify(earthquake.to_dict()), 201

if __name__ == 'main':
    app.run(port=5555, debug=True)