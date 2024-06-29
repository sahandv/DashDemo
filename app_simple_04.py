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
MAPFILE = 'data/countries.geojson' # 'data/world/ne_110m_admin_0_countries.shp'
gdf = gpd.read_file(MAPFILE)
gdf = gdf.rename(columns={'ADMIN':'country'})
gdf['country'] = gdf['country'].str.lower()


# Merge the dataframes
df_geo = df.merge(gdf, how='left', left_on='country', right_on='country')



app = Dash()

app.layout = [
    html.H1(children='Test 3', style={'textAlign':'center'}),
    dcc.Dropdown(list(df.country.unique())+["All"], 'All', id='dropdown-selection'),
    html.Br(),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10,id='table-content'),
    dcc.Graph(id='graph-content'),
    dcc.Graph(id='map-content')
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
    if value == 'All' or value is None:
        dff = df
    else:
        dff = df[df.country==value]
    
    line_graph = px.line(dff, x='year', y='pop')
    table_output = dff.to_dict('records')
    # print("geojson: ", geojson.head())

    # Latest life expectancy map
    latest_year = df['year'].max()
    df_latest = df_geo[df_geo['year'] == latest_year]
    print("Latest year: ", latest_year)
    print(df_latest.head())
    df_latest = gpd.GeoDataFrame(df_latest,geometry='geometry')
    df_latest = df_latest.to_crs(epsg=4326).__geo_interface__
    fig_map = px.choropleth_mapbox(
        df_latest,
        geojson=df_latest.geometry,
        locations=df_latest.index,
        color='lifeExp',
        hover_name='country',
        hover_data={'geometry': False},
        mapbox_style="carto-positron",
        zoom=1,
        center={"lat": 0, "lon": 0},
    )
    fig_map.update_layout(
        title_text='Latest Life Expectancy',
        margin={"r":0,"t":0,"l":0,"b":0}, 
        mapbox_accesstoken=MAPBOX_ACCESS_TOKEN)
    
    return [
        line_graph,
        table_output,
        fig_map
        ]

if __name__ == '__main__':
    app.run(debug=True)