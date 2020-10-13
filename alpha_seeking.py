from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_binary

driver = webdriver.Chrome()

html = driver.page_source

PARSER = 'html.parser'


def get_news(stock):
    url = 'https://seekingalpha.com/symbol/'+ stock +'/news'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,features="lxml")

    # Get list of atricles
    dirty_news_articles =  soup.find_all(attrs={"class": "a36d8-2-Y79"})[0]
    latest_news_article = []

    for article in dirty_news_articles:
        # Clean the response
         
        
        # add it to a new list
        latest_news_article.append(article.text)

    return latest_news_article[0]