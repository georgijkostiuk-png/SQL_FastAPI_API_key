import os
import json
import requests
api_key = str('23053eab7f3040c49ef3b6ef02b083c4f5dd586099f238225179705eeb3e13c5')

params = {
    "api_key": api_key,
  "engine": "google_hotels",
  "q": "Brisbane",
  "gl": "US",
  "currency": "EUR",
  "check_in_date": "2026-07-20",
  "check_out_date": "2026-07-27",
  "adults": "2",
  "children": "2",
  "children_ages": "4,8",
  "sort_by": "13",
}
#"rating": "8",

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


keys = ["properties"]

for key in keys:
    print("Key:", key)

    for hotel in response.get(key, []):
        hotel_info = {
            "type": hotel.get("type"),
            "name": hotel.get("name"),
            "link": hotel.get("link"),
            "check_in_date": params.get("check_in_date"),      # from request params
            "check_out_date": params.get("check_out_date"),    # from request params
            "total_rate": hotel.get("total_rate", {}).get("extracted_lowest"),
            "hotel_class":hotel.get("extracted_hotel_class"),
            "overall_rating": hotel.get("overall_rating"),
            "location_rating": hotel.get("location_rating")
        }

    print(json.dumps(hotel_info, indent=4))

    # for i in key:

    #     print("Total duration:", item.get("total_duration"))
    #     print("Price:", item.get("price"))

    #     departure = flight.get("departure_airport", {})
    #     arrival = flight.get("arrival_airport", {})

    #     print(departure.get("name"))
    #     print(departure.get("id"))
    #     print(departure.get("time"))
    

    #     print(arrival.get("name"))
    #     print(arrival.get("id"))
    #     print(arrival.get("time"))

    #     print(flight.get("airplane"))
    #     print(flight.get("airline"))
    #     print(flight.get("flight_number"))
    
    # print()