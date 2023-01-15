# ~~~ Imports
# ~~~ Imports
# ~~~ Imports
import uvicorn
from fastapi import FastAPI

from dotenv import load_dotenv
import os

from fastapi_sqlalchemy import DBSessionMiddleware, db
from models import Coffee
from models import Roaster

from schemas import Coffee as SchemaCoffee
from schemas import Roaster as SchemaRoaster


# ~~~ Config
# ~~~ Config
# ~~~ Config
load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])



# ~~~ Routes
# ~~~ Routes
# ~~~ Routes
@app.get("/")
async def root():
    return {"message": "You are live--on a FastAPI application created by Victor Haynes."}


@app.get("/coffees")
def get_coffees():
    coffees = db.session.query(Coffee).all()
    return coffees


@app.post("/coffees", response_model=SchemaCoffee)
def create_coffee(coffee: SchemaCoffee):
    db_coffee = Coffee(name=coffee.name, roast=coffee.roast, roaster_id=coffee.roaster_id)
    db.session.add(db_coffee)
    db.session.commit()
    return db_coffee



@app.post("/roasters", response_model=SchemaRoaster)
def create_roaster(roaster: SchemaRoaster):
    db_roaster = Roaster(name=roaster.name)
    db.session.add(db_roaster)
    db.session.commit()
    return db_roaster



# Run locally, outside of container from /.venv
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)