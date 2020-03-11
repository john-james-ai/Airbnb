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
import os

import numpy as np
import pandas as pd

from ..utils.print import Printer
from ..utils.format import proper
# --------------------------------------------------------------------------- #
#                             DataComponent                                   #
# --------------------------------------------------------------------------- #
class DataComponent(ABC):
    """Abstract base class for DataSet and DataGroup classes."""

    @abstractmethod
    def get_dataframe(self, **kwargs):
        pass

    @abstractmethod
    def load(self, path):
        pass

    @abstractmethod
    def save(self, path):
        pass

    @abstractmethod
    def summarize(self):
        pass

    @abstractmethod
    def describe(self):
        pass

# --------------------------------------------------------------------------- #
#                                DataSet                                      #
# --------------------------------------------------------------------------- #
class DataSet(DataComponent):
    """ Encapsulates a DataFrame object with summary and descriptive statistics."""

    def __init__(self, name):
        self._name = name
        self._dataframe = pd.DataFrame()

    def get_dataframe(self, columns=None, n=None, pct=None, sample='head'):
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
            
        """
        df = self._dataframe()
        if pct and not n:
                n = pct/100 * df.shape[0]
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
                df = df.sample(n)
            else:
                df = df.sample(5)
        return df

    def load(self, path):
        """Loads the dataframe from the a csv file at path.
        
        Parameters
        ----------
        path : str
            The path to the csv file containing the data to be loaded.
        """
        self._dataframe = pd.read_csv(path)
        self._city = proper(os.path.basename(path).split("_")[1:2][0])
        self._date = os.path.basename(path).split("_")[2:3][0]

    def save(self, path):
        """Saves the dataframe to the a csv file at path.
        
        Parameters
        ----------
        path : str
            The path to the csv file containing the data to be saved.
        """
        self._dataframe = pd.to_csv(path)

    def summarize(self, verbose=False):
        """Produces a summary of a dataframe.
        
        Parameters
        ----------
        verbose : bool
            If True, the summary is printed to sys.out.
        """
        summary = {}
        summary['Observations'] = self._dataframe.shape[0]
        summary['Variables'] = self._dataframe.shape[1]
        summary['Size (MB)'] = sum(self._dataframe.memory_usage(index=True))/1000000
        # Get columns by datatype
        dtypes = self._dataframe.get_dtype_counts()
        dtypes_dict = dtypes.to_dict()
        for k, v in dtypes_dict.items():
            summary[k] = v

        if verbose:
            p = Printer()
            p.print_dictionary(content=summary, title="Listings Summary")        

        return summary



# --------------------------------------------------------------------------- #
#                                Airbnb                                       #
# --------------------------------------------------------------------------- #
class Airbnb:
    """An Airbnb listings object.
    
    This class loads individual dataframes, each represented in a single
    csv file, into a single dataframe. It also provides basic summary
    and descriptive statistics.
    """

    def __init__(self):        
        self._dataframe =  pd.DataFrame()
        self._summary = pd.DataFrame()
    
    def summarize(self):        
        summary = {}
        summary['Observations'] = self._dataframe.shape[0]
        summary['Variables'] = self._dataframe.shape[1]-1 # exclude filedate col.
        summary['Size (MB)'] = sum(self._dataframe.memory_usage(index=True))/1000000
        # Get columns by datatype
        dtypes = self._dataframe.get_dtype_counts()
        dtypes_dict = dtypes.to_dict()
        for k, v in dtypes_dict.items():
            summary[k] = v
        p = Printer()
        p.print_dictionary(content=summary, title="Listings Summary")

    def load(self, path):
        """Loads data.

        Parameters
        ----------
        path : str
            A directory containing csv files or path to a single csv file.

        """
        for directory, _, filenames in os.walk(path):
            for filename in filenames:
                date = filename.split("_")[2:3][0]
                df = pd.read_csv(os.path.join(directory, filename), \
                    low_memory=False)
                df['filedate'] = date
                self._dataframe = pd.concat([self._dataframe, df], axis=1, sort=False)

    def save(self, path):
        """Loads data.

        Parameters
        ----------
        path : str
            A path to a single file to which the data is to be saved.

        """
        self._dataframe.to_csv(path, index=False)

