from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password_hash = db.Column(db.String(300),nullable=False)
    address = db.Column(db.String(250),nullable=False)
    type = db.Column(db.String(10), nullable=False, default='normal') 
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)    
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'address': self.address,
            'type': self.type
        }