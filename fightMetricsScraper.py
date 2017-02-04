import requests
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import csv
import datetime
import string

def check(stat):
    if stat == "" or stat == " " or stat == "--" or stat == "\n":
        stat = None
    return stat

new = ""
old = ""
letter = 'a'
alphabet = string.ascii_lowercase

f = open('fighters.txt', 'w')
cf = open('FightMetricStats.csv', 'w')
csv_file = csv.writer(cf)

headers = ['Name', 'Nickname', 'Record', 'Height', 'Weight (lbs)', 'Reach', 'Stance', 'Birth Date', 'Sig. Strikes landed/min', 'strike acc.', 'Sig Strikes taken/min', 'Strike def.', 'TD/15 min', 'TD acc.', 'TD def.', 'sub/15 min']
csv_file.writerow(headers)
#cf.close()

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

#print("file finished writing\n")
f.close()

f = open('fighters.txt', 'r')

url = "None"
for line in f:
    url = line.rstrip('\n')
    #print(line)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")

    try:
        fighter_name = soup.find('span', {'class': 'b-content__title-highlight'}).contents[0]
        fighter_name = fighter_name.strip()
    except AttributeError:
        fighter_name = None
        print("ERROR - NO fighter at " + url)
        continue

    try:
        nickname = soup.find('p', {'class': 'b-content__Nickname'}).contents[0]
        nickname = nickname.strip()
    except AttributeError:
        nickname = None
    else:
        check(nickname)

    try:
        fighter_record = soup.find('span', {'class': 'b-content__title-record'}).contents[0]
        fighter_record = fighter_record.strip().strip('Record: ')
    except AttributeError:
        fighter_record = None

    stats = []
    for li in soup.find_all('li', {'class': 'b-list__box-list-item b-list__box-list-item_type_block'}):
        #print(li.text)
        stats.append(li.text)

    i = 0
    for item in stats:
        if i == 0:
            try:
                fighter_height = item.strip().strip('Height:').strip()
            except AttributeError:
                fighter_height = None
        elif i == 1:
            try:
                fighter_weight = item.strip().strip('Weight:').strip().strip('lbs.').strip()
            except AttributeError:
                fighter_weight = None
        elif i == 2:
            try:
                fighter_reach = item.strip().strip('Reach:').strip()
            except AttributeError:
                fighter_reach = None
        elif i == 3:
            try:
                fighter_stance = item.strip().strip('STANCE:').strip()
            except AttributeError:
                fighter_stance = None
        elif i == 4:
            try:
                fighter_dob = item.strip().strip('DOB:').strip()
                try:
                    fighter_dob = datetime.datetime.strptime(fighter_dob, '%b %d, %Y')
                    fighter_dob = fighter_dob.strftime('%Y-%m-%d')
                except:
                    fighter_dob = None
            except AttributeError:
                fighter_dob = None
        elif i == 5:
            try:
                fighter_slpm = item.strip().strip('SLpM:').strip()
            except AttributeError:
                fighter_slpm = None
        elif i == 6:
            try:
                fighter_stracc = item.strip().strip('Str. Acc.:').strip()
            except AttributeError:
                fighter_stracc = None
        elif i == 7:
            try:
                fighter_sapm = item.strip().strip('SApM:').strip()
            except AttributeError:
                fighter_sapm = None
        elif i == 8:
            try:
                fighter_strdef = item.strip().strip('Str. Def:').strip()
            except AttributeError:
                fighter_strdef = None
        elif i == 10:
            try:
                fighter_tdavg = item.strip().strip('TD Avg.:').strip()
            except AttributeError:
                fighter_tdavg = None
        elif i == 11:
            try:
                fighter_tdacc = item.strip().strip('TD Acc.:').strip()
            except AttributeError:
                fighter_tdacc = None
        elif i == 12:
            try:
                fighter_tddef = item.strip().strip('TD Def.:').strip()
            except AttributeError:
                fighter_tddef = None
        elif i == 13:
            try:
                fighter_subavg = item.strip().strip('Sub. Avg.:').strip()
            except AttributeError:
                fighter_subavg = None

        i += 1

    fighter_name = check(fighter_name)
    nickname = check(nickname)
    fighter_record = check(fighter_record)
    fighter_height = check(fighter_height)
    fighter_weight = check(fighter_weight)
    fighter_reach = check(fighter_reach)
    fighter_stance = check(fighter_stance)
    fighter_dob = check(fighter_dob)
    fighter_slpm = check(fighter_slpm)
    fighter_stracc = check(fighter_stracc)
    fighter_sapm = check(fighter_sapm)
    fighter_strdef = check(fighter_strdef)
    fighter_tdavg = check(fighter_tdavg)
    fighter_tdacc = check(fighter_tdacc)
    fighter_tddef = check(fighter_tddef)
    fighter_subavg = check(fighter_subavg)

    """print(fighter_name)
    print(nickname)
    print(fighter_record)
    print(fighter_height)
    print(fighter_weight)
    print(fighter_reach)
    print(fighter_stance)
    print(fighter_dob)
    print(fighter_slpm)
    print(fighter_stracc)
    print(fighter_sapm)
    print(fighter_strdef)
    print(fighter_tdavg)
    print(fighter_tdacc)
    print(fighter_tddef)
    print(fighter_subavg)"""

    row = [fighter_name,
           nickname,
           fighter_record,
           fighter_height,
           fighter_weight,
           fighter_reach,
           fighter_stance,
           fighter_dob,
           fighter_slpm,
           fighter_stracc,
           fighter_sapm,
           fighter_strdef,
           fighter_tdavg,
           fighter_tdacc,
           fighter_tddef,
           fighter_subavg]

    csv_file.writerow(row)
    print(fighter_name)

try:
    cf.close()
except:
    print("ERROR - Can't close csv file - " + cf)
try:
    f.close()
except:
    print("ERROR - Can't close txt file - " + f)
print("Done!")

