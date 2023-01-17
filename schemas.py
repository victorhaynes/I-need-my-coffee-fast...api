from pydantic import BaseModel, validator
from fastapi import HTTPException


class Coffee(BaseModel):
    name: str
    roast: str
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
            raise HTTPException(status_code=400,detail=[{"msg": f"Error: {cls.__name__} name '{name}' must be at least {minimum} characters."}])
        return name


class Roaster(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def validate_roaster_name(cls, name):
        minimum = 3
        if len(name) < minimum:
            raise HTTPException(status_code=400,detail=[{"msg": f"Error: {cls.__name__} name '{name}' must be at least {minimum} characters."}])
        return name


class User(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True

