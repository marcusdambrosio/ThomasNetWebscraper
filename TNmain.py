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

#constants/init
username = 'marcus@exchangebees.com'
password = 'Marcus_2021!'
URL = 'https://www.thomasnet.com/'
data = {}
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
master = pd.DataFrame()


driver = webdriver.Chrome()
driver.get(URL)
time.sleep(3)
#login
login_button = driver.find_element_by_xpath('/html/body/div[3]/header/div/div/div/nav[2]/ul/li[4]/a/span').click()
time.sleep(1)
username_field = driver.find_element_by_xpath('/html/body/div[2]/div/section/div/div[2]/div/div[2]/div/form/div[1]/div/div/input').send_keys(username)
password_field = driver.find_element_by_xpath('/html/body/div[2]/div/section/div/div[2]/div/div[2]/div/form/div[2]/div/div/input').send_keys(password)
login_button2 = driver.find_element_by_xpath('/html/body/div[2]/div/section/div/div[2]/div/div[2]/div/form/div[3]/button').click()
time.sleep(3)

#back to home page
try:
    exit_button = driver.find_element_by_xpath('/html/body/div[4]/div/div/button').click()
    print('popup closed')
    time.sleep(1)
except:
    print('no popup found')
    time.sleep(1)


home_button = driver.find_element_by_xpath('/html/body/div[2]/div/main/div/div/nav/ol/li[1]/a').click()
time.sleep(1)


def find_all(string, sub):
    start = 0
    while True:
        start = string.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

for category in ['fertilizer']:
    data['category'] = category
    search_field = driver.find_element_by_xpath('/html/body/div[3]/section[1]/div/div/form/div/div/div[2]/input').send_keys(category)
    time.sleep(1)
    see_results_button = driver.find_element_by_xpath('/html/body/div[3]/section[1]/div/div/form/div/div/div[2]/div/a[9]/span').click()
    time.sleep(1)
    all_companies_button = driver.find_element_by_xpath('/html/body/div[3]/section[3]/div/div[1]/section/div/a')
    driver.execute_script("arguments[0].click();", all_companies_button)
    time.sleep(2)

    nav_buttons = driver.find_elements_by_class_name('page-link')
    nav_buttons = nav_buttons[2:len(nav_buttons)]
    nav_buttons = [c.get_attribute('href') for c in nav_buttons]

    for nav_button in nav_buttons:
        companies = driver.find_elements_by_class_name('profile-card__title')
        hrefs = []

        for company in companies:
            company_html = company.get_attribute('innerHTML')
            href = company_html[list(find_all(company_html, 'href'))[0] + 6:list(find_all(company_html, '"'))[1]]
            hrefs.append(href)

        for comp_number in range(len(companies)):
            failed_fields = []
            driver.get('https://www.thomasnet.com' + hrefs[comp_number])
            time.sleep(1)
            #general company info
            #small
            try:
                company = driver.find_element_by_xpath('/html/body/div[4]/section[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/h1')
                data['company_name'] = company.get_attribute('innerHTML')
            except:
                data['company_name'] = None
                failed_fields.append('company_name')

        #big
            if data['company_name'] == None:
                try:
                    company = driver.find_element_by_xpath('/html/body/div[4]/section[2]/div[1]/div/div/div[1]/div/div[2]/div[2]/h1/a[1]')
                    data['company_name'] = company.get_attribute('innerHTML')
                except:
                    data['company_name'] = None
                    failed_fields.append('company_name2')

            try:
                data['company_link'] = company.get_attribute('href')
            except:
                data['company_link'] = None
                failed_fields.append('company_links')


            try:
                company_general = driver.find_element_by_class_name('codetail').get_attribute('innerHTML')
                if 'Distributor' in company_general:
                    data['company_type'] = 'Distributor'
                elif 'Manufacturer' in company_general:
                    data['company_type'] = 'Manufacturer'
                else:
                    data['company_type'] = company_general
            except:
                data['company_type'] = None
                failed_fields.append('company_type')


            try:
                address_html = driver.find_element_by_class_name('addrline').get_attribute('innerHTML')
                data['address'] = address_html[:list(find_all(address_html, '|'))[0]]
            except:
                data['address'] = None
                failed_fields.append('address')


            try:
                phone_number_button = driver.find_element_by_class_name('phoneline__label').click()
                time.sleep(.5)
                data['phone_number'] = driver.find_element_by_xpath('/html/body/div[4]/section[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/p[3]/span').get_attribute('innerHTML')
            except:
                data['phone_number'] = None
                failed_fields.append('phone_number')

            if data['phone_number'] == None:
                try:
                    data['phone_number'] = driver.find_element_by_xpath('/html/body/div[4]/section[2]/div[1]/div/div/div[1]/div/div[2]/div[2]/p[3]/span').get_attribute('innerHTML')
                except:
                    data['phone_number'] = None
                    failed_fields.append('phone_number2')

            try:
                data['details'] = driver.find_element_by_id('copro_pdm').get_attribute('innerHTML')
            except:
                data['details'] = None
                failed_fields.append('details')

            try:
                driver.find_element_by_xpath('/html/body/div[4]/section[2]/div[1]/div/div/div[2]/div[1]/div/div[1]/ul/li[3]').click()
            except:
                None

            try:
                data['about'] = driver.find_element_by_id('copro_about').get_attribute('innerHTML')
            except:
                data['about'] = None
                failed_fields.append('about')


            try:
                prodserv = driver.find_element_by_id('copro_prodserv').get_attribute('innerHTML')
                prodserv_prodserv = prodserv[list(find_all(prodserv,'All Products / Services'))[0]:list(find_all(prodserv, 'View all products'))[0] - 20]
                starts = np.array(list(find_all(prodserv_prodserv, 'nofollow')))+10
                ends = list(find_all(prodserv_prodserv, '</a>'))
                equipment = []
                for i in range(len(starts)):
                    equipment.append(prodserv_prodserv[starts[i]:ends[i]])
                data['equipment'] =  equipment
            except:
                data['equipment'] = None
                failed_fields.append('equipment')

            # try:
            #     all_serv_link = driver.find_element_by_class_name('all').get_attribute('innerHTML')
            #     all_serv_link = all_serv_link[list(find_all(all_serv_link, 'href'))[0]+6:list(find_all(all_serv_link, 'position'))[0]+10]
            #     print(all_serv_link)
            #     driver.get('thomasnet.com/' + all_serv_link)
            #     time.sleep(1)
            #     all_equip = driver.find_elements_by_class_name('expand show').get_attribute('innerHTML')
            #     data['equipment'] = all_equip
            #     print(all_equip)
            #
            #     driver.back()
            #     time.sleep(1)
            # except:
            #     pass

            try:
                prodserv_service = prodserv[list(find_all(prodserv, 'Products / Services Offered'))[0]:list(find_all(prodserv,'All Products / Services'))[0]]
                starts = np.array(list(find_all(prodserv_service, 'cboxElement'))) + 13
                prodserv_service = prodserv_service[starts[0]:starts[-1]+30]
                ends = list(find_all(prodserv_service, '</a>'))
                starts = starts-starts[0]
                equip_categories = []
                for i in range(len(starts)):
                    equip_categories.append(prodserv_service[starts[i]:ends[i]])
                data['equip_categories'] = equip_categories
            except:
                data['equip_categories'] = None
                failed_fields.append('equip_categories')



            try:
                prodserv_brands = prodserv[list(find_all(prodserv, 'All Brands Carried'))[0]:]
                starts = np.array(list(find_all(prodserv_brands, '<li>'))) + 4
                ends  = list(find_all(prodserv_brands, '</li>'))
                brands = []
                for i in range(len(starts)):
                    brands.append(prodserv_brands[starts[i]:ends[i]])
                data['brands'] = brands
            except:
                data['brands'] = None
                failed_fields.append('brands')


            try:
                bus_details = driver.find_elements_by_class_name('bizdetail')
                bus_details = [c.get_attribute('innerHTML') for c in bus_details]
                detail_pairs = {}
                for det in bus_details:
                    try:
                        label = det[list(find_all(det, 'class="label"'))[0] + 14: list(find_all(det, ':</div>'))[0]]
                        detail = det[list(find_all(det, '<ul><li>'))[0] + 8:list(find_all(det, '</li></ul>'))[0]]
                        detail_pairs[label] = detail
                    except:
                        pass
                data['bus_details'] = detail_pairs
            except:
                data['bus_details'] = None
                failed_fields.append('bus_details')


            data['failed_fields'] = failed_fields
            master = master.append(data, ignore_index=True)
            driver.back()
            time.sleep(1)

        if nav_button == nav_button[-1]:
            continue
        driver.get(nav_button)
        time.sleep(2)

# master.to_csv('thomasnet_data.csv')

