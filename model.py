import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    lists = db.relationship("List", backref = "user", lazy = True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self,password):
        if self.password == password:
            return True
        else:
            return False


class List(db.Model):
    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ordered_list = db.Column(db.String(255), nullable = False)
    visited = db.Column(db.Boolean, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)


class Saltlakepark(db.Model):
    __tablename__ = "saltlakeparks"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    saltlakepark_name = db.Column(db.String(255), nullable = False)
    saltlakepark_description = db.Column(db.String(500), nullable = False)
    # dogparks = db.relationship("dogparks", backref = "saltlakeparks", lazy = True)
    # Visiteds = db.relationship("Visited", backref = "saltlakeparks", lazy = True)


class Dogpark(db.Model):
    __tablename__ = "dogparks"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    dogpark_name = db.Column(db.String(255), nullable = False)
    # Saltlakeparks_id = db.Column(db.Integer, db.ForeignKey("saltlakeparks.id"), nullable = False)


class Visited(db.Model):
    __tablename__ = "visiteds"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Visited_name = db.Column(db.String(255), nullable = False)
    Saltlakeparks_id = db.Column(db.Integer, db.ForeignKey("saltlakeparks.id"), nullable = False)
    checkable  = db.Column(db.Boolean, nullable = False)



def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Dog park db...")