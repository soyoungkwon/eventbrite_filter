# web scrap using Beautifulsoup
# eventbrite

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys

path_curr = os.getcwd()
url = 'https://www.eventbrite.com/d/netherlands/all-events/'
max_pages = 50

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
    event_pd_clean = clean_pd(event_pd)

    # save pandas to csv file
    event_pd_clean.to_csv(path_curr +'/eventlist_csv/' + 'eventlist_by_page' + str(page+1).zfill(2) +'.csv', encoding = 'utf-8', index=False)

# collect event websites for each page
def trade_spider(url, page):
    weblist = []
    eventlist = []
    # for page in range(max_pages):
    full_url = url + '?page='+ str(page+1)
    source_code = requests.get(full_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    # extract link
    hrefsoup = soup.findAll('a', {'class':'eds-media-card-content__action-link'})
    hrefsoup_half = hrefsoup[1::2]
    # extract event name
    eventsoup = soup.findAll('div', {'data-spec':'event-card__formatted-name'})
    eventsoup_half = eventsoup
    for link in range(len(hrefsoup_half)):
        href = hrefsoup_half[link].get('href')
        weblist.append(href)

        event_name = eventsoup_half[link].text
        eventlist.append(event_name)
        # page += 1
    return weblist, eventlist

# check html of each page & get price info
def extract_event(weblinks):
    price_list = []
    n_event = len(weblinks)
    for event in range(n_event):
        webhtml = requests.get(weblinks[event])
        soup = BeautifulSoup(webhtml.content, 'html.parser')
        obj = soup.find('div', {'class': 'js-display-price'})
        if isinstance(obj, type(None)):
            print(obj)
            string_content = 'NaN'
        else:
            print(obj)
            string_content = obj.text

        price_list.append(string_content)
    return price_list


# clean the pandas
def clean_pd(event_pd):
    n_event = len(event_pd)
    # event name is duplicated, so remove the half of the string
    for event in range(n_event):
        eventname_length = len(event_pd['Event'][event])
        event_pd['Event'][event] = event_pd['Event'][event][0:eventname_length/2]

    # Price has strange values
    event_pd['Price'] = event_pd['Price'].str.replace('\n\t', '')
    event_pd['Price'] = event_pd['Price'].str.replace('\n', '')
    return event_pd

# main
# input = "url"
# input1 = page_number
if __name__ == "__main__":

    main(url, max_pages)
