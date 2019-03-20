import urllib.request
import json
from PIL import Image

darkSkySecret = 'ee0942799d9678f785560fb85d7d4ec5';

#this file is for scraping weather data from Darksky and Open Weather Map
def weatherBasic( latitude, longitude, weather, hours):
    #Get Page from DarkSky
    url = 'https://api.darksky.net/forecast/' + darkSkySecret + '/' + latitude + ',' + longitude + '?exclude=minutely,daily,alerts,flags'
    page = urllib.request.urlopen(url)

    #Convert page into JSON Readable (documented response found here: https://www.wunderground.com/weather/api/d/docs?d=index)
    json_str = page.read().decode('utf8')
    parsed_json = json.loads(json_str)

    #Get Info
    weather['current_temp'] = parsed_json['currently']['temperature']
    weather['current_realfeel'] = parsed_json['currently']['apparentTemperature']
    weather['icon_to_use'] = parsed_json['currently']['icon']

    page.close()

    return

def weatherHourly( latitude, longitude, weather, hours):
    #Get Page WEATHER UNDERGROUND KEY = d1fec7897078849e
    url = 'https://api.darksky.net/forecast/' + darkSkySecret + '/' + latitude + ',' + longitude + '?exclude=minutely,daily,alerts,flags'
    page = urllib.request.urlopen(url)

    #Convert page into JSON Readable (documented response found here: https://www.wunderground.com/weather/api/d/docs?d=index)
    json_str = page.read().decode('utf8')
    parsed_json = json.loads(json_str)

    #Set up weather variable for hours
    weather['hourly']= {}

    #go on and get each hour
    for hour in range (0, len(parsed_json['hourly']['data']) - 1):
        weather['hourly'][hour] = {}
        weather['hourly'][hour]['time'] =  parsed_json['hourly']['data'][hour]['time']
        weather['hourly'][hour]['icon_to_use'] = parsed_json['hourly']['data'][hour]['icon']
        weather['hourly'][hour]['temperature'] = parsed_json['hourly']['data'][hour]['temperature']
        weather['hourly'][hour]['real_feel'] = parsed_json['hourly']['data'][hour]['apparentTemperature']
        weather['hourly'][hour]['chance_rain'] = parsed_json['hourly']['data'][hour]['precipProbability'] * 100

    page.close()

    return

def iter_frames(image):
    i = 0
    loop = True
    while loop:
        try:
            image.seek(i)
            transparency = image.info['transparency']
            image.save('radar' + str(i) + '.png', transparency=transparency)
            i += 1
        except EOFError:
            loop = False
            pass
    return i
    
def weatherRadar(city, state):
    key = 'AIzaSyCyQOjgzcgd3zF--Fha9LD0oz5C_O71Fg8'
    
    uri = 'http://api.wunderground.com/api/d1fec7897078849e/animatedradar/q/' + state + '/' + city + '.gif?num=15&timelabel=1&timelabel.x=30&timelabel.y=30&newmaps=0&width=900&height=900'
    urllib.request.urlretrieve(uri, 'radar.gif')

    gif = Image.open('radar.gif')

    frames = iter_frames(gif)
    
    style = '&maptype=roadmap&style=element:geometry%7Ccolor:0x212121&style=element:labels%7Cvisibility:off&style=element:labels.icon%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0x757575&style=element:labels.text.stroke%7Ccolor:0x212121&style=feature:administrative%7Celement:geometry%7Ccolor:0x757575&style=feature:administrative.country%7Celement:labels.text.fill%7Ccolor:0x9e9e9e&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.locality%7Celement:labels.text.fill%7Ccolor:0xbdbdbd&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:poi.park%7Celement:geometry%7Ccolor:0x181818&style=feature:poi.park%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:poi.park%7Celement:labels.text.stroke%7Ccolor:0x1b1b1b&style=feature:road%7Celement:geometry.fill%7Ccolor:0x4e4e4e&style=feature:road%7Celement:labels.text.fill%7Ccolor:0x8a8a8a&style=feature:road.arterial%7Celement:geometry%7Ccolor:0x373737&style=feature:road.arterial%7Celement:geometry.fill%7Ccolor:0x9d9d9d&style=feature:road.highway%7Celement:geometry%7Ccolor:0x959595&style=feature:road.highway.controlled_access%7Celement:geometry%7Ccolor:0x4e4e4e&style=feature:road.local%7Celement:geometry.fill%7Ccolor:0x818181&style=feature:road.local%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:transit%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:water%7Celement:geometry%7Ccolor:0x828282&style=feature:water%7Celement:labels%7Cvisibility:off&style=feature:water%7Celement:labels.text.fill%7Ccolor:0x3d3d3d'
    basemapuri = 'https://maps.googleapis.com/maps/api/staticmap?center=' + city + ',' + state + '&zoom=8&size=450x450&scale=2' + style + '&key=AIzaSyCyQOjgzcgd3zF--Fha9LD0oz5C_O71Fg8'
    urllib.request.urlretrieve(basemapuri, 'basemap.png')

    return frames

    

    
    


