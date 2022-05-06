from database import db
import datetime

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column("userID", db.Integer)
    darkModeToggle = db.Column("darkModeToggle", db.Integer)

    def __init__(self, userID, darkModeToggle):
        self.userID = userID
        self.darkModeToggle = darkModeToggle