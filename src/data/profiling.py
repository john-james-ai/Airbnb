#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project: Airbnb                                                             #
# Version: 0.1.0                                                              #
# File: \profiling.py                                                         #
# Python Version: 3.8.0                                                       #
# ---------------                                                             #
# Author: John James                                                          #
# Company: Decision Scients                                                   #
# Email: jjames@decisionscients.com                                           #
# ---------------                                                             #
# Create Date: Sunday January 5th 2020, 3:55:07 am                            #
# Last Modified: Sunday January 5th 2020, 3:25:21 pm                          #
# Modified By: John James (jjames@decisionscients.com)                        #
# ---------------                                                             #
# License: Modified BSD                                                       #
# Copyright (c) 2020 Decision Scients                                         #
# =========================================================================== #
"""The objective of this module is to summarize the Airbnb datasets, primarily
through descriptive statistics, in order to assess its quality, consistency,
characteristics, anomalies, and statistics.

As a first step, let's 
"""
#%%
import os
import numpy as np
from scipy.stats import kurtosis
from scipy.stats import skew
import pandas as pd
directory = "../../data/raw/" 
directory_inside = "./data/raw/"


def get_filenames():
    filenames = []    
    with os.scandir(directory_inside) as files:
        for file in files:
            filenames.append(file.name)
    return filenames
    
#%%
if __name__ == "__main__":

    # Get a filenames
    #filenames = get_filenames()
    
    filename = os.path.join(directory_inside, filenames[0])
    df = pd.read_csv(filename)
    print(df.head)




# %%
