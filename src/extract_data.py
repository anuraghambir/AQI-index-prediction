import os
import sys

import requests
from bs4 import BeautifulSoup
import csv

class extract_data:
    def get_html_data(self):
        url = ''
        for year in range(2001, 2022):
            for month in range(1, 13):
                if month < 10:
                    url = 'https://en.tutiempo.net/climate/0{}-{}/ws-702610.html'.format(month, year)
                else:
                    url = 'https://en.tutiempo.net/climate/{}-{}/ws-702610.html'.format(month, year)
                try:
                    htmls = requests.get(url, verify=False)
                    html_utf = htmls.text.encode('utf=8')
                    if not os.path.exists('Data/Html_data/{}'.format(year)):
                        os.makedirs('Data/Html_data/{}'.format(year))
                    with open("Data/Html_data/{}/{}".format(year, month), "wb") as output:
                        output.write(html_utf)
                except:
                    print("No data available for this month")

            sys.stdout.flush()

    def combine_data(self):
        #url = ''
        headers = ['Date', 'Average Temperature', 'Maximum temperature', 'Minimum temperature', 'Atmospheric pressure at sea level', 'Average relative humidity', 'Total rainfall and / or snowmelt', \
                   'Average visibility', 'Average wind speed', 'Maximum sustained wind speed', 'Maximum speed of wind', 'Indicate if there was rain or drizzle (In the monthly average, total days it rained)',\
                   'Snow', 'Thunderstorm', 'Fog']
        table_data = []
        for year in range(2001, 2022):
            for month in range(1, 13):
                try:
                    file_url = open("Data/Html_data/{}/{}".format(year, month), 'rb')
                    text = file_url.read()

                    soup = BeautifulSoup(text, 'html.parser')
                    # print(soup.prettify())

                    try:
                        _div = soup.find("div", attrs={"class": "mt5 minoverflow tablancpy"})
                        _table = _div.find("table", attrs={"class":"medias mensuales numspan"}).findAll("tr")
                            # _table.tbody
                        print(_table[:10])
                        break
                        t_headers = _table[0]
                        t_data = _table[1:]
                        for tr in t_data:
                            t_row = {}
                            for i, td in enumerate(tr.findAll("td")):
                                if i == 0:
                                    d = td.text.replace('\n', '').strip()
                                    str_date = str(d).zfill(2) + '/' + str(month).zfill(2) + '/' + str(year).zfill(4)
                                    t_row[headers[i]] = str_date
                                else:
                                    t_row[headers[i]] = td.text.replace('\n', '').strip()
                            table_data.append(t_row)
                        #print(table_data)
                        #break
                    except Exception as e:
                        print(e)
                except:
                    pass


        with open(f"data.csv", 'w') as out_file:
            writer = csv.DictWriter(out_file, headers)
            writer.writeheader()
            for row in table_data:
                if row:
                    writer.writerow(row)





