from db_setup import *
from sqlalchemy import create_engine
import datetime
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()

session.query(Place).delete()
session.query(User).delete()

# Create dummy users
User1 = User(name="Akhenaten", email="example@example.com",
             picture='https://i.imgur.com/d2lRHgd.jpg')
session.add(User1)
session.commit()

# Create fake categories
Place1 = Place(name="The Great Pyramid of Giza",
               date=datetime.datetime.now(),
               description="One of the 7 Wonders of the Ancient World. A place of magic and mystery.",
               lat="29.976480",
               lng="31.131302",
               picture_url="https://i.imgur.com/E4DZ4nH.jpg",
               user_id=1)
session.add(Place1)
session.commit()