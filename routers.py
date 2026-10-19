#RestService
from models import User, Todo, Flight
from database import get_db
from schema import *
from crud import UserRepository, TodoRepository, FlightRepository, HotelRepository
from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session


user_router = APIRouter(prefix="/users", tags=["User"])
todo_router = APIRouter(prefix="/todo", tags=["Todos"])
flights_router = APIRouter(prefix="/flights", tags=["Flights"])
hotels_router = APIRouter(prefix="/hotels", tags=["Hotels"])

@user_router.post("/", response_model=UserRead)
def create_user(user_create:UserCreate, db:Session = Depends(get_db)):
    repo = UserRepository(db)
    new_user = User(username = user_create.username,
                    password=user_create.password)
    return repo.create(new_user)

@todo_router.get("/todos5", response_model=list[TodoRead]) #http:/localhost:8000/users/1/todos. user_id = user table
def get_all_todos(db:Session=Depends(get_db)):
    repo = TodoRepository(db)
    return repo.find_all_todos()

#http://localhost:8000/todo?user_id=1
@todo_router.post("/", response_model=TodoRead) #oder user_id im Pfad "/{user_id}/"
def create_todo_by_userid(user_id:int, todo_create:TodoCreate, db:Session=Depends(get_db)):
    repo = TodoRepository(db)
    new_todo = Todo(**todo_create.model_dump())
    return repo.new_todo_by_user(user_id, new_todo)

@todo_router.post("/todos4", response_model=TodoRead) #oder user_id im Pfad "/{user_id}/"
def delete_todo_by_todoid(id:int, db:Session=Depends(get_db)):
    repo = TodoRepository(db)
    return repo.delete_todos_by_id(id)


@todo_router.get("/{user_id}/todos1", response_model=list[TodoRead]) #http:/localhost:8000/users/1/todos. user_id = user table
def get_all_todos_by_userid(user_id:int, db:Session=Depends(get_db)):
    repo = TodoRepository(db)
    return repo.find_todo_by_user(user_id)

@todo_router.get("/{id}/todos2", response_model=TodoRead) #http:/localhost:8000/users/1/todos. user_id = user table
def get_todo_by_todoid(id:int, db:Session=Depends(get_db)):
    repo = TodoRepository(db)
    return repo.find_todo_by_todoid(id)


@todo_router.get("/todos3", response_model=TodoRead) #http:/localhost:8000/users/1/todos. user_id = user table
def update_todo_by_departureid(id:int, departure_id:str, db:Session=Depends(get_db)):
    repo = TodoRepository(db)
    return repo.update_todo_departureid(id, departure_id)


@user_router.get("/", response_model=list[UserRead]) #http:/localhost:8000/users/
def get_all_users(db:Session = Depends(get_db)): # immer neu session haben wenn neu method aufrufen.
    repo = UserRepository(db)
    return repo.find_all()


# response_model: 1) connection to schema(pydantic validation). 2)should return same as function from crud.

@user_router.post("/authenticate", response_model=UserRead) #We want to return users data
def authenticate_user(user_login:UserLogin, db:Session=Depends(get_db)):
    repo = UserRepository(db)
    user = repo.find_user_by_credentials(user_login.username, user_login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Username or Password")
    return user

@flights_router.get("/flights", response_model=list[FlightRead]) #http:/localhost:8000/users/
def get_all_flights(db:Session = Depends(get_db)): # immer neu session haben wenn neu method aufrufen.
    repo = FlightRepository(db)
    return repo.find_all_flights()

@flights_router.get("/flights2", response_model=list[FlightRead]) #http:/localhost:8000/users/
def get_all_flights_by_departure_id(departure_id:str, db:Session = Depends(get_db)): # immer neu session haben wenn neu method aufrufen.
    repo = FlightRepository(db)
    return repo.find_all_flights_by_departure_id(departure_id)

@flights_router.post("/{id}/flights2", response_model=list[FlightRead]) #oder user_id im Pfad "/{user_id}/"
def create_flight_by_todoid_or_update(id:int, db:Session=Depends(get_db)):
    repo = FlightRepository(db)
    return repo.new_flight_by_todoid_or_update(id)

@flights_router.post("/flights3", response_model=list[FlightRead]) #oder user_id im Pfad "/{user_id}/"
def delete_flight_by_todoid(todo_id:int, db:Session=Depends(get_db)):
    repo = FlightRepository(db)
    return repo.delete_flights_by_todoid(todo_id)

@hotels_router.post("/hotels", response_model=list[HotelRead]) #oder user_id im Pfad "/{user_id}/"
def create_hotel_by_todoid_or_update(id:int, db:Session=Depends(get_db)):
    repo = HotelRepository(db)
    return repo.hotel_by_todoid_or_update(id)

@hotels_router.get("/hotels2", response_model=list[HotelRead]) #http:/localhost:8000/users/
def get_all_hotels(db:Session = Depends(get_db)): # immer neu session haben wenn neu method aufrufen.
    repo = HotelRepository(db)
    return repo.find_all_hotels()

@hotels_router.post("/hotels3", response_model=list[HotelRead]) #oder user_id im Pfad "/{user_id}/"
def delete_hotel_by_todoid(todo_id:int, db:Session=Depends(get_db)):
    repo = HotelRepository(db)
    return repo.delete_hotels_by_todoid(todo_id)
