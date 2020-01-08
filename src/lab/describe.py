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
import pandas
from  scipy.stats import shapiro, sem
from src.utils.file import File
f = File()
filename = "./data/raw/san_francisco.csv.gz"
df = f.read(filename)
d = df.describe(percentiles=[.05,.1,.25,.5,.75,.9,.95],
                        include=np.number)
print(d.T.columns)


# %%
