from application import app
from flask import render_template, request, flash, redirect, url_for, session , jsonify
from google.appengine.ext import db
from google.appengine.api import urlfetch
from models import *
from forms import *
import geopy, geopy.distance
import time, random, urllib, hashlib, json
import facebook

from functools import wraps
from flask import request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "user" in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# if 'username' in session:
#             return 'Logged in as %s' % escape(session['username'])
#             return 'You are not logged in'

uid = ""

@app.route('/loggedin')
@login_required
def index():
    if 'user' in session:
        app.logger.debug(session['user'])
    return render_template('index.html')

    # Return the html for login
@app.route('/')
def login():
    return render_template('login.html')
    
    # Handle the actual Login Post request
@app.route('/login', methods=["POST"])
def loginPost():
    uid = request.form['uid']
    token = request.form['token']
    if uid and token:
        try:
            graph = facebook.GraphAPI(token)
            profile = graph.get_object("me")

            # check if this user exists in datastore
            q = User.all().filter('id =', uid)
            user_count = q.count()
            if user_count == 1:
                session['user'] = q.get()
            else:
                name = profile["name"]
                newUser = User(id = int(uid), username = name)
                newUser.save()
                session['user'] = newUser
        except facebook.GraphAPIError:
            name = "token Error"
    else:
        name = "argument Error"

    if  name == "token Error" or name == "argument Error":
        data = name
    else:
        data = "success"
    return data

@login_required
@app.route('/tasks/new', methods=["POST"])
@login_required
def newTask():
    desc = request.form['description']
    duration = int(request.form['duration'])
    isPrivate = bool(request.form['isPrivate'])

    newTask = Task(description = desc, duration = duration, done=False, isPrivate = isPrivate)
    key = newTask.save()

    app.logger.debug("added %s   %s  %s" % (key, desc, type(key)))
    if key and 'user' in session:
        user = session['user'] 
        user.tasks.insert(0, key)
        user.save()
        session['user'] = user

    data = {"status": "ok"}
    return jsonify(data)

@login_required

# give me a task
@app.route('/gettasks', methods=["GET"])
@login_required
def giveMeTask():
    if 'user' in session:
        app.logger.debug(session['user'].tasks)

    keys = session['user'].tasks[:15]
    tasks = db.get(keys)

    task_list = []
    for key in keys:
        task = db.get(key)
        if task:
            task_list.append({"description": task.description, "duration": task.duration, "done": task.done, "isPrivate": task.isPrivate, "key": str(key), "timestamp": str(task.timestamp)})

    return jsonify({"task_list": task_list})

@app.route('/tasks', methods=["GET"])
@login_required
def allTask():
    if 'user' in session:
        app.logger.debug(session['user'].tasks)
    keys = session['user'].tasks[:15]
    tasks = db.get(keys)

    task_list = []
    for key in keys:
        task = db.get(key)
        if task:
            task_list.append({"description": task.description, "duration": task.duration, "done": task.done, "isPrivate": task.isPrivate, "key": str(key), "timestamp": str(task.timestamp)})

    return jsonify({"task_list": task_list})

@app.route('/tasks', methods=["PUT"])
@login_required
def finishTask():
   task = db.get(request.args.get('id'))
   task.done = true;

@app.route('/gettask')
@login_required
def gettask():
    return render_template('gettask.html')
