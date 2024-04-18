from service.accuweather import AccuWeatherService
from dotenv import load_dotenv

load_dotenv()
CITY_ID = '60449'

print(AccuWeatherService.get_daily_forecasts(city_id=CITY_ID))