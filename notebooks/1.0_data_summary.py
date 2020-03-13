#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : 1.0_data_summary.py                                               #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/airbnb                         #
# --------------------------------------------------------------------------- #
# Created       : Friday, January 17th 2020, 3:54:41 am                       #
# Last Modified : Friday, March 6th 2020, 11:28:38 am                         #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
#%%
import os
import sys

import numpy as np
import pandas as pd

root = "../data/raw/san-francisco"
if os.path.exists(root):
    summary_file = "../reports/figures/1.0_data_summary.csv"
    columns_file = "../reports/figures/1.0_columns.csv"
else:
    root = "./data/raw/san-francisco"
    summary_file = "./reports/figures/1.0_data_summary.csv"
    columns_file = "./reports/figures/1.0_columns.csv"

def summarize(root):
    base = "../data/raw/san-francisco/2019/ca_san-francisco_2019-12-04_data_listings.csv.gz"
    df_base = pd.read_csv(base, low_memory=False)
    columns = {'variable': df_base.columns.tolist()}
    city = []
    date = []
    rows = []
    cols = []
    size = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            city.append(name.split("_")[1:3][0])
            date.append(name.split("_")[2:3][0])
            df = pd.read_csv(os.path.join(path, name), low_memory=False)            
            rows.append(df.shape[0])
            cols.append(df.shape[1])
            size.append(round(sum(df.memory_usage(index=True))/1000000),2)

            columns[name.split("_")[2:3][0]] = np.in1d(df_base.columns.tolist(), df.columns.tolist())

    summary = {'City': city, 'Date': date, 'Observations': rows, \
        'Variables': cols, 'Size (MB)': size}
    summary = pd.DataFrame(summary)    
    summary.to_csv(summary_file, index=False)
    
    columns = pd.DataFrame(columns)
    booleandf = columns.select_dtypes(include=[bool])
    booleanDictionary = {True: ' ', False: '*'}
    for column in booleandf:
        columns[column] = columns[column].map(booleanDictionary)
    
    columns.to_csv(columns_file, index=False)
    return summary, columns

if os.path.exists(summary_file):
    summary = pd.read_csv(summary_file)
    columns = pd.read_csv(columns_file)
else:
    summary, columns = summarize(root)

# %%
