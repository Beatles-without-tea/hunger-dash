import requests
import pandas as pd
from io import StringIO

geojson_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
geojson_data = requests.get(geojson_url).json()

url = "http://apps.who.int/gho/athena/api/GHO/NUTRITION_ANT_HAZ_NE2?format=csv"
response = requests.get(url)

# "Overweight prevalence among children under 5 years of age (% weight-for-height >+2 SD), survey-based estimates",
# "NUTRITION_ANT_WHZ_NE2",


# "Wasting prevalence among children under 5 years of age (% weight-for-height <-2 SD), survey-based estimates",
# NUTRITION_WH_2

csv_data = StringIO(response.content.decode('utf-8'))
df = pd.read_csv(csv_data)

def keep_most_recent_date(df):
    df = df.sort_values(by=['COUNTRY', 'YEAR'], ascending=[True, False])
    df = df.drop_duplicates(subset='COUNTRY', keep='first')
    return df

df = keep_most_recent_date(df).loc[:,['COUNTRY','YEAR','Numeric']]
