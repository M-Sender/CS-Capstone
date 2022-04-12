from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

#def make_bar(x,y,)

app = Dash(__name__)
df = pd.read_csv('../datasets/covid_US_full_by_day.csv')

app.layout = html.Div(children=[
    html.H1(children='Music Trends During the Pandemic'),
    html.P(children='Sam Broth and Max Sender'),
    html.P(children='Mentor: Dr. Nick Mattei')
]
                               
                                
                                )

if __name__ ==  '__main__':
    app.run_server(debug=True)