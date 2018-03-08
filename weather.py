import subprocess, sys, re

grepDegrees = " | grep '<p class=\"myforecast-current-lrg\">'"

def getForcast(city):
    #send 0 just incase getAll
    url = getCityUrl(city, 0)

    #<div id="detailed-forecast" class="panel panel-default">
        #<div class="panel-body" id="detailed-forecast-body">
        ####Today
            #<div class="row row-odd row-forecast">
                #<div class="col-sm-10 forecast-text">###TEXT HERE
        ####Tonight
            #<div class="row row-even row-forecast">
                #<div class="col-sm-10 forecast-text">###TEXT HERE
    print(url[1])

#degree is a boolean value if true it is degrees we are trying to find
#else it is to get a forecast
def getAll(degree):
    listOfCities = ["slc","brigham","richmond"]
    if degree:
        for val in listOfCities:
            getDegreesOnly(val)
    else:
        print("In getAll")
    exit(0)

#get url and city name
#easy to add to if want to
def getCityUrl(city, degree):
    url = '\"https://forecast.weather.gov/MapClick.php?'
    #This is a dictionary (aka hashmap) the key is a string, the value is a list
    #the first value in the list is the url, the second value is the name of the city
    d = {'slc': [url + 'lat=40.7603&lon=-111.8882#.WpWFFBPwaAw\"', "Salt Lake City "],
         'brigham': [url + 'lat=41.5126&lon=-112.0157#.WpW9SxPwaAw\"', "Brigham City "],
         'richmond': [url + 'lat=41.9222&lon=-111.8144#.WpW93RPwaAw\"', 'Richmond ']}
    #get the list based off of the city
    ret = d.get(city)
    #if the city exists in the dictionary return the list
    #if the city does NOT exist, get all of the cities
    if ret != None:
        return ret

    getAll(degree)

def printDegreeinfo(city, grep, cityName):
    #first argument in findall is to find all the digits
    #second argument is to call curl and grep in the shell
    curlAndGrep = subprocess.check_output("curl -s " + city + grep, shell=True)
    getWebpageWithGrep = re.findall('\d+', curlAndGrep)
    degree = ''
    for val in getWebpageWithGrep:
        degree += val
    print(cityName + degree + " degrees Farenheit")

def getDegreesOnly(city):
    #1 is true boolean value, we use this just incase we want to get all of the cities
    url = getCityUrl(city, 1)
    printDegreeinfo(url[0], grepDegrees, url[1])



####****START OF PROGRAM****####
if len(sys.argv) < 2:
    print('Please enter a city. If you would like the forecast enter something after the city. eg. \'slc\' \'a\'')
    exit(0)

city = sys.argv[1]

if len(sys.argv) >= 3:
    getForcast(city)
else:
    getDegreesOnly(city)
