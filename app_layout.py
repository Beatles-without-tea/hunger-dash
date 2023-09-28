from dash import dcc
from dash import html
import plotly.express as px
from data_processing import df, geojson_data

fig = px.choropleth_mapbox(df, geojson=geojson_data, locations=df['COUNTRY'], color='Numeric',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=1.5, 
                           center = {"lat": 20, "lon": 0},
                           opacity=0.5,
                           featureidkey="properties.ISO_A3"
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

layout = html.Div([
    html.Div([
        html.H1("Harnessing Data to Address World Challenges: Malnutrition Across the Globe", style={'display': 'inline-block'}),
        html.Button("Section 1", id="btn-section1", n_clicks=0, style={'marginLeft': 20}),
        html.Button("Section 2", id="btn-section2", n_clicks=0, style={'marginLeft': 10}),
    ], style={'textAlign': 'center'}),

    html.Div(id='section1', children=[
        html.H2("Section 1"),
         dcc.Graph(figure=fig, style={"width": "100%","height": "80vh"})
    ], style={"width": "100%", "padding": "0"}),

    html.Div(id='section2', children=[
        html.H2("Section 2"),
    ], style={'marginTop': 50, 'display': 'none'}),
], style={"width": "100%", "padding": "0"})
