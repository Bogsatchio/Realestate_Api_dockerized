import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def initialize_search(driver, min, max, city):
    driver.get("https://www.otodom.pl/")

    time.sleep(2)
    cookies_button = driver.find_element(By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
    cookies_button.click()


    min_pow = driver.find_element(By.ID, value="areaMin")
    min_pow.send_keys(min)
    max_pow = driver.find_element(By.ID, value="areaMax")
    max_pow.send_keys(max)

    spot = driver.find_element(By.CLASS_NAME, value="css-1171ahe")
    spot.click()
    search_bar = driver.find_element(By.XPATH, value='//*[@id="location-picker-input"]')
    search_bar.send_keys(city)
    time.sleep(1)
    checkbox = driver.find_element(By.CLASS_NAME, value="css-104jm27")
    checkbox.click()
    time.sleep(1)
    search_button = driver.find_element(By.ID, value="search-form-submit")
    search_button.click()




def get_links_list(driver):
    time.sleep(3)
    links_list = []
    is_there_next_page = True
    while is_there_next_page:
        try:
            link_elements_list = driver.find_elements(By.CLASS_NAME, value="css-16vl3c1")
            #print("Elements")
            #print(link_elements_list)
            for element in link_elements_list:
                links_list.append(element.get_attribute("href"))
                #print(element.get_attribute("href"))
            print(len(links_list))

            # Find next page button and check if it is enabled
            lis = driver.find_elements(By.CLASS_NAME, value='css-gd4dj2')
            if len(lis) == 1 and lis[0].get_attribute("title") != "Go to next Page":
                break
            for x in lis:
                print(x.get_attribute("title"))
                print(x.get_attribute("aria-disabled"))
                if x.get_attribute("title") == "Go to next Page" and x.get_attribute("aria-disabled") != "true":
                    next_page_button = x
                    next_page_button.click()
                    time.sleep(2)
                elif x.get_attribute("title") == "Go to next Page" and x.get_attribute("aria-disabled") == "true":
                    is_there_next_page = False
                    break


        except:
            print("No more pages")
            is_there_next_page = False
    return links_list

def get_row_dict(driver, links_list, link, CITY_PHRASE, time_string, css_selectors_dict):
    row_dict = {}
    order_num = links_list.index(link)

    driver.get(link)
    time.sleep(1)

    row_dict["link"] = link
    row_dict["city"] = CITY_PHRASE
    try:
        row_dict["title"] = driver.find_element(By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/header/h1').text
    except:
        row_dict["title"] = None

    try:
        row_dict["price"] = driver.find_element(By.CLASS_NAME, value="css-t3wmkv").text
    except:
        row_dict["price"] = None

    try:
        row_dict["price_sqm"] = driver.find_element(By.CLASS_NAME, value='css-1h1l5lm').text
    except:
        row_dict["price_sqm"] = None

    try:
        row_dict["when_added_approx_days"] = driver.find_element(By.CLASS_NAME, value="css-1soi3e7").text
    except:
        row_dict["when_added_approx_days"] = None

    row_dict["scrap_time"] = time_string

    for key, value in css_selectors_dict.items():
        try:
            row_dict[key] = driver.find_element(By.CSS_SELECTOR, value=value).text
        except:
            row_dict[key] = None
    return row_dict, order_num



