#!/usr/bin/env python2.7

# Import modules and dependencies.
import os
import base64
from datetime import datetime
from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash, make_response
from sqlalchemy import create_engine, asc, desc, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from db_setup import Base, User, Place
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from functools import wraps


# Create a new Flask app.
app = Flask(__name__)


# Load client_secret.json for Google Oauth.
# This allows for the absolute path to be retried for the file,
# regardless of environment.
current_dir = os.path.dirname(os.path.abspath(__file__))
fb_client_secret = os.path.join(current_dir, 'fb_client_secret.json')


APPLICATION_NAME = "project-power"


# Connect to the database.
# Create database session.
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()


def login_required(f):
    '''Checks to see whether a user is logged in'''
    @wraps(f)
    def x(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return x


# Create anti-forgery state token
@app.route('/login')
def showLogin():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('fbsignin.html', STATE=state)


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token


    app_id = json.loads(open(fb_client_secret, 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open(fb_client_secret, 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "You are logged out."

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully logged out.")
        return redirect(url_for('showMap'))
    else:
        flash("You were not logged in.")
        return redirect(url_for('showMap'))

# Main landing page for Places of Power
@app.route('/main')
def Main():    
    return render_template('index.html')


# The Help Page route decorator.
@app.route('/help')
def showHelp():
    return render_template('help.html')


# Main page route decorator showing all Places of Power
@app.route('/')
@app.route('/place')
def showPlaces():
    places = session.query(Place).order_by(desc(Place.date))
    return render_template('places.html',
                               places=places)


# Add a new Place of Power route decorator
@app.route('/place/new', methods=['GET', 'POST'])
@login_required
def addPlace():
    if request.method == 'POST':
        newPlace = Place(
            user_name=request.form['user_name'],
            name=request.form['name'],
            description=request.form['description'],
            picture_url=request.form['picture_url'],
            lat=request.form['lat'],
            lng=request.form['lng'],
            date=datetime.now(),
            user_id=login_session['user_id'])
        session.add(newPlace)
        flash('New Details for %s Successfully Added!' % newPlace.name)
        session.commit()
        return redirect(url_for('showPlaces'))
    else:
        return render_template('newplace.html')


# Shows details of a Place of Power route decorator
@app.route('/place/<int:place_id>')
@app.route('/place/<int:place_id>/details')
def showPlace(place_id):
    place = session.query(Place).filter_by(id=place_id).one()
    creator = getUserInfo(place.user_id)
    if ('username' 
        not in login_session 
        or creator.id != login_session['user_id']):
        return render_template('publicplace.html', place=place)
    else:
        return render_template('place.html', place=place)


# Delete a Place of Power route decorator
@app.route('/place/<int:place_id>/delete', methods=['GET', 'POST'])
@login_required
def deletePlace(place_id):
    placeToDelete = session.query(
        Place).filter_by(id=place_id).one()
    if login_session['user_id'] != placeToDelete.user_id:
        return render_template('unauth.html')
    if request.method == 'POST':
        session.delete(placeToDelete)
        session.commit()
        flash('%s Successfully Deleted!' % (placeToDelete.name))
        return redirect(url_for('showPlaces'))
    else:
        return render_template('deleteplace.html',
                               place=placeToDelete)


# Edit details of a Place of Power route decorator
@app.route('/place/<int:place_id>/edit', methods=['GET', 'POST'])
@login_required
def editPlace(place_id):
    editedPlace = session.query(
        Place).filter_by(id=place_id).one()
    if login_session['user_id'] != editedPlace.user_id:
        return render_template('unauth.html')
    if request.method == 'POST':
        if request.form['user_name']:
            editedPlace.user_name = request.form['user_name']
        if request.form['name']:
            editedPlace.name = request.form['name']
        if request.form['description']:
            editedPlace.description = request.form['description']
        if request.form['picture_url']:
            editedPlace.picture_url = request.form['picture_url']
        if request.form['lat']:
            editedPlace.lat = request.form['lat']
        if request.form['lng']:
            editedPlace.lng = request.form['lng']

        session.add(editedPlace)
        session.commit()
        
        flash('Place of Power has been successfully updated!')
        return redirect(url_for('showPlaces'))
    else:
        return render_template('editplace.html',
                                place_id=place_id,
                                place=editedPlace)


# The Google Maps page route decorator
@app.route('/map')
def showMap():
    return render_template('map.html')


# JSON APIs to feed Places info from database.
@app.route('/json')
def placesJSON():
    places = session.query(Place).all()
    return jsonify(places=[r.serialize for r in places])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()