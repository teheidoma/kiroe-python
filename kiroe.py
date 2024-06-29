import datetime
import re

from bs4 import BeautifulSoup
from datetime import datetime
import requests


def datetime_from_hour(hour):
    return datetime.now().replace(hour=int(hour), minute=0, second=0, microsecond=0)


soup = BeautifulSoup(requests.get('https://kiroe.com.ua').text, 'html.parser')

info = soup.select_one('#info_popup .popup_inner div').text.replace('\r', '')
regex = re.compile('1 та 2 черги: (.*)')
start_hours = list(map(lambda x: datetime_from_hour(x.split('-')[0]), regex.findall(info)[0].split('; ')))
outages = list(filter(lambda x: x > datetime.now(), start_hours))
if outages.__len__() > 0:
    outages.sort(key=lambda x: x.time())
    print(f'⚡ {(outages[0] - datetime.now().replace(microsecond=0))}')
else:
    print(f'No outages for today!')
