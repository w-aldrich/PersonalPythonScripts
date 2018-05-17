# PersonalPythonScripts

## cheapFlightsWebCrawler.py
This is a webcrawler that will crawl multiple websites for cheap flight ticket prices.
This program utilizes Selenium and BeautifulSoup to crawl. I used Selenium to ensure that I could interact with JavaScript items. Originally this was run with multiThreading, I scrapped that due to too much traffic on their websites and trying to be polite in my web crawling.

As of 3-8-18 current run time for 17 international flights and 12 national flights is [real	17m31.528s]. Not all 29 flights are guaranteed to have actual flights. This is also only testing one airline for international flights, and one airline for national flights.

### To Run cheapFlightsWebCrawler.py
You must have a selenium driver installed. I used the Chrome driver to complete it. Once that is downloaded, make sure you change the path in which the driver is pointed to.

To run the program from the terminal, go to the folder that this program is in.
Once there run the following command
```
python cheapFlightsWebCrawler.py
```

## headlinesWebCrawler.py
This is a webscraper to grab only a few headlines from two news sources that I like looking at.
This program utilizes the shell and BeautifulSoup to run.

### To Run headlinesWebCrawler.py
To run the program from the terminal, go to the folder that this program is in.
Once there run the following command
```
python headlinesWebCrawler.py
```


## concertsWebScraper.py
This is a webscraper to grab the concerts that are going on from SmithTix. Simple Scrape using curl and BeautifulSoup.

### To Run concertsWebScraper.py
To run the program from the terminal, go to the folder that this program is in.
Once there run the following command
```
python concertsWebScraper.py
```

## costOfBillsThisMonth.py
This is a webcrawler that will grab the current amount due for a couple of my personal bills.
This utilizes Selenium and BeautifulSoup to grab the content.
This is utilizes multiprocessing for speed to get the content.

### To Run costOfBillsThisMonth.py
To run the program from the terminal, go to the folder that this program is in.
Once there run the following command
```
python costOfBillsThisMonth.py
```
You will need to fill out your username, password, email, and one additional password
