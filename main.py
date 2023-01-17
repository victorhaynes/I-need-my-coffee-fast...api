# ~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import uvicorn
from fastapi import FastAPI, status, HTTPException

from dotenv import load_dotenv
import os

from fastapi_sqlalchemy import DBSessionMiddleware, db
from models import Coffee
from models import Roaster

from schemas import Coffee as SchemaCoffee
from schemas import Roaster as SchemaRoaster


# ~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


# ~~~ Routes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Routes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Routes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.get("/")
async def root():
    return {"message": "You are live--on a FastAPI application created by Victor Haynes."}

### Coffee Routes
### Coffee Routes
### Coffee Routes
@app.get("/coffees", status_code=status.HTTP_200_OK)
def index_coffees():
    return db.session.query(Coffee).all()


@app.post("/coffees", response_model=SchemaCoffee, status_code=status.HTTP_201_CREATED)
def create_coffee(coffee: SchemaCoffee):
    coffee = Coffee(name=coffee.name, roast=coffee.roast, roaster_id=coffee.roaster_id)
    db.session.add(coffee)
    db.session.commit()
    return coffee


@app.get("/coffees/{id}", status_code=status.HTTP_200_OK)
def show_coffee(id: int):
    coffee = db.session.query(Coffee).get(id)
    if coffee:
        return coffee
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])
    

@app.put("/coffees/{id}", response_model=SchemaCoffee, status_code=status.HTTP_202_ACCEPTED)
def update_coffee(id: int, new_coffee: SchemaCoffee):
    coffee = db.session.query(Coffee).get(id)
    coffee.name = new_coffee.name
    coffee.roast = new_coffee.roast
    coffee.roaster_id = new_coffee.roaster_id
    db.session.commit()
    return coffee


@app.delete("/coffees/{id}", status_code=status.HTTP_202_ACCEPTED)
def destroy_coffee(id: int):
    coffee = db.session.query(Coffee).get(id)
    db.session.delete(coffee)
    db.session.commit()
    return {"message": f"Coffee ID# {id} successfully deleted."}


@app.get("/coffees/{id}/roaster", status_code=status.HTTP_200_OK)
def show_coffee_roaster(id: int):
    coffee = db.session.query(Coffee).get(id)
    return coffee.roaster


### Roaster Routes
### Roaster Routes
### Roaster Routes
@app.get("/roasters", status_code=status.HTTP_200_OK)
def index_roasters():
    return db.session.query(Roaster).all()


@app.post("/roasters", response_model=SchemaRoaster, status_code=status.HTTP_201_CREATED)
def create_roaster(roaster: SchemaRoaster):
    roaster = Roaster(name=roaster.name)
    db.session.add(roaster)
    db.session.commit()
    return roaster


@app.get("/roasters/{id}", status_code=status.HTTP_200_OK)
def show_roaster(id: int):
    roaster = db.session.query(Roaster).get(id)
    if roaster:
        return roaster
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])


@app.put("/roasters/{id}", response_model=SchemaRoaster, status_code=status.HTTP_202_ACCEPTED)
def update_rosater(id: int, new_roaster: SchemaRoaster):
    roaster = db.session.query(Roaster).get(id)
    roaster.name = new_roaster.name
    db.session.commit()
    return roaster


@app.delete("/roasters/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_roater(id: int):
    roaster = db.session.query(Roaster).get(id)
    db.session.delete(roaster)
    db.session.commit()
    return {"message": f"Roaster ID# {id} successfully deleted"}


@app.get("/roasters/{id}/coffees", status_code=status.HTTP_200_OK)
def show_roaster_coffees(id: int):
    roaster = db.session.query(Roaster).get(id)
    return roaster.coffees


# Run locally, outside of container from /.venv -> $ python main.py
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)