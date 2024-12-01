# from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy.orm import validates
# from sqlalchemy_serializer import SerializerMixin
# from config import db, bcrypt

# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'

#     serialize_rules = ('-recipes.user', '-_password_hash',)

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     _password_hash = db.Column(db.String, nullable=False)
#     image_url = db.Column(db.String)
#     bio = db.Column(db.String)

#     recipes = db.relationship('Recipe', backref='user', lazy=True)

#     # Password hashing and validation
#     @hybrid_property
#     def password(self):
#         raise AttributeError('Password is not a readable attribute.')

#     @password.setter
#     def password(self, plaintext_password):
#         self._password_hash = bcrypt.generate_password_hash(
#             plaintext_password.encode('utf-8')
#         ).decode('utf-8')

#     def authenticate(self, plaintext_password):
#         return bcrypt.check_password_hash(
#             self._password_hash, plaintext_password.encode('utf-8')
#         )

#     # Validations
#     @validates('username')
#     def validate_username(self, key, username):
#         if not username:
#             raise ValueError("Username cannot be empty.")
#         return username

#     def __repr__(self):
#         return f"<User {self.username}>"


# class Recipe(db.Model, SerializerMixin):
#     __tablename__ = 'recipes'

#     __table_args__ = (
#         db.CheckConstraint('length(instructions) >= 50', name='check_instructions_length'),
#     )

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     instructions = db.Column(db.String, nullable=False)
#     minutes_to_complete = db.Column(db.Integer, nullable=False)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
#     # Validations
    
    
#     @validates('title')
#     def validate_title(self, key, title):
#         if not title:
#             raise ValueError("Title cannot be empty.")
#         return title

#     @validates('instructions')
#     def validate_instructions(self, key, instructions):
#         if not instructions:
#             raise ValueError("Instructions cannot be empty.")
#         if len(instructions) < 50:
#             raise ValueError("Instructions must be at least 50 characters long.")
#         return instructions

#     def __repr__(self):
#         return f"<Recipe {self.id}: {self.title}>"




from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    
    serialize_rules = ('-recipes.user', '-_password_hash',)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)
    
    
    recipes = db.relationship('Recipe', backref='user')
    
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    def __repr__(self):
        return f'<User {self.username}>'

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    
    __table_args__ = (
        db.CheckConstraint('length(instructions) >= 50'),
    )
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    @validates('instructions')
    def validate_instructions(self, key, value):
        if len(value) < 50:
            raise ValueError("Instructions must be at least 50 characters long.")
        return value
    
    
    
    def __repr__(self):
        return f'<Recipe {self.id}: {self.title}>'