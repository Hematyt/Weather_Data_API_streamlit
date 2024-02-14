import streamlit as st
import definitions as defi
import matplotlib.pyplot as plt

station_list = ('PSZCZYNA', 'BRENNA', 'JAB£ONKA', 'POLANA CHOCHO£OWSKA',
       'RADZIECHOWY', '£AZY', 'JASTRZÊBIA', 'LIMANOWA', '£¥CKO',
       'KRO\x8cCIENKO', 'NIEDZICA', 'BUKOWINA TATRZAÑSKA',
       'DOLINA PIÊCIU STAWÓW', 'PIWNICZNA', 'PORONIN', 'MSZANA DOLNA',
       'DYNÓW', 'SOLINA-JAWOR', 'KOMAÑCZA', 'DRONIOWICE', 'LGOTA GÓRNA',
       'KRAKÓW-OBSERWATORIUM', 'BORUSOWA', '\x8cWIÊTY KRZY¯', 'STASZÓW',
       'JAROCIN', 'CIESZANÓW', 'STRZY¯ÓW', 'CEBER', 'RADZYÑ', 'PUCZNIEW',
       'SKIERNIEWICE', 'JARCZEW', 'PU£AWY', 'GORZYÑ', 'BABIMOST',
       'WIELICHOWO', 'KO£UDA WIELKA', 'LEGIONOWO', 'WARSZAWA-BIELANY',
       'WARSZAWA-FILTRY', 'PU£TUSK', 'WARSZAWA-OBSERWATORIUM II',
       'SZEPIETOWO', 'BIA£OWIE¯A', 'GOLENIÓW', 'CHRZ¥STOWO',
       'BIEBRZA-PIEÑCZYKÓWEK', 'MARIANOWO II', 'RÓ¯ANYSTOK',
       'GDAÑSK-RÊBIECHOWO', 'LIDZBARK WARMIÑSKI', 'OLECKO')

st.title('Weather data during years')
year = st.slider('Select year', min_value=2001, max_value=2023, help='select year between 2001 and 2023')
month = st.slider('Select month', min_value=1, max_value=12)
station = st.selectbox('Select station', station_list)
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

st.write(f'Temperature max: {max}')
st.write(f'Temperature min: {min}')
st.write(f'Rainfall total: {rain}')
st.image(image_url)
