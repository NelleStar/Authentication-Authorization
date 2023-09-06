from app import app
from models import db, User, Feedback
from flask_bcrypt import Bcrypt

db.drop_all()
db.create_all()

bcrypt = Bcrypt()

u1 = User(username="userOne", 
          password=bcrypt.generate_password_hash("passOne").decode("utf-8"), email="one@email.com", 
          first_name="FirstOne", 
          last_name="LastOne" )
u2 = User(username="userTwo", 
          password=bcrypt.generate_password_hash("passTwo").decode("utf-8"), email="two@email.com", 
          first_name="FirstTwo", 
          last_name="LastTwo" )
u3 = User(username="userThree", 
          password=bcrypt.generate_password_hash("passThree").decode("utf-8"), email="three@email.com", 
          first_name="FirstThree", 
          last_name="LastThree" )

db.session.add_all([u1, u2, u3])
db.session.commit()


f1 = Feedback(title="Test 1",
              content="This is a test",
              username=u1)
f2 = Feedback(title="Test 2",
              content="Change the content",
              username=u1)
f3 = Feedback(title="Test 3",
              content="What great feedback",
              username=u2)
f4 = Feedback(title="Test 4",
              content="beep boop",
              username=u3)
f5 = Feedback(title="Test 5",
              content="Just filling up my table",
              username=u3)
f6 = Feedback(title="Test 6",
              content="I am nothing",
              username=u3)

db.session.add_all([f1, f2, f3, f4, f5, f6])
db.session.commit()