#webscraper class
#webscraper running at line 231

import requests
import pandas as pd 
from bs4 import BeautifulSoup
import unicodedata
import dateutil.parser as dparser
import json
import re
import unicodedata
import dateutil.parser as dparser




## imports the beautiful soup object
#only had time to really work on formatting the regular expressions
class webscraper_a: 
    ## turns a python dict into a json file
    def make_json(self):
        js = None
        with open('tst.json', 'w') as json_file:
            json.dump(self.page_data_dict, json_file)
            js = self.json_table
    
        return 
           
    ##Get page takes an url as input and returns the html parsed page
    ## uses the beautuful soup package
    def get_page(self, url ):
        try: 
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            self.curr_page = soup
            return soup
        except: 
            print("exception thrown")
            return None 

     #Sets the main head page (the root of the crawler tree)   
    def set_main_soup(self): 
        self.main_soup = self.get_page(self.url)
        return 
        
    #get all the urls from this page url    
    def get_page_urls(self):
        #returns the urls
        try: 
            page_results = self.main_soup.find("div", class_ = "view-content").findAll("a", recursive = "false")
            for i in page_results: 
                self.page_urls.append(i["href"])
        except AttributeError: 
            print("error in reading the page urls")
        return 
    #get content for the subpages
    def get_page_content(self, url):
        self.curr_page = self.get_page(url)
        print("getting page content for: ", url)
        #returns the urls
        try: 
            page_results = self.curr_page.find("div", class_ = "content")
            return page_results
        except AttributeError: 
            print("error in reading the page")
            return None 
        
    
    ## constructor 
    def __init__(self, url):
        self.url = url
        #current page crawler is on (for debugging)
        self.curr_page = None
        #root page
        self.main_soup = None
        #child page of root
        self.side_soup = None 
        #list of page urls to visit
        self.page_urls = []
        #dict to eventually become the json
        self.page_data_dict = []
        #json 
        self.json_table = None
        #get the main page
        self.get_page(self.url)
        return
    #The main webscrape method, once the webscraper objected is constructed
    # this method is able to run without any additonal input
    ## possible upgrades
        ## Set tree crawl depth and navigate pages to that depth
        ## function to name_json 
        ## create error catching functions 
    def webscrape(self): 
        #make the main soup
        
        soup = self.set_main_soup()
        #get the urls from the page
        self.get_page_urls()
        formatter_ = data_formatting(self.url, self.curr_page.content)
        #progress
        print("------------------------------")
        print(len(self.page_urls),"subpages found ")
        #loop through each url and parse the data
        data__list = []
        for i in range(len(self.page_urls)): 
            self.side_soup = self.get_page_content(self.page_urls[i])
            formatter_ = data_formatting(self.page_urls[i], self.side_soup)
            page_data = formatter_.parse_html()
            #self.page_data_dict.append(page_data) 
            data__list.append(page_data)
            
            
        #make the json   
        data__list
        pd.Dataframe(data__list)
        #json_file = self.make_json()    
        return



##Data formatting class 
class data_formatting: 
    ## Updates should include better exception catching
    ## Better parsing of data to allow for more generality
    ## A way to define certain expression patterns the user could enter 
    ## constructor for data_formatting
    def __init__(self, url, html): 
        self.url = url
        self.data = None
        self.site_html = html
        # predefined rows of data
        # I struggled on to use the data on the page to name my rows
        # but not all people had the same datafields so I needed this baseline
        # I know I'm missing some data fields
        self.data_rows = ["name", "date of birth",  "sex", "height",  "eye color","ethic orgin", 
                      "languages spoken", "nationality", 
                      "crime", "case status", "source url"]
        return 
    ## Data patterns, essentially a dictionary of various patterns to look for
    def data_patterns_regex(self,data_type, url):
        self.url = url
        #matches the datatype ith the correct pattern
        pattern_type = {
            #date pattern
            1: ("(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|""Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|""Dec(ember)?)\s+\d{1,2},\s+\d{4}"), 
            #https://stackoverflow.com/questions/54058389/regex-match-month-name-day-year
            #crime pattern
            8: r'Crime:(.*) (?=Sex:)|(?= Nationality:)| (?= Ethnic Origin:)|(?= State of Case:)',
            #case state             
            9: "State of case((.|\n)+)(.+)((.|\n)+)(.*)(?=Reward)",
            4: "Eye colour:(.+?) ",
            5: "Ethic Origin:(.+?) ",
           #language pattern 
            7: "Language spoken:(.+?) ",
            6:"Nationality:(.+?) ",
            #search for string after 
            2:"Sex: (.+?) ", 
            3: "Approximate height:(.+?) ",
            #pattern for name
            0: "([A-Z\s])(.*) (?=Wanted)|(?=Crime)",
            10: "(.*) other(.*) "
            }

        return pattern_type.get(data_type, "na")
    ## the main html parser
    def parse_html(self):
       
            cleanr= re.compile('<.*?>')#remove the html
            cleantext = re.sub(cleanr, '', str(self.site_html)) #get the clean htm;
            #cleanr = unicodedata.normalize('NFKD', cleantext).encode('ascii', 'ignore')
            
            data_obj = []

           
            for i in self.data_rows:
                #i, self.url, "current scrape")
                if(i == "date of birth"):
                    d = self.data_patterns_regex(1, self.url)
                    date_patt = re.compile(d)
                    try:
                        dob = date_patt.search(cleantext).group() 
                        data_obj.append(dob)  
                    except: 
                        dob = "none"
                elif (i == "case status"): 
                    case_state_patt = self.data_patterns_regex(9, self.url)
                    data_obj.append(re.findall(case_state_patt, cleantext))   
                    
                else: 
                    patt = self.data_patterns_regex(self.data_rows.index(i), self.url)
                    data_obj.append(re.search(patt, cleantext))
                
                    

            
            self.data = data_obj
        
            self.fill_rows()
            return  self.data

    ## this populates my dict that I will eventually turn into a json
    def fill_rows(self):
        data_list = []
        
        print("filling rows!")
        for k in self.data:
            try: 
                
                s = k[0].strip() 
                data_list.append(s)   
            except:
                data_list.append("none")
                
                
        try:       
            data_list.append(str(self.url))
            self.data_rows.append("URL")
            #res = dict(zip( d, self.data))
            res = dict(zip(data_list, self.data))
        
            
        except: 
            print("error in formatting data")
            res = dict()
        print(res)
        return res
		
		
		
#run the webscraper
def main():

	URL = 'https://eumostwanted.eu'

    a = webscraper_a(URL)
    a.webscrape()

if __name__ == "__main__":
    main()

 
    
    