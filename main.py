from bs4 import BeautifulSoup
import requests
import csv
import os
import sys
import time
import selenium
from selenium import webdriver
from webscraping_utils import find_publishergames
from webscraping_utils import find_gamesIDs
from webscraping_utils import scrape_gamesprices
from fromgamesdata_utils import publishergames_insights
from fromgamesdata_utils import date_range

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

# Input publishers to analyse
publishers = ['devolver_digital']

# Find all games available to each publishers, and create a dictionary out with them
publishersdict = find_publishergames(publishers)
print(publishersdict)

# Find all of the IDs for each of the game on GOGDB
find_gamesIDs(publishersdict)
print(publishersdict)

# Create tables with prices and discounts for each of the games
scrape_gamesprices(publishersdict)

# Find all price tables for games in list
publishergames_insights(publishersdict)


for publisher in publishersdict.keys():
    # Create a graph with the spread of discounts through time
    discountsthroughtime(publisher)

    # Create a graph with the spread of discounts through time
    allgamesgraph(publisher)

# Create CSV compiling each publisher's relevant descriptive stats
crosspublishercsv_creator(publishersdict)

# Create graph to compare each publisher's relevant descriptive stats
