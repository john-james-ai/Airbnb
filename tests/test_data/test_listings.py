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
import pandas as pd
from pytest import mark, raises
from ...src.data.listings import DataSet, DataGroup 
# --------------------------------------------------------------------------- #
#                             Test DataSet                                    #
# --------------------------------------------------------------------------- #
class DataSetTests:
    """Tests DataSet Class"""

    @mark.data
    @mark.dataset    
    def test_dataset_init(self):
        path = "./data/raw/san-francisco/2019/ca_san-francisco_2019-12-04_data_listings.csv.gz"
        ds = DataSet(path)
        name = ds.name
        source = ds.source
        target = ds.target
        islocked = ds.islocked
        assert name == '2019-12-04', 'DataSet name incorrect'
        assert source == path, "DataSet source not correct"
        assert target == path, "DataSet target not correct"
        assert islocked is True, "DataSet islocked incorrect"
        ds = DataSet(path, name='san_francisco')
        name = ds.name
        assert name == 'san_francisco', "DataSet name incorrect"

    @mark.data
    @mark.dataset    
    def test_dataset_load(self):
        path = "./data/raw/san-francisco/2019/ca_san-francisco_2019-12-04_data_listings.csv.gz"
        ds = DataSet(path)
        ds.load()
        df = ds.get_data()
        assert df.shape[0] > 500, "DataSet load test - invalid shape[0]"
        assert df.shape[1] == 106, "DataSet load test - invalid shape[1]"

    @mark.data
    @mark.dataset    
    def test_dataset_save(self):
        path = "./data/raw/san-francisco/2019/ca_san-francisco_2019-12-04_data_listings.csv.gz"
        target = "./tests/data/test_dataset_save.csv"
        ds = DataSet(path)
        ds.load()
        with raises(Exception):
            ds.save()
        ds.save(target)
        assert os.path.exists(target), "DataSet save to new target not working."
        ds = DataSet(target)
        os.remove(target)
        ds.unlock
        ds.save()
        assert os.path.exists(target), "DataSet save to unlocked same source not working."
        

    @mark.data
    @mark.dataset    
    def test_dataset_get_data(self, get_dataset):    
        ds = get_dataset
        df = ds.get_data(columns=['id', 'city'])
        assert df.shape[0] > 8000, "df from get_data - invalid shape[0] "
        assert df.shape[1] == 2, "df from get_data - invalid shape[1] "
        df = ds.get_data(columns=['id', 'city'], n = 500)
        assert df.shape[0] > 500, "df from get_data - invalid shape[0] "
        assert df.shape[1] == 2, "df from get_data - invalid shape[1] "
        df = ds.get_data(pct = 10)
        assert df.shape[0] > 800, "df from get_data - invalid shape[0] "
        assert df.shape[1] == 106, "df from get_data - invalid shape[1] "
        df = ds.get_data(sample='head')
        assert df.shape[0] == 5, "df from get_data - invalid shape[0] "
        assert df.shape[1] == 106, "df from get_data - invalid shape[1] "   
        df = ds.get_data(sample='tail')
        assert df.shape[0] == 5, "df from get_data - invalid shape[0] "
        assert df.shape[1] == 106, "df from get_data - invalid shape[1] "               
        df1 = ds.get_data(sample='random')
        assert df1.shape[0] > 400 and df1.shape[0] < 800 , "df from get_data - invalid shape[0] "
        assert df1.shape[1] == 106, "df from get_data - invalid shape[1] "  
        df1 = ds.get_data(sample='random')
        df2 = ds.get_data(sample='random')
        assert df2.shape[0] > 400 and df2.shape[0] < 800 , "df from get_data - invalid shape[0] "
        assert df2.shape[1] == 106, "df from get_data - invalid shape[1] "  
        assert df1.equals(df2) == False, "df from get_data. Didn't return random copies"
        df1 = ds.get_data(sample='random',n=5000, seed = 10)
        df2 = ds.get_data(sample='random',n=5000, seed = 10)
        assert df2.shape[0] == 5000 , "df from get_data - invalid shape[0] "
        assert df2.shape[1] == 106, "df from get_data - invalid shape[1] "  
        assert df1.equals(df2) == True, "df from get_data. Didn't return same random with seeds"

    @mark.data
    @mark.dataset    
    def test_dataset_summarize(self, get_dataset):           
        ds = get_dataset
        summary = ds.summarize(verbose=True)
        assert isinstance(summary, dict), "DataSet summary: dict not returned"

    @mark.data
    @mark.dataset
    @mark.dataset_describe    
    def test_dataset_describe(self, get_dataset):           
        ds = get_dataset
        description = ds.describe(columns=['id', 'maximum_nights'])        
        assert isinstance(description, dict), "Describe didn't return a dictionary"
        assert isinstance(description['quant'], pd.DataFrame), "Describe didn't return a quant DataFrame"        
        print(description['quant'])
        description = ds.describe()        
        assert isinstance(description, dict), "Describe didn't return a dictionary"
        assert isinstance(description['quant'], pd.DataFrame), "Describe didn't return a quant DataFrame"        
        assert isinstance(description['qual'], pd.DataFrame), "Describe didn't return a qual DataFrame"        
        print("**************************************")
        print(description['quant'])
        print("**************************************")
        print(description['qual'])
    