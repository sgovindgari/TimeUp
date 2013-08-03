from application import app
from calculation import carbon, cost
from flask import render_template, request, flash, redirect, url_for, session , jsonify
from google.appengine.ext import db
from google.appengine.api import urlfetch
from models import *
from forms import *
import geopy, geopy.distance
import time, random, urllib, hashlib, json

@app.route('/')
def index():
  return render_template('index.html')
