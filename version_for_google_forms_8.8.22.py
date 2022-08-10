# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import numpy as np

# Consts
# all the utl for the project
URL_YAD2_SALE = "https://www.yad2.co.il/realestate/forsale"

URL_GOOGLE_FORMS = 'https://docs.google.com/forms/d/e/' \
                   '1FAIpQLSfcejfEwZToX6Y8JtSLk9TCFDEz4kk1oIlDetPyT2Llxx35AQ/viewform?usp=sf_link'


PRICE_CSS_SELECTOR = "div.feeditem div.left_col .price"

# Functions
clear_console = lambda: print('\n' * 80) # fake clear screen func for convinience


def create_driver():
    option = webdriver.ChromeOptions()
    option.add_argument('--no-sandbox')
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--window-size=800,200")
    # option.add_argument("--secondary-display-layout")
    return webdriver.Chrome(options=option)


def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def enter_email(email: str) -> bool:
    if "@" in email:
        return True


def loading_please_wait():
    clear_console()
    print("Loading, please wait")


def solve_human_test():
    clear_console()
    input("Press Enter to continue after site lunches.\n"
          "Solve human test if one appears and then press Enter.")


def get_selenium_list_prices(css_selector: str):
    return driver.find_elements(By.CSS_SELECTOR, css_selector)


def create_number_from_price_str(price_str: str):
    try:
        return int(price_str.replace(",", "").replace(" ₪", ""))
    except ValueError:
        return None


def convert_lists_of_webriver_to_text(webdriver_list) -> list:
    new_list_of_text = []
    for item in webdriver_list:
        new_list_of_text.append(item.text)
    return new_list_of_text


def create_list_int(text_list: list) -> list:
    price_list_int = []
    for item in text_list:
        price_list_int.append(create_number_from_price_str(item))
    return [x for x in price_list_int if x is not None]


def calculate_selenium_price_list_mean(webdriver_list) -> int:
    price_text_list = convert_lists_of_webriver_to_text(webdriver_list)
    price_list_int = create_list_int(price_text_list)
    price_list = reject_outliers(np.array(price_list_int), m=2)
    try:
        mean_price = int(np.mean(price_list))
    except ValueError:
        mean_price = None
        print("couldn't find results for the real estate query - please check your search query and retry.")
    return mean_price


def calculate_selenium_price_list_median(webdriver_list) -> int:
    price_text_list = convert_lists_of_webriver_to_text(webdriver_list)
    price_list_int = create_list_int(price_text_list)
    return int(np.median(price_list_int))


def enter_text_to_google_form(question_answer, css_selector: str):
    form_field = driver.find_element(By.XPATH, css_selector)
    form_field.send_keys(question_answer)


def get_current_url():
    loading_please_wait()
    narrow_down_url = driver.current_url
    loading_please_wait()
    return narrow_down_url


def email_validation():
    valid_email = False
    while not valid_email:
        text = 'Type your email and press enter key.\n' \
               'Enter the email here: '
        user_email = input(text)
        valid_email = enter_email(user_email)

    return user_email


def roi_calculation(rent_mean_price, assets_mean_price):
    return round(rent_mean_price * 11 / assets_mean_price * 100, 2)


def select_user_interface():
    work_in_replit = input("Do you work in Repl.it?\n"
                           "press 'y' if yes or 'n' not: ").lower()

    if work_in_replit == 'y':
        loading_please_wait()
        solve_human_test()
        url_yad2_from_user = input(f"Go to yad2 site to this link:\n"
                                   "\n"
                                   f"{URL_YAD2_SALE}\n"
                                   "\n"
                                   "Narrow down search results to a very specific asset type\n"
                                   "Make sure there are more then one search result.\n"
                                   "to improve ROI accuracy.\n"
                                   "Paste here the site link after narrowing\n"
                                   "only when site is in list view and not map view!\n"
                                   "Type here new url and press Enter:\n")

        loading_please_wait()

        driver.get(url_yad2_from_user)
    else:
        loading_please_wait()

        driver.get(URL_YAD2_SALE)
        text = 'Type "ok" and press Enter key after narrowing down search results.\n' \
               'Try to narrow to a very specific asset type to improve ROI accuracy.\n' \
               'Make sure there are more then one search result.\n'\
               'Press enter only when the yad2 site is in list view and not map view!\n' \
               'Enter "ok" here: '
        solve_human_test()
        input(text)


def secondary_screen():
    while True:
        secondary_screen_location = input("Do you have secondary screen?\n press 'n' if you don't or if work in replit\n " \
                                          "press 'r' if it's to the right or 'l' if it's to the left: \n")
        if secondary_screen_location == 'l':
            driver.set_window_position(-1000, 0)
            driver.maximize_window()
            text = 'New chrome window opened on the left secondary screen'
            return text
        elif secondary_screen_location == 'r':
            driver.set_window_position(1000, 0)
            driver.maximize_window()
            text = 'New chrome window opened on the right secondary screen'
            return text
        elif secondary_screen_location == 'n':
            text = 'New chrome window opened. Arrange it so you can see both the chrome and the IDE run console'
            return text
        else:
            print("Please use only 'r' , 'l' or 'n', and try again.")


if __name__ == "__main__":

    driver = create_driver()

    open_screen = secondary_screen()
    print(open_screen)

    clear_console()

    user_email = email_validation()

    clear_console()

    iterations = 0
    assets_mean_price = None
    while assets_mean_price is None and iterations < 2:
        select_user_interface()
        narrow_down_url_yad2 = get_current_url()
        assets_selenium_prices = get_selenium_list_prices(PRICE_CSS_SELECTOR)
        assets_mean_price = calculate_selenium_price_list_mean(assets_selenium_prices)
        iterations += 1

    if assets_mean_price is None:
        clear_console()
        print("couldn't find results for the real estate query - program is terminate.")
        exit(1)

    assets_median_price = calculate_selenium_price_list_median(assets_selenium_prices)
    number_of_assets_for_sale = len(convert_lists_of_webriver_to_text(assets_selenium_prices))

    new_url_for_rent = narrow_down_url_yad2.replace("forsale", "rent")
    driver.get(new_url_for_rent)

    loading_please_wait()

    solve_human_test()

    clear_console()

    rent_selenium_prices = get_selenium_list_prices(PRICE_CSS_SELECTOR)
    search_description = driver.find_element(By.CSS_SELECTOR, "div.feed_header_container div.feed_header h1")
    search_description_text = search_description.text
    search_description_text = search_description_text.replace("להשכרה", "").replace("  ", " ")
    print("")
    print(search_description_text)
    print("other way to print hebrew if the former goes reverse")
    print(search_description_text[::-1])

    rent_mean_price = calculate_selenium_price_list_mean(rent_selenium_prices)
    rent_median_price = calculate_selenium_price_list_median(rent_selenium_prices)
    number_of_assets_for_rent = len(convert_lists_of_webriver_to_text(rent_selenium_prices))

    calculate_roi = roi_calculation(rent_mean_price, assets_mean_price)

    print("-----Assets for sale info-----")
    print("Mean assets price:", "{:,}".format(assets_mean_price), "₪")
    print("Median assets price:", "{:,}".format(assets_median_price), "₪")
    print(f"Number of assets for sale is: {number_of_assets_for_sale}")
    print("")
    print("-----Assets for rent info-----")
    print("Mean rent price:", "{:,}".format(rent_mean_price), "₪")
    print("Median rent price:", "{:,}".format(rent_median_price), "₪")
    print(f"Number of assets for rent is: {number_of_assets_for_rent}")
    print("")
    print(f"The ROI for the assets is: {calculate_roi}%")

    driver.get(URL_GOOGLE_FORMS)
    time.sleep(2)

    list_of_columns_order_in_form_field = [
        [user_email, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [search_description_text,
         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [assets_mean_price, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [assets_median_price, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [number_of_assets_for_sale,
         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [rent_mean_price, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [rent_median_price, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [number_of_assets_for_rent,
         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [calculate_roi, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[9]/div/div/div[2]/div/div[1]/div/div[1]/input']
    ]

    for field in list_of_columns_order_in_form_field:
        enter_text_to_google_form(question_answer=field[0], css_selector=field[1])

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    driver.close()


