from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    url = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }

class People(db.Model):
    # Reference: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
    id = db.Column(db.Integer, primary_key=True)
    external_uid = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    birth_year = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<People %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.external_uid,
            # do not serialize the password, its a security breach
        }
class Favorites(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(120), nullable=False)
    fave_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "fave_id": self.fave_id,
            "name": self.name,
            "url": self.url,
        }