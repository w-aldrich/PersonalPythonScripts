import subprocess
from bs4 import BeautifulSoup

'''
This program will scrape nytimes.com and aljazeera.com
for the headlines I care about looking at
'''

# Using curl and beautiful soup for both of these sites

# NYTIMES
htmlNytimes = subprocess.check_output("curl -s \"https://www.nytimes.com\"", shell=True)
soup = BeautifulSoup(htmlNytimes, "html.parser")
nytimesHeadlines = soup.find_all('a')

nytimesText = []
headlineCount = 0
startHeadlines = False
# loop through all 'a' tags remove unneeded white space and grab the correct headlines
for headline in nytimesHeadlines:
    headline = headline.get_text().replace("\n", "").replace("\r", "").replace("\t", "")
    headline = headline.encode('ascii',errors='ignore')
    if 'T Magazine' in headline:
        startHeadlines = True
        continue
    if startHeadlines == True:
        if 'Comments' in headline or 'Subscribe' in headline or headline == '':
            continue
        if "Editorial:" in headline or headlineCount == 10:
            break
        nytimesText.append(headline)
        # headlineCount += 1

print "\nNEW YOURK TIMES TOP 10 HEADLINES"

for blah in nytimesText:
    headlineCount += 1
    print str(headlineCount) + ": " + blah
    if headlineCount == 10:
        break



# ALJAZEERA
htmlAljazeera = subprocess.check_output("curl -s \"https://www.aljazeera.com/news/\"", shell=True)
soup = BeautifulSoup(htmlAljazeera, "html.parser")

# Use soup to find all of the 'a' tags, these contain where the stories are from
topic = soup.find_all('a', {"class": "topics-sec-item-label"})
# Use soup to find all the 'h2' tags, these contain the actual headline
alHeadlines = soup.find_all('h2', {"class": "topics-sec-item-head"})

topicHeadlines = []
for x in topic:
    topicHeadlines.append(x.get_text())

print "\nALJAZERA OVERVIEW OF WORLD NEWS"

for place, headline in zip(topicHeadlines, alHeadlines):
    print place + ": ", headline.get_text()
