import pandas as pd
from zipfile import ZipFile
import requests
import os

link = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/'


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
def prepare_data(df):
    df = df.drop(columns=[6, 8, 10, 11, 12, 14, 15, 16, 17])
    header = ['station code', 'station name', 'year', 'month', 'day', 'temp_max', 'temp_min', 'temp_avg', 'rainfall']
    df.columns = header
    return df


def create_dataset(month, station):
    all_table = []
    if month < 10:
        month1 = '0' + str(month)
    else:
        month1 = month

    for year in range(2001, 2024):
        zip_url = f'{link}/{year}/{year}_{month1}_k.zip'
        filename = f'{year}_{month1}_k.zip'
        file = f'k_d_{month1}_{year}.csv'
        download_path = f'data/{filename}'
        extracted_path = 'temp'

        response = requests.get(zip_url)
        with open(download_path, 'wb') as zip_file:
            zip_file.write(response.content)

        with ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_path)

        df = pd.read_csv(f'temp/{file}', encoding='unicode_escape', header=None)

        df = df.drop(columns=[6, 8, 10, 11, 12, 14, 15, 16, 17])
        header = ['station code', 'station name', 'year', 'month', 'day', 'temp_max', 'temp_min', 'temp_avg',
                  'rainfall']
        df.columns = header
        all_table.append(df)

        # file removing
        os.remove(download_path)
        os.remove(f'temp/{file}')
        os.remove(f'temp/k_d_t_{month1}_{year}.csv')

    for year in range(1951, 2000, 5):
        for i in range(5):
            zip_url = f'{link}/{year}_{year + 4}/{year + i}_k.zip'
            filename = f'{year + i}_k.zip'
            file = f'k_d_{year + i}.csv'
            download_path = f'data/{filename}'
            extracted_path = 'temp'

            response = requests.get(zip_url)
            with open(download_path, 'wb') as zip_file:
                zip_file.write(response.content)

            with ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_path)

            df = pd.read_csv(f'temp/{file}', encoding='unicode_escape', header=None)

            df = df.drop(columns=[6, 8, 10, 11, 12, 14, 15, 16, 17])
            header = ['station code', 'station name', 'year', 'month', 'day', 'temp_max', 'temp_min', 'temp_avg',
                      'rainfall']
            df.columns = header
            all_table.append(df)

            # file removing
            os.remove(download_path)
            os.remove(f'temp/{file}')
            os.remove(f'temp/k_d_t_{year + i}.csv')

    df_all = pd.DataFrame()
    for i in range(len(all_table)):
        df_all = pd.concat([df_all, all_table[i]])

    df_all = df_all[df_all['month'] == month]
    df_all = df_all[df_all['station name'] == station]

    return df_all


def one_year(df, year):
    df = df[df['year'] == year]
    return df
