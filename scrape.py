'''scrape.py: Scrape historical end-of-season data from sports-reference.com'''

from bs4 import BeautifulSoup
import requests
import csv
from tqdm import tqdm
from time import sleep

years =  [i for i in range(1993, 2020)]

def write_table(table, year):
    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
    with open('data/{}data'.format(year), 'w') as f:
        for row in output_rows:
            f.write(",".join(row) + '\n')

for year in tqdm(years, desc='Downloading data...'):
    sleep(1.0)
    page = requests.get('https://www.sports-reference.com/cbb/seasons/{}-school-stats.html'.format(year))
    soup = BeautifulSoup(page.content,features="html.parser")
    table = soup.find('table', {'class': 'sortable stats_table'})
    write_table(table, year)

