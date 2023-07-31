from app.extensions import db
from dataclasses import dataclass

@dataclass
class Video(db.Model):
    id: int
    url: str

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)

    def __repr__(self):
        return f'<Post "{self.url}">'
