# ~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import uvicorn
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
import json
from fastapi.encoders import jsonable_encoder
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
from schemas import AuthenticatedUserResponse

from seeds import seed_coffees, seed_roasters, seed_users

from pydantic import BaseModel


# ~~~ Config & Auth Setup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Config & Auth Setup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Config & Auth Setup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

### JWT Config
### JWT Config
### JWT Config
class Settings(BaseModel):
    authjwt_secret_key: str = os.environ["JWT_SECRET_KEY"]
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = True
    # authjwt_cookie_samesite: str = 'none'

    authjwt_cookie_samesite: str = 'lax'


@AuthJWT.load_config
def get_config():
    return Settings()

def jwt_owner(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=[{"msg": "Invalid authorization token."}])
    # fastapi_jwt_auth.exceptions.CSRFError
    current_user = Authorize.get_jwt_subject()
    return json.loads(current_user)

def is_admin(current_user: dict) -> bool:
    try:
        if current_user["username"] == "admin":
            return True
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=[{"msg": "Not an admin."}])

    except KeyError:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=[{"msg": "Authorization failed. Please login again."}])


# ~~~ Routes / Endpoints ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Routes / Endpoints ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Routes / Endpoints ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Root
### Root
### Root
@app.get("/")
async def root():
    return {"message": "You are live--on a FastAPI application created by Victor Haynes. Navigate to /docs in browser to discover API."}


### Coffee Routes
### Coffee Routes
### Coffee Routes
@app.get("/coffees", response_model=list[CoffeeResponseSchema], status_code=status.HTTP_200_OK,)
def index_coffees():
    return db.session.query(Coffee).order_by(Coffee.id.asc()).all()


@app.post("/coffees", response_model=CoffeeResponseSchema, status_code=status.HTTP_201_CREATED)
def create_coffee(coffee: CoffeeSchema, Authorize: AuthJWT=Depends()):
    jwt_owner(Authorize)
    new_coffee = Coffee(name=coffee.name, roast=coffee.roast, image_url= coffee.image_url, roaster_id=coffee.roaster_id)
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
def update_coffee(id: int, coffee: CoffeeSchema, Authorize: AuthJWT=Depends()):
    jwt_owner(Authorize)
    updated_coffee = db.session.query(Coffee).get(id)
    updated_coffee.name = coffee.name
    updated_coffee.roast = coffee.roast
    updated_coffee.image_url = coffee.image_url
    updated_coffee.roaster_id = coffee.roaster_id
    db.session.commit()
    return updated_coffee


@app.delete("/coffees/{id}", status_code=status.HTTP_202_ACCEPTED)
def destroy_coffee(id: int, Authorize: AuthJWT=Depends()):
    if is_admin(jwt_owner(Authorize)):
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
def index_users(Authorize: AuthJWT=Depends()):
    if is_admin(jwt_owner(Authorize)):
        return db.session.query(User).all()


@app.post("/users", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


@app.get("/users/{id}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def show_user(id: int, Authorize: AuthJWT=Depends()):
    user = db.session.query(User).get(id)
    if user and jwt_owner(Authorize)["username"]=="admin":
        return user
    elif user and jwt_owner(Authorize)["id"]==id:
        return user
    elif user:
        raise HTTPException(status_code=404,detail=[{"msg": "Not authorized to view other accounts."}])
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])


@app.put("/users/{id}", response_model=UserResponseSchema, status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, user: UserSchema, Authorize: AuthJWT=Depends()):
    updated_user = db.session.query(User).get(id)
    if updated_user and updated_user.username =="admin":
        raise HTTPException(status_code=401,detail=[{"msg": "Not authorized to alter Admin account."}])
    elif user.username =="admin":
        raise HTTPException(status_code=401,detail=[{"msg": "Cannot give self 'admin' username."}])
    elif updated_user and jwt_owner(Authorize)["id"]==id:
        updated_user.username = user.username
        updated_user.email = user.email
        updated_user.password = user.password
        db.session.commit()
        return updated_user
    elif updated_user and jwt_owner(Authorize)["username"]=="admin":
        updated_user.username = user.username
        updated_user.email = user.email
        updated_user.password = user.password
        db.session.commit()
        return updated_user
    else:
        raise HTTPException(status_code=401,detail=[{"msg": "Not authorized to edit other account."}])


@app.delete("/users/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_user(id: int, Authorize: AuthJWT=Depends()):
    user_to_delete = db.session.query(User).get(id)
    if user_to_delete and is_admin(jwt_owner(Authorize)) and not user_to_delete.username == "admin":
        db.session.delete(user_to_delete)
        db.session.commit()
        return {"message": f"User ID# {id} successfully deleted"}
    elif user_to_delete and user_to_delete.username == "admin":
        raise HTTPException(status_code=401,detail=[{"msg": "Not authorized to delete admin accounts. Contact DB Admin."}])
    else:
        raise HTTPException(status_code=404,detail=[{"msg": "Item not found"}])


# ~~~ Database Management ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Database Management ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Database Management ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.get("/initialize", status_code=status.HTTP_200_OK)
def initialize():
    if db.session.query(User).filter_by(username=os.environ["FASTAPI_ADMIN_USERNAME"]).first():
        raise HTTPException(status_code=400, detail=[{"msg": "Already Initialized."}])
    else:
        admin = User(username=os.environ["FASTAPI_ADMIN_USERNAME"], email=os.environ["FASTAPI_ADMIN_EMAIL"], password=os.environ["FASTAPI_ADMIN_PASSWORD"])
        db.session.add(admin)
        db.session.commit()
        return {"message": "Initialization successful."}


@app.get("/seed-all", status_code=status.HTTP_201_CREATED)
def seed_database(Authorize: AuthJWT=Depends()):
    if is_admin(jwt_owner(Authorize)):
        seed_roasters()
        seed_coffees()
        seed_users()
        return {"message": "All seeds ran successfully."}


@app.get("/seed-roasters", status_code=status.HTTP_201_CREATED)
def populate_roasters(Authorize: AuthJWT=Depends()):
    if is_admin(jwt_owner(Authorize)):
        seed_roasters()
        return {"message": "Seeded database with Roasters successfully."}


@app.get("/seed-coffees", status_code=status.HTTP_201_CREATED)
def populate_coffees(Authorize: AuthJWT=Depends()):
    if is_admin(jwt_owner(Authorize)):
        seed_coffees()
        return {"message": "Seeded database with Coffees successfully."}


@app.get("/seed-users", status_code=status.HTTP_201_CREATED)
def populate_users(Authorize: AuthJWT=Depends()):
    if is_admin(jwt_owner(Authorize)):
        seed_users()
        return {"message": "Seeded database with Users successfully."}


@app.get("/delete-all", status_code=status.HTTP_202_ACCEPTED)
def delete_all_records(Authorize: AuthJWT=Depends()):
    if is_admin(jwt_owner(Authorize)):
        db.session.query(Coffee).delete()
        db.session.commit()
        db.session.query(Roaster).delete()
        db.session.commit()
        db.session.query(User).delete()
        db.session.commit()
        return {"message": "Deleted all database records--or no records were found."}


# ~~~ Login ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Login ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Login ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.post("/login")
def login(user: LoginDetails,Authorize: AuthJWT=Depends(), status_code=status.HTTP_201_CREATED):
    user = db.session.query(User).filter_by(username=user.username).filter_by(password=user.password).first()
    if user:
        access_token = Authorize.create_access_token(subject=json.dumps(jsonable_encoder(user)))
        refresh_token = Authorize.create_refresh_token(subject=json.dumps(jsonable_encoder(user)))

        Authorize.set_access_cookies(access_token)
        Authorize.set_refresh_cookies(refresh_token)
        
        return user

    else:
        raise HTTPException(status_code=401,detail=[{"msg": "Invalid username or password."}])


@app.get("/me")
def who_am_i(Authorize: AuthJWT=Depends()):
    return {**jwt_owner(Authorize), "csrf": Authorize.get_raw_jwt()["csrf"]}


@app.get("/test", response_model=list[UserResponseSchema], status_code=status.HTTP_200_OK)
def index_users_test():
    return db.session.query(User).all()


# @app.post("/refresh")
# def create_new_token(Authorize: AuthJWT=Depends()):
#     # try:
#     #     Authorize.jwt_refresh_token_required()
#     # except Exception:
#     #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=[{"msg": "Invalid refresh token."}])
#     Authorize.jwt_refresh_token_required()

#     current_user = Authorize.get_jwt_subject()
#     new_access_token = Authorize.create_access_token(subject=current_user)
#     Authorize.set_access_cookies(new_access_token)

#     return {"msg": "Token successfully refreshed."}


@app.get('/refreshed')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}

@app.delete("/logout")
def logout(Authorize: AuthJWT=Depends()):
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logged out."}


@app.get("/fresh-login")
def create_freshness_token(user: LoginDetails, Authorize: AuthJWT=Depends()):
    jwt_owner(Authorize)
    user = db.session.query(User).filter_by(username=user.username).filter_by(password=user.password).first()
    if user:
        freshness_token = Authorize.create_access_token(subject=json.dumps(jsonable_encoder(user)), fresh=True)
        return {"msg": "Successfully issued freshness token."}
    else:
        raise HTTPException(status_code=401,detail=[{"msg": "Invalid username or password."}])


# ~~~~~~~~~~~~ fresh test ~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~ fresh test ~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~ fresh test ~~~~~~~~~~~~~~~~~~~~~~
@app.get("/fresh-route")
def test_fresh(Authorize: AuthJWT=Depends()):
    jwt_owner(Authorize)
    try:
        Authorize.fresh_jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=[{"msg": "Invalid freshness token."}])

    current_user = Authorize.get_jwt_subject()
    return json.loads(current_user)


# ~~~ Database Management ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Database Management ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Database Management ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.get("/seed-all", status_code=status.HTTP_201_CREATED)
def seed_database():
    seed_roasters()
    seed_coffees()
    seed_users()
    return {"message": "All seeds ran successfully.."}


@app.get("/seed-roasters", status_code=status.HTTP_201_CREATED)
def populate_roasters():
    seed_roasters()
    return {"message": "Seeded database with Roasters successfully."}


@app.get("/seed-coffees", status_code=status.HTTP_201_CREATED)
def populate_coffees():
    seed_coffees()
    return {"message": "Seeded database with Coffees successfully."}


@app.get("/seed-users", status_code=status.HTTP_201_CREATED)
def populate_users():
    seed_users()
    return {"message": "Seeded database with Users successfully."}


@app.delete("/delete-all", status_code=status.HTTP_202_ACCEPTED)
def delete_all_records():
    db.session.query(Coffee).delete()
    db.session.commit()
    db.session.query(Roaster).delete()
    db.session.commit()
    db.session.query(User).delete()
    db.session.commit()
    return {"message": "Deleted all database records--or no records were found."}


# # Run locally, outside of container from venv -> (venv) $ python main.py
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)