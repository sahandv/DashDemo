""" Samples partially taken from plotly documentation 
https://dash.plotly.com/minimal-app

Interactive app with single output
"""
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

app.layout = [
    html.H1(children='Test 2', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(id='graph-content')
]


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='lifeExp')

if __name__ == '__main__':
    app.run(debug=True)