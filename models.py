# #models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'user'
     
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    password = db.Column(db.String(60), nullable=False)
    events = relationship('Event', backref='organizer', lazy=True)
    tickets = relationship('Ticket', backref='user', lazy=True)

class Event(db.Model, SerializerMixin):
    _tablename_ = 'event'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(255))
    tickets = relationship('Ticket', backref='event', lazy=True)

class Ticket(db.Model, SerializerMixin):
    _tablename_ = 'ticket'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    tickets_available = db.Column(db.Integer, nullable=False)
    tickets_purchased = db.Column(db.Integer, nullable=False)
    

    
class Review(db.Model, SerializerMixin):
    _tablename_ = 'review'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)