import os
import json
import requests
api_key = str('23053eab7f3040c49ef3b6ef02b083c4f5dd586099f238225179705eeb3e13c5')

params = {
    "api_key": api_key,
  "engine": "google_flights",
  "departure_id": "JFK",
  "arrival_id": "LAX",
  "currency": "EUR",
  "type": "2",
  "travel_class": "1",
  "adults": "1",
  "children": "1",
  "outbound_date": "2026-07-27",
  
  "deep_search": "false",
  "sort_by": "1",
  "stops": "1",
}
#"return_date": "2026-07-28",
# type:1 - Round trip (default), 2 - One way, 3 - Multi-city
# travel_class:1 - Economy (default), 2 - Premium Economy, 3 - Business, 4 - First
# sort_by: 1 - Top flights(default), 2 - Price, 3 - Departure time, 4 - Arrival Time, 5 - Duration, 6 - Emission

response = {}
try:

    search = requests.get("https://serpapi.com/search", params=params, timeout=30)
    search.raise_for_status()
    response = search.json()
    print(json.dumps(response, indent=3))

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
        for flight in item.get("flights", []):

            print("Total duration:", item.get("total_duration"))
            print("Price:", item.get("price"))

            departure = flight.get("departure_airport", {})
            arrival = flight.get("arrival_airport", {})

            print(departure.get("name"))
            print(departure.get("id"))
            print(departure.get("time"))
        

            print(arrival.get("name"))
            print(arrival.get("id"))
            print(arrival.get("time"))

            print(flight.get("airplane"))
            print(flight.get("airline"))
            print(flight.get("flight_number"))
        
        print()

# try:
#     for key in keys:
#         print("Key: " + key)
#         for item in response[key]:
#             for flight in item["flights"]:
#                 print(flight["departure_airport"]["name"], flight["departure_airport"]["id"], flight["departure_airport"]["time"])
#                 print(flight["arrival_airport"]["name"], flight["arrival_airport"]["id"], flight["arrival_airport"]["time"])
#                 print(flight["airplane"])
#                 print(flight["airline"])
#                 print(flight["flight_number"])
#             print("Total duration:" + str(item["total_duration"]))
#             print("Price:" + str(item["price"]))
#             print("")
# except KeyError:
#     price = None

