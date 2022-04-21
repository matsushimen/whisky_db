

from bs4 import BeautifulSoup
import pandas
from urllib import request
import re 
import time

class Scraper:

    def __init__(self):
        self.site = "https://smwsjapan.com/distilleries?limit=all"
        self.out_name = "dist.csv"
        
    def scrape_top(self):
        response_all_dist = request.urlopen(self.site)
        all_dist_source = BeautifulSoup(response_all_dist, 'html.parser')
        ref_uri = re.compile('https://smwsjapan\.com/distilleries/.+')               
        dist_list = []
        for tag in all_dist_source.find_all('a', class_='plain',href=ref_uri):

            dist_list.append(self.scrape_each_dist(tag.get('href')))
            time.sleep(1)

        pandas.DataFrame(dist_list).to_csv(self.out_name, index=None)


    def scrape_each_dist(self, uri):
        response_dist = request.urlopen(uri)
        dist_soup = BeautifulSoup(response_dist, 'html.parser')
        response_dist.close()

        name = dist_soup.select_one('h1.caps').contents[0].strip()
        name_en = uri.rsplit('/')[-1].rsplit('-', 1)[0]
        geo = dist_soup.select_one('div.grid__item:nth-child(6) > span:nth-child(1)').contents[0].strip()

        since = dist_soup.select_one('div.two-thirds:nth-child(2) > span:nth-child(1)').contents[0].strip()
        region = dist_soup.select_one('div.grid__item:nth-child(8) > span:nth-child(1)').contents[0].strip()

        print(name)
        return {'name': name, 'name_en': name_en, 'since': since, 'geo': geo, 'region': region}


if __name__ == '__main__':
    tmp = Scraper()
    tmp.scrape_top()
