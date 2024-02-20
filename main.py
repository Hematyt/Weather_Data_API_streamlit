import streamlit as st

# import function from other files
import definitions
import charts

st.title('Weather data during years')
year = st.slider('Select year', min_value=2001, max_value=2023, help='select year between 2001 and 2023')
month = st.slider('Select month', min_value=1, max_value=12)
station = st.selectbox('Select station', definitions.station_list)

if st.button('Submit'):
       df = definitions.create_dataset(month, station)
       st.subheader(f'Information for {station}, {month}.{year}')
       tmax = definitions.one_year(df, year)['temp_max'].max()
       tmin = definitions.one_year(df, year)['temp_min'].min()
       train = '{:.2f}'.format(definitions.one_year(df, year)['rainfall'].sum())

       st.write(f'Temperature max: {tmax} [C]')
       st.write(f'Temperature min: {tmin} [C]')
       st.write(f'Rainfall total: {train} [mm]')

       st.image(charts.chart1(df, year))
       # st.image(charts.chart2(df, month, year, station))
       # st.image(charts.chart2(df, month, year, station))
