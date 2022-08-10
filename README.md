# ROI calculation for real estate in Israel

This software will find the Return On Investment (ROI) for real estate investment in Israel. 

The user will adjust the search criteria using yad2 site for the preferable real 
estate type for example: A 3 to 4 rooms appartment with balcony in Bat-Yam. 

Once selected the Selenium webdriver will navigate throu the site, 
find the relevant rental options in this area that will make profit from the selected real
estate criteria. With this information the software will conduct calculation for the ROI.
The result with the search criteria will be return to the user and a log will be saved
in an open to view google sheet.

With this program you can calculate the following:
Median and Mean price for Assets for sale and rentals for your search query.
Number of assets for sale and rent.
The calculated ROI - return on investment calculate by dividing 
11 mean rent month by the mean asset price.


## Installation

To run this the user need to have an IDE such as PyCharm, 
Google Crome and the path for chromedrive in the environment
variables. explanation on that here: https://chromedriver.chromium.org/getting-started 

## Run Locally

Clone the project and follow the instraction on the run window in the IDE. A pop-up
window of Chrome will open after starting the program. There you will narrow down the
search criteria. Pay attention to the prompts given in the IDE run screen. This is the 
program interface. 

If chhose to run with Replit and not locally in IDE use this blogpost 
in hebrew for further explanation about Replit


## Usage/Examples


In order to deal with CAPTCHA  the webdriver will ask the user to solze
the puzzels given by the yad2 site such as this one:

![Alt text](https://nadlandata.files.wordpress.com/2022/01/chrome-capture-4.gif?w=555&zoom=2 "Optional title")

The output from the calculation will be print with the calculated info for 
the user search query:

![Alt text](https://nadlandata.files.wordpress.com/2022/01/image-19.png "Optional title")

## License

[MIT](https://choosealicense.com/licenses/mit/)

