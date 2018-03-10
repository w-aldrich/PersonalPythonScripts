# PersonalPythonScripts

## cheapFlightsWebCrawler.py
This is a webcrawler that will crawl multiple websites for cheap flight ticket prices.
This program utilizes Selenium and BeautifulSoup to crawl. I used Selenium to ensure that I could interact with JavaScript items. Originally this was run with multiThreading, I scrapped that due to too much traffic on their websites and trying to be polite in my web crawling. 

As of 3-8-18 current run time for 17 international flights and 12 national flights is [real	17m31.528s]. Not all 29 flights are guaranteed to have actual flights. This is also only testing one airline for international flights, and one airline for national flights.


## headlinesWebCrawler.py
This is a webcrawler to grab only a few headlines from two news sources that I like looking at.
This program utilizes the shell and BeautifulSoup to run. 

## concertsWebScraper.py
This is a webscraper to grab the concerts that are going on in Salt Lake City. Simple Scrape using curl and BeautifulSoup.
