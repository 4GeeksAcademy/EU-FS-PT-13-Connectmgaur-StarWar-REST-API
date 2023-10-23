import os
from flask_admin import Admin
from models import db, User, Character, Planet, FavouriteCharacter, FavouritePlanet
from flask_admin.contrib.sqla import ModelView
from wtforms.utils import unset_value

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(FavouriteCharacterMV(FavouriteCharacter, db.session))
    admin.add_view(FavouritePlanetMV(FavouritePlanet, db.session))
    
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))

class FavouriteCharacterMV(ModelView):
    column_hide_backrefs = False
    column_list = ('id', 'user_id', 'username', 'character_id', 'name')

class FavouritePlanetMV(ModelView):
    column_hide_backrefs = False
    column_list = ('id', 'user_id', 'username', 'planet_id', 'name')



