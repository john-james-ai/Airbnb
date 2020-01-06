#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : Airbnb                                                             #
# Version : 0.1.0                                                              #
# File    : data_classes.py                                                    #
# Python  : 3.8.0                                                              #
# ---------------------------------------------------------------------------- #
# Author : John James                                                          #
# Company: DecisionScients                                                     #
# Email  : jjames@decisionscients.com                                          #
# ---------------------------------------------------------------------------- #
# Created      : Monday, 6th January 2020 11:38:57 am                          #
# Last Modified: Monday, 6th January 2020 11:50:59 am                          #
# Modified By  : John James (jjames@decisionscients.com>)                      #
# ---------------------------------------------------------------------------- #
# License: BSD                                                                 #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
"""Data classes for individual data objects and containers.

This module defines a composite pattern for the following data classes:

    * DataComponent : The interface for all data classes.
    * DataSet : The abstract base class for all data leaf classes.
    * DataCollection : The composite container class for data objects.
    * AirbnbData : Data class containing data and descriptive statistics.
"""
#%%
import os

from abc import ABC, abstractmethod
import pandas as pd

from src.utils.file import FileGZDF
# --------------------------------------------------------------------------- #
#                                DataComponent                                #
# --------------------------------------------------------------------------- #
"""Abstract class that defines the interface for all Data classes.

Parameters
----------
name : str
       The name to assign to the DataComponent object
df : DataFrame
     The DataFrame containing the data

"""
class DataComponent(ABC):

    def __init__(self, name, df=None):
        self._name = name
        self._df = df
        self._datasets = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        return self        

    @abstractmethod
    def get_data(self, name):
        """Returns the Data object designated by the name."""
        pass

    @abstractmethod
    def add(self, data):
        pass

    @abstractmethod
    def remove(self, name):
        pass


# --------------------------------------------------------------------------- #
#                              DataCollection                                 #
# --------------------------------------------------------------------------- #
class DataCollection(DataComponent):
    """Container for DataSet objects.

    Parameters
    ----------
    name : str
        The name of the DataCollection
    directory : str
        The directory in which the DataCollection files are stored.
    """

    def __init__(self, name, df=None):
        self._datasets = {}
        self._name = name
        self._df = df
        
    @property
    def n_datasets(self):
        return len(self._datasets)

    @property
    def dataset_names(self):
        names = []
        for _, d in self._datasets.items():
            names.append(d.name)
        return names


    def get_data(self, name):
        try:
            return self._datasets[name]
        except (KeyError) as e:
            print(e)
            return self

    def get_datasets(self):
        return self._datasets


    def add(self, data):
        """Adds a DataSet object to the collection."""
        name = data.name
        self._datasets[name] = data        
        return self

    def remove(self, name):
        """Removes a DataSet object from the collection."""
        try:
            del self._datasets[name]
        except KeyError as e:
            print(e)

# --------------------------------------------------------------------------- #
#                              DataSet                                        #
# --------------------------------------------------------------------------- #
class DataSet(DataComponent):
    """Base class for all DataSet subclasses.
    
    Parameters
    ----------
    name : str
        The name of the dataset.
    df : DataFrame (Optional)
        The content in DataFrame format.
    """
    _FILE = {'gz': FileGZDF}

    def __init__(self, name, df=None):                
        self._name = name
        self._df = df

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        return self

    @property
    def attributes(self):
        return self._df.columns
    
    @property
    def nrows(self):
        return self._df.count()

    @property
    def ncols(self):
        return self._df.columns.count()

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
        return self

    def import_data(self, filename):
        """Reads the data from the location designated by the filename."""
        self._filename = filename
        filetype = filename.split(".")[-1]
        f = self._FILE.get(filetype)
        df = f.read(filename)
        return df

    def export_data(self, df, filename):
        """Writes the data to the location designated by the filename."""        
        filetype = filename.split(".")[-1]        
        f = self._FILE.get(filetype)
        f.write(df, filename)
        return self

    def get_data(self):
        """Returns the dataset in the DataFrame format."""
        return self._df

    def get_attribute(self, attribute):
        """Returns a series containing the attribute requested."""
        if attribute not in self._df.columns:
            raise ValueError("Attribute {attr} not valid for this data \
                            object.".format(attr=attribute))
        else:
            return self._df[attribute]

    def get_attributes(self, attributes):
        """Returns the DataFrame with the attributes requested."""
        for attribute in attributes:
            if attribute not in self._df.columns:
                raise ValueError("Attribute {attr} not valid for this data \
                                object.".format(attr=attribute))
            else:
                return self._df[["attributes"]]

# --------------------------------------------------------------------------- #
#                              AirbnbData                                     #
# --------------------------------------------------------------------------- #
class AirbnbData(DataSet):

    def __init__(self, name, df=None):                
        super(AirbnbData, self).__init__(name=name, df=df)

    def get_data(self):
        return self._df

    def add(self, dataset):
        pass

    def remove(self, name):
        pass




