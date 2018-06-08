# PersonalPythonScripts

### NOTES:
- If you want to use just one of these scripts, you will have to copy and paste them into a python editor of some kind.
- You can clone the entire repo if you want to have all of these.
- These scripts are specific to my computer. You will have to change certain file paths for some of these projects.
- You may have to download certain dependancies for each of these as well. I recommend using pip or pip3. pip is used for python2
projects, and pip3 is used for python3. I have included which python version each of these were written for.

## cheapFlightsWebCrawler.py
Python2
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
Python2
This is a webscraper to grab only a few headlines from two news sources that I like looking at.
This program utilizes the shell and BeautifulSoup to run.

#### To Run headlinesWebCrawler.py
To run the program from the terminal, go to the folder that this program is in.
Once there run the following command
```
python headlinesWebCrawler.py
```


## concertsWebScraper.py
Python2
This is a webscraper to grab the concerts that are going on from SmithTix. Simple Scrape using curl and BeautifulSoup.

#### To Run concertsWebScraper.py
To run the program from the terminal, go to the folder that this program is in.
Once there run the following command
```
python concertsWebScraper.py
```

## costOfBillsThisMonth.py
Python2
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
Python3
This is a program created to quickly go through all of your github repos and push them to github. This allows for quicker transition through all repos. Allows for manual entry of commit message while showing all of the untracked or changed files. If just doing a quick backup without many changes can set an automatic update message for the commit message. This program will always pull from a repo before committing to the repo.

This program does the equivalent of the following terminal commands.
```
git status
git pull
git add --all
git commit -m 'your message'
git push
```

#### To run this program
This program uses gitpython, and if you want to use the progress bar, must download progressbar2
I have added this program to my .profile as an alias to increase efficiency. I then only have to type 'update' and this program will run. If you would rather run this without adding an alias, go to the folder that this program is in. Once there run the following command
```
python3 updateGit.py
```
If you would like adding it to your .profile enter in the following alias
```
alias update="python3 ~/PersonalPythonScripts/updateGit.py"
```
You can change 'update' to whatever you would like the alias to be
The path must be the correct path to the project. If you would like this to update as it is written, all repos must be in your
home folder. If they are not, you will have to modify the code
