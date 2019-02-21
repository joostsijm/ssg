
"""
All models for module
"""

from urllib.parse import quote
from datetime import datetime
# from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
import markdown
from flask import Markup
from flask_login import UserMixin
from app import db, argon2, login_manager


class User(db.Model, UserMixin):
    """Model for User"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    _password = db.Column("password", db.String(255))
    registration_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, id=None):
        self.id = id

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @property
    def password(self):
        """Return the password"""
        return self._password

    @password.setter
    def password(self, password):
        """Hash password"""
        self._password = argon2.generate_password_hash(password)

    def check_password(self, password):
        """Check if password is correct"""
        return argon2.check_password_hash(self.password, password)


class Page(db.Model):
    """Model for Page"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    source = db.Column(db.String)


    def content(self):
        """Render page source"""
        return Markup(markdown.markdown(self.source))


    def url(self):
        """Generate URL for page"""
        return quote(self.title.strip().lower().replace(" ", "_"))


    def path(self):
        """Generate path with parents"""
        if self.parent_id:
            return '%s/%s' % (self.parent.path(), self.url())
        return self.url()

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )
    user = db.relationship(
        "User",
        backref=db.backref("Pages", lazy="dynamic")
    )

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("page.id")
    )
    parent = db.relationship(
        "Page",
        backref=db.backref("children", lazy="dynamic"),
        uselist=False,
        remote_side=id
    )
