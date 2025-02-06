from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager
from flask import url_for, current_app
from sqlalchemy import func
import os

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    video_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Like', backref='recipe', lazy='dynamic')

    def get_image_url(self):
        """Get the full URL for the recipe image"""
        if self.image_path:
            # Check if the image file exists
            image_file = os.path.join(current_app.root_path, 'static', self.image_path)
            if os.path.exists(image_file):
                return url_for('static', filename=self.image_path)
        return None  # Return None to use CSS default image

    def delete_image(self):
        """Delete the recipe's image file"""
        if self.image_path:
            try:
                image_file = os.path.join(current_app.root_path, 'static', self.image_path)
                if os.path.exists(image_file):
                    os.remove(image_file)
                    self.image_path = None
                    return True
            except Exception as e:
                current_app.logger.error(f"Error deleting image for recipe {self.id}: {e}")
        return False

    def to_dict(self):
        image_url = self.get_image_url()
        return {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,  # Keep as string for search
            'instructions': self.instructions.split('\n'),
            'image_path': image_url,
            'has_image': bool(image_url),  # Add flag for image existence
            'author': self.author.username,
            'likes_count': self.likes.count(),
            'created_at': self.created_at.isoformat(),
            'video_link': self.video_link,
            'source': 'user'
        }

    def __repr__(self):
        return f'<Recipe {self.title}>'
        
    def get_average_rating(self):
        """Calculate the average rating for the recipe"""
        result = db.session.query(func.avg(Comment.rating)).filter(Comment.recipe_id == self.id).scalar()
        return round(result, 1) if result else None

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))
    recipe = db.relationship('Recipe', backref=db.backref('comments', lazy='dynamic'))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe_comment'),
    )

    def __repr__(self):
        return f'<Comment {self.id}>'

    @staticmethod
    def validate_rating(rating):
        """Validate that the rating is between 1 and 10"""
        return isinstance(rating, int) and 1 <= rating <= 10

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe_like'),
    )

    def __repr__(self):
        return f'<Like {self.user_id} -> {self.recipe_id}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
