from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi import HTTPException
from models import Roaster
from models import Coffee
from models import User
import os
from dotenv import load_dotenv

load_dotenv(".env")

# ~~~ Seed Utilities ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Seed Utilities ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Seed Utilities ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Could refactor as ternaries [on_true] if [expression] else [on_false], but lines of code are long
def seed_roasters():
    if db.session.query(Roaster).filter_by(name="Alma").first():
        pass
    else:
        alma = Roaster(name="Alma")
        db.session.add(alma)

    if db.session.query(Roaster).filter_by(name="Metric").first():
        pass
    else:
        metric = Roaster(name="Metric")
        db.session.add(metric)

    if db.session.query(Roaster).filter_by(name="Sparrows").first():
        pass
    else:
        sparrows = Roaster(name="Sparrows")
        db.session.add(sparrows)

    if db.session.query(Roaster).filter_by(name="Dummy Roaster").first():
        pass
    else:
        dummy_roaster = Roaster(name="Dummy Roaster")
        db.session.add(dummy_roaster)

    if db.session.new:
        db.session.commit()
    else:
        raise HTTPException(status_code=400, detail=[{"msg": "No new Roasters seeded."}])


def seed_coffees():
    # could refactor as ternaries [on_true] if [expression] else [on_false], but lines of code are long
    if db.session.query(Coffee).filter_by(name="Honey Process").first():
        pass
    else:
        hp = Coffee(name="Honey Process", roast="Light", roaster_id=db.session.query(Roaster).filter_by(name="Alma").first().id)
        db.session.add(hp)

    if db.session.query(Coffee).filter_by(name="Extra").first():
        pass
    else:
        extra = Coffee(name="Extra", roast="Dark", roaster_id=db.session.query(Roaster).filter_by(name="Alma").first().id)
        db.session.add(extra)

    if db.session.query(Coffee).filter_by(name="Colorized").first():
        pass
    else:
        color = Coffee(name="Colorized", roast="Light", roaster_id=db.session.query(Roaster).filter_by(name="Metric").first().id)
        db.session.add(color)

    if db.session.query(Coffee).filter_by(name="Dimtu Tero").first():
        pass
    else:
        dimtu = Coffee(name="Dimtu Tero", roast="Medium", roaster_id=db.session.query(Roaster).filter_by(name="Sparrows").first().id)
        db.session.add(dimtu)

    if db.session.new:
        db.session.commit()
    else:
        raise HTTPException(status_code=400, detail=[{"msg": "No new Coffees seeded."}])


def seed_users():
    if db.session.query(User).filter_by(username=os.environ["FASTAPI_ADMIN_USERNAME"]).first():
        pass
    else:
        admin = User(username=os.environ["FASTAPI_ADMIN_USERNAME"], email=os.environ["FASTAPI_ADMIN_EMAIL"], password=os.environ["FASTAPI_ADMIN_PASSWORD"])
        db.session.add(admin)

    if db.session.query(User).filter_by(username="testuser1").first():
        pass
    else:
        test_user1 = User(username="testuser1", email="testuser1@testuser1.com", password="testuser1")
        db.session.add(test_user1)

    if db.session.query(User).filter_by(username="testuser2").first():
        pass
    else:
        test_user2 = User(username="testuser2", email="testuser1@testuser2.com", password="testuser2")
        db.session.add(test_user2)

    if db.session.new:
        db.session.commit()
    else:
        raise HTTPException(status_code=400, detail=[{"msg": "No new Users seeded."}])