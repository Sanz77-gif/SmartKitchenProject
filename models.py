from database import db
from datetime import datetime

class Favorite(db.Model):
    __tablename__ = 'favorites'

    meal_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)