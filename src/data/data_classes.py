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
        if self._datasets:
            return len(self._datasets)
        else:
            return 0

    @property
    def dataset_names(self):
        names = []
        for _, d in self._datasets.items():
            names.append(d.name)
        return names


    def get_data(self, name=None):
        if name:
            return self._datasets[name]            
        else:
            return self._datasets

    def add(self, dataset):
        """Adds a DataSet object to the collection."""
        name = dataset.name
        self._datasets[name] = dataset
        return self

    def remove(self, name):
        """Removes a DataSet object from the collection."""
        del self._datasets[name]        
        return self

    def import_data(self, directory):
        """Creates DataSet objects, imports the data and adds the DataSets.

        Parameters
        ----------
        directory : str
            The directory containing the files to import.
        """

        filenames = os.listdir(directory)
        for filename in filenames:
            name = filename.split(".")[0]
            dataset = DataSet(name=name)
            path = os.path.join(directory, filename)
            dataset.import_data(filename=path)
            self.add(dataset=dataset)
        return self

    def export_data(self, directory, file_format='csv'):
        """Exports the data from contained DataSets to the directory in format.

        Parameters
        ----------
        directory : str
            The directory to which the data will be exported.
        file_format : str
            The format in which the data will be saved.
        """
        for name, dataset in self._datasets.items():
            filename = name + "." + file_format
            path = os.path.join(directory, filename)
            dataset.export_data(filename=path)
        return self


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

    def export_data(self, filename):
        """Writes the data to the location designated by the filename."""        
        f = File()
        f.write(filename, self._df)
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

    def add_columns(self, df):
        """Adds a series or dataframe to the dataset

        Parameters
        ----------
        df : DataFrame or Series object
            The data to add to the dataframe.
        """
        self._df = pd.concat([self._df, df], axis=1, ignore_index=True) 
        return self

    def remove_columns(self, cols):
        """Removes selected columns from the dataset.
        
        Parameters
        ----------
        cols : list
            A list of column names to remove from the dataset

        """
        self._df = self._df.drop(columns=cols, axis=1)
        return self