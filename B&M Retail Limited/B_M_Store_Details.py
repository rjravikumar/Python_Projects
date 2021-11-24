import configparser
import time
from selenium import webdriver
import re
import pandas as pd

def remove_spaces(myString):
    removal_list = [' ', '\t', '\n']
    cont_list = []
    for cont in myString:
        for s in removal_list:
            cont_list.append(cont.replace(s, ''))
    return cont_list

config = configparser.ConfigParser(allow_no_value=True)
content = config.read('bmstores.ini')

list_links = []
driver = webdriver.Chrome('chromedriver.exe')
for zip_c in (config['zipcodes']['zipcode']).split(', '):
    print(zip_c)
    url = 'https://www.bmstores.co.uk/stores?location='+str(zip_c)
    driver.get(url)
    time.sleep(5)
    elems = driver.find_elements_by_css_selector(config['zipcode_link']['re_link'])
    links = [elem.get_attribute('href') for elem in elems]
    list_links.extend(links)

store_collection=[]
for link in list_links:
    print(link)
    link.rstrip()
    driver.get(link.rstrip())
    time.sleep(5)
    data_points=[]
    for key in config['regex']:
        if key != "hours":
            data = (driver.find_element_by_css_selector(config['regex'][key])).text
        else:
            store_hours = driver.find_elements_by_css_selector(config['regex'][key])
            hours = [elem.text for elem in store_hours]
            data = remove_spaces(hours)
        data_points.append(data)
    store_collection.append(data_points)

driver.quit()

df = pd.DataFrame(store_collection)
df.columns = list(dict(config.items('regex')).keys())
df.replace(r'\n',' ', regex=True)
df.to_excel('Store_Collection_Output.xlsx')