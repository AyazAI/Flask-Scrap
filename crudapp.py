"""
Main app for defining functions and arguments at command line
"""

#Necessary modules import

from app import app
import argparse as arg
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import argparse
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import string as s
import time
import math
import logging
import pandas as pd

#Function calculates the time of function
def calculate_time(func):
    def inner1(*args, **kwargs): 
    
        begin = time.time() 

        func(*args, **kwargs) 
        
        end = time.time() 
        print("Total tinme taken in : ", func.__name__, end - begin)
        return func(*args, **kwargs)
  
    return inner1 
def not_time(func):
     
 
    return func 

#Logging to specific name
def logging_to(name):
    logging.basicConfig(filename=name, filemode='a', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning('This will get logged to a file second')



state = calculate_time


#Toggling Decorator
def toggle_it(toggle):
    if toggle == 1:
        state = calculate_time
    elif toggle == 2:
        state = not_time

#Decorators Used
#Scrapping Functions

@state
def get_data():
    for i in range(26):
        alpha = s.ascii_lowercase[i]
        url = 'https://www.basketball-reference.com/players/'+alpha
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        tags = soup.findAll("th", {"data-stat" : "player"})
        for tag in tags:
            child = tag.findChildren("a")
            for c in child:
                print(c.string)
                print('https://www.basketball-reference.com'+c['href'])


@state
def getSinglePlayerDetail():
    url= 'https://www.basketball-reference.com/players/a/abdelal01.html'
    try:
        request= requests.get(url)
        if request.status_code == 200:
            soup = BeautifulSoup(request.content,"html.parser")

            for table in soup.findAll("table"):
                header = table.th.get_text()
                for row in table.findAll("tr"):
                    out_row = [ header ]
                    for col in row.findAll("td"):
                        out_row.append(col.get_text())
                    print(out_row)
        else:
            print('unable to connect ')
    except requests.HTTPError as e:
        print('Unable to open url',e)

#imdb scrapping function
def imdb():
    url = 'http://www.imdb.com/chart/top'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    movies = soup.select('td.titleColumn')
    links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
    crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
    ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
    votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

    images = [img.attrs.get('src') for img in soup.select('td.posterColumn img')]

    one_image = images[0]

    imdb = []

    # Store each item into dictionary (data), then put those into a list (imdb)
    for index in range(0, len(movies)):
        # Seperate movie into: 'place', 'title', 'year'
        movie_string = movies[index].get_text()
        movie = (' '.join(movie_string.split()).replace('.', ''))
        movie_title = movie[len(str(index))+1:-7]
        year = re.search('\((.*?)\)', movie_string).group(1)
        place = movie[:len(str(index))-(len(movie))]
        data = {"movie_title": movie_title,
                "year": year,
                "place": place,
                "star_cast": crew[index],
                "rating": ratings[index],
                "vote": votes[index],
                "link": links[index],
                "movie_poster":images[index]
            }
        imdb.append(data)
        #Scrap poster for all films
        url = images[index]
        r = requests.get(url)
        
        for x in range(len(movies)):
            val = str(random.randint(1,1001))
            with open("Image_"+val+".png",'wb') as f:
                f.write(r.content)
        
    for item in imdb:
        print(item['place'], '-', item['movie_title'], '('+item['year']+') -', 'Starring:', item['star_cast'],item['link'])
        print("Poster Image "+ item['movie_poster'])
        
    #Scrap single image
    url_one_image = one_image
    r = requests.get(url_one_image) 
    with open("Image.png",'wb') as f:
        f.write(r.content)

    url = 'https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UY67_CR0,0,45,67_AL_.jpg'
    r = requests.get(url)

    for x in range(len(movies)):
        val = str(random.randint(1,1001))
        with open("Image_"+val+".png",'wb') as f:
            f.write(r.content)

#amazon functions
def AmzonParser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
            XPATH_MOSTVALUE ='//div[@data-hook="review-collapsed"/span//text()]'
 
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            RAw_MOSTVALUE = doc.xpath(XPATH_AVAILABILITY)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
            MOSTVALUE = ''.join(RAw_MOSTVALUE).strip() if RAw_MOSTVALUE else None
 
            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE
 
            if page.status_code!=200:
                raise ValueError('captha')
            data = {
                    'NAME':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'MOSTVALUE': MOSTVALUE,
                    'URL':url,
                    }
 
            return data
        except Exception as e:
            print (e)

def ReadAsin():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    AsinList = ['B0046UR4F4',
    'B00JGTVU5A',
    'B00GJYCIVK',
    'B00EPGK7CQ',
    'B00EPGKA4G',
    'B00YW5DLB4',
    'B00KGD0628',
    'B00O9A48N2',
    'B00O9A4MEW',
    'B00UZKG8QU',]
    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.com/dp/"+i
        print ("Processing: "+url)
        extracted_data.append(AmzonParser(url))
        sleep(5)
    f=open('data.json','w')
    json.dump(extracted_data,f,indent=4)



#indeed functions


URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"
#conducting a request of the stated URL above:
page = requests.get(URL)
#specifying a desired format of "page" using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
soup = BeautifulSoup(page.text, "html.parser")
#printing soup in a more structured tree format that makes for easier reading
print(soup.prettify())

def extract_job_title_from_result(soup): 
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return(jobs)
extract_job_title_from_result(soup)

def extract_company_from_result(soup): 
    companies = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
         for b in company:
            companies.append(b.text.strip())
    else:
        sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
        for span in sec_try:
            companies.append(span.text.strip())
    return(companies)
 
extract_company_from_result(soup)

def extract_location_from_result(soup): 
    locations = []
    spans = soup.findAll('span', attrs={'class': 'location'})
    for span in spans:
        locations.append(span.text)
    return(locations)
    extract_location_from_result(soup)

def extract_salary_from_result(soup): 
    salaries = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        try:
            salaries.append(div.find('nobr').text)
        except:
            try:
                div_two = div.find(name="div", attrs={"class":"sjcl"})
                div_three = div_two.find("div")
                salaries.append(div_three.text.strip())
            except:

                salaries.append("Nothing_found")
            return(salaries)
extract_salary_from_result(soup)

def extract_summary_from_result(soup): 
    summaries = []
    spans = soup.findAll('span', attrs={'class': 'summary'})
    for span in spans:
        summaries.append(span.text.strip())
    return(summaries)


extract_summary_from_result(soup)

#Indeed Scrapping Function

def indeed_run():

    max_results_per_city = 100
    city_set = ['New+York','Chicago','San+Francisco', 'Austin', 'Seattle', 'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boulder']
    columns = ["city", "job_title", "company_name", "location", "summary", "salary"]
    sample_df = pd.DataFrame(columns = columns)

    #scraping code:
    for city in city_set:
        for start in range(0, max_results_per_city, 10):
            page = requests.get('http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=' + str(city) + '&start=' + str(start))
            time.sleep(1)  #ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
            for div in soup.find_all(name="div", attrs={"class":"row"}): 
        #specifying row num for index of job posting in dataframe
                num = (len(sample_df) + 1) 
                #creating an empty list to hold the data for each posting
                job_post = [] 
                #append city name
                job_post.append(city) 
                #grabbing job title
            for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
                job_post.append(a["title"])
                company = div.find_all(name="span", attrs={"class":"company"}) 
                if len(company) > 0:
                    for b in company:
                        job_post.append(b.text.strip()) 
                else:
                    sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
                    for span in sec_try:
                        job_post.append(span.text) 
            #grabbing location name
                c = div.findAll('span', attrs={'class': 'location'}) 
                for span in c:
                    job_post.append(span.text) 
            #grabbing summary text
                d = div.findAll('span', attrs={'class': 'summary'}) 
                for span in d:
                    job_post.append(span.text.strip()) 
            #grabbing salary
            try:
                job_post.append(div.find('nobr').text) 
            except:
                try:
                    div_two = div.find(name="div", attrs={"class":"sjcl"}) 
                    div_three = div_two.find("div") 
                    job_post.append(div_three.text.strip())
                except:
                    job_post.append("Nothing_found") 
            #appending list of job post info to dataframe at index num
                    sample_df.loc[num] = job_post



    #saving sample_df as a local csv file — define your own local path to save contents 
    sample_df.to_csv("[filepath].csv", encoding='utf-8')


#Mapping functions to command line arguments

FUNCTION_MAP = {'get_data' : get_data,
                'getSinglePlayerDetail': getSinglePlayerDetail,
                'imdb': imdb,
                'ReadAsin':ReadAsin,
                'indeed_run': indeed_run
                }
parser = argparse.ArgumentParser()
parser.add_argument('-c','--command', choices=FUNCTION_MAP.keys(), help="If you specify scrap then only list of names under alphabet a and detail for first player will be displayed. Specify each one separately for imdb, amazon and indeed scrapping",required=False)
parser.add_argument('-t','--toggle',type=int, metavar='' ,help="Enter 1 to enable decorator and 2 to disable decorator")
parser.add_argument('-n','--name',type=str, metavar='' ,help="Enter name of logging file")
parser.add_argument("-p", "--port", action="store", default="8000")

args = parser.parse_args()

toggle=args.toggle
toggle_it(toggle)

name_of_file=args.name
logging_to(name_of_file)

port = int(args.port)

if args.command:
    func = FUNCTION_MAP[args.command]
    func()

app.run(host="127.0.0.1", port=port)

from app import routes, models
