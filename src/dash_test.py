# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

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

path_data_root = '/custom/corona/data_ECDC/data'
name_file = 'COVID-19-geographic-disbtribution-worldwide-2020-03-21.xlsx'
path_data = path_data_root + '/' + name_file
df = dm.load_data_cases(path_data_root,name_file)
    
"""
select data for vizualisation, should be done automatically by the interface later
"""
sel_countries = ['Germany','Italy','United_States_of_America','France','Spain']
first_day = '2020-02-15'

if(sel_countries != 'all'):
    df = df[df['country'].isin(sel_countries)]
else:
    df = df
    
df = df[df['date'] >= first_day]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

options_countries = [{'label' : country, 'value' : country} for country in df.country.unique()]

app.layout = html.Div(children=[
    html.H1(children='RELOADING '),

    html.Div(children='''
        Dash: A web application framework for Python.sdfsaf
    '''),
    
    dcc.Markdown(children=markdown_text),
    
    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        options=options_countries,
        value=['MTL', 'SF'],
        multi=True
    ),
        
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': 
            [
                dict(
                    #x=df[df['country'] == country]['date'].apply(lambda x : x.strftime('%Y-%m-%d')),
                    x = np.arange(len(df[df['country'] == country]['date']))[::-1],
                    y = df[df['country'] == country]['cases_cumulative'],
                    text='was?',
                    mode='markers',
                    opacity=1,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=country
                ) 
                
            for country in df.country.unique()
            ],
            
            'layout': dict(
                xaxis={'type': 'linear', 'title': 'Time'},
                yaxis={'type': 'log', 'title': 'Cumulated Cases'},
                height= 700,
                width = 700,
                margin={'l': 100, 'b': 100, 't': 100, 'r': 100},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
    
    

])
             
            

print('__name__: ',__name__)
if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_hot_reload_max_retry=3000)
    


#%%
#a = df[df['country'] == country]['date'].apply(lambda x : x.strftime('%Y-%m-%d'))
