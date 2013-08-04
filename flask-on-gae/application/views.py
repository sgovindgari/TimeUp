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
        except GraphAPIError:
            name = "token Error"

    return render_template('test.html', data = name)
