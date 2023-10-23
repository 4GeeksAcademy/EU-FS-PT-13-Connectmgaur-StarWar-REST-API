"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, session
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavouritePlanet, FavouriteCharacter

import json

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


# Endpoint - 'GET' Users.
@app.route('/users', methods=['GET'])
def get_user():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


# Endpoint - 'GET' ALL Characters.
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    return jsonify([char.serialize() for char in characters]), 200


# Endpoint - 'GET' Single Character.
@app.route('/characters/<string:character_id>', methods=['GET'])
def get_character(character_id):
    char = Character.query.filter_by(external_uid=character_id).first_or_404()
    return jsonify(char.serialize()), 200


# Endpoint - 'GET' ALL Planets.
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


# Endpoint - 'GET' Single Planet.
@app.route('/planets/<string:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.filter_by(external_uid=planet_id).first_or_404()
    return jsonify(planet.serialize()), 200


# Endpoint - 'GET' User Favourites.
@app.route('/users/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):
    current_user = User.query.get(user_id)

    favourite_planets = current_user.planet
    favourite_planets = [fav_planet.serialize()
                         for fav_planet in favourite_planets]

    favourite_characters = current_user.character
    favourite_characters = [fav_char.serialize()
                            for fav_char in favourite_characters]

    user_favourites = favourite_characters + favourite_planets

    return jsonify({f"Current User '{current_user.username}' (id={current_user.id}) Favourites": user_favourites}), 200


# Endpoint - 'POST' Planet to Favourites.
@app.route('/user/<int:user_id>/favourite/planet/<string:planet_id>', methods=['POST'])
def add_favourite_planet(user_id, planet_id):

    char_exists = FavouritePlanet.query.filter_by(
        planet_id=planet_id).filter_by(user_id=user_id).first()

    if not char_exists:
        favourite = FavouritePlanet(user_id=user_id, planet_id=planet_id)
        db.session.add(favourite)
        db.session.commit()
        return jsonify({"status": f"Planet '{favourite.planet.name}' added to user '{favourite.user.username}' favourites."}), 200

    return jsonify({"status": f"Planet '{Planet.query.filter_by(id=planet_id).first().name}' already in user '{User.query.filter_by(id=user_id).first().username}' favourites."}), 200

# Endpoint - 'DELETE' Planet from Favourites.


@app.route('/user/<int:user_id>/favourite/planet/<string:planet_id>', methods=['DELETE'])
def delete_favourite_planet(user_id, planet_id):

    favourite = FavouritePlanet.query.filter_by(
        planet_id=planet_id).filter_by(user_id=user_id).first()
    if favourite:
        db.session.delete(favourite)
        db.session.commit()
        return jsonify({"status": f"Planet '{favourite.planet.name}' deleted from user '{favourite.user.username}' favourites."}), 200

    return jsonify({"status": f"Nothing to delete: Planet '{Planet.query.filter_by(id=planet_id).first().name}' is not in user '{User.query.filter_by(id=user_id).first().username}' favourites."}), 200


# Endpoint - 'POST' Character to Favourites.
@app.route('/user/<int:user_id>/favourite/character/<string:character_id>', methods=['POST'])
def add_favourite_character(user_id, character_id):

    char_exists = FavouriteCharacter.query.filter_by(
        character_id=character_id).filter_by(user_id=user_id).first()

    if not char_exists:
        favourite = FavouriteCharacter(
            user_id=user_id, character_id=character_id)
        db.session.add(favourite)
        db.session.commit()
        return jsonify({"status": f"Character '{favourite.character.name}' added to user '{favourite.user.username}' favourites."}), 200

    return jsonify({"status": f"Character '{Character.query.filter_by(id=character_id).first().name}' already in user '{User.query.filter_by(id=user_id).first().username}' favourites."}), 200

# Endpoint - 'DELETE' Character from Favourites.


@app.route('/user/<int:user_id>/favourite/character/<string:character_id>', methods=['DELETE'])
def delete_favourite_character(user_id, character_id):

    favourite = FavouriteCharacter.query.filter_by(
        character_id=character_id).filter_by(user_id=user_id).first()
    if favourite:
        db.session.delete(favourite)
        db.session.commit()
        return jsonify({"status": f"Character '{favourite.character.name}' deleted from user '{favourite.user.username}' favourites."}), 200

    return jsonify({"status": f"Nothing to delete: Character '{Character.query.filter_by(id=character_id).first().name}' is not in user '{User.query.filter_by(id=user_id).first().username}' favourites."}), 200
