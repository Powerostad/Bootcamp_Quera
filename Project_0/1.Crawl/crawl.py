from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time


options = Options()
#options.headless = True
driver = webdriver.Chrome(options=options)

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
driver.get(url)
html = driver.page_source
HEADERS = {'User-Agent': 'Mozilla/5.0'}
disable_warnings(InsecureRequestWarning)
#page = requests.get(url,headers=HEADERS,verify=False)
soup = BeautifulSoup(html,'html.parser')

movies = soup.select('.titleColumn a')
final = []

for count,movie in enumerate(movies):
    result = {}
    
    url = 'https://www.imdb.com'+movie.get('href')
    
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    #time.sleep(3)
    #wait = WebDriverWait(driver, 5)
    #element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sc-fa971bb0-0")))
    html = driver.page_source


    HEADERS = {'User-Agent': 'Mozilla/5.0'}
#    page = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(html,'html.parser')

    result['title'] = soup.find('h1').text
    result['movieid'] = movie.get('href')[9:16]
    result['year'] = soup.select('.sc-52d569c6-0 ul li')[0].find('a').text
    try:
        result['parental_guide'] = soup.select('.sc-52d569c6-0 ul li')[1].find('a').text
        result['runtime'] = soup.select('.sc-52d569c6-0 ul li')[2].text
    except:
        result['parental_guide'] = None
        result['runtime'] = soup.select('.sc-52d569c6-0 ul li')[1].text
    
    genres = soup.select('.ipc-chip-list__scroller')[0].find_all('a')
    result['genre'] = [genre.text for genre in genres]
    directors = soup.select('.cdbSXZ ul div')[0].find_all('li')
    result['director'] = [director.text for director in directors]
    writers = soup.select('.cdbSXZ ul div')[1].find_all('li')
    result['writer'] = [writer.text for writer in writers]
    stars = soup.select('.cdbSXZ ul div')[2].find_all('li')
    result['star'] = [star.text for star in stars]
    peopleid = soup.select('.cdbSXZ ul div a')
    result['peopleid'] = [people.get('href')[8:15] for people in peopleid]
    #result['storyline'] = soup.select('.faHifs .ipc-html-content-inner-div')[0].text
    test = 0
    for i in range(len(soup.select('.sc-6d4f3f8c-2 .ipc-metadata-list-item__label'))):
        if soup.select('.sc-6d4f3f8c-2 .ipc-metadata-list-item__label')[i].text == 'Gross US & Canada':
            test = 1
    if test == 1:
        result['gross'] = soup.select('.byhjlB ul')[i].text
    elif test == 0:
        result['gross'] = None
        
    print(result)
    final.append(result)


print('Finish scrape')

with open("imdb_250_movies.json", "w") as file:
    file.write(json.dumps(final))
    print('Finish save')
    