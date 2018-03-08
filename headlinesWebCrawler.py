import subprocess
from bs4 import BeautifulSoup

htmlNytimes = subprocess.check_output("curl -s \"https://www.nytimes.com\"", shell=True)
soup = BeautifulSoup(htmlNytimes, "html5lib")
nytimesHeadlines = soup.find_all('a')

nytimesText = []
headlineCount = 0
startHeadlines = False
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
        headlineCount += 1
print "\nNEW YOURK TIMES TOP 10 HEADLINES"
headlineCount = 1
for blah in nytimesText:
    print str(headlineCount) + ": " + blah
    headlineCount += 1

htmlAljazeera = subprocess.check_output("curl -s \"https://www.aljazeera.com/news/\"", shell=True)
soup = BeautifulSoup(htmlAljazeera, "html5lib")
topic = soup.find_all('a', {"class": "topics-sec-item-label"})
alHeadlines = soup.find_all('h2', {"class": "topics-sec-item-head"})

topicHeadlines = []
for x in topic:
    topicHeadlines.append(x.get_text())
print "\nALJAZERA OVERVIEW OF WORLD NEWS"
for place, headline in zip(topicHeadlines, alHeadlines):
    print place + ": ", headline.get_text()
