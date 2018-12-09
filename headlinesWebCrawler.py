import subprocess
from bs4 import BeautifulSoup

'''
This program will scrape nytimes.com and aljazeera.com
for the headlines I care about looking at
'''
def alj():
    # ALJAZEERA
    html_alj = subprocess.check_output("curl -s \"https://www.aljazeera.com/news/\"", shell=True)
    soup = BeautifulSoup(html_alj, "html.parser")

    # Use soup to find all of the 'a' tags, these contain where the stories are from
    topic = soup.find_all('a', {"class": "topics-sec-item-label"})
    # Use soup to find all the 'h2' tags, these contain the actual headline
    alj_headlines = soup.find_all('h2', {"class": "topics-sec-item-head"})

    topic_headlines = []
    for x in topic:
        topic_headlines.append(x.get_text())

    print("\nALJAZERA OVERVIEW OF WORLD NEWS")

    for place, headline in zip(topic_headlines, alj_headlines):
        print place + ": ", headline.get_text()


# Need to fix NYTIMES
def nytimes():
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
            if 'Comments' in headline or 'Subscribe' in headline or headline == '' or "Real Estate" in headline:
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


if __name__ == '__main__':
    nytimes()
    alj()
