from models import Todo, User, Flight
from sqlalchemy.orm import Session
from sqlalchemy import text, select
from util import hash_password, verify_password
import os
import json
import requests


    
class FlightRepository:

    def __init__(self, session:Session):
        self.session=session

    def new_flight_by_todoid_by_userid(self, id:int)-> Todo:#, user_id:int) ->Flight:
        
        todos = self.session.query(Todo).filter( Todo.id==id).all()
        todo = todos[0]
        if todo is None:
            raise ValueError(f"Todo with id={id} not found")
        print(todos)

        api_key = str('23053eab7f3040c49ef3b6ef02b083c4f5dd586099f238225179705eeb3e13c5')
        home_city = f'{todo.home_city}'
        departure_id = f'{todo.departure_id}'
        destination_city = f'{todo.home_city}'
        arrival_id = f'{todo.arrival_id}'
        vacation_start = f'{todo.vacation_start}'
        vacation_end = f'{todo.vacation_end}'
        

        params = {
        "api_key": api_key,
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": vacation_start,
        "return_date": vacation_end,
        "currency": "EUR",
        "type": "1",
        "travel_class": "1",
        "adults": "1",
        "children": "1",
        "deep_search": "false",
        "sort_by": "1",
        }

        # type:1 - Round trip (default), 2 - One way, 3 - Multi-city
        # travel_class:1 - Economy (default), 2 - Premium Economy, 3 - Business, 4 - First
        # sort_by: 1 - Top flights(default), 2 - Price, 3 - Departure time, 4 - Arrival Time, 5 - Duration, 6 - Emission

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
                    departure_time = str(departure.get("time"))

                    arrival_airport = str(arrival.get("name"))
                    arrival_id = str(arrival.get("id"))
                    arrival_time = str(arrival.get("time"))

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
                    self.session.commit()
                    self.session.refresh(flight)
        return todo
    
  
  
  
def __init__(self, session:Session):
    self.session=session  
repo = FlightRepository(Session)
todo = repo.new_flight_by_todoid_by_userid(1)

  


