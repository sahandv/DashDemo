from dash import Dash, dcc, html
import plotly.express as px
import geopandas as gpd
import json

# Load GeoJSON file
gdf = gpd.read_file('data/countries.geojson')

# Convert GeoDataFrame to GeoJSON
geojson = gdf.to_crs(epsg=4326).__geo_interface__

# Load your Mapbox access token
SECRETS = json.load(open("secrets/secrets.json"))
MAPBOX_ACCESS_TOKEN = SECRETS["MAPBOX_ACCESS_TOKEN"]

# Initialize the Dash app
app = Dash()

# Create the map figure
fig_map = px.choropleth_mapbox(
    gdf,
    geojson=geojson,
    locations=gdf.index,
    color=None,  # No color as we just want to show the country shapes
    hover_name='ADMIN',  # Hover information
    mapbox_style="carto-positron",
    zoom=1,
    center={"lat": 0, "lon": 0},
)
fig_map.update_layout(
    mapbox_accesstoken=MAPBOX_ACCESS_TOKEN,
    margin={"r":0,"t":0,"l":0,"b":0}
)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Countries Map", style={'textAlign': 'center'}),
    dcc.Graph(id='map', figure=fig_map)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
