from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    '''test user  models'''

    def setUp(self):
        """Clean up any existing pets."""

        User.query.delete()

        user = User(
            first_name="zoro", 
            last_name="enma",
            image_url="https://images.fineartamerica.com/images/artworkimages/mediumlarge/2/roronoa-zoro-darko-simple-art.jpg")

        db.session.add(user)
        db.session.commit()

        
        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:

            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('zoro',html)

    def test_show_user(self):
        with app.test_client() as client:

            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertIn('<h1>zoro enma</h1>', html)


class PostTestCase(TestCase):
    '''test post models'''

    def setUp(self):
        """Clean up any existing pets."""

        Post.query.delete()

        new_post = Post(
            title="legs", 
            content="need to run")

        db.session.add(new_post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def new_post(self):
        with app.test_client() as client:
            
            d = {"title":"legs2","content":"did it work"}
            resp = client.post('/users/{user.id}/posts/new', data = d, follow_redirects=True)


            self.assertIn('legs2', html)
    
class TagTestcase(TestCase):

    def setUp(self):
        """Clean up any existing pets."""

        Tag.query.delete()

        new_tag = Tag(
            name="runss")

        db.session.add(new_tag)
        db.session.commit()

        self.tag_id = tag.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def new_tag(self):
        with app.test_client() as client:
           
            d = {"name":"runssss"}
            resp = client.post('/tags', data = d, follow_redirects=True)


            self.assertEqual('runssss', html)





            