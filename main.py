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
from models import User

from schemas import Coffee as CoffeeSchema
from schemas import Roaster as RoasterSchema
from schemas import User as UserSchema
from schemas import UserResponse as UserResponseSchema
from schemas import CoffeeResponse as CoffeeResponseSchema
from schemas import RoasterResponse as RoasterResponseSchema 


# ~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


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


@app.get("/seed", status_code=status.HTTP_201_CREATED)
def seed_database():
    seed_roasters()
    seed_coffees()
    return {"message": "Seeded database with Roasters and Coffees successfully."}


@app.delete("/delete", status_code=status.HTTP_202_ACCEPTED)
def delete_all_records():
    db.session.query(Coffee).delete()
    db.session.commit()
    db.session.query(Roaster).delete()
    db.session.commit()
    return {"message": "Deleted existing Coffee, Roaster records."}


# ~~~ Routes / Endpoints ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Routes / Endpoints ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Routes / Endpoints ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.get("/")
async def root():
    return {"message": "You are live--on a FastAPI application created by Victor Haynes. Navigate to /docs in browser to discover API."}


### Coffee Routes
### Coffee Routes
### Coffee Routes
@app.get("/coffees", response_model=list[CoffeeResponseSchema], status_code=status.HTTP_200_OK)
def index_coffees():
    return db.session.query(Coffee).all()


@app.post("/coffees", response_model=CoffeeResponseSchema, status_code=status.HTTP_201_CREATED)
def create_coffee(coffee: CoffeeSchema):
    new_coffee = Coffee(name=coffee.name, roast=coffee.roast, roaster_id=coffee.roaster_id)
    db.session.add(new_coffee)
    db.session.commit()
    return new_coffee


@app.get("/coffees/{id}", response_model=CoffeeResponseSchema,status_code=status.HTTP_200_OK)
def show_coffee(id: int):
    coffee = db.session.query(Coffee).get(id)
    if coffee:
        return coffee
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])
    

@app.put("/coffees/{id}", response_model=CoffeeResponseSchema, status_code=status.HTTP_202_ACCEPTED)
def update_coffee(id: int, coffee: CoffeeSchema):
    updated_coffee = db.session.query(Coffee).get(id)
    updated_coffee.name = coffee.name
    updated_coffee.roast = coffee.roast
    updated_coffee.roaster_id = coffee.roaster_id
    db.session.commit()
    return updated_coffee


@app.delete("/coffees/{id}", status_code=status.HTTP_202_ACCEPTED)
def destroy_coffee(id: int):
    coffee = db.session.query(Coffee).get(id)
    db.session.delete(coffee)
    db.session.commit()
    return {"message": f"Coffee ID# {id} successfully deleted."}


@app.get("/coffees/{id}/roaster", response_model=RoasterResponseSchema, status_code=status.HTTP_200_OK)
def show_coffee_roaster(id: int):
    coffee = db.session.query(Coffee).get(id)
    return coffee.roaster


### Roaster Routes
### Roaster Routes
### Roaster Routes
@app.get("/roasters", response_model= list[RoasterResponseSchema], status_code=status.HTTP_200_OK)
def index_roasters():
    return db.session.query(Roaster).all()


@app.post("/roasters", response_model=RoasterResponseSchema, status_code=status.HTTP_201_CREATED)
def create_roaster(roaster: RoasterSchema):
    new_roaster = Roaster(name=roaster.name)
    db.session.add(new_roaster)
    db.session.commit()
    return new_roaster


@app.get("/roasters/{id}",response_model=RoasterResponseSchema, status_code=status.HTTP_200_OK)
def show_roaster(id: int):
    roaster = db.session.query(Roaster).get(id)
    if roaster:
        return roaster
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])


@app.put("/roasters/{id}", response_model=RoasterResponseSchema, status_code=status.HTTP_202_ACCEPTED)
def update_rosater(id: int, roaster: RoasterSchema):
    updated_roaster = db.session.query(Roaster).get(id)
    updated_roaster.name = roaster.name
    db.session.commit()
    return updated_roaster


@app.delete("/roasters/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_roater(id: int):
    roaster = db.session.query(Roaster).get(id)
    db.session.delete(roaster)
    db.session.commit()
    return {"message": f"Roaster ID# {id} successfully deleted"}


@app.get("/roasters/{id}/coffees", response_model=list[CoffeeResponseSchema],status_code=status.HTTP_200_OK)
def show_roaster_coffees(id: int):
    roaster = db.session.query(Roaster).get(id)
    return roaster.coffees


### User Routes
### User Routes
### User Routes

# @app.get("/users", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
# def index_users(user: UserSchema):
#     new_user

@app.post("/users", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

# # Run locally, outside of container from /.venv -> $ python main.py
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)