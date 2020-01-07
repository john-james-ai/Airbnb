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

from ..utils.file import File
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
        super(DataCollection, self).__init__(name=name, df=df)
        self._datasets = {}
        
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
    def __init__(self, name, df=None):
        super(DataSet, self).__init__(name=name, df=df)                

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        return self

    @property
    def columns(self):
        return self._df.columns.values.tolist()
    
    @property
    def nrows(self):
        return len(self._df)

    @property
    def ncols(self):
        return len(self.columns)

    def add(self, data):
        pass

    def remove(self, name):
        pass

    def import_data(self, filename):
        """Reads the data from the location designated by the filename."""
        f = File()
        self._df = f.read(filename)
        return self

    def export_data(self, filename, df):
        """Writes the data to the location designated by the filename."""        
        f = File()
        f.write(filename, df)
        return self

    def get_data(self, attribute=None):
        """Method to return all data or one, or more attributes.

        Parameters
        ----------
        attribute : str or list (Optional)
            The attribute or attributes to retrieve

        Returns
        -------
        DataFrame or Series
        
        """
        if attribute:
            return self._df[attribute]
        return self._df

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




