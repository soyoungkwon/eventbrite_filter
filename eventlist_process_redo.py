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
    df_filter = price_filter(df_all)
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

# event with filtered price
def price_filter(df):
    df_filter_orderbypage = df[df['Max']>min_price]
    # Price reorder to High--> Low
    df_filter = df_filter_orderbypage.sort_values(['Max'],ascending=False)

    return df_filter

if __name__ == "__main__":
    main()
