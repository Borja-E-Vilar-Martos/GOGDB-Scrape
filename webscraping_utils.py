from bs4 import BeautifulSoup
import requests
import os
import sys
from selenium import webdriver
import time
import urllib.parse

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def find_publishergames(publisherslist = []):
    driver = webdriver.Chrome(executable_path='D:\Python\exercises\Webscraping\chrome\\chromedriver.exe')
    publishersdict = {}

    for publisher in publisherslist:
        publishergameslist = []
        for number in range (1, 200):
            url ='https://www.gog.com/games?devpub={}&page={}&sort=popularity&hide=dlc'.format(publisher, number)
            driver.get(url)
            time.sleep(5)

            source = driver.page_source

            soup = BeautifulSoup(source, 'lxml')
            # uprint(soup.prettify())

            match = soup.body
            if (not any(match.find_all('div', class_='list-view__item'))):
                break

            else:
                for title in soup.find_all('div', class_='product-tile__title'):
                        #  <div class="product-tile__title" ng-bind="tile.data.title">
                    publishergameslist.append(title.text)
                # for title in soup.find_all('div', {'class' : 'product-tile__title'}):
                #     publishergameslist.append(title.text)
                publishergameslist = set(publishergameslist)
                publishergameslist = list(publishergameslist)
                publishersdict.update({publisher : publishergameslist })

    return publishersdict

def find_gamesIDs(publishers = {}):
    for publisher in publishers:
        GOGgamesID = dict()
        for item in publishers[publisher]:
        # item = "Shadow Warrior (2013)"
            itemcheck = item
            itemurl = item.replace(' ', '+').replace(':', '%3A').replace("'", '%27').replace('(', '%28').replace(')', '%29')
            url = 'https://www.gogdb.org/products?search={}'.format(itemurl)

            source = requests.get(url).text
            soup =  BeautifulSoup(source, 'lxml')

            match = soup.body.find('table', class_='shadow rowborder')

            for game in match.find_all('tr'):
                # print(game.prettify())
                if (game.find('td', {'class' : 'col-type'})) and (game.find('td', {'class' : 'col-name prod-unlisted'})):
                    if (game.find('td', {'class' : 'col-type'}).text == 'Game' or 'Package') and (game.find('td', {'class' : 'col-name prod-unlisted'}).find('a', {'class' : 'hoveronly'}).text.strip() == itemcheck):
                        # GOGgamesID = list(GOGgamesID)
                        GOGgamesID.update({itemcheck : game.find('td', class_='col-id').text.rstrip("\n").lstrip("\n")})

                else:
                    continue

            publishers[publisher] = GOGgamesID
    # return GOGgamesID

def scrape_gamesprices(publishersdict = {}):
    for publisher in publishersdict:
        for game in publishersdict[publisher]:
            if 'Demo' in game:
                continue

            url = 'https://www.gogdb.org/product/{}#prices'.format(publishersdict[publisher][game])

            source = requests.get(url).text
            soup =  BeautifulSoup(source, 'lxml')

            # Skip if prices are not available
            if (soup.body.find('div', {'id' : 'tab-prices'}).find('div', {'class': 'textbox shadow'})):
                if (soup.body.find('div', {'id' : 'tab-prices'}).find('div', {'class': 'textbox shadow'}).text.strip() == 'No price data available.'):
                    # publishersdict[publisher].pop(game)
                    continue

            match = soup.body.find('div', {'id': 'page'}).find('div', {'id': 'tab-prices'}).find('table', class_='shadow cellborder')

            # Create CSV as copied from GOGDB
            gameremovecolon = game.replace(':', '')
            file_path = 'D:\Python\exercises\Webscraping\GOGDB\csvsgames\\{}_{}prices.csv'.format(publisher, gameremovecolon)

            with open(file_path, 'w+', newline='') as new_file:
                csv_writer = csv.writer(new_file)
                csv_writer.writerow([game])
                csv_writer.writerow(['Start', 'End', 'Base', 'Final', 'Discount'])
                for price in match.find_all('tr'):
                    line = []
                    for entry in price.find_all('td'):
                        line.append(entry.text)
                    csv_writer.writerow(line)
#
# publishers = ['devolver_digital']
# print(find_publishergames(publishers))
