from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to the database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """user instance"""

    __tablename__= 'users'

    username = db.Column(db.String,
                   primary_key=True,
                   unique=True)
    password = db.Column(db.String, 
                         nullable=False)
    email = db.Column(db.String, 
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String,
                           nullable=False)
    last_name = db.Column(db.String,
                           nullable=False)
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """register user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return unstance of user with username and hashed password
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """validate that user exists and password is correct
        
        return user if valid, else return false.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else: 
            return False
    

class Feedback(db.Model):
    """feedback instance"""

    __tablename__= 'feedbacks'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.String,
                         db.ForeignKey('users.username'),
                         nullable=False)
    
    # define the relationship between the tables
    user = db.relationship('User', backref='feedbacks')