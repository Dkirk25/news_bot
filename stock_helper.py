import alpha_seeking
from model.news import StockInfo

def fetch_news(stock):
    stock_to_search = stock
    clean_stock_list = []
    try:
        i = alpha_seeking.get_news(stock_to_search)
        stock_info = StockInfo(i["uuid"], i["title"], i["source"], i["published_at"],
                                i["preview_text"], i["url"], stock_to_search)
        clean_stock_list.append(stock_info)
        print(stock_to_search + " = " + str(len(clean_stock_list)))
    except Exception as e:
        print("Error: ", e, "Occurred.")
        print("Skipping...")
        print()
    return clean_stock_list
