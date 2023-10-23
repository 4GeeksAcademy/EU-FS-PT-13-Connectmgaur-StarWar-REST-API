from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    planet = db.relationship("Planet", lazy='subquery', secondary="favourite_planets")
    character = db.relationship("Character", lazy='subquery', secondary="favourite_characters")

    def __repr__(self):
        return f"User(username={self.username}, id={self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Character(db.Model):
    __tablename__ = 'characters'
    # Reference: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
    id = db.Column(db.Integer, primary_key=True)
    external_uid = db.Column(db.String(120), nullable=True)
    name = db.Column(db.String(120), nullable=True)
    birth_year = db.Column(db.String(120), nullable=True)
    height = db.Column(db.Integer, nullable=True)

    user = db.relationship("User", lazy='subquery', secondary="favourite_characters")

    def __repr__(self):
        return f"Character(name={self.name}, id={self.id})"

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.external_uid,
            "name": self.name,
            "birth_year": self.birth_year,
            "height": self.height
        }
    
class FavouriteCharacter(db.Model):
    __tablename__ = 'favourite_characters'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    user = db.relationship(User, lazy='subquery', backref=db.backref("favourite_characters", cascade="all, delete-orphan"))
    character = db.relationship(Character, lazy='subquery', backref=db.backref("favourite_characters", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"FavouriteCharacter(user_id={self.user_id}, planet_id={self.character_id})"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,  
        }
    
    
class Planet(db.Model):
    __tablename__ = 'planets'
    # Reference: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
    id = db.Column(db.Integer, primary_key=True)
    external_uid = db.Column(db.String(120), nullable=True)
    name = db.Column(db.String(120), nullable=True)
    climate = db.Column(db.String(120), nullable=True)
    rotation_period = db.Column(db.String(120), nullable=True)
    orbital_period = db.Column(db.String(120), nullable=True)

    user = db.relationship("User", lazy='subquery', secondary="favourite_planets")

    def __repr__(self):
        return f"Planet(name={self.name}, id={self.id})"

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.external_uid,
            "name": self.name,
            "climate": self.climate,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period
        }
    
class FavouritePlanet(db.Model):
    __tablename__ = 'favourite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    user = db.relationship(User, lazy='subquery', backref=db.backref("favourite_planets", cascade="all, delete-orphan"))
    planet = db.relationship(Planet, lazy='subquery', backref=db.backref("favourite_planets", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"FavouritePlanet(user_id={self.user_id}, planet_id={self.planet_id})"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,  
        }
    
    