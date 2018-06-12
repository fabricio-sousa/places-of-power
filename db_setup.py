from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))


class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    date = Column(DateTime, nullable=False)
    description = Column(String(250), nullable=False)
    lat = Column(String(250), nullable=False)
    lng = Column(String(250), nullable=False)
    picture_url = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'          : self.name,
            'id'            : self.id,
            'description'   : self.description,
            'lat'           : self.lat,
            'lng'           : self.lng,
            'picture_url'   : self.picture_url
        }

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

Base.metadata.create_all(engine)