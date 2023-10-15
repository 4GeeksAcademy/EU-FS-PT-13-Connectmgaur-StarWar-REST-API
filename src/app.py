"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People
import requests 
import json
#from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/planet')
def import_planet():
    # Reference: https://stackoverflow.com/questions/61977076/how-to-fetch-data-from-api-using-python
    # Reference: https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html
    res = requests.get('https://www.swapi.tech/api/planets/')
    response = json.loads(res.text)

    data = response["results"]
    for planet_data in data:
        planet_res = requests.get(planet_data["url"])
        planet_json = json.loads(planet_res.text)
        result = planet_json['result']
        properties = result['properties']
        p = Planet(external_uid = result['uid'], name = properties['name'], url= properties['url'])
        db.session.add(p)

    db.session.commit()

    return jsonify({"msg": "All the people was added"}), 200


@app.route('/people')
def import_people():
    # Reference: https://stackoverflow.com/questions/61977076/how-to-fetch-data-from-api-using-python
    # Reference: https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html
    res = requests.get('https://www.swapi.tech/api/people/')
    response = json.loads(res.text)

    data = response["results"]
    for people_data in data:
        people_res = requests.get(people_data["url"])
        people_json = json.loads(people_res.text)
        result = people_json['result']
        properties = result['properties']
        p = People(uid = result['uid'], name = properties['name'], birth_year= properties['birth_year'])
        db.session.add(p)

    db.session.commit()

    return jsonify({"msg": "All the people was added"}), 200


@app.route('/people/<int:people_id>', methods=['PUT', 'GET'])
def get_single_person(people_id):
    """
    Single person
    """
    body = request.get_json() #{ 'username': 'new_username'}
    if request.method == 'PUT':
        user1 = People.query.get(people_id)
        user1.username = body.username
        db.session.commit()
        return jsonify(user1.serialize()), 200
    if request.method == 'GET':
        user1 = People.query.get(people_id)
        return jsonify(user1.serialize()), 200

    return "Invalid Method", 404
    

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
