from models import Todo, User, Flight, Hotel
from sqlalchemy.orm import Session
from sqlalchemy import text, select, delete
from util import hash_password, verify_password
import os
import json
import requests
from datetime import datetime

class TodoRepository:

    def __init__(self, session:Session):
        self.session=session

    # def save(self, user:User) -> User:
    #     self.session.add(user)
    #     self.session.commit()
    #     self.session.refresh(user) #Userobjekt aktualisieren
    #     return user
    
    def new_todo_by_user(self, user_id:int, todo:Todo) ->Todo:
        user = self.session.get(User, user_id)
        user.todos.append(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo
    def find_all_todos(self)->list[Todo]:
        todos = self.session.query(Todo).all()
        return todos
    
    def find_todo_by_user(self, user_id:int)->list[Todo]:
        return self.session.query(Todo).filter(Todo.user_id==user_id).all()
    
    def update_todo_state(self, todo_id:int, new_state:str)-> Todo | None:
        # TODO check new_state
        allowed = {"OPEN", "IN_PROGRESS", "DONE"}
        if new_state not in allowed:
            raise ValueError(f"Invalid State, allowed: {allowed}")

        todo = self.session.get(Todo, todo_id)
        if not todo:
            return None
        todo.state = new_state
        self.session.commit()
        self.session.refresh(todo)
        return todo
    
    def update_todo_departureid(self, id:int, departure_id:str)-> Todo | None:

        todo = self.session.get(Todo, id)
        if not todo:
            return None
        todo.departure_id = departure_id
        self.session.commit()
        self.session.refresh(todo)
        return todo
    
    def find_todos_by_task(self, user_id:int, task:str)->list[Todo]:
        return (
            self.session.query(Todo)
            .filter(
                Todo.user_id==user_id, 
                Todo.task.ilike(f"%{task}%")
            )
            .all()
        )
    
    def find_todos_by_user_by_state(self, user_id:int, state:str)->list[Todo]:
        return (
            self.session.query(Todo)
            .filter(
                Todo.user_id==user_id, 
                Todo.state.ilike(f"%{state}%")
            )
            .all()
            )
    
    def find_todo_by_todoid(self, id:int)->Todo:
        todo = self.session.get(Todo, id)
        if not todo:
            return None
        return todo
    
    def find_open_todos_by_user(self, user_id:int)->list[Todo]:
        return (
            self.session.query(Todo)
            .filter(
                Todo.user_id==user_id, 
                Todo.state== "OPEN"
            )
            .all()
        )

    def delete_todos_all(self)->list[Todo]:
        todo_list = self.session.query(Todo).all()
        for i in todo_list:
            self.session.delete(i)
            self.session.commit()
        return todo_list

    def delete_todos_by_id(self, id:int)->Todo | None:
        todo = self.session.get(Todo, id)
        # if not todo:
        #     return None
        if todo is None: # gleich als: if not todo:
            return None

        self.session.delete(todo)
        self.session.commit()
        return todo
    
    def delete_todos_by_state(self, state:str)->list[Todo]:
        todos_list = self.session.query(Todo).filter(Todo.state==state).all()
        for i in todos_list:
            self.session.delete(i)
            self.session.commit()
        return todos_list
    
    def delete_all_done_todos_by_user(self, user_id:int)->int:
        todos = (
            self.session.query(Todo)
            .filter(
                Todo.user_id == user_id,
                Todo.state == "DONE"
            )
            .all()
        )
        count = len(todos)
        for i in todos:
            self.session.delete(i)
        self.session.commit()
        return count
    

class UserRepository:

    def __init__(self, session:Session):
        self.session=session

    def create(self, user:User) -> User:
        existing = self.session.query(User).filter(User.username==user.username).first()
        if existing:
            raise ValueError("User existiert bereits!")

        user.password = hash_password(user.password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user) #Userobjekt aktualisieren
        return user
    
    # def delete_user(self, id:int)->User | None: #id or user_id works because we have relationship in models
    #     user =self.session.get(User, id)
    #     if user is not None:
    #         self.session.delete(user)
    #         self.session.commit()
    #     return user  
    
    def delete_user(self, user_id:int)->User | None: #id or user_id works because we have relationship in models
        user =self.session.get(User, user_id)
        if user is not None:
            self.session.delete(user)
            self.session.commit()
        return user 
    
    def find_all(self) -> list[User]:
        user = self.session.query(User).all()
        return user

    def find_user_by_id(self,id:int) -> User:
        user = self.session.query(User).filter(User.id==id).first()
        return user

    # def find_user_by_id(self,id:int) -> User:
    #     user = self.session.get(User, id)
    #     return user

    def create_user_with_password(self, user:User, plain_password:str) -> User:
        user.password = hash_password(plain_password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user) #Userobjekt aktualisieren
        return user


    def find_user_by_credentials(self, username:str, password:str)->User | None:   
        stored_user = self.session.query(User).filter(User.username==username).first()

        if stored_user is None:
            return None

        return stored_user
    

    def find_user_by_credentials_2(self, username:str, password:str)->User | None:   
        stored_user = self.session.query(User).filter(User.username==username).first()

        if stored_user is None:
            return None

        checkpw = verify_password(password, stored_user.password)
        return stored_user, checkpw
    
class FlightRepository:

    def __init__(self, session:Session):
        self.session=session

    
    def find_all_flights(self)->list[Flight]:
        flights = self.session.query(Flight).all()
        return flights
    
    def find_all_flights_by_departure_id(self, departure_id:str)->list[Flight]:
        flights = self.session.query(Flight).filter(Flight.departure_id==departure_id).all()
        return flights
    
    def delete_flights_by_id(self, id:int)->list[Flight] | None:
        flight = self.session.get(Flight, id)
        # if not todo:
        #     return None
        if flight is None: # gleich als: if not todo:
            return None

        self.session.delete(flight)
        self.session.commit()
        return flight
    
    def delete_flights_by_todoid(self, todo_id:int)->list[Flight] | None:
        flights = self.session.query(Flight).filter(Flight.todo_id==todo_id).all()
        # if not todo:
        #     return None
        for i in flights:
            if i is None: # gleich als: if not todo:
                return None

            self.session.delete(i)
            self.session.commit()
        return flights


    def new_flight_by_todoid_or_update(self, id:int) ->list[Flight]:
        todo = self.session.get(Todo, id)

        if todo is None:
            raise ValueError(f"Todo with id={id} not found")
        
        # Delete all existing flights for this todo
        self.session.execute(delete(Flight).where(Flight.todo_id == id))
        self.session.commit()

        api_key = str('23053eab7f3040c49ef3b6ef02b083c4f5dd586099f238225179705eeb3e13c5')
        # home_city = f'{todo.home_city}'
        departure_id = f'{todo.departure_id}'
        # destination_city = f'{todo.destination_city}'
        arrival_id = f'{todo.arrival_id}'
        vacation_start = f'{todo.vacation_start}'
        vacation_end = f'{todo.vacation_end}'
        

        params = {
        "api_key": api_key,
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": vacation_start,
        
        "currency": "EUR",
        "type": "2",
        "travel_class": "1",
        "adults": "2",
        "children": "2",
        "deep_search": "false",
        "sort_by": "1",
        "stops": "1",
        }
        #"return_date": vacation_end,

        # type:1 - Round trip (default), 2 - One way, 3 - Multi-city
        # travel_class:1 - Economy (default), 2 - Premium Economy, 3 - Business, 4 - First
        # sort_by: 1 - Top flights(default), 2 - Price, 3 - Departure time, 4 - Arrival Time, 5 - Duration, 6 - Emission
        # stops: 0 - any stops, 1 - no stops, 2- 1 stop or fewer, 3 - 2 stops of fewer 

        response = {}
        try:

            search = requests.get("https://serpapi.com/search", params=params, timeout=30)
            search.raise_for_status()
            response = search.json()
            #print(json.dumps(response, indent=3))

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401: # Invalid API key
                print(e.response.json().get("error")) # "Invalid API key. Your API key should be here: https://serpapi.com/manage-api-key"
            elif status_code == 400: # Missing required parameter
                pass
            elif status_code == 429: # Exceeds the hourly throughput limit OR account run out of searches
                pass
        except requests.exceptions.Timeout as e:
        # Handle timeout
            print(f"The request timed out: {e}")

        created_flights = []
        
        keys = ["best_flights", "other_flights"]

        for key in keys: # returns flights
            print("Key:", key)

            for item in response.get(key, []):

               

                for i in item.get("flights", []): # i == flight

                    total_duration = int(item.get("total_duration"))
                    price = int(item.get("price"))

                    departure = i.get("departure_airport", {})
                    arrival = i.get("arrival_airport", {})

                    departure_airport = str(departure.get("name"))
                    departure_id = str(departure.get("id"))
                    #departure_time = str(departure.get("time"))
                    departure_time = datetime.strptime(departure.get("time"),"%Y-%m-%d %H:%M")

                    arrival_airport = str(arrival.get("name"))
                    arrival_id = str(arrival.get("id"))
                    #arrival_time = str(arrival.get("time"))
                    arrival_time = datetime.strptime(arrival.get("time"),"%Y-%m-%d %H:%M")

                    airplane = str(i.get("airplane"))
                    airline = str(i.get("airline"))
                    flight_number = str(i.get("flight_number"))

            
                    flight = Flight(departure_airport=departure_airport,
                                            departure_id=departure_id, 
                                            departure_time=departure_time, 
                                            arrival_airport=arrival_airport, 
                                            arrival_id=arrival_id, 
                                            arrival_time=arrival_time, 
                                            airplane=airplane, 
                                            airline=airline, 
                                            flight_number=flight_number, 
                                            total_duration=total_duration, 
                                            price=price)
                
            
                    todo.flights.append(flight)
                    #self.session.add(flight)
                    created_flights.append(flight)

        self.session.commit()

        for flight in created_flights:
            self.session.refresh(flight)

        return created_flights
    

class HotelRepository:

    def __init__(self, session:Session):
        self.session=session

    def find_all_hotels(self)->list[Hotel]:
        hotels = self.session.query(Hotel).all()
        return hotels
    
    def delete_hotels_by_todoid(self, todo_id:int)->list[Hotel] | None:
        hotels = self.session.query(Hotel).filter(Hotel.todo_id==todo_id).all()
        # if not todo:
        #     return None
        for i in hotels:
            if i is None: # gleich als: if not todo:
                return None

            self.session.delete(i)
            self.session.commit()
        return hotels

    def hotel_by_todoid_or_update(self, id:int) ->list[Hotel]:
        todo = self.session.get(Todo, id)

        if todo is None:
            raise ValueError(f"Todo with id={id} not found")
        
        # Delete all existing flights for this todo
        self.session.execute(delete(Hotel).where(Hotel.todo_id == id))
        self.session.commit()

        api_key = str('23053eab7f3040c49ef3b6ef02b083c4f5dd586099f238225179705eeb3e13c5')
        #home_city = f'{todo.home_city}'
        #departure_id = f'{todo.departure_id}'
        destination_city = f'{todo.destination_city}'
        #arrival_id = f'{todo.arrival_id}'
        vacation_start = f'{todo.vacation_start}'
        vacation_end = f'{todo.vacation_end}'
        
        params = {
        "api_key": api_key,
        "engine": "google_hotels",
        "q": destination_city,
        "gl": "US",
        "currency": "EUR",
        "check_in_date": vacation_start,
        "check_out_date": vacation_end,
        "adults": "2",
        "children": "2",
        "children_ages": "4,8",
        "sort_by": "13",
        }

        #"return_date": vacation_end,

        # type:1 - Round trip (default), 2 - One way, 3 - Multi-city
        # travel_class:1 - Economy (default), 2 - Premium Economy, 3 - Business, 4 - First
        # sort_by: 1 - Top flights(default), 2 - Price, 3 - Departure time, 4 - Arrival Time, 5 - Duration, 6 - Emission
        # stops: 0 - any stops, 1 - no stops, 2- 1 stop or fewer, 3 - 2 stops of fewer 

        response = {}
        try:

            search = requests.get("https://serpapi.com/search", params=params, timeout=30)
            search.raise_for_status()
            response = search.json()
            #print(json.dumps(response, indent=3))

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401: # Invalid API key
                print(e.response.json().get("error")) # "Invalid API key. Your API key should be here: https://serpapi.com/manage-api-key"
            elif status_code == 400: # Missing required parameter
                pass
            elif status_code == 429: # Exceeds the hourly throughput limit OR account run out of searches
                pass
        except requests.exceptions.Timeout as e:
        # Handle timeout
            print(f"The request timed out: {e}")

        created_hotels = []
        
        keys = ["properties"]

        for key in keys:
            print("Key:", key)

            for i in response.get(key, []):

                hotel = Hotel(
                    type=str(i.get("type")),
                    name=str(i.get("name")),
                    link=str(i.get("link")),
                    check_in_date=str(i.get("check_in_date")),
                    check_out_date=str(i.get("check_out_date")),
                    hotel_class=i.get("extracted_hotel_class"),
                    total_rate=i.get("total_rate", {}).get("extracted_lowest"),
                    overall_rating=float(i.get("overall_rating")),
                    location_rating=float(i.get("location_rating"))
                )
              
                
            
                todo.hotels.append(hotel)
                #self.session.add(flight)
                created_hotels.append(hotel)

        self.session.commit()

        for flight in created_hotels:
            self.session.refresh(flight)

        return created_hotels