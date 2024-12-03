from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

#user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)  # Active/Inactive flag

    def __repr__(self):
        return f"<User {self.username}>"

    def activate(self):
        """Activate the user."""
        self.is_active = True

    def deactivate(self):
        """Deactivate the user."""
        self.is_active = False

# Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    book_type = db.Column(db.Integer, nullable=False)  # 1: 10 days, 2: 5 days, 3: 2 days
    available = db.Column(db.Boolean, default=True)

# Relationship to Borrow
    borrows = db.relationship('Borrow', back_populates='book', lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "book_type": self.book_type,
            "available": self.available,
        }

# Borrow (Loan) model
class Borrow(db.Model):
    __tablename__ = 'borrows'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrowed_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=False)

    # Relationships
    user = db.relationship('User', backref='borrows')
    book = db.relationship('Book', backref='borrows')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "borrowed_date": self.borrowed_date.strftime("%Y-%m-%d %H:%M:%S"),
            "return_date": self.return_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

# Helper function to calculate return date based on book type
def calculate_return_date(book_type):
    if book_type == 1:
        return datetime.utcnow() + timedelta(days=10)
    elif book_type == 2:
        return datetime.utcnow() + timedelta(days=5)
    elif book_type == 3:
        return datetime.utcnow() + timedelta(days=2)
    return datetime.utcnow()
