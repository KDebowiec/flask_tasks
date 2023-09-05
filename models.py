from __future__ import annotations
from . import db, ma
from flask_marshmallow import fields

class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    join_date = db.Column(db.String(100), unique=True)

    def __init__(self, name, join_date):
        self.name, self.join_date = name, join_date


class Notes(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), unique=True)

    def __init__(self, content):
        self.content = content

    def update(self, modified_note: Notes) -> None:
        self.content = modified_note.content


    @staticmethod
    def create_from_json(json_body: dict) -> Notes:
        return Notes(content=json_body['content'])


class NotesSchema(ma.Schema):
    _id = fields.fields.Integer()
    content = fields.fields.String()