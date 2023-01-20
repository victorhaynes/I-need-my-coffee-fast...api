from pydantic import BaseModel, validator
from typing import Optional, List, Dict
from pydantic_computed import Computed, computed
from fastapi import HTTPException
from datetime import datetime

# ~~~ Schemas for INBOUND processing ~~~~~~~
# ~~~ Schemas for INBOUND processing ~~~~~~~
# ~~~ Schemas for INBOUND processing ~~~~~~~
class Coffee(BaseModel):
    id: Optional[int]
    name: str
    roast: str
    image_url: str
    roaster_id: int
    
    class Config:
        orm_mode = True

    @validator("roast")
    def validate_roast_level(cls, roast):
        if roast.strip().capitalize() not in ("Light", "Medium", "Dark"):
            raise HTTPException(status_code=400,detail=[{"msg": f"Error: {cls.__name__} roast cannot be '{roast}'. Must be 'Light', 'Medium', or 'Dark'."}])
        return roast.strip().capitalize()

    @validator("name")
    def validate_coffee_name(cls, name):
        minimum = 3
        if len(name) < minimum:
            raise HTTPException(status_code=422,detail=[{"msg": f"Error: {cls.__name__} name '{name}' must be at least {minimum} characters."}])
        return name




class Roaster(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def validate_roaster_name(cls, name):
        minimum = 3
        if len(name) < minimum:
            raise HTTPException(status_code=422,detail=[{"msg": f"Error: {cls.__name__} name '{name}' must be at least {minimum} characters."}])
        return name


class User(BaseModel):
    username: str
    email: str
    password: str


    class Config:
        orm_mode = True


class LoginDetails(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

# ~~~ Schemas for OUTBOUND processing ~~~~~~~
# ~~~ Schemas for OUTBOUND processing ~~~~~~~
# ~~~ Schemas for OUTBOUND processing ~~~~~~~
class CoffeeResponse(BaseModel):
    id: int
    name: str
    roast: str
    image_url: str
    roaster_id: int
    roaster: Roaster
    time_created: datetime
    time_updated: Optional[datetime]

    class Config:
        orm_mode = True


class RoasterResponse(BaseModel):
    id: int
    name: str
    coffees: List[Coffee]
    time_created: datetime
    time_updated: Optional[datetime]

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    username: str
    greeting: Computed[str]
    time_created: datetime
    time_updated: Optional[datetime]

    @computed('greeting')
    def write_greeting(username: str, **kwargs):
        return f"Welcome back {username}"

    class Config:
        orm_mode = True


class AuthenticatedUserResponse(BaseModel):
    id: int
    username: str
    access_token: str
    time_created: datetime
    time_updated: Optional[datetime]
