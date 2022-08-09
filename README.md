# Yad2 data scrapping
### This is a scrapping program for yad2 real estate website.
######
The program ask the user for inputs from the console so make sure it's visible all the time.
<br />
This program will ask you to determine if you work with fast or slow internet.
<br />
In case you are working with replit choose slow - 'y'.
<br />
For fast internet the program will lunch a Chrome tab for you and for slow internet you will open one with a link.
<br />
In the yad2 link that will open you need to narrow down search result to a specific are of interest and specific asset type such as:
<br />
Tel Aviv, Ramat Aviv Gimel, 4 rooms, asset type = Apartment
<br />
After narrowing down and while the browser is in list mode (not map) continue by following the console prompt.
<br />
#####
With this program you can calculate the following:
<br />
Median and Mean price for Assets for sale and rentals for your search.
<br />
Number of assets for sale and rent.
<br />
The calculated ROI - return on investment calculate by dividing 11 mean rents by the mean asset price.
#####
The results will be displayed on the console. 
#####
The results saved for sharing with the community without any personal info.


# ROI calculation for real estate in Israel

This software will find the Return On Investment (ROI) for real estate investment in Israel. 

The user will adjust the search criteria using yad2 site for the preferable real 
estate type for example: A 3 to 4 rooms appartment with balcony in Bat-Yam. 

Once selected the Selenium webdriver will navigate throu the site, 
find the relevant rental options in this area that will make profit from the selected real
estate criteria. With this information the software will conduct calculation for the ROI.
The result with the search criteria will be return to the user and a log will be saved
in an open to view google sheet.



## Installation

To run this the user need to have an IDE such as PyCharm, 
Google Crome and the path for chromedrive in the environment
variables. explanation on that here: https://chromedriver.chromium.org/getting-started 

## Run Locally

Clone the project and follow the instraction on the run window in the IDE. A pop-up
window of Chrome will open after starting the program. There you will narrow down the
search criteria. 

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run start
```


## Usage/Examples

```javascript
import Component from 'my-project'

function App() {
  return <Component />
}
```


## License

[MIT](https://choosealicense.com/licenses/mit/)


