import matplotlib
from matplotlib.pyplot import legend, text
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
app.title = 'Music Trends During the Pandemic'
server = app.server
df = pd.read_csv('covid_US_full_by_day.csv')
df['Date'] = pd.to_datetime(df['Date'],dayfirst=True)
df_pre = df[df['Date']<=f('03/10/2020')]
df_post = df[df['Date']>f('03/10/2020')]


css_dict = {
    'page': {
        'backgroundColor':'teal',
        'fontFamily': 'sans-serif',
        'overflow-x':'hidden',
        'max-width':'100%',
    },
    'heading': {
        'text-align':'center',
        },
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
        'color':'black',
        'margin-left':'12.5%',
        },
    'metricText': {
        'margin-top':'2%',
        'text-align':'center',
    },
    'graph_container': {
        'padding-top':'2%',
        'color':'white',
        },
    'right_jumbo': {
        'margin-left':'-5%',
        #'height':'17%',
    }
}


def heading(text,style='heading'):
    return html.H2(text, style=css_dict[style])
def paragraph(text,style='paragraph'):
    return html.P(text, style=css_dict[style])
metricExpl = {
    'VADER':'VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media, and works well on texts from other domains.',
    'Polarity':'The expression that determines the sentimental aspect of an opinion. In textual data, the result of sentiment analysis can be determined for each entity in the sentence, document or sentence. The sentiment polarity can be determined as positive, negative and neutral.',
    'Danceability':'According to Spotify\'s Web API: "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable."',
    'Subjectivity':'How subjective the lyrics are (ranging from 0 to 1).',
    'VADER (Negative)':'How negative the lyrics are (ranging from -1 to 1).',
    'VADER (Neutral)':'How neutral the lyrics are (ranging from -1 to 1).',
    'VADER (Positive)':'How positive the lyrics are (ranging from -1 to 1).',
    'Valence':'According to Spotify\'s Web API: "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)."',
    'Tempo':'According to Spotify\'s Web API: "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration."',
    'Energy':'According to Spotify\'s Web API: "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy."',
    'Duration':'According to Spotify\'s Web API: "The duration of the track in milliseconds."',
    'Loudness': 'According to Spotify\'s Web API: "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db."',
    'Mode':'According to Spotify\'s Web API: "Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0."',
    'Speechiness': "How sppechy the song is.",
    'Acousticness':'According to Spotify\'s Web API: "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic."',
    'Instrumentalness':"How instrumental the song is.",
    'Liveness':'According to Spotify\'s Web API: "Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live."',

    
}

spotify_metrics = ['Duration','Danceability','Energy','Key','Loudness','Mode','Speechiness','Acousticness','Instrumentalness','Liveness','Valence','Tempo']
sentiment_metrics = ['Sentiment','Polarity','Subjectivity','VADER','VADER (Positive)','Vader (Negative)','VADER (Neutral)']
metContainer = {'Spotify':spotify_metrics,'sentiment':sentiment_metrics}
metDef = {'Spotify':'Energy','sentiment':'VADER'}
def make_fig(metric,metricText):
    return px.line(df,x='Date',y=metric,title=metricText,height=400,width=300)#370

def graph_layout(collection):
    ret_lay = html.Div([
    dbc.Container([
            html.Div(
                html.H3(children='Select a '+collection+' metric to explore:',className='display-4',style=css_dict['heading'])),
            html.Div(
                dbc.Row(children=[dcc.Dropdown(metContainer[collection],id='yaxis_'+collection,value=metDef[collection],style=css_dict['dropdown_menu'])],justify='center',align='center')),
            dcc.Graph(id='graph_'+collection,style=css_dict['graph_container']),
            html.Div([ html.Div(id=collection+'Text',style=css_dict['metricText'],className='lead')])],fluid=True,className='py-3')],className="p-3 bg-dark rounded-3 text-white p-5")
    return ret_lay
def right_jumbo(metric,metricName):
    ret_lay = html.Div([
                dbc.Container([
                    dcc.Graph(figure= make_fig(metric,metricName),), #style={'margin-left':'-35%','margin-top':'-33%'}
                   ],fluid=True,className='py-3')],className="p-3 bg-dark rounded-3 text-white p-5",style=css_dict['right_jumbo'])            
    return ret_lay

app.layout = html.Div(children=[
    
    dbc.Row(html.Div(children=[#HEADER
        dbc.Row(html.H1(children='Music Trends During the Pandemic')),
        dbc.Row(html.H2(children='Sam Broth and Max Sender')),
        dbc.Row(html.H2(children='Mentor: Dr. Nick Mattei'))
    ]),className='text-center',style={'padding-top':'2%','color':'white'}),#HEADER END______
    html.Hr(className='my-2'),

    #BEGIN DUAL PAGE
    html.Div(children=[
        dbc.Row(children=[dbc.Col(children=[        
    #left side            
            graph_layout('Spotify'),
            html.Hr(className='my-2'),
            graph_layout('sentiment'),
            
            ]
                                  
                                  
            ,width=8,style={'backgroundColor':'teal'}),     
        
         #Right side
        dbc.Col(children=[
            dbc.Row(children=[html.P(children='Some Fun Stuff:')],style={'padding-top':'2%','color':'white'}),
            right_jumbo('Search Term: Online Therapy','Search Term: Online Therapy'),
            html.Hr(className='my-2'),
            right_jumbo('Search Term: COVID','Search Term: COVID'),
            html.Hr(className='my-2'),
            right_jumbo('Search Term: Symptoms','Search Term: Symptoms'),
            html.Hr(className='my-2'),
            right_jumbo('Search Term: Vaccine','Search Term: Vaccine'),
            html.Hr(className='my-2'),
            right_jumbo('Duration','Duration'),
            ],width=4,style={'backgroundColor':'teal'})]),
        
        ]),

    
    #dbc.Row(html.Div(children=arr,)),
        
    
],style=css_dict['page'])
@app.callback(
    [Output('graph_Spotify', 'figure'),
     Output('SpotifyText', 'children')],
    Input('yaxis_Spotify', 'value'))
def update_spotify(yaxis_name='Energy'):
    fig = make_subplots(rows=1,cols=2,shared_yaxes=True,vertical_spacing=0.1,subplot_titles=('Pre-pandemic','Pandemic'))
    fig.add_trace(go.Scatter(x=df_pre['Date'],y=df_pre[yaxis_name],mode='lines',name=yaxis_name),row=1,col=1)
    fig.add_trace(go.Scatter(x=df_post['Date'],y=df_post[yaxis_name],mode='lines',name=yaxis_name),row=1,col=2)
    fig.update_layout(xaxis_title='Date',yaxis_title=yaxis_name,showlegend=False)
    fig.add_hline(y=df_pre[yaxis_name].mean(),row=1,col=1)
    fig.add_hline(y=df_post[yaxis_name].mean(),row=1,col=2)
    return [fig,metricExpl[yaxis_name]]
@app.callback(
    [Output('graph_sentiment', 'figure'),
     Output('sentimentText', 'children')],
    Input('yaxis_sentiment', 'value'))
def update_sentiment(yaxis_name='VADER'):
    fig = make_subplots(rows=1,cols=2,shared_yaxes=True,vertical_spacing=0.1,subplot_titles=('Pre-pandemic','Pandemic'))
    fig.add_trace(go.Scatter(x=df_pre['Date'],y=df_pre[yaxis_name],mode='lines',name=yaxis_name),row=1,col=1)
    fig.add_trace(go.Scatter(x=df_post['Date'],y=df_post[yaxis_name],mode='lines',name=yaxis_name),row=1,col=2)
    fig.update_layout(xaxis_title='Date',yaxis_title=yaxis_name,showlegend=False)
    fig.add_hline(y=df_pre[yaxis_name].mean(),row=1,col=1)
    fig.add_hline(y=df_post[yaxis_name].mean(),row=1,col=2)
    return [fig,metricExpl[yaxis_name]]

if __name__ ==  '__main__':
    app.run_server(debug=True)
