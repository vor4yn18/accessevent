from datetime import datetime
 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
 
db = SQLAlchemy()
 
 
class User(db.Model):
    __tablename__ = "users"
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    is_deaf = db.Column(db.Boolean, nullable=False, default=False)
 
    events = db.relationship("Event", backref="organizer", lazy=True)
    registrations = db.relationship("Registration", backref="user", lazy=True)
 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
 
 
class Category(db.Model):
    __tablename__ = "categories"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
 
 
class Event(db.Model):
    __tablename__ = "events"
 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    is_inclusive = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(20), nullable=False, default="active")
    organizer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
 
    registrations = db.relationship(
        "Registration", backref="event", lazy=True,
        cascade="all, delete-orphan",
    )
 
 
class EventCategory(db.Model):
    __tablename__ = "event_categories"
 
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), primary_key=True)
 
 
class Registration(db.Model):
    __tablename__ = "registrations"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
 
    __table_args__ = (
        db.UniqueConstraint("user_id", "event_id", name="uq_reg_user_event"),
        db.CheckConstraint(
            "status IN ('pending', 'confirmed', 'cancelled')",
            name="ck_reg_status",
        ),
    )
 
 
class Notification(db.Model):
    __tablename__ = "notifications"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    type = db.Column(db.String(20), nullable=False, default="info")
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
 
    __table_args__ = (
        db.CheckConstraint(
            "type IN ('info', 'reminder', 'cancellation')",
            name="ck_notif_type",
        ),
    )
 
 
class Review(db.Model):
    __tablename__ = "reviews"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
 
    __table_args__ = (
        db.CheckConstraint("rating BETWEEN 1 AND 5", name="ck_rating"),
        db.UniqueConstraint("user_id", "event_id", name="uq_review_user_event"),
    )
 
 
class ChatMessage(db.Model):
    __tablename__ = "chat_messages"
 
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
