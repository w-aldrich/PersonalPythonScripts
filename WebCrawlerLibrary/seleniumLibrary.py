# This is a high level library to interact with selenium
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

class SeleniumInteraction:

    def __init__(self, website, user_name=None, password=None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(executable_path=r'/Users/waldrich/PersonalPythonScripts/chromeDriver',
                                       chrome_options=chrome_options)
        self.driver.get(website)
        self.action = ActionChains(self.driver) #This will allow simulation of mouse movement
        self.user_name = user_name
        self.password = password

    def find_element(self, element, type='id', x_path_object=None):
        if type == 'id':
            try:
                return self.driver.find_element_by_id(element)
            except:
                print("Unable to find: " + element)
                return None
        elif type == 'class':
            try:
                return self.driver.find_element_by_class_name(element)
            except:
                print("Unable to find: " + element)
                return None
        elif type == 'xpath':
            if x_path_object is not None:
                return x_path_object.find_element_by_xpath(element)
            try:
                return self.driver.find_element_by_xpath(element)
            except:
                print("Unable to find: " + element)
                return None
        elif type == 'name':
            try:
                return self.driver.find_element_by_name(element)
            except:
                print("Unable to find: " + element)
                return None

    def find_element_in_list(self, element_list, type='id'):
        return_value = None
        for element in element_list:
            return_value = self.find_element(element, type)
            if return_value is not None:
                break
        return return_value

    def click_on_element(self, element):
        try:
            self.action.move_to_element(element)
            time.sleep(.5)
            self.action.click(element)
            element.click()
        except:
            print("Unable to click on: " + str(element))

    def click_on_js(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except:
            print("Unable to click on JavaScript: " + str(element))

    def send_letters(self, word, element):
        for letter in word:
            element.send_keys(letter)
            time.sleep(.15)

    def login(self, user_name_element, user_password_element, submit_button_element,
              name_type='id', password_type='id', submit_type='id', submit_is_js=False):

        enter_user_name = None

        if isinstance(user_name_element, list):
            enter_user_name = self.find_element_in_list(user_name_element, name_type)
        else:
            enter_user_name = self.find_element(user_name_element, name_type)

        if enter_user_name is None:
            print("Unable to find user_name_element: " + user_name_element)
            print("Unable to log in")
            return None

        self.click_on_element(enter_user_name)
        self.send_letters(self.user_name, enter_user_name)

        enter_password = None
        if isinstance(user_password_element, list):
            enter_password = self.find_element_in_list(user_password_element, password_type)
        else:
            enter_password = self.find_element(user_password_element, password_type)

        if enter_password is None:
            print("Unable to find user_password_element: " + user_password_element)
            print("Unable to log in")
            return None

        self.click_on_element(enter_password)
        self.send_letters(self.password, enter_password)

        submit_button = None
        if isinstance(submit_button_element, list):
            submit_button = self.find_element_in_list(submit_button_element, submit_type)
        else:
            submit_button = self.find_element(submit_button_element)
        if submit_is_js:
            self.click_on_js(submit_button)
        else:
            self.click_on_element(submit_button, submit_type)

    def press_enter(self, element):
        element.send_keys(Keys.RETURN)

    def go_back(self):
        self.driver.execute_script("window.history.go(-1)")

    def get_password(self):
        return self.password

    def shut_down(self):
        self.driver.close()
