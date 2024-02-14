import streamlit as st
import definitions as defi
import matplotlib.pyplot as plt

st.title('Weather data during years')
year = st.slider('Select year', min_value=2001, max_value=2023, help='description')
month = st.slider('Select month', min_value=1, max_value=12)
station = st.selectbox('Select station', ('PSZCZYNA', 'BRENNA', 'LALIKI'))
st.subheader(f'Information for {station}, {month}.{year}')

df1 = defi.import_extract(year, month)
df = defi.prepare_data(df1)

one_station = df[df['station name'] == station]

max = one_station['temp_max'].max()
min = one_station['temp_min'].min()
rain = one_station['rainfall'].sum()

fig, ax = plt.subplots(figsize=(12, 7))
twin = ax.twinx()

p1, = ax.plot(
    one_station['day'], one_station['temp_max'],
    color='red',
    label='temp. max',
    alpha=0.5
)

p2, = ax.plot(
    one_station['day'], one_station['temp_min'],
    color='blue',
    label='temp. min',
    alpha=0.5
)

p3, = ax.plot(
    one_station['day'], one_station['temp_avg'],
    color='grey',
    label='temp. avg',
    alpha=0.5
)

p4 = twin.bar(
    x=one_station['day'], height=one_station['rainfall'],
    color='lightgrey',
    label='rainfall',
    alpha=0.5
)

ax.axhline(0, c='grey', ls='--')
ax.set_xlim(0)

ax.set_xlabel('Day', fontsize=12)
ax.set_ylabel('Temperature', fontsize=12)
twin.set_ylabel('Rainfall [mm]', fontsize=12)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(handles=[p1, p2, p3, p4], frameon=False)

fig1 = plt.gcf()
fig1.savefig('static/chart.png')
image_url = 'static/chart.png'

st.image(image_url)
