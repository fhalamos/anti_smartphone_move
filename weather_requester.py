import requests
import os

openweather_api_key = os.environ['OPENWEATHER_API_KEY']

def get_weather():

  units_dict = {'C':'metric','F':'imperial'} #metric for °C, imperial for °F

  weather_api_url_='https://api.openweathermap.org/data/2.5/weather?q=Chicago,usa&APPID='+openweather_api_key

  output=[]

  for unit_measure in units_dict:

    weather_api_url = weather_api_url_ +'&units='+units_dict[unit_measure]
    response = requests.get(weather_api_url)
  
    output.append(str(response.json()['main']['temp'])+'°'+unit_measure)

  return '\n'.join(output)


if __name__ == '__main__':
  print(get_weather())