#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project: Airbnb                                                             #
# Version: 0.1.0                                                              #
# File: \analysis.py                                                          #
# Python Version: 3.8.0                                                       #
# ---------------                                                             #
# Author: John James                                                          #
# Company: Decision Scients                                                   #
# Email: jjames@decisionscients.com                                           #
# ---------------                                                             #
# Create Date: Sunday January 5th 2020, 5:35:06 pm                            #
# Last Modified: Sunday January 5th 2020, 6:51:35 pm                          #
# Modified By: John James (jjames@decisionscients.com)                        #
# ---------------                                                             #
# License: Modified BSD                                                       #
# Copyright (c) 2020 Decision Scients                                         #
# =========================================================================== #
"""Convenience functions used for analysis."""
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew

def describe_quant(x):
    """Computes descriptive statistics for quantitative variables."""
    d  = {}
    x=x.astype(float)
    print(x)
    a = x.describe()
    d['count'] = a[0]
    d['na'] = x.isna().sum()
    d['min'] = a[3]
    d['5%'] = np.quantile(a=x,q=0.05, axis=None)
    d['10%'] = x.quantile(q=0.1)
    d['25%'] = a[4]
    d['50%'] = a[5]
    d['mean'] = a[1]
    d['mode'] = x.mode()
    d['75%'] = a[6]
    d['90%'] = x.quantile(q=0.9)
    d['95%'] = x.quantile(q=0.95)
    d['max'] = a[7]
    d['std'] = a[2]
    d['kurtosis'] = kurtosis(x)
    d['skew'] = skew(x)
    return d

def describe_qual(x):
    """Computes descriptive statistics for qualitative variables."""
    d = {}
    a = x.describe()    
    d['count'] = a[0]
    d['na'] = pd.isnull(x)
    d['unique'] = a[1]
    d['top'] = a[2]
    d['freq'] = a[3]
    return d
