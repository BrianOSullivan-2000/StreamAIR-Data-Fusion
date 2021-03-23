
import requests
import json
import pandas as pd
import geopandas as gpd
import shapely.geometry as shp
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from datetime import datetime, timedelta

import warnings
warnings.filterwarnings('ignore')

# In[1]

#List of in-situ weather stations
locations = [
    # Ireland
    {
        "name": "Macehead",
        "point": "53.25,-10.0",
        "station_code": ''
    },
    {
        "name": "Dublin Blanchardstown River Road",
        "point": "53.5,-6.25",
        "station_code": "IE0131A"
    },
    {
        "name": "Dublin Rathmines Wynnefield Road",
        "point": "53.25,-6.25",
        "station_code": "IE0028A"
    },
    {
        "name": "Raheny",
        "point": "53.25,-6.25",
        "station_code": 'IE002AP'
    },
    {
        "name": "Finglas",
        "point": "53.5,-6.25",
        "station_code": 'IE003AP'
    },
    {
        "name": "Phoenix Park",
        "point": "53.25,-6.25",
        "station_code": 'IE0095A'
    },
    {
        "name": "Ballyfermot",
        "point": "53.25,-6.25",
        "station_code": 'IE0036A'
    },
    {
        "name": "Inchicore",
        "point": "53.25,-6.25",
        "station_code": 'IE001AP'
    },
    {
        "name": "Castlebar",
        "point": "53.75,-9.25",
        "station_code": 'IE0118A'
    },
    {
        "name": "Cork Ballinlough Heatherton Park",
        "point": "52.0,-8.5",
        "station_code": 'IE0110A'
    },
    {
        "name": "Cork South Link Road Landfill",
        "point": "52.0,-8.5",
        "station_code": 'IE001BP'
    },
    # Northern Ireland
    {
        "name": "Belfast",
        "point": "54.5,-6.0",
        "station_code": 'GB0567A'
    },
    {
        "name": "Belfast Stockmans Lane",
        "point": "54.5,-6.0",
        "station_code": 'GB0567A'
    },
    {
        "name": "Armagh Roadside",
        "point": "54.25,-6.75",
        "station_code": 'GB0996A'
    },
    {
        "name": "Lough Navar",
        "point": "54.5,-8.0",
        "station_code": 'GB0006R'
    },
    {
        "name": "Ballymena",
        "point": "54.75,-6.25",
        "station_code": 'GB0934A'
    },
    {
        "name": "Ballymena Antrim Road",
        "point": "54.75,-6.25",
        "station_code": 'GB1074A'
    },
    {
        "name": "Derry Rosemount",
        "point": "55.0,-7.5",
        "station_code": 'GB1060A'
    },
    # Great Britain
    {
        "name": "London Marylebone Road - UKA00315",
        "point": "51.5,-0.25",
        "station_code": 'GB0682A'
    },
    {
        "name": "Manchester Piccadilly - UKA00248",
        "point": "53.5,-2.25",
        "station_code": 'GB0613A'
    },
    {
        "name": "Edinburgh Nicolson Street - UKA00649",
        "point": "56.0,-3.25",
        "station_code": 'GB1091A'
    },
    {
        "name": "Edinburgh Nicolson Street - UKA00649",
        "point": "56.0,-3.25",
        "station_code": 'GB0839A'
    },
    {
        "name": "Cardiff", #
        "point": "51.5,-3.25",
        "station_code": 'GB0580A'
    },
    # France
    {
        "name": "Paris",
        "point": "48.75,2.25",
        "station_code": 'FR25053' # NO2, PM2.5
    },
    {
        "name": "Paris",
        "point": "48.75,2.25",
        "station_code": 'FR04004' # O3, PM10
    },
    {
        "name": "MARSEILLE RABATAU",
        "point": "43.5,5.0",
        "station_code": 'FR03006'
    },
    {
        "name": "MARSEILLE RABATAU",
        "point": "43.5,5.0",
        "station_code": 'FR12021'
    },
    {
        "name": "Lyon",#
        "point": "45.75,8.0",
        "station_code": 'FR20062'
    },
    {
        "name": "Bordeaux",#
        "point": "44.75,-0.5",
        "station_code": 'FR31007'
    },
    {
        "name": "Nantes",#
        "point": "47.25,-1.75",
        "station_code": 'FR23188'
    },
    # Spain
    {
        "name": "RIVAS-VACIAMADRID",
        "point": "40.25,-3.5",
        "station_code": 'ES1807A'
    },
    {
        "name": "RIVAS-VACIAMADRID",
        "point": "40.25,-3.5",
        "station_code": 'ES0118A'
    },
    {
        "name": "Barcelona (el Poblenou)",
        "point": "41.5,2.25",
        "station_code": 'ES0691A'
    },
    {
        "name": "Barcelona (el Poblenou)",
        "point": "41.5,2.25",
        "station_code": 'ES1679A'
    },
    {
        "name": "Barcelona (el Poblenou)",
        "point": "41.5,2.25",
        "station_code": 'ES0694A'
    },
    {
        "name": "Seville",#
        "point": "37.25,-6.0",
        "station_code": 'ES1630A'
    },
    # Belgium
    {
        "name": "Antwerp",#
        "point": "51.25,4.25",
        "station_code": 'BETR804'
    },
    {
        "name": "Brussels",#
        "point": "50.75,4.25",
        "station_code": 'BETR001'
    },
    # Italy
    {
        "name": "ROMA",
        "point": "42.0,12.5",
        "station_code": 'IT0755A'
    },
    {
        "name": "ROMA",
        "point": "42.0,12.5",
        "station_code": 'IT1953A'
    },
    {
        "name": "MILANO - VERZIERE",
        "point": "45.5,9.25",
        "station_code": 'IT0705A'
    },
    {
        "name": "MILANO - VERZIERE",
        "point": "45.5,9.25",
        "station_code": 'IT0706A'
    },
    {
        "name": "Naples",#
        "point": "40.75,14.25",
        "station_code": 'IT1491A' # PM10/NO2
    },
    {
        "name": "Naples",#
        "point": "40.75,14.25",
        "station_code": 'IT1497A' # 03
    },
    {
        "name": "Naples",#
        "point": "40.75,14.25",
        "station_code": 'IT1493A' # PM2.5
    },
    # Germany
    {
        "name": "Berlin Friedrichshagen",
        "point": "52.5,13.5",
        "station_code": 'DEBE056'
    },
    {
        "name": "Berlin Friedrichshagen",
        "point": "52.5,13.5",
        "station_code": 'DEBB110'
    },
    {
        "name": "Frankfurt-Ost",
        "point": "50.25,8.75",
        "station_code": 'DEHE008'
    },
    {
        "name": "Frankfurt-Ost",
        "point": "50.25,8.75",
        "station_code": 'DEBB092'
    },
    {
        "name": "Hamburg Wilhelmsburg",
        "point": "53.5,10.0",
        "station_code": 'DEHH059'
    },
    {
        "name": "Hamburg Wilhelmsburg",
        "point": "53.5,10.0",
        "station_code": 'DEHH047'
    },
    {
        "name": "Munich",#
        "point": "48.25,11.5",
        "station_code": 'DEBY037'
    },
    # Czeck Republic
    {
        "name": "Prague",#
        "point": "50.0,14.5",
        "station_code": 'CZ0ALIB'
    },
    # Croatia
    {
        "name": "ZAGREB-1",
        "point": "45.75,16.0",
        "station_code": 'HR0007A'
    },
    {
        "name": "ZAGREB-1",
        "point": "45.75,16.0",
        "station_code": 'HR0009A'
    },
    # Netherlands
    {
        "name": "Eindhoven-Noordbrabantlaan",
        "point": "51.5,5.5",
        "station_code": 'NL00237'
    },
    {
        "name": "Eindhoven-Noordbrabantlaan",
        "point": "51.5,5.5",
        "station_code": 'NL00236'
    },
    {
        "name": "Amsterdam",#
        "point": "52.5,4.75",
        "station_code": 'NL00641'
    },
    # Norway
    {
        "name": "Vigernes",
        "point": "60.25,11.25",
        "station_code": 'NO0111A'
    },
    {
        "name": "Vigernes",
        "point": "60.25,11.25",
        "station_code": 'NO0056R'
    },
    {
        "name": "Bergen", #
        "point": "60.25,5.25",
        "station_code": 'NO0120A'
    },
    # Sweden
    {
        "name": "Stockholm Hornsgatan 108 Gata",
        "point": "59.25,18.0",
        "station_code": 'NO0111A'
    },
    {
        "name": "Stockholm Hornsgatan 108 Gata",
        "point": "59.25,18.0",
        "station_code": 'SE0022A'
    },
    {
        "name": "Gothenburg",
        "point": "57.5,12.0",
        "station_code": 'SE0004A'
    },
    # Portugal
    {
        "name": "Lisbon",
        "point": "38.75,-9.0",
        "station_code": 'PT03071'
    },
    {
        "name": "Porto",
        "point": "41.25,-8.75",
        "station_code": 'PT02004'
    },
    # Luxembourg
    {
        "name": "Luxembourg",
        "point": "49.5,6.25",
        "station_code": 'LU0101A'
    },
    # Switzerland
    {
        "name": "Zurich",
        "point": "47.25,8.5",
        "station_code": 'CH0010A'
    },
    {
        "name": "Geneva",
        "point": "46.25,6.0",
        "station_code": 'CH0055A'
    },
    {
        "name": "Bern",
        "point": "47.0,7.5",
        "station_code": 'CH0054A'
    },
    # EPA Data
    {
        "name": "Cork UCC Distillery Fields",
        "point": "52.0,-8.5",
        "station_code": 'IE004BP'
    },
    {
        "name": "Monaghan Kilkitt Waterworks",
        "point": "54.0,-7.0",
        "station_code": 'IE0090A'
    },
    {
        "name": "Kilkenny Seville Lodge",
        "point": "52.75,-7.25",
        "station_code": 'IE0147A'
    },
    # New Data
    {
        "name": "Legionowo-Zegrzynska",
        "point": "52.5,21.0",
        "station_code": 'PL0129A'
    },
    {
        "name": "Poznan-Dabrowskiego",
        "point": "52.5,17.0",
        "station_code": 'PL0245A'
    },
    {
        "name": "Zloty Potok",
        "point": "50.75,19.5",
        "station_code": 'PL0243A'
    },
    {
        "name": "AM15 Malbork Mickiewicza",
        "point": "54.0,19.0",
        "station_code": 'PL0559A'
    },
    {
        "name": "KMS Puszcza Borecka",
        "point": "54.0,22.0",
        "station_code": 'PL0005R'
    },
    {
        "name": "Przemysl-Grunwaldzka-WIOS",
        "point": "49.75,22.75",
        "station_code": 'PL0594A'
    },
    {
        "name": "Vilnius - Lazdynai",
        "point": "54.75,25.25",
        "station_code": 'LT00002'
    },
    {
        "name": "Kaunas - Petrasiunai",
        "point": "55.0,24.0",
        "station_code": 'LT00041'
    },
    {
        "name": "Mazeikiai",
        "point": "56.25,22.25",
        "station_code": 'LT00023'
    },
    {
        "name": "Rezekne",
        "point": "56.5,27.5",
        "station_code": 'LV0008A'
    },
    {
        "name": "Liepaja",
        "point": "56.5,21.0",
        "station_code": 'LV0012A'
    },
    {
        "name": "Oismae",
        "point": "59.5,24.75",
        "station_code": 'EE0018A'
    },
    {
        "name": "Narva",
        "point": "59.5,28.25",
        "station_code": 'EE0022A'
    },
    {
        "name": "Tartu",
        "point": "58.25,26.75",
        "station_code": 'EE0021A'
    },
    {
        "name": "Vilsandi",
        "point": "58.5,21.75",
        "station_code": 'EE0011R'
    },
    {
        "name": "Kallio 2",
        "point": "60.25,25.0",
        "station_code": 'FI00425'
    },
    {
        "name": "Virolahti 2",
        "point": "60.5,27.75",
        "station_code": 'FI00893'
    },
    {
        "name": "Oulun keskusta 2",
        "point": "65.0,25.5",
        "station_code": 'FI00446'
    },
    {
        "name": "Opava-Katerinky",
        "point": "50.0,18.0",
        "station_code": 'CZ0TOVK'
    },
    {
        "name": "Mikulov-Sedlec",
        "point": "48.75,16.75",
        "station_code": 'CZ0BMIS'
    },
    {
        "name": "Schwechat Sportplatz",
        "point": "48.25,16.5",
        "station_code": 'AT32701'
    },
    {
        "name": "Voitsberg Muhlgasse",
        "point": "47.0,15.25",
        "station_code": 'AT60107'
    },
    {
        "name": "Worgl Stelzhamerstrabe",
        "point": "47.5,12.0",
        "station_code": 'AT72530'
    },
    {
        "name": "Ruzomberok - Riadok",
        "point": "49.0,19.25",
        "station_code": 'SK0008A'
    },
    {
        "name": "Nitra - Janikovce",
        "point": "48.25,18.25",
        "station_code": 'SK0134A'
    },
    {
        "name": "Humenne - Nam. slobody",
        "point": "49.0,22.0",
        "station_code": 'SK0037A'
    },
    {
        "name": "Jelsava - Jesenskeho",
        "point": "48.75,20.25",
        "station_code": 'SK0025A'
    },
    {
        "name": "Budapest Gilice",
        "point": "47.5,19.25",
        "station_code": 'HU0022A'
    },
    {
        "name": "Kazincbarcika",
        "point": "48.25,20.5",
        "station_code": 'HU0026A'
    },
    {
        "name": "Pecs Boszorkany",
        "point": "46.0,18.25",
        "station_code": 'HU0029A'
    },
    {
        "name": "CJ-5",
        "point": "47.25,24.0",
        "station_code": 'RO0077A'
    },
    {
        "name": "NT-2",
        "point": "47.0,27.0",
        "station_code": 'RO0172A'
    },
    {
        "name": "BZ-1",
        "point": "45.25,26.75",
        "station_code": 'RO0123A'
    },
    {
        "name": "B-7",
        "point": "44.25,26.0",
        "station_code": 'RO0071A'
    },
    {
        "name": "DJ-4",
        "point": "44.5,23.75",
        "station_code": 'RO0081A'
    },
    {
        "name": "AMS Hipodruma-Sofia",
        "point": "42.75,23.25",
        "station_code": 'BG0050A'
    },
    {
        "name": "AMS Kamenitsa-Plovdiv",
        "point": "42.25,24.75",
        "station_code": 'BG0051A'
    },
    {
        "name": "AMS SOU Angel Kanchev-Varna",
        "point": "43.25,28.0",
        "station_code": 'BG0075A'
    },
    {
        "name": "AMS Vazrazhdane-Ruse",
        "point": "43.75,26.0",
        "station_code": 'BG0045A'
    },
    {
        "name": "AGIA SOFIA",
        "point": "40.75,23.0",
        "station_code": 'GR0018A'
    },
    {
        "name": "Agia PARASKEVI",
        "point": "38.0,23.75",
        "station_code": 'GR0039A'
    },
    {
        "name": "ALIARTOS",
        "point": "38.5,23.0",
        "station_code": 'GR0110R'
    },
    {
        "name": "BORGO VAL",
        "point": "46.0,11.5",
        "station_code": 'IT0703A'
    },
    {
        "name": "VIA SCARPELLINI",
        "point": "44.0,13.0",
        "station_code": 'IT1578A'
    },
    {
        "name": "Scuola Antonelli",
        "point": "42.5,14.25",
        "station_code": 'IT2166A'
    },
    {
        "name": "stadio casardi",
        "point": "41.25,16.25",
        "station_code": 'IT2003A'
    },
    {
        "name": "brindisi VIA MAGELLANO",
        "point": "40.75,18.0",
        "station_code": 'IT1702A'
    },
    {
        "name": "Enna",
        "point": "37.5,14.25",
        "station_code": 'IT1890A'
    },
    {
        "name": "Locri",
        "point": "38.25,16.25",
        "station_code": 'IT1940A'
    },
    {
        "name": "Msida",
        "point": "36.0,14.5",
        "station_code": 'MT00005'
    },
    {
        "name": "CENCA1",
        "point": "39.25,9.0",
        "station_code": 'IT2056A'
    },
    {
        "name": "AJACCIO CANETTO",
        "point": "42.0,8.75",
        "station_code": 'FR41001'
    },
    {
        "name": "MAZADES",
        "point": "43.5,1.5",
        "station_code": 'FR12021'
    },
    {
        "name": "Aurillac-Lagarde",
        "point": "45.0,2.5",
        "station_code": 'FR07052'
    },
    {
        "name": "Station MORVAN",
        "point": "47.25,4.0",
        "station_code": 'FR26012'
    },
    {
        "name": "St DIZIER L. Michel",
        "point": "48.75,5.0",
        "station_code": 'FR14042'
    },
    {
        "name": "VALENCIA - AVD. FRANCIA",
        "point": "39.5,-0.25",
        "station_code": 'ES1912A'
    },
    {
        "name": "TORREVIEJA",
        "point": "38.0,-0.75",
        "station_code": 'ES2008A'
    },
    {
        "name": "PURIFICACION TOMAS",
        "point": "43.25,-6.0",
        "station_code": 'ES1572A'
    },
    {
        "name": "TUDELA II",
        "point": "42.0,-1.5",
        "station_code": 'ES2094A'
    },
    {
        "name": "NOIA",
        "point": "42.75,-9.0",
        "station_code": 'ES0005R'
    },
    {
        "name": "Erfurt Bautzener Weg",
        "point": "51.0,11.0",
        "station_code": 'DETH117'
    },
    {
        "name": "Schwerte",
        "point": "51.5,7.5",
        "station_code": 'DENW179'
    },
    {
        "name": "Greiz Mollbergstr.",
        "point": "50.75,12.25",
        "station_code": 'DETH036'
    },
    {
        "name": "Tiefenbach/Altenschneeberg",
        "point": "49.5,12.5",
        "station_code": 'DEBY072'
    },
    {
        "name": "Neu-Ulm/Gabelsbergerstrabe",
        "point": "48.5,10.0",
        "station_code": 'DEBY052'
    }, # New stations
    {
        "name": "Terena",
        "point": "38.5,-7.5",
        "station_code": 'PT04006'
    },
    {
        "name": "Joaquim",
        "point": "37.0,-8.0",
        "station_code": 'PT05007'
    },
    {
        "name": "Ervedeira",
        "point": "40.0,-9.0",
        "station_code": 'PT02019'
    },
    {
        "name": "Douro Norte",
        "point": "41.5,-7.75",
        "station_code": 'PT01048'
    },
    {
        "name": "Fundao",
        "point": "40.25,-7.25",
        "station_code": 'PT02020'
    },
    {
        "name": "Ferrol",
        "point": "43.5,-8.25",
        "station_code": 'ES1867A'
    },
    {
        "name": "SALAMANCA 6",
        "point": "41.0,-5.5",
        "station_code": 'ES1889A'
    },
    {
        "name": "BURGOS 4",
        "point": "42.25,-3.75",
        "station_code": 'ES1443A'
    },
    {
        "name": "ALBACETE",
        "point": "39.0,-1.75",
        "station_code": 'ES1535A'
    },
    {
        "name": "CIUDAD DEPORTIVA",
        "point": "37.25,-3.5",
        "station_code": 'ES1973A'
    },
    {
        "name": "CACERES",
        "point": "39.5,-6.25",
        "station_code": 'ES1615A'
    },
    {
        "name": "Inverness",
        "point": "57.5,-4.25",
        "station_code": 'GB0742A'
    },
    {
        "name": "Stockton-on-Tees",
        "point": "54.5,-1.25",
        "station_code": 'GB1041A'
    },
    {
        "name": "Greenock",
        "point": "56.0,-4.75",
        "station_code": 'GB1062A'
    },
    {
        "name": "Wrexham",
        "point": "53.0,-3.0",
        "station_code": 'GB0755A'
    },
    {
        "name": "Birmingham",
        "point": "52.5,-1.75",
        "station_code": 'GB1067A'
    },
    {
        "name": "BERTHELOT",
        "point": "43.5,1.5",
        "station_code": 'FR12030'
    },
    {
        "name": "Montlucon",
        "point": "46.25,2.5",
        "station_code": 'FR07058'
    },
    {
        "name": "Brest Mace",
        "point": "48.5,-4.5",
        "station_code": 'FR19012'
    },
    {
        "name": "Bethune Stade",
        "point": "50.5,2.75",
        "station_code": 'FR28028'
    },
    {
        "name": "STE SAVINE",
        "point": "48.25,4.0",
        "station_code": 'FR14033'
    },
    {
        "name": "Metz-Centre",
        "point": "49.0,6.25",
        "station_code": 'FR01011'
    },
    {
        "name": "Weserbergland",
        "point": "52.25,9.0",
        "station_code": 'DENI041'
    },
    {
        "name": "Spremberg",
        "point": "51.5,14.5",
        "station_code": 'DEBB083'
    },
    {
        "name": "Rostock-Warnemunde",
        "point": "54.25,12.0",
        "station_code": 'DEMV021'
    },
    {
        "name": "Szczecin_Andrzejewskiego",
        "point": "53.5,14.5",
        "station_code": 'PL0248A'
    },
    {
        "name": "Bydgoszcz Warszawska",
        "point": "53.25,18.0",
        "station_code": 'PL0064A'
    },
    {
        "name": "Lublin ul. Obywatelska",
        "point": "51.25,22.5",
        "station_code": 'PL0507A'
    },
    {
        "name": "Wroclaw - Korzeniowskiego",
        "point": "51.0,17.0",
        "station_code": 'PL0194A'
    },
    {
        "name": "Malmo Radhuset",
        "point": "55.5,13.0",
        "station_code": 'SE0001A'
    },
    {
        "name": "Kalmar Sodra Vagen",
        "point": "57.75,14.25",
        "station_code": 'SE157868'
    },
    {
        "name": "Asa",
        "point": "67.75,21.0",
        "station_code": 'SE0013R'
    },
    {
        "name": "Odense/9159",
        "point": "55.5,10.5",
        "station_code": 'DK0046A'
    },
    {
        "name": "Arhus/6160",
        "point": "56.25,10.25",
        "station_code": 'DK0056A'
    },
    {
        "name": "Copenhagen/1103",
        "point": "55.75,12.5",
        "station_code": 'DK0034A'
    },
    {
        "name": "Klosterhaugen",
        "point": "60.5,5.25",
        "station_code": 'NO0120A'
    },
    {
        "name": "Birkenesobservatoriet",
        "point": "58.5,8.25",
        "station_code": 'NO0002R'
    },
    {
        "name": "Schancheholen",
        "point": "59.0,5.75",
        "station_code": 'NO0125A'
    }
]

# In[2]

#Set dates & columns
fromDate = "2020-08-01 00:00"
toDate = "2020-08-31 23:59"
keys = ['location', 'datetime', 'meas_NO2', 'model0_NO2', 'model1_NO2']

#Empty row to hold dictionaries
rows = []

#Loop through locations
for location in locations:

    #Prepare dictionary & add values
    data = {}
    data['location'] = location['name']
    data['fromDate'], data['toDate'] = fromDate, toDate

    #Create Shapely point for gdf geometry
    coord = location['point'].split(',')
    coord = shp.Point(float(coord[1]), float(coord[0]))

    #HTTPS Post request
    r = requests.post('https://streamair.nuigalway.ie/api/realtime', data=data)

    #Loop through post request adding dictionaries to rows for each datapoint
    for d in r.json():

        #Add each key
        d = {key: d[key] for key in keys}
        d['geometry'] = coord
        rows.append(d)

#Convert list of dictionaries to rows in GeoDataFrame
gdf = gpd.GeoDataFrame(rows)

# In[3]

#Clean data (Drop NaN values)
gdf_clean = gdf.drop("model1_NO2", axis=1)
gdf_clean = gdf_clean.dropna()

# In[4]

gdf_clean['datetime'] = pd.to_datetime(gdf_clean['datetime'], unit='ms')
gdf_clean = gdf_clean.set_index('datetime')

# In[5]

days = []

for i in range(31):

    gdf_day = gdf_clean.loc['2020-08-{}'.format(i + 1):'2020-08-{}'.format(i + 1)]
    days.append(gdf_day)

# In[6]

i = 0

for day in days:

    i += 1

    #Save frame in .json format
    if day.empty == False:
        day.to_file("data/real_time/" + "Aug/" + "Aug_Real_Time_{}.json".format(i), driver='GeoJSON')

# In[7]

#Set longitude and latitude bounds
lon_b = (-11, 36)
lat_b = (36, 64)

#Function for plotting values
def map_plot(gdf, variable, markersize):

    #World map overlay
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    #Plot formatting
    plt.rcParams["font.serif"] = "Times New Roman"
    fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=100)
    ax = plt.axes(projection=ccrs.PlateCarree())
    gdf.plot(column=variable, cmap='rainbow', marker=',', markersize=markersize , ax=ax, legend=True)
    ax.coastlines()


#Plot for Western Europe
map_plot(gdf_clean, "meas_NO2", 5)
plt.title("NO2 Concentration (mol m^2) February 16th 2021")
plt.xlim(lon_b)
plt.ylim(lat_b)
plt.show()
