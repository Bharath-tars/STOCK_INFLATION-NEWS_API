import requests
import datetime
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


dt = datetime.datetime.now()
str_month = dt.month

if dt.month < 10:
    str_month = str(0) + str(dt.month)
day1 = dt.day - 1
dt1 = str(dt.year) + "-" + str(str_month) + "-" + str(day1)
day2 = dt.day - 2
dt2 = str(dt.year) + "-" + str(str_month) + "-" + str(day2)

STOCK_NAME = "TSLA"
API_KEY_Stock = 'T3I330RY7C6Q8HQH'
STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY_News = 'eca590761b2a4008918bc67d61a3d3c0'
AUTH_ACCOUNT = 'ACa94fa1debd2417973488cb6c52f353e8'
AUTH_TOKEN = 'bdf4305ffac06f2d24df9f1b0128334a'

parameters_stock = {
    'symbol': STOCK_NAME,
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'apikey': API_KEY_Stock
}
responce_api = requests.get(STOCK_ENDPOINT, params=parameters_stock)
responce_api.raise_for_status()
data = responce_api.json()

data_day1_close = data["Time Series (Daily)"][dt1]['4. close']
data_day2_close = data["Time Series (Daily)"][dt2]['4. close']

data_day_close_diff = float(data_day1_close) - float(data_day2_close)
per_diff = (data_day_close_diff / float(data_day1_close)) * float(100)

trusted_domains = 'techcrunch.com,engadget.com,thenextweb.com,business-standard.com'
excluded_domains = 'breitbart.com,clickhole.com'

parameters_news = {
    "q": "tesla",
    "from": dt2,
    "to": dt1,
    "language": "en",
    "domains": trusted_domains,
    "excludeDomains": excluded_domains,
    "apikey": API_KEY_News
}
stock_news_api = requests.get(NEWS_ENDPOINT,params=parameters_news)
stock_news_api.raise_for_status()
stock_news = stock_news_api.json()
news_articles = []
for news_no in range(0,3):
    news_articles.append(stock_news["articles"][news_no])
if per_diff >0:
    sign = "🔺"
else:
    sign = "🔻"


message_to_be_sent = f"\nTESLA {dt1} STOCK REVIEW\n"+f"Inflation   : {sign}{'%.2f'%per_diff}%\n"+f"Start Price : {data['Time Series (Daily)'][dt2]['4. close']}\n"+f"Close Price : {data['Time Series (Daily)'][dt1]['4. close']}\n"
message_to_be_sent_body = f"\nNEWS REPORT TSLA\n"
message_to_be_sent_body_1 = f"HeadLine : {news_articles[0]['title']}\n" + f"Brief : {news_articles[0]['description']}\n" + f"Report URL : {news_articles[0]['url']}\n"
end_message = message_to_be_sent + message_to_be_sent_body + message_to_be_sent_body_1

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}
client = Client(AUTH_ACCOUNT, AUTH_TOKEN, http_client=proxy_client)
message = client.messages.create(
    body=end_message,
    from_="+19285997896",
    to="+918639196174"
)

print(message.status)

