#!/usr/bin/env python3

""" corpus_scraper.py:
Scrapes the corpus of each poet in PoemHunter.com's Top 500 into a txt file.
Poet info is loaded from a json file created by poet_scraper.py
author: ingversed
"""

from poet_scraper import get_soup
from bs4 import BeautifulSoup
import json, requests, re, os, time

BASE_URL = 'https://www.poemhunter.com'
POEMS_STRAINER = 'strong a' # identifies poem links
DIR_PATH = 'PoemHunterTop500' # destination directory for text files
POETS_JSON = 'poets.json' # file created by poet_scraper

def get_poets_json():
    poets_file = os.path.join(DIR_PATH, POETS_JSON)
    with open(poets_file, 'r') as input_file:
        poets_json = json.load(input_file)
        return poets_json

def get_lastpage(soup, current_page):
    last_page = soup.select('div.pagination.mb-15 ul > li.next')
    if not last_page:
        last_page = current_page
    else:
        last_page = int(last_page[0].previous_sibling.text)
    return last_page

def main():
    poets_json = get_poets_json()
    for poet in poets_json:        
        poet_link = poets_json[poet]['link']

        current_page = 1
        page_url = '{}{}{}'.format(BASE_URL, poet_link, 'poems/page-')

        page_soup = get_soup(page_url+str(current_page))
        last_page = get_lastpage(page_soup, current_page)
        poems_soup = page_soup.select(POEMS_STRAINER)

        print('Writing corpus of ' + poet + '...')
        while current_page <= last_page:
            for poem_link in poems_soup:           
                poem_soup = get_soup(BASE_URL + poem_link.get('href'))
                poem_title = poem_soup.find('h1', itemprop='name').get_text(strip=True)
                poem_text = poem_soup.find('p', itemprop='text').get_text('\n', strip=True)

                poet_file = os.path.join(DIR_PATH, poet_link[1:-1]+'.txt')
                with open(poet_file, 'a+', encoding='utf-8') as output_file:
                    output_file.write(poem_title + '\n\n')
                    output_file.write(poem_text + '\n\n\n')

            print('-- Finished writing page ' + str(current_page) + '. Last poem written: ' + poem_title)
            if current_page != last_page: 
                current_page += 1
                poems_soup = get_soup(page_url+str(current_page)).select(POEMS_STRAINER)
            else:
                break
            
        print('- Finished writing corpus of ' + poet + '.')


if __name__ == "__main__":
    main()


