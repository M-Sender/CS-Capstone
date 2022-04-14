from turtle import color
import matplotlib
from matplotlib.pyplot import legend
matplotlib.use('Agg')
from dash import Dash, html, dcc, Input, Output
import os
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from functools import partial
f = partial(pd.to_datetime,yearfirst=True)


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
df = pd.read_csv('covid_US_full_by_day.csv')
df['date'] = pd.to_datetime(df['date'],dayfirst=True)
df_pre = df[df['date']<=f('03/10/2020')]
df_post = df[df['date']>f('03/10/2020')]


css_dict = {
    'page': {
        'backgroundColor': 'blue',
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
    
    dbc.Row(html.Div(children=[#HEADER
        dbc.Row(html.H1(children='Music Trends During the Pandemic')),
        dbc.Row(html.H2(children='Sam Broth and Max Sender')),
        dbc.Row(html.H2(children='Mentor: Dr. Nick Mattei'))
    ]),className='text-center',style={'padding-top':'2%','color':'white','backgroundColor':'black'}),#HEADER END______
    
    #BEGIN DUAL PAGE
    html.Div(children=[
        dbc.Row(children=[dbc.Col(children=[        
    #left side
            html.Div(dbc.Row(children=[dcc.Dropdown(df.columns,id='yaxis',value='vader',style={'width':'50%','text-align':'center','padding-left':'25%'})],style={'padding-top':'2%','color':'black'})),
            html.Div([ html.Div(id='metricText',style={'padding-top':'2%','color':'black'})]),
            dcc.Graph(id='graph',style={'padding-top':'2%','color':'white'}),],width=9),
                          
                          #Right side
        dbc.Col(children=[html.P('cool stuff')],width=3,style={'backgroundColor':'black'})]),
        
        ]),

    
    #dbc.Row(html.Div(children=arr,)),
        
    
],style=css_dict['page'])
@app.callback(
    Output('graph', 'figure'),
    Input('yaxis', 'value'))
def update_graph(yaxis_name='vader'):
    fig = make_subplots(rows=1,cols=2,shared_yaxes=True,vertical_spacing=0.1,subplot_titles=('Pre-pandemic','Pandemic'))
    fig.add_trace(go.Scatter(x=df_pre['date'],y=df_pre[yaxis_name],mode='lines',name=yaxis_name),row=1,col=1)
    fig.add_trace(go.Scatter(x=df_post['date'],y=df_post[yaxis_name],mode='lines',name=yaxis_name),row=1,col=2)
    fig.update_layout(title_text=yaxis_name,xaxis_title='date',yaxis_title=yaxis_name,showlegend=False)
    fig.add_hline(y=df_pre[yaxis_name].mean(),row=1,col=1)
    fig.add_hline(y=df_post[yaxis_name].mean(),row=1,col=2)
        #return px.line(df, x=xaxis_name, y=yaxis_name,height=500,width=800)
    return fig
        #return px.scatter(df, x=xaxis_name, y=yaxis_name,trendline='lowess' ,height=500,width=800)
'''@app.callback(
    Output('metricText', 'children'),
    [Input('xaxis', 'value'),
     Input('yaxis', 'value')]
)
def update_text(xaxis_name='date', yaxis_name='vader'):
    retStr = '{xaxis} is being graphed on the x-axis and is displaying the {xaxis_exp}. On the y-axis, {yaxis} is being graphed and is displaying the {yaxis_exp}.'.format(xaxis=xaxis_name[0].upper()+xaxis_name[1:],xaxis_exp=metricExpl[xaxis_name],yaxis=yaxis_name,yaxis_exp=metricExpl[yaxis_name])
    return   retStr'''

if __name__ ==  '__main__':
    app.run_server(debug=True)
