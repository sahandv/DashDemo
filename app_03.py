""" Samples partially taken from plotly documentation 
https://dash.plotly.com/minimal-app

Interactive app with multiple outputs
"""
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

app.layout = [
    html.H1(children='Test 3', style={'textAlign':'center'}),
    dcc.Dropdown(list(df.country.unique())+["All"], 'All', id='dropdown-selection'),
    html.Br(),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10,id='table-content'),
    dcc.Graph(id='graph-content')
]


@callback(
    [
        Output('graph-content', 'figure'),
        Output('table-content', 'data'),
    ],
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    if value == 'All' or value is None:
        dff = df
    else:
        dff = df[df.country==value]
        
    return [
        px.line(dff, x='year', y='lifeExp'),
        dff.to_dict('records')]

if __name__ == '__main__':
    app.run(debug=True)