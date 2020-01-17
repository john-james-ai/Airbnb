#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : Airbnb                                                             #
# Version : 0.1.0                                                              #
# File    : test_describe.py                                                   #
# Python  : 3.8.0                                                              #
# ---------------------------------------------------------------------------- #
# Author : John James                                                          #
# Company: DecisionScients                                                     #
# Email  : jjames@decisionscients.com                                          #
# ---------------------------------------------------------------------------- #
# Created      : Tuesday, 7th January 2020 6:04:11 pm                          #
# Last Modified: Tuesday, 7th January 2020 6:04:11 pm                          #
# Modified By  : John James (jjames@decisionscients.com>)                      #
# ---------------------------------------------------------------------------- #
# License: BSD                                                                 #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
"""Tests the Describe class."""
import os

import pandas as pd
import pytest
from pytest import mark
import shutil

from Airbnb.src.analysis.univariate import Describe
# ---------------------------------------------------------------------------- #
#                             Test DataSet                                     #
# ---------------------------------------------------------------------------- #
class DescribeTests:
    """Tests DataSet Class"""

    @mark.analysis
    @mark.analysis_univariate
    @mark.analysis_univariate_describe
    def test_analysis_univariate_describe(self, get_dataset):
        ds = get_dataset
        d = Describe()
        d.fit(ds)
        analysis = d.get_analysis()
        pd.set_option('display.max_columns', None)
        assert isinstance(analysis['quant'], pd.DataFrame), "No quant dataframe"
        assert isinstance(analysis['qual'], pd.DataFrame), "No qual dataframe"        
        print("***********************************************************")
        print(analysis['qual'])