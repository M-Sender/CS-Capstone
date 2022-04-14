import matplotlib
matplotlib.use('Agg')
from dash import Dash, html, dcc, Input, Output
import os
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
df = pd.read_csv('https://raw.githubusercontent.com/M-Sender/CS-Capstone/master/covid_US_full_by_day.csv') #https://raw.githubusercontent.com/M-Sender/CS-Capstone/master/covid_US_full_by_day.csv?token=GHSAT0AAAAAABTHEWZ4OUNHU6ESH2TYWTCQYSV4G3A
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
metricExpl = {
    'vader':'Vader',
    'date':'Date',
    'polarity':'Polarity',
    'dancibility':'Dancibility',
    'subjectivity':'Subjectivity',
    'vader_compound':'Vader Compound',
    'vader_neg':'Vader Negative',
    'vader_neu':'Vader Neutral',
    'vader_pos':'Vader Positive',
    'subjectivity':'Subjectivity',
    'valence':'Valence',
    'tempo':'Tempo',
    
}
app.layout = html.Div(children=[
    
    dbc.Row(html.Div(children=[
        dbc.Row(html.H1(children='Music Trends During the Pandemic')),
        dbc.Row(html.H2(children='Sam Broth and Max Sender')),
        dbc.Row(html.H2(children='Mentor: Dr. Nick Mattei'))
    ]),className='text-center',style={'padding-top':'2%','color':'white'}),
    html.Div(dbc.Row(children=[dcc.Dropdown(df.columns,id='yaxis',value='vader',style={'width':'50%','text-align':'center','padding-left':'25%'}),dcc.Dropdown(df.columns,id='xaxis',value='date',style={'width':'50%','text-align':'center','padding-left':'25%'})],style={'padding-top':'2%','color':'black'})),
        
    
    html.Div([dcc.RadioItems(id='graphType',options=[{'label':'Line','value':'line'},{'label':'scatter','value':'scatter'}],value='line')],style={'padding-top':'2%','color':'white'}),
    html.Div(id='metricText',style={'padding-top':'2%','color':'white'}),
    dcc.Graph(id='graph',style={'padding-top':'2%','color':'black'}),
    
    #dbc.Row(html.Div(children=arr,)),
        
    
],style=css_dict['page'])
@app.callback(
    Output('graph', 'figure'),
    [Input('xaxis', 'value'),
     Input('yaxis', 'value'),
     Input('graphType', 'value')])
def update_graph(xaxis_name='date', yaxis_name='vader', graphType='line'):
    if graphType=='line':
        return px.line(df, x=xaxis_name, y=yaxis_name,height=500,width=800)
    elif graphType=='scatter':
        return px.scatter(df, x=xaxis_name, y=yaxis_name,height=500,width=800)
@app.callback(
    Output('metricText', 'children'),
    [Input('xaxis', 'value'),
     Input('yaxis', 'value')]
)
def update_text(xaxis_name='date', yaxis_name='vader'):
    retStr = '{xaxis} is being graphed on the x-axis and is displaying the {xaxis_exp}. On the y-axis, {yaxis} is being graphed and is displaying the {yaxis_exp}.'.format(xaxis=xaxis_name[0].upper()+xaxis_name[1:],xaxis_exp=metricExpl[xaxis_name],yaxis=yaxis_name,yaxis_exp=metricExpl[yaxis_name])
    return   retStr

if __name__ ==  '__main__':
    app.run_server(debug=True)
