#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project: Airbnb                                                             #
# Version: 0.1.0                                                              #
# File: \get_data.py                                                          #
# Python Version: 3.8.0                                                       #
# ---------------                                                             #
# Author: John James                                                          #
# Company: Decision Scients                                                   #
# Email: jjames@decisionscients.com                                           #
# ---------------                                                             #
# Create Date: Saturday January 4th 2020, 7:13:14 pm                          #
# Last Modified: Sunday January 5th 2020, 6:51:07 pm                          #
# Modified By: John James (jjames@decisionscients.com)                        #
# ---------------                                                             #
# License: Modified BSD                                                       #
# Copyright (c) 2020 Decision Scients                                         #
# =========================================================================== #
#                               GET DATA                                      #
# =========================================================================== #
"""Downloads the Airbnb from the Inside Airbnb site 
(http://insideairbnb.com/get-the-data.html). Data has been made available
under the Creative Commons CC0 1.0 Universal (CC0 1.0) 
"Public Domain Dedication" license. 

This script downloads the web page into html, extracts the file names 
for the files containing listing information for the United States, then
downloads the files by filename."""
#%%
import os

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

from src.data.file import FileGZDF
from src.analysis.describe import describe_qual, describe_quant
from src.utils.persistence import Persistence
# --------------------------------------------------------------------------- #
#                                DataComponent                                #
# --------------------------------------------------------------------------- #
"""Abstract class that defines the interface for all Data classes."""
class DataComponent(ABC):

    def __init__(self, name, df=None, mutable=False):
        self._datasets = {}
        self._name = name
        self._df = df
        self._description = {}
        self._mutable = mutable    

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

    def __init__(self, name, df=None, mutable=False):
        self._datasets = {}
        self._name = name
        self._df = df
        self._description = {}
        self._mutable = mutable
        
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

    def describe(self, attribute):
        """Returns descriptive statistics for all attributes."""        
        for _, data in self._datasets.items():
            return data.describe(attribute)

    def describe_all(self):
        """Returns descriptive statistics for the attribute indicated."""        
        d = {}
        for name, data in self._datasets.items():
            d[name] = data.describe_all()
        return d


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
    mutable : bool
        Indicates whether the data can be modified.
    """
    _FILE = {'gz': FileGZDF}

    def __init__(self, name, df=None, mutable=False):                
        self._name = name
        self._df = df
        self._description = {}
        self._mutable = mutable

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

    def read(self, filename):
        """Reads the data from the location designated by the filename."""
        filetype = filename.split(".")[-1]
        f = self._FILE.get(filetype)
        df = f.read(filename)
        return df

    def write(self, df, filename):
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

    def remove(self, filename):
        """Removes a file."""
        f = FileGZDF()
        f.remove(filename)
        return self

    def copy(self, frompath, topath):
        """Copies a data object from frompath to topath."""
        self._frompath = frompath
        self._topath = topath
        df = self.read(frompath)
        self.write(df, topath)
        return self

    def move(self, frompath, topath):
        """Moves a dataset from 'frompath' to 'topath' if mutable."""
        if self._mutable:
            self._frompath = frompath
            self._topath = topath
            df = self.read(frompath)
            self.write(df, topath)
        else:
            raise Exception("This data object is immutable and cannot be moved.")
        return self




# --------------------------------------------------------------------------- #
#                              AirbnbData                                     #
# --------------------------------------------------------------------------- #
class AirbnbData(DataComponent):

    _NUMBER = ["float", "float64", "int", "int64"]

    def __init__(self, name, df=None, mutable=False):                
        super(AirbnbData, self).__init__(name=name, df=df, mutable=mutable)

    def get_data(self):
        return self._df

    def add(self, dataset):
        pass

    def remove(self, name):
        pass

    def describe(self, attribute):
        """Returns descriptive statistics for all attributes."""        
        if attribute not in self._df.columns:
            raise ValueError("Attribute {attr} not valid for this data \
                            object.".format(attr=attribute)) 
        if self._df[attribute].dtypes in self._NUMBER:
            self._description = describe_quant(x=self._df[attribute])
        else:
            self._description = describe_qual(x=self._df[attribute])          
        return self._description

    def describe_all(self):
        """Returns descriptive statistics for the attribute indicated."""        
        df_qual = pd.DataFrame()
        df_quant = pd.DataFrame()        
        for col in self._df.columns:            
            if self._df[col].dtypes in self._NUMBER:
                d = describe_quant(x=self._df[col])
                d = pd.DataFrame(d, index=[0]).T
                df_quant = pd.concat([df_quant,d], axis=1)
            else:
                d = describe_qual(x=self._df[col])
                d = pd.DataFrame(d, index=[0]).T
                df_qual = pd.concat([df_qual,d], axis=1)

        self._description[self._name] = {'quant': df_quant, 'qual': df_qual}
        return self._description

# --------------------------------------------------------------------------- #
#                              get_data                                       #
# --------------------------------------------------------------------------- #
def get_data():
    # Directories and filepaths
    directory_cmd_line = "../../data/raw/" 
    directory_interpreter = "./data/raw/" 
    if os.path.isdir(directory_cmd_line):
        directory = directory_cmd_line
    else:
        directory = directory_interpreter

    # Get a list of the files in the directory
    files = os.listdir(directory)

    # Iterate through the filenames, create the DataSet object, read the 
    # data, then add it the object to the DataCollection.
    dc = DataCollection(name="Airbnb")
    df = pd.DataFrame()
    for filename in files:
        filename = os.path.join(directory, filename)
        print("Loading {file} file.".format(file=filename))
        # Extract the city from the filename
        city = filename.split(".")[0]
        f = FileGZDF()
        df = f.read(filename)
        # Create DataSet object
        ds = AirbnbData(name=city, df=df)
        # Add DataSet object to collection
        dc.add(ds)
    
    # Run describe on the collection
    print(dc)
    dc.describe_all()
    return dc
#%%



if __name__ == "__main__":

    data_collection = get_data()
    filename = "./DataCollection"
    p = Persistence()
    p.serialize(data_collection, filename) 

# %%
