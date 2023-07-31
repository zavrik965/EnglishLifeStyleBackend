from app.extensions import db
from dataclasses import dataclass

@dataclass
class Review(db.Model):
    id: int
    author: str
    content: str

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(150))
    content = db.Column(db.Text)

    def __repr__(self):
        return f'<Post "{self.author}">'
