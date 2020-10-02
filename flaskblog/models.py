from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db,login_manager
from flask_login import UserMixin
from flask import current_app



# flask_login extension expect your User model to have certain attributes and methods.its going to be expect
# four to be exact.
# 1. is_autheticated [will return true if they provided valid credentials]
# 2. is_active
# 3. is_anonymous
# 4. get_id [method]
# we can implement this but flask_login extension has a class called UserMixin its done for us to implement
# all the methods and attributes.

@login_manager.user_loader
def load_user(user_id):
    print("load_user : userid:",user_id)
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="profile.jpg")
    password = db.Column(db.String(30), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # here posts does not mean a column. its a relation between Post and User model.
    # backref help to get the posts for the specific user by calling author. example:
    # user.author where user is a instance of User model

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_code(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']
            print("verify_reset_code:", user_id)
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "<User {}>".format(self.id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "<Post {}>".format(self.id)
