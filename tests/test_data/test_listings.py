#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : test_listings.py                                                  #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/airbnb                         #
# --------------------------------------------------------------------------- #
# Created       : Monday, January 6th 2020, 4:34:30 pm                        #
# Last Modified : Tuesday, March 10th 2020, 11:43:59 pm                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #

"""Tests Listing classes."""
import os
from pytest import mark
from ...src.data.listings import DataSet 
# --------------------------------------------------------------------------- #
#                             Test DataSet                                    #
# --------------------------------------------------------------------------- #
class DataSetTests:
    """Tests DataSet Class"""

    @mark.data
    @mark.dataset    
    def test_dataset_load(self):
        sf = "./data/raw/san-francisco/2019/ca_san-francisco_2019-12-04_data_listings.csv.gz"
        ds = DataSet(name='san_francisco')
        ds.load(sf)
        df = ds.get_dataframe()
        assert len(df) > 0, "DataSet load failed"

    @mark.data
    @mark.dataset
    def test_dataset_save(self):
        filename = "./tests/data/san_francisco.csv.gz"
        ds = DataSet(name='san_francisco')
        ds.load(filename)
        filename = "./tests/data/san_francisco_export.csv.gz"
        ds.save(filename)
        assert os.path.exists(filename), "DataSet export failed"
