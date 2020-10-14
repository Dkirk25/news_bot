import json
from newsapi import NewsApiClient
from datetime import datetime as dt
import os
from dotenv import load_dotenv
load_dotenv(override=True)

key = os.getenv("NEWS_API_KEY")
newsapi = NewsApiClient(api_key=key)

def get_news(stock):
    top_headlines = newsapi.get_everything(q=stock)['articles']
    top_headlines.sort(key=extract_time, reverse=True)
    latest_article = top_headlines[0]
    data = {}

    data['uuid'] = latest_article['source']['id']
    #Title
    data['title'] = latest_article['title']
    #Description
    data['preview_text'] = latest_article['description']
    # Source
    data['source'] = latest_article['source']['name']
    # published_at
    data['published_at'] = latest_article['publishedAt']
    # URL
    data['url'] = latest_article['url']
    filtered_stock_list = list(filter(lambda x: "Seeking Alpha" in x['source']['name'], top_headlines))
    return json.loads(json.dumps(data))


def extract_time(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        json_date = dt.strptime(json['publishedAt'],"%Y-%m-%dT%H:%M:%SZ")
        return json_date
    except KeyError:
        return 0