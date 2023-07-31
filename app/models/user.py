from app.extensions import db
from dataclasses import dataclass

@dataclass
class User(db.Model):
    id: int
    login: str
    password: str

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text)
    password = db.Column(db.Text)

    def __repr__(self):
        return f'<Post "{self.login}">'
