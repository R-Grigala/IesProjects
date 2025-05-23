import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from src.models.base import BaseModel

# ONE - TO - ONE relationship
class User(db.Model, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(255), unique=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)

    last_sent_email = db.Column(db.DateTime(), default=datetime.now(), nullable=True)

    # One-to-Many relationship with Role
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', back_populates='users')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def check_permission(self, permission_name):
        if self.role:
            permission_attr = getattr(self.role, permission_name, None)
            return permission_attr is True
        return False

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"
    

class Role(db.Model, BaseModel):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    can_users = db.Column(db.Boolean, default=False)
    can_project = db.Column(db.Boolean, default=False)
    can_geophysic = db.Column(db.Boolean, default=False)
    can_geologic = db.Column(db.Boolean, default=False)
    can_hazard = db.Column(db.Boolean, default=False)
    can_geodetic = db.Column(db.Boolean, default=False)

    # One-to-Many relationship with User
    users = db.relationship('User', back_populates='role')

    def get_permissions(self):

        permissions = {
            
            "id": self.id,
            "name": self.name,
            "is_admin": self.is_admin,
            "can_users": self.can_users,
            "can_project": self.can_project,
            "can_geophysic": self.can_geophysic,
            "can_geologic": self.can_geologic,
            "can_hazard": self.can_hazard,
            "can_geodetic": self.can_geodetic
        }

        return permissions
    

    def __repr__(self):
        return f"{self.name}"