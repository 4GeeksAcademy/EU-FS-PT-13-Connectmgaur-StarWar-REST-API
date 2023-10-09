import unittest, os
from ..main import app
from ..models import db

TEST_DB = os.getcwd() + '/test.db'

class TestWrapper(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
    
    # executed prior to each test
    def setUp(self):
        # app = create_app()
        app.app_context().push()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)
 
        # executed after each test
    def tearDown(self):
        pass