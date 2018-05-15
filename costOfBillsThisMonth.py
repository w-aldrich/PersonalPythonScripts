# import mechanize, getpass
# from mechanize import Browser
from bs4 import BeautifulSoup
import time, re, getpass
from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

'''
This program will log into:
Rocky Mountain Power
CenturyLink
Quest Star Gas
and Precept Properties.
It will then grab how much is owed to each company and print it in the console
'''

user = getpass.getpass("User: ")
password = getpass.getpass()
email = getpass.getpass("Email: ")
internetpass = getpass.getpass("InternetPassword: ") #For Century Link


'''
This section is for Rocky Mountain Power
'''
def powerBill():
    seleniumDriver = webdriver.Chrome(executable_path=r'/Users/waldrich/python/chromeDriver')
    seleniumDriver.get('https://www.rockymountainpower.net/index.html')
    seleniumDriver.find_element_by_id('nav-account-anchor').click()
    usernameSel = seleniumDriver.find_element_by_id('cams_cb_username')
    usernameSel.send_keys(user)
    passwordSel = seleniumDriver.find_element_by_id('cams_cb_password')
    passwordSel.send_keys(password)
    seleniumDriver.find_element_by_id("loginButton").click()
    time.sleep(8)
    html = seleniumDriver.page_source
    seleniumDriver.close()
    soup = BeautifulSoup(html, "html5lib")
    soup = soup.prettify()
    elements = soup.split("\n")
    found = False
    for blah in elements:
        if found:
            print "Rocky Mountain Power Bill: " + blah
            break
        if "due last" in blah:
            found = True
'''
This section is for Quest Star Gas
'''
def gasBill():
    seleniumDriver = webdriver.Chrome(executable_path=r'/Users/waldrich/python/chromeDriver')
    seleniumDriver.get('https://www.questargas.com/WSS/servlet/CMMainControllerServlet?action=CMSignInAction')
    usernameSel = seleniumDriver.find_element_by_name('UserID')
    usernameSel.send_keys(user)
    passwordSel = seleniumDriver.find_element_by_xpath('/html/body/div/table[2]/tbody/tr/td[2]/table/tbody/tr/td/form/table/tbody/tr[8]/td/table/tbody/tr[4]/td[2]/input')
    passwordSel.send_keys(password)
    seleniumDriver.find_element_by_id("submit").click()
    # time.sleep(7)
    html = seleniumDriver.page_source
    seleniumDriver.close()
    soup = BeautifulSoup(html, "html5lib")
    soup = soup.prettify()
    elements = soup.split("\n")
    found = False
    count = 0
    for blah in elements:
        if found:
            if count < 4:
                count = count + 1
                continue
            else:
                print "Queststar Gas Bill: " + blah
                break
        if "Current Amount Due" in blah:
            found = True

'''
This section is for Century Link
'''
def internetBill():
    seleniumDriver = webdriver.Chrome(executable_path=r'/Users/waldrich/python/chromeDriver')
    seleniumDriver.get('https://eam.centurylink.com/eam/login.do')
    usernameSel = seleniumDriver.find_element_by_id('USER')
    usernameSel.send_keys(user)
    passwordSel = seleniumDriver.find_element_by_id('PASSWORD')
    passwordSel.send_keys(internetpass)
    seleniumDriver.find_element_by_id("loginButton").click()
    # time.sleep(5)
    html = seleniumDriver.page_source
    seleniumDriver.close()
    soup = BeautifulSoup(html, "html5lib")
    mydivs = soup.find_all("div", class_='myBill__balance_due_large')
    moneyList = []
    for blah in mydivs:
        hey = str(blah.text)
        moneyList.append(re.sub('[\s+]', '', hey))

    s = moneyList[0]
    s = s[:len(s)-2] + '.' + s[len(s)-2:]
    print "CeunturyLink Bill: \t\t\t" + s

'''
This section is for Precept Properties
'''
def rentBill():
    seleniumDriver = webdriver.Chrome(executable_path=r'/Users/waldrich/python/chromeDriver')
    seleniumDriver.get('https://preceptproperty.managebuilding.com/Resident/PublicPages/Home.aspx?ReturnUrl=%2fResident')
    usernameSel = seleniumDriver.find_element_by_id('_ctl0_contentPlaceHolderBody_ucResidentLogin_txtUserName')
    usernameSel.send_keys(email)
    passwordSel = seleniumDriver.find_element_by_id('_ctl0_contentPlaceHolderBody_ucResidentLogin_txtPassword')
    passwordSel.send_keys(password)
    seleniumDriver.find_element_by_id("_ctl0_contentPlaceHolderBody_ucResidentLogin_btnLogIn").click()
    time.sleep(3)
    html = seleniumDriver.page_source
    seleniumDriver.close()
    soup = BeautifulSoup(html, "html5lib")
    soup = soup.prettify()
    elements = soup.split("\n")
    found = False
    for blah in elements:
        if found:
            print "Rent Bill: \t\t\t" + blah
            break
        if "payment-current-amount ng-binding" in blah:
            found = True

power = Process(target=powerBill, args=())
gas = Process(target=gasBill, args=())
internet = Process(target=internetBill, args=())
rent = Process(target=rentBill, args=())
gas.start()
power.start()
internet.start()
rent.start()
gas.join()
power.join()
internet.join()
rent.join()
