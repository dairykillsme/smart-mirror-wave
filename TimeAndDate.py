import time

def getDateTime():
    hours = int(time.strftime('%H'))
    minutes = int(time.strftime('%M'))
    meridiem = time.strftime('%p')
    displaytime = time.strftime('%I:%M %p')
    displaydate = time.strftime('%A, %B %d %Y')
    return displaytime, displaydate, hours, minutes, meridiem

