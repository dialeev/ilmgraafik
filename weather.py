import requests
from datetime import datetime

LATITUDE = 59.1336
LONGITUDE = 25.5656
MET_NO_API_URL = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={LATITUDE}&lon={LONGITUDE}"

headers = {
    'User-Agent': 'WeatherApp/1.0 (mario.veelaid@gmail.com)'
}

def get_weather_data():
    response = requests.get(MET_NO_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_todays_weather_string(data):
    timeseries = data.get("properties", {}).get("timeseries", [])
    
    if not timeseries:
        return "No weather data available."
    
    current_time = datetime.utcnow()
    today_weather = None
    
    for forecast in timeseries:
        forecast_time = forecast.get("time")
        forecast_datetime = datetime.fromisoformat(forecast_time[:-1])
        
        if forecast_datetime.date() == current_time.date():
            today_weather = forecast.get("data", {}).get("instant", {}).get("details", {})
            break
    
    if today_weather:
        temperature = today_weather.get("air_temperature", "N/A")
        wind_speed = today_weather.get("wind_speed", "N/A")
        wind_direction = today_weather.get("wind_from_direction", "N/A")
        
        weather_info = (
            f"Tänane ilm Ardu, Eestis:\n"
            f"Temperatuur: {temperature}°C\n"
            f"Tuule kiirus: {wind_speed} m/s\n"
            f"Tuule suund: {wind_direction}°\n"
            f"Viimane uuendus: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return weather_info
    else:
        return "No forecast available for today."

def main():
    weather_data = get_weather_data()
    
    if weather_data:
        weather_string = get_todays_weather_string(weather_data)
        print(weather_string)

if __name__ == "__main__":
    main()
