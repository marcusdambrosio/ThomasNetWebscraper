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
from csv_combiner import combine_csvs

def find_all(string, sub):
    start = 0
    while True:
        start = string.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)




'''DEFINE SEARCH CATEGORIES HERE'''
# categories = ['fertilizer']


def TN_scrape(categories, csvCounter, companyStart = False):
    # constants/init
    username = 'marcus@exchangebees.com'
    password = 'Marcus_2021!'
    URL = 'https://www.thomasnet.com/'
    data = {}
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    full_master = pd.DataFrame()

    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(3)
    # login
    login_button = driver.find_element_by_xpath('/html/body/div[3]/header/div/div/div/nav[2]/ul/li[4]/a/span').click()
    time.sleep(1)
    username_field = driver.find_element_by_xpath(
        '/html/body/div[2]/div/section/div/div[2]/div/div[2]/div/form/div[1]/div/div/input').send_keys(username)
    password_field = driver.find_element_by_xpath(
        '/html/body/div[2]/div/section/div/div[2]/div/div[2]/div/form/div[2]/div/div/input').send_keys(password)
    login_button2 = driver.find_element_by_xpath(
        '/html/body/div[2]/div/section/div/div[2]/div/div[2]/div/form/div[3]/button').click()
    time.sleep(3)

    # back to home page
    popup = True

    while popup == True:
        try:
            exit_button = driver.find_element_by_xpath('/html/body/div[4]/div/div/button').click()
            print('popup closed')
            popup = False
            time.sleep(2)
        except:
            print('no popup found')
            time.sleep(1)

        home_button = driver.find_element_by_xpath('/html/body/div[2]/div/main/div/div/nav/ol/li[1]/a').click()
        time.sleep(1)


    try:
        for category in categories:
            master = pd.DataFrame()
            data['master_category'] = category
            search_field = driver.find_element_by_xpath('/html/body/div[3]/section[1]/div/div/form/div/div/div[2]/input').send_keys(category)
            time.sleep(1)
            see_results_button = driver.find_element_by_xpath('/html/body/div[3]/section[1]/div/div/form/div/div/div[2]/div/a[9]/span').click()
            time.sleep(1)

            driver.find_element_by_class_name('search-result__view-all').click()
            # driver.execute_script("arguments[0].click();", all_companies_button)
            time.sleep(1)
            category_buttons = driver.find_elements_by_class_name('title')
            category_reset = driver.current_url
            categories = [c.text for c in category_buttons]
            company_counter = 0
            category_hrefs = []



            # if companyStart:
            #     category_buttons = category_buttons[category_buttons.index(companyStart['categoryButton'])]




            for category_button in category_buttons:
                category_html = category_button.get_attribute('innerHTML')
                current_href = category_html[list(find_all(category_html, 'href'))[0] + 6:list(find_all(category_html, '"'))[1]]
                current_href = current_href.replace('amp;', '')
                category_hrefs.append(current_href)

            for i, current_href in enumerate(category_hrefs):
                current_category = categories[i]
                # category_html = category_button.get_attribute('innerHTML')
                # current_href = category_html[list(find_all(category_html, 'href'))[0] + 6:list(find_all(category_html, '"'))[1]]
                # current_href = current_href.replace('amp;', '')
                driver.get('https://www.thomasnet.com' + current_href)
                time.sleep(1)
                nav_buttons = driver.find_elements_by_class_name('page-link')
                nav_buttons = nav_buttons[2:len(nav_buttons)]
                nav_buttons = [c.get_attribute('href') for c in nav_buttons]

                #
                #
                # if companyStart:
                #     nav_buttons = nav_buttons[nav_buttons.index(companyStart['navButton']):]





                if len(nav_buttons) == 0:
                    nav_buttons = [0,0,0,0]
                for nav_button in nav_buttons:
                    time.sleep(1)
                    print('hi')
                    companies = driver.find_elements_by_class_name('profile-card__title')


                    #
                    # if companyStart:
                    #     companies = companies[companies.index(companyStart['company']):]


                    company_names = [c.text for c in companies]
                    haveCompanies = []
                    for companyName in company_names:
                        if companyName in currCompanies.tolist():
                            haveCompanies.append(True)
                        else:
                            haveCompanies.append(False)
                    if False not in haveCompanies:
                        print(f'have all of {company_names}')
                        continue
                    else:
                        companyList = [c for c in companies]
                        companies = companyList[haveCompanies.index(False)]
                        if not type(companies) == list:
                            companies = [companies]


                    company_names = [c.text for c in companies]
                    hrefs = []
                    try:
                        for company in companies:
                            data['master_category'] = category
                            data['specific_category'] = current_category
                            company_html = company.get_attribute('innerHTML')
                            href = company_html[list(find_all(company_html, 'href'))[0] + 6:list(find_all(company_html, '"'))[1]]
                            href = href.replace('amp;', '')
                            hrefs.append(href)

                        for comp_number in range(len(companies)):
                            failed_fields = []
                            driver.get('https://www.thomasnet.com' + hrefs[comp_number])
                            time.sleep(1)
                            #general company info
                            #small
                            try:
                                data['company_name'] = company_names[comp_number]
                            except:
                                print('SHITBROKEN')

                        #     try:
                        #         company = driver.find_element_by_xpath('/html/body/div[4]/section[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/h1')
                        #         data['company_name'] = company.get_attribute('innerHTML')
                        #     except:
                        #         data['company_name'] = None
                        #         failed_fields.append('company_name')
                        #
                        # #big
                        #     if data['company_name'] == None:
                        #         try:
                        #             company = driver.find_element_by_xpath('/html/body/div[4]/section[2]/div[1]/div/div/div[1]/div/div[2]/div[2]/h1/a[1]')
                        #             data['company_name'] = company.get_attribute('innerHTML')
                        #         except:
                        #             data['company_name'] = None
                        #             failed_fields.append('company_name2')
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

                            # try:
                            #     data['company_link'] = company.get_attribute('href')
                            # except:
                            #     data['company_link'] = None
                            #     failed_fields.append('company_links')

                            try:
                                data['company_link'] = company_general[list(find_all(company_general, 'href'))[0] + 6:list(find_all(company_general, '"'))[1]]
                            except:
                                data['company_link'] = None
                                failed_fields.append('company_link')

                            try:
                                address_html = driver.find_element_by_class_name('addrline').get_attribute('innerHTML')
                                data['address'] = driver.find_element_by_class_name('addrline').text
                            except:
                                data['address'] = None
                                failed_fields.append('address')

                            try:
                                phone_number_button = driver.find_element_by_class_name('phoneline__label').click()
                                time.sleep(.5)
                                codetail = driver.find_element_by_class_name('codetail').get_attribute('innerHTML')
                                phone_start = list(find_all(codetail, '<span class="">'))[0] + 15
                                data['phone_number'] = codetail[phone_start:phone_start+12]
                            except:
                                data['phone_number'] = None
                                failed_fields.append('phone_number')

                            try:
                                data['details'] = driver.find_element_by_id('copro_pdm').text
                            except:
                                data['details'] = None
                                failed_fields.append('details')

                            try:
                                time.sleep(.5)
                                driver.find_element_by_class_name('link').click()
                            except:
                                None


                            try:
                                data['about'] = driver.find_element_by_id('copro_about').text
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
                            full_master = full_master.append(data,ignore_index = True)
                            time.sleep(1)
                    except:
                        print(f'{company} failed')
                    nav_buttons = driver.find_elements_by_class_name('page-link')
                    nav_buttons = nav_buttons[2:len(nav_buttons)]
                    nav_buttons = [c.get_attribute('href') for c in nav_buttons]

                    if len(nav_buttons) == 0:
                        nav_buttons = [0, 0, 0, 0]

                    if nav_button == nav_buttons[-1]:
                        continue
                    driver.get(nav_button)
                    time.sleep(2)
                driver.back()
            master.to_csv(f'{category}_data/{category}_data_partial{csvCounter}.csv')
            return 1

    except:
        print("Unexpected error:", sys.exc_info()[0])
        master.to_csv(f'{category}_data/{category}_data_partial{csvCounter}.csv')

        # if not companyStart:
        #     master.to_csv(f'{category}_data_partial3.csv')
        # else:
        #     master.to_csv(f'{category}_data_partial{3+companyStart["count"]}.csv')
        #
        # return {'categoryButton': category_button,
        #         'navButton': nav_button,
        #         'company': company,
        #         'count': 1 if not companyStart else companyStart['count'] + 1}


check = False
csvCounter = 0
while check != 1:
    try:
        currData = pd.read_csv('fertilizer_data/MASTER.csv')
        currCompanies = currData['company_name']
    except:
    check = TN_scrape(['fertilizer'], csvCounter = csvCounter, companyStart = check)
    combine_csvs('fertilizer_data')
    time.sleep(1)
    csvCounter += 1
