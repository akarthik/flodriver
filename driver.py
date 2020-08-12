from datetime import datetime

import requests
import urllib.request
import time
from time import sleep

from bs4 import BeautifulSoup
from twilio.rest import Client

#Global Variables
TodaysList = {}

'''
Send SMS using twilio
'''


def sendsms():
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'AC9eb34fb303a7d2b6c72040846a0be897'
    auth_token = '4d1356ed8518a5da8205e99a70673920'
    client = Client(account_sid, auth_token)
    for msg in TodaysList.keys():
        if(TodaysList[msg]== False):
             print(msg)
             numbers_to_message = ['+15122419428', '+15122210780']
             for number in numbers_to_message:
                 message = client.messages.create(
                 body=msg,
                 from_='+12029533287',
                 to=number
                 )
             TodaysList[msg] = True

'''
Scrape the website for alerts
'''


def parse():
    # Set the URL you want to webscrape from
    url = 'https://app.flowalgo.com/'

    payload = {
        'amember_login': 'akarthik47',
        'amember_pass': 'Cloud.123$'
    }
    r = requests.head(url, allow_redirects=True)
    print(r.url)
    now = datetime.now()

    with requests.Session() as session:
        response = session.post(r.url, data=payload)
        # print(response.text)
        # Parse HTML and save to BeautifulSoup object¶
        html_soup = BeautifulSoup(response.text, "html.parser")
        rows1 = html_soup.find_all('div', class_='aai_signal bullish ontrack')
        rows2 = html_soup.find_all('div', class_='aai_signal bearish ontrack')
        rows = rows1 + rows2
        print(type(rows))
        print(len(rows))

        for row in rows:
            items = row.find_all('div')
            date_str = items[0].text
            symbol_str = items[1].text
            price_str = items[2].text
            sentiment_str = items[3].text.strip()
            # Time from the span string
            span_items = row.find_all('span')
            time_str = span_items[0].attrs['title']
            msg = date_str + ' ' + time_str + ', ' + symbol_str + ', ' + price_str + ', ' + sentiment_str
            date_time_str = date_str + '/' + str(now.year) + ' ' + time_str
            date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y %H:%M %p')
            #check if todays
            if(now.date() == date_time_obj.date()):
                if (msg not in TodaysList.keys()):
                     TodaysList[msg] = False
            else:
                if(msg in TodaysList.keys()):
                    TodaysList.pop(msg)


# Main Code starts here
def main():
    while True:
        print ('Checking...')
        parse()
        sendsms()
        print ('Sleeping...')
        sleep(1)

# Call the main
main()