from pydantic import BaseModel, Field
from datetime import date, datetime
from enum import Enum

#------------------------User------------------
class UserBase(BaseModel):
    username:str

class UserCreate(UserBase):
    password:str=Field(min_length=5, max_length=20) #TODO Welche Zeichen? -Pattern:regex

class UserRead(UserBase):
    id:int
    todos:list[TodoRead] = []

class UserLogin(BaseModel):
    username:str
    password:str

    #-------------------Todo--------------------
class TodoState(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TodoBase(BaseModel):
    home_city:str
    departure_id:str
    destination_city:str
    arrival_id:str
    vacation_start:date | None = None
    vacation_end:date | None = None
    #FIXME user_id

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id:int
    user_id:int | None = None

#-------------------Flight--------------------

class FlightBase(BaseModel):
    departure_airport:str
    departure_id:str
    departure_time:datetime | None = None
    arrival_airport:str
    arrival_id:str
    arrival_time:datetime | None = None
    airplane:str
    airline:str
    flight_number:str
    total_duration:int
    price:int
    #FIXME user_id

class FlightCreate(FlightBase):
    pass

class FlightRead(FlightBase):
    id:int
    todo_id:int

    #-------------------Hotel--------------------

class HotelBase(BaseModel):
    type:str
    name:str
    link:str
    check_in_date:str
    check_out_date:str
    hotel_class:int | None = None
    total_rate:int | None = None
    overall_rating:float
    location_rating:float
  
    #FIXME user_id

class HotelCreate(HotelBase):
    pass

class HotelRead(HotelBase):
    id:int
    todo_id:int


