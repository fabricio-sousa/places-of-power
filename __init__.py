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
client_secret = os.path.join(current_dir, 'client_secret.json')

CLIENT_ID = json.loads(
    open(client_secret, 'r').read())['web']['client_id']
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


# Create anti-forgery state token route decorator.
@app.route('/login')
def showLogin():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state
    # return "The current session state is %s" % session['state']
    return render_template('login.html', STATE=state)


# gconnect route decorator.
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Login and/or register a user using Google OAuth."""
    # Check if the posted STATE matches the session state
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Get the token sent through ajax
    token = request.data

    # Verify it
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, g_requests.Request(), CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            # Wrong issuer
            message = 'Wrong issuer.'
            response = make_response(json.dumps(message), 401)
            response.headers['Content-Type'] = 'application/json'

            return response

    except ValueError:
        # Invalid token
        message = 'Invalid token.'
        response = make_response(json.dumps(message), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # ID token is valid. Get the user's Google Account ID from the decoded token.
    gplus_id = idinfo['sub']

    # Check that our client's id matches that of the token
    # returned by Google API's server
    if idinfo['aud'] != CLIENT_ID:
        message = "Token's client ID does not match this app's."
        response = make_response(json.dumps(message), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Verify that the user's NOT ALREADY LOGGED IN

    # Get the access token stored in the session if there is one
    stored_token = session.get('token')
    # Get the user id stored in the session if there is one
    stored_gplus_id = session.get('gplus_id')

    # Check if there is already an access token in the session
    # and if so, if the id of the token from the CREDENTIALS OBJECT
    # matches the id stored in the session
    if stored_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                  'Current user is already connected. '), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # If we get this far, the access token is VALID
    # and it's THE RIGHT ACCESS TOKEN.
    # The user can be successfully logged in

    # 1. Store the access token in the session
    session['token'] = token
    session['gplus_id'] = gplus_id

    # 3. Store user info in the session
    session['username'] = idinfo['name']
    session['picture'] = idinfo['picture']
    session['email'] = idinfo['email']

    # Specify we used Google to sign in
    session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(session['email'])
    if not user_id:
        user_id = createUser(session)
    session['user_id'] = user_id

    output = ''
    output += '<img src="'
    output += login_session['picture']
    output += '''"style = "width: 150px;
                            height: 150px;border-radius: 75px;
                            -webkit-border-radius: 75px;
                            -moz-border-radius: 75px;">'''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '! Retrieving the latest Places of Power...</h1>'
   
    
    flash("You are now logged in as %s" % login_session['username'])
    return output


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


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You are now logged out.")
        return redirect(url_for('showPlaces'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showPlaces'))


# Main landing page for Places of Power
@app.route('/')
def Main():    
    return render_template('index.html')


# The Help Page route decorator.
@app.route('/help')
def showHelp():
    return render_template('help.html')


# Main page route decorator showing all Places of Power
@app.route('/place')
def showPlaces():
    places = session.query(Place).order_by(desc(Place.date))

    if 'username' not in login_session:
        return render_template('publicplaces.html',
                               places=places)
    else:
        return render_template('places.html',
                               places=places)


# Add a new Place of Power route decorator
@app.route('/place/new', methods=['GET', 'POST'])
@login_required
def addPlace():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newPlace = Place(
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
        return render_template('publicplace.html',
                               place=place,
                               creator=creator)
    else:
        return render_template('place.html',
                               place=place,
                               creator=creator)


# Delete a Place of Power route decorator
@app.route('/place/<int:place_id>/delete', methods=['GET', 'POST'])
@login_required
def deletePlace(place_id):
    placeToDelete = session.query(
        Place).filter_by(id=place_id).one()
    if placeToDelete.user_id != login_session['user_id']:
        return '''<script>function myFunction()
                {alert('You are not authorized to delete this place.
                Please add your own Place of Power!');}
                </script><body onload='myFunction()'>'''
    if request.method == 'POST':
        session.delete(placeToDelete)
        session.commit()
        flash('%s Successfully Deleted!' % placeToDelete.name)
        session.commit()
        return redirect(url_for('showPlaces', place_id=place_id))
    else:
        return render_template('deleteplace.html',
                               place=placeToDelete)


# Edit details of a Place of Power route decorator
@app.route('/place/<int:place_id>/edit', methods=['GET', 'POST'])
@login_required
def editPlace(place_id):
    editedPlace = session.query(
        Place).filter_by(id=place_id).one()
    if editedPlace.user_id != login_session['user_id']:
        return '''<script>function myFunction()
                {alert('You are not authorized to edit this place.
                Please add your own Place of Power!');}
                </script><body onload='myFunction()'>'''
    if request.method == 'POST':
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
            flash('Place of Power has been successfully updated!')
            return redirect(url_for('showPlaces', place_id=place_id))
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