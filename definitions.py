import pandas as pd
from zipfile import ZipFile
import requests
import os


link = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/'
# year = '2023'
# month = '01'


# open zip folder
def import_extract(year, month):
    if month < 10:
        month = '0' + str(month)
    zip_url = f'{link}/{year}/{year}_{month}_k.zip'
    filename = f'{year}_{month}_k.zip'
    file = f'k_d_{month}_{year}.csv'
    download_path = f'data/{filename}'
    extracted_path = 'temp'

    try:
        # Download the zip file
        response = requests.get(zip_url)
        with open(download_path, 'wb') as zip_file:
            zip_file.write(response.content)

        with ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_path)

        df = pd.read_csv(f'temp/{file}', encoding='unicode_escape', header=None)

        # file removing
        os.remove(download_path)
        os.remove(f'temp/{file}')
        os.remove(f'temp/k_d_t_{month}_{year}.csv')
        return df

    except Exception as e:
        return f"Error: {str(e)}"


# data preparation
def prepare_data(df_name):
    df_name = df_name.drop(columns=[6, 8, 10, 11, 12, 14, 15, 16, 17])
    header = ['station code', 'station name', 'year', 'month', 'day', 'temp_max', 'temp_min', 'temp_avg', 'rainfall']
    df_name.columns = header
    return df_name
