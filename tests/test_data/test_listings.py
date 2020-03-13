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
        df = ds.get_data()
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

    @mark.data
    @mark.dataset
    @mark.get_data
    def test_dataset_get(self, get_dataset):
        ds = get_dataset
        df = ds.get_data(n=10)
        assert df.shape[0] == 10, "get_dataset invalid rows; n=10, head"
        assert df.shape[1] == 106, "get_dataset invalid cols; n=10, head"
        df = ds.get_data(pct=10)
        assert df.shape[0] > 800, "get_dataset invalid rows; pct=10, head"
        assert df.shape[1] == 106, "get_dataset invalid cols; pct=10, head"
        columns = ['id', 'listing_url', 'scrape_id', 'last_scraped', 'name']
        df = ds.get_data(columns=columns, pct=10)
        assert df.shape[0] > 800, "get_dataset invalid rows; pct=10, head"
        assert df.shape[1] == 5, "get_dataset invalid cols; pct=10, head"
        summary = ds.summarize(verbose=False)
        assert isinstance(summary, dict), "Summary is not a dictionary"
