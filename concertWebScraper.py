#Use beautiful soup and mechanize if certain website has javascript use selenium for that website
import subprocess
from bs4 import BeautifulSoup

smithstix = subprocess.check_output("curl -s \"https://www.smithstix.com/music\"", shell=True)
soup = BeautifulSoup(smithstix, "html.parser")
events = soup.find_all("div", {"class": "event-row"})


for allEvents in events:
    # Grab the event title
    title = allEvents.find("div", {"class": "event-title"}).get_text()
    # Get the month day and year of the concert
    day = allEvents.find("div", {"class": "day-week-container"}).get_text().replace("\n", "").replace(" ", "")
    day += ' ' + allEvents.find("div", {"class": "month-container"}).get_text().replace("\n", "").replace(" ", "")
    day += ' ' + allEvents.find("div", {"class": "day-container"}).get_text().replace("\n", "").replace(" ", "")
    day += ' ' + allEvents.find("div", {"class": "year-container"}).get_text().replace("\n", "").replace(" ", "")
    # Get what venue it is at
    venue = ' ' + allEvents.find("div", {"class": "event-venue"}).get_text()
    # Get the price of the concert
    getPrice = allEvents.find("div", {"class": "price"})
    price = ''

    # ignore the ascii errors this allows to grab the text
    # if the ascii encoding doesnt work skip it
    try:
        getPrice = getPrice.encode('ascii',errors='ignore')
    except AttributeError:
        continue

    # Print the text needed
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
