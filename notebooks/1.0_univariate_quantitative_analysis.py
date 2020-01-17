#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : 1.0_univariate_quantitative_analysis.py                           #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Friday, January 17th 2020, 3:54:41 am                       #
# Last Modified : Friday, January 17th 2020, 3:54:42 am                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Univariate exploratory data analysis of quantitative variables."""
#%%
import os
from pathlib import Path
import site
import sys
PROJECT_DIR = Path(__file__).resolve().parents[1]
site.addsitedir(PROJECT_DIR)

import pandas as pd

from src.data.data_classes import DataSet
# --------------------------------------------------------------------------- #
#                               OVERVIEW                                      #
# --------------------------------------------------------------------------- #
train_file = "../data/interim/san-francisco/train.csv"
validation_file = "../data/interim/san-francisco/validation.csv"
test_file = "../data/interim/san-francisco/test.csv"

train = DataSet(name='train')
train.import_data(filename=train_file)

validation = DataSet(name='validation')
validation.import_data(filename=validation_file)

test = DataSet(name='test')
test.import_data(filename=test_file)

data_summary = pd.DataFrame()
datasets = [train, validation, test]
for dataset in datasets:
    df = pd.DataFrame()    
    data = dataset.get_data()
    df[dataset.name] = data.dtypes
    data_summary = data_summary.append(df)
print(data_summary)


    


# %%
