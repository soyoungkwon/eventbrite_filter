# read all events
import pandas as pd
import os
import decimal

path_curr = os.getcwd()
max_pages = 50
min_price = 300

# main function
def main():
    df_all = load_all_files()
    df_filter = price_max_extract(df_all)
    df_filter.to_csv(path_curr +'/' + 'eventlist_filtered_300euro.csv', encoding = 'utf-8', index=False)

# load all the csv files
def load_all_files():
    for page in range(max_pages):
        df_onepage = pd.read_csv(path_curr + '/eventlist_csv/' + 'eventlist_by_page' + str(page+1).zfill(2) + '.csv')
        if page ==0:
            df_allpages = df_onepage
        else:
            df_allpages = df_allpages.append(df_onepage, ignore_index =True)
    return df_allpages

# filter pandas with certain price_value
def price_max_extract(df):
    price_list = []
    n_allevent = len(df)
    for event in range(n_allevent):
        price_raw = df['Price'][event]
        # Price in case free/gratis/donation/nan
        if (type(price_raw) == float) or (price_raw == 'Free') or (price_raw == 'Gratis') or (price_raw == 'Donation') or (price_raw == 'Donatie'): # price not written (NaN)
            price_max = 0
        # Price value written
        else:
            price_clean0 = price_raw.decode('ascii', 'ignore')
            # check whether there are min-max or just one price written
            if len(price_clean0.split()) == 2: # min, max value
                [min, max] = price_clean0.split()
                price_onevalue = max
            else:
                price_onevalue = price_clean0

            # check whether the max price has more than 1 comma
            if (price_onevalue.count('.') + price_onevalue.count(','))>1: # more than 1 comma
                price_onevalue1 = price_onevalue.replace(',','')
            else:
                price_onevalue1 = price_onevalue.replace(',', '.')

            # remove all the string ($, R, US)
            price_onevalue1 = price_onevalue1.replace('$', '')
            price_onevalue1 = price_onevalue1.replace('R', '')
            price_onevalue1 = price_onevalue1.replace('US', '')

            price_max = float(price_onevalue1)
        price_list.append(price_max)
    # add another column (Price Max)
    df['Price Max'] = pd.Series(price_list, index=df.index)
    df_filter = df[df['Price Max']>min_price]

    return df_filter

if __name__ == "__main__":
    main()
