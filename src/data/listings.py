#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : listings.py                                                       #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/airbnb                         #
# --------------------------------------------------------------------------- #
# Created       : Tuesday, March 10th 2020, 5:54:12 pm                        #
# Last Modified : Tuesday, March 10th 2020, 5:54:12 pm                        #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
""" Module for creating a single listings object from multiple files.""" 
from abc import ABC, abstractmethod
import math
import os

import numpy as np
import pandas as pd

from ..analysis.univariate import DescribeQual, DescribeQuant
from ..utils.print import Printer
from ..utils.format import proper
# --------------------------------------------------------------------------- #
#                             DataComponent                                   #
# --------------------------------------------------------------------------- #
class DataComponent(ABC):
    """Abstract base class for DataSet and DataGroup classes."""

    @abstractmethod
    def get_data(self, **kwargs):
        pass

    @abstractmethod
    def load(self, path):
        pass

    @abstractmethod
    def save(self, path):
        pass

    @property
    def name(self):
        return self._name

    @property
    def islocked(self):
        return self._islocked

    @property
    def lock(self):
        self._islocked = True

    @property
    def unlock(self):
        self._islocked = False    
# --------------------------------------------------------------------------- #
#                                DataSet                                      #
# --------------------------------------------------------------------------- #
class DataSet(DataComponent):
    """ Encapsulates a DataFrame object with summary and descriptive statistics.

    Parameters
    ----------
    path : str
        The relative path to the underlying data on disk.
    name : str
        A unique string which identifies the DataSet object.

    Attributes
    ----------
    name : str
        If the name is not provided, it is set to the date extracted from the 
        source path.  If there is no date in the source path, the name is set 
        to the basename of the source path. The name of the DataSet object is used 
        as the key in the DataGroup object, as such the name, once assigned, 
        is immutable.
    source : str
        The relative path to the source of the underlying data on disk. 
    target : str
        The relative path to which the dataframe is saved on disk. 
    islocked : boolean
        True if the source of the data is locked. If the islocked attribute 
        is True, the source is immutable.

    
    """

    def __init__(self, path, name=None):        
        self._name = name or path.split("_")[2:3][0] or os.path.basename(path)
        self._source = path
        self._target = path
        self._islocked = True
        self._dataframe = pd.DataFrame()

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target
      

    def get_data(self, columns=None, n=None, pct=None, sample=None, seed=None):
        """Returns the complete or a part of a dataframe.

        Parameters
        ----------
        columns : None, array-like
            The columns to return                
        n : None or int
            The maximum number of rows to return.
        pct : None or int
            The percentage of rows to return 
        sample : str
            'head' returns the first n (or pct) rows. If n and pct are None, 
            this returns the first five rows
            'tail' returns the last n (or pct) rows. If n and pct are None, 
            this returns the last five rows
            'random' returns random sampling of n (or pct) rows. If n and
            pct are None, this returns a random sampling of 5% of 
            the rows in the dataframe.
        seed : None or integer
            Sets seed for pseudorandom sampling repeatability
            
        """
        if self._dataframe.empty:
            raise Exception("DataSet is empty. Run load method on DataSet object.")

        df = self._dataframe
        if pct and not n:
                n = math.floor(pct/100 * df.shape[0])
        if columns:
            df = df[columns]
        if sample == 'head':
            if n:
                df = df.head(n)
            else:
                df = df.head(5)
        elif sample == 'tail':
            if n:
                df = df.tail(n)
            else:
                df = df.tail(5)                
        elif sample == 'random':
            if n:
                df = df.sample(n, random_state=seed)
            else:
                df = df.sample(frac=.05, random_state=seed)
        return df

    def load(self):
        """Loads data from the source path.
        
        This method can load data from one or multiple csv files into a single
        DataFrame object. If the source parameter is a directory, all data from the 
        underlying files will be loaded into a single DataFrame. Otherwise, the
        DataFrame will contain the data from a single csv file.  
        
        """        
        if os.path.isdir(self._source):
            for directory, _, filenames in os.walk(self._source):
                for filename in filenames:             
                    df = pd.read_csv(os.path.join(directory, filename), \
                        low_memory=False)
                    self._dataframe = pd.concat([self._dataframe, df], axis=1, sort=False)
        else:        
            self._dataframe = pd.read_csv(self._source, low_memory=False)

        return self

    def save(self, path=None, **kwargs):
        """Saves the dataframe to the a csv file.        

        This method accepts a path parameter which may be a directory or a
        relative path including a filename. The DataSet object will also have a 
        source and target file location. The name and location to which the
        file is saved depends upon the path parameter and the current target
        value.

        The path may be a directory or a file path including a filename. If
        the path is a directory, the current target filename is appended to
        the path and the data is saved at that location. Otherwise, the
        data is saved at the filepath designated by the path parameter.

        If there is no path parameter, the data is saved to the current
        target location.
                
        Parameters
        ----------
        path : str (Optional)
            A directory or filename to which the data is to be saved.

        Raises
        ------
        Exception if islocked is True and path is equal to source.

        Note
        ----
        Once the file is saved, the target location is updated to reflect the 
        new location.
        """

        source_dir = os.path.dirname(self._source)
        source_filename = os.path.basename(self._source)

        if path:
            if self._islocked and (self._source == path or source_dir == path):
               raise Exception("'{path}' is locked.".format(path=path))    
            elif os.path.isdir(path):
                self._dataframe.to_csv(os.path.join(path, source_filename))
                self._target = os.path.join(path, source_filename)
            else:
                self._dataframe.to_csv(path)
                self._target = path
        else:
            if self._islocked and (self._target == self._source):
                raise Exception("The source file path is locked. Designate an\
                    alternative location or unlock the source file.")    
            else:
                self._dataframe.to_csv(self._target)                

        return self

    def summarize(self, verbose=False):
        """Produces a summary of a dataframe.
        
        Parameters
        ----------
        verbose : bool
            If True, the summary is printed to sys.out.
        """
        if self._dataframe.empty:
            raise Exception("DataSet is empty. Run load method on DataSet object.")

        summary = {}
        # Obtain basic statistics
        summary['Observations'] = self._dataframe.shape[0]
        summary['Variables'] = self._dataframe.shape[1]
        summary['Size (MB)'] = sum(self._dataframe.memory_usage(index=True))/1000000
        
        # Get columns by datatype
        dtypes = self._dataframe.dtypes.value_counts()
        dtypes_dict = dtypes.to_dict()
        for k, v in dtypes_dict.items():
            summary[k] = v

        # Count missing values
        counts = []
        min_ranges = [0.000, 0.001, 0.051, 0.101, 0.251, 0.501]
        max_ranges = [0.000, 0.050, 0.100, 0.250, 0.500, 1.000]

        missing = self._dataframe.isna().sum() / self._dataframe.shape[0]
        def count_values_in_range(series, min_range, max_range):
            return series.between(left=min_range, right=max_range).sum()

        for min_range, max_range in zip(min_ranges, max_ranges):
            counts.append(count_values_in_range(missing, min_range, max_range))
        
        summary["# Columns with no Missing Values"] = counts[0]
        summary["# Columns with 0 to 5% Missing Values"] = counts[1]
        summary["# Columns with 5% to 10% Missing Values"] = counts[2]
        summary["# Columns with 10% to 25% Missing Values"] = counts[3]
        summary["# Columns with 25% to 50% Missing Values"] = counts[4]
        summary["# Columns with more than 50% Missing Values"] = counts[5]

        if verbose:
            p = Printer()
            p.print_dictionary(content=summary, title="Listings Summary")        

        return summary

    def describe(self, columns=None):
        """Descriptive statistics for quantitative and qualitative variables.""" 
        if self._dataframe.empty:
            raise Exception("DataSet is empty. Run load method on DataSet object.")

        description = {}
        description['quant'] = None
        description['qual'] = None

        if columns:
            df = self._dataframe[columns]
        else:
            df = self._dataframe
        d = DescribeQuant()
        description['quant'] = d.describe(df)            
        d = DescribeQual()
        description['qual'] = d.describe(df)            
        
        return description

# --------------------------------------------------------------------------- #
#                                DataGroup                                    #
# --------------------------------------------------------------------------- #
class DataGroup(DataComponent):

    def __init__(self, name):
        self._name = name
        self._islocked = False
        self._datagroup = {}

    def lock_datasets(self, names=None):
        """Locks the enclosed (or named) DataSet objects.

        Parameters
        ----------
        names : list-like
            The names of the DataSet objects to lock.

        """
        if names:
            for name in names:
                try:
                    self._datagroup[name].lock
                except KeyError:
                    print("DataSet named '{name}' does not exist\
                        in the DataGroup".format(name=name))
        else:
            for name in self._datagroup.keys():
                self._datagroup[name].lock
        
        return self

    def unlock_datasets(self, names=None):
        """Unlocks the enclosed (or named) DataSet objects.

        Parameters
        ----------
        names : list-like
            The names of the DataSet objects to unlock.

        """
        if names:
            for name in names:
                try:
                    self._datagroup[name].unlock
                except KeyError:
                    print("DataSet named '{name}' does not exist\
                        in the DataGroup".format(name=name))
        else:
            for name in self._datagroup.keys():
                self._datagroup[name].unlock
        
        return self

    def get_data(self, names=None):
        """Returns a named (or all) DataSet objects.

        This method returns a dictionary containing one or more
        dataset objects.

        Parameters
        ----------
        names : list-like
            The name or names of the underlying DataSet objects to return.

        Raises
        ------
        Exception if the DataGroup object is empty.

        """
        if len(self._datagroup) == 0:
            raise Exception("DataSet is empty.")

        d = {}
        if names:       
            for name in names:
                try:
                    d[name] = self._datagroup[name]
                except KeyError as e: 
                    print(e)

        else:
            d = self._datagroup
        return d

    def load(self, names=None):
        """Loads the named (or all) contained DataSet objects.

        Parameters
        ----------
        names : str or list-like
            The name or names of the underlying DataSet objects to load.

        Raises
        ------
        Exception if the DataGroup object is empty.

        """        
        if len(self._datagroup) == 0:
            raise Exception("DataSet is empty. Run load method on DataSet object.")

        for name, dataset in self._datagroup.items():
            self._datagroup[name] = dataset.load()

    def save(self, path=None, names=None):
        """Saves enclosed or named DataSet objects.
        
        If the path parameter is provided, it must be a directory. In such case,
        each enclosed DataSet object or objects specified by the names
        parameter, will be saved in the new directory specified by the path 
        parameter in csv format. The filename will remain the same as 
        the current target filename.  
        
        If the path parameter is not provided the data in the enclosed or named
        DataSet objects will be saved at their current target locations in
        csv format.

        """
        if path:
            if os.path.isfile(path):
                raise ValueError("The path parameter must be a directory, not a filename.")   
            if not os.path.exists(path):
                os.mkdir(path)
            for dataset in self._datagroup.values():
                filename = os.path.basename(dataset.target)
                dataset.save(os.path.join(path, filename))            
        else:
            for dataset in self._datagroup.values():
                dataset.save()            

        return self


    def add_dataset(self, dataset):
        """Adds a DataSet object to the DataGroup.
        
        Parameters
        ----------
        dataset : DataSet
            The DataSet object to add to the DataGroup object.

        Raises
        ------
        KeyError if DataSet object of same name exists in DataGroup object.

        """
        name = dataset.name

        if name in self._datagroup.keys():
            raise KeyError("A DataSet object '{name}' already exists in the \
                DataGroup".format(name=name))
        self._datagroup[name] = dataset

        return self

    def add_dataset_from_path(self, path):
        """Adds DataSet objects from files located at path.

        If path is a directory, DataSet objects are created, loaded from the
        path directory and stored in the DataGroup object. Otherwise, if
        the path is a directory to a single file, a single DataSet object
        is created, loaded and added. 

        Parameters
        ----------
        path : str
            A relative directory containing csv files or a path to a single
            file.

        """

        if os.path.isdir(path):
            for directory, _, filenames in os.walk(path):
                for filename in filenames:                     
                    d = DataSet(os.path.join(directory, filename))
                    ds = d.load() 
                    self._datagroup[ds.name] = ds
        else:
            d = DataSet(path)
            ds = d.load() 
            self._datagroup[ds.name] = ds     

        return self

    def change_dataset(self, dataset):
        """Replaces a dataset object of same name with the passed dataset.

        This method is designed to allow a DataSet object with the same name
        as a new DataSet object to be overwritten by the new DataSet object.
        If no DataSet object of the same name exists, the 'add_dataset' method
        is invoked.

        Parameters
        ----------
        dataset : DataSet
            The new DataSet object to replace an existing DataSet object of 
            the same name.

        """
        if dataset.name in self._datagroup.keys():
            self._datagroup[dataset.name] = dataset
        else:
            self._add_dataset(dataset)

        return self

    def remove_dataset(self, dataset):
        """Removes a dataset from the DataGroup object.

        Parameters
        ----------
        dataset : DataSet object
            The DataSet object to be removed.

        Raises
        ------
        KeyError if the DataSet object doesn't exist in the DataGroup object.

        """
        try:
            del self._datagroup[dataset.name]
        except KeyError as e:
            print(e)

        return self


 
           




