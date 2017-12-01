import urllib.request
import json

#this file is for scraping weather data fromi Weather Underground
def weatherBasic( city, state, weather, hours ):
    #Get Page WEATHER UNDERGROUND KEY = d1fec7897078849e
    url = 'http://api.wunderground.com/api/d1fec7897078849e/conditions/q/' + state + '/' + city + '.json'
    page = urllib.request.urlopen(url)

    #Convert page into JSON Readable (documented response found here: https://www.wunderground.com/weather/api/d/docs?d=index)
    json_str = page.read().decode('utf8')
    parsed_json = json.loads(json_str)

    #Get Info
    weather['location'] = parsed_json['current_observation']['display_location']['full']
    weather['current_temp'] = parsed_json['current_observation']['temp_f']
    weather['current_realfeel'] = parsed_json['current_observation']['feelslike_f']
    weather['icon_to_use'] = parsed_json['current_observation']['icon']

    #Convert icon to use to the few icons I have
    if (weather['icon_to_use'] == 'chanceflurries' or weather['icon_to_use'] == 'chancesnow' or weather['icon_to_use'] == 'flurries' or weather['icon_to_use'] == 'snow'):
        weather['icon_to_use'] = 'snow'
    elif (weather['icon_to_use'] == 'chancerain' or weather['icon_to_use'] == 'rain'):
        weather['icon_to_use'] = 'rain'
    elif (weather['icon_to_use'] == 'sleet' or weather['icon_to_use'] == 'chancesleet'):
        weather['icon_to_use'] = 'sleet'
    elif (weather['icon_to_use'] == 'chancetstorms' or weather['icon_to_use'] == 'tstorms'):
        weather['icon_to_use'] = 'thunderstorm'
    elif (weather['icon_to_use'] == 'sunny' or weather['icon_to_use'] == 'clear'):
        if (hours >= 6 and hours <= 18):
            weather['icon_to_use'] = 'clear'
        else:
            weather['icon_to_use'] = 'night'
    elif (weather['icon_to_use'] == 'cloudy' or weather['icon_to_use'] == 'mostlycloudy' or weather['icon_to_use'] == 'partlysunny'):
        weather['icon_to_use'] = 'cloudy'
    elif (weather['icon_to_use'] == 'fog' or weather['icon_to_use'] == 'hazy'):
        weather['icon_to_use'] = 'fog'
    else:
        if (hours >= 6 and hours <= 18):
            weather['icon_to_use'] = 'partlycloudy'
        else:
            weather['icon_to_use'] = 'nt_partlycloudy'

    page.close()

    return

def weatherHourly( city, state, weather, hours):
    #Get Page WEATHER UNDERGROUND KEY = d1fec7897078849e
    url = 'http://api.wunderground.com/api/d1fec7897078849e/hourly/q/' + state + '/' + city + '.json'
    page = urllib.request.urlopen(url)

    #Convert page into JSON Readable (documented response found here: https://www.wunderground.com/weather/api/d/docs?d=index)
    json_str = page.read().decode('utf8')
    parsed_json = json.loads(json_str)

    #Set up weather variable for hours
    weather['hourly'] = {}

    #go on and get each hour
    for hour in range (0, len(parsed_json['hourly_forecast']) - 1):
        weather['hourly'][hour] = {}
        weather['hourly'][hour]['time'] =  parsed_json['hourly_forecast'][hour]['FCTTIME']['civil']
        weather['hourly'][hour]['icon_to_use'] = parsed_json['hourly_forecast'][hour]['icon']
        weather['hourly'][hour]['temperature'] = parsed_json['hourly_forecast'][hour]['temp']['english']
        weather['hourly'][hour]['real_feel'] = parsed_json['hourly_forecast'][hour]['temp']['english']
        weather['hourly'][hour]['chance_rain'] = parsed_json['hourly_forecast'][hour]['pop']

        #Convert icon to use to the few icons I have
        if (weather['hourly'][hour]['icon_to_use'] == 'chanceflurries' or weather['hourly'][hour]['icon_to_use']  == 'chancesnow' or weather['hourly'][hour]['icon_to_use']  == 'flurries' or weather['hourly'][hour]['icon_to_use']  == 'snow'):
            weather['hourly'][hour]['icon_to_use']  = 'snow'
        elif (weather['hourly'][hour]['icon_to_use']  == 'chancerain' or weather['hourly'][hour]['icon_to_use']  == 'rain'):
            weather['hourly'][hour]['icon_to_use'] = 'rain'
        elif (weather['hourly'][hour]['icon_to_use']  == 'sleet' or weather['hourly'][hour]['icon_to_use']  == 'chancesleet'):
            weather['hourly'][hour]['icon_to_use']  = 'sleet'
        elif (weather['hourly'][hour]['icon_to_use']  == 'chancetstorms' or weather['hourly'][hour]['icon_to_use']  == 'tstorms'):
            weather['hourly'][hour]['icon_to_use']  = 'thunderstorm'
        elif (weather['hourly'][hour]['icon_to_use'] == 'sunny' or weather['hourly'][hour]['icon_to_use']  == 'clear'):
            if (hours >= 6 and hours <= 18):
                weather['hourly'][hour]['icon_to_use']  = 'clear'
            else:
                weather['hourly'][hour]['icon_to_use']  = 'night'
        elif (weather['hourly'][hour]['icon_to_use']  == 'cloudy' or weather['hourly'][hour]['icon_to_use']  == 'mostlycloudy' or weather['hourly'][hour]['icon_to_use']  == 'partlysunny'):
            weather['hourly'][hour]['icon_to_use']  = 'cloudy'
        elif (weather['hourly'][hour]['icon_to_use']  == 'fog' or weather['hourly'][hour]['icon_to_use'] == 'hazy'):
            weather['hourly'][hour]['icon_to_use']   = 'fog'
        else:
            if (hours >= 6 and hours <= 18):
                weather['hourly'][hour]['icon_to_use']  = 'partlycloudy'
            else:
                weather['hourly'][hour]['icon_to_use']  = 'nt_partlycloudy'

    page.close()

    return

def weatherRadar(city, state):
    uri = 'http://api.wunderground.com/api/d1fec7897078849e/animatedradar/q/' + state + '/' + city + '.gif?num=15&timelabel=1&timelabel.x=30&timelabel.y=30&newmaps=1&width=750&height=750'
    urllib.request.urlretrieve(uri, 'radar.gif')

    
    


