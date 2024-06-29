""" Samples partially taken from plotly documentation 
https://dash.plotly.com/minimal-app

Interactive app with multiple outputs
"""
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
df['country'] = df['country'].str.lower()
SECRETS = json.load(open("secrets/secrets.json"))
MAPBOX_ACCESS_TOKEN = SECRETS["MAPBOX_ACCESS_TOKEN"]

# Load geopandas world dataset
MAPFILE = 'data/countries.geojson'
gdf = gpd.read_file(MAPFILE)
gdf = gdf.rename(columns={'ADMIN':'country'})
gdf['country'] = gdf['country'].str.lower()


# Merge the dataframes
df_geo = gdf.merge(df, how='left', left_on='country', right_on='country')
df_geo.country = df_geo.country.str.capitalize()
df.country = df.country.str.capitalize()


app = Dash()

app.layout = [
    html.H1(children='Test 4', style={'textAlign':'center'}),
    dcc.Dropdown(list(df.country.unique())+["All"], 'All', id='dropdown-selection'),
    html.Br(),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10,id='table-content'),
    dcc.Graph(id='map-content'),
    dcc.Graph(id='graph-content'),
]


@callback(
    [
        Output('graph-content', 'figure'),
        Output('table-content', 'data'),
        Output('map-content', 'figure')
    ],
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    print('=====================')
    if value == 'All' or value is None:
        dff = df
    else:
        dff = df[df.country==value]
    
    line_graph = px.line(dff, x='year', y='pop')
    table_output = dff.to_dict('records')

    # Latest life expectancy map
    latest_year = df['year'].max()
    df_latest = df_geo[df_geo['year'] == latest_year]
    df_latest = df_latest.dropna(subset=['lifeExp'])
    print("Latest year: \n", latest_year)
    print("Head:\n",df_latest.head())

    fig_map = px.choropleth_mapbox(
        df_latest,
        geojson=df_latest.geometry,
        locations=df_latest.index,
        color='lifeExp', 
        hover_name='country',  
        mapbox_style="carto-positron",
        zoom=1,
        center={"lat": 0, "lon": 0},
    )
    fig_map.update_layout(
        title_text='Latest Life Expectancy',
        mapbox_accesstoken=MAPBOX_ACCESS_TOKEN)
    
    return [
        line_graph,
        table_output,
        fig_map
        ]

if __name__ == '__main__':
    app.run(debug=True)