from . import db


class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    join_date = db.Column(db.String(100), unique=True)

    def __init__(self, name, join_date):
        self.name, self.join_date = name, join_date
