import urllib2, bs4, datetime, random, ConfigParser, re, math, itertools, logging, os
from twitter import Twitter, OAuth
from time import sleep
import pandas as pd
import dateutil.parser as parser


def load_rss(user_rss):
    rss = user_rss
    rss_data = bs4.BeautifulSoup(urllib2.urlopen(rss).read())
    return rss_data.find_all('item')


def df_rss(items):
    title_list = []
    url_list = []
    for item in items:
        if int(item.find_next('pubdate').text[12:17]) > 2013:
            title_list.append(item.find_next('title').text)
            url_list.append(item.find_next('link').text)

    rss_dict = {'title' : title_list, 'url' : url_list}
    return pd.DataFrame(rss_dict)


def df_dates(df):
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
    return df


def first_date(df):
    df['date'] = ''
    for entry in df['date0'].index:
        if df['date0'][entry] not in ('', 'no date'):
            date_list = df['date0'][entry].split()
            df['date'][entry] = parser.parse(date_list[1] + ' ' + date_list[2] + ' ' + date_list[3]).date()
    return df


def twitter_message(line):
    config= ConfigParser.ConfigParser()
    config.read('/Users/JS/Code/DLab/config.cfg')

    oauth = OAuth(config.get('OAuth','accesstoken'),
                  config.get('OAuth','accesstokenkey'),
                  config.get('OAuth','consumerkey'),
                  config.get('OAuth','consumersecret'))

    t = Twitter(auth=oauth)
    t.statuses.update(status=line)


def main():
    url = 'http://dlab.berkeley.edu/training/rss.xml'
    # Load RSS Content
    items = load_rss(url)

    # DataFrame: titles, URLs
    df = df_rss(items)

    # DataFrame: titles, URLs, date(s)
    df = df_dates(df)

    # DataFrame: date variable based on date0
    df = first_date(df)
    
    # DataFrame: remove duplicates
    df = df.drop_duplicates(subset = ['title', 'date0', 'date1', 'date2', 'date3', 'date4'])

    # DataFrame: subset only records n days in the future
    forward_days = 7
    df = df[df['date'] == datetime.date.today() + datetime.timedelta(days=forward_days)].reset_index(drop=True)

    # DataFrame: proceed if events exist n days in the future
    if len(df) == 0:
        pass
    else:
        # Message variables & dict
        for i in df.title.index:
            title = df['title'][i]
            date = df['date'][i].strftime('%m/%d')
            link = df['url'][i]

            # Create dictionary
            message_dict = {
            0 : str('Don\'t miss "' + title + '" happening on ' + date + '. Sign up now: ' + link), 
            1 : str('Register for our upcoming workshop, "' + title + '." ' + link), 
            2 : str('"' + title + '" happens on ' + date + '. Register now: ' + link), 
            3 : str('Sign up for "' + title + '," ' + date + '. Register at this link: ' + link), 
            4 : str('Join us for "' + title + '" on ' + date + '. Sign up at ' + link), 
            5 : str('Register now for "' + title + '," ' + date + ': ' + link)
            }

            # Check message length, link always at most 22 chars
            # What if no spaces? Should not happen, but still
            line = ''
            while line == '':
                # Random message
                seed = random.randint(0, 5)
                if len(message_dict[seed][:message_dict[seed].rfind(' ') + 23]) <= 140:
                    line = message_dict[seed]
            twitter_message(line)
            n_seconds = random.randint(60, 300) * 60
            sleep(n_seconds)




if __name__ == "__main__":
    main()