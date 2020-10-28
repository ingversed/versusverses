#!/usr/bin/env python3

""" poet_scraper.py:
Scrapes name, number of poems and link for all PoemHunter.com's Top 500 poets into a json file.
author: ingversed
"""

from bs4 import BeautifulSoup
import json, requests, re, os, time

PAGE_URL = 'https://www.poemhunter.com/p/t/l.asp?a=0&l=Top500&cinsiyet=&Populer_mi=&Classicmi=&Dogum_Tarihi_yil=&Dogum_Yeri=&p='
POETS_STRAINER = 'ol.poets-grid li' # identifies list of poets 
DIR_PATH = 'PoemHunterTop500' # destination directory for text files

def get_soup(PAGE_URL):
    tries = 1
    while True:
        try:
            seconds = 60
            response = requests.get(PAGE_URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, features='html.parser')
            return soup
        
        except requests.exceptions.HTTPError as e:
            print('HTTP Error:', e)
            if response.status_code == 504:
                print('504 Gateway Timeout. Sleeping for ' + str(tries) + ' minute/s')
                time.sleep(seconds * tries)
                tries += 1
                
        except requests.exceptions.ConnectionError as e:
            print('Error Connecting:', e)

        except requests.exceptions.Timeout as e:
            print('Timeout Error:', e)
            print('Sleeping for ' + str(tries) + ' minute/s')
            time.sleep(seconds * tries)
            tries += 1

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)


def main():
    message = "Enter minimum number of poems required for a poet's corpus to be scraped: "
    min_poems = int(input(message)) 

    poets = {}

    page_soup = get_soup(PAGE_URL)
    poet_soup = page_soup.select(POETS_STRAINER)

    last_page = int(page_soup.find('li', 'next').previous_sibling.text)
    current_page = 1

    print('Writing json file...')

    while current_page <= last_page:
        for poet in poet_soup:
            num_poems_string = poet.find('div', 'info').text
            num_poems = int(re.search(r'\d+',num_poems_string)[0])

            if num_poems >= min_poems:
                name = poet.find('a', 'name').text
                link = poet.find('a').get('href')
                poets[name] = { 'num_poems': num_poems, 'link': link }

        current_page += 1
        poet_soup = get_soup(PAGE_URL+str(current_page)).select(POETS_STRAINER)


    poets_file = os.path.join(DIR_PATH, 'poets.json')  
    with open(poets_file, 'w') as fp:
        json.dump(poets, fp)

    print('Finished writing json file.')


if __name__ == "__main__":
    main()


    
