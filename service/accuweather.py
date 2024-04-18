import requests
import os 
from typing import List
from datetime import datetime


class AccuWeatherService:
    @staticmethod
    def proccess_days(next_five_days: List): 
        """
        "forecasts": [
            {
            "date": "2022-03-24",
            "clothes": ["Coat", "Winter jacket"]
            },
            {
            "date": "2022-03-25",
            "clothes": ["Rain Coat"]
            }
        ]
        """
        forecasts = []
        for day in next_five_days:
            data = dict()
            temperature_maximum = day['Temperature']['Maximum']['Value']
            day_rain_probability = day['Day']['RainProbability']
            night_rain_probability = day['Night']['RainProbability']

            day_snow_probability = day['Day']['SnowProbability']
            night_snow_probability = day['Night']['SnowProbability']
            
            day_ice_probability = day['Day']['SnowProbability']
            night_ice_probability = day['Night']['SnowProbability']

            data['date'] = datetime.strptime(day['Date'], '%Y-%m-%dT%H:%M:%S%z')
            
            if temperature_maximum < 45:
                data['clothes'] = ['Coat', 'Winter Jacket']
                
            if temperature_maximum >= 45 and temperature_maximum <= 79:
                data['clothes'] = ['Fleece', 'Short Sleeves']
    
            if temperature_maximum >= 80:
                data['clothes'] = ['Shorts']

            if (day_rain_probability or night_rain_probability) > 50:
                data['clothes'].append('Rain Coat')
            
            if (day_snow_probability or night_snow_probability) > 50:
                data['clothes'].append('Snow Outfit')
            
            if (day_ice_probability or night_ice_probability) > 50:
                data['clothes'].append('Rain Coat')

            forecasts.append(data)

        return forecasts

    @staticmethod
    def get_daily_forecasts(city_id: str):
        API_URL = os.getenv('API_URL')
        API_KEY = os.getenv('API_KEY')

        endpoint = f'{API_URL}{city_id}?apikey={API_KEY}&details=true'
        
        print(endpoint)
        response = requests.get(
            endpoint
        )

        next_five_days = AccuWeatherService.proccess_days(
            next_five_days=response.json()['DailyForecasts'][:5]
        )

        return next_five_days