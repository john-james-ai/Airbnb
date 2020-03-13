#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : Airbnb                                                             #
# Version : 0.1.0                                                              #
# File    : describe.py                                                        #
# Python  : 3.8.0                                                              #
# ---------------------------------------------------------------------------- #
# Author : John James                                                          #
# Company: DecisionScients                                                     #
# Email  : jjames@decisionscients.com                                          #
# ---------------------------------------------------------------------------- #
# Created      : Tuesday, 7th January 2020 6:24:43 pm                          #
# Last Modified: Tuesday, 7th January 2020 6:24:43 pm                          #
# Modified By  : John James (jjames@decisionscients.com>)                      #
# ---------------------------------------------------------------------------- #
# License: BSD                                                                 #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
#%%
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, kurtosistest, skew, skewtest, shapiro


path = "../../data/raw/san-francisco/2019/ca_san-francisco_2019-12-04_data_listings.csv.gz"

df = pd.read_csv(path)
data = df.select_dtypes([np.number])
cols = np.array(data.columns)
# Compute basic descriptive statistics, round to 2 sig digits, and transform.
d = data.describe(percentiles=[0.5], include=np.number)   
d = d.round(2)
d = d.T
# Add missing counts 
d_missing = data.isnull().sum()
d_missing = d_missing.rename('# Missing')
# Add missing percentages
d_pct_missing = round(data.isnull().sum() / len(data) * 100, 2)
d_pct_missing = d_pct_missing.rename('% Missing')
# Add Kurtosis
d_kurtosis = data.kurtosis()
d_kurtosis = d_kurtosis.rename('Kurtosis')
# Add Skew
d_skew = data.skew()
d_skew = d_skew.rename('skew')
# Concatenate pandas objects into dataframe
d = pd.concat([d, d_missing, d_pct_missing, d_kurtosis, d_skew], axis=1)
# Add Kurtosis test
_, d_kurtosis_test = kurtosistest(data)
d['Kurtosis p-value'] = pd.DataFrame(data=[d_kurtosis_test], columns=cols).T
# Add Skew test
_, d_skew_test = skewtest(data)
d['Skew p-value'] = pd.DataFrame(data=[d_skew_test], columns=cols).T
# Add shapiro
df = data.apply(lambda x: pd.Series(shapiro(x), index=['w', 'Shapiro p-value'])).T
d = pd.concat([d, df['Shapiro p-value']], axis=1)
print(d)


# d_pct_missing = round(data.isnull().sum() / len(data) * 100, 2)
# d_pct_missing = d_pct_missing.rename('% Missing')
# d = pd.concat([d.T, d_missing.T, d_pct_missing.T], axis=1)
# d = pd.concat([d, kurtosis(data)]
# _, d['Kurtosis p-value'] = kurtosistest(data)
# d['Skew'] = skew(data)
# _, d['Skew p-value'] = skewtest(data)
# d['Shapiro'], d['Shapiro p-value'] = shapiro(data)





# %%
