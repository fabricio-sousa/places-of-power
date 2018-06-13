# Project Places of Power | Backend (In production)

#### Developer: Fabricio Sousa

## Description

This is a RESTful web app created via Python and the Flask framework, SQLAlchemy, along with third-party Google OAuth authentication, backed by a PostgreSQL database. Users can login in order to create, read, update and delete their own Places of Power. It will eventually serve those places to the frontend web app that will render those places as markers on World Google Map. Front end features KnockoutJS, JQuery, HTML5 and CSS. Markers on the Google Map will feature InfoWindows containing content served by the backend, as well as from Wikipedia's API.

## Frameworks, Libraries, and APIs

Javascript, KnockoutJS, jQuery, Bootstrap, the Google Maps API, Wikipedia's API and of course html and css. Google Map styles from SnazzyMaps.

## Frameworks, Libraries, and APIs

HTML5 and CSS, Python 2.7, Javascript, PostgreSQL, Flask.

## Software Used For This Project

* `fail2ban` - to help prevent brute-force server attacks.
* `sendmail` - to send the admin mail anytime suspicious activity is detected via fail2ban.
* `unattended-upgrades` - to allow automatic system updates.
* `apache2` - installs Apache Web Server package.
* `libapache2-mod-wsgi python-dev` - enables Apache to serve Flask apps
* `git` - for version control and cloning the remote repository.
* `pip` - allows for Python package installs.
* `virtualvenv` - installs the virtual environment.
* `Flask` - to install the Flask module.
* Project dependencies software to allow Python to interact with Flask, the webserver and database:
`bleach`, `httplib2`, `request`, `oauth2client`, `sqlalchemy`, `python-psycopg2`
* `libpq-dev python-dev` and `postgresql postgresql-contrib` - installs Python packages for PostgreSQL.

## Installation and How To Run

1. Clone repo into your Apache environment on Linux/Ubuntu.
2. Access the live version [here](http://ec2-18-220-254-32.us-east-2.compute.amazonaws.com/).
3. Please note, the "Maps" site is not yet live. I created a dummy version using client side data to illustrate functionality. You can access the repo for that [here](https://github.com/fabricio-sousa/fabricio-sousa.github.io) and the live version [here](https://fabricio-sousa.github.io/).

