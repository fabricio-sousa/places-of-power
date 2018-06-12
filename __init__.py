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
import random
import string
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
