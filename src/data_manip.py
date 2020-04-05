#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 21:58:23 2020

@author: joachimrosenberger
"""
import pandas as pd
import os

def load_data_cases(path_data_root,name_file):
    
    path_data = path_data_root + '/' + name_file
    
    name_file_mod = name_file.split('.')[0] + '_mod_' + '.csv'
    path_data_mod = path_data_root + '/' + name_file_mod
    
    if(not os.path.isdir(path_data_mod)):
        
        df = pd.read_excel(path_data)
        df.rename(columns={'cases': 'new_cases','countriesAndTerritories':'country','dateRep':'date'},inplace=True)
        df = df.sort_values(by=['country','date'],ascending=[True,True])
        df['cases_cumulative'] = df.groupby('country')['new_cases'].cumsum()
        df = df.sort_values(by=['country','date'],ascending=[True,False])
        df.to_csv(path_data_mod)
    
    else:
        df = pd.read_csv(path_data_mod)
        
    return df