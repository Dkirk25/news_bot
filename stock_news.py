from pyrh import Robinhood
from datetime import datetime
from model.news import StockInfo
import numpy as np
import tulipy as ti
import sched
import time
import pyotp
import os
from dotenv import load_dotenv
load_dotenv()


totp = pyotp.TOTP(os.getenv("MFA")).now()
rh = Robinhood()
rh.login(username=os.getenv("USERNAME"),
         password=os.getenv("PASSWORD"),
         qr_code=os.getenv("MFA"))
# Initiate our scheduler so we can keep checking every minute for new price changes
s1 = sched.scheduler(time.time, time.sleep)


def fetch_news(sc1):
    print("Getting news\n")

    # incorporate discord

    # Have news be sent to "stock-news" channel in chat

    news = rh.get_news("WKHS")
    info_results = news["results"]
    for i in info_results:
        stock_info = StockInfo(i["title"], i["source"],
                               i["preview_text"].replace("\n\n", ""), i["url"])
        print(str(stock_info))

    s1.enter(300, 1, fetch_news, (sc1, ))


s1.enter(1, 1, fetch_news, (s1, ))
s1.run()
