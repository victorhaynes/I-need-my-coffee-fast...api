# ~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import uvicorn
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

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
from schemas import LoginDetails

from seeds import seed_coffees, seed_roasters, seed_users

from pydantic import BaseModel

# ~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# ~~~ Auth Setup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Auth Setup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Auth Setup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Settings(BaseModel):
    authjwt_secret_key: str = os.environ["JWT_SECRET_KEY"]

@AuthJWT.load_config
def get_config():
    return Settings()

def logged_in(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=[{"msg": "Invalid authorization token."}])

    user_and_id = Authorize.get_jwt_subject().split(",")
    return user_and_id

# ~~~ Example Usage ~~~~~~~~~
# ~~~ Example Usage ~~~~~~~~~
# ~~~ Example Usage ~~~~~~~~~
# @app.get("/coffees", response_model=list[CoffeeResponseSchema], status_code=status.HTTP_200_OK,)
# def index_coffees(Authorize: AuthJWT=Depends()):
#     if logged_in(Authorize):
#         return db.session.query(Coffee).all()


# ~~~ Database Management ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Database Management ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Database Management ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.get("/seed", status_code=status.HTTP_201_CREATED)
def seed_database():
    seed_roasters()
    seed_coffees()
    seed_users()
    return {"message": "Seeded database with Roasters, Coffees, Users successfully."}


@app.delete("/delete", status_code=status.HTTP_202_ACCEPTED)
def delete_all_records():
    db.session.query(Coffee).delete()
    db.session.commit()
    db.session.query(Roaster).delete()
    db.session.commit()
    db.session.query(User).delete()
    db.session.commit()
    return {"message": "Deleted existing Coffee, Roaster, User records."}


# ~~~ Routes / Endpoints ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Routes / Endpoints ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Routes / Endpoints ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.get("/")
async def root():
    return {"message": "You are live--on a FastAPI application created by Victor Haynes. Navigate to /docs in browser to discover API."}


### Coffee Routes
### Coffee Routes
### Coffee Routes
@app.get("/coffees", response_model=list[CoffeeResponseSchema], status_code=status.HTTP_200_OK,)
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
    if coffee:
        return coffee.roaster
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])


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
    if roaster:
        return roaster.coffee
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])

### User Routes
### User Routes
### User Routes
@app.get("/users", response_model=list[UserResponseSchema], status_code=status.HTTP_200_OK)
def index_users():
    return db.session.query(User).all()

@app.post("/users", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

@app.get("/users/{id}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def show_user(id: int):
    user = db.session.query(User).get(id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])

### Auth Routes
### Auth Routes
### Auth Routes
@app.post("/login")
def login(user: LoginDetails, Authorize: AuthJWT=Depends(), status_code=status.HTTP_201_CREATED):
    user = db.session.query(User).filter_by(username=user.username).filter_by(password=user.password).first()
    if user:
        access_token = Authorize.create_access_token(subject=f"{user.username},{user.id}")
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=422,detail=[{"msg": "Invalid username or password."}])



# # Run locally, outside of container from venv -> (venv) $ python main.py
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)