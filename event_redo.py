# event list redo
# web scrap using Beautifulsoup
# eventbrite

# web scrap using Beautifulsoup
# eventbrite

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
import collections

path_curr = os.getcwd()
url = 'https://www.eventbrite.com/d/netherlands/all-events/'
# page = 0
max_pages = 1#50
trash_price_str = ['$', 'R', 'US']
free_list = ['Free','Gratis','Donation','Donatie','NaN']

# for each page
def main(url, max_pages):
    for page in range(max_pages):
        main_page(page)

# main function
def main_page(page):
    print(page)
    # create weblinks, eventlists as LIST
    weblinks, eventlists = trade_spider(url, page)

    # change into pandas
    event_data = {'Event': eventlists}
    event_pd = pd.DataFrame(event_data)
    event_pd.insert(1, 'Link', weblinks)

    # add price into pandas
    price_lists = extract_event(weblinks)
    event_pd.insert(2, 'Price', price_lists)
    event_pd = clean_pd(event_pd)
    price_max_lists = get_max_price(event_pd)
    event_pd.insert(3, 'Max', price_max_lists)
    # add max price into pandas
    # save pandas to csv file
    event_pd.to_csv(path_curr +'/eventlist_csv/' + 'eventlist_by_page' + str(page+1).zfill(2) +'.csv', encoding = 'utf-8', index=False)


# collect event websites for each page
def trade_spider(url, page):
    weblist = []
    eventlist = []
    # extract html sources
    full_url = url + '?page='+ str(page+1)
    source_code = requests.get(full_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    # extract link
    hrefsoup = soup.findAll('aside', {"class","eds-media-card-content__image-container"})#('a', {'class': "eds-media-card-content__action-link"})#")

    # extract event name
    eventsoup = soup.findAll('div', {'data-spec':'event-card__formatted-name'})
    # eventsoup_half = eventsoup#[0:20]

    # href_link, event_name extract
    for link in range(len(hrefsoup)):
        # links extract
        aclass = hrefsoup[link].findAll('a')
        href = aclass[0].get('href')
        weblist.append(href)

        # evnet_name extract
        divsoup = eventsoup[link].find('div', {'class', 'eds-is-hidden-accessible'})
        event_unicode = divsoup.text # get only text part
        event_name = event_unicode.encode('ascii', 'ignore') # remove ascii coding
        eventlist.append(event_name)

    # change list --> orderedcit --> list (to remove redundant element)
    weblist = list(collections.OrderedDict.fromkeys(weblist))
    eventlist = list(collections.OrderedDict.fromkeys(eventlist))
    # print(eventlist)
    return weblist, eventlist

# check html of each page & get price info
def extract_event(weblinks):
    price_list = []
    n_event = len(weblinks)
    for event in range(n_event):
        webhtml = requests.get(weblinks[event])
        soup = BeautifulSoup(webhtml.content, 'html.parser')
        obj = soup.find('div', {'class': 'js-display-price'})
        if isinstance(obj, type(None)) or (obj.text == 'Free'): # in case of price empty
            print(obj)
            price_long = 'NaN'
        else: # price is written
            price_string = obj.text
            price_long = price_string#.encode('ascii', 'ignore') #
        print(price_long)
        price_list.append(price_long)
    return price_list

# clean the pandas
def clean_pd(event_pd):

    # Price has strange values
    event_pd['Price'] = event_pd['Price'].str.replace('\n\t', '')
    event_pd['Price'] = event_pd['Price'].str.replace('\n', '')
    return event_pd

def get_max_price(event_pd):
    n_event = len(event_pd)
    max_price_list = []

    # Only max Price (1. check number of values (0-2), 2. 29,8 --> 29.8, 3. )
    for event in range(n_event):
        price_raw = event_pd['Price'][event]
        price_str = price_raw.encode('ascii', 'ignore')
        # price split into 2 values
        if len(price_str.split()) == 2: # min, max value
            [min_str, max_str] = price_str.split()
            price_onevalue = (max_str) # change into number
        else: # one value is written in price

            # price not written or free
            if (price_str in free_list) | (price_str == ''):
                price_onevalue = str(0)
            else: # just one number
                price_onevalue = price_str

        # check whether the max price has more than 1 comma
        if (price_onevalue.count('.') + price_onevalue.count(','))>1: # more than 1 comma
            price_onevalue1 = price_onevalue.replace(',','')
        else: # one or zero comma (e.g., 29,8 --> 29.8)
            price_onevalue1 = price_onevalue.replace(',', '.')
        # remove all the string ($, R, US)
        price_onevalue1 = price_onevalue1.replace('$', '')
        price_onevalue1 = price_onevalue1.replace('R', '')
        price_onevalue1 = price_onevalue1.replace('US', '')
        # each event
        price_max = float(price_onevalue1)
        max_price_list.append(price_max) # each event
    return max_price_list

# main
# input = "url"
# input1 = page_number
if __name__ == "__main__":

    main(url, max_pages)
