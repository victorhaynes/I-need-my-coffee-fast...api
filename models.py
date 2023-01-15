from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()



class Coffee(Base):
    __tablename__ = "coffees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    roast = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    roaster_id = Column(Integer, ForeignKey("roasters.id"))

    roaster = relationship("Roaster")


class Roaster(Base):
    __tablename__ = "roasters"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())