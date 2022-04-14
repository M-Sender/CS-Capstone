from turtle import color
from dash import Dash, html, dcc, Input, Output
import os
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
df = pd.read_csv('covid_US_full_by_day.csv') #https://raw.githubusercontent.com/M-Sender/CS-Capstone/master/covid_US_full_by_day.csv?token=GHSAT0AAAAAABTHEWZ4OUNHU6ESH2TYWTCQYSV4G3A
arr = []
for i in df.columns:
    if i != 'date':
        arr.append(dcc.Graph(figure=px.line(df, x='date', y=i,height=500,width=800)))
css_dict = {
    'page': {
        'backgroundColor': 'black',
        'fontFamily': 'sans-serif',
    },
    'heading': {
        'text-align':'center',
        'text-decoration':'underline',
        'margin-top':'7%',
        'color':'#86C232',
        'margin-bottom':'2%'},
    'paragraph': {
        'color':'rgb(157, 170, 179)',
        'padding-left':'7%',
        'padding-right':'7%',
        'font-size':'120%',
    }
}

def heading(text,style='heading'):
    return html.H2(text, style=css_dict[style])
def paragraph(text,style='paragraph'):
    return html.P(text, style=css_dict[style])
app.layout = html.Div(children=[
    
    dbc.Row(html.Div(children=[
        dbc.Row(html.H1(children='Music Trends During the Pandemic')),
        dbc.Row(html.H2(children='Sam Broth and Max Sender')),
        dbc.Row(html.H2(children='Mentor: Dr. Nick Mattei'))
    ]),className='text-center',style={'padding-top':'2%','color':'white'}),
    dbc.Row(html.Div(children=[
        dbc.Row(html.B(heading('1. Introduction'))), #make bold
        dbc.Row(paragraph('Lorep Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.')),
    ])),
    dbc.Row(html.Div(children=[
        dbc.Row(heading('2. Our Questions')),
        dbc.Row(html.Ul(children=[
            html.Li(paragraph('* What are the trends in music during the pandemic?')),
            html.Li(paragraph('* What are the trends in music during the pandemic?')),
            html.Li(paragraph('* What are the trends in music during the pandemic?')),
        ]
            
            
            )),
        dbc.Row(paragraph('This leads us to our hypothesis:')),
        dbc.Row(paragraph('lorep ipsum  simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a ga')),
    ])),
    dbc.Row(html.Div(children=[
        dbc.Row(html.B(heading('3. Our Analysis'))),
        
        
        
        
        
    ])),
    dcc.Graph(figure=px.line(df, x='date', y='vader', hover_data=['vader'],height=500,width=800)),
    dbc.Row(html.Div(children=arr,)),
        
    
],style=css_dict['page'])
                               
                        

if __name__ ==  '__main__':
    app.run_server(debug=True)