from bs4 import BeautifulSoup 

import pandas as pd

soup = BeautifulSoup(open("specific_dist.html"),'html.parser')

print(soup.select_one('div.grid__item:nth-child(6) > span:nth-child(1)').contents[0].strip())
print(soup.select_one('h1.caps').contents[0].strip())
