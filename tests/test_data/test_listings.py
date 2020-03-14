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
import shutil
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
    def test_dataset_save(self, get_dataset):
        ds = get_dataset
        # Test without a path. 
        with raises(Exception):            
            ds.save()
        ds.unlock
        ds.save
        # Test with new path as directory
        path = "./tests/data/"
        newpath = os.path.join(path, os.path.basename(ds.target))
        ds.save(path)
        assert os.path.exists(newpath), "New file not created or incorrect filename"
        source = ds.source
        target = ds.target
        assert target == newpath, "Target not updated"
        assert source != target, "Target equals source"
        # Test witih new path as filepath
        path = "./tests/data/test_dataset_save_II.csv"
        ds.save(path)
        source = ds.source
        target = ds.target
        assert target == path, "Target not updated"
        assert source != target, "Target equals source"
        assert os.path.exists(path), "New file not created or incorrect filename"
        

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
    @mark.summary
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
    

# --------------------------------------------------------------------------- #
#                             Test DataGroup                                  #
# --------------------------------------------------------------------------- #
class DataGroupTests:
    """Tests DataGroup Class"""

    @mark.data
    @mark.datagroup    
    def test_datagroup_init(self):    
        name = 'san-francisco'
        dg = DataGroup(name=name) 
        dg_name = dg.name
        locked = dg.islocked
        assert name == dg_name, "Name not initialized."
        assert locked is False, "Locked is not initialized."
        dg.lock
        locked = dg.islocked
        assert locked is True, "Not locked."
        dg.unlock
        locked = dg.islocked
        assert locked is False, "Not unlocked."

    @mark.data
    @mark.datagroup    
    def test_datagroup_add_dataset_from_path(self): 
        # Load single dataset from path
        path = "./data/raw/san-francisco/2019/ca_san-francisco_2019-12-04_data_listings.csv.gz"
        name = 'san-francisco_2019-12-04'
        dg = DataGroup(name=name) 
        dg.add_dataset_from_path(path)
        # Get specified single dataset
        dict_of_datasets = dg.get_data(names=['2019-12-04'])
        assert isinstance(dict_of_datasets['2019-12-04'], DataSet), "get_data failed to return dict containing dataset"
        for k, v in dict_of_datasets.items():
            df = v.get_data()
            assert df.shape[0] > 8000, "Failed to return dataframe of >8000 rows"
            assert df.shape[1] == 106, "Failed to return dataframe of 106 columns"

    @mark.data
    @mark.datagroup    
    def test_datagroup_add_multiple_datasets_from_path(self, get_datagroup): 
        # Load single dataset from path
        path = "./data/raw/san-francisco/2019/"
        name = 'san-francisco_2019'        
        dg = get_datagroup
        dict_of_datasets = dg.get_data(names=['2019-12-04', '2019-10-14'])
        assert isinstance(dict_of_datasets['2019-12-04'], DataSet), "get_data failed to return dict containing dataset"
        assert isinstance(dict_of_datasets['2019-10-14'], DataSet), "get_data failed to return dict containing dataset"
        for k, v in dict_of_datasets.items():
            df = v.get_data()
            assert df.shape[0] > 8000, "Failed to return dataframe of >8000 rows"
            assert df.shape[1] == 106, "Failed to return dataframe of 106 columns"
        dict_of_datasets = dg.get_data()
        assert len(dict_of_datasets) == 12, "Failed to return all dataset objects."

    @mark.data
    @mark.datagroup    
    def test_datagroup_add_dataset(self, get_dataset): 
        ds = get_dataset
        dg = DataGroup(name='san-fran') 
        dg.add_dataset(ds)
        # Check for single dataset by name
        dict_of_datasets = dg.get_data(names=['2019-12-04'])
        assert isinstance(dict_of_datasets['2019-12-04'], DataSet), "get_data failed to return dict containing dataset"
        # Check for single dataset by default
        dict_of_datasets = dg.get_data()
        for k, v in dict_of_datasets.items():
            df = v.get_data()
            assert df.shape[0] > 8000, "Failed to return dataframe of >8000 rows"
            assert df.shape[1] == 106, "Failed to return dataframe of 106 columns"        
        assert len(dict_of_datasets) == 1, "Failed to return all dataset objects."        

    @mark.data
    @mark.datagroup    
    def test_datagroup_locking(self, get_datagroup):    
        name = 'san-francisco_2019'
        path = "./data/raw/san-francisco/2019/"
        dg = get_datagroup
        # Test unlocking of all DataSet objects
        dg.unlock_datasets()
        ds = dg.get_data()
        for name, dataset in ds.items():
            locked = dataset.islocked
            assert locked is False, "Failed to unlock all enclosed DataSet objects."
        # Test locking of all DataSet objects
        dg.lock_datasets()
        ds = dg.get_data()
        for name, dataset in ds.items():
            locked = dataset.islocked
            assert locked is True, "Failed to lock all enclosed DataSet objects."
        # Test unlocking named DataSet objects
        names = names=['2019-10-14', '2019-12-04']
        dg.unlock_datasets(names=names)
        ds = dg.get_data()
        for name, dataset in ds.items():
            locked = dataset.islocked
            if name in names:
                assert locked is False, "Failed to unlock all enclosed DataSet objects."            
            else:
                assert locked is True, "Failed to leave unnamed objects locked."  
        # Test locking named DataSets
        dg.lock_datasets(names=names)
        ds = dg.get_data()
        for name, dataset in ds.items():
            locked = dataset.islocked
            assert locked is True, "Failed to lock all enclosed DataSet objects."        
                  
    @mark.data
    @mark.datagroup    
    def test_datagroup_save(self, get_datagroup):    
        name = 'san-francisco_2019'        
        path = "./data/raw/san-francisco/2019/"
        dg = get_datagroup
        # Attempt to save without path parameter
        # should fail since items are locked
        with raises(Exception):
            dg.save()
        # Attempt to save with new path parameter, should be goodtogo
        path = "./tests/data/test_save_datagroup/"
        dg.save(path)
        ds = dg.get_data()
        for name, dataset in ds.items():
            target = dataset.target
            assert str(os.path.dirname(target)+"/") == path, "Target not updated to new location"
            assert os.path.exists(target), "DataSet objects not saved to correct location"
        shutil.rmtree(path)

    @mark.data
    @mark.datagroup    
    @mark.summary
    def test_datagroup_summary(self, get_datagroup):    
        name = 'san-francisco_2019'        
        path = "./data/raw/san-francisco/2019/"
        dg = get_datagroup
        summary = dg.summarize(verbose=True)        
        assert isinstance(summary, dict), "DataGroup summary failed to return a dataframe."
        assert isinstance(summary['stats'], pd.DataFrame), "Summary stats not dataframe object."
        assert isinstance(summary['data'], pd.DataFrame), "Summary data not dataframe object."