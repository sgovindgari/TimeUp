from google.appengine.ext import db

class User(db.Model):
    # this id is facebook id
    id = db.IntegerProperty(required = True)
    username = db.StringProperty(required = True)
    tasks = db.ListProperty(db.Key)

class Task(db.Model):
    description = db.StringProperty(required = True)  
    # unit is min
    duration = db.IntegerProperty(required = True)
    done = db.BooleanProperty(required=True)
    isPrivate = db.BooleanProperty(required=True)

    owner = db.ReferenceProperty(User)
    timestamp = db.DateTimeProperty(auto_now=True)
    
