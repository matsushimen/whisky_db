
import pandas 
from bs4 import BeautifulSoup
from urllib import request 
import re 
import sys

base_url = "https://www.whisky.com"
def scrape_by_initial(initial: str)->list:
    print(initial)
    url = "https://www.whisky.com/whisky-database/bottle-search/whisky/fdb/Bottles/List.html?tx_datamintsflaschendb_pi4[searchCriteria][titleStartsWith]=" + initial
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    req = request.Request(url=url, headers=headers)
    response = request.urlopen(req)
    soup = BeautifulSoup(response,features="html.parser")
    whiskies = []
    try:
        last_url = soup.select_one('div.pagination:nth-child(6) > ul:nth-child(1) > li:nth-child(3) > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)')['href']
        print(last_url)
        last_page_num = int(last_url.rsplit('=')[-1])
        child_page_url_base = url + '&tx_datamintsflaschendb_pi4%5BcurPage%5D='
        for num in range(1, last_page_num+1):
            child_page_url = child_page_url_base + str(num)
            whiskies.extend(scrape_by_page_num(child_page_url))
    except TypeError:
        child_page_url = url
        whiskies.extend(scrape_by_page_num(child_page_url))
    return whiskies
        

def scrape_by_page_num(url: str)-> list:
    print("scrape by page num")
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    req = request.Request(url=url, headers=headers)
    response = request.urlopen(req)
    soup = BeautifulSoup(response,features="html.parser")

    whiskies = []
    whisky_pages = set([x.a['href'] for x in soup.select('div.resultlist:nth-child(7) > div')])
    if len(whisky_pages) == 0:
        whisky_pages = set([x.a['href'] for x in soup.select('div.resultlist:nth-child(8) > div')])
    print(whisky_pages)
    for whisky in whisky_pages:
        whisky_url = base_url + whisky

        whiskies.append(scrape_by_whisky(whisky_url))

    return whiskies

def scrape_by_whisky(url:str)->dict:

    print("scrape by whisky")
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    req = request.Request(url=url, headers=headers)
    response = request.urlopen(req)
    soup = BeautifulSoup(response,features="html.parser")

    name = " ".join(filter(lambda y: y!="", [x.strip().replace(" ","") for x in soup.select_one('.flaschenIdentifier').strings])).strip()
    try: 
        dist_link = soup.select_one('tr.brennerei > td:nth-child(1) > span > a')['href']
    except:
        dist_link = ""
    try:
        age = " ".join([x.strip() for x in soup.select_one('.fassnummern > td:nth-child(1) > span:nth-child(2)').strings]).strip()
    except:
        age = ""
    try:
        whisky_type = " ".join([x.strip() for x in soup.select_one('.sorte > td:nth-child(1) > span:nth-child(2)').strings]).strip()
    except:
        whisky_type = ""
    try:
        ABV = " ".join([x.strip() for x in soup.select_one('.alkoholgehalt > td:nth-child(1) > span:nth-child(2)')]).strip().replace("%","")
    except:
        ABV = ""

    whisky_info = {"name": name, "age": age, "whisky_type": whisky_type, "ABV": ABV}

    if dist_link != "":
        dist_info = scrape_by_distillary(base_url + dist_link)
    else:
        dist_info = {"dist_name": "", "geo": "", "land": '', "region": '', "company": ''}

    whisky_info.update(dist_info)
    return whisky_info

def scrape_by_distillary(url: str)-> dict:
    print('scrape_by_dist')
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    req = request.Request(url=url, headers=headers)
    response = request.urlopen(req)
    soup = BeautifulSoup(response,features="html.parser")

    name = " ".join(filter(lambda y: y!="", [x.strip() for x in soup.select_one('.brennereien-detail > div:nth-child(1) > div:nth-child(1) > h1:nth-child(1)').strings])).strip()
    geo = ""
    try:
        geo = "".join(filter(lambda x: re.match(r"/whisky-database/distilleries.html", x.get('href')), soup.select('#attributes > tr > td > span > a')))
    except:
        geo = ""
    land = ''
    region = ''
    company = ''
    for span in soup.select('#attributes > tr > td > span > span'):
        if span.get('class') == 'land':
            land = span.text.strip().replace(',', '')
        elif span.get('class') == 'region':
            region = span.text.strip().replace(',', '')
    for a in soup.select('#attributes > tr > td > span > a') :
        if re.match('Company', a.get('href')):
            company = a.text.strip()
    return {"dist_name": name, "geo": geo, "land": land, "region": region, "company": company}


if __name__ == "__main__":
    args = sys.argv
    initial = args[1]
    whiskies = []
    whiskies.extend(scrape_by_initial(initial))
    pandas.DataFrame(whiskies).to_csv("whiskies.csv", index=None, mode='a')
