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
        'backgroundColor':'#40E0D0',
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
    },
    'dropdown_menu': {
        'text-align':'center',
        'margin-top':'2%',
        'width':'50%',
        },
    'metricText': {
        'margin-top':'2%',
        'text-align':'center',
    },
    'graph_container': {
        'padding-top':'2%',
        'color':'white',
        },
}


def heading(text,style='heading'):
    return html.H2(text, style=css_dict[style])
def paragraph(text,style='paragraph'):
    return html.P(text, style=css_dict[style])
metricExpl = {
    'vader':'VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media, and works well on texts from other domains.',
    'polarity':'The expression that determines the sentimental aspect of an opinion. In textual data, the result of sentiment analysis can be determined for each entity in the sentence, document or sentence. The sentiment polarity can be determined as positive, negative and neutral.',
    'danceability':'How danceable the track is (ranging from 0 to 1).',
    'subjectivity':'How subjective the track is (ranging from 0 to 1).',
    'vader_compound':'Vader Compound',
    'vader_neg':'How negative the text is (ranging from -1 to 1).',
    'vader_neu':'How neutral the text is (ranging from -1 to 1).',
    'vader_pos':'How positive the text is (ranging from -1 to 1).',
    'valence':'relative mood of the song',
    'tempo':'Tempo/pace of the song',
    'energy':'how energetic the song is'
    
}

spotify_metrics = ['duration_ms','danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']
sentiment_metrics = ['sentiment','polarity','subjectivity','vader','vader_pos','vader_neg','vader_neut']
def make_fig(metric,metricText):
    return px.line(df,x='date',y=metric,title=metricText,height=400,width=300)
app.layout = html.Div(children=[
    
    dbc.Row(html.Div(children=[#HEADER
        dbc.Row(html.H1(children='Music Trends During the Pandemic')),
        dbc.Row(html.H2(children='Sam Broth and Max Sender')),
        dbc.Row(html.H2(children='Mentor: Dr. Nick Mattei'))
    ]),className='text-center',style={'padding-top':'2%','color':'white'}),#HEADER END______
    
    #BEGIN DUAL PAGE
    html.Div(children=[
        dbc.Row(children=[dbc.Col(children=[        
    #left side
    
            html.Div(html.H3(children='Select a spotify metric to explore:'),style={'text-align':'center','margin-top':'2%'}),
            html.Div(
            dbc.Row(children=[dcc.Dropdown(spotify_metrics,id='yaxis_spotify',value='energy',style=css_dict['dropdown_menu'])],justify='center',align='center')),
            html.Div([ html.Div(id='spotifyText',style=css_dict['metricText'],)]),
            dcc.Graph(id='graph_spotify',style=css_dict['graph_container']),
            
            html.Div(html.H3(children='Select a sentiment metric to explore:'),style={'text-align':'center','margin-top':'2%'}),
            html.Div(dbc.Row(children=[dcc.Dropdown(sentiment_metrics,id='yaxis_sentiment',value='vader',style=css_dict['dropdown_menu'])],justify='center')),
            html.Div([ html.Div(id='sentimentText',style=css_dict['metricText'])]),
            dcc.Graph(id='graph_sentiment',style=css_dict['graph_container']),]
                                  
                                  
            ,width=9,style={'backgroundColor':'white'}),     
        
         #Right side
        dbc.Col(children=[
            dbc.Row(children=[html.P(children='Some Fun Stuff:')],style={'padding-top':'2%','color':'white'}),
            dcc.Graph(figure= make_fig('symptoms: (United States)','Symptoms Search Frequency')),
            dcc.Graph(figure= make_fig('vader_neg','Symptoms Search Frequency')),
            dcc.Graph(figure= make_fig('subjectivity','Symptoms Search Frequency')),
            dcc.Graph(figure= make_fig('polarity','Symptoms Search Frequency')),
            dcc.Graph(figure= make_fig('vader_pos','Symptoms Search Frequency')),
            dcc.Graph(figure= make_fig('valence','Symptoms Search Frequency')),
            dcc.Graph(figure= make_fig('duration_ms','Symptoms Search Frequency')),

            ],width=3,style={'backgroundColor':'black'})]),
        
        ]),

    
    #dbc.Row(html.Div(children=arr,)),
        
    
],style=css_dict['page'])
@app.callback(
    [Output('graph_spotify', 'figure'),
     Output('spotifyText', 'children')],
    Input('yaxis_spotify', 'value'))
def update_spotify(yaxis_name='energy'):
    fig = make_subplots(rows=1,cols=2,shared_yaxes=True,vertical_spacing=0.1,subplot_titles=('Pre-pandemic','Pandemic'))
    fig.add_trace(go.Scatter(x=df_pre['date'],y=df_pre[yaxis_name],mode='lines',name=yaxis_name),row=1,col=1)
    fig.add_trace(go.Scatter(x=df_post['date'],y=df_post[yaxis_name],mode='lines',name=yaxis_name),row=1,col=2)
    fig.update_layout(xaxis_title='date',yaxis_title=str(yaxis_name[0].upper()+yaxis_name[1:]),showlegend=False)
    fig.add_hline(y=df_pre[yaxis_name].mean(),row=1,col=1)
    fig.add_hline(y=df_post[yaxis_name].mean(),row=1,col=2)
        #return px.line(df, x=xaxis_name, y=yaxis_name,height=500,width=800)
    return [fig,metricExpl[yaxis_name]]
        #return px.scatter(df, x=xaxis_name, y=yaxis_name,trendline='lowess' ,height=500,width=800)
@app.callback(
    [Output('graph_sentiment', 'figure'),
     Output('sentimentText', 'children')],
    Input('yaxis_sentiment', 'value'))
def update_sentiment(yaxis_name='vader'):
    fig = make_subplots(rows=1,cols=2,shared_yaxes=True,vertical_spacing=0.1,subplot_titles=('Pre-pandemic','Pandemic'))
    fig.add_trace(go.Scatter(x=df_pre['date'],y=df_pre[yaxis_name],mode='lines',name=yaxis_name),row=1,col=1)
    fig.add_trace(go.Scatter(x=df_post['date'],y=df_post[yaxis_name],mode='lines',name=yaxis_name),row=1,col=2)
    fig.update_layout(xaxis_title='date',yaxis_title=str(yaxis_name[0].upper()+yaxis_name[1:]),showlegend=False)
    fig.add_hline(y=df_pre[yaxis_name].mean(),row=1,col=1)
    fig.add_hline(y=df_post[yaxis_name].mean(),row=1,col=2)
        #return px.line(df, x=xaxis_name, y=yaxis_name,height=500,width=800)
    return [fig,metricExpl[yaxis_name]]

if __name__ ==  '__main__':
    app.run_server(debug=True)
