import pandas as pd
from zipfile import ZipFile
import requests
import os

link = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/'
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
all_table = []
for year in range(2001, 2024):
    for month in months:
        zip_url = f'{link}/{year}/{year}_{month}_k.zip'
        filename = f'{year}_{month}_k.zip'
        file = f'k_d_{month}_{year}.csv'
        download_path = f'data/{filename}'
        extracted_path = 'temp'

        response = requests.get(zip_url)
        with open(download_path, 'wb') as zip_file:
            zip_file.write(response.content)

        with ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_path)

        df = pd.read_csv(f'temp/{file}', encoding='unicode_escape', header=None)

        df = df.drop(columns=[5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17])
        header = ['station code', 'station name', 'year', 'month', 'day', 'temp_avg']
        df.columns = header
        all_table.append(df)

    # file removing
        os.remove(download_path)
        os.remove(f'temp/{file}')
        os.remove(f'temp/k_d_t_{month}_{year}.csv')

print(type(all_table))
print(all_table)

df_all = pd.DataFrame()
for i in range(len(all_table)):
    df_all = pd.concat([df_all, all_table[i]])

# print(df_all.info())
df_all.to_csv('static/df_all.csv', sep=',', index=False, encoding='utf-8')
