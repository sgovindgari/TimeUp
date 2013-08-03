from google.appengine.ext import db

class User(db.Model):
    # this id is facebook id
    id = db.IntegerProperty(required = True)
    username = db.StringProperty(required = True)
    email = db.EmailProperty()
    passwd = db.StringProperty()
    tasks = db.ListProperty(db.Key)
    friends = db.ListProperty(db.IntegerProperty)

class Task(db.Model):
    description = db.StringProperty(required = True)  
    # unit is min
    duration = db.IntegerProperty(required = True)
