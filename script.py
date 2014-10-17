import bs4
import urllib2
import pandas as pd


def main():
    # Point to RSS
    rss = "http://dlab.berkeley.edu/training/rss.xml"

    # Pull RSS data
    rss_data = bs4.BeautifulSoup(urllib2.urlopen(rss).read())

    # Pull title and url data
    titles = rss_data.find_all('title')
    urls = rss_data.find_all('link')

    # Check equality ?
    len(titles)
    len(urls)

    # Listify
    t_list = list(titles)
    u_list = list(urls)

    # Remove tags
    title_list = []
    url_list   = []
    for entry in range(0, len(t_list)):
        title_list.append(str(t_list[entry])[7 : -8])
        url_list.append(str(u_list[entry])[6 : -7])

    # Dictionary (how to ensure 1-to-1 match?)
    rss_dict = {'title' : title_list, 'url' : url_list}

    # DataFrame
    df = pd.DataFrame(rss_dict)

    # Dates
    # How to determine, ahead-of-time, how many date entries there could be?
    df['date0'] = ''
    df['date1'] = ''
    df['date2'] = ''
    for item in df.url.index:
        if df.title[item] != 'Training Archive':
            try:
                event_url = df.url[item]
                test_page = bs4.BeautifulSoup(urllib2.urlopen(event_url))

                # Date: handles multiple-entries
                date_info = test_page.find_all('span', class_ = 'date-display-single')
                for i in range(0, len(date_info)):
                    col = 'date' + str(i)
                    df[col][item] =  date_info[i].text
            except:
                df.date0[item] = 'no date'

    return df




if __name__ == "__main__":
    main()