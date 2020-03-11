#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : missing.py                                                        #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/airbnb                         #
# --------------------------------------------------------------------------- #
# Created       : Tuesday, March 10th 2020, 10:56:12 pm                       #
# Last Modified : Tuesday, March 10th 2020, 10:56:12 pm                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
#%%
import pandas as pd
path = "../../data/raw/san-francisco/2019/ca_san-francisco_2019-12-04_data_listings.csv.gz"
df = pd.read_csv(path)
missing = df.isna().sum() / df.shape[0]
print(missing.shape)
def count_values_in_range(series, min_range, max_range):
    return series.between(left=min_range, right=max_range).sum()

counts = []
min_ranges = [0.000, 0.001, 0.051, 0.101, 0.251, 0.501]
max_ranges = [0.000, 0.050, 0.100, 0.250, 0.500, 1.000]
for min_range, max_range in zip(min_ranges, max_ranges):
    counts.append(count_values_in_range(missing, min_range, max_range))
print(counts)
