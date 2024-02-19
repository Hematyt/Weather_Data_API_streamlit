import definitions as defi
import pandas as pd

station = 'PSZCZYNA'
month = 1
year = 2019

data = pd.read_csv('static/df_all.csv')
data = data[data['station name'] == station]

print(defi.chart3(data, month, year))
