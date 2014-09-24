import bs4
import urllib2

rss = "http://dlab.berkeley.edu/training/rss.xml"

page = bs4.BeautifulSoup(urllib2.urlopen("http://dlab.berkeley.edu/training/intro-data-visualization-arcgis-0").read())

print(page.find('span', {"class" : "date-display-single"}))
