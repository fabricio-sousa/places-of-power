from db_setup import *
from sqlalchemy import create_engine
import datetime
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()

'''
place = session.query(Place).filter_by(id=6).one()
session.delete(place)
session.commit()
'''

'''
user = session.query(User).filter_by(id=6).one()
session.delete(user)
session.commit()
'''

# print "Place and User deleted!"

users = session.query(User).all()

for user in users:
    print user.name
    print user.id
    print user.email
    








