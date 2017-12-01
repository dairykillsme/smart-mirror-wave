import pygame, sys, textwrap
from pygame import *
from pygame.locals import *
from WeatherParser import weatherBasic
from TimeAndDate import getDateTime
from NewsParser import newsBasic
import urllib.request
import flicklib

#Pygame Set up
pygame.init()

screen = pygame.display.set_mode()
#pygame.display.toggle_fullscreen()
pygame.display.set_caption('Smart Mirror V0.1')

clock = pygame.time.Clock()

#time and date set up
displaytime, displaydate, hours, minutes, meridiem = getDateTime()

#declare data variables
weather = {}
newspaper = {}
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
pygame.time.set_timer(GETWEATHER, 300000)

#set up Newspaper Data Gathering (startup only)
newsBasic(newspaper)

#on off variable
on = True

#declare colors
black = 0,0,0
white = 255,255,255
grey = 190,190,190
dark_grey = 130,130,130

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
selectednews = int(len(newspaper) / 2) #start with middle news item selected
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
        basictemp = numberfont.render(str(int(weather['current_temp'])) + '°F', True, white)
        basictempcaption = captionfont.render('Current', True, white)
        basictempcaption = pygame.transform.rotate(basictempcaption, 270)
        basicfeelslike = numberfont.render(str(int(float(weather['current_realfeel']))) + '°F', True, white)
        feelslikecaption = captionfont.render('Feels Like', True, white)
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
        timeblock = timefont.render(displaytime, True, white)
        dateblock = datefont.render(displaydate, True, white)

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
        #set up elements
        newsblock1 = textfont.render(newspaper[selectednews - 2]['title'], True, dark_grey)
        newsblock2 = textfont.render(newspaper[selectednews - 1]['title'], True, grey)
        newsblock3 = textfont.render(newspaper[selectednews]['title'], True, white)
        newsblock4 = textfont.render(newspaper[selectednews + 1]['title'], True, grey)
        newsblock5 = textfont.render(newspaper[selectednews + 2]['title'], True, dark_grey)
        
        #get element sizes
        newsblock1_w, newsblock1_h = newsblock1.get_rect().size
        newsblock2_w, newsblock2_h = newsblock2.get_rect().size
        newsblock3_w, newsblock3_h = newsblock3.get_rect().size
        newsblock4_w, newsblock4_h = newsblock4.get_rect().size
        newsblock5_w, newsblock5_h = newsblock5.get_rect().size
        
        #position relative to bottom news item
        newsblock5_position = [(w / 2) - (newsblock5_w / 2), h - 30]
        newsblock4_position = [(w / 2) - (newsblock4_w / 2), newsblock5_position[1] - newsblock4_h]
        newsblock3_position = [(w / 2) - (newsblock3_w / 2), newsblock4_position[1] - newsblock3_h]
        newsblock2_position = [(w / 2) - (newsblock2_w / 2), newsblock3_position[1] - newsblock2_h]
        newsblock1_position = [(w / 2) - (newsblock1_w / 2), newsblock2_position[1] - newsblock1_h]
        
        #draw elements
        screen.blit(newsblock1, newsblock1_position)
        screen.blit(newsblock2, newsblock2_position)
        screen.blit(newsblock3, newsblock3_position)
        screen.blit(newsblock4, newsblock4_position)
        screen.blit(newsblock5, newsblock5_position)

        #event listner
        for event in pygame.event.get():
            if event.type == GETWEATHER:
                weatherBasic('Burlington', 'VT', weather, hours)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if (event.key == K_w): #finger spin will replace
                    #move selected news item up
                    if selectednews <= len(newspaper) - 4 :
                        selectednews += 1
                if (event.key == K_s): #finger spin will replace
                    #move selected news item down
                    if selectednews >= 2 :
                        selectednews -= 1
                        
        if flicktxt == 'EW': #gesture from east to west for news
            navigation = 'news'
            scroll = 0
            airwheelint = 0
            flicktxt = ''
            if newspaper[selectednews]['image'] != 'NULL':
                urllib.request.urlretrieve(newspaper[selectednews]['image'], 'newsimage.jpg')
                newsimg = pygame.image.load('newsimage.jpg')

        if doubletaptxt != '': #double tap to turn off
            on = False

    #NEWS PAGE
    elif navigation == 'news':

        #TITLE (Text Wrapped, scrolled)
        wrappedtext = wraptext(newspaper[selectednews]['title'], titlefont, 900)


        newstitle = titlefont.render(wrappedtext[0], True, white)
        newstitle_w, newstitle_h = newstitle.get_rect().size
        newstitle_position = [(w / 2) - (newstitle_w / 2), scroll + newstitle_h]
        screen.blit(newstitle, newstitle_position)
            
        for line in range(1, len(wrappedtext)):
            try:
                newstitle = titlefont.render(wrappedtext[line], True, white)
                newstitle_w, newstitle_h = newstitle.get_rect().size
                newstitle_position = [newstitle_position[0], newstitle_h + newstitle_position[1]]
                screen.blit(newstitle, newstitle_position)
            except:
                print("dummy machine broke")

        #Draw image if one exists
        if newspaper[selectednews]['image'] != 'NULL':
            newsimg_w, newsimg_h = newsimg.get_rect().size
            newsimg_position = [(w / 2) - (newsimg_w / 2), newstitle_h + newstitle_position[1] + 5]
            screen.blit(newsimg, newsimg_position)
        else:
            newsimg_position = [0, newstitle_h + newstitle_position[1]]
            newsimg_h = 0
            
    
        wrappedtext = wraptext(newspaper[selectednews]['body'], textfont, 800)

        newsbody = textfont.render(wrappedtext[0].lstrip(), True, white)
        newsbody_w, newsbody_h = newsbody.get_rect().size
        newsbody_position = [(w / 2) - (newsbody_w / 2), 50 + newsimg_position[1] + newsimg_h]
        screen.blit(newsbody, newsbody_position)

        for line in range(1, len(wrappedtext)):
            try:
                newsbody = textfont.render(wrappedtext[line].lstrip(), True, white)
                newsbody_w, newsbody_h = newsbody.get_rect().size
                newsbody_position = [newsbody_position[0], newsbody_h + newsbody_position[1]]
                screen.blit(newsbody, newsbody_position)

                if newsbody_w < 700:
                    newsbody_position[1] += newsbody_h
            except:
                print('you suckxd')

        scroll = airwheelint / 10

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if (event.key == K_w):#remove with addition of airwheel
                    scroll -= 20
                if (event.key == K_s):#remove with addition of airwheel
                    scroll += 20

        if flicktxt == 'WE': #gesture from east to west for news
            navigation = 'home'
            scroll = 0
            airwheelint = 0
            flicktxt = ''

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
