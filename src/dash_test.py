# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd
import numpy as np
import flask
import json
from textwrap import dedent as d
from dash.dependencies import Input, Output, State

import data_manip as dm


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def generate_plot_cumulated_cases(df,countries,yscale):
    figure={
    'data': 
    [
        dict(
            #x=df[df['country'] == country]['date'].apply(lambda x : x.strftime('%Y-%m-%d')),
            x = np.arange(len(df[df['country'] == country]['date']))[::-1],
            y = df[df['country'] == country]['cases_cumulative'],
            #text='was?',
            mode='markers',
            opacity=1,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=country
        ) 
        
        for country in countries
    ],
    
    'layout': dict(
        xaxis={'type': 'linear', 'title': 'Time'},
        yaxis={'type': yscale, 'title': 'Cumulated Cases'},
        height= 700,
        width = 700,
        margin={'l': 100, 'b': 100, 't': 20, 'r': 100},
        legend={'x': 1, 'y': 1},
        hovermode='closest'
    )
    }
    return figure

port = 80
path_data_root = '/custom/corona/data_ECDC/data'
name_file = 'COVID-19-geographic-disbtribution-worldwide-2020-03-24.xlsx'
path_data = path_data_root + '/' + name_file
df = dm.load_data_cases(path_data_root,name_file)
    
"""
select data for vizualisation, should be done automatically by the interface later
"""
sel_countries = 'all'#['Germany','Italy','United_States_of_America','France','Spain']
first_day = '2020-02-15'

if(sel_countries != 'all'):
    df = df[df['country'].isin(sel_countries)]
else:
    df = df
    
df = df[df['date'] >= first_day]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, server=server)

markdown_text = '''
# Overview over covid 19 cases

Data taken from [ECDC](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide).
Last data pulled 24.03.2020 20:17 (GMT+1 / Berlin)
Do you want to add or change stuff or make suggestions: https://github.com/Jogala/corona
'''

options_countries = [{'label' : country, 'value' : country} for country in df.country.unique()]
default_countries_drop_down = ['Germany', 'Italy','United_States_of_America','United_Kingdom']

app.layout = html.Div(children=[

    dcc.Markdown(children=markdown_text),
    dcc.Markdown(children='## Cumulated Cases'),
    
    html.Label('Select countries:'),
    
    dcc.Dropdown(id='multi_drop_down_selection_countries',options=options_countries,
                 value=default_countries_drop_down,multi=True),
    
    html.Button(id='button_update_plot', n_clicks=0, children='update graph'),
    
    daq.BooleanSwitch(id='boolean_switch_log_linear', on=True,  label = 'log-linear'),#, labelPosition='right'), #color="#9B51E0"
    
    dcc.Graph(id='plot_cases_cumulated'),
        
        
])
    

@app.callback(Output('plot_cases_cumulated', 'figure'),
              [Input('button_update_plot', 'n_clicks'),
               Input('boolean_switch_log_linear', 'on')],
              [State('multi_drop_down_selection_countries', 'value'),
               State('boolean_switch_log_linear', 'on')])
def update_plot_cases_cumulated_upon_button_update_plot_pressed(n_clicks, _, countries, y_axis_log):
    
    if(y_axis_log == True):
        yscale = 'log'
    else:
        yscale = 'linear'
    
    figure = generate_plot_cumulated_cases(df,countries,yscale)    

    return figure



print('__name__: ',__name__)
if __name__ == '__main__':
    app.run_server(host= '0.0.0.0', port=port,debug=False,dev_tools_hot_reload_max_retry=3000)
    

