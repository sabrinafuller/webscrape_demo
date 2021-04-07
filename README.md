# webscrape_demo
webscrape demo of most_wanted sites

# Webscraping bad guys 
## Sabrina
###### The python file and python notebook should be equivalent, the python notebook was useful for quick tests of the code. 

#### 1. First and formost I decided to to do this in a python notebook as it is more interactive and easier to test small bits of code. Espcially since working with regex , I needed to be testing as I go. 

#### 2. I decided to use beautiful soup, because I have used beautiful soup to scrape wikipedia before (the data formatting was much easier). 
### ________________________________________________________________________

#### The webscraper_a class is goes to the requested url and scrapes all the pages that that page links to, then linearly converts the html to json

#### the formatting_data class formats my data such that it can read into a json

### ________________________________________________________________________
#### current issues : 
###### My regular expressions are not working right 
###### I blieve the issue is due to the regex search expressions not working right
###### Since I haven't really worked intensly with regex I need more time to read the docs to understand the timing issue 
###### Formatting scraps details my current regex searches (they work for some) but not all data on the site
###### http://www.regular-expressions.info/catastrophic.htmlCurrent 
