
import pandas 
from bs4 import BeautifulSoup
from urllib import request 
import re 
import time 


def scrape_by_initial(initial: str):
    url = "https://www.whisky.com/whisky-database/bottle-search/whisky/fdb/Bottles/List.html?tx_datamintsflaschendb_pi4[searchCriteria][titleStartsWith]=" + initial
    response = request.urlopen(url)

