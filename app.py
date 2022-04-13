from dash import Dash, html, dcc, Input, Output
import os
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


app.layout = html.Div(children=[
    html.H1(children='Music Trends During the Pandemic'),
    html.P(children='Sam Broth and Max Sender'),
    html.P(children='Mentor: Dr. Nick Mattei')
]
                               
                                
                                )

if __name__ ==  '__main__':
    app.run_server(debug=True)