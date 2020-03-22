#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 15:43:49 2020

@author: joachimrosenberger
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import data_manip as dm

#%%
path_data_root = '/custom/corona/data_ECDC/data'
name_file = 'COVID-19-geographic-disbtribution-worldwide-2020-03-21.xlsx'
path_data = path_data_root + '/' + name_file

df = dm.load_data_cases(path_data_root,name_file)
    
sel_countries = ['Germany','Italy','United_States_of_America','France','Spain']
first_day = '2020-02-15'
number_days_fit = 10
number_days_projection = 21

if(sel_countries != 'all'):
    df_sel = df[df['country'].isin(sel_countries)]
else:
    df_sel = df
    
df_sel = df_sel[df_sel['date'] >= first_day]

#%% Plot new cases

fig = plt.figure()
ax = fig.add_subplot()
for country,data in df_sel.groupby('country'):
    ax.plot(data['date'],data['new_cases'],label = country)

ax.set_title('New case')    
ax.legend()
ax.set_yscale('log')    
fig.show()
    
#%% Plot Cumulative cases

fig = plt.figure()
ax = fig.add_subplot()
for country,data in df_sel.groupby('country'):
    
    ax.plot(data['date'],data['cases_cumulative'],label = country)
    
    y = np.log(data['cases_cumulative'][:number_days_fit])[::-1]    
    t = np.arange(len(y))
    days_fit = data['date'][:number_days_fit]
    fit = np.polyfit(t, y, 1)
    
    #cases_cumulated = A*e^(alpha*t)
    alpha = fit[0]
    A = np.exp(fit[1])
    
    days_projection = pd.date_range(start=days_fit.iloc[-1], end=days_fit.iloc[0]+pd.Timedelta(number_days_projection, unit='D'))
    t_projection = np.arange(len(days_projection))
    cum_cases_projection = A*np.exp(alpha*t_projection)
    
    ax.plot(days_projection,cum_cases_projection, label = 'fit ' + country)


ax.set_title('Cumulative cases')    
ax.legend()
ax.set_yscale('log')    
fig.show()







