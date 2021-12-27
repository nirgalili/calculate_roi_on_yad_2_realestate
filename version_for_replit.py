from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import statistics

import os.path


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

def enter_email(email: str) -> bool:
    if "@" in email:
        return True


valid_email = False
while not valid_email:
    text = 'Type your email and press enter key.\n' \
           'Enter the email here: '
    user_email = input(text)
    valid_email = enter_email(user_email)


url = "https://www.yad2.co.il/realestate/forsale"

slow_network = input("Is the internet slow?\n"
                     "press 'y' if the network slow or "
                     "'n' if network fast: ").lower()


if slow_network == 'y':
    url = input(f"Go to yad2 site to this link:\n"
                "\n"
                f"{url}\n"
                "\n"
                "Narrow down search results to a very specific asset type\n"
                "to improve ROI accuracy.\n"
                "Paste here the site link after narrowing\n"
                "only when site is in list view and not map view!\n"
                "Type here new url and press enter: ")
    driver.get(url)
else:
    driver.get(url)
    text = 'Type "ok" and press enter key after narrowing down search results.\n' \
           'Try to narrow to a very specific asset type to improve ROI accuracy.\n' \
           'Press enter only when the yad2 site is in list view and not map view!\n' \
           'Enter "ok" here: '

narrow_down_url = driver.current_url

# print(narrow_down_url)


def get_sellenium_list_prices(css_selector: list):
    return driver.find_elements(By.CSS_SELECTOR, css_selector)


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


PRICE_CSS_SELECTOR = "div.feeditem div.left_col .price"
assets_selenium_prices = get_sellenium_list_prices(PRICE_CSS_SELECTOR)
assets_mean_price = calculate_selenium_price_list_mean(assets_selenium_prices)

new_url_for_rent = narrow_down_url.replace("forsale", "rent")
driver.get(new_url_for_rent)


rent_selenium_prices = get_sellenium_list_prices(PRICE_CSS_SELECTOR)
search_description = driver.find_element(By.CSS_SELECTOR, "div.feed_header_container div.feed_header h1")
search_description_text = search_description.text
search_description_text = search_description_text.replace("להשכרה", "").replace("  ", " ")
print(search_description_text)

rent_mean_price = calculate_selenium_price_list_mean(rent_selenium_prices)
calculate_roi = round(rent_mean_price*11/assets_mean_price*100, 2)

print("mean asset price:", "{:,}".format(assets_mean_price), "₪")
print("mean rent price:", "{:,}".format(rent_mean_price), "₪")
print(f"The ROI for the assets is: {calculate_roi}%")

dict_to_add = {
    "description in hebrew": [search_description_text],
    "assets mean price": ["{:,}".format(assets_mean_price)],
    "rent mean price": ["{:,}".format(rent_mean_price)],
    "ROI": [str(calculate_roi)+"%"]
}

df = pd.DataFrame.from_dict(dict_to_add)

file_exists = os.path.isfile("my_csv.csv")

if file_exists:
    df.to_csv('my_csv.csv', mode='a', header=False, encoding="utf-8-sig", index=False)
else:
    df.to_csv('my_csv.csv', encoding="utf-8-sig", index=False)

driver.close()