import urllib2, bs4, time, datetime, arrow
import pandas as pd
import numpy as np


def get_date(df):
    df['date'] = ''
    for entry in df['date0'].index:
        if df['date0'][entry] not in ('', 'no date'):
            date_list = df['date0'][entry].split()
            date = str(date_list[1] + ' ' + date_list[2].strip(',') + ' ' + date_list[3])
            date_structure = time.strptime(date, "%B %d %Y")
            df['date'][entry] = datetime.date(date_structure[0], date_structure[1], date_structure[2])
        else:
            df['date'][entry] = datetime.date(2000, 1, 1)
    return df


def main():
    # Point to RSS
    rss = "http://dlab.berkeley.edu/training/rss.xml"

    # Pull RSS data
    rss_data = bs4.BeautifulSoup(urllib2.urlopen(rss).read())
    
    # Pull items
    items = rss_data.find_all('item')

    # Listify
    title_list = []
    url_list = []
    for item in items:
        if int(item.find_next('pubdate').text[12:17]) > 2013:
            title_list.append(item.find_next('title').text)
            url_list.append(item.find_next('link').text)

    # Dictionary (how to ensure 1-to-1 match?)
    rss_dict = {'title' : title_list, 'url' : url_list}

    # DataFrame
    df = pd.DataFrame(rss_dict)

    # Pull dates
    # How to determine, ahead-of-time, how many date entries there could be?
    df['date0'] = ''
    df['date1'] = ''
    df['date2'] = ''
    df['date3'] = ''
    df['date4'] = ''
    for item in df.url.index:
        if df.title[item] != 'Training Archive':
            event_url = df.url[item]
            test_page = bs4.BeautifulSoup(urllib2.urlopen(event_url))

            # Pull content
            content = test_page.find_all('div', class_ = 'span9')
            date_info = content[0].find_all('span', class_ = 'date-display-single')

            # Date: handles multiple-entries
            for i in range(0, len(date_info)):
                col = 'date' + str(i)
                try:
                    df[col][item] =  date_info[i].text
                except:
                    df[col][item] = ''

    # Create date variable based on first date
    df = get_date(df)

    # Remove duplicates
    df = df.drop_duplicates(subset = ['title', 'date0', 'date1', 'date2'])
    
    # Sort
    return df.sort(columns = 'date', ascending = False)




if __name__ == "__main__":
    main()