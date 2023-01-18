from fastapi_sqlalchemy import DBSessionMiddleware, db
from models import Roaster
from models import Coffee
from models import User


# ~~~ Seed Utilities ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Seed Utilities ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Seed Utilities ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def seed_roasters():
    alma = Roaster(name="Alma")
    metric = Roaster(name="Metric")
    sparrows = Roaster(name="Sparrows")
    dummy_roaster = Roaster(name="Dummy Roaster")
    db.session.add(alma)
    db.session.add(metric)
    db.session.add(sparrows)
    db.session.add(dummy_roaster)
    db.session.commit()


def seed_coffees():
    hp = Coffee(name="Honey Process", roast="Light", roaster_id=db.session.query(Roaster).filter_by(name="Alma").first().id)
    extra = Coffee(name="Extra", roast="Dark", roaster_id=db.session.query(Roaster).filter_by(name="Alma").first().id)
    color = Coffee(name="Colorized", roast="Light", roaster_id=db.session.query(Roaster).filter_by(name="Metric").first().id)
    dimtu = Coffee(name="Dimtu Tero", roast="Medium", roaster_id=db.session.query(Roaster).filter_by(name="Sparrows").first().id)
    db.session.add(hp)
    db.session.add(extra)
    db.session.add(color)
    db.session.add(dimtu)
    db.session.commit()


def seed_users():
    admin = User(username="admin", email="admin@admin.com", password="admin")
    test_user1 = User(username="testuser1", email="testuser1@testuser1.com", password="testuser1")
    test_user2 = User(username="testuser2", email="testuser1@testuser2.com", password="testuser2")
    db.session.add(admin)
    db.session.add(test_user1)
    db.session.add(test_user2)
    db.session.commit()

