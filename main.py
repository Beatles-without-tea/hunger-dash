import requests
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px
from io import StringIO
import plotly.graph_objs as go
from iso3_dict import country_codes
import plotly.figure_factory as ff
import numpy as np

geojson_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
geojson_data = requests.get(geojson_url).json()



def fetch_data(endpoint):
    url = f"http://apps.who.int/gho/athena/api/GHO/{endpoint}?format=csv"
    response = requests.get(url)
    print(f'Fetched data for {endpoint}')
    csv_data = StringIO(response.content.decode('utf-8'))
    df = pd.read_csv(csv_data)
    return df

def format_malnutrition_data(df):
    df = keep_most_recent_date(df).loc[:, ['COUNTRY', 'YEAR', 'Numeric','REGION']]
    return df

def keep_most_recent_date(df):
    df = df.sort_values(by=['COUNTRY', 'YEAR'], ascending=[True, False])
    df = df.drop_duplicates(subset='COUNTRY', keep='first')
    return df

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1(["Harnessing Data to Address World Challenges:", html.Br() ,"Malnutrition Across the Globe"], 
                style={'fontSize': '24px',
                       'fontFamily': "'Courier New', monospace", 'color':'white'}),
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
            html.Button("3. Economic Patterns", id="btn-section3", n_clicks=0, style={
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
            # html.Button("4. Future", id="btn-section4", n_clicks=0, style={
            #     'backgroundColor': '#008CBA',  # Blue color
            #     'color': 'white',
            #     'border': 'none',
            #     'borderRadius': '8px',
            #     'padding': '10px 20px',
            #     'fontSize': '16px',
            #     'outline': 'none',
            #     'cursor': 'pointer',
            #     'marginLeft': 10
            # }),

        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'padding': '0 10px', 'background-color':'black'}),



    html.Div(id='section1', children=[

        html.H3(["Malnourishment is a ", html.Span("global", style={"color": "red"}), " problem. Although, its forms vary by region"],
                style= {'padding-left':'1%'}),
        dcc.Dropdown(
            id='data-selector',
            options=[
                {'label': 'Stunting prevalence among children under 5 years', 'value': 'NUTRITION_ANT_HAZ_NE2'},
                {'label': 'Overweight prevalence among children under 5 years', 'value': 'NUTRITION_ANT_WHZ_NE2'},
                {'label': 'Wasting prevalence among children under 5 years', 'value': 'NUTRITION_WH_2'}
            ],
            value='NUTRITION_ANT_HAZ_NE2',
            searchable = False,
            clearable=False
        ),
        dcc.Graph(id='section1-graph', style={"width": "100%", "height": "70vh"}),
        html.H4("Prevalence among children under 5 years (% weight-for-height +-2 SD), survey-based estimates")
    ], style={"width": "100%", "padding": "0"}),
    # section 2
    html.Div(id='section2', children=[
        html.H3("Regions vary in the types of malnutrition they predominantly face",
                 style= {'padding-left':'1%'}),
        dcc.Dropdown(
        id='dropdown2',
        options=[
            {'label': 'Stunting prevalence among children under 5 years', 'value': 'NUTRITION_ANT_HAZ_NE2'},
            {'label': 'Overweight prevalence among children under 5 years', 'value': 'NUTRITION_ANT_WHZ_NE2'},
            {'label': 'Wasting prevalence among children under 5 years', 'value': 'NUTRITION_WH_2'}
        ],
        value='NUTRITION_ANT_HAZ_NE2',
        clearable=False
        ),
        #row 1
        html.Div([
            dcc.Graph(id='barchart_section2', figure={}, style={"width": "50%", "height": "40vh"}),
            dcc.Graph(id='plot_section2', figure={}, style={"width": "50%", "height": "40vh"}),
        # put graphs side by side
        ], style={"display": "flex"}), 
        # row 2
        html.Div([
            dcc.Graph(id='boxplot_section2', figure={}, style={"width": "50%", "height": "40vh"}),
            dcc.Graph(id='barchart2_section2', figure={}, style={"width": "50%", "height": "40vh"}),
        ], style={"display": "flex"})

    ], style={'marginTop': 50, 'display': 'none'}),
    #section 3
    html.Div(id='section3', children=[
        html.H3("Higher investment doesn't always equate to better outcomes",
                style= {'padding-left':'1%'}),
        dcc.Dropdown(
        id='dropdown3',
        options=[
            {'label': 'Stunting prevalence among children under 5 years', 'value': 'NUTRITION_ANT_HAZ_NE2'},
            {'label': 'Overweight prevalence among children under 5 years', 'value': 'NUTRITION_ANT_WHZ_NE2'},
            {'label': 'Wasting prevalence among children under 5 years', 'value': 'NUTRITION_WH_2'}
        ],
        value='NUTRITION_ANT_HAZ_NE2',
        clearable=False
        ),
        #row 1
        html.Div([
            dcc.Graph(id='correlations2_section3', figure={}, style={"width": "50%", "height": "40vh"}),
            dcc.Graph(id='correlations_section3', figure={}, style={"width": "50%", "height": "40vh"}),
        # put graphs side by side
        ], style={"display": "flex"}), 
        html.Div([
            dcc.Graph(id='correlations3_section3', figure={}, style={"width": "50%", "height": "40vh"}),
            dcc.Graph(id='correlations4_section3', figure={}, style={"width": "50%", "height": "40vh"}),

        ], style={"display": "flex"})
    ]),
    # #section 4
    # html.Div(id='section4', children=[
    #     html.H3("future",
    #             style= {'padding-left':'1%'}),
    # ])

], style={"width": "100%", "padding": "0"})



@app.callback(
    dash.dependencies.Output('section1-graph', 'figure'),
    [dash.dependencies.Input('data-selector', 'value')]
)
def update_graph(data_type):
    df = fetch_data(data_type)
    df = format_malnutrition_data(df)
    print('updating choloropeth')
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

labels_dict = {"WPR":"Western Pacific",
               "SEAR":"South-East Asia",
               "EUR":"Europe",
               "EMR":"Eastern Mediterranean",
               "AMR":"Americas",
               "AFR":"Africa"
               }


@app.callback(
    [dash.dependencies.Output('barchart_section2', 'figure'),
     dash.dependencies.Output('plot_section2', 'figure'),
     dash.dependencies.Output('boxplot_section2', 'figure'),
     dash.dependencies.Output('barchart2_section2', 'figure'),

    ],
    [dash.dependencies.Input('dropdown2', 'value')],
    # prevent_initial_call=True
    )
def update_graph(data_type):
    df = fetch_data(data_type)
    print('updating barchart')
    recent_df = format_malnutrition_data(df)
    grouped_df = recent_df.groupby('REGION')['Numeric'].mean().reset_index().sort_values(by='Numeric', ascending=False)
    fig = px.bar(grouped_df, y='REGION', x='Numeric', orientation='h', labels = { "Numeric": "%", "REGION":''})
    fig.update_yaxes(tickvals=list(labels_dict.keys()), ticktext= list(labels_dict.values()))

    max_index = grouped_df['Numeric'].idxmax()
    most_affected_region = grouped_df.loc[max_index,'REGION']
    df['YEAR'] = df['YEAR'].astype(int)
    df_region = df[df['REGION'] == most_affected_region].groupby('YEAR')['Numeric'].mean().reset_index(drop=False).sort_values(by="YEAR")
    fig2 = px.line(df_region, x="YEAR", y="Numeric", title=f'% in {labels_dict[most_affected_region]} over time', labels = {'Numeric':'%',"YEAR":'Year'})
    
    fig3 = px.box(recent_df, x='REGION' ,y="Numeric", labels = { "Numeric": "%", "REGION":''})
    fig3.update_xaxes(tickvals=list(labels_dict.keys()), ticktext= list(labels_dict.values()))


    df_country = recent_df.groupby('COUNTRY')['Numeric'].mean().reset_index().sort_values(by='Numeric', ascending=False).iloc[:5,:]
    fig4 = px.bar(df_country, y='COUNTRY', x='Numeric', orientation='h', labels = { "Numeric": "%", "COUNTRY":''})
    # country_codes
    fig4.update_yaxes(tickvals=list(country_codes.keys()), ticktext= list(country_codes.values()))

    return fig, fig2,fig3, fig4




@app.callback(
    [dash.dependencies.Output('correlations_section3', 'figure'),
     dash.dependencies.Output('correlations2_section3', 'figure'),
     dash.dependencies.Output('correlations3_section3', 'figure'),
     dash.dependencies.Output('correlations4_section3', 'figure'),


    ],

    [dash.dependencies.Input('dropdown3', 'value')]
)
def update_graph(data_type):
    gdp_spending = fetch_data('GHED_GGHE-DGDP_SHA2011')
    recent_gdp_spending = format_malnutrition_data(gdp_spending)


    malnutrition_data = fetch_data(data_type)
    recent_malnutrition_data = format_malnutrition_data(malnutrition_data)
 
    recent_malnutrition_data = recent_malnutrition_data.rename(columns = {'Numeric':'Malnutrition'})
    recent_gdp_spending = recent_gdp_spending.rename(columns = {'Numeric':'GDP'})
 
    merg = recent_gdp_spending.merge(recent_malnutrition_data, left_on = 'COUNTRY', right_on='COUNTRY')

    # select all values by REGION and plot y= malnutrion (data_type) and x = gdp spending, then draw line through it

    print('updating 4 g1')
    merg = merg.rename(columns = {"REGION_x":"Region"})
    fig = px.scatter(merg, 
                 x='GDP', 
                 y='Malnutrition', 
                 color='Region',
                 hover_data=['COUNTRY'],
                 trendline='ols',
                 title="Does more public spending on health decrease malnutrition?",
                 labels={'Malnutrition': '%', 
                         'GDP': 'Domestic general government health expenditure (GGHE-D) as percentage of gross domestic product (GDP) (%)',
                         })
    fig.update_layout(legend_title_text='')
    for trace in fig.data: #update legend
        trace.name = labels_dict[trace.name]


    GDP_22 = pd.read_csv('local_data/GDP_22_per_capita_usd.csv')
    inv_map_iso3 = {v: k for k, v in country_codes.items()}
    GDP_22['iso'] = GDP_22['Area'].apply(lambda x: inv_map_iso3.get(x,'nan'))
    merge_2 = recent_malnutrition_data.merge(GDP_22, left_on='COUNTRY', right_on='iso')
    # fig2 = px.density_heatmap(merge_2, x='Value', y='Malnutrition', title='Heatmap of Malnutrition vs Value')
    merge_2 = merge_2.rename(columns ={'Value':'GDP Per Capita USD'})

    # Compute the correlation matrix
    corr_matrix = merge_2[['Malnutrition','GDP Per Capita USD']].corr()

    # Create a heatmap using plotly.figure_factory
    fig2 = ff.create_annotated_heatmap(
        z=corr_matrix.values,
        x=list(corr_matrix.columns),
        y=list(corr_matrix.index),
        annotation_text=corr_matrix.round(2).values,
        showscale=True
    )



    fig2.update_layout(title_text='Correlation Heatmap', title_x=0.5)




    hist, xedges, yedges = np.histogram2d(merge_2['Malnutrition'], merge_2['GDP Per Capita USD'], bins=30)

    # Mask zeros
    hist[hist == 0] = np.nan

    # Create the heatmap using go.Figure
    fig3 = go.Figure(go.Heatmap(
        z=hist,
        x=xedges,
        y=yedges,
        colorscale='Viridis',
        hoverongaps=False
    ))

    fig3.update_layout(title='Density Heatmap of Malnutrition vs GDP Per Capita USD', 
                       xaxis_title='Malnutrition %',
                       yaxis_title='GDP Per Capita USD')
    

    cost_healthy_diet = pd.read_csv('local_data/cost_healthy_diet.csv')
    cost_healthy_diet['iso'] = cost_healthy_diet['Area'].apply(lambda x: inv_map_iso3.get(x,'nan'))
    merge_3 = recent_malnutrition_data.merge(cost_healthy_diet, left_on='COUNTRY', right_on='iso')
    merge_3 = merge_3.rename(columns ={'Value':'Cost of healthy diet (PPP USD per person per day)', 'REGION':'Region'})
    fig4 = px.scatter(merge_3, 
                 x='Cost of healthy diet (PPP USD per person per day)', 
                 y='Malnutrition', 
                 color='Region',
                 hover_data=['COUNTRY'],
                 trendline='ols',
                 title="How does the relative cost of a healthy diet affect malnutrition rates?",
                 labels={'Malnutrition': '%'
                        #  'GDP': 'Domestic general government health expenditure (GGHE-D) as percentage of gross domestic product (GDP) (%)',
                         })
    fig4.update_layout(legend_title_text='')
    for trace in fig4.data: #update legend
        trace.name = labels_dict[trace.name]


    return fig3, fig, fig2, fig4

@app.callback(
    [dash.dependencies.Output(f"btn-section{i}", "style") for i in range(1,4)],  # Outputs for each button
    [dash.dependencies.Input(f"btn-section{i}", "n_clicks") for i in range(1,4)]  # Inputs for each button
)
def update_button_colors(*args):
    # 'args' will be a tuple of click counts for the buttons in the order btn-0, btn-1, btn-2

    # Find which button was most recently clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        print('no trigger')
        # No button has been clicked yet
        return [{
                'backgroundColor': f'{color}',  # Blue color
                'color': 'white',
                'border': 'none',
                'borderRadius': '8px',
                'padding': '10px 20px',
                'fontSize': '16px',
                'outline': 'none',
                'cursor': 'pointer',
                'marginLeft': 10
            } for color in ['red','#008CBA','#008CBA']]
    print(ctx.triggered)
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    clicked_btn_index = int(btn_id.split('-')[-1][-1])
    print(clicked_btn_index)
    # Generate the style for each button
    styles = []
    for i in range(1,4):
        if i == clicked_btn_index:
            styles.append({
            'backgroundColor': 'red', 
            'color': 'white',
            'border': 'none',
            'borderRadius': '8px',
            'padding': '10px 20px',
            'fontSize': '16px',
            'outline': 'none',
            'cursor': 'pointer',
            'marginLeft': 10
           })
        else:
            styles.append({
                'backgroundColor': '#008CBA',  # Blue color
                'color': 'white',
                'border': 'none',
                'borderRadius': '8px',
                'padding': '10px 20px',
                'fontSize': '16px',
                'outline': 'none',
                'cursor': 'pointer',
                'marginLeft': 10
            })  # Default color for other buttons

    return styles

# correlation between Domestic general government health expenditure (GGHE-D) as percentage of gross domestic product (GDP) (%)
# and malnutrition 

@app.callback(
    [dash.dependencies.Output('section1', 'style'),
     dash.dependencies.Output('section2', 'style'),
     dash.dependencies.Output('section3', 'style'),
     ],
    [dash.dependencies.Input('btn-section1', 'n_clicks'),
     dash.dependencies.Input('btn-section2', 'n_clicks'),
     dash.dependencies.Input('btn-section3', 'n_clicks'),

     ]
)
def toggle_sections(btn1, btn2, btn3):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dict(), {'display': 'none'} ,{'display':'none'} 
    else:
        btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if btn_id == 'btn-section1':
            return {'display': 'block'}, {'display': 'none'} , {'display':'none'} 
        elif btn_id == 'btn-section2':
            return {'display': 'none'}, {'display': 'block'} , {'display':'none'} 
        elif btn_id == 'btn-section3':
            return {'display': 'none'},  {'display':'none'},  {'display': 'block'} 




if __name__ == '__main__':
    app.run_server(debug=True,  host='0.0.0.0', port=8050)


