from application import app
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

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserForm()  
    if form.validate_on_submit():
        # Unique username
        user = db.GqlQuery("SELECT * "
                "FROM User "
                "WHERE username = :1 ", form.username.data)
        if user.count() > 0:
            flash('Username already exists', 'warning')
            return render_template('signup.html', form=form, username=check_user())

        user = User(username = form.username.data,
                    email = form.email.data,
                    passwd = hashlib.sha224(form.passwd.data).hexdigest(),
                    f_name = form.f_name.data,
                    l_name = form.l_name.data,
                    #mpg = form.mpg.data,
                    #fare = form.fare.data,
                    search_history = [],
                    rec_loc = [],
                    fav_loc = []
                    )
        user.put()
        flash('User created', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form, username=check_user())

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        passwd = hashlib.sha224(request.form['passwd']).hexdigest()
        user_temp = db.GqlQuery("SELECT * "
                "FROM User "
                "WHERE username = :1 ", username)

        user = db.GqlQuery("SELECT * "
                "FROM User "
                "WHERE username = :1 AND passwd = :2", username, passwd)
        if user.count() > 0:
            session['username'] = username
            flash('Login successful', 'success')
       	elif user_temp.count() > 0 and user_temp[0].passwd != passwd:
            flash('Password incorrect', 'warning')
        else:
            flash('User does not exist', 'warning')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/user/<username>', methods = ["GET", "POST"])
def user(username):
    username = check_user()
    q = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE username = :1", username)

    ranked_co2 = db.GqlQuery("SELECT *"
                                "FROM User "
                                "ORDER BY carbon DESC")
   
    ranked_savings = db.GqlQuery("SELECT *"
                                    "FROM User "
                                    "ORDER BY savings DESC")
    for index, item in enumerate(ranked_savings):
        if item.username == username:
            rank_savings = ordinal(index + 1)
    for index, item in enumerate(ranked_co2):
        if item.username == username:
            rank_co2 = ordinal(index + 1)
    user = q[0]
    favorite = q[0].fav_loc
    favorite.sort()
    email = q[0].email 
    default = "mm" #"http://green-cents.appspot.com/static/img/logo.png" # green-cents logo default avatar
    size = 50 
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    
    form = UpdateUserForm()  
    if form.is_submitted():
        settings = 1
        if form.validate():
            user.f_name = form.f_name.data
            user.l_name = form.l_name.data
            user.email = form.email.data
            if form.mpg.data:
                user.mpg = form.mpg.data
            if form.transit_cost.data:
                user.transit_cost = form.transit_cost.data
            if form.passwd.data:
                user.passwd = hashlib.sha224(form.passwd.data).hexdigest()
                          
            user.put()
            flash('Settings updated', 'success')
            #return redirect(url_for('user', username=username))
    else:
        settings = 0

    return render_template('user.html', current_user=user, fav_loc=favorite, username=check_user(),
    gurl=gravatar_url, form=form, settings=settings, rank_co2=rank_co2, rank_savings=rank_savings)

def ordinal(n):
    if 10 < n < 14: return u'%sth' % n
    if n % 10 == 1: return u'%sst' % n
    if n % 10 == 2: return u'%snd' % n
    if n % 10 == 3: return u'%srd' % n
    return u'%sth' % n

@app.route('/bmap')
def bing_map():
    username=check_user()
    rec = None
    fav = None
    if username:
        q = db.GqlQuery("SELECT * "
                "FROM User "
                "WHERE username = :1", username)
        rec = q[0].rec_loc
        fav = q[0].fav_loc
    return render_template('bmap.html', rec_loc=rec, fav_loc=fav,  username=check_user())

@app.route('/about')
def about():
    return render_template('about.html', username=check_user())

@app.route('/meet')
def meet():
    return render_template('meet.html', username=check_user())

def add_to_rec(the_list, item):
    """ helper function: maintain rrd for recent locations """
    """ TODO: FULL should be customizable """
    FULL = 10 
    if len(the_list) == FULL:
        the_list.pop()
    if item not in the_list:
        the_list.insert(0, item)

@app.route('/fetch_locs', methods = ["GET", "POST"])
def fetch_locs():
    """ fetch both rec and fav locs """
    if request.method == "POST":
        username = check_user()
        if not username:
            return ""
        q = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE username = :1", username)
        rec = q[0].rec_loc
        favs = q[0].fav_loc 
        fav = [item.split(":")[0] for item in favs]
        fav_address = [item.split(":")[1] for item in favs]

        data = {"rec": rec, "fav": fav, "fav_address": fav_address}
        return jsonify(data)

@app.route('/add_fav', methods = ["GET", "POST"])
def add_fav():
    """ from ajax, input: name and address """
    if request.method == "POST":
        username = check_user()
        if not username:
            return ""
        q = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE username = :1", username)
        name = request.form["name"]
        address = request.form["address"]
        
        user = q[0] 
        item = name + ":" + address.replace("%20", " ")
        user.fav_loc.append(item)   
        user.put()
        return jsonify({})

@app.route('/search', methods = ["GET", "POST"])
def search():
    username = check_user()
    if request.method == "POST":
        # Get args
        start = request.form["from"].replace(" ", "%20")
        end = request.form["to"].replace(" ", "%20")
        method = request.form["method"]
        maxSolns = request.form["maxSolns"]
        # Construct request url 
        request_url = "http://dev.virtualearth.net/REST/V1/Routes/{method}?wp.0={start}&wp.1={end}&timeType=Departure&routePathOutput=Points&dateTime=3:00:00PM&optmz=distance&{maxSolns}=3&distanceUnit=mi&output=json&key=AupvjJj-8-1RYDPSIIxnP8IQfomRdF8CJAyhe4KrWMBNS7pdOkUDRBU2OtlBoPu8".format(method=method, start=start, end=end, maxSolns=maxSolns)
        r = urlfetch.fetch(request_url, deadline=50)
        if r.status_code != 200:
            return "Error"
        raw = json.loads(r.content)

        # for no user
        mpg=20
        fare=2

        if username:
            q = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE username = :1", username)
            user = q[0]
            #Set recent locations
            add_to_rec(user.rec_loc, start.replace("%20", " "))
            add_to_rec(user.rec_loc, end.replace("%20", " "))
            #Get mpg fare for calculation
            mpg = user.mpg 
            fare = user.transit_cost 
             
            user.put()

        routes = raw['resourceSets'][0]['resources']
        #routes = rjson[0]['resources']

        data = {}
        associ = ["a","b","c"]
        # support three options
        index = 0

        # use first option
        first = True
        for route in routes:
            # use first option
            if first: first = False
            else: break 

            # This is for just Transit
            if method == "Transit":
                points = route['routePath']['line']['coordinates']
                distance = 0
                p0 = geopy.Point(points[0][0], points[0][1])
                for point in points:
                   p1 = geopy.Point(point[0], point[1])
                   distance += geopy.distance.distance(p0, p1).miles
                   p0 = p1
                dist = route['travelDistance']
                distance -= dist
            else: 
                distance = route['travelDistance']
            time = route['travelDuration']

            # Get Instruction for parts
            legs = route['routeLegs'][0]['itineraryItems']
            parts = []
            usedTypes = set([])
            transfer = 0
            for leg in legs:
                part = {} 
                if leg['transitTerminus']:
                    info = "Terminus is " + str(leg['transitTerminus'])
                else:
                    info = ""

                part["ins"] = leg['instruction']['text'],
                part["dis"]  = leg['travelDistance']
                part["info"] = info
                part["type"] = leg['iconType']
                if leg['iconType'] != 'Walk':
                    if usedTypes and leg['iconType'] not in usedTypes:
                        transfer += 1
                    usedTypes.add(str(leg['iconType']))
                parts.append(part)


            # Construct the json 
            data[associ[index]] = {}
            data[associ[index]]['parts'] = parts
            data[associ[index]]['distance'] = distance
            data[associ[index]]['time'] = time
            data[associ[index]]['url'] = request_url
            data[associ[index]]['co2'] = carbon(distance, mpg, method)
            data[associ[index]]['cost'] = cost(distance, fare, mpg, method, transfer)
            
            index += 1
            
        return jsonify(data) 

@app.route('/update_fav', methods = ["GET", "POST"])
def update_fav():
    """ Update Fav Location"""
    if request.method == "POST":
        username = check_user()
        if not username:
            return ""
        old_name = request.form['old_name'] 
        name = request.form['name'] 
        address = request.form['address'] 
        q = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE username = :1", username)
        user = q[0]
        new_fav_loc = [item for item in user.fav_loc]

        for loc in user.fav_loc: 
            if old_name == loc.split(":")[0]:
                new_fav_loc.remove(loc) 
                break

        new_item = name + ":" + address.replace("%20", " ")
        new_fav_loc.append(new_item)
        user.fav_loc = new_fav_loc
        user.put()
        return jsonify("")


@app.route('/delete_fav', methods = ["GET", "POST"])
def delete_fav():
    """ Delete Fav Location"""
    if request.method == "POST":
        username = check_user()
        if not username:
            return ""
        name = request.form['name'] 
        q = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE username = :1", username)
        user = q[0]
        new_fav_loc = [item for item in user.fav_loc]

        for loc in user.fav_loc: 
            if name == loc.split(":")[0]:
                new_fav_loc.remove(loc) 
                break
        user.fav_loc = new_fav_loc
        user.put()
        return jsonify("")

@app.route('/update_savings', methods = ["GET", "POST"])
def update_savings():
    """ Update savings """
    if request.method == "POST":
        username = check_user()
        if not username:
            return "1"
        cost = request.form['cost'] 
        co2 = request.form['co2'] 
        q = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE username = :1", username)
        user = q[0]
        #carbon reduction is coming in kg
        user.carbon += 1000 * float(co2)
        user.savings += float(cost)

        user.put()
        return "0"
