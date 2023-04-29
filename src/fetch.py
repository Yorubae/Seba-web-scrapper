#!/bin/env python3

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import json
import os
import sys
import urllib3

urllib3.disable_warnings()
class Scraper:
    """ Scrape PDFs from the seba site """
    def __init__(self):
        self.links = []
        self.titles = []
        self.USER = os.getlogin()
        if self.USER != "Yoru":
            self.PATH = f"/home/self.USER/sebaInfo"
        else:
            self.PATH = f"/home/Yoru/yoru-dump/sebaInfo"
        
        if self._check_status():
            html = requests.get('https://www.sebaonline.org/notifications', verify=False)
            self.soup = BeautifulSoup(html.content, 'html.parser')
        else:
            if os.path.exists(f"{self.PATH}/cache/seba.html"):
                self.soup = self.site_cache()
            else:
                print("No internet connection and cache")
                sys.exit(1)

    def lookup_links(self, pattern=None):
        index_X = 0
        for link in self.soup.find_all('a'):
            href = link.get('href')
            title = link.get('title')
            if index_X > 12:
                self.titles.append(title)
            if pattern and pattern in href:
                self.links.append(href)
            index_X += 1
        for _ in range(11):
            self.titles.pop()

    def download_pdfs(self, option: int) -> None:
        try:
            content = requests.get(self.links[int(option)], timeout=10, stream=True, verify=False)
        except requests.ConnectionError as Error:
            print('Something is worng with your wifi')
            print(f"Error: {Error}")
        else:
            total_size = int(content.headers.get('content-length', 0))
            progress_bar = tqdm(unit="B", unit_scale=True,total=total_size)
            with open(f'{self.PATH}/pdfs/{self.titles[int(option) - 1]}.pdf', 'wb') as f:
                for chunk in content.iter_content(chunk_size=128):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))
                progress_bar.close()

    def site_cache(self):
        json_data = json.dumps(self.links, indent=4)
        if os.path.exists(f"{self.PATH}/cache/seba.html"):
            try:
                with open(f'{self.PATH}/cache/seba.html', 'r') as r:
                    soup = BeautifulSoup(r.read(), 'html.parser')
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

        if os.path.exists(f"{self.PATH}/cache/cache.json"):
            try:
                cache_con = open(f"{self.PATH}/cache/cache.json", 'w')
            except Exception as e:
                print(e)
            else:
                cache_con.write(json_data)
                cache_con.close()
        return soup
    
    def _check_status(self) -> bool:
        try:
            requests.get('https://www.google.com/')
            return True
        except ConnectionError:
            return False

if __name__ == "__main__":
    scrape = Scraper()
    scrape.lookup_links("photo")
    scrape.download_pdfs(2)
