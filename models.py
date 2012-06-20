from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import MySQLdb

app = Flask(__name__)
db = SQLAlchemy(app)

class Coupon(db.Model):
    value = db.Column(db.String(80), primary_key=True)
    is_valid = db.Column(db.Boolean)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "<Coupon %r>" % self.value

