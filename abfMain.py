from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import pandas as pd
import re
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import re
import textwrap
from bs4 import BeautifulSoup as BS



def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver


#constants/init
username = 'exchangebees'
password = 'ilovebees123'
URL = 'https://www.abfnet.org/search/newsearch.asp'

driver = webdriver.Chrome()

url = driver.command_executor._url
session_id = driver.session_id




print(url)
print(session_id)

driver.get(URL)

savedURL = 'http://127.0.0.1:62177'
savedSession = '40d186e7c790b5a39827a8c52ad88401'
time.sleep(60)

# username field
driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div/form/table/tbody/tr[1]/td/div[3]/table/tbody/tr[1]/td/input').send_keys(username)
time.sleep(2)
#password field
driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div/form/table/tbody/tr[1]/td/div[3]/table/tbody/tr[2]/td/input').send_keys(password)
#login button
time.sleep(1)
driver.find_element_by_class_name('formbutton').click()
sys.exit()
#
# driver = create_driver_session(savedSession, savedURL)
#
# time.sleep(1)


# 
# 
# url = driver.command_executor._url
# session_id = driver.session_id
# 
# 
# print(url)
# print(session_id)

# personLinks = driver.find_element_by_id("//*[contains(@id, 'MiniProfileLink')]")
# personSections = driver.find_element_by_id('GridPanel')
# print(personSections.get_attribute('innerHTML'))

#
# personSections = driver.find_elements_by_class_name('lineitem')
# print(personSections)
# hrefs = []
# for p in personSections:
#     print(p)
#     currHTML = p.get_attribute('innerHTML')
#     print(currHTML)
#     href = currHTML[list(find_all(currHTML, 'href='))[0] + 5 :]
#     href = str( currHTML[:list(find_all(href, '"')[1])].strip('"') )
#     print(href)
#     hrefs.append(href)
#
# sys.exit()

#MiniProfileLink_64628162
#MiniProfileLink_65974730
#SearchResultsGrid > tbody > tr:nth-child(1)






data = pd.DataFrame()
pageRange = np.arange(1,41)


for possibleID in np.arange(60000000, 70000000):
    newURL = f'https://www.abfnet.org/members/?id={possibleID}'
    driver.get(newURL)
    time.sleep(1)

    try:
        name = driver.find_element_by_id('SpTitleBar').text
        print(name)
        lastUpdated = driver.find_element_by_class_name('small').text
        type = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div/table[2]/tbody/tr/td/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/text()').text
        email = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div/table[2]/tbody/tr/td/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/a').text
        address = driver.find_element_by_id('tdAddress').text

        phones = driver.find_element_by_id('tdHomePhone').text
        phones = re.sub('[^0-9]', '', phones)
        if len(phones)>11:
            phones = textwrap.wrap(phones, 11)

        data = data.append({'personLink' : person,
                            'name' : name,
                            'lastUpdated' : lastUpdated,
                            'type' : type,
                            'email' : email,
                            'address' : email,
                            'phones' : phones}, ignore_index = True)


        print(data)
    except:
        print('failed')
        driver.back()


# try:
#     for page in pageRange:
#         for person in personLinks:
#             person.click()
#             time.sleep(1)
#             name = driver.find_element_by_id('SpTitleBar').text
#             lastUpdated = driver.find_element_by_class_name('small').text
#             type = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div/table[2]/tbody/tr/td/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/text()').text
#             email = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div/table[2]/tbody/tr/td/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/a').text
#             address = driver.find_element_by_id('tdAddress').text
# 
#             phones = driver.find_element_by_id('tdHomePhone').text
#             phones = re.sub('[^0-9]', '', phones)
#             if len(phones)>11:
#                 phones = textwrap.wrap(phones, 11)
# 
#             data = data.append({'personLink' : person,
#                                 'name' : name,
#                                 'lastUpdated' : lastUpdated,
#                                 'type' : type,
#                                 'email' : email,
#                                 'address' : email,
#                                 'phones' : phones}, ignore_index = True)
#             driver.back()
#             time.sleep(1)
#         if (page-10)<0:
#             driver.execute_script(f"__doPostBack('SearchResultsGrid$ct129$ct10{page}'.'')")
#         else:
#             driver.execute_script(f"__doPostBack('SearchResultsGrid$ct129$ct1{page}'.'')")
# except:
#     print('shit failed')
#     data.to_csv('abfData.csv')

