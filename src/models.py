from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##################################################################################
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    gravity = db.Column(db.String(50))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.Integer)
#     fav_planet = Column(Integer, ForeignKey('fav_planets.id'))
#     fav_planet_relationship = relationship("Fav_planets", uselist=False)


    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    mass = db.Column(db.Integer)
    height = db.Column(db.Integer)
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    planet = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet_relationship = db.relationship(Planets)
   
#     fav_character = Column(Integer, ForeignKey('fav_characters.id'))
#     fav_character_relationship = relationship("Fav_Characters", uselist=False)


    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "planet": self.planet,
            
        }
    
############################ USERS ####################################################

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
############################## FAVS ####################################################

class Fav_Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet_relationship = db.relationship(Planets)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_relationship = db.relationship(User)

    def __repr__(self):
        return '<Fav_Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet,
            "user": self.user,
        }
    

class Fav_Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character_relationship = db.relationship(Characters)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_relationship = db.relationship(User)

    def __repr__(self):
        return '<Fav_Characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "character": self.character,
            "user": self.user,
        }
    
