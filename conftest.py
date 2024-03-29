#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : Airbnb                                                             #
# Version : 0.1.0                                                              #
# File    : conftest.py                                                        #
# Python  : 3.8.0                                                              #
# ---------------------------------------------------------------------------- #
# Author : John James                                                          #
# Company: DecisionScients                                                     #
# Email  : jjames@decisionscients.com                                          #
# ---------------------------------------------------------------------------- #
# Created      : Sunday, 5th January 2020 4:20:48 am                           #
# Last Modified: Monday, 6th January 2020 4:15:48 pm                           #
# Modified By  : John James (jjames@decisionscients.com>)                      #
# ---------------------------------------------------------------------------- #
# License: BSD                                                                 #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
# %%
import pandas as pd
from pytest import fixture

from .src.data.listings import DataSet, DataGroup

@fixture(scope="session")
def get_dataset():
    sf = "./data/raw/san-francisco/2019/ca_san-francisco_2019-12-04_data_listings.csv.gz"
    ds = DataSet(sf)
    ds.load()
    return ds

@fixture(scope="session")
def get_datagroup():
    path = "./data/raw/san-francisco/2019/"
    name = 'san-francisco_2019'        
    dg = DataGroup(name=name) 
    dg.add_dataset_from_path(path)    
    return dg



    