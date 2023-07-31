from app.extensions import db
from dataclasses import dataclass

@dataclass
class TopSlider(db.Model):
    id: int
    image_url: str
    content: str

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.Text)
    content = db.Column(db.Text)

    def __repr__(self):
        return f'<Post "{self.content}">'
