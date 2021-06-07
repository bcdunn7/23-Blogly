"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connects to db."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String(128),
                    nullable=False)

    last_name = db.Column(db.String(128),
                    nullable=False)

    image_url = db.Column(db.String,
                    default="https://i.pinimg.com/originals/0c/3b/3a/0c3b3adb1a7530892e55ef36d3be6cb8.png")
                        #default user image
    
class Post(db.Model):
    """Post model."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    title = db.Column(db.String(128),
                    nullable=False)

    content = db.Column(db.String,
                    nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id'))

    user = db.relationship('User', backref='post')