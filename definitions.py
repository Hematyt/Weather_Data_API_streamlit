import pandas as pd
from zipfile import ZipFile
import requests
import os

link = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/'
station_list = ('PSZCZYNA', 'CIESZYN', 'BRENNA', 'WISLA', 'ISTEBNA-KUBALONKA',
       'INWALD', 'MIEDZYBRODZIE BIALSKIE', 'MAKOW PODHALANSKI',
       'LUBON WIELKI', 'NOWY DWOR', 'ZAWOJA', 'RABKA', 'LALIKI',
       'OBIDOWA', 'JABLONKA', 'POLANA CHOCHOLOWSKA', 'HALA ORNAK', 'LAZY',
       'DOBCZYCE', 'JASTRZEBIA', 'LIMANOWA', 'PTASZKOWA', 'LACKO',
       'LOPUSZNA', 'MIZERNA', 'KROSCIENKO', 'PIWNICZNA', 'NIEDZICA',
       'KRYNICA', 'BUKOWINA TATRZANSKA', 'MUSZYNA', 'PORONIN',
       'HALA GASIENICOWA', 'DOLINA PIECIU STAWOW', 'BIECZ-GRUDNA',
       'DUKLA', 'WYSOWA', 'BARWINEK', 'DYNOW', 'SANOK-TREPCZA',
       'SOLINA-JAWOR', 'BALIGROD=MCHAWA', 'KOMANCZA', 'TERKA',
       'STUPOSIANY', 'BOGATYNIA', 'SWIERADOW ZDROJ', 'JAKUSZYCE',
       'KARPACZ', 'PAPROTKI', 'PSZENNO', 'SZCZAWNO ZDROJ', 'TARNOW',
       'SLOSZOW', 'LADEK ZDROJ', 'DLUGOPOLE ZDROJ', 'BOLESLAWOW',
       'DOBROGOSZCZ', 'GRODKOW', 'KORFANTOW', 'OTMUCHOW', 'GLUCHOLAZY',
       'GLUBCZYCE', 'STARE OLESNO', 'KOCHCICE', 'SWIERKLANIEC',
       'SUKOWICE', 'SILNICZKA', 'LGOTA GORNA', 'ZABKOWICE', 'OLEWIN',
       'BIERUN STARY', 'KRAKOW OBSERWATORIUM', 'KATOWICE PYRZOWICE',
       'BODZENTYN', 'SKRONIOW', 'MIECHOW', 'SIELEC', 'BORUSOWA',
       'IGOLOMNIA', 'SWIETY KRZYZ', 'STASZOW', 'CHORZELOW', 'ZAWADA',
       'WYSOKIE', 'JAROCIN', 'TOMASZOW LUBELSKI', 'NOWY LUBLINIEC',
       'CEBER', 'GRABIK', 'TOMASZOW BOLESLAWIECKI', 'ZGORZELEC',
       'POLKOWICE DOLNE', 'CHWALKOWICE', 'WITASZYCE', 'SMOLICE',
       'GRABOWNICA', 'NAMYSLOW', 'JELCZ-LASKOWICE', 'SIERADZ', 'PUCZNIEW',
       'SKIERNIEWICE', 'LAZISKA', 'JARCZEW', 'PULAWY', 'SOBIESZYN',
       'BEZEK', 'KRZYZ', 'GORZYN', 'LUBNICKO-SWIEBODZIN',
       'SZAMOTULY-BABOROWKO', 'PAPROC', 'WIELICHOWO', 'GNIEZNO', 'SLUPCA',
       'KORNIK', 'KOLUDA WIELKA', 'GLODOWO', 'POSWIETNE', 'LEGIONOWO',
       'WARSZAWA-BIELANY', 'PULTUSK', 'WARSZAWA-OBSERWATORIUM',
       'WARSZAWA-OBSERWATORIUM II', 'SZEPIETOWO', 'BIALOWIEZA', 'CICIBOR',
       'GOLENIOW', 'PRZELEWICE', 'WIERZCHOWO', 'CHRZESTOWO', 'RADOSTOWO',
       'SLIWICE', 'GRUDZIADZ', 'BYDGOSZCZ', 'DOBROCIN', 'PRABUTY',
       'LIDZBARK', 'SZCZYTNO', 'MYSZYNIEC', 'BIEBRZA-PIENCZYKOWEK',
       'MARIANOWO', 'ROZANYSTOK', 'DZIWNOW', 'DARLOWO', 'MIASTKO',
       'KARZNICZKA', 'KOSCIERZYNA', 'ROZEWIE', 'GDYNIA',
       'GDANSK-REBIECHOWO', 'GDANSK-SWIBNO', 'LISEWO', 'FROMBORK',
       'KMIECIN', 'LIDZBARK WARMINSKI', 'GOLDAP', 'OLECKO', 'PRZEMYSL',
       'STRZYZOW', 'SZKLARSKA POREBA', 'JEDRZEJOW SUDOL', 'DRONIOWICE',
       'CIESZANOW', 'RADZYN', 'WARSZAWA-FILTRY', 'MORSKIE OKO',
       'BORUCINO', 'WARSZAWA-BABICE', 'NIELISZ', 'RADZIECHOWY',
       'KASPARUS', 'NOWY CYDZYN', 'SUPRASL', 'MSZANA DOLNA', 'BABIMOST',
       'BYDGOSZCZ-SZWEDEROWO', 'MARIANOWO II', 'SWIETAJNO',
       'NIEPOKOLANOW', 'BIALA PODLASKA', 'TRZEBIEZ', 'SLUPSK',
       'TOLKMICKO', 'BIELSKO-BIALA', 'ZAKOPANE', 'KASPROWY WIERCH',
       'JELENIA GORA', 'SNIEZKA', 'KLODZKO', 'OPOLE', 'RACIBORZ',
       'CZESTOCHOWA', 'KATOWICE', 'KRAKOW-BALICE', 'KIELCE-SUKOW',
       'SANDOMIERZ', 'ZAMOSC', 'ZIELONA GORA', 'LEGNICA', 'WROCLAW',
       'KALISZ', 'WIELUN', 'LODZ', 'LUBLIN-RADAWIEC', 'WLODAWA',
       'SLUBICE', 'GORZOW WIELKOPOLSKI', 'POZNAN', 'KOLO', 'PLOCK',
       'WARSZAWA', 'SIEDLCE', 'SWINOUJSCIE', 'SZCZECIN', 'RESKO-SMOLSKO',
       'SZCZECINEK', 'CHOJNICE', 'TORUN', 'OLSZTYN', 'OSTROLEKA',
       'BIALYSTOK', 'KOLOBRZEG', 'KOSZALIN', 'USTKA', 'LEBA', 'LEBORK',
       'HEL', 'ELBLAG-MILEJEWO', 'SUWALKI', 'ZAWODZIE',
       'RZESZOW-JASIONKA', 'MIKOLAJKI', 'KATOWICE-MUCHOWIEC',
       'WROCLAW-STRACHOWICE', 'LODZ-LUBLINEK', 'POZNAN-LAWICA',
       'WARSZAWA-OKECIE', 'KOLOBRZEG-DZWIRZYNO', 'NNOWY SACZ', 'LESKO',
       'KRYNICA-GORA PARKOWA', 'TERESPOL', 'PRUDNIK', 'WINSKO', 'SWIDER',
       'HOPOWO', 'LESZNO', 'CIECHOCINEK', 'JASTRZEBIE-ZDROJ', 'GUBALOWKA',
       'WITOW', 'SIENIAWA', 'ZYWIEC', 'WADOWICE', 'ROZNOW', 'BOCHNIA',
       'IWONICZ-ZDROJ', 'KROSNO', 'ZARNOWA', 'BIRCZA', 'BRZEGI DOLNE',
       'DUSZNIKI-ZDROJ', 'SWIDNICA', 'OLAWA', 'LUBLINIEC', 'OLKUSZ',
       'WIELICZKA', 'KOLBUSZOWA', 'TARNOGROD', 'OZANSK', 'LEZAJSK',
       'WERBKOWICE', 'LUBACZOW', 'SZPROTAWA', 'OPOLE LUBELSKIE', 'FELIN',
       'NOWA WIES', 'RADZYN PODLASKI', 'KRASNYSTAW', 'TREZBIECHOW',
       'SULECIN', 'TOPOLA-BLONIE', 'BRWINOW', 'SINOLEKA',
       'BIELSK PODLASKI', 'LIPNIK (LIPKI)', 'POLCZYN-ZDROJ', 'PRZASNYSZ',
       'BISKUPIEC', 'SZCZUCZYN', 'CZARNA DABROWKA', 'GIZYCKO', 'SULEJOW',
       'MLAWA', 'KONCZEWICE', 'RYBNIK', 'CZEKANOW', 'DEBNO',
       'SZCZEKOCINY', 'CHMIELOW', 'BOGUSLAWICE', 'PLOCZKI DOLNE',
       'BELCHATOW', ' WLOCHOW', 'GRABOWIEC', 'NIEGOW', 'PLATEROW',
       'KRZYZEWO', 'BOBROWNIKI', 'STARY BRZESC', 'ZADABROWIE', 'POKOJ',
       'WEGRZCE', 'ZYBISZOW', 'LUCMIERZ', 'CZESLAWICE', 'UHNIN',
       'SLUPIA WIELKA', 'GLEBOKIE', 'KAWECZYN', 'PRZEDWOJEWO',
       'NOWA WIES UJSKA', 'WYCZECHY', 'WROCIKOWO', 'BIALOGARD',
       'TRZCINSKO-ZDROJ', 'OPIESIN-GLOGOWA', 'REDLO', 'LIBERTOW',
       'LESKOWIEC', 'CZORSZTYN-NADZAMCZE', 'ZBYSZYCE', 'ZUBRACZE',
       'JODLOWNIK')

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

    df_all['station name'] = df_all['station name'].replace(to_replace={'WIS£A': 'WISLA','INWA£D': 'INWALD',
                                                                'MIÊDZYBRODZIE BIALSKIE': 'MIEDZYBRODZIE BIALSKIE',
                                                                'MAKÓW PODHALAÑSKI': 'MAKOW PODHALANSKI',
                                                                'LUBOÑ WIELKI': 'LUBON WIELKI',
                                                                'NOWY DWÓR': 'NOWY DWOR',
                                                                'JAB£ONKA': 'JABLONKA',
                                                                'POLANA CHOCHO£OWSKA': 'POLANA CHOCHOLOWSKA',
                                                                '£AZY': 'LAZY',
                                                                'JASTRZÊBIA': 'JASTRZEBIA', '£¥CKO': 'LACKO',
                                                                '£OPUSZNA': 'LOPUSZNA', 'KRO\x8cCIENKO': 'KROSCIENKO',
                                                                'BUKOWINA TATRZAÑSKA': 'BUKOWINA TATRZANSKA',
                                                                'HALA G¥SIENICOWA': 'HALA GASIENICOWA',
                                                                'DOLINA PIÊCIU STAWÓW': 'DOLINA PIECIU STAWOW',
                                                                'DYNÓW': 'DYNOW', 'BALIGRÓD-MCHAWA': 'BALIGROD=MCHAWA',
                                                                'KOMAÑCZA': 'KOMANCZA',
                                                                '\x8cWIERADÓW-ZDRÓJ': 'SWIERADOW ZDROJ',
                                                                'SZCZAWNO-ZDRÓJ': 'SZCZAWNO ZDROJ', 'TARNÓW': 'TARNOW',
                                                                'S£OSZÓW': 'SLOSZOW', 'L¥DEK-ZDRÓJ': 'LADEK ZDROJ',
                                                                'D£UGOPOLE-ZDRÓJ': 'DLUGOPOLE ZDROJ',
                                                                'BOLES£AWÓW': 'BOLESLAWOW',
                                                                'GRODKÓW': 'GRODKOW', 'KORFANTÓW': 'KORFANTOW',
                                                                'OTMUCHÓW': 'OTMUCHOW', 'G£UCHO£AZY': 'GLUCHOLAZY',
                                                                'G£UBCZYCE': 'GLUBCZYCE',
                                                                '\x8cWIERKLANIEC': 'SWIERKLANIEC',
                                                                'LGOTA GÓRNA': 'LGOTA GORNA', 'Z¥BKOWICE': 'ZABKOWICE',
                                                                'BIERUÑ STARY': 'BIERUN STARY',
                                                                'KRAKÓW-OBSERWATORIUM': 'KRAKOW OBSERWATORIUM',
                                                                'SKRONIÓW': 'SKRONIOW', 'MIECHÓW': 'MIECHOW',
                                                                'IGO£OMIA': 'IGOLOMNIA',
                                                                '\x8cWIÊTY KRZY¯': 'SWIETY KRZYZ', 'STASZÓW': 'STASZOW',
                                                                'CHORZELÓW': 'CHORZELOW',
                                                                'TOMASZÓW LUBELSKI': 'TOMASZOW LUBELSKI',
                                                                'TOMASZÓW BOLES£AWIECKI': 'TOMASZOW BOLESLAWIECKI',
                                                                'CHWA£KOWICE': 'CHWALKOWICE', 'NAMYS£ÓW': 'NAMYSLOW',
                                                                '£AZISKA': 'LAZISKA', 'PU£AWY': 'PULAWY',
                                                                'KRZY¯': 'KRZYZ', 'GORZYÑ': 'GORZYN',
                                                                'LUBINICKO-\x8cWIEBODZIN': 'LUBNICKO-SWIEBODZIN',
                                                                'SZAMOTU£Y-BABORÓWKO': 'SZAMOTULY-BABOROWKO',
                                                                'PAPROÆ': 'PAPROC', 'S£UPCA': 'SLUPCA',
                                                                'KÓRNIK': 'KORNIK', 'KO£UDA WIELKA': 'KOLUDA WIELKA',
                                                                'G£ODOWO': 'GLODOWO', 'PO\x8cWIÊTNE': 'POSWIETNE',
                                                                'PU£TUSK': 'PULTUSK', 'BIA£OWIE¯A': 'BIALOWIEZA',
                                                                'CICIBÓR': 'CICIBOR',
                                                                'GOLENIÓW': 'GOLENIOW', 'CHRZ¥STOWO': 'CHRZESTOWO',
                                                                '\x8cLIWICE': 'SLIWICE', 'GRUDZI¥DZ': 'GRUDZIADZ',
                                                                'BIEBRZA-PIEÑCZYKÓWEK': 'BIEBRZA-PIENCZYKOWEK',
                                                                'RÓ¯ANYSTOK': 'ROZANYSTOK', 'DZIWNÓW': 'DZIWNOW',
                                                                'DAR£OWO': 'DARLOWO','KAR¯NICZKA': 'KARZNICZKA',
                                                                'KO\x8cCIERZYNA': 'KOSCIERZYNA',
                                                                'GDAÑSK-RÊBIECHOWO': 'GDANSK-REBIECHOWO',
                                                                'GDAÑSK-\x8cWIBNO': 'GDANSK-SWIBNO',
                                                                'LIDZBARK WARMIÑSKI': 'LIDZBARK WARMINSKI',
                                                                'GO£DAP': 'GOLDAP', 'PRZEMY\x8cL': 'PRZEMYSL',
                                                                'STRZY¯ÓW': 'STRZYZOW',
                                                                'SZKLARSKA PORÊBA': 'SZKLARSKA POREBA',
                                                                'JÊDRZEJÓW-SUDÓ£': 'JEDRZEJOW SUDOL',
                                                                'CIESZANÓW': 'CIESZANOW', 'RADZYÑ': 'RADZYN',
                                                                'SUPRA\x8cL': 'SUPRASL', '\x8cWIÊTAJNO': 'SWIETAJNO',
                                                                'NIEPOKALANÓW': 'NIEPOKOLANOW',
                                                                'BIA£A PODLASKA': 'BIALA PODLASKA',
                                                                'TRZEBIE¯': 'TRZEBIEZ', 'S£UPSK': 'SLUPSK',
                                                                'BIELSKO-BIA£A': 'BIELSKO-BIALA',
                                                                'JELENIA GÓRA': 'JELENIA GORA', '\x8cNIE¯KA': 'SNIEZKA',
                                                                'K£ODZKO': 'KLODZKO', 'RACIBÓRZ': 'RACIBORZ',
                                                                'CZÊSTOCHOWA': 'CZESTOCHOWA',
                                                                'KRAKÓW-BALICE': 'KRAKOW-BALICE',
                                                                'KIELCE-SUKÓW': 'KIELCE-SUKOW',
                                                                'ZAMO\x8cÆ': 'ZAMOSC', 'ZIELONA GÓRA': 'ZIELONA GORA',
                                                                'WROC£AW': 'WROCLAW',
                                                                'WIELUÑ': 'WIELUN', '£ÓD\x8f': 'LODZ',
                                                                'W£ODAWA': 'WLODAWA',
                                                                'S£UBICE': 'SLUBICE',
                                                                'GORZÓW WIELKOPOLSKI': 'GORZOW WIELKOPOLSKI',
                                                                'POZNAÑ': 'POZNAN', 'KO£O': 'KOLO', 'P£OCK': 'PLOCK',
                                                                '\x8cWINOUJ\x8cCIE': 'SWINOUJSCIE',
                                                                'RESKO-SMÓLSKO': 'RESKO-SMOLSKO', 'TORUÑ': 'TORUN',
                                                                'OSTRO£ÊKA': 'OSTROLEKA', 'BIA£YSTOK': 'BIALYSTOK',
                                                                'KO£OBRZEG': 'KOLOBRZEG', '£EBA': 'LEBA',
                                                                'ELBL¥G-MILEJEWO': 'ELBLAG-MILEJEWO',
                                                                'SUWA£KI': 'SUWALKI',
                                                                'RZESZÓW-JASIONKA': 'RZESZOW-JASIONKA',
                                                                'MIKO£AJKI': 'MIKOLAJKI',
                                                                'WROC£AW-STRACHOWICE': 'WROCLAW-STRACHOWICE',
                                                                '£ÓD\x8f-LUBLINEK': 'LODZ-LUBLINEK',
                                                                'POZNAÑ-£AWICA': 'POZNAN-LAWICA',
                                                                'WARSZAWA-OKÊCIE': 'WARSZAWA-OKECIE',
                                                                'KO£OBRZEG-D\x8fWIRZYNO': 'KOLOBRZEG-DZWIRZYNO',
                                                                'NOWY S¥CZ': 'NNOWY SACZ',
                                                                'KRYNICA-GÓRA PARKOWA': 'KRYNICA-GORA PARKOWA',
                                                                'WIÑSKO': 'WINSKO',
                                                                '\x8cWIDER': 'SWIDER',
                                                                'JASTRZÊBIE-ZDRÓJ': 'JASTRZEBIE-ZDROJ',
                                                                'GUBA£ÓWKA': 'GUBALOWKA', 'WITÓW': 'WITOW',
                                                                '¯YWIEC': 'ZYWIEC', 'RO¯NÓW': 'ROZNOW',
                                                                'IWONICZ-ZDRÓJ': 'IWONICZ-ZDROJ', '¯ARNOWA': 'ZARNOWA',
                                                                'DUSZNIKI-ZDRÓJ': 'DUSZNIKI-ZDROJ',
                                                                '\x8cWIDNICA': 'SWIDNICA', 'O£AWA': 'OLAWA',
                                                                'TARNOGRÓD': 'TARNOGROD', 'O¯AÑSK': 'OZANSK',
                                                                'LE¯AJSK': 'LEZAJSK', 'LUBACZÓW': 'LUBACZOW',
                                                                'NOWA WIE\x8c': 'NOWA WIES',
                                                                'RADZYÑ PODLASKI': 'RADZYN PODLASKI',
                                                                'TRZEBIECHÓW': 'TREZBIECHOW', 'SULÊCIN': 'SULECIN',
                                                                'TOPOLA-B£ONIE': 'TOPOLA-BLONIE', 'BRWINÓW': 'BRWINOW',
                                                                'SINO£ÊKA': 'SINOLEKA',
                                                                'PO£CZYN-ZDRÓJ': 'POLCZYN-ZDROJ',
                                                                'CZARNA D¥BRÓWKA': 'CZARNA DABROWKA',
                                                                'GI¯YCKO': 'GIZYCKO', 'SULEJÓW': 'SULEJOW',
                                                                'M£AWA': 'MLAWA', 'KOÑCZEWICE': 'KONCZEWICE',
                                                                'CZEKANÓW': 'CZEKANOW',
                                                                'DÊBNO': 'DEBNO', 'CHMIELÓW': 'CHMIELOW',
                                                                'BOGUS£AWICE': 'BOGUSLAWICE',
                                                                'P£ÓCZKI DOLNE': 'PLOCZKI DOLNE',
                                                                'BE£CHATÓW': 'BELCHATOW', 'W£OCHÓW': ' WLOCHOW',
                                                                'NIEGÓW': 'NIEGOW', 'PLATERÓW': 'PLATEROW',
                                                                'KRZY¯EWO': 'KRZYZEWO',
                                                                'STARY BRZE\x8cÆ': 'STARY BRZESC',
                                                                'ZAD¥BROWIE': 'ZADABROWIE', 'POKÓJ': 'POKOJ',
                                                                'WÊGRZCE': 'WEGRZCE', 'ZYBISZÓW': 'ZYBISZOW',
                                                                'LUÆMIERZ': 'LUCMIERZ', 'CZES£AWICE': 'CZESLAWICE',
                                                                'S£UPIA WIELKA': 'SLUPIA WIELKA',
                                                                'G£ÊBOKIE': 'GLEBOKIE', 'KAWÊCZYN': 'KAWECZYN',
                                                                'NOWA WIE\x8c UJSKA': 'NOWA WIES UJSKA',
                                                                'BIA£OGARD': 'BIALOGARD',
                                                                'TRZCIÑSKO-ZDRÓJ': 'TRZCINSKO-ZDROJ',
                                                                'OPIESIN-G£OGOWA': 'OPIESIN-GLOGOWA', 'RED£O': 'REDLO',
                                                                'LIBERTÓW': 'LIBERTOW',
                                                                '¯UBRACZE': 'ZUBRACZE', 'JOD£OWNIK': 'JODLOWNIK'})

    df_all = df_all[df_all['month'] == month]
    df_all = df_all[df_all['station name'] == station]

    return df_all


def one_year(df, year):
    df = df[df['year'] == year]
    return df
