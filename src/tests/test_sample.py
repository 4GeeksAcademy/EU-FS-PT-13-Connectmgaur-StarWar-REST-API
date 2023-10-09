import os, unittest
from ..models import db, User
from .base import TestWrapper
 
class TestUser(TestWrapper):
 
    ###############
    #### tests ####
    ###############
 
    def test_get_all_users(self):
        user = User(email="bob@gmail.com", password="12341243", is_active=False)
        db.session.add(user)
        db.session.commit()

        response = self.app.get('/user', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['data']), 1)
