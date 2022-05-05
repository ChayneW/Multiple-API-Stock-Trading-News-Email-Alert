import requests
import smtplib
import datetime as dt

# Datetime Module to convert UTC data into desired date and time format.
TODAY = dt.datetime.now().date() # Return just the date
previous_date = TODAY - dt.timedelta(days=1)
day_before = TODAY - dt.timedelta(days=2)

TODAY = str(TODAY)
previous_date = str(previous_date)
day_before_date = str(day_before)

print(f" the past previous dates are: {previous_date}, {day_before_date}") 


# Target stock that is used for API's:
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

'''Funct. that takes API: alphavantage.co stock data as parameters, converts day before and previous day's close to calculate percent change.
    - Returns value as int.
    '''
def is_stable(previous_day: float, day_before: float):
    first_val = day_before
    second_val = previous_day
    is_stable = ((second_val - first_val) / first_val) * 100
    is_stable = int(is_stable)
    print(f"The percent change is: {is_stable}")
    return is_stable

'''Funct. connects to API: https://newsapi.org that finds news data on targeted stock,
    - Parses through json data,
    - Finds 3 newest story data and returns them.
    '''
def get_news():
    news_request = requests.get(url=News_Endpoint, params=news_parameters)
    news_request.raise_for_status()
    news_data = news_request.json()
    
    news_articles = news_data['articles'][:3]
    return news_articles


'''Function that takes the news that's been converted data that was returned from 'get_news()' funct.
    - Uses SMTPLIP Mod to connect to email and send data to either email, or use email provider format to
        send data as email-text.
        '''
def send_news(news):
    news_info = news

    MY_EMAIL = 'YOUR EMAIL HERE'
    PASSWORD = 'YOUR PASSWORD HERE'

    for x in news_info:
            
            print('\n')
            title = x['title']
            description = x['description']
            print(f'Title: {title}')
            print(f'Description: {description}')

            # UNCOMMENT to Initiate smtplib connection to send email status.
            #   - format uses phone provider's text format to send emails from email provider to text phone. 

            # with smtplib.SMTP('smtp.EMAILPROVIDER.com', port=587) as connection:
            #     connection.starttls()
            #     connection.login(MY_EMAIL, PASSWORD)
            #     connection.sendmail(from_addr=MY_EMAIL, to_addrs='PHONENUMBER@txt.att.net', msg=f"{title}\n{description}")



###### TODOS:

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org 
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com ***Optional technology to recieve data through Text.***
# Send a separate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


########## MAIN PROGRAM STARTS HERE!!: ##########

'''***SENSITIVE INFO!!!
    -Your api key's inputted here to be used as parameters.'''

Alpha_Van_Endpoint = 'https://www.alphavantage.co/query' 
alpha_api_key = 'YOUR KEY HERE'

News_Endpoint = 'https://newsapi.org/v2/top-headlines'
news_api_key = 'YOUR KEY HERE'


''' Alpha Vantage Para:'''
# API Parameters DAILY REQUIREMENTS:
# ❚ Required: function
# The time series of your choice. In this case, function=TIME_SERIES_DAILY
# ❚ Required: symbol
# The name of the equity of your choice. For example: symbol=IBM

stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'TSLA',
    'apikey': alpha_api_key,
}


'''NEWS Para:
https://newsapi.org/docs/endpoints/top-headlines '''

news_parameters = {
    'apiKey': news_api_key,
    'q' : 'Tesla'
}

''' API request for Alpha'''
alpha_request = requests.get(url=Alpha_Van_Endpoint, params=stock_parameters)
alpha_request.raise_for_status()
alpha_stock_data = alpha_request.json()

# target stock float conversion:
previous_day_close = float(alpha_stock_data['Time Series (Daily)'][previous_date]['4. close'])
day_before_close = float(alpha_stock_data['Time Series (Daily)'][day_before_date]['4. close'])

print(f"{previous_date} : {previous_day_close}")
print(f"{day_before_date} : {day_before_close}")

#Data Check:
# change_in_price = is_stable(day_before_close, previous_day_close)
# print(type(change_in_price))

# Variable
change_in_price = is_stable(previous_day_close, day_before_close)
# print(type(change_in_price))

# Conditional Logic check to proceed on send type of info to email/text:
if change_in_price > 5 and change_in_price > 0:
    print("There's a gain. Check the news.")
    good_news = get_news()
    send_news(good_news)
elif change_in_price < -5 and change_in_price < 0:
    print("There's a loss, check the news.")
    bad_news = get_news()
    send_news(bad_news)
else:
    print('Nothing crazy to report. Within the (-/+) 5% threshold')
    
