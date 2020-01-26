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

    '''
        To find single element

        find_element_by_id
        find_element_by_name
        find_element_by_xpath
        find_element_by_link_text
        find_element_by_partial_link_text
        find_element_by_tag_name
        find_element_by_class_name
        find_element_by_css_selector

        To find multiple elements (these methods will return a list):

        find_elements_by_name
        find_elements_by_xpath
        find_elements_by_link_text
        find_elements_by_partial_link_text
        find_elements_by_tag_name
        find_elements_by_class_name
        find_elements_by_css_selector
    '''
    def return_none(self, element):
        print("Unable to find: " + element)
        return None

    def find_element(self, element, type='id', x_path_object=None):
        try:
            if type == 'id':
                return self.driver.find_element_by_id(element)
            elif type == 'class':
                return self.driver.find_element_by_class_name(element)
            elif type == 'xpath':
                if x_path_object is not None:
                    return x_path_object.find_element_by_xpath(element)
                else:
                    return self.driver.find_element_by_xpath(element)
            elif type == 'name':
                return self.driver.find_element_by_name(element)
            elif type == 'link':
                return self.driver.find_element_by_link_text(element)
        except Exception as e:
            self.return_none(element)

    def find_element_in_list(self, element_list, type='id'):
        return_value = None
        for element in element_list:
            return_value = self.find_element(element, type)
            if return_value is not None:
                break
        return return_value

    def click_on_element(self, element):
        if element is None:
            raise Exception ("No Element to click on")
        try:
            self.action.move_to_element(element)
            time.sleep(.5)
            self.action.click(element)
            element.click()
        except Exception as e:
            print("Unable to click on: " + str(element))

    def click_on_js(self, element):
        if element is None:
            raise Exception ("No Element to click on")
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            print("Unable to click on JavaScript: " + str(element))

    def send_letters(self, word, element):
        for letter in word:
            element.send_keys(letter)
            time.sleep(.15)

    def enter_password(self, user_password_element, password_type):
        enter_pass = None
        if isinstance(user_password_element, list):
            enter_pass = self.find_element_in_list(user_password_element, password_type)
        else:
            enter_pass = self.find_element(user_password_element, password_type)

        if enter_pass is None:
            print("Unable to find user_password_element: " + user_password_element)
            print("Unable to log in")
            return None

        self.click_on_element(enter_pass)
        self.send_letters(self.password, enter_pass)
        return "Able to enter password"

    def login(self, user_name_element, user_password_element, submit_button_element,
              name_type='id', password_type='id', submit_type='id', submit_is_js=False, try_password=False):
        if not try_password:
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

            password = self.enter_password(user_password_element, password_type)
            if not password:
                try_password = True
        else:
            self.enter_password(user_password_element, password_type)
            try_password = False

        submit_button = None
        if isinstance(submit_button_element, list):
            submit_button = self.find_element_in_list(submit_button_element, submit_type)
        else:
            submit_button = self.find_element(submit_button_element, submit_type)
        if submit_is_js:
            self.click_on_js(submit_button)
        else:
            self.click_on_element(submit_button)

        if try_password:
            self.login(user_name_element, user_password_element, submit_button_element, name_type, password_type, submit_type, submit_is_js, try_password)

    def press_enter(self, element):
        element.send_keys(Keys.RETURN)

    def go_back(self):
        self.driver.execute_script("window.history.go(-1)")

    def get_password(self):
        return self.password

    def shut_down(self):
        self.driver.close()
