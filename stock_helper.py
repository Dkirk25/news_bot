from pyrh import Robinhood
import pyotp
import os
from dotenv import load_dotenv
from model.news import StockInfo
import yahoo_news
load_dotenv(override=True)

# MFA = os.getenv("MFA")
# USERNAME = os.getenv("USERNAME")
# PASSWORD = os.getenv("PASSWORD")

# totp = pyotp.TOTP(MFA).now()
# rh = Robinhood()
# rh.login(username=USERNAME,
#          password=PASSWORD,
#          qr_code=MFA)


async def fetch_news(stock):
    stock_to_search = stock
    clean_stock_list = []
    try:
        news = yahoo_news.get_news(stock_to_search)
        # info_results = news["results"]
        # for i in info_results:
        #     stock_info = StockInfo(i["uuid"], i["title"], i["source"], i["published_at"],
        #                            i["preview_text"].replace("\n\n", ""), i["url"], stock_to_search)
            # print(str(stock_info))
        clean_stock_list.append(news)
        print(stock_to_search + " = " + str(len(clean_stock_list)))
    except Exception as e:
        print("Error: ", e, "Occurred.")
        print("Skipping...")
        print()
    return clean_stock_list
