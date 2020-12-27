from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    '''test user  models'''

    def setUp(self):
        """Clean up any existing pets."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_create(self):
        with app.test_client() as client:

            resp = client.get('/users/new', query_string={
            "first_name":"zoro", 
            "last_name":"enma",
            "image_url":"https://images.fineartamerica.com/images/artworkimages/mediumlarge/2/roronoa-zoro-darko-simple-art.jpg"})
        
            self.assertIn(b"zoro", resp.data)

# class PostTestCase(TestCase):
#     '''test post models'''

#     def setUp(self):
#         """Clean up any existing pets."""

#         Post.query.delete()

#     def tearDown(self):
#         """Clean up any fouled transaction."""

#         db.session.rollback()

#     def