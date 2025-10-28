from app import db

class UserDetails(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(20), nullable=False)

class FinDetails(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    amount=db.Column(db.Integer, nullable=False)
    type=db.Column(db.String(50), nullable=False, default='Expenditure')