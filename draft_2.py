def enter_email(email: str) -> bool:
    if "@" in email:
        return True


valid_email = False
while not valid_email:
    text = 'Type your email and press enter key after narrowing down search results.\n' \
           'Try to narrow to a very specific asset type to improve ROI accuracy.\n' \
           'Press enter only when the yad2 site is in list view and not map view!\n' \
           'Enter the email here: '
    user_email = input(text)
    valid_email = enter_email(user_email)

url = "https://www.yad2.co.il/realestate/forsale"

url = input(f"Go to yad2 site to this link:\n"
                "\n"
                f"{url}\n"
                "\n"
                "Narrow down search results to a very specific asset type"
                "to improve ROI accuracy."
                "paste here the site link after narrowing"
                "only when site is in list view and not map view!")
