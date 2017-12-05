import pygame, sys, textwrap
from pygame import *
from pygame.locals import *
from WeatherParser import weatherBasic, weatherRadar, weatherHourly
from TimeAndDate import getDateTime
from NewsParser import newsBasic
from GoogleCalendar import get_credentials, get_calendar
import urllib.request
import flicklib
import datetime

#google calendar set up
credentials = get_credentials()

#Pygame Set up
pygame.init()

screen = pygame.display.set_mode()
#pygame.display.toggle_fullscreen()
pygame.display.set_caption('Smart Mirror V0.1')

pygame.mouse.set_visible(False)

clock = pygame.time.Clock()

#time and date set up
displaytime, displaydate, hours, minutes, meridiem = getDateTime()

#declare data variables
weather = {}
newspaper = {}
calendar = list()
date = ''
time = ''

#icon locations
weathericons = {'clear':'clear.png',
                'cloudy':'cloudy.png',
                'fog':'fog.png',
                'night':'clear_night.png',
                'partlycloudy':'partly_day.png',
                'nt_partlycloudy':'partly_night.png',
                'rain':'rain.png',
                'sleet':'sleet.png',
                'snow':'snow.png',
                'thunderstorm':'thunderstorm.png'}

#Set Up Weather Data Gathering
GETWEATHER = USEREVENT + 1
getweatherevent = pygame.event.Event(GETWEATHER)
pygame.event.post(getweatherevent)


weatherBasic('Burlington', 'VT', weather, hours)
radarframes = weatherRadar('Burlington', 'VT')
weatherHourly('Burlington', 'VT', weather, hours)
pygame.time.set_timer(GETWEATHER, 345600)

#set up Newspaper Data Gathering (startup only)
newsBasic(newspaper)

#on off variable
on = True

#declare colors
black = 0,0,0
white = 255,255,255
grey = 190,190,190
dark_grey = 130,130,130
red = 230,0,0

#Set up Fonts
numberfont = pygame.font.Font('timeburnernormal.ttf', 100)
captionfont = pygame.font.Font('timeburnerbold.ttf', 30)
textfont =  pygame.font.Font('timeburnerbold.ttf', 20)
titlefont = pygame.font.Font('timeburnernormal.ttf', 50)
timefont = pygame.font.Font('timeburnernormal.ttf', 100)
datefont = pygame.font.Font('timeburnerbold.ttf', 40)

#set up positions
weatherimg_position = [30,30]
basictemp_position = [0,0]
basictempcaption_position = [0,0]
basicfeelslike_position = [0,0]
feelslikecaption_position = [0,0]
timeblock_position = [0,0]
newsblock1_position = [0,0]
newsblock2_position = [0,0]
newsblock3_position = [0,0]
newsblock4_position = [0,0]
newsblock5_position = [0,0]
newstitle_position = [0,0]
newsauthor_position = [0,0]


#User input Variables
navigation = 'home' #start on the homepage
selectednews = 0
selectedevent = 0
selectedframe = 0
scroll = 0

#Gesture Pad
global xyztxt
global flicktxt
global airwheelint
global touchtxt
global taptxt
global doubletaptxt

xyztxt = ''
flicktxt = ''
airwheelint = 0
touchtxt = ''
taptxt = ''
doubletaptxt = ''

@flicklib.move()
def move(x, y, z):
    global xyztxt
    xyztxt = '{:5.3f} {:5.3f} {:5.3f}'.format(x,y,z)

@flicklib.flick()
def flick(start,finish):
    global flicktxt
    flicktxt = start[0].upper() + finish[0].upper()

@flicklib.airwheel()
def spinny(delta):
    global airwheelint
    airwheelint += delta

@flicklib.double_tap()
def doubletap(position):
    global doubletaptxt
    doubletaptxt = position

@flicklib.tap()
def tap(position):
    global taptxt
    taptxt = position

@flicklib.touch()
def touch(position):
    global touchtxt
    touchtxt = position


#NEWBLOCK
newslabel = titlefont.render('Headlines', True, white, black)
newslabel_w, newslabel_h = newslabel.get_rect().size

#set up news page data gathering
GETNEWS = USEREVENT + 2
getnewsevent = pygame.event.Event(GETNEWS)
pygame.event.post(getnewsevent)
pygame.time.set_timer(GETNEWS, 5760000)

#CALENDAR PAGE
get_calendar(credentials,calendar)
calendar_buffer = 50
markerwidth = 700
eventBlock_w = 650

#WEATHER PAGE
hourly_top = 950
hourly_scale = 20

#formatting
def wraptext(text, font, width):
    """Wrap text to fit inside a given width when rendered.
    :param text: The text to be wrapped.
    :param font: The font the text will be rendered in.
    :param width: The width to wrap to.
    """
    text_lines = text.replace('\t', '    ').split('\n')
    if width is None or width == 0:
        return text_lines

    wrapped_lines = []
    for line in text_lines:
        line = line.rstrip() + ' '
        if line == ' ':
            wrapped_lines.append(line)
            continue

        # Get the leftmost space ignoring leading whitespace
        start = len(line) - len(line.lstrip())
        start = line.index(' ', start)
        while start + 1 < len(line):
            # Get the next potential splitting point
            next = line.index(' ', start + 1)
            if font.size(line[:next])[0] <= width:
                start = next
            else:
                wrapped_lines.append(line[:start])
                line = line[start+1:]
                start = line.index(' ')
        line = line[:-1]
        if line:
            wrapped_lines.append(line)
    return wrapped_lines

while on:
    
    if datetime.datetime.now().hour == 0 and datetime.datetime.now().minute == 0:
        calendar = []
        get_calendar(credentials,calendar)
    
    #get time
    displaytime, displaydate, hours, minutes, meridiem = getDateTime()

    #get display info
    w, h = pygame.display.get_surface().get_size()

    #Reset Background
    screen.fill(black)

    #HOME PAGE
    if navigation == 'home':
        
        #WEATHER BLOCK
        #set up elements
        weatherimg = pygame.image.load(weathericons[weather['icon_to_use']])
        basictemp = numberfont.render(str(int(weather['current_temp'])) + '°F', True, white, black)
        basictempcaption = captionfont.render('Current', True, white, black)
        basictempcaption = pygame.transform.rotate(basictempcaption, 270)
        basicfeelslike = numberfont.render(str(int(float(weather['current_realfeel']))) + '°F', True, white, black)
        feelslikecaption = captionfont.render('Feels Like', True, white, black)
        feelslikecaption = pygame.transform.rotate(feelslikecaption, 270)

        #get elements sizes
        weatherimg_w, weatherimg_h = weatherimg.get_rect().size
        basictemp_w,basictemp_h = basictemp.get_rect().size
        basicfeelslike_w,basicfeelslike_h = basicfeelslike.get_rect().size

        #positionelements relative to weatherimg 
        basictemp_position = [weatherimg_position[0] + (weatherimg_w / 2) - (basictemp_w / 2), weatherimg_h + weatherimg_position[1] + 15]
        basictempcaption_position = [basictemp_w + basictemp_position[0], weatherimg_h + weatherimg_position[1] + 25]
        basicfeelslike_position = [weatherimg_position[0] + (weatherimg_w / 2) - (basictemp_w / 2), basictemp_position[1] + basictemp_h]
        feelslikecaption_position = [basicfeelslike_w + basicfeelslike_position[0], basictemp_h + basictemp_position[1]]

        #draw objects
        screen.blit(weatherimg, weatherimg_position)
        screen.blit(basictemp, basictemp_position)
        screen.blit(basictempcaption, basictempcaption_position)
        screen.blit(basicfeelslike, basicfeelslike_position)
        screen.blit(feelslikecaption, feelslikecaption_position)


        #TIMEDATE BLOCK
        #set up elements
        timeblock = timefont.render(displaytime, True, white, black)
        dateblock = datefont.render(displaydate, True, white, black)

        #get element sizes
        timeblock_w, timeblock_h = timeblock.get_rect().size
        dateblock_w, dateblock_h = dateblock.get_rect().size

        #position relative to time and right side of screen
        timeblock_position = [w - timeblock_w - 30, 30]
        dateblock_position = [w - dateblock_w - 30, timeblock_h]

        #draw elements
        screen.blit(timeblock, timeblock_position)
        screen.blit(dateblock, dateblock_position)

        #NEWS BLOCK
        #block of visible news
        visiblenews = Rect(0, h - 400, w, 300)
        
        #news label
        newslabel_position = [(w / 2) - (newslabel_w / 2), visiblenews.top - newslabel_h]
        screen.blit(newslabel, newslabel_position)
        
        #news headlines
        for article in range (0, len(newspaper) - 1):

            newsitem = textfont.render(newspaper[article]['title'], True, white, black)
            newsitem_w, newsitem_h = newsitem.get_rect().size
            newsitem_position = [(w / 2) - (newsitem_w / 2), scroll + (h / 2) + (article * newsitem_h)]

            #check if news item is in visible news box
            if newsitem_position[1] < visiblenews.bottom and newsitem_position[1] > visiblenews.top:

                #check if center of visible box is inside news item and selected item if true
                if visiblenews.top + visiblenews.height / 2 > newsitem_position[1] and visiblenews.top + visiblenews.height / 2 < newsitem_position[1] + newsitem_h:
                    selectednews = article
                #check if center of visible box is below bottom of news item
                elif visiblenews.top + visiblenews.height / 2 > newsitem_position[1] + newsitem_h:
                    rgbval = 220 * (newsitem_position[1] - visiblenews.top) / (visiblenews.height / 2)
                    
                    if rgbval > 255:
                        rgbval = 255
                    elif rgbval < 0:
                        rgbval = 0
                        
                    color = (rgbval, rgbval, rgbval)
                    newsitem = textfont.render(newspaper[article]['title'], True, color, black)
                else:
                    rgbval = 220 * (visiblenews.bottom - newsitem_position[1]) / (visiblenews.height / 2)
                    
                    if rgbval > 255:
                        rgbval = 255
                    elif rgbval < 0:
                        rgbval = 0
                        
                    color = (rgbval, rgbval, rgbval)
                    newsitem = textfont.render(newspaper[article]['title'], True, color, black)
                
                screen.blit(newsitem, newsitem_position)


        scroll = - airwheelint / 20

        #event listner
        for event in pygame.event.get():
            if event.type == GETWEATHER:
                print('Fetching Weather')
                weatherBasic('Burlington', 'VT', weather, hours)
            if event.type == GETNEWS:
                print('Fetching News')
                newsBasic(newspaper)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        if flicktxt == 'SN': #gesture from South to north
            navigation = 'news'
            scroll = 0
            airwheelint = 0
            flicktxt = ''
            if newspaper[selectednews]['image'] != 'NULL':
                urllib.request.urlretrieve(newspaper[selectednews]['image'], 'newsimage.jpg')
                newsimg = pygame.image.load('newsimage.jpg')

        if flicktxt == 'EW': #gesture from east to west
            navigation = 'calendar'
            scroll = 0
            airwheelint = 0
            flicktxt = ''
            selectedevent = 0

        if flicktxt == 'WE': #gesture from west to east
            navigation = 'weather'
            scroll = 0
            airwheelint = 0
            flicktxt = ''
            #weather page setup
            selectedframe = 0
            weatherHourly('Burlington', 'VT', weather, hours)
            radarframes = weatherRadar('Burlington', 'VT')
            
        if doubletaptxt != '': #double tap to turn off
            on = False

    #NEWS PAGE
    elif navigation == 'news':

        #TITLE (Text Wrapped, scrolled)
        wrappedtext = wraptext(newspaper[selectednews]['title'], titlefont, 900)


        newstitle = titlefont.render(wrappedtext[0], True, white, black)
        newstitle_w, newstitle_h = newstitle.get_rect().size
        newstitle_position = [(w / 2) - (newstitle_w / 2), scroll + newstitle_h]
        screen.blit(newstitle, newstitle_position)
            
        for line in range(1, len(wrappedtext)):
            try:
                newstitle = titlefont.render(wrappedtext[line], True, white, black)
                newstitle_w, newstitle_h = newstitle.get_rect().size
                newstitle_position = [newstitle_position[0], newstitle_h + newstitle_position[1]]
                screen.blit(newstitle, newstitle_position)
            except:
                print("Unicode Error Unprintable character Found in News")

        #Draw image if one exists
        if newspaper[selectednews]['image'] != 'NULL':
            newsimg_w, newsimg_h = newsimg.get_rect().size
            newsimg_position = [(w / 2) - (newsimg_w / 2), newstitle_h + newstitle_position[1] + 5]
            screen.blit(newsimg, newsimg_position)
        else:
            newsimg_position = [0, newstitle_h + newstitle_position[1]]
            newsimg_h = 0
            
    
        wrappedtext = wraptext(newspaper[selectednews]['body'], textfont, 800)

        newsbody = textfont.render(wrappedtext[0].lstrip(), True, white, black)
        newsbody_w, newsbody_h = newsbody.get_rect().size
        newsbody_position = [(w / 2) - (newsbody_w / 2), 50 + newsimg_position[1] + newsimg_h]
        screen.blit(newsbody, newsbody_position)

        for line in range(1, len(wrappedtext)):
            try:
                newsbody = textfont.render(wrappedtext[line].lstrip(), True, white, black)
                newsbody_w, newsbody_h = newsbody.get_rect().size
                newsbody_position = [newsbody_position[0], newsbody_h + newsbody_position[1]]
                screen.blit(newsbody, newsbody_position)

                if newsbody_w < 600:
                    newsbody_position[1] += newsbody_h
            except:
                print('you suckxd')

        scroll = - airwheelint / 10

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if flicktxt == 'NS': #gesture from north to south
            navigation = 'home'
            scroll = 0
            airwheelint = 0
            flicktxt = ''

    elif navigation == 'calendar':
        
        scale = 1.1
        
        #draw 24 background lines and times
        for i in range(0,24):
            #lines
            hourline_position1 = [(w / 2) - (markerwidth / 2), calendar_buffer + (scale * i * 60)]
            hourline_position2 = [hourline_position1[0] + markerwidth, hourline_position1[1]]
            pygame.draw.line(screen, grey, hourline_position1, hourline_position2)

            #labels
            if i == 0 or i == 24:
                hourtxt = '12:00 AM'
            elif i == 12:
                hourtxt = '12:00 PM'
            elif i < 12:
                hourtxt = str(i) + ':00 AM'
            else:
                hourtxt = str(i - 12) + ':00 PM'

            hourlabel = textfont.render(hourtxt, True, grey)
            hourlabel_w, hourlabel_h = hourlabel.get_rect().size
            hourlabel_position = [hourline_position1[0] - hourlabel_w , hourline_position1[1] - (hourlabel_h / 2)]
            screen.blit(hourlabel, hourlabel_position)

        #red now line
        nowline_position1 = [(w / 2) - (markerwidth / 2),
                             calendar_buffer + ((datetime.datetime.now().hour * 60) + datetime.datetime.now().minute) * scale]
        nowline_position2 = [nowline_position1[0] + markerwidth,
                             nowline_position1[1]]
        pygame.draw.line(screen, red, nowline_position1, nowline_position2)

        nowlinelabel = textfont.render(datetime.datetime.now().strftime('%I:%M %p'), True, red)
        nowlinelabel_w, nowlinelabel_h = nowlinelabel.get_rect().size
        nowlinelabel_position = [nowline_position2[0] + 5,
                                 nowline_position2[1] - (nowlinelabel_h / 2)]
        screen.blit(nowlinelabel, nowlinelabel_position)

        #Create Rectangles and text for each event
        for event in range(0, len(calendar)):

            #end events at midnight if they don't already
            if calendar[event]['end'].day != datetime.datetime.now().day:
                eoday = datetime.timedelta(hours = -calendar[event]['end'].hour, minutes = -calendar[event]['end'].minute - 1)
                calendar[event]['end'] += eoday

            eventBlock_top = calendar_buffer + ((calendar[event]['start'].hour * 60 + calendar[event]['start'].minute) * scale)
            eventBlock_bot = calendar_buffer + ((calendar[event]['end'].hour * 60 + calendar[event]['end'].minute) * scale)
            eventBlock_h = eventBlock_bot - eventBlock_top
            calendar[event]['rect'] = Rect((w / 2) - (eventBlock_w / 2), eventBlock_top, eventBlock_w, eventBlock_h)

        #draw rectangles and text for each event
        for eventBlock in range(0, len(calendar)):

            #check for colliding rectangles
            for eventBlock2 in range(eventBlock, len(calendar)):
                if eventBlock != eventBlock2 and calendar[eventBlock]['rect'].colliderect(calendar[eventBlock2]['rect']):

                    calendar[eventBlock]['rect'].width /= 2
                    calendar[eventBlock2]['rect'].width /= 2
                    calendar[eventBlock2]['rect'].left = calendar[eventBlock]['rect'].right

            eventlabel = captionfont.render(calendar[eventBlock]['name'], True, black)
            eventlabel_w, eventlabel_h = eventlabel.get_rect().size
            eventlabel_position = [calendar[eventBlock]['rect'].left +  5,
                                   calendar[eventBlock]['rect'].top]
            
            eventtime = textfont.render(calendar[eventBlock]['start'].strftime('%I:%M %p') + ' to ' + calendar[eventBlock]['end'].strftime('%I:%M %p'),
                                        True,
                                        dark_grey)
            eventtime_w, eventtime_h = eventtime.get_rect().size

            if eventlabel_h + eventtime_h <= calendar[eventBlock]['rect'].height + 10:
                eventtime_position = [eventlabel_position[0],
                                      eventlabel_position[1] + eventlabel_h]
            else:
                eventtime_position = [eventlabel_position[0] + eventlabel_w + 10,
                                      calendar[eventBlock]['rect'].bottom - eventtime_h]

            if selectedevent == eventBlock:
                pygame.draw.rect(screen, white, calendar[eventBlock]['rect'].inflate(-1,-1))
            else:
                pygame.draw.rect(screen, grey, calendar[eventBlock]['rect'].inflate(-2,-2))

            screen.blit(eventlabel, eventlabel_position)
            screen.blit(eventtime, eventtime_position)

        #selecting event
        scroll = airwheelint / 360

        if int(scroll) > len(calendar):
            scroll = 0
            airwheelint = 0
        elif int(scroll) < 0:
            scroll = len(calendar)
            airwheelint = len(calendar) * 360

        selectedevent = int(scroll)

    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if flicktxt == 'WE': #gesture from West to East for Home
            navigation = 'home'
            scroll = 0
            airwheelint = 0
            flicktxt = ''

        if flicktxt == 'EW': #gesture from east to west for further event data
            if len(calendar) > 0:
                navigation = 'event'
                scroll = 0
                airwheelint = 0
                flicktxt = ''
                weatherHourly('Burlington', 'VT', weather, hours)

    elif navigation == 'event':
        #is this event in the future?
        if calendar[selectedevent]['start'] > datetime.datetime.now():
            timeuntil_time = calendar[selectedevent]['start'] - datetime.datetime.now()
            timeuntil_txt = 'Starts in ' + str(int(timeuntil_time.seconds / (60 * 60))) + ' Hours ' + str(int(timeuntil_time.seconds / 60) % 60) + ' Minutes'
            timeuntil_color = red
            
        else:
            timeuntil_txt = 'This Event Already Happened'
            timeuntil_color = grey

        timeuntil = datefont.render(timeuntil_txt, True, timeuntil_color)
        timeuntil_w, timeuntil_h = timeuntil.get_rect().size
        timeuntil_position = [ w - timeuntil_w - 50, 50 ]
        screen.blit(timeuntil, timeuntil_position)

        eventtitle = titlefont.render(calendar[selectedevent]['name'], True, white)
        eventtitle_w, eventtitle_h = eventtitle.get_rect().size
        eventtitle_position = [ 50, timeuntil_position[1] + timeuntil_h]
        screen.blit(eventtitle, eventtitle_position)

        start2end_txt = calendar[selectedevent]['start'].strftime('%H:%M %p') + ' - ' + calendar[selectedevent]['end'].strftime('%H:%M %p')
        start2end = datefont.render(start2end_txt, True, grey)
        start2end_w, start2end_h = start2end.get_rect().size
        start2end_position = [50, eventtitle_position[1] + eventtitle_h]
        screen.blit(start2end, start2end_position)

        

        if flicktxt == 'WE': #gesture from West to East for Calendar
            navigation = 'calendar'
            scroll = 0
            airwheelint = 0
            flicktxt = ''

    elif navigation == 'weather':

        #radar drawing
        mapimage = pygame.image.load('basemap.png')
        radarimage = pygame.image.load('radar' + str(selectedframe) + '.png')

        mapimage_w, mapimage_h = mapimage.get_rect().size
        mapimage_position = [(w / 2) - (mapimage_w / 2), 100]

        screen.blit(mapimage, mapimage_position)
        screen.blit(radarimage, mapimage_position)

        #hourly forecast drawing
        for hour in range(0, len(weather['hourly']) - 1):

            hourimage_lg = pygame.image.load(weathericons[weather['hourly'][hour]['icon_to_use']])
            hourimage_lg_w, hourimage_lg_h = hourimage_lg.get_rect().size

            hourimage = pygame.transform.scale(hourimage_lg, (int(hourimage_lg_w / 10), int(hourimage_lg_h / 10)))
            hourimage_h, hourimage_w = hourimage.get_rect().size
            hourimage_position = [0, hourly_top + (hourly_scale * hour)]

            screen.blit(hourimage, hourimage_position)

        #selecting radar frame
        scroll = airwheelint / 100

        if int(scroll) > radarframes - 1:
            scroll = 0
            airwheelint = 0
        elif int(scroll) < 0:
            scroll = radarframes -1
            airwheelint = (radarframes - 1) * 100

        selectedframe = int(scroll)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if flicktxt == 'EW': #gesture from east to west
            navigation = 'home'
            scroll = 0
            airwheelint = 0
            flicktxt = ''

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
