import requests
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import csv
import string

new = ""
old = ""
letter = 'a'
alphabet = string.ascii_lowercase

f = open('fighters.txt', 'w')

fighter_urls = []

for i in alphabet:
    r = requests.get("http://www.fightmetric.com/statistics/fighters?char=" + i + "&page=all")
    soup = BeautifulSoup(r.content, "html5lib")
    fighters = soup.find_all("td", {"class": "b-statistics__table-col"})
    print(i)
    for td in fighters:
        for link in td.find_all('a'):
            new = link.get('href')

            if new == old:
                pass
            else:
                fighter_urls.append(link.get('href'))
                #f.write(link.get('href') + "\n")
            old = link.get('href')

fight_urls = pd.DataFrame(fighter_urls, columns=['link'])
fight_urls.to_csv('fighter urls.csv', index=False)

for s in fighter_urls:
    f.write(s + "\n")

print("file finished writing\n")
f.close()

f = open('fighters.txt', 'r')

url = "None"
for line in f:
    url = line.rstrip('\n')
    #print(line)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")

    fighter_name = soup.find('span', {'class': 'b-content__title-highlight'}).contents[0]
    fighter_name = fighter_name.strip()
    print(fighter_name)

    fighter_record = soup.find('span', {'class': 'b-content__title-record'}).contents[0]
    fighter_record = fighter_record.strip()
    fighter_record = fighter_record.strip('Record: ')
    print(fighter_record)


