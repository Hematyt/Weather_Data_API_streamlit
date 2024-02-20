import streamlit as st

# import function from other files
import definitions
import charts

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


df = definitions.create_dataset(month, station)

if st.button('Submit'):
       st.subheader(f'Information for {station}, {month}.{year}')
       tmax = definitions.one_year(df, year)['temp_max'].max()
       tmin = definitions.one_year(df, year)['temp_min'].min()
       train = definitions.one_year(df, year)['rainfall'].sum()

       st.write(f'Temperature max: {tmax} C')
       st.write(f'Temperature min: {tmin} C')
       st.write(f'Rainfall total: {train} mm')

       st.image(charts.chart1(df, year))
       # st.image(charts.chart2(df, month, year, station))
       # st.image(charts.chart2(df, month, year, station))
