from selenium import webdriver
from selenium.webdriver.common.by import By
import ctypes
import pandas as pd
import time
import statistics
import pymsgbox
import os.path

def create_number_from_price_str(price_str: str) -> int:
    try:
        return int(price_str.replace(",", "").replace(" ₪", ""))
    except ValueError:
        return None


def convert_lists_of_webriver_to_text(webdriver_list) -> list:
    new_list_of_text = []
    for item in webdriver_list:
        new_list_of_text.append(item.text)
    return new_list_of_text


def calculate_selenium_price_list_mean(webdriver_list) -> int:
    price_text_list = convert_lists_of_webriver_to_text(webdriver_list)
    price_list_int =[]
    for item in price_text_list:
        price_list_int.append(create_number_from_price_str(item))

    price_list_int = [x for x in price_list_int if x is not None]
    return int(statistics.mean(price_list_int))


driver = webdriver.Firefox()
# tests
# url = "https://www.yad2.co.il/realestate/forsale?topArea=101&area=15&city=6500&neighborhood=666&propertyGroup=apartments&property=1&rooms=4-4&floor=1-2"
# correct
url = "https://www.yad2.co.il/realestate/forsale"

driver.get(url)

text = 'Press OK after narrowing down search results.' \
       'Try to narrow to a very specific asset type to improve ROI accuracy'
title = 'Pop Up'

answer = ctypes.windll.user32.MessageBoxExW(0, text, title, 0x40000)

new_url = driver.current_url
print(type(new_url))

assets_prices = driver.find_elements(By.CSS_SELECTOR, "div.feeditem div.left_col .price")
# print(assets_prices[0].text)

assets_mean_price = calculate_selenium_price_list_mean(assets_prices)


new_url_for_rent = new_url.replace("forsale", "rent")

driver.get(new_url_for_rent)

rent_prices = driver.find_elements(By.CSS_SELECTOR, "div.feeditem div.left_col .price")
search_description = driver.find_element(By.CSS_SELECTOR, "div.feed_header_container div.feed_header h1")
search_description_text = search_description.text
print(search_description_text)
# print(rent_price)

rent_mean_price = calculate_selenium_price_list_mean(rent_prices)
calculate_roi = round(rent_mean_price*11/assets_mean_price*100, 2)



print("mean asset price:", "{:,}".format(assets_mean_price), "₪")
print("mean rent price:", "{:,}".format(rent_mean_price), "₪")
print(f"The ROI for the assets is: {calculate_roi}%")

# dict_of_title = {
#     "description in hebrew": ["description in hebrew"],
#     "assets mean price": ["assets mean price"],
#     "rent mean price": ["rent mean price"],
#     "ROI": ["ROI"]
# }
#
# df = pd.DataFrame.from_dict(dict_of_title)
#
# df.to_csv('my_csv.csv', encoding="utf-8-sig", index=False)

dict_to_add = {
    "description in hebrew": [search_description_text],
    "assets mean price": ["{:,}".format(assets_mean_price)],
    "rent mean price": ["{:,}".format(rent_mean_price)],
    "ROI": [str(calculate_roi)+"%"]
}

print(dict_to_add)

df = pd.DataFrame.from_dict(dict_to_add)

file_exists = os.path.isfile("my_csv.csv")

if file_exists:
    df.to_csv('my_csv.csv', mode='a', header=False, encoding="utf-8-sig", index=False)
else:
    df.to_csv('my_csv.csv', encoding="utf-8-sig", index=False)