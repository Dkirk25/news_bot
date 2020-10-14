from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_binary
import json
import time

op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)

html = driver.page_source

def get_news(stock):
    time.sleep(30)
    url = 'https://seekingalpha.com/symbol/'+ stock +'/news'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,features="lxml")

    # Get list of atricles
    dirty_news_article =  soup.find_all(attrs={"class": "a36d8-2-Y79"})[0]
    data = {}

    data['uuid'] = "None"
    #Title
    data['title'] = soup.find(attrs={"class": "_66147-2pxC0 _7e758-JdZFq _7e758-SfA3O _7e758-1Ou5t"}).contents[0]
    #Description
    data['preview_text'] = dirty_news_article.contents[0].next_element.text
    # Source
    data['source'] = dirty_news_article.contents[0].next_sibling.next.text
    # published_at
    data['published_at'] = dirty_news_article.contents[0].next_sibling.next.next_sibling.text
    # URL
    data['url'] = dirty_news_article.contents[0].next_element.attrs['href']  
    # add it to a new list
    return json.loads(json.dumps(data))
