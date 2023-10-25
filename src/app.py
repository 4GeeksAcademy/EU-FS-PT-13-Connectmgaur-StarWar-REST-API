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
from models import db, User, Characters, Planets, Fav_Characters, Fav_Planets
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

############################## USERS #################################################

# GET ALL USERS:

@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()

    if not users:
        return jsonify(message="No users found"), 404

    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(message="Users", users=all_users), 200

# GET ONE USER:

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    serialized_user = user.serialize()
    return jsonify({'user': serialized_user}), 200

# ADD USERS:

@app.route('/user', methods=['POST'])
def add_new_user():
    request_body_user = request.get_json()

    new_user = User(email=request_body_user["email"], password=request_body_user["password"], is_active=request_body_user["is_active"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(request_body_user), 200

# DELETE ONE USER:

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User with ID {user_id} deleted successfully'}), 200

############################## CHARACTERS #################################################

# GET ALL CHARACTERS:

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()

    if not characters:
        return jsonify({'message': 'Characters not found'}), 404
    
    all_characters = list(map(lambda x: x.serialize(), characters))
    return jsonify(message="Characters", characters=all_characters), 200

# ADD A CHARACTER

@app.route('/characters', methods=['POST'])
def add_new_character():
    request_body_character = request.get_json()

    new_character = Characters(name=request_body_character["name"])
    db.session.add(new_character)
    db.session.commit()

    return jsonify(request_body_character), 200

# DELETE A CHARACTER

@app.route('/characters/<int:characters_id>', methods=['DELETE'])
def delete_character(characters_id):
    character = Characters.query.get(characters_id)

    if not character:
        return jsonify({'message': 'Character not found'}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({'message': f'Character with ID {characters_id} deleted successfully'}), 200

############################## PLANETS #################################################

# GET ALL PLANETS:

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()

    if not planets:
        return jsonify({'message': 'Planets not found'}), 404

    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(message="Planets", planets=all_planets), 200

# ADD A PLANET:

@app.route('/planets', methods=['POST'])
def add_new_planet():
    request_body_planet = request.get_json()

    new_planet = Planets(name=request_body_planet["name"], diameter=request_body_planet["diameter"], rotation_period=request_body_planet["rotation_period"], gravity=request_body_planet["gravity"], population=request_body_planet["population"], climate=request_body_planet["climate"], terrain=request_body_planet["terrain"], surface_water=request_body_planet["surface_water"])
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(request_body_planet), 200

# DELETE A PLANET

@app.route('/planets/<int:planets_id>', methods=['DELETE'])
def delete_planet(planets_id):
    planet = Planets.query.get(planets_id)

    if not planet:
        return jsonify({'message': 'Planet not found'}), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify({'message': f'Planet with ID {planets_id} deleted successfully'}), 200


############################## FAV CHARACTERS ###########################################

# GET ALL FAV_CHARACTERS:

@app.route('/fav_characters', methods=['GET'])
def get_fav_characters():
    fav_characters = Fav_Characters.query.all()
    fav_all_characters = list(map(lambda x: x.serialize(), fav_characters))
    return jsonify(message="Fav_characters", fav_characters=fav_all_characters), 200

# GET ALL FAV_CHARACTERS OF A USER:

@app.route('/fav_characters/<int:user>', methods=['GET'])
def get_fav_characters_of_user(user):
    fav_characters = Fav_Characters.query.filter_by(user=user).all()
    fav_all_characters = list(map(lambda x: x.serialize(), fav_characters))
    return jsonify(message="Fav_characters", fav_characters=fav_all_characters), 200

# POST A FAV CHARACTER: 

@app.route('/fav_characters', methods=['POST'])
def add_new_fav_character():
    request_body_fav_character = request.get_json()

    new_fav_character = Fav_Characters(character=request_body_fav_character["character"], user=request_body_fav_character["user"])
    db.session.add(new_fav_character)
    db.session.commit()

    return jsonify(request_body_fav_character), 200

# DELETE A FAV CHARACTER

@app.route('/fav_characters/<int:fav_characters_id>', methods=['DELETE'])
def delete_fav_character(fav_characters_id):
    fav_character = Fav_Characters.query.get(fav_characters_id)

    if not fav_character:
        return jsonify({'message': 'Fav Character not found'}), 404

    db.session.delete(fav_character)
    db.session.commit()

    return jsonify({'message': f'Fav character with ID {fav_characters_id} deleted successfully'}), 200


############################## FAV PLANETS ###########################################

# GET ALL FAV_PLANETS:

@app.route('/fav_planets', methods=['GET'])
def get_fav_planets():
    fav_planets = Fav_Planets.query.all()
    fav_all_planets = list(map(lambda x: x.serialize(), fav_planets))
    return jsonify(message="Fav_planets", fav_planets=fav_all_planets), 200

# GET ALL FAV_PLANETS OF A USER:

@app.route('/fav_planets/<int:user>', methods=['GET'])
def get_fav_planets_of_user(user):
    fav_planets = Fav_Planets.query.filter_by(user=user).all()
    fav_all_planets = list(map(lambda x: x.serialize(), fav_planets))
    #or:  fav_all_planets = [planet.serialize() for planet in fav_planets]
    return jsonify(message={'message': f'Fav planets of user {user}'}, fav_planets=fav_all_planets), 200

# POST A FAV_PLANET: 

@app.route('/fav_planets', methods=['POST'])
def add_new_fav_planet():
    request_body_fav_planet = request.get_json()

    new_fav_planet = Fav_Planets(planet=request_body_fav_planet["planet"], user=request_body_fav_planet["user"])
    db.session.add(new_fav_planet)
    db.session.commit()

    return jsonify(request_body_fav_planet), 200

# DELETE A FAV PLANET

@app.route('/fav_planets/<int:fav_planets_id>', methods=['DELETE'])
def delete_fav_planet(fav_planets_id):
    fav_planet = Fav_Planets.query.get(fav_planets_id)

    if not fav_planet:
        return jsonify({'message': 'Fav planet not found'}), 404

    db.session.delete(fav_planet)
    db.session.commit()

    return jsonify({'message': f'Fav planet with ID {fav_planets_id} deleted successfully'}), 200


###########################################################################################

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


# pipenv run python src/app.py