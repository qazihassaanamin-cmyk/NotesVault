from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Junction Table for User Purchased Notes (Many-to-Many)
purchases = db.Table('purchases',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    resources = db.relationship('Resource', backref='author', lazy=True)
    unlocked_resources = db.relationship('Resource', secondary=purchases, backref=db.backref('buyers', lazy=True))

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(50), nullable=False) # e.g., Calculus, Physics, Python
    description = db.Column(db.Text, nullable=False)
    resource_link = db.Column(db.String(500), nullable=False)
    
    # New Access & Business Control Fields
    is_private = db.Column(db.Boolean, default=False)  # Private to owner vs. Public
    is_paid = db.Column(db.Boolean, default=False)     # Free vs. Paid
    price = db.Column(db.Float, default=0.0)           # Price in PKR/USD
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)