from bs4 import BeautifulSoup
import time, datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

# API's ?
# https://developer.alaskaair.com/
# http://www.flyfrontier.com/f9_services/wordwheel/wordwheellocal.asmx
# https://www.travelboutiqueonline.com/flight_api.aspx

# List of airlines that fly out of SLC
# Delta --- Can Scrape for personal use
# United --- Cannot Scrape
# Frontier --- maybe API?
# SouthWest --- Cannot Scrape
# Alaska --- Has API Change from Scraping to API 2 hits per min?
# Boutique --- maybe api
# American
# jetBlue

'''
This program will scrape multiple Airlines for the cheapest flights
It will take a while to run due to not getting banned from these sites
If Alaska Airlines asks if you are a robot must run just the driver pulling up the website
and complete the "I am not a robot" test
'''

'''
THIS SECTION COMPUTES PROPPER DATES FOR SEARCHING
'''
week_in_advance = '' #week from current day
three_day_trip = '' #3 days from a week from the current day
trip_in_2_m_depart = '' #2 months from the current day
trip_in_2_m_return = '' #2 weeks from 2 months from the current day

def week_in_advance_3_day_trip():
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
    week_in_advance = str(month) + "/" + str(day) + "/" + str(year)

    three_day_return_day = day + 3
    three_day_return_month = month
    if three_day_return_day > 30:
        three_day_return_day %=30
        three_day_return_month += 1
        if three_day_return_month > 12:
            three_day_return_month %=30

    ###This is a return date 3 days from week_in_advance
    three_day_trip = str(three_day_return_month)+ "/" + str(three_day_return_day) + "/" + str(year)

    return (week_in_advance, three_day_trip)


def depart_2_m_2_wk_trip():
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    year = now.year

    trip_depart_month = month + 2
    if trip_depart_month > 12:
        month %= 12
    trip_depart_day = day
    trip_return_month = trip_depart_month
    trip_return_day = trip_depart_day + 14
    if trip_return_day > 30:
        trip_return_day %= 30
        trip_return_month += 1
        if trip_return_month > 12:
            trip_return_month %= 12
    ###This is the departure date 2 months from now
    trip_in_2_m_depart = str(trip_depart_month) + "/" + str(trip_depart_day) + "/" + str(year)
    ###This is the return date 2 weeks from the departure date in 2 months
    trip_in_2_m_return = str(trip_return_month) + "/" + str(trip_return_day) + "/" + str(year)
    return (trip_in_2_m_depart, trip_in_2_m_return)

def graduation_trip():
    graduation_trip_depart = "12/16/2018"
    graduation_trip_return = "12/23/2019"
    return (graduation_trip_depart, graduation_trip_return)


'''
THIS SECTION IS WHERE TO ADD NEW CITIES
'''
###SLC is our departure point
slc = 'Salt Lake City, UT'
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

interNationalCityList ={"Rome Italy": 'FCO', "FrankFurt": 'FRA', "Hanoi, Vietnam": 'HAN', "New Zealand": 'AKL',
                        "Austrailia": 'SYD', "Peru": "LIM", "Rio de Janeiro, Brazil": 'GIG', "Brazil": 'BSB',
                        "Chile": 'SCL', "Mongolia": 'ULN', "Thailand": 'BKK', "Marrakech": 'RAK', "Barcelona": 'BCN',
                        "Istanbul": 'IST', "Croacia": 'ZAG', "Iceland": 'KEF'}

beachSpots = {"Koh Lanta, Thailand (KBV)": 'KBV', "El Nido, Palawan, Philippines (MNL)": 'MNL',
              "Costa Rica (SJO)": 'SJO', "Maui, Hawaii (OGG)": 'OGG', "Rio de Janeiro, Brazil (GIG)": 'GIG',
              "Musandam, Oman (KHS)": 'KHS', "Corn Islands, Nicaragua (MGU)": 'MGU', "Aruba (AUA)": 'AUA',
              "Gan (Maldives) (GAN)": 'GAN', "Handimaadhoo Maldives (HAQ)": 'HAQ', "Hulhule Maldives (HLE)": 'MLE',
              "Maamingili Maldives (VAM)": 'VAM', "Bali Indonesia (DPS)": 'DPS', "Bora Bora (BOB)": 'BOB', "Grand Cayman": "GCM"}

# def navigateAlaskaAirlines(gotToCity, selenium_driver):
#     time.sleep(3) #ensure that the page loads before doing anything else
#     # selenium_driver.find_element_by_id('oneWay').click() #click for a one way ticket price
#     moveMouseToFromCity = selenium_driver.find_element_by_id('fromCity1')
#     actions = ActionChains(selenium_driver) #This will allow simulation of mouse movement
#     actions.move_to_element(moveMouseToFromCity)
#     actions.click(moveMouseToFromCity)
#     # time.sleep(2)
#     # for letter in slc:
#     #     moveMouseToFromCity.send_keys(letter) #enter in departure city
#     #     time.sleep(.15)
#     moveMouseToFromCity.send_keys(slc)
#     moveMouseToFromCity.send_keys(Keys.TAB)
#     # time.sleep(2)
#     # for letter in gotToCity:
#     #     selenium_driver.find_element_by_id('toCity1').send_keys(letter) #enter in the city to go to
#     #     time.sleep(.15)
#     selenium_driver.find_element_by_id('toCity1').send_keys(gotToCity)
#     selenium_driver.find_element_by_id('toCity1').send_keys(Keys.TAB)
#     # time.sleep(2)
#     departureDate = selenium_driver.find_element_by_id('departureDate1')
#     # departureDate.send_keys(Keys.DELETE)
#     departureDate.clear() #clear the date in the departure date and send a week in advance
#     # for letter in week_in_advance:
#     #     departureDate.send_keys(letter)
#     #     time.sleep(.15)
#     departureDate.send_keys(week_in_advance)
#     departureDate.send_keys(Keys.TAB)
#     # time.sleep(1)
#     returnDate = selenium_driver.find_element_by_id('returnDate')
#     # returnDate.send_keys(Keys.DELETE)
#     returnDate.clear()
#     # for letter in three_day_trip:
#     #     returnDate.send_keys(letter)
#     #     time.sleep(.15)
#     returnDate.send_keys(three_day_trip)
#     returnDate.send_keys(Keys.TAB)
#     select = Select(selenium_driver.find_element_by_id('adultCount')) #Select 2 adults for price
#     select.select_by_visible_text('2 adults')
#     # time.sleep(1)
#     submitButton = selenium_driver.find_element_by_id('findFlights')
#     actions.move_to_element(submitButton)
#     # time.sleep(1)
#     actions.click(submitButton)
#     submitButton.click() #Submit your search results
#     time.sleep(5) # wait for page to load
#     selectLowPrice = Select(selenium_driver.find_element_by_id('SortBy0')) #Sort by price
#     actions = ActionChains(selenium_driver) #This will allow simulation of mouse movement
#     actions.move_to_element(selectLowPrice)
#     actions.click(selectLowPrice)
#     selectLowPrice.select_by_visible_text('Price')
#     time.sleep(2)
#     html = selenium_driver.page_source #grab the html from the webpage
#     selenium_driver.close()
#     soup = BeautifulSoup(html, "html.parser") #soup it
#     cheapestFlight = soup.find(id='flightInfoRow_0_0') #This id is where the cheapestFlight actually resides
#     flightInfo = cheapestFlight.get_text() #grab the text and put it into a list
#     return flightInfo.split() #split on all the whitespace
#
# '''
# THIS WILL PRINT OUT ALL OF THE INFORMATION FROM navigateAlaskaAirlines()
# '''
# def printOutInformationAlaska(goThroughFlightInfo, cityGoingTo):
#     cost = ''
#     flightTime = ''
#     count = 0 #Count to get the cost, broken into 4 parts, once this is 4 done finding info
#     foundHours = False #Flag, the first time hours appears is the flight time hours
#     foundMinues = False #Flag, the first time minutes appears is the flight time minutes
#     prev = '' #Keep track of the previous string
#     stops = ''
#     for string in goThroughFlightInfo:
#         if string == 'stop' or string == 'stops':
#             stops += prev + ' ' + string
#         if 'hours' in string:
#             if foundHours == False:
#                 flightTime += string
#                 foundHours = True
#         if 'minutes' in string:
#             if foundMinues == False:
#                 flightTime += ' ' + string
#                 foundMinues = True
#         if '$' in string:
#             count += 1
#             if count == 4:
#                 cost = string
#                 break
#         prev = string
#     print "\nALASKA AIRLINES: The price for: "+ week_in_advance + " to " + three_day_trip + " from " + slc + " to " + cityGoingTo + " is: " + cost + "\nThe Flight Time is: " + flightTime
#     if stops == '':
#         print "This flight has: 0 stops\n"
#     else:
#         print "This flight has: " + stops + "\n"


# def runAlaska(city):
#     #create a new driver for every city to get rid of cookie issues
#     # options = Options()
#     # options.add_argument("--headless")
#     # options.add_argument('--disable-gpu')
#     # selenium_driver = webdriver.Chrome(executable_path=r'/Users/waldrich/python/chromeDriver'', chrome_options=options)
#     selenium_driver = webdriver.Chrome(executable_path=r'/Users/waldrich/PersonalPythonScripts/chromeDriver')
#     selenium_driver.get('https://www.alaskaair.com/')
#     time.sleep(2)
#     try:
#         printOutInformationAlaska(navigateAlaskaAirlines(city, selenium_driver), city)
#     except NoSuchElementException:
#         selenium_driver.close()
#         print "\nAlaska Airlines Unable to find: " + city + "\n"
#     except AttributeError:
#         selenium_driver.close()
#         print "\nAlaska Airlines Unable to find: " + city + "\n"

'''
This will navigate www.delta.com
The large wait times must happen so that the page actually loads up
'''
def navigate_delta(airport_code, selenium_driver):
    time.sleep(3)
    action = ActionChains(selenium_driver) #This will allow simulation of mouse movement

    # destination = selenium_driver.find_element_by_id('destinationCity')
    destination = selenium_driver.find_element_by_id('input_destination_1')
    clickOnElement(destination, action)
    sendLetters(airport_code, destination)
    time.sleep(3)
    # depart = selenium_driver.find_element_by_id('departureDate')
    depart = selenium_driver.find_element_by_class('calenderDepartSpan')
    clickOnElement(depart, action)

    gradTrip = graduation_trip()
    ### USE FOR BEACH VACATIONS
    sendLetters(gradTrip[0], depart)

    returnDate = selenium_driver.find_element_by_class('calenderReturnSpan')
    clickOnElement(returnDate, action)

    ### USE FOR BEACH VACATIONS
    sendLetters(gradTrip[1], returnDate)

    select = Select(selenium_driver.find_element_by_id('paxCount')) #Select 2 adults for price
    select.select_by_visible_text('2')
    selenium_driver.find_element_by_id('findFlightsSubmit').click()
    # clickOnElement(subButton, action)
    time.sleep(10)
    try:
        url = selenium_driver.current_url
        splitUrl = url.split('search-')
        splitUrl[1] = splitUrl[1][7:]
        url = splitUrl[0] + 'flexible-dates' + splitUrl[1]
        time.sleep(10)
        selenium_driver.get(url) #Change URL to flexible dates
        time.sleep(20)
        html = selenium_driver.page_source
        selenium_driver.close()
        soup = BeautifulSoup(html, "html.parser")
        cheapestFlight = soup.prettify()
        return cheapestFlight.split("\n")
    except IndexError:
        selenium_driver.close()
        return "Delta could not find the flight you were looking for"

def printDelta(cheapestFlight, cityGoingTo):
    departOptions = []
    startPoint = False
    '''
    This section splits the page source to get the table of flexible dates
    '''
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

    # This is to get the lowest fare from the departure options

    for information in flightInformation:
        if "LowestFare" in information:
            information.replace("LowestFare", "")
            lowestFairs.append(information)
    if lowestFairs == []:
        for information in flightInformation:
            print information

    for information in lowestFairs:
        print "DELTA Options: The lowest fair for " + cityGoingTo + " is: " + information
    if lowestFairs == []:
        print "Delta could not find the flight you were looking for: " + cityGoingTo
    print "\n"


def runDelta(city, airport_code):
    selenium_driver = webdriver.Chrome(executable_path=r'/Users/waldrich/PersonalPythonScripts/chromeDriver')
    selenium_driver.get('https://www.delta.com/flight-search/book-a-flight')
    try:
        printDelta(navigate_delta(airport_code, selenium_driver), city)
    except NoSuchElementException :
        selenium_driver.close()
        print "\nDELTA Unable to find: " + city
    except AttributeError:
        selenium_driver.close()
        print "\nDELTA Unable to find: " + city


# def unitedAirlines(airport_code, city):
#     selenium_driver = webdriver.Chrome(executable_path=r'/Users/waldrich/PersonalPythonScripts/chromeDriver')
#     selenium_driver.get('https://www.united.com/ual/en/us/')
#     depart = selenium_driver.find_element_by_id("Origin")
#     action = ActionChains(selenium_driver) #This will allow simulation of mouse movement
#     clickOnElement(depart, action)
#     sendLetters(slc, depart)
#     destination = selenium_driver.find_element_by_id("Destination")
#     clickOnElement(destination, action)
#     sendLetters(airport_code, destination)
#     # selenium_driver.find_element_by_id("flexDate").click()
#     departDate = selenium_driver.find_element_by_id("DepartDate")
#     clickOnElement(departDate, action)
#     sendLetters(graduation_trip_depart, departDate)
#     returnDate = selenium_driver.find_element_by_id("ReturnDate")
#     # clickOnElement(returnDate, action)
#     sendLetters(graduation_trip_return, returnDate)
#     selenium_driver.find_element_by_id("flightBookingSubmit").click()
#     time.sleep(20)
#     soup = BeautifulSoup(selenium_driver.page_source, "html.parser")
#     lowest = soup.find_all("span", {"class": "lowest-Economy"})
#
#     text = lowest[0].text
#     lowestPrice = text.split("price")
#     print("United Airlines lowest price for: " + city)
#     print (lowestPrice[1])
#
#     selenium_driver.close()

def clickOnElement(element, action):
    action.move_to_element(element)
    time.sleep(.5)
    action.click(element)

def sendLetters(word, element):
    for letter in word:
        element.send_keys(letter)
        time.sleep(.15)

'''
-----START OF PROGRAM-----
'''
for city in beachSpots.items():
    runDelta(city[0], city[1])
for city in interNationalCityList.items():
    runDelta(city[0], city[1])
