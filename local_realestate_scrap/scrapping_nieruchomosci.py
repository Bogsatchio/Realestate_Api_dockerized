import time
import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

from utils.dicts import css_selectors_dict
from utils.helper_functions import get_links_list, get_row_dict, initialize_search

# city_phrase = "Plock"
# min_size = 30
# max_size = 100


def scrap_real_estate_data(city_phrase, min_size, max_size):
    # Get current time and format it as a string in "year-month-day-hour-minute" format
    current_time = datetime.now()
    time_string = current_time.strftime("%Y-%m-%d-%H-%M")

    # Keep Chrome browser open
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)

    initialize_search(driver=driver, min=min_size, max=max_size, city=city_phrase)

    time.sleep(2) # zmienić na Wait Until Load

    # Get hold of a links for the offers
    links_list = get_links_list(driver)
    while len(links_list) == 0:
        links_list = get_links_list(driver)

    data_dict = {}

    for link in links_list:
        row_dict, order_num = get_row_dict(driver, links_list, link, city_phrase, time_string, css_selectors_dict)
        print(row_dict)
        data_dict[order_num] = row_dict
    print(data_dict)

    # save as json file
    file_path = fr"C:\Users\ADMIN\Desktop\Pliki\Data_Stuff\Python\API_real_estate\data\{time_string}_{city_phrase}_min{min_size}_max{max_size}.json"
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False)

    file_path_2 = fr"C:\Users\ADMIN\Desktop\Pliki\Data_Stuff\Python\Prod_API_realestate\data\{time_string}_{city_phrase}_min{min_size}_max{max_size}.json"
    with open(file_path_2, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False)




