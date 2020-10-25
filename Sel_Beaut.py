from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

movie_names = []
movie_descriptions = []
movie_ratings = []
def open_site():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=C:/Users/sectr/AppData/Local/Google/Chrome/User Data/Default")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-notifiactions")
    driver = webdriver.Chrome(executable_path='C:/Users/sectr/OneDrive/Desktop/PythonProjects/chromedriver_win32/chromedriver.exe',options=options)
    driver.get(r'https://www.amazon.com/ap/signin?accountStatusPolicy=P1&clientContext=261-1149697-3210253&language=en_US&openid.assoc_handle=amzn_prime_video_desktop_us&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.primevideo.com%2Fauth%2Freturn%2Fref%3Dav_auth_ap%3F_encoding%3DUTF8%26location%3D%252Fref%253Ddv_auth_ret')
    sleep(5)
    driver.find_element_by_id('ap_email').send_keys('preethanair239@gmail.com')
    driver.find_element_by_id('ap_password').send_keys('Ashish1222',Keys.ENTER)
    sleep(2)
    search(driver)    
def search(driver):
    driver.find_element_by_id('pv-search-nav').send_keys('Comedy Movies',Keys.ENTER)
    
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = driver.page_source
    Soup = soup(html,'lxml')
    tiles = Soup.find_all('div',attrs={"class" : "av-hover-wrapper"})
    
    for tile in tiles:
        movie_name = tile.find('h1',attrs={"class" : "_1l3nhs tst-hover-title"})
        movie_description = tile.find('p',attrs={"class" : "_36qUej _1TesgD tst-hover-synopsis"})
        movie_rating = tile.find('span',attrs={"class" : "dv-grid-beard-info"})
        rating = (movie_rating.span.text)
        try:
            if float(rating[-3:]) > 8.0 and float(rating[-3:]) < 10.0:
                movie_descriptions.append(movie_description.text)
                movie_ratings.append(movie_rating.span.text)
                movie_names.append(movie_name.text)
                print(movie_name.text, rating)
        except ValueError:
            pass
    dataFrame()
def dataFrame():
    
    
    details = {
        'Movie Name' : movie_names,
        'Description' : movie_descriptions,
        'Rating' : movie_ratings
    }
    data = pd.DataFrame.from_dict(details,orient='index')
    data = data.transpose()
    data.to_csv('Comedy.csv')
            
    sleep(15)
    

open_site()
