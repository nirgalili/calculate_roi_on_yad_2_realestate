def main():

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    import time
    import statistics

    url_yad_2_sale = "https://www.yad2.co.il/realestate/forsale"
    url_google_forms = "https://docs.google.com/forms/d/e/1FAIpQLSfBB9nKjz3wSzWMjQWSZPgIRxgpNpj7CCRaalom97SVYOFPew/viewform?usp=sf_link"

    clearConsole = lambda: print('\n' * 150)

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

    clearConsole()

    slow_network = input("Is the internet slow?\n"
                        "press 'y' if the network slow or "
                        "'n' if network fast: ").lower()

    clearConsole()

    if slow_network == 'y':
        url_yad_2_sale = input(f"Go to yad2 site to this link:\n"
                    "\n"
                    f"{url_yad_2_sale}\n"
                    "\n"
                    "Narrow down search results to a very specific asset type\n"
                    "to improve ROI accuracy.\n"
                    "Paste here the site link after narrowing\n"
                    "only when site is in list view and not map view!\n"
                    "Type here new url and press Enter:\n")
        clearConsole()
        print("Loading, please wait")
        driver.get(url_yad_2_sale)
    else:
        driver.get(url_yad_2_sale)
        text = 'Type "ok" and press Enter key after narrowing down search results.\n' \
            'Try to narrow to a very specific asset type to improve ROI accuracy.\n' \
            'Press enter only when the yad2 site is in list view and not map view!\n' \
            'Enter "ok" here: '

    clearConsole()
    print("Loading, please wait")

    clearConsole()
    input("Press Enter to continue after site lunches.\n"
        "Solve human test if one appears.")
    narrow_down_url = driver.current_url

    clearConsole()
    print("Loading, please wait")

    def get_selenium_list_prices(css_selector: list):
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

    def create_list_int(text_list: list) -> list:
        price_list_int =[]
        for item in text_list:
            price_list_int.append(create_number_from_price_str(item))
        return [x for x in price_list_int if x is not None]

    def calculate_selenium_price_list_mean(webdriver_list) -> int:
        price_text_list = convert_lists_of_webriver_to_text(webdriver_list)
        price_list_int = create_list_int(price_text_list)
        return int(statistics.mean(price_list_int))

    def calculate_selenium_price_list_median(webdriver_list) -> int:
        price_text_list = convert_lists_of_webriver_to_text(webdriver_list)
        price_list_int = create_list_int(price_text_list)
        return int(statistics.median(price_list_int))

    price_css_selector = "div.feeditem div.left_col .price"
    assets_selenium_prices = get_selenium_list_prices(price_css_selector)
    assets_mean_price = calculate_selenium_price_list_mean(assets_selenium_prices)
    assets_median_price = calculate_selenium_price_list_median(assets_selenium_prices)
    number_of_assets_for_sale = len(convert_lists_of_webriver_to_text(assets_selenium_prices))

    new_url_for_rent = narrow_down_url.replace("forsale", "rent")
    driver.get(new_url_for_rent)

    clearConsole()
    print("Loading, please wait")

    clearConsole()
    input("Press Enter to continue after site lunches.\n"
        "Solve human test if one appears.")

    clearConsole()

    rent_selenium_prices = get_selenium_list_prices(price_css_selector)
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

    calculate_roi = round(rent_mean_price*11/assets_mean_price*100, 2)

    print("-----Assets for sale info-----")
    print("Mean asset price:", "{:,}".format(assets_mean_price), "₪")
    print("Median asset price:", "{:,}".format(assets_median_price), "₪")
    print(f"Number of assets for sale is: {number_of_assets_for_sale}")
    print("")
    print("-----Assets for rent info-----")
    print("Mean rent price:", "{:,}".format(rent_mean_price), "₪")
    print("Median rent price:", "{:,}".format(rent_median_price), "₪")
    print(f"Number of assets for rent is: {number_of_assets_for_rent}")
    print("")
    print(f"The ROI for the assets is: {calculate_roi}%")

    driver.get(url_google_forms)
    time.sleep(2)

    list_of_columns_order_in_form_field = [
        [user_email, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [search_description_text, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [assets_mean_price, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [assets_median_price, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [number_of_assets_for_sale, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [rent_mean_price, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [rent_median_price, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [number_of_assets_for_rent, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input'],
        [calculate_roi, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[9]/div/div/div[2]/div/div[1]/div/div[1]/input']
    ]

    def enter_text_to_google_form(question_answer, css_selector: int):
        form_field = driver.find_element(By.XPATH, css_selector)
        form_field.send_keys(question_answer)

    for field in list_of_columns_order_in_form_field:
        enter_text_to_google_form(question_answer=field[0], css_selector=field[1])

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    driver.close()


if __name__=="__main__":
    main()