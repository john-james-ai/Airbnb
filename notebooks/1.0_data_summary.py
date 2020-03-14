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
from src.data.listings import DataGroup

path = "./data/raw/san-francisco"
datagroup = DataGroup(name='san-francisco')
datagroup.add_dataset_from_path(path)
summary = datagroup.summarize()
summary_data = summary['data']
summary_stats = summary['stats']

