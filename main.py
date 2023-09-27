import requests
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px
from io import StringIO
import plotly.graph_objs as go

geojson_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
geojson_data = requests.get(geojson_url).json()


# "Stunting prevalence among children under 5 years of age (% height-for-age <-2 SD), survey-based estimates",
url = "http://apps.who.int/gho/athena/api/GHO/NUTRITION_ANT_HAZ_NE2?format=csv"
response = requests.get(url)

# "Overweight prevalence among children under 5 years of age (% weight-for-height >+2 SD), survey-based estimates",
# "NUTRITION_ANT_WHZ_NE2",


# "Wasting prevalence among children under 5 years of age (% weight-for-height <-2 SD), survey-based estimates",
# NUTRITION_WH_2


# Convert the string response to a pandas DataFrame
csv_data = StringIO(response.content.decode('utf-8'))
df = pd.read_csv(csv_data)


def keep_most_recent_date(df):
    df = df.sort_values(by=['COUNTRY', 'YEAR'], ascending=[True, False])
    df = df.drop_duplicates(subset='COUNTRY', keep='first')
    return df

# print(df.loc[:,['COUNTRY','YEAR','Numeric']].head(10))
df = keep_most_recent_date(df).loc[:,['COUNTRY','YEAR','Numeric']]

# # Convert the data to a DataFrame
# df = pd.DataFrame(data['fact'])

countries = df['COUNTRY']  
values = df['Numeric']      


app = dash.Dash(__name__)





fig = px.choropleth_mapbox(df, geojson=geojson_data, locations=countries, color='Numeric',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=1.5, center = {"lat": 20, "lon": 0},
                           opacity=0.5,
                           featureidkey="properties.ISO_A3"
                          )


fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
app.layout = html.Div([
    dcc.Graph(figure=fig, style={"width": "100%","height": "80vh"})
], style={"width": "100%", "padding": "0"})

if __name__ == '__main__':
    app.run_server(debug=True)
