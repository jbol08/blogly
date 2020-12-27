"""Models for Blogly."""

"""Demo file showing off a model for SQLAlchemy."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://images.fineartamerica.com/images/artworkimages/mediumlarge/2/roronoa-zoro-darko-simple-art.jpg"
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """users, their names and image (if they upload one)."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                     nullable=False)
    last_name = db.Column(db.Text,
                     nullable=False)
    image_url = db.Column(db.Text,
                     nullable=False,
                     default=DEFAULT_IMAGE_URL)
    posts = db.relationship("Post",backref="user",cascade="all, delete-orphan")

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text)

    content = db.Column(db.Text,nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    @property
    def date(self):

        return self.created_at.strftime('%A %B %Y, %I:%M %p')
