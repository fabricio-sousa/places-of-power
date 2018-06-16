# Project Places of Power (Portfolio Demo)

#### Developer: Fabricio Sousa
#### Live Version: http://ec2-18-220-254-32.us-east-2.compute.amazonaws.com/main

## Description

This project serves as a demonstration of everything I've mastered so far in my Full Stack Development education. This is a RESTful web app with a backend developed with Python and the Flask framework, SQLAlchemy, along with third-party Google OAuth authentication, a PostgreSQL database and deployed to an Amazon Lightsail Ubuntu Linux instance running Apache. Users can login in order to create, read, update and delete their own Places of Power (CRUD operations). A json router app decorator allows for the data to be served to the frontend, which renders those places as markers on the World Google Map. The frontend features KnockoutJS, JQuery, HTML5 and CSS. Markers on the Google Map feature infowindows with content served by the backend. Additional content might will added via 3rd party API integration.


## Backend Frameworks, Libraries, and APIs

HTML5 and CSS, Python 2.7, Javascript, PostgreSQL, Flask.


## Frontend Frameworks, Libraries, and APIs

Javascript, KnockoutJS, jQuery, Bootstrap, the Google Maps API, Wikipedia's API and of course html and css. Google Map styles from SnazzyMaps.


## Linux Deployment - Software Used

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
2. Access the live version [here](http://ec2-18-220-254-32.us-east-2.compute.amazonaws.com/main).

