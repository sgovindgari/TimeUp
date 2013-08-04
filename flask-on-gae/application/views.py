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
            q = User.all().filter("uid =", uid)
            user_count = q.count()
            app.logger.debug(user_count)
            session['token'] = token 
            if user_count == 1:
                session['user'] = q.get()
                app.logger.debug("fetched user")
                name = session['user'].username
            else:
                app.logger.debug("create new user")
                name = profile["name"]
                newUser = User(uid = uid, username = name)
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

@app.route('/logout', methods=["GET"])
@login_required
def logout():
    session.pop("user", None)
    session.pop("token", None)
    return "ok"

@app.route('/tasks/new', methods=["POST"])
@login_required
def newTask():
    desc = request.form['description']
    duration = int(request.form['duration'])
    isPrivate = bool(request.form['isPrivate'])

    newTask = Task(description = desc, duration = duration, done=False, isPrivate = isPrivate, ownername=session.get("user").username)

    if 'user' in session:
        user = session['user'] 
        #user.tasks.insert(0, key)
        #user.save()
        session['user'] = user
    
    newTask.owner = session['user'].key()
    key = newTask.save()
    app.logger.debug("added %s   %s  %s" % (key, desc, type(key)))
    time.sleep(0.5)

    data = {"status": "ok"}
    return jsonify(data)

# give me a task
@app.route('/givetask', methods=["POST"])
@login_required
def giveMeTask():
    q_duration = request.form['duration']
    q_me = request.form['me']
    q_friend = request.form['me']

    if q_friend and 'token' in session:
        graph = facebook.GraphAPI(session['token'])
        friends = graph.get_connections("me", "friends")
        session["friend_list"] =friends;
        friend_id_list = [friend['id'] for friend in friends['data']]
    else:
        friend_id_list = []

    all_task = [] 
    # friends
    for uid in friend_id_list:
        friend = User.all().filter("uid =", uid).get()
        friend_tasks = friend.task_set
        #for friend_task in friend_tasks:
            #friend_task
        all_task.extend(friend_tasks)

    # my task
    user = session['user'] 
    tasks = user.task_set
    all_task.extend(tasks)

    task_list = []
    for task in all_task:
        key = task.key()
        if task and int(task.duration) == int(q_duration) :
            task_list.append({"description": task.description, "duration": task.duration, "done": task.done, "isPrivate": task.isPrivate, "key": str(key), "timestamp": str(task.timestamp), "ownername": task.ownername})
    session['my_task_list'] = task_list
    return jsonify({"task_list": task_list})

@app.route('/tasks', methods=["GET"])
@login_required
def allTask():
    user = session['user'] 
    tasks_of_user = user.task_set

    task_list = []
    for task in tasks_of_user:
        key = task.key()
        if task:
            task_list.append({"description": task.description, "duration": task.duration, "done": task.done, "isPrivate": task.isPrivate, "key": str(key), "timestamp": str(task.timestamp), "ownername": task.ownername})

    return jsonify({"task_list": task_list})
#TODO
@app.route('/deletetask', methods=["POST"])
@login_required
def deleteTask():
    return render_template('gettask.html', data= tasks)

@app.route('/finishtasks', methods=["POST"])
@login_required
def finishTask():
    app.logger.debug(request.form['id'])
    task = db.get(request.form['id'])
    task.done = true
    return jsonify(task)

@app.route('/gettask')
@login_required
def gettask():
    return render_template('gettask.html')
