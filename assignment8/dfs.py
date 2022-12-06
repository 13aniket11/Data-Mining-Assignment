import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import pandas as pd

seed_url = "https://en.wikipedia.org/wiki/Sustainable_energy"

def is_valid(url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

def getLinks(url):
    reqs = None
    try:
        reqs = requests.get(url,timeout=5)
    except:
        return []

    urls = []
    if reqs:
        soup = BeautifulSoup(reqs.text, 'html.parser')
        
        for link in soup.find_all('a'):
            urls.append(link.get('href'))
    return urls

def DFS_crawler(seedLink):
    dict = {}
    data1 = set()
    def dfs(link,level):
        if level==3 or not is_valid(link):
            return

        print(link)
        data1.add(link)

        dict[link] = True
        links = getLinks(link)

        for i in links:
            if not i in dict.keys():
                dfs(i,level+1)        
        
    dfs(seedLink,0)
    print("----------------")
    # print(data1)
    return data1
       
# DFS_crawler(seed_url)