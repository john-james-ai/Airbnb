#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : test_univariate.py                                                #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/airbnb                         #
# --------------------------------------------------------------------------- #
# Created       : Wednesday, March 11th 2020, 11:29:26 am                     #
# Last Modified : Wednesday, March 11th 2020, 11:29:43 am                     #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Tests Univariate Analysis Modules."""
from pytest import mark
from ...src.analysis.univariate import DescribeQuant, DescribeQual
# --------------------------------------------------------------------------- #
#                             Test DataSet                                    #
# --------------------------------------------------------------------------- #
class DescribeTests:
    """Tests Univariate Analysis Classes"""

    @mark.analysis
    @mark.analysis_univariate    
    def test_describe_quant(self, get_dataset):
        ds = get_dataset
        data = ds.get_data()
        d = DescribeQuant()
        print(d.describe(data))

    @mark.analysis
    @mark.analysis_univariate  
    def test_describe_qual(self, get_dataset):
        ds = get_dataset
        data = ds.get_data()
        d = DescribeQual()
        print(d.describe(data))        