import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "get your API key from https://www.alphavantage.co"
NEWS_API_KEY = "get your API key from https://newsapi.org"

#twilio account
account_sid = "get your account API from twilio"
auth_token = "get your token from twilio"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
data = response.json()
yesterday_close = float(data["Time Series (Daily)"]["2022-09-13"]["4. close"])
print(yesterday_close)

before_yesterday_close = float(data["Time Series (Daily)"]["2022-09-12"]["4. close"])
print(before_yesterday_close)

##v2 using list comprehension
# data = response.json()["Time Series (Daily)"]
# data_list = [value for (key, value) in data.items()]
# yesterday_data = data_list[0]
# yesterday_close = yesterday_data["4. close"]
# print(yesterday_close)

#before_yesterday_close = data_list[1]
#before_yesterday_close = yesterday_data["4. close"]

difference = round((yesterday_close - before_yesterday_close),2)
#print(difference)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
average = (yesterday_close+before_yesterday_close)/2
#print(average)
percent_dif = round((difference / average)*100, 2)
#print(percent_dif)

if abs(percent_dif) > 5:
    parameters = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}
    response = requests.get(NEWS_ENDPOINT, params=parameters)
    articles = response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)

#list comprehension [new_item for intem in list]
formatted_articles = [f"{STOCK_NAME}: {up_down}{percent_dif}%\nHeadlines: {article['title']}.\nBrief: {article['description']}" for article in three_articles]

#send message to user
client = Client(account_sid, auth_token)

for article in formatted_articles:
    message = client.messages.create(
         body=article,
         from_="get your trial phone number from twilio",
         to="your phone number or number you want to send the alert"

     )
    
