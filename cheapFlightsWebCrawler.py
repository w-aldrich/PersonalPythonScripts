from bs4 import BeautifulSoup
import time, datetime, sys, re
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

'''
This program will scrape Alaska Airlines and Delta Airlines for the cheapest flights
It will take a while to run due to not getting banned from these sites
If Alaska Airlines asks if you are a robot must run just the driver pulling up the website
and complete the "I am not a robot" test
'''

'''
THIS SECTION COMPUTES PROPPER DATES FOR SEARCHING
'''
weekInAdvance = '' #week from current day
threeDayTrip = '' #3 days from a week from the current day
tripInTwoMonthsDepart = '' #2 months from the current day
tripInTwoMonthsReturn = '' #2 weeks from 2 months from the current day

now = datetime.datetime.now()
month = now.month
day = now.day + 7
year = now.year

if day > 30:
    month += 1
    day %= 30
    month += 1
    if month > 12:
        month %= 12

###This will get the current date 7 days from now
weekInAdvance = str(month) + "/" + str(day) + "/" + str(year)

threeDayReturnDay = day + 3
threeDayReturnMonth = month
if threeDayReturnDay > 30:
    threeDayReturnDay %=30
    threeDayReturnMonth += 1
    if threeDayReturnMonth > 12:
        threeDayReturnMonth %=30

###This is a return date 3 days from weekInAdvance
threeDayTrip = str(threeDayReturnMonth)+ "/" + str(threeDayReturnDay) + "/" + str(year)

tripDepartMonth = month + 2
if tripDepartMonth > 12:
    month %= 12
tripDepartDay = day - 7
tripReturnMonth = tripDepartMonth
tripReturnDay = tripDepartDay + 14
if tripReturnDay > 30:
    tripReturnDay %= 30
    tripReturnMonth += 1
    if tripReturnMonth > 12:
        tripReturnMonth %= 12

###This is the departure date 2 months from now
tripInTwoMonthsDepart = str(tripDepartMonth) + "/" + str(tripDepartDay) + "/" + str(year)
###This is the return date 2 weeks from the departure date in 2 months
tripInTwoMonthsReturn = str(tripReturnMonth) + "/" + str(tripReturnDay) + "/" + str(year)


'''
THIS SECTION IS WHERE TO ADD NEW CITIES
'''
###SLC is our departure point
slc = 'Salt Lake City, UT'
#Delta
rome = "FCO"
frankfurt = "FRA"
hanoiVietnam = "HAN"
zealand = "AKL"
austrailia = 'SYD'
peru = 'LIM'
rio = 'GIG'
brazil = 'BSB'
chili = 'SCL'
costa = 'SJO'
mongolia = 'ULN'
thai = 'BKK'
marrakech = 'RAK' #Morroco
barcelona = 'BCN'
istanbul = 'IST'
croacia = 'ZAG'
iceland = 'KEF'
#Alaska
coloradoSpring = 'Colorado Springs, CO'
portland = 'Portland, OR'
newMexico = 'Albuquerque, NM'
eugene = 'Eugene, OR'
bayArea = 'San Diego, CA'
denver = 'Denver, CO'
vegas = 'Las Vegas, NV'
newYork = 'New York, NY (JFK-Kennedy)'
newOrleans = 'New Orleans, LA'
boston = 'Boston, MA'
alaska = 'Anchorage, AK (ANC-Anchorage Intl.)'
southDakota = 'Rapid City, SD (RAP-Rapid City Regional)'
#A list of all the cities in the USA I care about
nationalCityList = [bayArea, coloradoSpring, denver, portland, newMexico, eugene, vegas, newYork, newOrleans, boston, alaska, southDakota]
#A list of country airports to travel to
interNationalCityList = [rome, frankfurt, hanoiVietnam, zealand, austrailia, peru, rio, brazil, chili, costa, mongolia, thai, marrakech, barcelona, istanbul, croacia, iceland]

'''
This will navigate Alaska Airlines website
If the website thinks you are a robot, must open website in webscraper without doing this
You must then navigate the I am not a robot functions to complete
'''
def navigateAlaskaAirlines(gotToCity, seleniumDriver):
    time.sleep(3) #ensure that the page loads before doing anything else
    # seleniumDriver.find_element_by_id('oneWay').click() #click for a one way ticket price
    moveMouseToFromCity = seleniumDriver.find_element_by_id('fromCity1')
    actions = ActionChains(seleniumDriver) #This will allow simulation of mouse movement
    actions.move_to_element(moveMouseToFromCity)
    actions.click(moveMouseToFromCity)
    # time.sleep(2)
    # for letter in slc:
    #     moveMouseToFromCity.send_keys(letter) #enter in departure city
    #     time.sleep(.15)
    moveMouseToFromCity.send_keys(slc)
    moveMouseToFromCity.send_keys(Keys.TAB)
    # time.sleep(2)
    # for letter in gotToCity:
    #     seleniumDriver.find_element_by_id('toCity1').send_keys(letter) #enter in the city to go to
    #     time.sleep(.15)
    seleniumDriver.find_element_by_id('toCity1').send_keys(gotToCity)
    seleniumDriver.find_element_by_id('toCity1').send_keys(Keys.TAB)
    # time.sleep(2)
    departureDate = seleniumDriver.find_element_by_id('departureDate1')
    # departureDate.send_keys(Keys.DELETE)
    departureDate.clear() #clear the date in the departure date and send a week in advance
    # for letter in weekInAdvance:
    #     departureDate.send_keys(letter)
    departureDate.send_keys(weekInAdvance)
    departureDate.send_keys(Keys.TAB)
    # time.sleep(1)
    returnDate = seleniumDriver.find_element_by_id('returnDate')
    # returnDate.send_keys(Keys.DELETE)
    returnDate.clear()
    # for letter in threeDayTrip:
    #     returnDate.send_keys(letter)
    returnDate.send_keys(threeDayTrip)
    returnDate.send_keys(Keys.TAB)
    select = Select(seleniumDriver.find_element_by_id('adultCount')) #Select 2 adults for price
    select.select_by_visible_text('2 adults')
    # time.sleep(1)
    submitButton = seleniumDriver.find_element_by_id('findFlights')
    actions.move_to_element(submitButton)
    # time.sleep(1)
    actions.click(submitButton)
    submitButton.click() #Submit your search results
    time.sleep(5) # wait for page to load
    selectLowPrice = Select(seleniumDriver.find_element_by_id('SortBy0')) #Sort by price
    actions = ActionChains(seleniumDriver) #This will allow simulation of mouse movement
    actions.move_to_element(selectLowPrice)
    actions.click(selectLowPrice)
    selectLowPrice.select_by_visible_text('Price')
    time.sleep(2)
    html = seleniumDriver.page_source #grab the html from the webpage
    seleniumDriver.close()
    soup = BeautifulSoup(html, "html5lib") #soup it
    cheapestFlight = soup.find(id='flightInfoRow_0_0') #This id is where the cheapestFlight actually resides
    flightInfo = cheapestFlight.get_text() #grab the text and put it into a list
    return flightInfo.split() #split on all the whitespace

'''
THIS WILL PRINT OUT ALL OF THE INFORMATION FROM navigateAlaskaAirlines()
'''
def printOutInformationAlaska(goThroughFlightInfo, cityGoingTo):
    cost = ''
    flightTime = ''
    count = 0 #Count to get the cost, broken into 4 parts, once this is 4 done finding info
    foundHours = False #Flag, the first time hours appears is the flight time hours
    foundMinues = False #Flag, the first time minutes appears is the flight time minutes
    prev = '' #Keep track of the previous string
    stops = ''
    for string in goThroughFlightInfo:
        if string == 'stop' or string == 'stops':
            stops += prev + ' ' + string
        if 'hours' in string:
            if foundHours == False:
                flightTime += string
                foundHours = True
        if 'minutes' in string:
            if foundMinues == False:
                flightTime += ' ' + string
                foundMinues = True
        if '$' in string:
            count += 1
            if count == 4:
                cost = string
                break
        prev = string
    print "\nALASKA AIRLINES: The price for: "+ weekInAdvance + " to " + threeDayTrip + " from " + slc + " to " + cityGoingTo + " is: " + cost + "\nThe Flight Time is: " + flightTime
    if stops == '':
        print "This flight has: 0 stops\n"
    else:
        print "This flight has: " + stops + "\n"

'''
This allows the opportunity for multi-threading with Alaska Airlines
BE CAREFUL!!! If multi-threading more likely to be considered a robot
'''
def runAlaskaWithThreads(city):
    #create a new driver for every city to get rid of cookie issues
    # options = Options()
    # options.add_argument("--headless")
    # options.add_argument('--disable-gpu')
    # seleniumDriver = webdriver.Chrome(executable_path=r'/Users/waldrich/python/chromeDriver', chrome_options=options)
    seleniumDriver = webdriver.Chrome(executable_path=r'/Users/waldrich/python/chromeDriver')
    seleniumDriver.get('https://www.alaskaair.com/')
    time.sleep(2)
    try:
        printOutInformationAlaska(navigateAlaskaAirlines(city, seleniumDriver), city)
    except NoSuchElementException:
        seleniumDriver.close()
        print "\nAlaska Airlines Unable to find: " + city + "\n"
    except AttributeError:
        seleniumDriver.close()
        print "\nAlaska Airlines Unable to find: " + city + "\n"

'''
This will navigate www.delta.com
Must have so many sleep functions so you dont look like a robot
The large wait times must happen so that the page actually loads up
'''
def navigateDelta(city, seleniumDriver):
    time.sleep(3)
    destination = seleniumDriver.find_element_by_id('destinationCity')
    destination.send_keys(city)
    destination.send_keys(Keys.TAB)
    time.sleep(3)
    depart = seleniumDriver.find_element_by_id('departureDate')
    if city in nationalCityList:
        depart.send_keys(weekInAdvance)
    else:
        depart.send_keys(tripInTwoMonthsDepart)
    # time.sleep(2)
    returnDate = seleniumDriver.find_element_by_id('returnDate')
    if city in nationalCityList:
        returnDate.send_keys(threeDayTrip)
    else:
        returnDate.send_keys(tripInTwoMonthsReturn)
    # time.sleep(2)
    select = Select(seleniumDriver.find_element_by_id('paxCount')) #Select 2 adults for price
    # time.sleep(2)
    select.select_by_visible_text('2')
    # seleniumDriver.find_element_by_id('paxCount-button').click() #number of adults button
    # time.sleep(3)
    # seleniumDriver.find_element_by_id('ui-id-19').click() #2 adults
    # time.sleep(2)
    seleniumDriver.find_element_by_id('findFlightsSubmit').click()
    time.sleep(10)
    try:
        url = seleniumDriver.current_url
        splitUrl = url.split('search-')
        splitUrl[1] = splitUrl[1][7:]
        url = splitUrl[0] + 'flexible-dates' + splitUrl[1]
        time.sleep(10)
        seleniumDriver.get(url) #Change URL to flexible dates
        time.sleep(20)
        html = seleniumDriver.page_source
        seleniumDriver.close()
        soup = BeautifulSoup(html, "html5lib")
        cheapestFlight = soup.prettify()
        return cheapestFlight.split("\n")
    except IndexError:
        seleniumDriver.close()
        return "Delta could not find the flight you were looking for"

'''
THIS WILL PRINT ALL OF THE INFORMATION FROM navigateDelta()
'''
def printDelta(cheapestFlight, cityGoingTo):
    departOptions = []
    startPoint = False
    '''
    This section splits the page source to get the table of flexible dates
    '''
    if(cheapestFlight == "Delta could not find the flight you were looking for"):
        "Delta could not find the flight you were looking for: " + cityGoingTo
    for blah in cheapestFlight:
        if startPoint == True:
            if "<" not in blah:
                departOptions.append(blah)
        if 'Available Flights from Flexible Dates Price Table' in blah:
            startPoint = True
        if '&lt; Swipe to view more &gt;' in blah:
            startPoint = False

    startPoint = False
    countToSkip = 0
    countToAdd = 0
    info = ''
    flightInformation = []
    '''
    This section will get all of the departure options in the flexible table
    '''
    for blah in departOptions:
        if countToSkip > 10:
            if countToAdd <= 10:
                if countToAdd == 0 and "Departure" not in blah:
                    continue
                blah = blah.replace(" ", "")
                info = info + ' ' + blah
                countToAdd += 1
            if countToAdd == 10:
                flightInformation.append(info)
                info = ''
                countToAdd = 0
        countToSkip += 1

    lowestFairs = []
    '''
    This is to get the lowest fare from the departure options
    '''
    for information in flightInformation:
        if "LowestFare" in information:
            information.replace("LowestFare", "")
            lowestFairs.append(information)
    if lowestFairs == []:
        for information in flightInformation:
            print information

    '''
    This is printing the absolute lowest fares searching 2 months in advance for 2 weeks trip
    '''
    for information in lowestFairs:
        print "DELTA Options: The lowest fair for " + cityGoingTo + " is: " + information
    print "\n"

'''
This allows for the opportunity to run with multiple threads
BE CAREFUL!!!! If multithreading Delta will ban you if using more than
two threads. THIS IS STILL SKETCHY. Must restart computer to be able to access site again.
'''
def runDeltaWithThreads(city):
    seleniumDriver = webdriver.Chrome(executable_path=r'/Users/waldrich/python/chromeDriver')
    seleniumDriver.get('https://www.delta.com/')
    try:
        printDelta(navigateDelta(city, seleniumDriver), city)
    except NoSuchElementException :
        seleniumDriver.close()
        print "\nDELTA Unable to find: " + city
    except AttributeError:
        seleniumDriver.close()
        print "\nDELTA Unable to find: " + city

'''
Uncomment below incase of Robot message from Alaska Airlines
If blocked from Delta turn off computer for a few minutes then retry
'''
# seleniumDriver = webdriver.Chrome(executable_path=r'/Users/waldrich/python/chromeDriver')
# seleniumDriver.get('https://www.alaskaair.com')

'''
-----START OF PROGRAM-----
'''
for city in nationalCityList:
    runAlaskaWithThreads(city)
for city in nationalCityList: #must run Delta separately to get through Alaska quickly
    runDeltaWithThreads(city)
for city in interNationalCityList:
    runDeltaWithThreads(city)
