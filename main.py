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

from schemas import Coffee as SchemaCoffee
from schemas import Roaster as SchemaRoaster
from schemas import User as SchemaUser


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
    return {"message": "You are live--on a FastAPI application created by Victor Haynes. Navigate to /docs in browser to discover API."}

### Coffee Routes
### Coffee Routes
### Coffee Routes
@app.get("/coffees", status_code=status.HTTP_200_OK)
def index_coffees():
    return db.session.query(Coffee).all()


@app.post("/coffees", response_model=SchemaCoffee, status_code=status.HTTP_201_CREATED)
def create_coffee(coffee: SchemaCoffee):
    new_coffee = Coffee(name=coffee.name, roast=coffee.roast, roaster_id=coffee.roaster_id)
    db.session.add(new_coffee)
    db.session.commit()
    return new_coffee


@app.get("/coffees/{id}", status_code=status.HTTP_200_OK)
def show_coffee(id: int):
    coffee = db.session.query(Coffee).get(id)
    if coffee:
        return coffee
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])
    

@app.put("/coffees/{id}", response_model=SchemaCoffee, status_code=status.HTTP_202_ACCEPTED)
def update_coffee(id: int, coffee: SchemaCoffee):
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
    new_roaster = Roaster(name=roaster.name)
    db.session.add(new_roaster)
    db.session.commit()
    return new_roaster


@app.get("/roasters/{id}", status_code=status.HTTP_200_OK)
def show_roaster(id: int):
    roaster = db.session.query(Roaster).get(id)
    if roaster:
        return roaster
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])


@app.put("/roasters/{id}", response_model=SchemaRoaster, status_code=status.HTTP_202_ACCEPTED)
def update_rosater(id: int, roaster: SchemaRoaster):
    updated_roaster = db.session.query(Roaster).get(id)
    updated_roaster.name = roaster.name
    db.session.commit(updated_roaster)
    return updated_roaster


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


### User Routes
### User Routes
### User Routes

@app.post("/users", response_model=SchemaUser, status_code=status.HTTP_201_CREATED)
def create_user(user: SchemaUser):
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

# Run locally, outside of container from /.venv -> $ python main.py
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)