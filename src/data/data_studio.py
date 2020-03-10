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
"""Data cleaning, transforming, and analysis for machine learning.

This module includes a Data Object abstraction, support for data cleaning
and preparation as well as analysis and inference capabilities commonly
performed during end-to-end analysis and machine learning projects.

This analysis and modeling framework centers upon three capabilities:
1. Data as Objects : Data organized and managed as objects and metadata
2. Data Curation :  Cleaning, transforming, normalizing and curating 
3. Data Influence : Data-driven learning and change.

Accordingly, the core offering is the Data object model, a composite 
data class that integrates basic analysis and metadata. Data processing and 
development functionality extends the data objects as they move
through the AI process. An analysis and inference module is about
inference, insight, and storytelling.

"""
#%%
from datetime import datetime
import os
from pathlib import Path
import platform
import psutil
import site
import time
import uuid
PROJECT_DIR = Path(__file__).resolve().parents[1]
site.addsitedir(PROJECT_DIR)

from abc import ABC, abstractmethod
from collections import OrderedDict
import pandas as pd
pd.set_option('display.max_columns', None)

from src.analysis.univariate import Describe
from src.data.file_classes import File
from src.utils.system import get_size
from .constants import DTYPES
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

    def __init__(self, path):

        self._id = uuid.uuid4()
        self._name = os.path.basename(path)        
        self._path = path
        self._df = pd.DataFrame()
        self._summary = pd.DataFrame()
    
        # meta data
        self._metadata = {}
        self._metadata['name'] = os.path.basename(path)
        self._metadata['path'] = path
        self._metadata['creator'] = os.getlogin()
        self._metadata['created'] = time.ctime(os.path.getctime(__file__))
        self._metadata['modifier'] = os.getlogin()
        self._metadata['modified'] = time.ctime(os.path.getmtime(__file__))

    def metadata(self):
        """Prints object metadata."""
        print("\n#","="*30,  "Author Information",  "="*30,"#")
        print(f"Id: {self._id}")
        print(f"Creator: {self._creator}")
        print(f"Created: {self._created}")
        print(f"Modifier: {self._modifier}")
        print(f"Modified: {self._modified}")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        return self

    @abstractmethod
    def summarize(self):
        pass

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
    """The Composite of the Data Object Model."""

    def __init__(self, name):
        super(DataCollection, self).__init__(name)
        self._data_collection = OrderedDict()

    def merge_data(self):
        """Merges all DataSets and DataCollections into a single DataFrame."""
        merged = pd.DataFrame()
        for _, data_object in self._data_collection.items():
            df = data_object.get_data()
            merged = pd.concat([merged,df], axis=0)
        return merged


    def metadata(self):
        """Prints DataCollection metadata."""
        super(DataCollection, self).metadata(verbose)
        print("="*30, "DataType Summary", "="*30)
        merged = self._merge_data()
        metadata = pd.DataFrame()
        metadata[self._name] = merged.dtypes.value_counts()
        print(metadata)
        return metadata


    def summarize(self):
        """Descriptive summaries for DataCollection and DataSet objects.
        
        Parameters
        ----------
        verbose : Bool
            True if the summary should be printed.

        Returns
        -------
        Dict : Cointaining quantitative and qualitative descriptive 
               statistics.
        
        """
        describe = Describe()
        df = self.merge_data()
        describe.fit(df)            
        summary = describe.get_analysis()        
    
        print("#","=*35  Quantitative Analysis  35*=","#")
        print(summary['quant'])
        print("#","=*35  Quantitative Analysis  35*=","#")
        print(summary['qual'])            
        return summary

    def get_data(self, name=None):
        """Return all data or the named dataset or collection.
        
        Parameters
        ----------
        name : str
            The name of the DataSet or DataCollection object.
        """
        if name:
            return self._data_collection[name]            
        else:
            return self._data_collection

    def add(self, data):
        """Adds a DataSet or DataCollection object to the collection.
        
        Parameters
        ----------
        dataset : DataSet or DataCollection object.
        """
        name = data.name
        self._data_collection[name] = data
        return self

    def remove(self, name):
        """Removes a DataSet or DataCollection object from the collection."""
        del self._data_collection[name]        
        return self

    def replace_string(self, pattern, replace, columns=None, regex=True):
        """Regex capable, string replace method for DataSet objects.
        
        Parameters
        ----------
        pattern : str
            A (regex) pattern to find in the DataSet or designated columns.
        replace : str
            A string sequence to replace the pattern
        columns : array-like (Optional)
            List of columns to which the replacement should be applied.
        regex : Bool
            Indicates whether the pattern and replacement are valid regex.

        """
        for _, data_object in self._data_collection.items():
            if columns:
                data_object.replace_string(pattern, replace, columns, regex)
            else:
                data_object.replace_string(pattern, replace, regex)
            self._add(data_object)


    def cast_types(self, data_types):
        """Cast objects of the dataframe to designated types."""
        for _, data_object in self._data_collection.items():
            data_object.cast_types(data_types)
            self._add(data_object)


    def import_data(self, directory, columns=None):
        """Creates DataSet objects, imports the data and adds the DataSets.

        Parameters
        ----------
        directory : str
            The directory containing the files to import.
        columns : list
            List of column names to return.
        """

        filenames = os.listdir(directory)
        for filename in filenames:
            name = filename.split(".")[0]
            dataset = DataSet(name=name)            
            path = os.path.join(directory, filename)
            dataset.import_data(filename=path, columns=columns)
            self.add(data=dataset)
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
        for name, dataset in self._data_collection.items():
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
    def __init__(self, name):
        super(DataSet, self).__init__(name)           

    def metadata(self):
        """Prints DataSet metadata."""
        super(DataSet, self).metadata()
        print("#","="*30, "DataType Summary", "="*30,"#")
        metadata = pd.DataFrame()
        metadata[self._name] = self._df.dtypes.value_counts()
        print(metadata)
        print("#","="*30, "DataType Detail", "="*30,"#")                
        metadata = pd.DataFrame()
        metadata[self._name] = self._df.dtypes.T        
        print(metadata)        
        return metadata
    
    def summarize(self, verbose=True):
        """Prints DataSet descriptive statistics."""
        describe = Describe()
        describe.fit(self)
        summary = describe.get_analysis()
        if verbose:
            print("\n#=*35  Quantitative Analysis  35*=#")
            print(summary['quant'])
            print("#=*35  Qualitative Analysis  35*=#")
            print(summary['qual'])            
        return summary        

    def add(self, data):
        pass

    def remove(self, name):
        pass

    def replace_string(self, pattern, replace, columns=None, regex=True):
        """Regex capable, string replace method for DataSet objects.
        
        Parameters
        ----------
        pattern : str
            A (regex) pattern to find in the DataSet or designated columns.
        replace : str
            A string sequence to replace the pattern
        columns : array-like (Optional)
            List of columns to which the replacement should be applied.
        regex : Bool
            Indicates whether the pattern and replacement are valid regex.

        """
        if columns:
            self._df[columns] = self._df[columns].replace({pattern:replace}, regex=regex)
        else:
            self._df = self._df.replace({pattern:replace}, regex=regex)


    def import_data(self, filename, columns=None):
        """Reads the data from filename and appends it to the dataframe member."""
        f = File()
        df = f.read(filename, columns=columns)        
        self._df = pd.concat([self._df, df], axis=0, sort=False)                
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
        if attribute is not None:
            return self._df[attribute]
        return self._df

from .constants import DTYPES


# --------------------------------------------------------------------------- #
#                           TYPE CASTER                                       #
# --------------------------------------------------------------------------- #

class TypeCaster():
    """Type casting, conversions, normalization, standardization, transformation."""
    types = ["BOOL", "CATEGORY", "DATETIME", "FLOAT", "INT", "OBJECT"]


    def cast_bool(self, df, labels):
        """Casts the labeled data as type boolean."""
        for label in labels:
            df[label].astype('bool')
            return df

    def cast_category(self, df, labels):
        """Casts the labeled data as type category."""
        for label in labels:
            df[label].astype('category')
            return df

    def cast_datetime(self, df, labels):
        """Casts the labeled data as type datetime."""
        for label in labels:
            pd.to_datetime(df[[labels]])
            return df
            
    def cast_float(self, df, labels):
        """Casts the labeled data as type float."""
        for label in labels:
            df[label]astype('float')
            return df            

    def cast_int(self, df, labels):
        """Casts the labeled data as type integer."""
        for label in labels:
            df[label]astype('int')
            return df            

    def cast_object(self, df, labels):
        """Casts the labeled data as type integer."""
        for label in labels:
            df[label]astype('object')
            return df            

# --------------------------------------------------------------------------- #
#                           QUANT STUDIO                                      #
# --------------------------------------------------------------------------- #
class QuantStudio(ABC):
    """Abstract base class and interface for the treatment of quantitative data."""

    def __init__(self, name):
        self._id = uuid.uuid4()
        self._name = name
        self._creator = os.getlogin()
        self._created = time.ctime(os.path.getctime(__file__))
        self._modifier = os.getlogin()
        self._modified = time.ctime(os.path.getmtime(__file__))        

    def fit(dataset, y=None):
        pass

    def transform(dataset, y=None):
        pass

    def reverse(dataset, y=None):
        pass


# --------------------------------------------------------------------------- #
#                               RINSE DATA                                    #
# --------------------------------------------------------------------------- #
class RinseData(QuantStudio):
    """Basic hygeine for quantitativae data."""

    def __init__(self, name):
        super(RinseData, self).__init__(name)


    vars = [price,weekly_price, monthly_price,	security_deposit, 
            cleaning_fee,	extra_people]
    df = dataset.get_data()
    for var in vars:
        df[var] = df[var].str.replace(',', '')
        df[var] = df[var].str.replace('$', '')
        df[var] = df[var].str.replace('%', '')
    
    dataset.add(df)

    return dataset



# --------------------------------------------------------------------------- #
#                               DATA SERVER                                   #
# --------------------------------------------------------------------------- #
def serve_data():
    """Serves the data forward during the preliminary inspection."""
    
    for year, directory in Constants.SFO.items():
        
        for filename in os.listdir(directory):           
            
            name = "_".join(filename.split("_")[1:4])
            dataset = DataSet(name=name)
            dataset.import_data(os.path.join(directory, filename))
            dataset = number_rince(dataset)
            dataset = text_rince(dataset)
            dataset = type_cast(dataset)
            dataset = format_data(dataset)
            dataset = select_data(dataset)
            dataset = check_data(dataset)

