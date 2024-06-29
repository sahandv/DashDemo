""" Samples partially taken from plotly documentation 

Non-interactive App
"""
from dash import Dash, html, dash_table
import pandas as pd

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.H1(children='Test 1', style={'textAlign':'center'}),
    html.Div(children='My First App with Data!'),
    html.Hr(),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)