from app.extensions import db
from dataclasses import dataclass

@dataclass
class Price(db.Model):
    id: int
    points: str
    value: str
    old_value: str
    price_type: int

    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Text)
    value = db.Column(db.Text)
    old_value = db.Column(db.Text)
    price_type = db.Column(db.Integer)

    def __repr__(self):
        return f'<Post "{self.title}">'
