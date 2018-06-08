# PersonalPythonScripts

## cheapFlightsWebCrawler.py
This is a webcrawler that will crawl multiple websites for cheap flight ticket prices.
This program utilizes Selenium and BeautifulSoup to crawl. I used Selenium to ensure that I could interact with JavaScript items. Originally this was run with multiThreading, I scrapped that due to too much traffic on their websites and trying to be polite in my web crawling.

As of 3-8-18 current run time for 17 international flights and 12 national flights is [real	17m31.528s]. Not all 29 flights are guaranteed to have actual flights. This is also only testing one airline for international flights, and one airline for national flights.

#### To Run cheapFlightsWebCrawler.py
You must have a selenium driver installed. I used the Chrome driver to complete it. Once that is downloaded, make sure you change the path in which the driver is pointed to.

To run the program from the terminal, go to the folder that this program is in.
Once there run the following command
```
python cheapFlightsWebCrawler.py
```

## headlinesWebCrawler.py
This is a webscraper to grab only a few headlines from two news sources that I like looking at.
This program utilizes the shell and BeautifulSoup to run.

#### To Run headlinesWebCrawler.py
To run the program from the terminal, go to the folder that this program is in.
Once there run the following command
```
python headlinesWebCrawler.py
```


## concertsWebScraper.py
This is a webscraper to grab the concerts that are going on from SmithTix. Simple Scrape using curl and BeautifulSoup.

#### To Run concertsWebScraper.py
To run the program from the terminal, go to the folder that this program is in.
Once there run the following command
```
python concertsWebScraper.py
```

## costOfBillsThisMonth.py
This is a webcrawler that will grab the current amount due for a couple of my personal bills.
This utilizes Selenium and BeautifulSoup to grab the content.
This is utilizes multiprocessing for speed to get the content.

#### To Run costOfBillsThisMonth.py
To run the program from the terminal, go to the folder that this program is in.
Once there run the following command
```
python costOfBillsThisMonth.py
```
You will need to fill out your username, password, email, and one additional password

## updateGit.py
This is a program created to quickly go through all of your github repos and push them to github. This allows for quicker transition through all repos. Allows for manual entry of commit message while showing all of the untracked or changed files. If just doing a quick backup without many changes can set an automatic update message for the commit message. This program also allows an option to pull from a repo before you commit. 

This program does the equivalent of the following terminal commands.
```
git status
git pull
git add --all
git commit -m 'your message'
git push
```

#### To run this program
I have added this program to my .profile as an alias to increase efficiency. I then only have to type 'update' and this program will run. If you would rather run this without adding an alias, go to the folder that this program is in. Once there run the following command
```
python updateGit.py
```
