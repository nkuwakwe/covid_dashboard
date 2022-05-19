import numpy as np
import pandas as pd
import datetime

import dash
from dash import dcc
from dash import html
from dash.dash import Dash

import plotly.express as px
import plotly.graph_objects as go

'''Getting the DataFrame'''

import datetime

path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
today_date = datetime.date.today()
a = 1

try:
    current_date = datetime.date.strftime(today_date, '%m-%d-%Y')
    path += current_date + '.csv'
    df = pd.read_csv(path)
except:
    while True:
        try:
            path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
            current_date = today_date - datetime.timedelta(a)
            current_date = datetime.date.strftime(current_date, '%m-%d-%Y')
            path += current_date + '.csv'
            df = pd.read_csv(path)
        except:
            a += 1
            continue
        else:
            break


'''The Map'''

center_pt = {'lat' : df.iloc[677, 5],
    'lon' : df.iloc[677, 6]}
px.set_mapbox_access_token(open(r"token.txt").read()) #mapbox token goes here

map_fig = px.scatter_mapbox(df, lat="Lat", lon="Long_", size="Confirmed",
                size_max=20, zoom=3, color_discrete_sequence=['rgb(255, 109, 18)'], mapbox_style='dark',
                opacity=1, width=1250, height=600,
                center=center_pt,
                custom_data=['Confirmed', 'Deaths', 'Incident_Rate']
                
)

map_fig.update_layout(
    hoverlabel=dict(
        bgcolor="rgb(245, 109, 18)",
        font_size=16,
        font_family="Rockwell",
        
    ),
    
)


map_fig.update_traces(
    hovertemplate="Cases : %{customdata[0]:,}<br>Deaths : %{customdata[1]:,}"
)

map_fig.update_layout(margin_b=0, margin_t=0, margin_r=0, margin_l=0)



'''Confirmed Table'''

confirm_list = []

for i in range(len(df['Confirmed'])):
    if pd.notna(df['Confirmed'][i]) and pd.notna(df['Province_State'][i]) and df['Province_State'][i] != 'Unknown':
        state_country = f" <br><span style='color:rgb(235, 55, 52)'><b>{'{:,}'.format(df['Confirmed'][i])}</b></span> <span style='color:rgb(180, 180, 180)'> cases </span><br><span style='color:white'>{df['Province_State'][i]}, {df['Country_Region'][i]} </span> <span><br> </span>"
        confirm_list.append(state_country)

total_confirm = round(np.sum(df['Confirmed']) / 1000000, 1)


confirmed_fig = go.Figure(data=[go.Table(


    header=dict(values=[f'<b>   Total<br>Confirmed</b><br> <span style="color:rgb(235, 55, 52)">{total_confirm} mil</span>'],
                fill_color='rgb(80, 80, 80)',
                line_color='rgb(80, 80, 80)',
                align='left',
                font=dict(color='white', size=54),
                font_family='Comic Sans MS',
                height=100),
                

    cells=dict(values=[confirm_list],
               fill_color='rgb(80, 80, 80)',
               align='left',
               line_color='rgb(110, 110, 110)',
               font_family='Comic Sans MS',
               font=dict(size=16),

               
    ))
])
confirmed_fig.update_layout(margin_b=0, margin_t=0, margin_r=0, margin_l=0, height=900, width=300)


'''Deaths Table'''

death_list = []

for i in range(len(df['Deaths'])):
    if pd.notna(df['Deaths'][i]) and pd.notna(df['Province_State'][i]) and df['Province_State'][i] != 'Unknown':
        state_country = f" <br><span style='color:rgb(235, 55, 52)'><b>{'{:,}'.format(df['Deaths'][i])}</b></span> <span style='color:rgb(180, 180, 180)'> deaths </span><br><span style='color:white'>{df['Province_State'][i]}, {df['Country_Region'][i]} </span> <span><br> </span>"
        death_list.append(state_country)


total_death = round(np.sum(df['Deaths']) / 1000000, 1)

death_fig = go.Figure(data=[go.Table(

    header=dict(values=[f'<b>   Total<br>  Deaths</b><br>    <span style="color:rgb(235, 55, 52)">{total_death} mil</span>'],
                fill_color='rgb(80, 80, 80)',
                line_color='rgb(80, 80, 80)',
                align='left',
                font=dict(color='white', size=54),
                font_family='Comic Sans MS',
                height=100),
                

    cells=dict(values=[death_list],
               fill_color='rgb(80, 80, 80)',
               align='left',
               line_color='rgb(110, 110, 110)',
               font_family='Comic Sans MS',
               font=dict(size=16),
               
    ))
])

death_fig.update_layout(margin_b=0, margin_t=0, margin_r=0, margin_l=0, height=900, width=300)

'''Incident Rate Table'''

inc_list = []

for i in range(len(df['Incident_Rate'])):
    if pd.notna(df['Incident_Rate'][i]) and pd.notna(df['Province_State'][i]) and df['Province_State'][i] != 'Unknown':
        state_country = f" <br><span style='color:white'><b>{'{:,.0f}'.format(df['Incident_Rate'][i])}</b></span> <span style='color:rgb(180, 180, 180)'> cases a day<br><span style='color:white'>{df['Province_State'][i]}, {df['Country_Region'][i]}</span> <span><br> </span>"
        inc_list.append(state_country)

avg_incident = np.average(df['Incident_Rate'].dropna())

incident_fig = go.Figure(data=[go.Table(

    header=dict(values=[f"<b>Avg. Incident <br>     Rate</b><br>   {'{:,.2f}'.format(avg_incident)}"],
                fill_color='rgb(80, 80, 80)',
                line_color='rgb(80, 80, 80)',
                align='left',
                font=dict(color='white', size=54),
                font_family='Comic Sans MS',
                height=100),
                

    cells=dict(values=[inc_list],
               fill_color='rgb(80, 80, 80)',
               align='left',
               line_color='rgb(110, 110, 110)',
               font_family='Comic Sans MS',
               font=dict(size=16),
               
    ))
])

incident_fig.update_layout(margin_b=0, margin_t=0, margin_r=0, margin_l=0, height=900, width=400)


'''The App'''

app = dash.Dash(__name__)
app.title = 'Corona virus cases today'

app.layout = html.Div(

    children=[


        dcc.Graph(
            figure=map_fig,
            style={'width': '100%'}
            ),

        dcc.Graph(
            figure=confirmed_fig,
            style={
                'display': 'inline-block',
                'paddingRight':'22.847100175746924vh'
                }
            ),

        dcc.Graph(
            figure=incident_fig,
            style={
                'display': 'inline-block',
                'paddingRight':'19.332161687170476vh'
                }
            ),

        
        dcc.Graph(
            figure=death_fig,
            style={'display': 'inline-block'}
        ),
            
    ],
    style={'backgroundColor':'rgb(80, 80, 80)'}
)

if __name__ == "__main__":
    app.run_server(debug=True)

server = app.server