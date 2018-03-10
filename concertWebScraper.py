#Use beautiful soup and mechanize if certain website has javascript use selenium for that website
import mechanize, subprocess
from bs4 import BeautifulSoup

smithstix = subprocess.check_output("curl -s \"https://www.smithstix.com/music\"", shell=True)
soup = BeautifulSoup(smithstix, "html5lib")
events = soup.find_all("div", {"class": "event-row"})


for allEvents in events:
    title = allEvents.find("div", {"class": "event-title"}).get_text()
    day = allEvents.find("div", {"class": "day-week-container"}).get_text().replace("\n", "").replace(" ", "")
    day += ' ' + allEvents.find("div", {"class": "month-container"}).get_text().replace("\n", "").replace(" ", "")
    day += ' ' + allEvents.find("div", {"class": "day-container"}).get_text().replace("\n", "").replace(" ", "")
    day += ' ' + allEvents.find("div", {"class": "year-container"}).get_text().replace("\n", "").replace(" ", "")
    venue = ' ' + allEvents.find("div", {"class": "event-venue"}).get_text()
    getPrice = allEvents.find("div", {"class": "price"})
    price = ''
    try:
        getPrice = getPrice.encode('ascii',errors='ignore')
    except AttributeError:
        continue
    beginFlag = False
    for char in getPrice:
        if char == '>':
            beginFlag = True
            continue
        if beginFlag == True:
            if char == '<':
                break
            price += char
    print '\n' + title + ': ' + day + ' ' + price + '\n' + venue
