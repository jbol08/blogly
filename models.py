"""Models for Blogly."""

"""Demo file showing off a model for SQLAlchemy."""

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
    

    