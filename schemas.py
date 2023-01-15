from pydantic import BaseModel

class Coffee(BaseModel):
    name: str
    roast: str
    roaster_id: int

    class Config:
        orm_mode = True


class Roaster(BaseModel):
    name: str

    class Config:
        orm_mode = True
