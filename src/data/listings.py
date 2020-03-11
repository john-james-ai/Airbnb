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
        """Loads data.

        Parameters
        ----------
        path : str
            A directory containing csv files or path to a single csv file.

        """
        if os.path.isdir(path):
            for directory, _, filenames in os.walk(path):
                for filename in filenames:             
                    df = pd.read_csv(os.path.join(directory, filename), \
                        low_memory=False)
                    self._dataframe = pd.concat([self._dataframe, df], axis=1, sort=False)
        else:        
            self._dataframe = pd.read_csv(path)

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
        # Obtain basic statistics
        summary['Observations'] = self._dataframe.shape[0]
        summary['Variables'] = self._dataframe.shape[1]
        summary['Size (MB)'] = sum(self._dataframe.memory_usage(index=True))/1000000
        
        # Get columns by datatype
        dtypes = self._dataframe.get_dtype_counts()
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

    def describe(self):
        pass



