from urllib.request import urljoin
from bs4 import BeautifulSoup
import requests
from urllib.request import urlparse
from collections import deque


links_intern = set()
seed_url = "https://en.wikipedia.org/wiki/Sustainable_energy"
depth = 1
queue = deque([])

links_extern = set()


def BFS_crawler(seed_url):
    depth = 1
    temp_urls = set()
    queue.append(seed_url)
    current_url_domain = urlparse(seed_url).netloc
    while (len(queue)) != 0 and len(temp_urls) < 1000 and depth < 6:
        size = len(queue)
        for i in range (0,size):
            current_url = queue.popleft()
            if(current_url not in temp_urls):
                beautiful_soup_object = BeautifulSoup(requests.get(current_url).content, "lxml")
                for anchor in beautiful_soup_object.findAll("a"):
                    href = anchor.attrs.get("href")
                    if(href != "" or href != None):
                        href = urljoin(seed_url, href)
                        href_parsed = urlparse(href)
                        href = href_parsed.scheme
                        href += "://"
                        href += href_parsed.netloc
                        href += href_parsed.path
                        final_parsed_href = urlparse(href)
                        is_valid = bool(final_parsed_href.scheme) and bool(
				final_parsed_href.netloc)
                        if is_valid:
                            queue.append(href)
                            temp_urls.add(href)
                            if current_url_domain not in href and href not in links_extern:
                                print("Extern - {}".format(href))
                                links_extern.add(href)
                                
                            if current_url_domain in href and href not in links_intern:
                                print("Intern - {}".format(href))
                                links_intern.add(href)
        depth +=1             
    return temp_urls


# BFS_crawler(seed_url)