from application import app
from flask import render_template, request, flash, redirect, url_for, session , jsonify
from google.appengine.ext import db
from google.appengine.api import urlfetch
from models import *
from forms import *
import geopy, geopy.distance
import time, random, urllib, hashlib, json
import facebook

@app.route('/loggedin')
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
	    name = profile["name"]
	    newUser = User(id = int(uid), username = name)
	    newUser.save()
	except facebook.GraphAPIError:
	    name = "token Error"
    return render_template('test.html', data = name)
    
@app.route('/tasks/new', methods=["POST"])
def newTask():
    desc = request.form['description']
    duration = int(request.form['duration'])
    done = bool(request.form['done'])
    isPrivate = bool(request.form['isPrivate'])

    newTask = Task(description = desc, duration = duration, done = done, isPrivate = isPrivate)
    key = newTask.save()

    app.logger.debug("added %s   %s  %s" % (key, desc, type(key)))
    user = session['user'] 
    user.tasks.insert(0, key)
    user.save()
    session['user'] = user

    data = {"status": "ok"}
    return jsonify(data)

@app.route('/tasks', methods=["GET"])
def allTask():
    if 'user' in session:
        app.logger.debug(session['user'].tasks)
    tasks = db.get(session['user'].tasks[:15])

    task_list = [{"description": task.description, "duration": task.duration, "done": task.done, "isPrivate": task.isPrivate} for task in tasks]
    return jsonify({"task_list": task_list})

@app.route('/gettask')
def gettask():
    return render_template('gettask.html')
