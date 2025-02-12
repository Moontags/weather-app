from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY is not set. Check your .env file.")

def get_current_weather(city="Helsinki"):
   
    requests_url = f"http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}&units=metric"

    try:
        response = requests.get(requests_url)
        weather_data = response.json()

        print("API Response:", weather_data)

        if "cod" not in weather_data:
            return {"error": "Invalid API response format."}

        if int(weather_data["cod"]) == 404:
            return {"error": "City not found. Please try again."}

        if "main" not in weather_data or "weather" not in weather_data:
            return {"error": "Missing weather data in response."}

        return weather_data

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

if __name__ == "__main__":
    print('\n*** Get Current Weather ***\n')

    city = input("Enter city name: ").strip()

    if not city:
        city = "Helsinki"

    weather_data = get_current_weather(city)

    print('\nWeather Data:')
    pprint(weather_data)  
