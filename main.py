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

def fetch_data(endpoint):
    url = f"http://apps.who.int/gho/athena/api/GHO/{endpoint}?format=csv"
    response = requests.get(url)
    csv_data = StringIO(response.content.decode('utf-8'))
    df = pd.read_csv(csv_data)
    df = keep_most_recent_date(df).loc[:, ['COUNTRY', 'YEAR', 'Numeric']]
    return df

def keep_most_recent_date(df):
    df = df.sort_values(by=['COUNTRY', 'YEAR'], ascending=[True, False])
    df = df.drop_duplicates(subset='COUNTRY', keep='first')
    return df

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Harnessing Data to Address World Challenges: Malnutrition Across the Globe", 
                style={'fontSize': '24px',
                       'fontFamily': "'Courier New', monospace"}),
        html.Div([
            html.Button("1. A  Global Issue", id="btn-section1", n_clicks=0, style={
            'backgroundColor': '#4CAF50',  # Green color
            'color': 'white',              # White text
            'border': 'none',
            'borderRadius': '8px',
            'padding': '10px 20px',
            'fontSize': '16px',
            'outline': 'none',
            'cursor': 'pointer',
            'marginLeft': 20
        }),
            html.Button("2. Regional Specifics", id="btn-section2", n_clicks=0, style={
                'backgroundColor': '#008CBA',  # Blue color
                'color': 'white',
                'border': 'none',
                'borderRadius': '8px',
                'padding': '10px 20px',
                'fontSize': '16px',
                'outline': 'none',
                'cursor': 'pointer',
                'marginLeft': 10
            }),
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'padding': '0 10px'}),



    html.Div(id='section1', children=[
        html.P("""In children under the age of 5, undernutrition manifests in stunted growth, wasting, and heightened
                susceptibility to infections. Conversely, an increasing number of children in this age bracket are overweight,
                placing them at risk for chronic conditions such as diabetes, cardiovascular diseases, and other obesity-related 
               complications later in life. """),
        dcc.Dropdown(
            id='data-selector',
            options=[
                {'label': 'Stunting prevalence among children under 5 years', 'value': 'NUTRITION_ANT_HAZ_NE2'},
                {'label': 'Overweight prevalence among children under 5 years', 'value': 'NUTRITION_ANT_WHZ_NE2'},
                {'label': 'Wasting prevalence among children under 5 years', 'value': 'NUTRITION_WH_2'}
            ],
            value='NUTRITION_ANT_HAZ_NE2',
            clearable=False
        ),
        dcc.Graph(id='section1-graph', style={"width": "100%", "height": "70vh"}),
        html.H4("Prevalence among children under 5 years (% weight-for-height +-2 SD), survey-based estimates")
    ], style={"width": "100%", "padding": "0"}),

    html.Div(id='section2', children=[
        html.H2("Section 2"),
        # ... other content for section 2 ...
    ], style={'marginTop': 50, 'display': 'none'}),

], style={"width": "100%", "padding": "0"})

@app.callback(
    dash.dependencies.Output('section1-graph', 'figure'),
    [dash.dependencies.Input('data-selector', 'value')]
)
def update_graph(data_type):
    df = fetch_data(data_type)
    countries = df['COUNTRY']
    values = df['Numeric']

    fig = px.choropleth_mapbox(df, geojson=geojson_data, locations=countries, color='Numeric',
                               color_continuous_scale="Viridis",
                               range_color=(0, 12),
                               mapbox_style="carto-positron",
                               zoom=1.5,
                               center={"lat": 20, "lon": 0},
                               opacity=0.5,
                               featureidkey="properties.ISO_A3"
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, 
                          coloraxis_colorbar_title="%"
                    )
    return fig

@app.callback(
    [dash.dependencies.Output('section1', 'style'),
     dash.dependencies.Output('section2', 'style')],
    [dash.dependencies.Input('btn-section1', 'n_clicks'),
     dash.dependencies.Input('btn-section2', 'n_clicks')]
)
def toggle_sections(btn1, btn2):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dict(), {'display': 'none'}
    else:
        btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if btn_id == 'btn-section1':
            return {'display': 'block'}, {'display': 'none'}
        elif btn_id == 'btn-section2':
            return {'display': 'none'}, {'display': 'block'}

if __name__ == '__main__':
    app.run_server(debug=True)


