import subprocess, datetime
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

    print("\nALJAZERA world headlines\nhttps://www.aljazeera.com/news/\n")

    for topic, headline in zip(topic_headlines, alj_headlines):
        print (topic + ": ", headline.get_text())


def nytimes():
    nytimes_html = subprocess.check_output("curl -s \"https://www.nytimes.com/section/world\"", shell=True)
    soup = BeautifulSoup(nytimes_html, "html.parser")
    headline_date = {}

    for headline in soup.find_all('h2'):
        try:
            date = headline.find('a')['href']
            if date.startswith('/2019'):
                date = date.split("/")
                date = '/'.join(date[:4])
                headline_date[headline.text] = date[1:]
        except:
            headline_date[headline.text] = str(datetime.datetime.now()).split(" ")[0]

    print('\nNYTIMES world headlines\nhttps://www.nytimes.com/section/world\n')
    for headline, date in headline_date.items():
        print(date + "\t" + headline)

if __name__ == '__main__':
    nytimes()
    alj()
