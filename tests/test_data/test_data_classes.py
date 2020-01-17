#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : Airbnb                                                             #
# Version : 0.1.0                                                              #
# File    : test_data_classes.py                                               #
# Python  : 3.8.0                                                              #
# ---------------------------------------------------------------------------- #
# Author : John James                                                          #
# Company: DecisionScients                                                     #
# Email  : jjames@decisionscients.com                                          #
# ---------------------------------------------------------------------------- #
# Created      : Monday, 6th January 2020 4:34:30 pm                           #
# Last Modified: Monday, 6th January 2020 4:34:31 pm                           #
# Modified By  : John James (jjames@decisionscients.com>)                      #
# ---------------------------------------------------------------------------- #
# License: BSD                                                                 #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
"""Tests DataComponent classes."""
import os

import pandas as pd
import pytest
from pytest import mark
from pathlib import Path
import platform
import site
PROJECT_DIR = Path(__file__).resolve().parents[1]
site.addsitedir(PROJECT_DIR)
import shutil

from src.data.data_classes import DataCollection, DataSet
# ---------------------------------------------------------------------------- #
#                             Test DataSet                                     #
# ---------------------------------------------------------------------------- #
class DataSetTests:
    """Tests DataSet Class"""

    @mark.data
    @mark.dataset
    @mark.dataset_import
    def test_dataset_import(self):
        filename = "./tests/data/san_francisco.csv.gz"
        ds = DataSet(name='san_francisco')
        ds.import_data(filename)
        df = ds.get_data()
        assert len(df) > 0, "DataSet import failed"

    @mark.data
    @mark.dataset
    @mark.dataset_export
    def test_dataset_export(self):
        filename = "./tests/data/san_francisco.csv.gz"
        ds = DataSet(name='san_francisco')
        ds.import_data(filename)
        filename = "./tests/data/san_francisco_export.csv.gz"
        ds.export_data(filename)
        assert os.path.exists(filename), "DataSet export failed"

    @mark.data
    @mark.dataset
    @mark.dataset_properties
    @mark.dataset_properties_name
    def test_dataset_properties_name(self, get_dataset):
        ds = get_dataset
        name = ds.name
        assert name == "test_dataset", "Name property not set."
        ds.name = 'something_else'
        assert ds.name == "something_else", "Name property not set."


    @mark.data
    @mark.dataset
    @mark.dataset_get_data
    def test_dataset_get_data(self, get_dataset):
        ds = get_dataset
        df = ds.get_data()        
        cols = df.columns.values
        # Test no attribute
        df = ds.get_data()
        assert len(df.columns) == len(cols), "Get data failed to return all columns"

        # Test multiple attributes
        print(cols[1:4])
        df = ds.get_data(cols[1:4])
        assert len(df.columns) == 3, "Get data on multiple attributes failed."


    @mark.data
    @mark.dataset
    @mark.dataset_metadata
    def test_dataset_metadata(self, get_dataset):
        ds = get_dataset
        ds.metadata()

    @mark.data
    @mark.dataset
    @mark.dataset_summary
    def test_dataset_summary(self, get_dataset):
        ds = get_dataset
        ds.summarize() 
        ds.metadata()
# ---------------------------------------------------------------------------- #
#                             Test DataCollection                              #
# ---------------------------------------------------------------------------- #
class DataCollectionTests:
    """Tests DataSet Class"""

    @mark.data
    @mark.data_collection
    @mark.data_collection_add
    def test_data_collection_add(self, get_dataset):
        dataset = get_dataset
        dc = DataCollection(name='test_collection')
        dc.add(data=dataset)
        d = dc.get_data()
        assert len(d)== 1, "Dataset add not working"

    @mark.data
    @mark.data_collection
    @mark.data_collection_get_data
    def test_data_collection_get_data(self, get_dataset):
        dataset = get_dataset
        dc = DataCollection(name='test_collection')
        dc.add(data=dataset)
        d = dc.get_data()
        assert len(d) == 1, "Dataset add not working"        
        d = dc.get_data()
        assert isinstance(d["test_dataset"], DataSet), "Get data not working"

    @mark.data
    @mark.data_collection
    @mark.data_collection_remove
    def test_data_collection_remove(self, get_dataset):
        dataset = get_dataset
        dc = DataCollection(name='test_collection')
        dc.add(data=dataset)
        dc.remove('test_dataset')
        d = dc.get_data() 
        assert len(d) == 0, "Dataset remove not working"

    @mark.data
    @mark.data_collection
    @mark.data_collection_import_export_data
    def test_data_collection_import_export_data(self):
        directory = "./data/raw/san-francisco/2016/"        
        dc = DataCollection(name='test_collection')
        dc.import_data(directory)
        d = dc.get_data()
        assert len(d)== 10, "Dataset import not working"
        directory = "./tests/data/export/"
        shutil.rmtree(directory)
        dc.export_data(directory, "csv")
        d = dc.get_data()
        for name, data in d.items():
            name = name + ".csv"
            path = os.path.join(directory, name)
            assert os.path.exists(path), "Export is missing files."

    @mark.data
    @mark.data_collection
    @mark.data_collection_error
    def test_data_collection_error(self, get_dataset):
        dataset = get_dataset
        dc = DataCollection(name='test_collection')
        dc.add(data=dataset)
        with pytest.raises(Exception):
            dc.get_data(name='daa')
        with pytest.raises(Exception):
            dc.remove(name='daa')
        