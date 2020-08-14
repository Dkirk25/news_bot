from pyrh import Robinhood
from datetime import datetime
from model.news import StockInfo
import sys
import numpy as np
import tulipy as ti
import schedule
import time
import pyotp
import os
from dotenv import load_dotenv
load_dotenv(override=True)

MFA = os.getenv("MFA")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

totp = pyotp.TOTP(MFA).now()
rh = Robinhood()
rh.login(username=USERNAME,
         password=PASSWORD,
         qr_code=MFA)

# Initiate our scheduler so we can keep checking every minute for new price changes
# s1 = sched.scheduler(time.time, time.sleep)


def fetch_news():
    print("Getting news\n")

    news = rh.get_news("WKHS")
    info_results = news["results"]
    for i in info_results:
        stock_info = StockInfo(i["uuid"], i["title"], i["source"], i["published_at"],
                               i["preview_text"].replace("\n\n", ""), i["url"])
        print(str(stock_info))


schedule.every().minute.at(":10").do(fetch_news)

while True:
    schedule.run_all()
    # time.sleep(1)
